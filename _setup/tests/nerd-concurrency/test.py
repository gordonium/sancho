"""
name: test-nerd-concurrency
type: script
description: nerd.run deferral and disjoint-writes concurrency with a fake claude in a temp tree. sancho_lib.nerd_admit: alone yes; beside a whole-tree session no; beside a session with `writes_only` only when this task's `writes_only` cannot meet it; never a third. nerd-run.py: a refused start exits 75 with "deferred", starts no session and leaves no lease; a disjoint task runs beside the live one and its lease carries `writes_only`; `model:` and `effort:` in the task's frontmatter reach the session (defaults claude-opus-5-5 / high; a malformed model falls back). The watcher: an exit 75 moves the request to _queue/deferred/ with a `deferred` result and no push, the network release leaves it there, and it returns to requests/ once the lease is gone.
why: The nomad-brief task died at 23:17 on 2026-10-01 with "one at a time" and a warn while the backfill ran (STATUS.md, Cowork 23:40); a refusal that needs nothing from Gordon must wait, not fail.
reads: _setup/nerd-run.py, _setup/sancho_lib.py, _setup/sancho-watcher.py, _setup/nerd-settings.json
writes: temp files only
test: (this is the test)
"""
import importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SETUP = Path(__file__).resolve().parents[2]
T = Path(tempfile.mkdtemp())
if not T.is_dir():
    print("test-nerd-concurrency: FAIL: no temp dir"); sys.exit(1)
sleeper = subprocess.Popen(["sleep", "120"])  # a live pid that is not this test: "another session"


def done(code, msg):
    sleeper.kill(); shutil.rmtree(T, ignore_errors=True)
    print(f"test-nerd-concurrency: {msg}"); sys.exit(code)


def need(cond, msg):
    if not cond:
        done(1, f"FAIL: {msg}")


tree = T / "tree"
(tree / "_setup").mkdir(parents=True); (tree / "_queue/inbox").mkdir(parents=True); (tree / "_queue/requests").mkdir()
(tree / "CLAUDE.md").write_text("x")
for f in ("nerd-run.py", "sancho_lib.py", "nerd-settings.json", "sancho-watcher.py"):
    shutil.copy(SETUP / f, tree / "_setup" / f)
fake = T / "claude"
fake.write_text("""#!/usr/bin/env python3
import sys, json, os
d = os.environ["FAKE_OUT"]
json.dump(sys.argv[1:], open(d + "/argv.json", "w"))
open(d + "/effort.txt", "w").write(os.environ.get("CLAUDE_CODE_EFFORT_LEVEL", "unset"))
me = "_queue/leases/nerd-" + os.environ["SANCHO_IN_NERD"] + ".md"
open(d + "/lease.txt", "w").write(open(me).read() if os.path.exists(me) else "")
print(json.dumps({"type": "system", "subtype": "init", "model": sys.argv[sys.argv.index("--model") + 1]}))
print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "ok\\nReceipt: nothing written, a fake"}))
""")
fake.chmod(0o755)
out_dir = T / "out"; out_dir.mkdir()
os.environ.update(SANCHO_ROOT=str(tree), SANCHO_STATE=str(T / "state"), SANCHO_CLAUDE_BIN=str(fake), SANCHO_KIT=str(T / "kit"), FAKE_OUT=str(out_dir))
for k in ("SANCHO_SESSION", "SANCHO_REQUESTED_BY", "SANCHO_REQUEST_FILE", "SANCHO_IN_NERD"):
    os.environ.pop(k, None)
sys.path.insert(0, str(tree / "_setup"))
import sancho_lib as L  # noqa: E402

leases = tree / "_queue/leases"


def clear():
    for p in leases.glob("*.md") if leases.exists() else []:
        p.unlink()
    for p in out_dir.glob("*"):
        p.unlink()


# 1. the admission rule
need(L.nerd_admit(tree, None)[0], "alone, a session without writes_only must start")
L.write_lease(tree, "nerd-whole", "nerd.run", "s", sleeper.pid)
need(not L.nerd_admit(tree, None)[0], "a second whole-tree session was admitted")
ok, why = L.nerd_admit(tree, ["personal/nomad/brief.md"])
need(not ok and "whole tree" in why, f"admitted beside a session with no writes_only: {why}")
clear()
L.write_lease(tree, "nerd-backfill", "nerd.run", "s", sleeper.pid, "", ["people/adam.md", "people/_backfill-census.md"])
need("writes_only: [\"people/adam.md\", \"people/_backfill-census.md\"]" in (leases / "nerd-backfill.md").read_text(), "lease does not carry writes_only")
need(L.nerd_admit(tree, ["personal/nomad/brief.md"])[0], "disjoint writes_only refused")
need(not L.nerd_admit(tree, None)[0], "a task without writes_only admitted beside a running session")
ok, why = L.nerd_admit(tree, ["people"])
need(not ok and "overlap" in why, f"a folder above a leased file admitted: {why}")
need(not L.nerd_admit(tree, ["people/_backfill-census.md"])[0], "the same file admitted twice")
L.write_lease(tree, "nerd-second", "nerd.run", "s", sleeper.pid, "", ["work/x.md"])
ok, why = L.nerd_admit(tree, ["personal/nomad/brief.md"])
need(not ok and "already running" in why, f"a third session admitted: {why}")
(leases / "nerd-second.md").unlink()
L.write_lease(tree, "nerd-dead", "nerd.run", "s", 999999, "", ["personal/nomad/brief.md"])
need(L.nerd_admit(tree, ["personal/nomad/brief.md"])[0], "a lease whose pid is gone still blocks")
(leases / "nerd-dead.md").unlink()


