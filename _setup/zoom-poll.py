#!/usr/bin/env python3
"""
name: zoom-poll
type: command
description: Poll Zoom cloud recordings (Server-to-Server OAuth). Per meeting: download the VTT transcript and the audio-only M4A into Sancho-Audio/zoom/<YYYY-MM-DD>_<topic-slug>/, leave the MP4 to `zoom.video` (a heavy command, so it waits for an unmetered network), and land the VTT as a recording in recordings/inbox/<rec_id>/ (transcript.md, speakers.md, meta.md, ledger row, source zoom) with Zoom's participant names kept verbatim as the speaker labels. No Groq when a VTT exists; a meeting with no VTT after VTT_GRACE_H hours goes to the normal pipeline stages by its M4A. Without credentials: prints "zoom: not configured", exits 0, and asks once in _setup/MAC-SETUP.md.
why: Architecture §13.6. Zoom's transcript carries participant names, which is better than any diarizer; Gordon wants the transcripts and the recordings pulled without anyone remembering to. A name is still only a machine candidate (must-never 7); the ingest skill confirms.
reads: ~/.config/sancho/env (ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET; optional ZOOM_USER); Zoom API (oauth/token, users/<user>/recordings, meetings/<uuid>/recordings, download URLs); people/*.md (name, aliases); ~/.local/state/sancho/network.json
writes: Sancho-Audio/zoom/<date>_<slug>/; Sancho-Audio/ledger.sqlite (recordings, zoom_meetings, zoom_files, meta zoom_*); recordings/inbox/<rec_id>/; recordings/STATUS.md; _setup/MAC-SETUP.md (one line, once); _queue/requests/ (zoom.video when an MP4 is waiting)
schedule: every 15 min: the 5-minute pipeline sync enqueues zoom.poll (earballs.py zoom_schedule); zoom.video is queued by zoom.poll
test: _setup/tests/zoom-poll/
"""
from __future__ import annotations

import base64, datetime as dt, json, os, re, socket, sys, time, unicodedata, urllib.error, urllib.request
from pathlib import Path
from urllib.parse import quote, urlencode, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "pipeline"))
import earballs as eb  # noqa: E402  (stdlib at import; the ledger, rec_ ids, STATUS.md and the metered flag live there)
from sancho_lib import read_frontmatter, enqueue  # noqa: E402

ROOT, ENV = eb.ROOT, eb.ENV
ZOOM_DIR = eb.AUDIO / "zoom"
API = ENV.get("ZOOM_API_BASE", "https://api.zoom.us/v2").rstrip("/")
TOKEN_URL = ENV.get("ZOOM_TOKEN_URL", "https://zoom.us/oauth/token")
USER = ENV.get("ZOOM_USER", "me")
SETUP_MD = ROOT / "_setup" / "MAC-SETUP.md"
SETUP_MARK = "Zoom is not configured"  # the one line's fixed words; present = already asked
CRED = ("ZOOM_ACCOUNT_ID", "ZOOM_CLIENT_ID", "ZOOM_CLIENT_SECRET")

FIRST_LOOKBACK_DAYS = 30   # first poll; also Zoom's widest list window
OVERLAP_DAYS = 7           # later polls re-list a week: transcripts finish after the meeting does
VTT_GRACE_H = 3            # no transcript this long after the meeting ended → Groq by the M4A
RETRY_FAILED_MIN = 60      # a file that failed to download is tried again after this
VIDEO_BUDGET_S = 40 * 60   # zoom.video starts no new download after this
EXT = {"TRANSCRIPT": ".vtt", "M4A": ".m4a", "MP4": ".mp4"}
NO_LABEL = "(no label)"


class ZoomError(RuntimeError):
    pass


# ---------------------------------------------------------------- network (one door; the test replaces _open)

