"""
name: test-guard-leases
type: script
description: quarantine-guard.py's second duty, lease enforcement (ERRORS.md #12), with hook inputs on stdin against a temp tree. An Edit, a Write and a Bash redirection (`>`, `>>`, `tee`) onto a path inside another live lease's `writes_only` are refused and logged in lease-access.log; the holder passes, both as the nerd.run session named by the lease and as a process under the lease's pid; a path outside every lease passes; a read of the leased file passes; a lease whose pid is gone refuses nothing; `--install` widens an older reads-only registration to Write and Edit.
why: A Cowork subagent edited people/_backfill-census.md at 01:3x on 2026-10-02 while the backfill job's lease declared that file; leases were advisory.
reads: _setup/quarantine-guard.py
writes: temp files only
test: (this is the test)
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[2] / "quarantine-guard.py"
T = Path(tempfile.mkdtemp())
if not T.is_dir():
    print("test-guard-leases: FAIL: no temp dir"); sys.exit(1)
sleeper = subprocess.Popen(["sleep", "120"])  # a live pid that is not a parent of the hook: another session


def done(code, msg):
    sleeper.kill(); shutil.rmtree(T, ignore_errors=True)
    print(f"test-guard-leases: {msg}"); sys.exit(code)


tree = T / "tree"; leases = tree / "_queue/leases"; leases.mkdir(parents=True); (tree / "people").mkdir()
log = T / "log"
ENV = {**os.environ, "SANCHO_LEASE_TREE": str(tree), "SANCHO_QUARANTINE_LOG_DIR": str(log), "SANCHO_CLAUDE_SETTINGS": str(T / "settings.json")}
ENV.pop("SANCHO_IN_NERD", None)


def lease(name, pid, scope):
    (leases / f"{name}.md").write_text(f"---\nname: {name}\ntype: lease\nkind: nerd.run\nsession: s\npid: {pid}\nwrites_only: {json.dumps(scope)}\n---\nnote\n")


def refused(tool, tool_input, **env):
    r = subprocess.run([sys.executable, str(GUARD)], input=json.dumps({"tool_name": tool, "tool_input": tool_input, "cwd": str(tree)}),
                       env={**ENV, **env}, capture_output=True, text=True, timeout=30)
    return "LEASE GUARD" in r.stdout and '"deny"' in r.stdout


def need(cond, msg):
    if not cond:
        done(1, f"FAIL: {msg}")


census = str(tree / "people/_backfill-census.md")
lease("nerd-job1", sleeper.pid, ["people/adam.md", "people/_backfill-census.md", "work/acme"])
need(refused("Edit", {"file_path": census, "old_string": "a", "new_string": "b"}), "an Edit on a path in a live foreign lease was not refused")
need(refused("Write", {"file_path": "people/adam.md", "content": "x"}), "a Write by relative path was not refused")
need(refused("MultiEdit", {"file_path": str(tree / "work/acme/notes/a.md"), "edits": []}), "a file under a leased folder was not refused")
need(refused("Bash", {"command": "echo row >> people/_backfill-census.md"}), "a >> redirection was not refused")
need(refused("Bash", {"command": f'printf x > "{census}"'}), "a quoted > redirection was not refused")
need(refused("Bash", {"command": "ls | tee -a people/adam.md"}), "tee onto a leased path was not refused")
need(not refused("Edit", {"file_path": str(tree / "people/roy.md"), "old_string": "a", "new_string": "b"}), "a path outside all leases was refused")
need(not refused("Bash", {"command": "grep -c x people/_backfill-census.md > /dev/null 2>&1"}), "reading a leased file was refused")
need(not refused("Read", {"file_path": census}), "a Read of a leased file was refused")
need(not refused("Edit", {"file_path": census, "old_string": "a", "new_string": "b"}, SANCHO_IN_NERD="job1"), "the lease holder's own Edit (nerd.run id) was refused")
need(refused("Edit", {"file_path": census, "old_string": "a", "new_string": "b"}, SANCHO_IN_NERD="other"), "another nerd.run session passed as the holder")
lines = (log / "lease-access.log").read_text().splitlines()
need(len(lines) == 7 and all("\trefused\t" in l and l.endswith("nerd-job1") for l in lines) and "people/_backfill-census.md" in lines[0], f"refusals not logged one per line: {lines}")
lease("nerd-job1", os.getpid(), ["people/_backfill-census.md"])  # the lease's process is a parent of the hook: an interactive holder
need(not refused("Edit", {"file_path": census, "old_string": "a", "new_string": "b"}), "a session running under the lease's pid was refused")
lease("nerd-job1", 999999, ["people/_backfill-census.md"])
need(not refused("Edit", {"file_path": census, "old_string": "a", "new_string": "b"}), "a lease whose pid is gone still refuses")

# --install widens a registration made before the lease check existed
settings = T / "settings.json"
settings.write_text(json.dumps({"hooks": {"PreToolUse": [{"matcher": "Read|Grep|Glob|Bash", "hooks": [{"type": "command", "command": "/usr/bin/python3 x/quarantine-guard.py"}]},
                                                         {"matcher": "Bash", "hooks": [{"type": "command", "command": "live-site-guard"}]}]}}))
r = subprocess.run([sys.executable, str(GUARD), "--check"], env=ENV, capture_output=True, text=True)
need(r.returncode == 0 and "reads only" in r.stdout, f"--check does not say the registration lacks Write/Edit: {r.stdout}")
subprocess.run([sys.executable, str(GUARD), "--install"], env=ENV, capture_output=True, text=True)
pre = json.loads(settings.read_text())["hooks"]["PreToolUse"]
need(len(pre) == 2 and "Edit" in pre[0]["matcher"] and "Write" in pre[0]["matcher"] and pre[1]["matcher"] == "Bash", f"--install did not widen the matcher in place: {pre}")
r = subprocess.run([sys.executable, str(GUARD), "--check"], env=ENV, capture_output=True, text=True)
need("reads only" not in r.stdout, "still reported as reads only after --install")
done(0, "PASS")