# 2. nerd-run.py: deferral (exit 75, no session, no lease), then side by side with model and effort from the task
def nerd(rid, task_file):
    r = subprocess.run([sys.executable, str(tree / "_setup/nerd-run.py"), "--task-file", task_file],
                       env={**os.environ, "SANCHO_REQUEST_ID": rid}, capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout + r.stderr


inbox = tree / "_queue/inbox"
(inbox / "plain.md").write_text("---\nname: plain\n---\ndo a thing\n")
(inbox / "nomad.md").write_text('---\nname: nomad\nwrites_only: ["personal/nomad/brief.md"]\nmodel: claude-fable-5-1\neffort: max\n---\nwrite the brief\n')
(inbox / "census.md").write_text('---\nname: census\nwrites_only: ["people/_backfill-census.md"]\n---\nedit the census\n')
(inbox / "badmodel.md").write_text("---\nname: bad\nmodel: gpt-9; rm -rf\neffort: frantic\n---\ndo a thing\n")
rc, out = nerd("d1", "_queue/inbox/plain.md")
need(rc == L.EX_DEFER == 75 and "nerd-run: deferred:" in out, f"no deferral for a task without writes_only (rc {rc}): {out}")
need(not (out_dir / "argv.json").exists() and not (leases / "nerd-d1.md").exists(), "a deferred run started a session or left a lease")
rc, out = nerd("d2", "_queue/inbox/census.md")
need(rc == 75 and "overlap" in out, f"overlapping writes_only not deferred (rc {rc}): {out}")
rc, out = nerd("p1", "_queue/inbox/nomad.md")
need(rc == 0 and "disjoint writes" in out, f"disjoint task did not run beside the live session (rc {rc}): {out}")
argv = json.loads((out_dir / "argv.json").read_text())
need(argv[argv.index("--model") + 1] == "claude-fable-5-1", "model: from the task not passed")
need((out_dir / "effort.txt").read_text() == "max", "effort: from the task not in the session's environment")
need(json.loads(Path(argv[argv.index("--settings") + 1]).read_text()).get("effortLevel") == "max", "effort not in the session's settings")
need('writes_only: ["personal/nomad/brief.md"]' in (out_dir / "lease.txt").read_text(), "the session's own lease lacks its writes_only")
need("model claude-fable-5-1 effort max" in out, f"result line does not name model and effort: {out}")
need(not (leases / "nerd-p1.md").exists() and (leases / "nerd-backfill.md").exists(), "leases wrong after the run")
clear()
rc, out = nerd("m1", "_queue/inbox/plain.md")
argv = json.loads((out_dir / "argv.json").read_text())
need(rc == 0 and argv[argv.index("--model") + 1] == "claude-opus-5-5" and (out_dir / "effort.txt").read_text() == "high", f"defaults are not claude-opus-5-5 / high: {out}")
rc, out = nerd("m2", "_queue/inbox/badmodel.md")
argv = json.loads((out_dir / "argv.json").read_text())
need(rc == 0 and argv[argv.index("--model") + 1] == "claude-opus-5-5" and "is not a model id" in out and "is not one of" in out, f"malformed model or effort not replaced by the default: {out}")

# 3. the watcher: exit 75 -> deferred/, a `deferred` result, nothing pushed; stays through the network release; back when the lease is gone
spec = importlib.util.spec_from_file_location("watcher", tree / "_setup/sancho-watcher.py"); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
pushed = []
W.notify_on_change = lambda *a, **k: pushed.append(a)
clear()
L.write_lease(tree, "nerd-whole", "nerd.run", "s", sleeper.pid)
req = tree / "_queue/requests/20261002T000000Z_nerd.run_aaaaaa.md"
req.write_text("---\ncommand: nerd.run\ntask_file: _queue/inbox/plain.md\nrequested_by: cowork\nsession: cowork hop 9\n---\n")
cmds = {"nerd.run": {"script": "_setup/nerd-run.py", "timeout": 60, "heavy": False, "terminal_only": False}}
st = W.run_one(req, cmds, dict(os.environ))
dfile = tree / "_queue/deferred" / req.name
need(st == "deferred" and dfile.exists() and not req.exists(), f"request not moved to deferred/ (status {st})")
res = (tree / "_queue/results" / req.name).read_text()
need("status: deferred" in res and "starts it when the lease clears" in res, f"result does not say deferred: {res}")
need(not pushed, "a deferral pushed to Gordon")
need(not list((tree / "_queue/running").glob("*.md")), "request left in running/")
W.check_network(); W.release_nerds()
need(dfile.exists(), "a nerd.run waiting for a lease was released while the lease is live")
(leases / "nerd-whole.md").unlink()
W.release_nerds()
need(req.exists() and not dfile.exists(), "request not released when the lease cleared")
logs = "".join(p.read_text() for p in (tree / "_queue/log").glob("*.log"))
need("deferred (info)" in logs and "released from deferred (info)" in logs, "no info lines in the log")
st = W.run_one(req, cmds, dict(os.environ))
need(st == "ok" and "status: ok" in (tree / "_queue/results" / req.name).read_text(), f"released request did not run (status {st})")
done(0, "PASS")