class _NoAuthOnRedirect(urllib.request.HTTPRedirectHandler):
    """Zoom's download URL redirects to a signed URL; the bearer token never follows to another host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urlparse(newurl).hostname != urlparse(req.full_url).hostname:
            new.headers.pop("Authorization", None)
            new.unredirected_hdrs.pop("Authorization", None)
        return new


_OPENER = urllib.request.build_opener(_NoAuthOnRedirect)


def _open(url: str, headers: dict | None = None, data: bytes | None = None, method: str = "GET", timeout: int = 120):
    return _OPENER.open(urllib.request.Request(url, data=data, headers=headers or {}, method=method), timeout=timeout)


def _json(url: str, headers: dict, method: str = "GET") -> dict:
    try:
        with _open(url, headers, b"" if method == "POST" else None, method) as r:
            return json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", "replace")[:300]
        except Exception:
            detail = ""
        raise ZoomError(f"HTTP {e.code} from {urlparse(url).path}: {detail}") from None
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise ZoomError(f"{urlparse(url).path}: {e}") from None


def token() -> str:
    basic = base64.b64encode(f"{ENV['ZOOM_CLIENT_ID']}:{ENV['ZOOM_CLIENT_SECRET']}".encode()).decode()
    r = _json(f"{TOKEN_URL}?{urlencode({'grant_type': 'account_credentials', 'account_id': ENV['ZOOM_ACCOUNT_ID']})}",
              {"Authorization": f"Basic {basic}"}, "POST")
    if not r.get("access_token"):
        raise ZoomError("Zoom gave no access token; check the Server-to-Server app's three values")
    return r["access_token"]


def api(path: str, tok: str, params: dict | None = None) -> dict:
    return _json(f"{API}{path}" + (f"?{urlencode(params)}" if params else ""), {"Authorization": f"Bearer {tok}"})


def list_meetings(tok: str, since: dt.date) -> list[dict]:
    """Every cloud recording from `since` to today, in 30-day windows (Zoom's limit), all pages."""
    out, start, today = [], since, dt.datetime.now(dt.timezone.utc).date()
    while start <= today:
        end = min(today, start + dt.timedelta(days=29))
        page = ""
        while True:
            p = {"from": start.isoformat(), "to": end.isoformat(), "page_size": 300}
            if page:
                p["next_page_token"] = page
            r = api(f"/users/{quote(USER, safe='')}/recordings", tok, p)
            out += r.get("meetings") or []
            page = r.get("next_page_token") or ""
            if not page:
                break
        start = end + dt.timedelta(days=1)
    return list({m["uuid"]: m for m in out if m.get("uuid")}.values())


def meeting_recordings(tok: str, uuid: str) -> dict:
    enc = quote(uuid, safe="")
    if uuid.startswith("/") or "//" in uuid:
        enc = quote(enc, safe="")  # Zoom wants these double-encoded
    return api(f"/meetings/{enc}/recordings", tok)


def online() -> bool:
    try:
        socket.gethostbyname(urlparse(API).hostname or "api.zoom.us")
        return True
    except OSError:
        return False


def valid(kind: str, p: Path) -> bool:
    head = p.open("rb").read(12)
    return head.lstrip(b"\xef\xbb\xbf").startswith(b"WEBVTT") if kind == "TRANSCRIPT" else head[4:8] == b"ftyp"


def download(url: str, tok: str, dest: Path, kind: str):
    """Atomic: .part, check it is what it claims, rename. An existing file is never overwritten."""
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(f".{dest.name}.part")
    try:
        with _open(url, {"Authorization": f"Bearer {tok}"}, timeout=300) as r, tmp.open("wb") as f:
            for chunk in iter(lambda: r.read(1 << 16), b""):
                f.write(chunk)
        if not valid(kind, tmp):
            raise ValueError(f"download is not a {EXT[kind]} file")
        os.replace(tmp, dest)
    finally:
        tmp.unlink(missing_ok=True)


# ---------------------------------------------------------------- setup line (asked once)

def configured() -> bool:
    return all(ENV.get(k) for k in CRED)


def note_setup() -> bool:
    """One line in MAC-SETUP.md saying what Gordon creates at Zoom. Returns True if written now, False if already there."""
    old = SETUP_MD.read_text(encoding="utf-8") if SETUP_MD.exists() else ""
    if SETUP_MARK in old:
        return False
    line = (f"- **{SETUP_MARK} (zoom.poll, {dt.date.today().isoformat()}).** What Gordon creates at marketplace.zoom.us: a Server-to-Server OAuth app "
            "with the scope `recording:read:admin` (or the user-level `recording:read`), activated. Its Account ID, Client ID and Client Secret go into the secrets as "
            "`ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET` (`sancho.unlock`, edit `~/.config/sancho/env`, `sancho.lock-secrets`). The Zoom account also needs "
            "cloud recording and the audio transcript switched on. Until the three values exist, `zoom.poll` does nothing; once they do, it starts on its own within 15 minutes.")
    SETUP_MD.parent.mkdir(parents=True, exist_ok=True)
    tmp = SETUP_MD.with_name(".MAC-SETUP.md.tmp")
    tmp.write_text(old + ("" if old.endswith("\n") or not old else "\n") + line + "\n", encoding="utf-8")
    os.replace(tmp, SETUP_MD)
    return True


# ---------------------------------------------------------------- the VTT

_TS = r"(?:(\d+):)?(\d\d):(\d\d)[.,](\d{3})"
TIMING = re.compile(_TS + r"\s*-->\s*" + _TS)
LABEL = re.compile(r"^([^:<>]{1,60}?):\s+(.*)$", re.S)
VOICE = re.compile(r"^<v(?:\.[^ >]*)?\s+([^>]+)>(.*)$", re.S)


def _secs(h, m, s, ms) -> float:
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_vtt(text: str, offset: float = 0.0) -> list[dict]:
    """Cues as {start, end, speaker, text}. The speaker is the participant label Zoom put before the first colon
    (or a <v Name> tag), verbatim. A cue without one gets speaker None. A would-be label seen only once in a file
    that also has unlabelled cues is treated as spoken text ("Note: …"), so no participant is invented."""
    cues = []
    for block in re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n")):
        lines = block.strip().split("\n")
        i = next((n for n, ln in enumerate(lines) if TIMING.search(ln)), None)
        if i is None:
            continue
        g = TIMING.search(lines[i]).groups()
        body = " ".join(ln.strip() for ln in lines[i + 1:]).strip()
        if not body:
            continue
        v, m = VOICE.match(body), LABEL.match(body)
        if v:
            who, said = v.group(1).strip(), re.sub(r"</?v[^>]*>", "", v.group(2)).strip()
        elif m and len(m.group(1).split()) <= 6:
            who, said = m.group(1).strip(), m.group(2).strip()
        else:
            who, said = None, body
        cues.append({"start": _secs(*g[:4]) + offset, "end": _secs(*g[4:]) + offset, "speaker": who, "text": said, "raw": body})
    if any(c["speaker"] is None for c in cues):
        seen: dict = {}
        for c in cues:
            seen[c["speaker"]] = seen.get(c["speaker"], 0) + 1
        for c in cues:
            if c["speaker"] is not None and seen[c["speaker"]] == 1:
                c["speaker"], c["text"] = None, c["raw"]
    return cues


def people_index() -> dict:
    """{casefolded name or alias: [slug, …]} from people/*.md. Exact strings only; no fuzzy matching."""
    idx: dict = {}
    for p in sorted((ROOT / "people").glob("*.md")):
        if p.name.startswith("_") or p.name == "INDEX.md":
            continue
        fm, _ = read_frontmatter(p)
        if fm.get("type") != "person":
            continue
        al = fm.get("aliases") or []
        for n in [fm.get("name")] + (al if isinstance(al, list) else [al]):
            key = " ".join(str(n or "").split()).casefold()
            if key and p.stem not in idx.setdefault(key, []):
                idx[key].append(p.stem)
    return idx


def speaker_rows(cues: list[dict]) -> list[dict]:
    idx, rows = people_index(), {}
    for c in cues:
        label = c["speaker"] or NO_LABEL
        r = rows.setdefault(label, {"cluster": label, "talk": 0.0})
        r["talk"] += max(0.0, c["end"] - c["start"])
    for label, r in rows.items():
        hits = idx.get(" ".join(label.split()).casefold(), []) if label != NO_LABEL else []
        if label == NO_LABEL:
            r.update(cand="none", note="Zoom gave no participant label for these lines")
        elif len(hits) == 1:
            r.update(cand=f"{hits[0]} source: zoom-label", note=f"Zoom participant label; exact match on a name or alias in people/{hits[0]}.md; machine candidate, not confirmed")
        elif hits:
            r.update(cand=label, note=f"Zoom participant label; matches {len(hits)} people ({', '.join(hits)}); confirm the person slug")
        else:
            r.update(cand=label, note="Zoom participant label; confirm the person slug")
    return list(rows.values())


# ---------------------------------------------------------------- ledger rows for meetings and files

def now() -> str:
    return eb.now_utc()


def slug(topic: str) -> str:
    s = unicodedata.normalize("NFKD", topic or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60].strip("-") or "meeting"


def local_start(m: dict) -> dt.datetime:
    files = [f.get("recording_start") for f in m.get("recording_files") or [] if f.get("recording_start")]
    iso = m.get("start_time") or (min(files) if files else None) or now()
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    try:
        from zoneinfo import ZoneInfo
        return t.astimezone(ZoneInfo(m["timezone"]))
    except Exception:
        return t


def duration_s(m: dict) -> float:
    spans = [(f.get("recording_start"), f.get("recording_end")) for f in m.get("recording_files") or []]
    spans = [(a, b) for a, b in spans if a and b]
    if spans:
        a = min(dt.datetime.fromisoformat(x.replace("Z", "+00:00")) for x, _ in spans)
        b = max(dt.datetime.fromisoformat(x.replace("Z", "+00:00")) for _, x in spans)
        if b > a:
            return (b - a).total_seconds()
    return float(m.get("duration") or 0) * 60


def meeting_row(c, m: dict):
    r = c.execute("SELECT * FROM zoom_meetings WHERE uuid=?", (m["uuid"],)).fetchone()
    if r:
        return r
    t = local_start(m)
    base = f"{t.date().isoformat()}_{slug(m.get('topic') or '')}"
    taken = lambda f: c.execute("SELECT 1 FROM zoom_meetings WHERE folder=?", (f,)).fetchone() or (ZOOM_DIR / f).exists()  # noqa: E731
    folder = base
    if taken(folder):
        folder = f"{base}_{t.strftime('%H%M')}"
    n = 2
    while taken(folder):
        folder, n = f"{base}_{t.strftime('%H%M')}_{n}", n + 1
    c.execute("INSERT INTO zoom_meetings (uuid, meeting_id, topic, start_time, duration_seconds, host, folder, state, first_seen, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
              (m["uuid"], str(m.get("id") or ""), m.get("topic") or "", t.isoformat(), duration_s(m), m.get("host_email") or m.get("host_id") or "", folder, "waiting", now(), now()))
    return c.execute("SELECT * FROM zoom_meetings WHERE uuid=?", (m["uuid"],)).fetchone()


def set_meeting(c, uuid, **f):
    f["updated_at"] = now()
    c.execute(f"UPDATE zoom_meetings SET {', '.join(k + '=?' for k in f)} WHERE uuid=?", [*f.values(), uuid])


def set_file(c, f: dict, uuid: str, path: str, state: str, note: str = "", **extra):
    old = c.execute("SELECT state, failed_since FROM zoom_files WHERE file_id=?", (f["id"],)).fetchone()
    since = (old["failed_since"] if old and old["failed_since"] else now()) if state == "failed" else None
    c.execute("INSERT INTO zoom_files (file_id, uuid, file_type, recording_type, recording_start, path, size_bytes, sha256, state, note, failed_since, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) "
              "ON CONFLICT(file_id) DO UPDATE SET path=excluded.path, size_bytes=excluded.size_bytes, sha256=excluded.sha256, state=excluded.state, note=excluded.note, failed_since=excluded.failed_since, updated_at=excluded.updated_at",
              (f["id"], uuid, f["file_type"], f.get("recording_type") or "", f.get("recording_start") or "", path, extra.get("size", f.get("file_size") or 0), extra.get("sha256"), state, note[:500], since, now()))


def file_path(c, mrow, f: dict) -> str:
    """Folder-relative name for one Zoom file: its recording type, e.g. audio_only.m4a, audio_transcript.vtt, shared_screen_with_speaker_view.mp4."""
    old = c.execute("SELECT path FROM zoom_files WHERE file_id=?", (f["id"],)).fetchone()
    if old and old["path"]:
        return old["path"]
    stem = re.sub(r"[^a-z0-9_]+", "_", (f.get("recording_type") or f["file_type"]).lower()).strip("_") or f["file_type"].lower()
    used = {r[0] for r in c.execute("SELECT path FROM zoom_files WHERE uuid=?", (mrow["uuid"],))}
    name, n = f"{mrow['folder']}/{stem}{EXT[f['file_type']]}", 2
    while name in used:
        name, n = f"{mrow['folder']}/{stem}_{n}{EXT[f['file_type']]}", n + 1
    return name


def retry_due(frow) -> bool:
    if not frow or frow["state"] != "failed":
        return True
    return (eb.hours_since(frow["updated_at"]) or 0) * 60 >= RETRY_FAILED_MIN


# ---------------------------------------------------------------- one meeting

def handle(c, m: dict, tok: str, kinds: set) -> list[str]:
    """Download this meeting's files of the given kinds; in poll mode (no MP4 in kinds) also land it. Returns error lines."""
    errs = []
    mrow = meeting_row(c, m)
    uuid, net = m["uuid"], eb.metered()
    files = sorted((f for f in m.get("recording_files") or [] if f.get("file_type") in EXT and f.get("id")), key=lambda f: f.get("recording_start") or "")
    for f in files:
        kind = f["file_type"]
        frow = c.execute("SELECT * FROM zoom_files WHERE file_id=?", (f["id"],)).fetchone()
        if frow and frow["state"] == "done":
            continue
        rel = file_path(c, mrow, f)
        size = int(f.get("file_size") or 0)
        if (f.get("status") or "completed") != "completed":
            set_file(c, f, uuid, rel, "waiting", "Zoom is still processing it")
            continue
        if kind not in kinds and frow and frow["state"] in ("deferred", "failed"):
            continue  # the video's state belongs to zoom.video
        if kind == "MP4" and (kind not in kinds or net):
            set_file(c, f, uuid, rel, "deferred", f"metered network ({net}); video waits for an unmetered one" if net else "video is fetched by zoom.video")
            continue
        if kind not in kinds or not retry_due(frow):
            continue
        if kind == "M4A" and net and size > eb.METERED_MAX_DOWNLOAD:
            set_file(c, f, uuid, rel, "deferred", f"metered network ({net}); audio over 50 MB waits (~{size / 1048576:.0f} MB)")
            continue
        try:
            dest = ZOOM_DIR / rel
            download(f["download_url"], tok, dest, kind)
            set_file(c, f, uuid, rel, "done", size=dest.stat().st_size, sha256=eb.file_hash(dest, "sha256"))
            eb.audit(c, "zoom", mrow["rec_id"], "downloaded", f"{rel} {dest.stat().st_size} B")
        except Exception as e:
            set_file(c, f, uuid, rel, "failed", f"{type(e).__name__}: {e}")
            errs.append(f"{rel}: {type(e).__name__}: {str(e)[:160]}")
    if "MP4" not in kinds:
        try:
            land(c, m, uuid)
        except Exception as e:
            set_meeting(c, uuid, note=f"landing failed: {type(e).__name__}: {str(e)[:300]}")
            errs.append(f"{mrow['folder']}: landing failed: {type(e).__name__}: {str(e)[:160]}")
    return errs


def land(c, m: dict, uuid: str):
    mrow = c.execute("SELECT * FROM zoom_meetings WHERE uuid=?", (uuid,)).fetchone()
    fl = c.execute("SELECT * FROM zoom_files WHERE uuid=? ORDER BY recording_start, path", (uuid,)).fetchall()
    audio = next((f for f in fl if f["file_type"] == "M4A" and f["state"] == "done"), None)
    if mrow["state"] == "landed":
        if audio and not c.execute("SELECT audio_path FROM recordings WHERE id=?", (mrow["rec_id"],)).fetchone()[0]:
            eb.upd(c, mrow["rec_id"], audio_path=f"zoom/{audio['path']}", size_bytes=audio["size_bytes"], sha256=audio["sha256"], downloaded_at=now())
        return
    vtts = [f for f in fl if f["file_type"] == "TRANSCRIPT"]
    if vtts and all(f["state"] == "done" for f in vtts):
        return land_vtt(c, m, mrow, vtts, fl, audio)
    end = dt.datetime.fromisoformat(mrow["start_time"]) + dt.timedelta(seconds=mrow["duration_seconds"] or 0)
    waited_h = (dt.datetime.now(dt.timezone.utc) - end).total_seconds() / 3600
    if vtts:
        return set_meeting(c, uuid, state="waiting", note="transcript listed, not downloaded yet")
    if waited_h < VTT_GRACE_H:
        return set_meeting(c, uuid, state="waiting", note=f"no transcript from Zoom yet; goes to Groq by its audio {VTT_GRACE_H} h after the meeting")
    if not audio:
        return set_meeting(c, uuid, state="waiting", note="no transcript from Zoom and no audio downloaded yet")
    rid = mrow["rec_id"] or eb.new_rec_id(c)
    c.execute("INSERT INTO recordings (id, source, era, title, plaud_metadata, recorded_at, duration_seconds, audio_path, size_bytes, sha256, status, listed_at, downloaded_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (rid, "zoom", "fresh", mrow["topic"], zoom_meta(mrow), mrow["start_time"], mrow["duration_seconds"], f"zoom/{audio['path']}", audio["size_bytes"], audio["sha256"],
               eb.ST_DOWNLOADED, mrow["first_seen"], now(), now()))
    set_meeting(c, uuid, rec_id=rid, landed_via="groq", state="landed", note="no VTT from Zoom; the M4A goes through transcription and diarization")
    eb.audit(c, "zoom", rid, "queued_for_groq", mrow["folder"])


