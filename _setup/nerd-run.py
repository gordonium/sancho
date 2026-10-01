#!/usr/bin/env python3
"""
name: nerd-run
type: command
description: Run one headless Claude Code session (the Nerd) on the Mac for a task given in the request (`task_file:` inside the tree, or a request body ending with the line `-- end of task --`; a bare `task:` line is refused, ERRORS.md #7). Fixed tool allowlist, OS sandbox (writes only in the tree and the kit; network only GitHub and Anthropic), no MCP connectors, no outbound messaging, timeout, lease (kind, session, pid) while running, the request's `session:` echoed, transcript kept, one-line receipt.
why: Gordon wants full rounds without being the messenger between Cowork and the Mac; scheduled Cowork is ruled out (decisions 2026-09-30). This is v2's spawn.sh idea made safe by the allowlist, the sandbox and the queue; it is also the harness skill scenarios run on.
reads: the request file ($SANCHO_REQUEST_FILE); _setup/nerd-settings.json; CLAUDE.md (the session reads it itself)
writes: _queue/results/<request id>.transcript.jsonl; _queue/leases/nerd-<request id>.md while running; whatever the task writes inside the tree or ~/Dev/clc-plugins
schedule:
test: _setup/tests/nerd-run/
"""
from __future__ import annotations
import os, sys, json, time, signal, fcntl, argparse, datetime, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter, live_leases, write_lease

ROOT = tree_root()
KIT = Path(os.environ.get("SANCHO_KIT", Path.home() / "Dev/clc-plugins"))
CLAUDE = os.environ.get("SANCHO_CLAUDE_BIN", str(Path.home() / ".local/bin/claude"))
SETTINGS = ROOT / "_setup" / "nerd-settings.json"
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho"))
DEFAULT_TIMEOUT = 1800
MAX_BUDGET_USD = "10"

# What a Nerd session may use. Read/Write/Edit are further limited by the sandbox and the path rules in nerd-settings.json.
ALLOWED = ["Read", "Glob", "Grep", "Write", "Edit", "TodoWrite",
           "Bash(python3 _setup/*)", "Bash(bash _setup/*)", "Bash(_setup/*)",
           "Bash(git status *)", "Bash(git diff *)", "Bash(git log *)", "Bash(git show *)", "Bash(git -C *)",
           "Bash(ls *)", "Bash(rg *)", "Bash(grep *)", "Bash(find *)", "Bash(wc *)", "Bash(head *)", "Bash(tail *)",
           "Bash(cat *)", "Bash(sed -n *)", "Bash(sqlite3 *)", "Bash(date *)", "Bash(mkdir *)", "Bash(mv *)", "Bash(cp *)"]
DENIED = ["WebFetch", "WebSearch", "Agent", "Bash(curl *)", "Bash(wget *)", "Bash(ssh *)", "Bash(scp *)", "Bash(rm *)",
          "Bash(git push *)", "Bash(git commit *)", "Bash(git reset *)", "Bash(git clean *)", "Bash(sudo *)",
          "Bash(launchctl *)", "Bash(osascript *)", "Bash(open *)", "Bash(mail *)", "Bash(sendmail *)"]

PREAMBLE = """You are the Nerd: Sancho's Claude Code session on Gordon's Mac, started headless by the `nerd.run` command (request {rid}, from {by}; session {session}).
Read CLAUDE.md first; it applies to you, must-nevers included. Then read _design/STATUS.md if the task is about Sancho itself.
You run unattended: nobody can answer a question. If the task needs a decision that is Gordon's, stop, write the question into _design/STATUS.md under "Open for Gordon", and end.
You cannot push, commit, send anything outbound, or reach the network except through the tools allowed; the hourly autocommit commits your writes.
Tests are automatic: before calling anything done, run python3 _setup/test-all.py and say what it printed.
End with exactly one line starting "Receipt:" naming the files you wrote (paths only), or "Receipt: nothing written" and why.

TASK:
{task}
"""


END_MARK = "-- end of task --"


