#!/usr/bin/env python3
"""
name: earballs
type: script
description: The recording pipeline. Plaud fetch (incremental every 5 min, full reconcile daily) → download → Groq transcription → pyannote diarization + embeddings → voiceprint match → transcript.md / speakers.md / meta.md in recordings/inbox/ → recordings/STATUS.md → watchdog push. Also backfill, reprocess, library rebuild.
why: Architecture §13. Recordings are the main raw input; the pipeline must keep up without anyone watching, and say so loudly when it can't (must-never 10). Ported from v3's tools/earballs (code only) with Sancho's changes: no silence stripping, incremental fetch, ledger in Sancho-Audio, library derived from speakers.md records, three speaker states.
reads: ~/.config/sancho/env (PLAUD_BEARER_TOKEN, PLAUD_BASE_URL, GROQ_API_KEY, HUGGINGFACE_TOKEN); Plaud web API; Sancho-Audio/inbox/; Sancho-Audio/processed/; recordings/**/speakers.md (confirmation records); people/*.md (voiceprint.auto)
writes: Sancho-Audio/processed/<rec_id>.{ogg,json}; Sancho-Audio/voiceprints/; Sancho-Audio/ledger.sqlite (+ ledger-backups/); recordings/inbox/<rec_id>/; recordings/backlog/<era>/<rec_id>/; recordings/STATUS.md; ~/.local/state/sancho/pipeline.*
schedule: sync every 5 min (com.sancho.pipeline); backfill nightly 01:00 (com.sancho.backfill); on demand via pipeline.* commands
test: _setup/tests/pipeline/
"""
from __future__ import annotations

import argparse, datetime as dt, fcntl, hashlib, json, math, os, re, secrets, shutil, socket, sqlite3, subprocess, sys, tempfile, time, wave
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sancho_lib import tree_root, read_frontmatter  # noqa: E402

# ---------------------------------------------------------------- config

ROOT = tree_root()
AUDIO = Path(os.environ.get("SANCHO_AUDIO", Path.home() / "Sync/Sancho-Audio"))
PROCESSED, INBOX_AUDIO = AUDIO / "processed", AUDIO / "inbox"
VOICE_REC, VOICE_SPK = AUDIO / "voiceprints/recordings", AUDIO / "voiceprints/speakers"
LEDGER, BACKUPS = AUDIO / "ledger.sqlite", AUDIO / "ledger-backups"
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho"))
ENV_FILE = Path(os.environ.get("SANCHO_SECRETS_PLAIN", Path.home() / ".config/sancho/env"))
REC_INBOX, REC_BACKLOG = ROOT / "recordings/inbox", ROOT / "recordings/backlog"
STATUS_MD = ROOT / "recordings/STATUS.md"

# Cutover (§13.5): everything from seven days before v3's last known transcript (2026-09-17) is "fresh".
FRESH_START = dt.date(2026, 9, 10)
# Backlog eras by recorded date (§13.2 names them; boundaries are this script's reading, decisions.md 2026-09-30).
ERAS = [("era3", dt.date(2026, 5, 1)), ("era2", dt.date(2026, 3, 1)), ("era1", dt.date(1970, 1, 1))]
PLAUD_DEMO_SERIAL = "04d6a02708c6b8eb77c5f334a92a3cba"  # onboarding demos on every Plaud account (v3)
AUDIO_MAGIC = {b"OggS", b"ID3\x04", b"ID3\x03", b"ID3\x02", b"RIFF", b"fLaC"}
JUNK_MIN_DURATION_S, JUNK_BPS = 30.0, 500  # v3: tiny file claiming a long duration = empty audio

GROQ_URL = os.environ.get("SANCHO_GROQ_URL", "https://api.groq.com/openai/v1/audio/transcriptions")
GROQ_MODEL = "whisper-large-v3"
GROQ_MAX_BYTES = 24 * 1024 * 1024
CHUNK_MINUTES, CHUNK_OVERLAP_S = 18, 2
GROQ_BACKOFF = [2, 8, 30]
BACKFILL_DAILY_AUDIO_S = 6 * 3600  # free-tier drip (§13.2)
MAX_ERRORS = 5
NET_FILE = STATE / "network.json"  # written by _setup/netstate.py each watcher tick; metered → no backfill, no self-heal re-downloads, small list pages, no single download > 50 MB
METERED_MAX_DOWNLOAD = 50 * 1024 * 1024
OPUS_BYTES_PER_S = 4000  # Plaud opus ≈ 32 kbps; used to estimate a download's size before fetching it
RUN_BUDGET_S = 45 * 60

SLA_AMBER_H, SLA_RED_H = 12, 24
SYNC_STALE_H = 2
MIN_FREE_GB = 5

# Speaker rules (§10.2)
SIM_CANDIDATE, SIM_MERGE = 0.70, 0.85
AUTO_SIM, AUTO_SIM_FEW, SOLO_SIM = 0.95, 0.98, 0.90
THIN_REFS, THIN_RECS = 5, 3
MIN_TALK_S = 30.0
DIAR_MODEL = "pyannote/speaker-diarization-3.1"

ST_LISTED, ST_QUEUED, ST_DOWNLOADED, ST_READY, ST_FAILED, ST_JUNK = "listed", "queued", "downloaded", "ready", "failed", "junk"


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).date().isoformat()


def load_env() -> dict:
    env = dict(os.environ)
    if ENV_FILE.exists():
        for ln in ENV_FILE.read_text().splitlines():
            if "=" in ln and not ln.lstrip().startswith("#"):
                k, v = ln.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


ENV = load_env()

# ---------------------------------------------------------------- ledger

