"""
name: test-pipeline
type: script
description: earballs.py end to end against fake Plaud, Groq and Pushover servers in a temp tree: fresh recording → transcript/speakers/meta in recordings/inbox; corrupt download retried not lost; demo filtered; old recording listed into its era; incremental list stops at the first known ID; Groq 429 is rate-limited not failed; Plaud 401 turns STATUS red and pushes; metered mode refuses backfill; backfill lands in recordings/backlog; the ledger follows a filed folder; library rebuild enrolls only human-confirmed rows; the solo rule machine-confirms but never human-confirms.
why: The pipeline runs unattended; a regression here means recordings silently stop arriving (must-never 10). Gap: §13.4's real-voice fixture clips (Gordon solo, two speakers) need recordings Gordon picks; diarization itself is not exercised here.
reads: _setup/pipeline/earballs.py, _setup/notify.py, _setup/sancho_lib.py
writes: temp files only
requires: mac
test: (this is the test)
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

SETUP = Path(__file__).resolve().parents[2]
VENV_PY = Path(os.environ.get("SANCHO_VENV", Path.home() / ".local/share/sancho/venv")) / "bin/python"
if not VENV_PY.exists():
    print("test-pipeline: FAIL: pipeline venv missing (run _setup/pipeline/install-venv.sh)"); sys.exit(1)
T = Path(tempfile.mkdtemp())
def fail(m):
    print(f"test-pipeline: FAIL: {m}"); shutil.rmtree(T, ignore_errors=True); sys.exit(1)

# --- temp tree
tree = T / "tree"; (tree / "_setup/pipeline").mkdir(parents=True); (tree / "people").mkdir(); (tree / "recordings/inbox").mkdir(parents=True)
(tree / "CLAUDE.md").write_text("x")
for f in ("sancho_lib.py", "notify.py", "notify-reasons.md"): shutil.copy(SETUP / f, tree / "_setup" / f)
shutil.copy(SETUP / "pipeline/earballs.py", tree / "_setup/pipeline/earballs.py")
good = T / "good.ogg"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=frequency=440:duration=40", "-c:a", "libopus", "-b:a", "24k", str(good)], check=True)
GOOD = good.read_bytes(); MD5 = hashlib.md5(GOOD).hexdigest()

# --- fake servers
S = {"list_calls": 0, "plaud_401": False, "groq_429": False, "pushes": [], "groq_calls": 0}
def item(i, day, serial="abc", dur=40000):
    import datetime as d
    ts = int(d.datetime(*day, 12, 0).timestamp() * 1000)
    return {"id": f"p{i}", "filename": f"Meeting {i}", "start_time": ts, "timezone": 2, "duration": dur, "serial_number": serial, "file_md5": MD5 if i != 2 else ""}
ITEMS = [item(1, (2026, 9, 28)), item(2, (2026, 9, 27)), item(3, (2026, 6, 15)), item(9, (2023, 1, 1), serial="04d6a02708c6b8eb77c5f334a92a3cba")]
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _json(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        if S["plaud_401"]: return self._json(401, {})
        if self.path.startswith("/file/simple/web"):
            S["list_calls"] += 1; return self._json(200, {"data_file_list": ITEMS})
        if self.path.startswith("/file/temp-url/"):
            pid = self.path.split("/")[3].split("?")[0]; return self._json(200, {"temp_url_opus": f"http://127.0.0.1:{PORT}/audio/{pid}"})
        if self.path.startswith("/audio/"):
            body = b"<html>not audio</html>" if self.path.endswith("p2") else GOOD
            self.send_response(200); self.end_headers(); self.wfile.write(body); return
        self._json(404, {})
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); raw = self.rfile.read(n)
        if self.path.startswith("/groq"):
            S["groq_calls"] += 1
            if S["groq_429"]: return self._json(429, {"error": "rate_limit"})
            return self._json(200, {"text": "hello there general", "duration": 40, "segments": [{"start": 0, "end": 3, "text": "hello there general"}],
                                    "words": [{"word": "hello", "start": 0.1, "end": 0.5}, {"word": "there", "start": 0.6, "end": 1.0}, {"word": "general", "start": 1.1, "end": 1.8}]})
        if self.path.startswith("/push"):
            S["pushes"].append(raw.decode()); return self._json(200, {"status": 1})
srv = HTTPServer(("127.0.0.1", 0), H); PORT = srv.server_port; threading.Thread(target=srv.serve_forever, daemon=True).start()

envf = T / "env"; envf.write_text(f"PLAUD_BEARER_TOKEN=tok\nPLAUD_BASE_URL=http://127.0.0.1:{PORT}\nGROQ_API_KEY=g\nHUGGINGFACE_TOKEN=\nPUSHOVER_USER=u\nPUSHOVER_TOKEN=a\n")
ENV = {**{k: v for k, v in os.environ.items() if not k.startswith(("PLAUD", "GROQ", "HUGGING", "PUSHOVER"))},
       "SANCHO_ROOT": str(tree), "SANCHO_AUDIO": str(T / "audio"), "SANCHO_STATE": str(T / "state"), "SANCHO_SECRETS_PLAIN": str(envf),
       "SANCHO_GROQ_URL": f"http://127.0.0.1:{PORT}/groq", "SANCHO_PUSHOVER_URL": f"http://127.0.0.1:{PORT}/push"}
EB = tree / "_setup/pipeline/earballs.py"
def run(*a):
    r = subprocess.run([str(VENV_PY), str(EB), *a], env=ENV, capture_output=True, text=True, timeout=300)
    if r.returncode: fail(f"earballs {' '.join(a)} exit {r.returncode}: {r.stdout[-500:]}{r.stderr[-1500:]}")
    return r.stdout
import sqlite3
def ledger():
    c = sqlite3.connect(T / "audio/ledger.sqlite"); c.row_factory = sqlite3.Row; return c
def rows(): return {r["plaud_id"]: dict(r) for r in ledger().execute("SELECT * FROM recordings")}

# 1. first sync (full reconcile on the first run of the day)
run("sync")
R = rows()
if "p9" in R: fail("demo recording not filtered")
if R["p1"]["status"] != "ready" or R["p1"]["era"] != "fresh": fail(f"p1 not ready: {R['p1']['status']} {R['p1']['last_error']}")
if R["p2"]["status"] != "queued" or R["p2"]["error_count"] != 1: fail(f"corrupt p2 should be queued with 1 error: {R['p2']}")
if R["p3"]["status"] != "listed" or R["p3"]["era"] != "era3": fail(f"old p3 should be listed era3: {R['p3']}")
rid = R["p1"]["id"]; d = tree / "recordings/inbox" / rid
for f in ("transcript.md", "speakers.md", "meta.md"):
    if not (d / f).exists(): fail(f"missing {f}")
t = (d / "transcript.md").read_text()
if "type: transcript" not in t or f"[{rid} 2026-09-28]" not in t or "hello there general" not in t or "**SPEAKER_00** [00:00:00]" not in t: fail("transcript content:\n" + t)
if "not run" not in (d / "speakers.md").read_text(): fail("speakers.md should say diarization not run")
if not (T / "audio/processed" / f"{rid}.ogg").read_bytes() == GOOD: fail("audio not stored byte-identical")
if not (T / "audio/processed" / f"{rid}.json").exists(): fail("word json missing")
st = (tree / "recordings/STATUS.md").read_text()
if "waiting for ingest (recordings/inbox/): 1" not in st or "| era3 | listed | 1 |" not in st: fail("STATUS.md:\n" + st)
if not list((T / "audio/ledger-backups").glob("ledger.*.sqlite")): fail("no ledger backup")

# 1b. ingest moves the folder; the ledger follows it
dest = tree / "work/acme/clients/x/transcripts" / f"2026-09-28_{rid}"; dest.parent.mkdir(parents=True); d.rename(dest)
run("status")
if rows()["p1"]["location"] != str(dest.relative_to(tree)): fail(f"ledger did not follow the move: {rows()['p1']['location']}")

# 2. incremental: stops at the first known id, no duplicates, no new Groq calls
g0 = S["groq_calls"]; run("sync")
if len(rows()) != 3: fail("duplicate rows after incremental sync")
if S["groq_calls"] != g0: fail("ready recording re-transcribed")

# 3. Groq 429 → rate_limited, not failed
ITEMS.insert(0, item(4, (2026, 9, 29))); S["groq_429"] = True
run("sync")
p4 = rows()["p4"]
if p4["status"] != "downloaded" or p4["error_count"] != 0 or "rate-limited" not in (p4["last_error"] or ""): fail(f"429 handling: {p4}")
S["groq_429"] = False

# 4. Plaud 401 → token expired, STATUS red, one push
S["plaud_401"] = True; run("sync")
st = (tree / "recordings/STATUS.md").read_text()
if "RED" not in st or "token expired" not in st: fail("401 not RED in STATUS:\n" + st[:600])
if not any("token+expired" in p or "token%20expired" in p for p in S["pushes"]): fail(f"no push for expired token: {S['pushes']}")
if not any("Sancho+ALERT" in p and "unregistered" not in p for p in S["pushes"]): fail(f"red watchdog not an alert with a registered reason: {S['pushes']}")
n = len(S["pushes"]); run("sync")
if len(S["pushes"]) != n: fail("push repeated within the day")
S["plaud_401"] = False

# 5. metered: backfill refuses; then backfill lands in recordings/backlog/<era>/
(T / "state").mkdir(exist_ok=True); (T / "state/network.json").write_text(json.dumps({"label": "phone", "metered": True}))
out = run("backfill", "--era", "era3", "--limit", "5")
if "refused" not in out or rows()["p3"]["status"] != "listed": fail("metered backfill not refused: " + out)
if "metered network (phone)" not in (tree / "recordings/STATUS.md").read_text(): fail("STATUS.md lacks the metered line")
# a long fresh recording waits while metered; a short one still downloads
ITEMS.insert(0, item(5, (2026, 9, 29), dur=5 * 3600 * 1000)); ITEMS.insert(0, item(6, (2026, 9, 29)))
run("sync", "--full")
R = rows()
if R["p5"]["status"] != "queued" or "unmetered" not in (R["p5"]["last_error"] or ""): fail(f"5 h recording downloaded while metered: {R['p5']}")
if R["p6"]["status"] != "ready": fail(f"short recording blocked while metered: {R['p6']}")
(T / "state/network.json").unlink()
run("backfill", "--era", "era3", "--limit", "5")
p3 = rows()["p3"]
if p3["status"] != "ready" or not (tree / "recordings/backlog/era3" / p3["id"] / "transcript.md").exists(): fail(f"backfill: {p3}")

# 6. library rebuild: human rows enroll, machine rows don't; solo rule machine-confirms only
code = f"""
import sys, json, numpy as np; sys.argv=['x']
sys.path.insert(0, {str(tree / '_setup/pipeline')!r}); import earballs as e
e.VOICE_REC.mkdir(parents=True, exist_ok=True)
for i in range(4):
    rid = f'rec_00000000{{i:02d}}'; v = np.ones((2, 4)); v[1] = [1, -1, 1, -1]
    np.save(e.VOICE_REC / f'{{rid}}.npy', v); (e.VOICE_REC / f'{{rid}}.labels.json').write_text(json.dumps({{'labels': ['SPEAKER_00', 'SPEAKER_01']}}))
    d = e.REC_INBOX / rid; d.mkdir(parents=True, exist_ok=True)
    by0 = 'gordon' if i < 3 else 'machine: solo rule sim=0.99'
    (d / 'speakers.md').write_text(f'---\\nrec_id: {{rid}}\\n---\\n| cluster | talk | cand | confirmed | by | when | note |\\n|---|---|---|---|---|---|---|\\n| SPEAKER_00 | 1 | x | gordon | {{by0}} | 2026-09-30 | |\\n| SPEAKER_01 | 1 | x | roy | machine: voiceprint sim=0.99 | | |\\n')
    if i == 0: (d / 'speakers.md').write_text((d / 'speakers.md').read_text() + '| SPEAKER_00 | 1 | x | gordon | gordon | 2026-09-30 | dup |\\n')