def zoom_meta(mrow) -> str:
    return json.dumps({"zoom_uuid": mrow["uuid"], "zoom_meeting_id": mrow["meeting_id"], "host": mrow["host"], "folder": mrow["folder"]})


def cell(s) -> str:
    return " ".join(str(s if s is not None else "").replace("|", "/").split())


def land_vtt(c, m: dict, mrow, vtts, fl, audio):
    """name: land · reads: the meeting's VTT file(s) · writes: recordings/inbox/<rec_id>/{transcript,speakers,meta}.md, the ledger row (status ready, backend zoom vtt)."""
    uuid = mrow["uuid"]
    t0 = min((f["recording_start"] for f in vtts if f["recording_start"]), default="")
    cues = []
    for f in vtts:  # a meeting recorded in parts has one VTT per part; each restarts at zero
        off = (dt.datetime.fromisoformat(f["recording_start"].replace("Z", "+00:00")) - dt.datetime.fromisoformat(t0.replace("Z", "+00:00"))).total_seconds() if f["recording_start"] and t0 else 0.0
        cues += parse_vtt((ZOOM_DIR / f["path"]).read_text(encoding="utf-8-sig", errors="replace"), off)
    rid = mrow["rec_id"] or eb.new_rec_id(c)
    set_meeting(c, uuid, rec_id=rid, state="landing")  # the id is reserved before any file is written, so a crash re-lands the same id
    dest = eb.REC_INBOX / rid
    dest.mkdir(parents=True, exist_ok=True)
    rows = speaker_rows(cues)
    dur = mrow["duration_seconds"] or (cues[-1]["end"] if cues else 0)
    date, mins, n = mrow["start_time"][:10], round(dur / 60), len([r for r in rows if r["cluster"] != NO_LABEL])
    src = f'["[{rid} {date}]"]'
    head = (f"---\nname: Recording {rid} · {mrow['start_time'][:16].replace('T', ' ')} · {mins} min\ntype: transcript\n"
            f"description: Zoom recording, {mins} min, {n} named speakers in Zoom's transcript; raw transcript, not yet ingested\n"
            f"lobe: both\nsources: {src}\nrec_id: {rid}\nsource: zoom\nrecorded_at: {mrow['start_time']}\nduration_seconds: {dur}\n"
            f"speakers_detected: {n}\nbackend: zoom vtt\ntranscript_version: 1\n---\n")
    body = [f"# {rid} · transcript (raw; never edited; speaker labels are the participant names Zoom gave; who they are lives in speakers.md)", ""]
    if not cues:
        body.append("*(empty transcript)*")
    cur, para, start = object(), [], 0.0
    for q in cues + [{"speaker": object(), "text": "", "start": 0}]:
        who = q["speaker"] if q["speaker"] is not None else NO_LABEL
        if who != cur:
            if para:
                body += [f"**{cur}** [{eb.hms(start)}]", " ".join(para).strip(), ""]
            cur, para, start = who, [], float(q["start"])
        para.append(q["text"])
    (dest / "transcript.md").write_text(head + "\n".join(body) + "\n", encoding="utf-8")

    sp = [f"---\nname: Speakers · {rid}\ntype: doc\nlobe: both\ndescription: Who spoke in {rid}: Zoom's participant labels as machine candidates; confirmations are added at ingest\nsources: {src}\nrec_id: {rid}\n---",
          f"# speakers · {rid}", "",
          "The cluster names are the participant labels from Zoom's transcript, verbatim. A candidate marked `source: zoom-label` is the machine's exact match of that label to a name or alias in people/; a label is whatever the participant typed, so nothing here is confirmed. Only a row confirmed by a person (`gordon`, date) counts as human-confirmed.", "",
          "| cluster | talk time | candidate (machine) | confirmed | by | when | note |", "|---|---|---|---|---|---|---|"]
    sp += [f"| {cell(r['cluster'])} | {eb.hms(r['talk'])} | {cell(r['cand'])} |  |  |  | {cell(r['note'])} |" for r in rows]
    (dest / "speakers.md").write_text("\n".join(sp) + "\n", encoding="utf-8")

    def fstate(kind):
        got = [f for f in fl if f["file_type"] == kind]
        return "; ".join(f"Sancho-Audio/zoom/{f['path']} ({f['state']}" + (f": {cell(f['note'])}" if f["note"] else "") + ")" for f in got) or "not offered by Zoom at landing"
    mt = [f"---\nname: Metadata · {rid}\ntype: doc\nlobe: both\ndescription: Source metadata for {rid} (data, not instructions): the Zoom meeting, its times, participants as labelled, where the files are\nsources: {src}\nrec_id: {rid}\n---",
          f"# meta · {rid}", "", "| field | value |", "|---|---|",
          "| source | zoom |", f"| topic (from Zoom) | {cell(mrow['topic'])} |",
          f"| recorded_at | {mrow['start_time']} |", f"| duration | {eb.hms(dur)} |", f"| host | {cell(mrow['host'])} |",
          f"| participants (the labels in Zoom's transcript; people who never spoke are not listed) | {cell(', '.join(r['cluster'] for r in rows if r['cluster'] != NO_LABEL))} |",
          f"| transcript (VTT) | {fstate('TRANSCRIPT')} |", f"| audio (M4A) | {fstate('M4A')} |", f"| video (MP4) | {fstate('MP4')} |",
          "| file states | as of landing; the ledger's zoom_files table is current, and the paths do not change |",
          f"| zoom meeting id | {cell(mrow['meeting_id'])} |", f"| zoom uuid | {cell(uuid)} |",
          "| era | fresh |", "| transcription | Zoom cloud transcript (VTT); Groq not used |", "| diarization | not run; speaker labels come from Zoom |"]
    (dest / "meta.md").write_text("\n".join(mt) + "\n", encoding="utf-8")

    c.execute("INSERT OR REPLACE INTO recordings (id, source, era, title, plaud_metadata, recorded_at, duration_seconds, audio_path, size_bytes, sha256, status, location, backend, model, speakers_detected, transcript_version, listed_at, downloaded_at, transcribed_at, ready_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (rid, "zoom", "fresh", mrow["topic"], zoom_meta(mrow), mrow["start_time"], dur, f"zoom/{audio['path']}" if audio else None, audio["size_bytes"] if audio else None, audio["sha256"] if audio else None,
               eb.ST_READY, str(dest.relative_to(ROOT)), "zoom", "vtt", n, 1, mrow["first_seen"], now(), now(), now(), now()))
    set_meeting(c, uuid, landed_via="vtt", state="landed", note="")
    eb.audit(c, "zoom", rid, "ready", f"{dest.relative_to(ROOT)}/transcript.md from {mrow['folder']}")


