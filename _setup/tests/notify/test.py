"""
name: test-notify
type: script
description: notify.py against a sink file (and, where localhost can be bound, a local fake Pushover endpoint): sends with the right fields and priority, skips a repeat within a day, sends again when the message for the key changes, fails cleanly without keys; levels are info -1, warn 0, alert 0 with its own title and sound (nothing breaks quiet hours); the sender's session is echoed and does not defeat dedupe; a warn with an unregistered reason is sent but tagged; every warn or alert in a script or skill carries a reason registered at that level in _setup/notify-reasons.md.
why: A phone channel that silently stops sending is worse than none; one that sounds for no reason teaches Gordon to ignore it.
reads: _setup/notify.py, _setup/notify-reasons.md, _setup/*.py|sh, _setup/pipeline/*.py, skills/*/SKILL.md
writes: temp state only
test: (this is the test)
"""
import os, re, sys, json, tempfile, threading, subprocess, urllib.parse
from pathlib import Path
NOTIFY = Path(__file__).resolve().parents[2] / "notify.py"
SETUP = NOTIFY.parent
tmp = tempfile.mkdtemp()
SINK = Path(tmp, "sink")
env = dict(os.environ, SANCHO_STATE=tmp, SANCHO_PUSHOVER_URL=f"file://{SINK}", PUSHOVER_USER="u1", PUSHOVER_TOKEN="t1", SANCHO_SESSION="")
def run(*a, e=env): return subprocess.run([sys.executable, str(NOTIFY), *a], env=e, capture_output=True, text=True)
def got(): return [urllib.parse.parse_qs(l) for l in SINK.read_text().splitlines()] if SINK.exists() else []
def fail(m): print(f"test-notify: FAIL: {m}"); sys.exit(1)
r = run("warn", "job fix waiting at gate", "--key=pipe", "--reason=job-gate")
if r.returncode or len(got()) != 1: fail(f"first send: {r.stdout}{r.stderr}")
g = got()[0]
if g["user"] != ["u1"] or g["token"] != ["t1"] or g["priority"] != ["0"] or g["message"] != ["job fix waiting at gate"] or g["title"] != ["Sancho"]: fail(f"fields {g}")
run("warn", "job fix waiting at gate", "--key=pipe", "--reason=job-gate")
if len(got()) != 1: fail("repeat within a day was sent")
run("info", "pipeline recovered", "--key=pipe")
if len(got()) != 2 or got()[1]["priority"] != ["-1"]: fail("state change not sent / wrong priority")
# alert: priority 0 for now (quiet hours hold) with its own title and sound [gordon 2026-10-01]
run("alert", "x", "--reason=pipeline-red")
a = got()[-1]
if a["priority"] != ["0"] or a["title"] != ["Sancho ALERT"] or a.get("sound") != ["siren"]: fail(f"alert fields {a}")
if any(int(x["priority"][0]) > 0 for x in got()): fail("a push above priority 0 would break quiet hours")
st = json.loads(Path(tmp, "notify.json").read_text()); st["pipe"]["sent"] -= 90000; Path(tmp, "notify.json").write_text(json.dumps(st))
run("info", "pipeline recovered", "--key=pipe")
if len(got()) != 4: fail("not re-sent after a day")
r = run("warn", "no keys", "--reason=job-gate", e={k: v for k, v in env.items() if not k.startswith("PUSHOVER")})
if r.returncode != 1 or len(got()) != 4: fail("sent or succeeded without keys")
# unregistered reason: still sent (never silence a stuck job) but tagged; a missing reason likewise
r = run("warn", "made up", "--reason=because")
if r.returncode or "(unregistered reason)" not in got()[-1]["message"][0] or "not registered" not in r.stdout: fail(f"unregistered reason not tagged: {r.stdout} {got()[-1]}")
r = run("alert", "wrong level", "--reason=job-gate")
if "(unregistered reason)" not in got()[-1]["message"][0]: fail("a warn reason accepted for alert")
# session echoed, from env or flag, and it does not make a repeat news
n = len(got())
run("info", "hop 2 done", "--key=s", e=dict(env, SANCHO_SESSION="cowork hop 2"))
if got()[-1]["message"] != ["hop 2 done · from cowork hop 2"]: fail(f"session not echoed: {got()[-1]}")
run("info", "hop 2 done", "--key=s", "--session=cowork hop 3")
if len(got()) != n + 1: fail("a different sender defeated dedupe")
# the real HTTP path, where this process may bind localhost (not inside a nerd.run sandbox)
try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    posted = []
    class H(BaseHTTPRequestHandler):
        def do_POST(self):
            posted.append(urllib.parse.parse_qs(self.rfile.read(int(self.headers["Content-Length"])).decode()))
            self.send_response(200); self.end_headers(); self.wfile.write(b'{"status":1}')
        def log_message(self, *a): pass
    srv = HTTPServer(("127.0.0.1", 0), H)