SCHEMA = """
CREATE TABLE IF NOT EXISTS recordings (
  id TEXT PRIMARY KEY, plaud_id TEXT UNIQUE, source TEXT NOT NULL DEFAULT 'plaud', era TEXT NOT NULL,
  title TEXT, plaud_metadata TEXT, recorded_at TEXT, duration_seconds REAL,
  audio_path TEXT, size_bytes INTEGER, sha256 TEXT, status TEXT NOT NULL,
  location TEXT, backend TEXT, model TEXT, speakers_detected INTEGER, transcript_version INTEGER DEFAULT 0,
  listed_at TEXT, downloaded_at TEXT, transcribed_at TEXT, diarized_at TEXT, ready_at TEXT,
  error_count INTEGER DEFAULT 0, last_error TEXT, next_try_at TEXT, updated_at TEXT);
CREATE INDEX IF NOT EXISTS ix_status ON recordings(status);
CREATE TABLE IF NOT EXISTS groq_usage (day TEXT PRIMARY KEY, audio_seconds REAL DEFAULT 0, backfill_seconds REAL DEFAULT 0, requests INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, stage TEXT, rec_id TEXT, action TEXT, detail TEXT);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def db() -> sqlite3.Connection:
    AUDIO.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(LEDGER, isolation_level=None, timeout=30)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA journal_mode=DELETE")  # one file: sync.com backs up a whole, consistent ledger
    c.executescript(SCHEMA)
    return c


def audit(c, stage, rec_id, action, detail=""):
    c.execute("INSERT INTO audit (ts, stage, rec_id, action, detail) VALUES (?,?,?,?,?)", (now_utc(), stage, rec_id, action, str(detail)[:2000]))


def meta_get(c, k, default=None):
    r = c.execute("SELECT value FROM meta WHERE key=?", (k,)).fetchone()
    return r[0] if r else default


def meta_set(c, k, v):
    c.execute("INSERT INTO meta (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (k, str(v)))


def upd(c, rec_id, **f):
    f["updated_at"] = now_utc()
    c.execute(f"UPDATE recordings SET {', '.join(k + '=?' for k in f)} WHERE id=?", [*f.values(), rec_id])


def new_rec_id(c) -> str:
    while True:
        rid = "rec_" + secrets.token_hex(5)
        if not c.execute("SELECT 1 FROM recordings WHERE id=?", (rid,)).fetchone():
            return rid


def metered() -> str | None:
    """Metered connection guard (Gordon roaming, 2026-09-30). Returns the network's label while metered."""
    try:
        st = json.loads(NET_FILE.read_text())
        return (st.get("label") or "metered") if st.get("metered") else None
    except (OSError, ValueError):
        return None


def era_for(recorded_at: str | None) -> str:
    if not recorded_at:
        return "era1"
    d = dt.date.fromisoformat(recorded_at[:10])
    if d >= FRESH_START:
        return "fresh"
    for name, start in ERAS:
        if d >= start:
            return name
    return "era1"


# ---------------------------------------------------------------- stage 1: Plaud fetch

class PlaudAuthError(RuntimeError):
    pass


def _requests():
    import requests  # venv
    return requests


def plaud_get(path: str, params: dict | None = None) -> dict:
    r = _requests().get(ENV.get("PLAUD_BASE_URL", "https://api.plaud.ai") + path, params=params or {},
                        headers={"Authorization": f"Bearer {ENV.get('PLAUD_BEARER_TOKEN', '')}"}, timeout=60)
    if r.status_code == 401:
        raise PlaudAuthError("Plaud token expired (401)")
    r.raise_for_status()
    return r.json()


def plaud_list(known: set, full: bool) -> list[dict]:
    """Newest-first by upload. Incremental: stop at the first already-known ID. Full: walk every page."""
    out, skip = [], 0
    limit = 10 if (metered() and not full) else 50
    while True:
        batch = plaud_get("/file/simple/web", {"skip": skip, "limit": limit, "is_trash": 0, "sort_by": "created_at", "is_desc": 1}).get("data_file_list") or []
        for r in batch:
            if r.get("serial_number") == PLAUD_DEMO_SERIAL:
                continue
            if not full and str(r.get("id") or r.get("file_id")) in known:
                return out
            out.append(r)
        if len(batch) < limit:
            return out
        skip += limit


def plaud_recorded_at(r: dict) -> str | None:
    ms = r.get("start_time")
    if not ms:
        return None
    secs = ms / 1000 if ms > 9_999_999_999 else ms
    try:
        return dt.datetime.fromtimestamp(secs, tz=dt.timezone(dt.timedelta(hours=r.get("timezone", 0) or 0))).isoformat()
    except (ValueError, OSError, OverflowError):
        return None


def plaud_duration(r: dict) -> float:
    d = r.get("duration", 0) or 0
    return float(d // 1000) if d > 10000 else float(d)


def stage_fetch(c, full: bool) -> dict:
    """name: fetch · reads: Plaud list API · writes: ledger rows (fresh → queued; older → listed with era)."""
    known = {r[0] for r in c.execute("SELECT plaud_id FROM recordings WHERE plaud_id IS NOT NULL")}
    items = plaud_list(known, full)
    added = {"fresh": 0, "backlog": 0}
    for r in items:
        pid = str(r.get("id") or r.get("file_id"))
        if pid in known:
            continue
        rec_at = plaud_recorded_at(r)
        era = era_for(rec_at)
        c.execute("INSERT OR IGNORE INTO recordings (id, plaud_id, source, era, title, plaud_metadata, recorded_at, duration_seconds, status, listed_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (new_rec_id(c), pid, "plaud", era, r.get("filename") or r.get("fullname"), json.dumps(r), rec_at, plaud_duration(r),
                   ST_QUEUED if era == "fresh" else ST_LISTED, now_utc(), now_utc()))
        known.add(pid)
        added["fresh" if era == "fresh" else "backlog"] += 1
    meta_set(c, "last_list_ok", now_utc())
    if full:
        meta_set(c, "last_full_reconcile", now_utc())
    return added


# ---------------------------------------------------------------- stage 2: download + ingest

def valid_audio(p: Path) -> bool:
    try:
        head = p.open("rb").read(4)
    except OSError:
        return False
    return len(head) == 4 and (head in AUDIO_MAGIC or (head[0] == 0xFF and (head[1] & 0xE0) == 0xE0))


def file_hash(p: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def download(url: str, dest: Path):
    with _requests().get(url, stream=True, timeout=180) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)


