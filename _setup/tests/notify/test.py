"""
name: test-notify
type: script
description: notify.py against a local fake Pushover endpoint: sends with the right fields and priority, skips a repeat within a day, sends again when the message for the key changes, fails cleanly without keys; only the pipeline's red watchdog sends warn; everything else is info.
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
# notify.push through the watcher's calling convention: a request as sancho-enqueue writes it, parsed and turned into argv by the watcher's own code
import importlib.util
sys.path.insert(0, str(NOTIFY.parent))
from sancho_lib import read_frontmatter
spec = importlib.util.spec_from_file_location("watcher", NOTIFY.parent / "sancho-watcher.py"); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
cmds = W.load_commands()
if cmds.get("notify.push", {}).get("script") != "_setup/notify.py": fail(f"notify.push not on the allowlist: {cmds.get('notify.push')}")
def via_request(args):
    req = Path(tmp, "req.md"); req.write_text(f"---\ncommand: notify.push\nargs: [{', '.join(args)}]\nrequested_by: test\n---\n")
    argv = W.argv_for(NOTIFY, read_frontmatter(req)[0]["args"])
    return subprocess.run(argv, env=env, capture_output=True, text=True)
n = len(got)
r = via_request(["info", "check-back done, 3 hops left"])
if r.returncode or len(got) != n + 1: fail(f"request-shaped send: {r.stdout}{r.stderr}")
if got[-1]["priority"] != ["-1"] or got[-1]["message"] != ["check-back done, 3 hops left"]: fail(f"comma message not whole / wrong priority: {got[-1]}")
r = via_request(["warn", "--key=cb", "recordings stuck, act today"])
if r.returncode or len(got) != n + 2 or got[-1]["priority"] != ["0"] or got[-1]["message"] != ["recordings stuck, act today"]: fail(f"request with --key: {r.stdout}{r.stderr} {got[-1]}")
# "Warn means WARN" (Gordon, 2026-09-30): the only warn sender is the pipeline watchdog's red state; every other push is info
import re
SETUP = NOTIFY.parent
senders = {}
for f in list(SETUP.glob("*.py")) + list(SETUP.glob("*.sh")) + list(SETUP.glob("pipeline/*.py")):
    if f.name in ("notify.py", "notify-test.sh"): continue
    for m in re.finditer(r"""(?:push\(|notify\)?,\s*|level = )["'](warn|alert)["']""", f.read_text()):
        senders.setdefault(f.name, []).append(m.group(1))
if set(senders) - {"earballs.py"}: fail(f"warn/alert sent outside the pipeline watchdog: {senders}")
if senders.get("earballs.py", []) != ["warn"]: fail(f"earballs should have exactly one warn (the red watchdog): {senders.get('earballs.py')}")
print("test-notify: PASS")