# ---------------------------------------------------------------- commands

def pending_request(command: str) -> bool:
    return any(list((ROOT / "_queue" / d).glob(f"*_{command}_*.md")) for d in ("requests", "deferred", "running") if (ROOT / "_queue" / d).exists())


def poll_failed(c, e) -> int:
    eb.meta_set(c, "zoom_state", "failing")
    eb.meta_set(c, "zoom_last_error", str(e)[:300])
    eb.meta_set(c, "zoom_last_fail", now())
    if not eb.meta_get(c, "zoom_fail_since"):
        eb.meta_set(c, "zoom_fail_since", now())
    eb.audit(c, "zoom", None, "poll_failed", e)
    eb.write_status(c)
    print(f"zoom: poll failed: {e}")
    return 1


def cmd_poll() -> int:
    _l = eb.lock("zoom")
    c = eb.db()
    if not configured():
        asked = note_setup()
        eb.meta_set(c, "zoom_state", "not configured")
        eb.write_status(c)
        print("zoom: not configured" + (" (what to create is now one line in _setup/MAC-SETUP.md)" if asked else ""))
        return 0
    if not online():
        print("zoom: offline; nothing to do (a known state, not a failure)")
        return 0
    eb.meta_set(c, "zoom_last_attempt", now())
    last = eb.meta_get(c, "zoom_last_poll_ok")
    today = dt.datetime.now(dt.timezone.utc).date()
    since = dt.date.fromisoformat(last[:10]) - dt.timedelta(days=OVERLAP_DAYS) if last else today - dt.timedelta(days=FIRST_LOOKBACK_DAYS)
    try:
        tok = token()
        meetings = list_meetings(tok, since)
        seen = {m["uuid"] for m in meetings}
        # meetings older than the window that still owe a transcript or audio
        for r in c.execute("SELECT DISTINCT m.uuid FROM zoom_meetings m LEFT JOIN zoom_files f ON f.uuid=m.uuid AND f.file_type!='MP4' AND f.state!='done' "
                           "WHERE m.state!='gone' AND (m.state!='landed' OR f.file_id IS NOT NULL)").fetchall():
            if r["uuid"] not in seen:
                try:
                    meetings.append(meeting_recordings(tok, r["uuid"]))
                except ZoomError as e:
                    if "HTTP 404" not in str(e):
                        raise
                    set_meeting(c, r["uuid"], state="gone", note="Zoom no longer has this recording")
    except ZoomError as e:
        return poll_failed(c, e)
    errs = []
    for m in meetings:
        if m.get("uuid"):
            errs += handle(c, m, tok, {"TRANSCRIPT", "M4A"})
    eb.meta_set(c, "zoom_last_poll_ok", now())
    eb.meta_set(c, "zoom_state", "ok")
    c.execute("DELETE FROM meta WHERE key IN ('zoom_fail_since', 'zoom_last_error', 'zoom_last_fail')")
    videos = c.execute("SELECT COUNT(*) FROM zoom_files WHERE file_type='MP4' AND state IN ('deferred', 'failed')").fetchone()[0]
    queued = ""
    if videos and not pending_request("zoom.video"):
        enqueue(ROOT, "zoom.video", ["video"], by="zoom.poll", session=os.environ.get("SANCHO_SESSION") or "schedule zoom.poll")
        queued = "; zoom.video queued"
    eb.write_status(c)
    s = zoom_counts(c)
    print(f"zoom: {len(meetings)} meeting(s) listed; landed {s['vtt']} by VTT and {s['groq']} via Groq in total, {s['waiting']} waiting, {videos} video(s) to fetch{queued}"
          + (f"; {len(errs)} file error(s): " + " | ".join(errs[:3]) if errs else ""))
    return 0