def stage_download(c, row) -> bool:
    """name: download · reads: Plaud temp-url API · writes: Sancho-Audio/processed/<rec_id>.<ext> (atomic rename), sha256, status downloaded."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    meta = json.loads(row["plaud_metadata"] or "{}")
    urls = plaud_get(f"/file/temp-url/{row['plaud_id']}", {"is_opus": 1})
    opus, plain = urls.get("temp_url_opus"), urls.get("temp_url")
    if not (opus or plain):
        raise RuntimeError("Plaud returned no download URL")
    tmp = PROCESSED / f".{row['id']}.part"
    ext = ".ogg"
    download(opus or plain, tmp)
    if not valid_audio(tmp) and opus and plain:
        download(plain, tmp)
        ext = ".mp3"
    if not valid_audio(tmp):
        tmp.unlink(missing_ok=True)
        raise ValueError("downloaded file is not audio (tried opus and plain)")
    md5 = (meta.get("file_md5") or "").strip().lower()
    if md5 and ext == ".ogg" and file_hash(tmp, "md5") != md5:
        tmp.unlink(missing_ok=True)
        raise ValueError("MD5 mismatch with Plaud: corrupt download")
    final = PROCESSED / f"{row['id']}{ext}"
    if final.exists():  # never overwrite an original
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"{final.name} already exists; refusing to overwrite")
    os.replace(tmp, final)
    size = final.stat().st_size
    upd(c, row["id"], audio_path=str(final.relative_to(AUDIO)), size_bytes=size, sha256=file_hash(final, "sha256"),
        status=ST_DOWNLOADED, downloaded_at=now_utc(), last_error=None)
    dur = row["duration_seconds"] or 0
    if dur >= JUNK_MIN_DURATION_S and size / dur < JUNK_BPS:
        upd(c, row["id"], status=ST_JUNK, last_error=f"junk: {size} B for {dur:.0f} s ({size / dur:.0f} B/s); Plaud metadata likely bogus")
        audit(c, "download", row["id"], "junk", f"bps={size / dur:.0f}")
    audit(c, "download", row["id"], "downloaded", f"{size} B")
    return True


def stage_inbox(c) -> int:
    """name: inbox · reads: Sancho-Audio/inbox/ (rare non-Plaud audio) · writes: the file moved to processed/<rec_id>.<ext>, ledger row source=external."""
    n = 0
    if not INBOX_AUDIO.exists():
        return 0
    for p in sorted(INBOX_AUDIO.iterdir()):
        if p.name.startswith(".") or not p.is_file() or time.time() - p.stat().st_mtime < 120:
            continue  # still syncing in
        if not valid_audio(p) and p.suffix.lower() not in (".m4a", ".aac", ".opus"):
            continue
        rid = new_rec_id(c)
        rec_at = dt.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat()
        final = PROCESSED / f"{rid}{p.suffix.lower()}"
        PROCESSED.mkdir(parents=True, exist_ok=True)
        os.replace(p, final)
        c.execute("INSERT INTO recordings (id, source, era, title, recorded_at, duration_seconds, audio_path, size_bytes, sha256, status, listed_at, downloaded_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                  (rid, "external", "fresh", p.name, rec_at, ffprobe_duration(final), str(final.relative_to(AUDIO)), final.stat().st_size,
                   file_hash(final, "sha256"), ST_DOWNLOADED, now_utc(), now_utc(), now_utc()))
        audit(c, "inbox", rid, "ingested", p.name)
        n += 1
    return n


# ---------------------------------------------------------------- stage 4: transcription

def ffprobe_duration(p: Path) -> float:
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(p)],
                             capture_output=True, text=True, timeout=60).stdout.strip()
        return float(out)
    except Exception:
        return 0.0


def chunk_audio(p: Path, work: Path) -> list[tuple[float, Path]]:
    dur = ffprobe_duration(p)
    size = p.stat().st_size
    if size <= GROQ_MAX_BYTES or dur <= 0:
        return [(0.0, p)]
    length = CHUNK_MINUTES * 60
    # keep each piece under the byte cap even for high-bitrate files
    length = min(length, max(120, int(dur * GROQ_MAX_BYTES / size * 0.9)))
    step, out = length - CHUNK_OVERLAP_S, []
    for i in range(int(math.ceil(dur / step))):
        start = i * step
        if start >= dur:
            break
        cp = work / f"chunk_{i:03d}{p.suffix}"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.3f}", "-t", str(length), "-i", str(p), "-c", "copy", str(cp)], check=True, timeout=600)
        out.append((float(start), cp))
    return out


class GroqRateLimited(RuntimeError):
    pass


def groq_call(p: Path) -> dict:
    req = _requests()
    last = None
    for attempt, wait in enumerate(GROQ_BACKOFF + [None]):
        with p.open("rb") as f:
            try:
                r = req.post(GROQ_URL, headers={"Authorization": f"Bearer {ENV.get('GROQ_API_KEY', '')}"}, timeout=600,
                             files={"file": (p.name, f)},
                             data=[("model", GROQ_MODEL), ("response_format", "verbose_json"),
                                   ("timestamp_granularities[]", "word"), ("timestamp_granularities[]", "segment")])
            except Exception as e:
                last = f"network: {e}"
                r = None
        if r is not None:
            if r.status_code == 200:
                return r.json()
            last = f"HTTP {r.status_code}: {r.text[:300]}"
            if r.status_code in (400, 401, 403, 413):
                raise RuntimeError(f"Groq refused: {last}")
            if r.status_code == 429 and wait is None:
                raise GroqRateLimited(last)
        if wait is None:
            break
        ra = r.headers.get("retry-after") if r is not None else None
        time.sleep(min(float(ra), 120) if ra and ra.replace(".", "").isdigit() else wait)
    if last and "429" in last:
        raise GroqRateLimited(last)
    raise RuntimeError(f"Groq failed after retries: {last}")


def dedupe_overlap(words: list[dict]) -> list[dict]:
    out = []
    for w in sorted(words, key=lambda w: w.get("start", 0.0)):
        if out and abs(w.get("start", 0) - out[-1].get("start", 0)) < 0.5 and (w.get("word") or "").strip().lower() == (out[-1].get("word") or "").strip().lower():
            continue
        out.append(w)
    return out


def stage_transcribe(c, row, backfill: bool) -> dict:
    """name: transcribe · reads: processed/<rec_id> audio · writes: processed/<rec_id>.json (words, segments), Groq usage in the ledger."""
    audio = AUDIO / row["audio_path"]
    words, segs, texts = [], [], []
    with tempfile.TemporaryDirectory() as td:
        pieces = chunk_audio(audio, Path(td))
        for i, (off, piece) in enumerate(pieces):
            if i:
                time.sleep(3)
            raw = groq_call(piece)
            texts.append(raw.get("text", ""))
            for w in raw.get("words") or []:
                words.append({**w, "start": float(w.get("start", 0)) + off, "end": float(w.get("end", 0)) + off})
            for s in raw.get("segments") or []:
                segs.append({"start": float(s.get("start", 0)) + off, "end": float(s.get("end", 0)) + off, "text": s.get("text", "")})
            c.execute("INSERT INTO groq_usage (day, audio_seconds, backfill_seconds, requests) VALUES (?,0,0,0) ON CONFLICT(day) DO NOTHING", (dt.date.today().isoformat(),))
            secs = float(raw.get("duration") or 0) or (row["duration_seconds"] or 0) / len(pieces)
            c.execute("UPDATE groq_usage SET audio_seconds=audio_seconds+?, backfill_seconds=backfill_seconds+?, requests=requests+1 WHERE day=?",
                      (secs, secs if backfill else 0, dt.date.today().isoformat()))
    if len(pieces) > 1:
        words = dedupe_overlap(words)
    result = {"rec_id": row["id"], "backend": "groq", "model": GROQ_MODEL, "words": words, "segments": segs, "text": " ".join(texts).strip()}
    upd(c, row["id"], backend="groq", model=GROQ_MODEL, transcribed_at=now_utc())
    return result


# ---------------------------------------------------------------- stage 5: diarization + embeddings

class DiarizationUnavailable(RuntimeError):
    pass


def load_wav16k(p: Path):
    import numpy as np
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)], check=True, timeout=1800)
        with wave.open(str(wav)) as w:
            data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype("float32") / 32768.0
    return data


_PIPELINE = None


def diar_pipeline():
    global _PIPELINE
    if _PIPELINE is None:
        try:
            import torch
            from pyannote.audio import Pipeline
        except ImportError as e:
            raise DiarizationUnavailable(f"pyannote not installed: {e}")
        if not ENV.get("HUGGINGFACE_TOKEN"):
            raise DiarizationUnavailable("HUGGINGFACE_TOKEN not set")
        _PIPELINE = Pipeline.from_pretrained(DIAR_MODEL, token=ENV["HUGGINGFACE_TOKEN"])
        try:
            if torch.backends.mps.is_available():
                os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
                _PIPELINE.to(torch.device("mps"))
        except Exception:
            pass
    return _PIPELINE


def stage_diarize(c, row, words: list[dict], num_speakers: int | None) -> dict:
    """name: diarize · reads: audio (decoded by ffmpeg to 16 kHz mono, passed in memory) · writes: voiceprints/recordings/<rec_id>.npy + .labels.json; speaker per word."""
    import numpy as np, torch
    data = load_wav16k(AUDIO / row["audio_path"])
    kw = {"num_speakers": int(num_speakers)} if num_speakers else {}
    out = diar_pipeline()({"waveform": torch.from_numpy(data).unsqueeze(0), "sample_rate": 16000}, **kw)
    ann_full = getattr(out, "speaker_diarization", out)
    ann = getattr(out, "exclusive_speaker_diarization", None) or ann_full
    segs = sorted(({"start": float(t.start), "end": float(t.end), "speaker": str(s)} for t, _, s in ann.itertracks(yield_label=True)), key=lambda s: s["start"])
    emb = getattr(out, "speaker_embeddings", None)
    labels = [str(l) for l in ann_full.labels()]
    if emb is not None and len(labels):
        VOICE_REC.mkdir(parents=True, exist_ok=True)
        np.save(VOICE_REC / f"{row['id']}.npy", np.asarray(emb))
        (VOICE_REC / f"{row['id']}.labels.json").write_text(json.dumps({"labels": labels, "model": DIAR_MODEL}))

    def who(mid: float):
        for s in segs:
            if s["start"] <= mid <= s["end"]:
                return s["speaker"]
        return min(segs, key=lambda s: s["start"] - mid if mid < s["start"] else mid - s["end"])["speaker"] if segs else None

    for w in words:
        w["speaker"] = who((float(w.get("start", 0)) + float(w.get("end", 0))) / 2)
    speakers = sorted({s["speaker"] for s in segs})
    upd(c, row["id"], speakers_detected=len(speakers), diarized_at=now_utc())
    return {"segments": segs, "speakers": speakers}


# ---------------------------------------------------------------- stage 6: speaker match (library derived from speakers.md records)

def cos(a, b) -> float:
    import numpy as np
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    return float(a @ b / (na * nb)) if na and nb else 0.0


def load_library() -> dict:
    f = VOICE_SPK / "_library.json"
    return json.loads(f.read_text()) if f.exists() else {"speakers": {}}


def person_auto(slug: str) -> str:
    fm, _ = read_frontmatter(ROOT / "people" / f"{slug}.md")
    vp = fm.get("voiceprint") if isinstance(fm.get("voiceprint"), dict) else {}
    return str(vp.get("auto") or "paused")


def talk_times(segs: list[dict]) -> dict:
    t: dict = {}
    for s in segs:
        t[s["speaker"]] = t.get(s["speaker"], 0.0) + max(0.0, s["end"] - s["start"])
    return t


def stage_match(row, diar: dict) -> list[dict]:
    """name: match · reads: voiceprints/recordings/<rec_id>.npy, voiceprints/speakers/, people/<slug>.md voiceprint.auto · writes: nothing (returns rows for speakers.md).
    States (§10.2): candidate; machine-confirmed only when the bar is met and no veto fires. Never human-confirmed (must-never 7)."""
    import numpy as np
    tt = talk_times(diar["segments"])
    rows = [{"cluster": s, "talk": tt.get(s, 0.0), "cand": None, "sim": 0.0, "refs": 0, "recs": 0, "confirmed": "", "by": "", "note": ""} for s in diar["speakers"]]
    f = VOICE_REC / f"{row['id']}.npy"
    lib = load_library().get("speakers", {})
    if not f.exists() or not lib:
        for r in rows:
            r["note"] = "no voiceprint library yet" if not lib else "no embeddings saved"
        return rows
    emb = np.load(f)
    labels = json.loads((VOICE_REC / f"{row['id']}.labels.json").read_text())["labels"]
    refs = {slug: np.load(VOICE_SPK / f"{slug}.npy") for slug in lib if (VOICE_SPK / f"{slug}.npy").exists()}
    for r in rows:
        if r["cluster"] not in labels:
            continue
        v = emb[labels.index(r["cluster"])]
        best = max(((max(cos(v, x) for x in np.atleast_2d(m)), slug) for slug, m in refs.items()), default=(0.0, None))
        if best[0] >= SIM_CANDIDATE:
            r.update(cand=best[1], sim=best[0], refs=lib[best[1]]["refs"], recs=lib[best[1]]["recordings"])
    # vetoes and the auto bar
    by_person: dict = {}
    for r in rows:
        if r["cand"]:
            by_person.setdefault(r["cand"], []).append(r)
    solo = len(rows) == 1
    for r in rows:
        if not r["cand"]:
            r["note"] = r["note"] or f"no match ≥ {SIM_CANDIDATE}"
            continue
        thin = r["refs"] < THIN_REFS or r["recs"] < THIN_RECS
        dup = len(by_person[r["cand"]]) > 1
        if dup:
            others = [o for o in by_person[r["cand"]] if o is not r]
            if any(o["sim"] >= SIM_MERGE for o in others) and r["sim"] >= SIM_MERGE:
                r["note"] = f"may be the same speaker as {', '.join(o['cluster'] for o in others)} (both match {r['cand']} ≥ {SIM_MERGE})"
            else:
                r["note"] = f"{r['cand']} also matched by another cluster: no auto-tag"
            continue
        if thin:
            r["note"] = f"{r['cand']} is thin ({r['refs']} refs / {r['recs']} recordings): needs confirmation"
            continue
        if r["talk"] < MIN_TALK_S:
            r["note"] = f"under {MIN_TALK_S:.0f} s of talk: no auto-tag"
            continue
        if solo and r["cand"] == "gordon" and r["sim"] >= SOLO_SIM:
            r.update(confirmed="gordon", by=f"machine: solo rule sim={r['sim']:.2f}")
            continue
        bar = AUTO_SIM if r["refs"] >= THIN_REFS else AUTO_SIM_FEW
        if person_auto(r["cand"]) == "allowed" and r["sim"] >= bar:
            r.update(confirmed=r["cand"], by=f"machine: voiceprint sim={r['sim']:.2f} refs={r['refs']}")
        elif person_auto(r["cand"]) != "allowed":
            r["note"] = f"auto-tag {person_auto(r['cand'])} for {r['cand']}"
    return rows


def rebuild_library() -> dict:
    """name: library · reads: every recordings/**/speakers.md (human-confirmed rows only) + voiceprints/recordings/ · writes: voiceprints/speakers/<slug>.npy, _library.json.
    The records are the truth; the library is derived and rebuilt whole, so an un-enroll is just editing a row (§10.2)."""
    import numpy as np
    acc: dict = {}
    for sp in ROOT.glob("**/speakers.md"):
        if "_quarantine" in sp.parts:
            continue
        fm, body = read_frontmatter(sp)
        rid = str(fm.get("rec_id") or sp.parent.name)
        f = VOICE_REC / f"{rid}.npy"
        if not f.exists():
            continue
        labels = json.loads((VOICE_REC / f"{rid}.labels.json").read_text())["labels"]
        emb = np.load(f)
        for ln in body.splitlines():
            cells = [x.strip() for x in ln.strip().strip("|").split("|")]
            if len(cells) < 6 or not cells[0].startswith("SPEAKER_"):
                continue
            cluster, confirmed, by = cells[0], cells[3], cells[4]
            if not confirmed or confirmed.startswith(("unknown", "ignored", "(")) or not by or by.startswith("machine"):
                continue  # only a human act enrolls (must-never 7)
            if cluster in labels:
                acc.setdefault(confirmed, []).append((rid, emb[labels.index(cluster)]))
    VOICE_SPK.mkdir(parents=True, exist_ok=True)
    lib = {"model": DIAR_MODEL, "built_at": now_utc(), "speakers": {}}
    for slug, items in acc.items():
        np.save(VOICE_SPK / f"{slug}.npy", np.vstack([v for _, v in items]))
        lib["speakers"][slug] = {"refs": len(items), "recordings": len({r for r, _ in items})}
    for old in VOICE_SPK.glob("*.npy"):
        if old.stem not in lib["speakers"]:
            old.rename(old.with_suffix(".retired"))  # never delete (must-never 11)
    (VOICE_SPK / "_library.json").write_text(json.dumps(lib, indent=1))
    return lib


# ---------------------------------------------------------------- stage 7: write transcript, speakers, meta

def hms(s: float) -> str:
    s = int(s)
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def over_cluster(segs: list[dict], n: int, dur: float) -> str:
    """v3's heuristic: clusters with little talk time are usually noise; suggest a count."""
    if n < 2:
        return ""
    tt = talk_times(segs)
    thr = max(30.0, 0.05 * dur)
    anchored = [s for s, t in tt.items() if t >= thr]
    if len(anchored) == len(tt):
        return ""
    if not anchored:
        return f"Diarization unreliable: no cluster has ≥ {thr:.0f} s of speech (heavy overlap?)."
    return f"Over-split suspected: {len(anchored)} of {n} clusters have ≥ {thr:.0f} s of speech; likely {max(2, len(anchored))} speakers. Reprocess with that count if confirmed."


