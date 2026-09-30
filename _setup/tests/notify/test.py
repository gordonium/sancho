"""
name: test-notify
type: script
description: notify.py against a local fake Pushover endpoint: sends with the right fields and priority, skips a repeat within a day, sends again when the message for the key changes, fails cleanly without keys; no caller sends at info.
why: A phone channel that silently stops sending is worse than none.
reads: _setup/notify.py
writes: temp state only
test: (this is the test)
"""
import os, sys, json, tempfile, threading, subprocess, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
NOTIFY = Path(__file__).resolve().parents[2] / "notify.py"
got = []
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        got.append(urllib.parse.parse_qs(self.rfile.read(int(self.headers["Content-Length"])).decode()))
        self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":1}')
    def log_message(self, *a): pass
srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
tmp = tempfile.mkdtemp()
env = dict(os.environ, SANCHO_STATE=tmp, SANCHO_PUSHOVER_URL=f"http://127.0.0.1:{srv.server_port}/", PUSHOVER_USER="u1", PUSHOVER_TOKEN="t1")
def run(*a, e=env): return subprocess.run([sys.executable, str(NOTIFY), *a], env=e, capture_output=True, text=True)
def fail(m): print(f"test-notify: FAIL: {m}"); sys.exit(1)
r = run("warn", "pipeline behind", "--key=pipe")
if r.returncode or len(got) != 1: fail(f"first send: {r.stdout}{r.stderr}")
g = got[0]
if g["user"] != ["u1"] or g["token"] != ["t1"] or g["priority"] != ["0"] or g["message"] != ["pipeline behind"]: fail(f"fields {g}")
run("warn", "pipeline behind", "--key=pipe")
if len(got) != 1: fail("repeat within a day was sent")
run("info", "pipeline recovered", "--key=pipe")
if len(got) != 2 or got[1]["priority"] != ["-1"]: fail("state change not sent / wrong priority")
run("alert", "x")
if got[-1]["priority"] != ["1"]: fail("alert priority")
st = json.loads(Path(tmp, "notify.json").read_text()); st["pipe"]["sent"] -= 90000; Path(tmp, "notify.json").write_text(json.dumps(st))
run("info", "pipeline recovered", "--key=pipe")
if len(got) != 4: fail("not re-sent after a day")
r = run("warn", "no keys", e={k: v for k, v in env.items() if not k.startswith("PUSHOVER")})
if r.returncode != 1 or len(got) != 4: fail("sent or succeeded without keys")
# nothing Gordon needs to see goes at info (silent, in-app only on his phone; decided 2026-09-30)
import re
SETUP = NOTIFY.parent
for f in list(SETUP.glob("*.py")) + list(SETUP.glob("*.sh")) + list(SETUP.glob("pipeline/*.py")):
    if f.name == "notify.py": continue
    txt = f.read_text()
    if "notify" in txt and re.search(r"""notify[^\n]{0,80}["']info["']|level = "info"|:-info}""", txt): fail(f"{f.name} sends a push at info level")
print("test-notify: PASS")