def zoom_counts(c) -> dict:
    g = lambda q: c.execute(q).fetchone()[0]  # noqa: E731
    return {"vtt": g("SELECT COUNT(*) FROM zoom_meetings WHERE state='landed' AND landed_via='vtt'"), "groq": g("SELECT COUNT(*) FROM zoom_meetings WHERE state='landed' AND landed_via='groq'"),
            "waiting": g("SELECT COUNT(*) FROM zoom_meetings WHERE state IN ('waiting', 'landing')")}


def cmd_video() -> int:
    _l = eb.lock("zoom")
    c = eb.db()
    if not configured():
        print("zoom: not configured")
        return 0
    if eb.metered():
        print(f"zoom video: deferred; metered network ({eb.metered()})")
        return 0
    if not online():
        print("zoom video: offline; nothing to do")
        return 0
    t0, done, errs = time.time(), 0, []
    try:
        tok = token()
    except ZoomError as e:
        print(f"zoom video: failed: {e}")
        return 1
    for r in c.execute("SELECT DISTINCT uuid FROM zoom_files WHERE file_type='MP4' AND state IN ('deferred', 'failed') ORDER BY recording_start").fetchall():
        if time.time() - t0 > VIDEO_BUDGET_S:
            break
        before = c.execute("SELECT COUNT(*) FROM zoom_files WHERE uuid=? AND file_type='MP4' AND state='done'", (r["uuid"],)).fetchone()[0]
        try:
            errs += handle(c, meeting_recordings(tok, r["uuid"]), tok, {"MP4"})
        except ZoomError as e:
            if "HTTP 404" in str(e):
                c.execute("UPDATE zoom_files SET state='gone', note='Zoom no longer has this file', updated_at=? WHERE uuid=? AND file_type='MP4' AND state!='done'", (now(), r["uuid"]))
            else:
                errs.append(f"{r['uuid']}: {e}")
        done += c.execute("SELECT COUNT(*) FROM zoom_files WHERE uuid=? AND file_type='MP4' AND state='done'", (r["uuid"],)).fetchone()[0] - before
    left = c.execute("SELECT COUNT(*) FROM zoom_files WHERE file_type='MP4' AND state IN ('deferred', 'failed')").fetchone()[0]
    eb.write_status(c)
    print(f"zoom video: {done} downloaded, {left} still to fetch" + (f"; {len(errs)} error(s): " + " | ".join(errs[:3]) if errs else ""))
    return 1 if errs else 0


def main(argv=None) -> int:
    args = [a for a in (sys.argv[1:] if argv is None else argv) if a]
    if args and args[0] == "video":
        return cmd_video()
    if args and args[0] != "poll":
        print("usage: zoom-poll.py [poll | video]")
        return 2
    return cmd_poll()


if __name__ == "__main__":
    sys.exit(main())