def rel_audio(row) -> str:
    return f"Sancho-Audio/{row['audio_path']}"


def stage_write(c, row, tr: dict, diar: dict | None, sp_rows: list[dict], dest: Path, diar_note: str = "") -> Path:
    """name: write · reads: the transcription and diarization results · writes: <dest>/transcript.md (raw, never rewritten; a reprocess adds transcript.vN.md), speakers.md, meta.md; processed/<rec_id>.json."""
    dest.mkdir(parents=True, exist_ok=True)
    rid = row["id"]
    date = (row["recorded_at"] or now_utc())[:10]
    mins = round((row["duration_seconds"] or 0) / 60)
    n = len(diar["speakers"]) if diar else 0
    ver = (row["transcript_version"] or 0) + 1
    tname = "transcript.md" if ver == 1 and not (dest / "transcript.md").exists() else f"transcript.v{ver}.md"
    (PROCESSED / f"{rid}.json").write_text(json.dumps({**tr, "diarization": diar, "version": ver}, ensure_ascii=False))
    src = f'["[{rid} {date}]"]'
    head = (f"---\nname: Recording {rid} · {(row['recorded_at'] or '')[:16].replace('T', ' ')} · {mins} min\ntype: transcript\n"
            f"description: {row['source'].capitalize()} recording, {mins} min, {n or 'unknown'} speakers detected; raw transcript, not yet ingested\n"
            f"lobe: both\nsources: {src}\nrec_id: {rid}\nrecorded_at: {row['recorded_at']}\nduration_seconds: {row['duration_seconds']}\n"
            f"speakers_detected: {n}\nbackend: {tr['backend']} {tr['model']}\ntranscript_version: {ver}\n---\n")
    body = [f"# {rid} · transcript (raw; never edited; speaker names live in speakers.md)", ""]
    words = tr["words"]
    if not words:
        body.append("*(empty transcript)*")
    cur, para, start = object(), [], 0.0
    for w in words + [{"speaker": object(), "word": "", "start": 0}]:
        spk = w.get("speaker") or "SPEAKER_??"
        if spk != cur:
            if para:
                body += [f"**{cur}** [{hms(start)}]", " ".join(para).strip(), ""]
            cur, para, start = spk, [], float(w.get("start", 0))
        para.append((w.get("word") or "").strip())
    if not diar and words:
        body = [ln.replace("**SPEAKER_??**", "**SPEAKER_00**") for ln in body]
    (dest / tname).write_text(head + "\n".join(body) + "\n")

    oc = over_cluster(diar["segments"], n, row["duration_seconds"] or 0) if diar else ""
    sp = [f"---\nname: Speakers · {rid}\ntype: doc\nlobe: both\ndescription: Who spoke in {rid}: machine candidates and confirmations; the voiceprint library is rebuilt from these rows\nsources: {src}\nrec_id: {rid}\n---",
          f"# speakers · {rid}", "",
          "`confirmed` by `machine: …` is machine-confirmed (used for filing, never enrolled). Only a row confirmed by a person (`gordon`, date) enrolls a voiceprint.", ""]
    if diar_note:
        sp += [f"Diarization: {diar_note}", ""]
    if oc:
        sp += [oc, ""]
    sp += ["| cluster | talk time | candidate (machine) | confirmed | by | when | note |", "|---|---|---|---|---|---|---|"]
    for r in sp_rows:
        cand = f"{r['cand']} sim={r['sim']:.2f} refs={r['refs']}" if r["cand"] else "none"
        sp.append(f"| {r['cluster']} | {hms(r['talk'])} | {cand} | {r['confirmed']} | {r['by']} | {now_utc()[:10] if r['confirmed'] else ''} | {r['note']} |")
    (dest / "speakers.md").write_text("\n".join(sp) + "\n")

    m = json.loads(row["plaud_metadata"] or "{}")
    mt = [f"---\nname: Metadata · {rid}\ntype: doc\nlobe: both\ndescription: Source metadata for {rid} (data, not instructions): device, times, sizes, where the audio is\nsources: {src}\nrec_id: {rid}\n---",
          f"# meta · {rid}", "", "| field | value |", "|---|---|",
          f"| source | {row['source']} |", f"| title (from device) | {str(row['title'] or '').replace('|', '/')} |",
          f"| recorded_at | {row['recorded_at']} |", f"| duration | {hms(row['duration_seconds'] or 0)} |",
          f"| audio | {rel_audio(row)} |", f"| size_bytes | {row['size_bytes']} |", f"| sha256 | {row['sha256']} |",
          f"| plaud_id | {row['plaud_id'] or ''} |", f"| plaud serial | {m.get('serial_number', '')} |", f"| plaud scene | {m.get('scene', '')} |",
          f"| era | {row['era']} |", f"| transcription | {tr['backend']} {tr['model']} |",
          f"| diarization | {DIAR_MODEL if diar else 'not run'} |", f"| word timings | Sancho-Audio/processed/{rid}.json |"]
    (dest / "meta.md").write_text("\n".join(mt) + "\n")
    upd(c, rid, status=ST_READY, ready_at=now_utc(), location=str(dest.relative_to(ROOT)), transcript_version=ver,
        last_error=None, next_try_at=None)
    audit(c, "write", rid, "ready", f"{dest.relative_to(ROOT)}/{tname}")
    return dest