except PermissionError:
    srv = None
    print("test-notify: (localhost blocked here: HTTP path not exercised; the board outside the sandbox runs it)")
if srv:
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    r = run("info", "over http", e=dict(env, SANCHO_PUSHOVER_URL=f"http://127.0.0.1:{srv.server_port}/"))
    if r.returncode or len(posted) != 1 or posted[0]["message"] != ["over http"]: fail(f"http send: {r.stdout}{r.stderr}")
# notify.push through the watcher's calling convention: a request as sancho-enqueue writes it, parsed and turned into argv by the watcher's own code
import importlib.util
sys.path.insert(0, str(SETUP))
from sancho_lib import read_frontmatter
spec = importlib.util.spec_from_file_location("watcher", SETUP / "sancho-watcher.py"); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
cmds = W.load_commands()
if cmds.get("notify.push", {}).get("script") != "_setup/notify.py": fail(f"notify.push not on the allowlist: {cmds.get('notify.push')}")
def via_request(args):
    req = Path(tmp, "req.md"); req.write_text(f"---\ncommand: notify.push\nargs: [{', '.join(args)}]\nrequested_by: test\n---\n")
    argv = W.argv_for(NOTIFY, read_frontmatter(req)[0]["args"])
    return subprocess.run(argv, env=env, capture_output=True, text=True)
n = len(got())
r = via_request(["info", "check-back done, 3 hops left"])
if r.returncode or len(got()) != n + 1: fail(f"request-shaped send: {r.stdout}{r.stderr}")
if got()[-1]["priority"] != ["-1"] or got()[-1]["message"] != ["check-back done, 3 hops left"]: fail(f"comma message not whole / wrong priority: {got()[-1]}")
r = via_request(["warn", "--key=cb", "--reason=chain-end", "recordings stuck, act today"])
if r.returncode or len(got()) != n + 2 or got()[-1]["priority"] != ["0"] or got()[-1]["message"] != ["recordings stuck, act today"]: fail(f"request with --key/--reason: {r.stdout}{r.stderr} {got()[-1]}")
# the registry: every sounding push in a script or skill names a reason registered at that level (replaces "only the pipeline may warn")
spec = importlib.util.spec_from_file_location("notify", NOTIFY); N = importlib.util.module_from_spec(spec); spec.loader.exec_module(N)
reg = N.registered_reasons()
for need in ("job-gate", "job-stopped", "chain-end", "pipeline-red", "watcher-dead"):
    if need not in reg: fail(f"notify-reasons.md lacks {need}")
if reg.get("pipeline-red") != "alert" or reg.get("job-gate") != "warn": fail(f"registry levels wrong: {reg}")
bad, seen = [], 0
LEVEL = re.compile(r"""["'](warn|alert)["']""")
REASON = re.compile(r"""(?:--reason=|reason=["']|reason\s*=\s*["']|["'](warn|alert)["'],\s*["'])([a-z0-9-]+)""")
for f in list(SETUP.glob("*.py")) + list(SETUP.glob("*.sh")) + list(SETUP.glob("pipeline/*.py")):
    if f.name == "notify.py": continue
    lines = f.read_text().splitlines()
    for i, ln in enumerate(lines):
        if not re.search(r"notify|push\(|level", ln) or ln.lstrip().startswith("#"): continue
        for m in LEVEL.finditer(ln):
            seen += 1
            near = ln[m.start():] + " ".join(lines[i + 1:i + 3])
            rm = [x for x in REASON.finditer(near)]
            reason = rm[0].group(2) if rm else None
            if reason is None or reg.get(reason) != m.group(1): bad.append(f"{f.name}:{i + 1} {m.group(1)} reason={reason}")
ROOT = SETUP.parent
for f in ROOT.glob("skills/*/SKILL.md"):
    for i, ln in enumerate(f.read_text().splitlines()):
        for m in re.finditer(r"notify\.push (warn|alert)\b|args: \[(warn|alert),", ln):
            seen += 1
            lvl = m.group(1) or m.group(2)
            rm = re.search(r"--reason=([a-z0-9-]+)", ln[m.start():])
            if not rm or reg.get(rm.group(1)) != lvl: bad.append(f"{f.parent.name}/SKILL.md:{i + 1} {lvl} reason={rm.group(1) if rm else None}")
if bad: fail(f"sounding push without a registered reason: {bad}")
if seen < 4: fail(f"the sender scan found only {seen} sounding pushes; the pattern has drifted from the code")
print(f"test-notify: PASS ({seen} sounding pushes, all with registered reasons)")