lib = e.rebuild_library()
assert 'roy' not in lib['speakers'], 'machine row enrolled'
assert lib['speakers']['gordon'] == {{'refs': 4, 'recordings': 3}}, lib
row = {{'id': 'rec_0000000000'}}
solo = e.stage_match(row, {{'speakers': ['SPEAKER_00'], 'segments': [{{'start': 0, 'end': 60, 'speaker': 'SPEAKER_00'}}]}})
assert solo[0]['confirmed'] == '' and 'thin' in solo[0]['note'], solo   # 4 refs < 5: thin, no auto
np.save(e.VOICE_SPK / 'gordon.npy', np.ones((5, 4))); (e.VOICE_SPK / '_library.json').write_text(json.dumps({{'speakers': {{'gordon': {{'refs': 5, 'recordings': 3}}}}}}))
solo = e.stage_match(row, {{'speakers': ['SPEAKER_00'], 'segments': [{{'start': 0, 'end': 60, 'speaker': 'SPEAKER_00'}}]}})
assert solo[0]['confirmed'] == 'gordon' and solo[0]['by'].startswith('machine: solo rule'), solo
two = e.stage_match(row, {{'speakers': ['SPEAKER_00', 'SPEAKER_01'], 'segments': [{{'start': 0, 'end': 60, 'speaker': 'SPEAKER_00'}}, {{'start': 60, 'end': 120, 'speaker': 'SPEAKER_01'}}]}})
assert two[0]['confirmed'] == '' and 'auto-tag paused' in two[0]['note'], two   # people/gordon.md absent → auto paused
print('lib-ok')
"""
r = subprocess.run([str(VENV_PY), "-c", code], env=ENV, capture_output=True, text=True, timeout=120)
if "lib-ok" not in r.stdout: fail("library/match: " + r.stderr[-1500:])

shutil.rmtree(T, ignore_errors=True)
print("test-pipeline: PASS")