def load_task(a) -> tuple[str, dict]:
    """--task (job.run's own calls), task_file: inside the tree, or a request body ending with END_MARK.
    A request's `task:` line or unmarked body is refused: shell-composed requests lost words silently (ERRORS.md #7)."""
    fm, body = {}, ""
    req = os.environ.get("SANCHO_REQUEST_FILE")
    if req and Path(req).exists():
        fm, body = read_frontmatter(Path(req))
    task = a.task or ""
    tf = a.task_file or fm.get("task_file")
    if tf and not task:
        p = (ROOT / str(tf)).resolve()
        if ROOT.resolve() not in p.parents:
            raise SystemExit(f"nerd-run: task_file must be inside the tree: {tf}")
        task = p.read_text(encoding="utf-8")
    if not task and body.strip():
        lines = body.rstrip().splitlines()
        if lines[-1].strip() != END_MARK:
            raise SystemExit(f"nerd-run: refused: the request body does not end with the line `{END_MARK}` (it may have been cut or mangled; ERRORS.md #7). Write the task to a file and use task_file:")
        task = "\n".join(lines[:-1]).strip()
    if not task and fm.get("task"):
        raise SystemExit("nerd-run: refused: a `task:` line in a request is no longer accepted (ERRORS.md #7); use task_file: or a body ending with " + END_MARK)
    if not str(task).strip():
        raise SystemExit(f"nerd-run: no task (give task_file:, or a request body ending with `{END_MARK}`)")
    return str(task), fm


def build_argv(prompt: str) -> list[str]:
    return [CLAUDE, "-p", prompt,
            "--output-format", "stream-json", "--verbose",
            "--settings", str(SETTINGS),
            "--setting-sources", "project",          # the user's own settings (and their permissions) don't leak in
            "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',  # no connectors: no mail, Drive, calendar
            "--permission-mode", "dontAsk",           # anything not allowed is refused, never prompted
            "--allowedTools", *ALLOWED,
            "--disallowedTools", *DENIED,
            "--add-dir", str(KIT),
            "--max-budget-usd", MAX_BUDGET_USD]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task")
    ap.add_argument("--task-file")
    ap.add_argument("--timeout", type=int)
    a = ap.parse_args()
    task, fm = load_task(a)
    rid = os.environ.get("SANCHO_REQUEST_ID") or datetime.datetime.now().strftime("manual-%Y%m%dT%H%M%S")
    by = os.environ.get("SANCHO_REQUESTED_BY") or fm.get("requested_by") or "unknown"
    session = os.environ.get("SANCHO_SESSION") or fm.get("session") or "(none given)"
    timeout = int(a.timeout or fm.get("timeout") or DEFAULT_TIMEOUT)
    if not Path(CLAUDE).exists():
        print(f"nerd-run: claude not found at {CLAUDE}")
        return 1
    STATE.mkdir(parents=True, exist_ok=True)
    lock = open(STATE / "nerd-run.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("nerd-run: another Nerd session is running; one at a time")
        return 1
    results = ROOT / "_queue" / "results"
    results.mkdir(parents=True, exist_ok=True)
    others = [p.stem for p, fm in live_leases(ROOT) if fm.get("kind") == "interactive"]
    if others:
        print(f"nerd-run: note: an interactive Nerd holds a lease ({', '.join(others)}); this session runs beside it")
    lease = write_lease(ROOT, f"nerd-{rid}", "nerd.run", f"{session} · requested by {by}", os.getpid(), task)
    transcript = results / f"{rid}.transcript.jsonl"
    started = time.time()
    status, final = "ok", ""
    try:
        with transcript.open("w") as out:
            p = subprocess.Popen(build_argv(PREAMBLE.format(rid=rid, by=by, session=session, task=task)), cwd=ROOT, stdout=out,
                                 stderr=subprocess.STDOUT, start_new_session=True,
                                 env={**os.environ, "SANCHO_IN_NERD": rid, "SANCHO_SESSION": f"nerd.run {rid}",
                                      "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"})
            try:
                rc = p.wait(timeout=timeout)
                status = "ok" if rc == 0 else f"failed (exit {rc})"
            except subprocess.TimeoutExpired:
                for sig, pause in ((signal.SIGTERM, 5), (signal.SIGKILL, 0)):
                    try:
                        os.killpg(p.pid, sig)
                    except OSError:  # already gone (macOS says EPERM for an exited group)
                        break
                    time.sleep(pause)
                p.wait()
                status = f"timeout after {timeout} s"
    finally:
        lease.unlink(missing_ok=True)
    for ln in transcript.read_text(errors="replace").splitlines():
        try:
            ev = json.loads(ln)
        except ValueError:
            continue
        if ev.get("type") == "result":
            final = str(ev.get("result") or "")
            if ev.get("is_error") and status == "ok":
                status = f"failed ({ev.get('subtype')})"
    receipt = next((l for l in reversed(final.splitlines()) if l.startswith("Receipt:")), "Receipt: (none given)")
    print(final[-3000:])
    print(f"nerd-run: {status} in {int(time.time() - started)} s · session {session} · transcript _queue/results/{transcript.name} · {receipt}")
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