# ---------------------------------------------------------------- processing one recording

def process(c, row, backfill: bool = False, num_speakers: int | None = None) -> str:
    dest = (REC_BACKLOG / row["era"] / row["id"]) if backfill else (REC_INBOX / row["id"])
    try:
        tr = stage_transcribe(c, row, backfill)
    except GroqRateLimited as e:
        upd(c, row["id"], last_error=f"groq rate-limited: {e}", next_try_at=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30)).isoformat())
        audit(c, "transcribe", row["id"], "rate_limited", e)
        return "rate_limited"
    except Exception as e:
        fail(c, row, "transcribe", e)
        return "failed"
    diar, sp_rows, note = None, [], ""
    try:
        diar = stage_diarize(c, row, tr["words"], num_speakers)
        sp_rows = stage_match(row, diar)
    except DiarizationUnavailable as e:
        note = f"not run ({e})"
        audit(c, "diarize", row["id"], "unavailable", e)
    except Exception as e:  # a diarizer crash never loses the transcript
        note = f"failed ({type(e).__name__}: {str(e)[:200]})"
        audit(c, "diarize", row["id"], "error", e)
    stage_write(c, dict(c.execute("SELECT * FROM recordings WHERE id=?", (row["id"],)).fetchone()), tr, diar, sp_rows, dest, note)
    return "ready"


def fail(c, row, stage, e):
    n = (row["error_count"] or 0) + 1
    wait = min(24 * 60, 10 * 2 ** n)
    upd(c, row["id"], error_count=n, last_error=f"{stage}: {type(e).__name__}: {str(e)[:500]}",
        next_try_at=(dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=wait)).isoformat(),
        status=ST_FAILED if n >= MAX_ERRORS else row["status"])
    audit(c, stage, row["id"], "error", f"{type(e).__name__}: {e}")


def due(row) -> bool:
    return not row["next_try_at"] or row["next_try_at"] <= dt.datetime.now(dt.timezone.utc).isoformat()


# ---------------------------------------------------------------- commands

def lock(name: str):
    STATE.mkdir(parents=True, exist_ok=True)
    f = open(STATE / f"{name}.lock", "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"earballs: another {name} run is going; exiting")
        sys.exit(0)
    return f


def online() -> bool:
    from urllib.parse import urlparse
    try:
        socket.gethostbyname(urlparse(ENV.get("PLAUD_BASE_URL", "https://api.plaud.ai")).hostname or "api.plaud.ai")
        return True
    except OSError:
        return False


def cmd_sync(a) -> int:
    _l = lock("pipeline")
    c = db()
    t0 = time.time()
    msgs = []
    if not online():
        meta_set(c, "last_sync_attempt", now_utc())
        meta_set(c, "network", "offline")
        print("earballs: offline; nothing to do (a known state, not a failure)")
        write_status(c)
        return 0
    meta_set(c, "network", "online")
    meta_set(c, "last_sync_attempt", now_utc())
    if not ENV.get("PLAUD_BEARER_TOKEN"):
        meta_set(c, "token_state", "missing")
    else:
        full = a.full or (meta_get(c, "last_full_reconcile", "") or "")[:10] != dt.date.today().isoformat()
        try:
            added = stage_fetch(c, full)
            meta_set(c, "token_state", "ok")
            msgs.append(f"{'full' if full else 'incremental'} list: {added['fresh']} new fresh, {added['backlog']} new backlog")
        except PlaudAuthError:
            meta_set(c, "token_state", "expired")
            msgs.append("Plaud token expired")
        except Exception as e:
            meta_set(c, "last_list_error", f"{now_utc()} {e}")
            msgs.append(f"Plaud list failed: {e}")
        if meta_get(c, "token_state") == "ok":
            for row in c.execute("SELECT * FROM recordings WHERE status=? ORDER BY recorded_at", (ST_QUEUED,)).fetchall():
                if not due(row):
                    continue
                if metered() and (row["duration_seconds"] or 0) * OPUS_BYTES_PER_S > METERED_MAX_DOWNLOAD:
                    upd(c, row["id"], last_error=f"waiting for unmetered network (~{(row['duration_seconds'] or 0) * OPUS_BYTES_PER_S / 1048576:.0f} MB)")
                    continue
                try:
                    stage_download(c, row)
                except PlaudAuthError:
                    meta_set(c, "token_state", "expired")
                    break
                except Exception as e:
                    fail(c, row, "download", e)
            if full and not metered():
                heal(c)
    n_in = stage_inbox(c)
    if n_in:
        msgs.append(f"{n_in} file(s) from the audio inbox")
    done = {"ready": 0, "failed": 0, "rate_limited": 0}
    if ENV.get("GROQ_API_KEY"):
        rows = c.execute("SELECT * FROM recordings WHERE status=? AND era='fresh' ORDER BY recorded_at", (ST_DOWNLOADED,)).fetchall()
        for row in rows:
            if time.time() - t0 > RUN_BUDGET_S:
                break
            if not due(row):
                continue
            st = process(c, row)
            done[st] = done.get(st, 0) + 1
            write_status(c)  # a long run shouldn't leave STATUS.md stale
            if st == "rate_limited":
                break
    msgs.append(f"processed: {done['ready']} ready, {done['failed']} failed" + (", Groq rate-limited" if done["rate_limited"] else ""))
    backup(c)
    write_status(c)
    watchdog(c)
    print("earballs sync: " + "; ".join(msgs))
    return 0


def heal(c):
    """Full reconcile: a ledger row whose audio vanished is re-downloaded (v3's self-heal)."""
    for row in c.execute("SELECT * FROM recordings WHERE source='plaud' AND audio_path IS NOT NULL").fetchall():
        if not (AUDIO / row["audio_path"]).exists():
            audit(c, "heal", row["id"], "audio_missing", row["audio_path"])
            try:
                p = AUDIO / row["audio_path"]
                urls = plaud_get(f"/file/temp-url/{row['plaud_id']}", {"is_opus": 1})
                tmp = p.with_name(f".{p.name}.part")
                download(urls.get("temp_url_opus") or urls.get("temp_url"), tmp)
                if valid_audio(tmp):
                    os.replace(tmp, p)
                    audit(c, "heal", row["id"], "restored", p.name)
            except Exception as e:
                audit(c, "heal", row["id"], "failed", e)


def cmd_backfill(a) -> int:
    _l = lock("pipeline")
    c = db()
    if not online():
        print("earballs backfill: offline")
        return 0
    if metered() and not a.force:
        print(f"earballs backfill: refused; metered network ({metered()}); backlog audio is bulk data. --force overrides.")
        write_status(c)
        return 0
    eras = ["era3", "era2", "era1"] if a.era == "auto" else [a.era]
    today = dt.date.today().isoformat()
    n = 0
    for era in eras:
        rows = c.execute("SELECT * FROM recordings WHERE era=? AND status IN (?,?) ORDER BY recorded_at DESC", (era, ST_LISTED, ST_DOWNLOADED)).fetchall()
        for row in rows:
            if n >= a.limit:
                break
            used = (c.execute("SELECT backfill_seconds FROM groq_usage WHERE day=?", (today,)).fetchone() or [0])[0]
            if used + (row["duration_seconds"] or 0) > BACKFILL_DAILY_AUDIO_S:
                print(f"earballs backfill: daily cap reached ({used / 3600:.1f} of {BACKFILL_DAILY_AUDIO_S / 3600:.0f} audio-hours)")
                write_status(c)
                return 0
            if not due(row):
                continue
            try:
                if row["status"] == ST_LISTED:
                    stage_download(c, row)
                    row = c.execute("SELECT * FROM recordings WHERE id=?", (row["id"],)).fetchone()
                    if row["status"] != ST_DOWNLOADED:
                        continue
            except Exception as e:
                fail(c, row, "download", e)
                continue
            st = process(c, row, backfill=True)
            n += st == "ready"
            if st == "rate_limited":
                break
    write_status(c)
    print(f"earballs backfill: {n} recording(s) to recordings/backlog/")
    return 0


def cmd_reprocess(a) -> int:
    """Re-diarize with a fixed speaker count (ingest's "were there three of you?"); reuses the word JSON, writes transcript.vN.md."""
    _l = lock("pipeline")
    c = db()
    row = c.execute("SELECT * FROM recordings WHERE id=?", (a.rec_id,)).fetchone()
    if not row or not row["location"]:
        print(f"earballs reprocess: {a.rec_id} is not ready yet")
        return 1
    tr = json.loads((PROCESSED / f"{a.rec_id}.json").read_text())
    tr = {k: tr[k] for k in ("rec_id", "backend", "model", "words", "segments", "text")}
    diar = stage_diarize(c, row, tr["words"], a.num_speakers)
    row = c.execute("SELECT * FROM recordings WHERE id=?", (a.rec_id,)).fetchone()
    old = ROOT / row["location"] / "speakers.md"
    if old.exists():
        old.rename(old.with_name(f"speakers.v{row['transcript_version']}.md"))  # supersede, never overwrite
    stage_write(c, row, tr, diar, stage_match(row, diar), ROOT / row["location"], f"re-run with {a.num_speakers} speakers")
    write_status(c)
    print(f"earballs reprocess: {a.rec_id} re-diarized with {a.num_speakers} speakers")
    return 0


def cmd_library(a) -> int:
    lib = rebuild_library()
    print(f"earballs library: {len(lib['speakers'])} people, {sum(s['refs'] for s in lib['speakers'].values())} references")
    return 0


def cmd_status(a) -> int:
    c = db()
    write_status(c)
    print(STATUS_MD.read_text())
    return 0


# ---------------------------------------------------------------- stage 8: STATUS.md · stage 10: watchdog · stage 11: backup

def hours_since(iso: str | None) -> float | None:
    if not iso:
        return None
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if t.tzinfo is None:
        t = t.astimezone()
    return (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600


def problems(c) -> list[tuple[str, str, str]]:
    """(level, code, one plain actionable line). Offline and asleep are known states, not failures (§13.1 stage 10)."""
    out = []
    tok = meta_get(c, "token_state", "unknown")
    if tok == "expired":
        out.append(("critical", "token", "Plaud token expired; re-capture it from app.plaud.ai and update the secrets."))
    elif tok == "missing":
        out.append(("critical", "token", "No Plaud token in the secrets file."))
    if not ENV.get("GROQ_API_KEY"):
        out.append(("critical", "groq", "No Groq key; nothing can be transcribed."))
    lo = hours_since(meta_get(c, "last_list_ok"))
    if meta_get(c, "network") == "online" and tok == "ok" and lo is not None and lo > SYNC_STALE_H:
        out.append(("critical" if lo > 24 else "warn", "sync", f"Plaud hasn't answered since {meta_get(c, 'last_list_ok')[:16]}."))
    waiting = c.execute("SELECT id, downloaded_at, listed_at FROM recordings WHERE era='fresh' AND status IN (?,?) ORDER BY listed_at", (ST_QUEUED, ST_DOWNLOADED)).fetchall()
    if waiting:
        h = hours_since(waiting[0]["listed_at"]) or 0
        if h > SLA_AMBER_H:
            day = dt.datetime.fromisoformat(waiting[0]["listed_at"].replace("Z", "+00:00")).astimezone().strftime("%a %-m/%-d")
            out.append(("critical" if h > SLA_RED_H else "warn", "sla", f"{len(waiting)} recording(s) waiting; oldest since {day}."))
    stuck = c.execute("SELECT COUNT(*) FROM recordings WHERE status=?", (ST_FAILED,)).fetchone()[0]
    if stuck:
        out.append(("warn", "failed", f"{stuck} recording(s) failed {MAX_ERRORS} times; see recordings/STATUS.md."))
    try:
        free = shutil.disk_usage(AUDIO).free / 1024 ** 3
        if free < MIN_FREE_GB:
            out.append(("critical", "disk", f"Only {free:.0f} GB free for audio."))
    except OSError:
        pass
    bh = hours_since(meta_get(c, "last_backup"))
    if bh is not None and bh > 48:
        out.append(("warn", "backup", "Ledger backup is over two days old."))
    return out


def watchdog(c):
    """CRITICAL → push (notify.py dedupes: on change, then at most daily). Recovery after a critical → one info push."""
    probs = problems(c)
    crit = [p for p in probs if p[0] == "critical"]
    was = meta_get(c, "watchdog_state", "green")
    notify = ROOT / "_setup" / "notify.py"
    env = {**os.environ, **{k: v for k, v in ENV.items() if k.startswith("PUSHOVER")}}
    if crit:
        msg = "Pipeline: " + " ".join(p[2] for p in crit)
        subprocess.run([sys.executable if sys.executable else "python3", str(notify), "warn", msg, "--key=pipeline"], env=env, capture_output=True, timeout=30)
        meta_set(c, "watchdog_state", "red")
    else:
        if was == "red":
            subprocess.run(["python3", str(notify), "info", "Pipeline back to green.", "--key=pipeline"], env=env, capture_output=True, timeout=30)
        meta_set(c, "watchdog_state", "amber" if probs else "green")


def backup(c):
    if (meta_get(c, "last_backup", "") or "")[:10] == dt.date.today().isoformat():
        return
    BACKUPS.mkdir(parents=True, exist_ok=True)
    target = BACKUPS / f"ledger.{dt.date.today().isoformat()}.sqlite"
    dst = sqlite3.connect(target)
    c.backup(dst)
    dst.close()
    for old in sorted(BACKUPS.glob("ledger.*.sqlite"))[:-7]:
        old.unlink()  # rotating copies of state, not knowledge
    meta_set(c, "last_backup", now_utc())


def reconcile_locations(c):
    """Ingest moves a recording's folder out of recordings/inbox/ (§3.5). Follow it so the ledger always knows where each rec_id lives."""
    for r in c.execute("SELECT id, location FROM recordings WHERE status=? AND location IS NOT NULL", (ST_READY,)).fetchall():
        if (ROOT / r["location"]).is_dir():
            continue
        hits = [p for p in ROOT.rglob(f"*{r['id']}") if p.is_dir() and ".git" not in p.parts and "_quarantine" not in p.parts]
        if len(hits) == 1:
            upd(c, r["id"], location=str(hits[0].relative_to(ROOT)))
            audit(c, "locate", r["id"], "moved", f"{r['location']} → {hits[0].relative_to(ROOT)}")
        else:
            audit(c, "locate", r["id"], "not_found" if not hits else "ambiguous", ", ".join(str(h) for h in hits)[:500])


def write_status(c):
    """name: status · reads: the ledger, recordings/inbox/ · writes: recordings/STATUS.md (generated; the greeting's pipeline line); ledger locations of filed recordings."""
    reconcile_locations(c)
    probs = problems(c)
    level = "RED" if any(p[0] == "critical" for p in probs) else "AMBER" if probs else "GREEN"
    counts = {r[0]: r[1] for r in c.execute("SELECT status, COUNT(*) FROM recordings WHERE era='fresh' GROUP BY status")}
    inbox = sorted(p.name for p in REC_INBOX.iterdir() if p.is_dir() and p.name.startswith("rec_")) if REC_INBOX.exists() else []
    oldest = c.execute(f"SELECT id, recorded_at FROM recordings WHERE id IN ({','.join('?' * len(inbox))}) ORDER BY recorded_at LIMIT 1", inbox).fetchone() if inbox else None
    today = dt.date.today().isoformat()
    g = c.execute("SELECT audio_seconds, backfill_seconds, requests FROM groq_usage WHERE day=?", (today,)).fetchone() or (0, 0, 0)
    eras = c.execute("SELECT era, status, COUNT(*), SUM(duration_seconds) FROM recordings WHERE era!='fresh' GROUP BY era, status").fetchall()
    down = c.execute("SELECT COALESCE(SUM(size_bytes),0) FROM recordings WHERE downloaded_at LIKE ?", (today_utc() + "%",)).fetchone()[0]
    up = c.execute("SELECT COALESCE(SUM(size_bytes),0) FROM recordings WHERE transcribed_at LIKE ?", (today_utc() + "%",)).fetchone()[0]
    stuck = c.execute("SELECT id, status, last_error FROM recordings WHERE status=? OR (error_count>0 AND status NOT IN (?,?)) ORDER BY updated_at DESC LIMIT 10", (ST_FAILED, ST_READY, ST_JUNK)).fetchall()
    L = ["# recordings · STATUS", f"generated {dt.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')} by earballs.py · pipeline {level}", ""]
    L += [f"**{level}**" + (": " + " ".join(p[2] for p in probs) if probs else ": keeping up."), ""]
    L += [f"- waiting for ingest (recordings/inbox/): {len(inbox)}" + (f"; oldest {oldest['id']} recorded {str(oldest['recorded_at'])[:16].replace('T', ' ')}" if oldest else ""),
          f"- fresh in the pipeline: {counts.get(ST_QUEUED, 0)} to download, {counts.get(ST_DOWNLOADED, 0)} to transcribe, {counts.get(ST_READY, 0)} ready in total, {counts.get(ST_JUNK, 0)} junk",
          f"- last Plaud list: {(meta_get(c, 'last_list_ok') or 'never')[:16]} · last full reconcile: {(meta_get(c, 'last_full_reconcile') or 'never')[:16]} · token: {meta_get(c, 'token_state', 'unknown')} · network: {meta_get(c, 'network', 'unknown')}",
          f"- Groq today: {g[0] / 3600:.1f} audio-hours in {g[2]} requests ({g[1] / 3600:.1f} h backfill of {BACKFILL_DAILY_AUDIO_S / 3600:.0f} h cap)",
          f"- voiceprint library: {len(load_library().get('speakers', {}))} people · diarization: {DIAR_MODEL}",
          f"- ledger backup: {(meta_get(c, 'last_backup') or 'never')[:16]}",
          f"- data today: {down / 1048576:.0f} MB audio downloaded, {up / 1048576:.0f} MB sent to Groq (sync.com backs the audio up again)"
          + (f" · **metered network ({metered()}): backfill, bulk re-downloads and downloads over 50 MB wait**" if metered() else ""), ""]
    if eras:
        L += ["## Backlog", "", "| era | status | recordings | audio hours |", "|---|---|---|---|"]
        L += [f"| {e[0]} | {e[1]} | {e[2]} | {(e[3] or 0) / 3600:.0f} |" for e in eras] + [""]
    if stuck:
        L += ["## Needs attention", ""] + [f"- {s['id']} ({s['status']}): {str(s['last_error'] or '')[:160]}" for s in stuck] + [""]
    STATUS_MD.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATUS_MD.with_name(".STATUS.md.tmp")
    tmp.write_text("\n".join(L))
    os.replace(tmp, STATUS_MD)


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="earballs")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync"); s.add_argument("--full", action="store_true"); s.set_defaults(fn=cmd_sync)
    b = sub.add_parser("backfill"); b.add_argument("--era", default="auto", choices=["auto", "era3", "era2", "era1"]); b.add_argument("--limit", type=int, default=50); b.add_argument("--force", action="store_true"); b.set_defaults(fn=cmd_backfill)
    r = sub.add_parser("reprocess"); r.add_argument("rec_id"); r.add_argument("--num-speakers", type=int, required=True); r.set_defaults(fn=cmd_reprocess)
    sub.add_parser("library").set_defaults(fn=cmd_library)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
