#!/usr/bin/env python3
"""
name: nerd-run
type: command
description: Run one headless Claude Code session (the Nerd) on the Mac for a task given in the request (`task_file:` inside the tree, or a request body ending with the line `-- end of task --`; a bare `task:` line is refused, ERRORS.md #7). Fixed tool allowlist, OS sandbox (writes only in the tree and the kit; network only GitHub and Anthropic), no MCP connectors, no outbound messaging, timeout, lease (kind, session, pid) while running, the request's `session:` echoed, transcript kept, one-line receipt. Every session carries the quarantine guard as a PreToolUse hook (the user-level registration does not reach a session started with project-only setting sources). A task file whose frontmatter says `quarantine_reader: true` starts the session with SANCHO_QUARANTINE_READER=1, which the guard admits to Read/Grep/Glob in the legacy folders only together with this session's nerd.run lease; a run fails if it touched a legacy folder and the guard logged nothing.
why: Gordon wants full rounds without being the messenger between Cowork and the Mac; scheduled Cowork is ruled out (decisions 2026-09-30). This is v2's spawn.sh idea made safe by the allowlist, the sandbox and the queue; it is also the harness skill scenarios run on.
reads: the request file ($SANCHO_REQUEST_FILE); the task file's frontmatter (`quarantine_reader`); _setup/nerd-settings.json; _setup/quarantine-paths.md; _queue/log/quarantine-access.log; CLAUDE.md (the session reads it itself)
writes: _queue/results/<request id>.transcript.jsonl; ~/.local/state/sancho/nerd-settings.json (nerd-settings.json plus the guard hook, rebuilt every run); _queue/leases/nerd-<request id>.md while running; whatever the task writes inside the tree or ~/Dev/clc-plugins
schedule:
test: _setup/tests/nerd-run/
"""
from __future__ import annotations
import os, re, sys, json, time, signal, fcntl, argparse, datetime, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter, live_leases, write_lease, nerd_admit, as_paths, task_frontmatter, EX_DEFER

ROOT = tree_root()
KIT = Path(os.environ.get("SANCHO_KIT", Path.home() / "Dev/clc-plugins"))
CLAUDE = os.environ.get("SANCHO_CLAUDE_BIN", str(Path.home() / ".local/bin/claude"))
SETTINGS = ROOT / "_setup" / "nerd-settings.json"
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho"))
DEFAULT_TIMEOUT = 1800
MAX_BUDGET_USD = "10"
GUARD = ROOT / "_setup" / "quarantine-guard.py"
GUARD_LOG = ROOT / "_queue" / "log" / "quarantine-access.log"
GUARD_MATCHER = "Read|Grep|Glob|Bash|Write|Edit|MultiEdit|NotebookEdit"  # reads: the quarantine; writes: other sessions' leases (ERRORS.md #12)
# Model per task [gordon 2026-10-01: "Sonnet too dumb; Opus 5.5 high"]: a task's own frontmatter may say otherwise.
DEFAULT_MODEL, DEFAULT_EFFORT = "claude-opus-5-5", "high"
EFFORTS = ("low", "medium", "high", "xhigh", "max")
MODEL_RE = re.compile(r"^claude-[a-z0-9][a-z0-9.-]{2,60}$")

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


def effective_settings(rid: str = "", effort: str = DEFAULT_EFFORT) -> Path:
    """nerd-settings.json plus the quarantine guard as a PreToolUse hook, written beside the lock (one fixed name: the sandbox
    protects exactly that file from the session; two sessions side by side share it, and each one's effort also travels in
    its own environment as CLAUDE_CODE_EFFORT_LEVEL). The session is started with
    `--setting-sources project`, so the hook registered in ~/.claude/settings.json never fires in it (measured 2026-10-01:
    a Read under gordon-os-v2 from a nerd.run session left no line in either guard log)."""
    st = json.loads(SETTINGS.read_text(encoding="utf-8"))
    pre = st.setdefault("hooks", {}).setdefault("PreToolUse", [])
    if not any("quarantine-guard.py" in str(h.get("command", "")) for e in pre for h in e.get("hooks", [])):
        pre.append({"matcher": GUARD_MATCHER, "hooks": [{"type": "command", "command": f'/usr/bin/python3 "{GUARD}"', "timeout": 10}]})
    st["effortLevel"] = effort
    STATE.mkdir(parents=True, exist_ok=True)
    out = STATE / "nerd-settings.json"
    out.write_text(json.dumps(st, indent=1), encoding="utf-8")
    return out


def model_and_effort(task: str) -> tuple[str, str, str]:
    """`model:` and `effort:` from the task's own frontmatter; anything missing or malformed falls back to the default, and says so."""
    fm = task_frontmatter(task)
    model, effort, notes = str(fm.get("model") or "").strip(), str(fm.get("effort") or "").strip().lower(), []
    if model and not MODEL_RE.match(model):
        notes.append(f"model `{model[:40]}` is not a model id, using {DEFAULT_MODEL}")
        model = ""
    if effort and effort not in EFFORTS:
        notes.append(f"effort `{effort[:20]}` is not one of {'/'.join(EFFORTS)}, using {DEFAULT_EFFORT}")
        effort = ""
    return model or DEFAULT_MODEL, effort or DEFAULT_EFFORT, "; ".join(notes)


def model_used(transcript: Path) -> str:
    """The model the session itself reported at start (the transcript's init event), or ''."""
    try:
        for ln in transcript.read_text(errors="replace").splitlines()[:50]:
            try:
                ev = json.loads(ln)
            except ValueError:
                continue
            if isinstance(ev, dict) and ev.get("type") == "system" and ev.get("model"):
                return str(ev["model"])
    except OSError:
        pass
    return ""


def fenced_names() -> list[str]:
    try:
        text = (ROOT / "_setup" / "quarantine-paths.md").read_text(encoding="utf-8")
        names = [m.rstrip("/").rsplit("/", 1)[-1].lower() for m in re.findall(r"(?m)^-\s*`([^`]+)`", text)]
    except OSError:
        names = []
    return sorted(set(names)) or ["gordon-os-v2", "jarvis-v3"]


def log_lines() -> int:
    try:
        return len(GUARD_LOG.read_text(errors="replace").splitlines())
    except OSError:
        return 0


def touched_legacy(transcript: Path) -> bool:
    """Did a Read, Grep or Glob in the session name a path through a fenced folder? (The bare word in an Edit or a search
    pattern is not a read.)"""
    names = fenced_names()

    def through(item: dict) -> bool:
        inp = item.get("input") or {}
        paths = [inp.get("file_path"), inp.get("path"), inp.get("pattern") if item.get("name") == "Glob" else None]
        return any(part.lower() in names for p in paths if isinstance(p, str) for part in p.split("/"))

    for ln in transcript.read_text(errors="replace").splitlines():
        try:
            ev = json.loads(ln)
        except ValueError:
            continue
        content = (ev.get("message") or {}).get("content") if isinstance(ev, dict) and ev.get("type") == "assistant" else None
        for item in content if isinstance(content, list) else []:
            if isinstance(item, dict) and item.get("type") == "tool_use" and item.get("name") in ("Read", "Grep", "Glob") and through(item):
                return True
    return False


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
        fm = {**fm, "quarantine_reader": read_frontmatter(p)[0].get("quarantine_reader")}  # only a task FILE in the tree carries the flag
    else:
        fm = {**fm, "quarantine_reader": None}
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


def build_argv(prompt: str, settings: Path = SETTINGS, model: str = DEFAULT_MODEL) -> list[str]:
    return [CLAUDE, "-p", prompt,
            "--model", model,
            "--output-format", "stream-json", "--verbose",
            "--settings", str(settings),
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
    ap.add_argument("--append", default="", help="text added after the task (job.run's stage contract and retry brief)")
    ap.add_argument("--timeout", type=int)
    a = ap.parse_args()
    task, fm = load_task(a)
    task += a.append
    reader = str(fm.get("quarantine_reader")).lower() == "true"
    rid = os.environ.get("SANCHO_REQUEST_ID") or datetime.datetime.now().strftime("manual-%Y%m%dT%H%M%S")
    by = os.environ.get("SANCHO_REQUESTED_BY") or fm.get("requested_by") or "unknown"
    session = os.environ.get("SANCHO_SESSION") or fm.get("session") or "(none given)"
    timeout = int(a.timeout or fm.get("timeout") or DEFAULT_TIMEOUT)
    if not Path(CLAUDE).exists():
        print(f"nerd-run: claude not found at {CLAUDE}")
        return 1
    model, effort, me_note = model_and_effort(task)
    only = as_paths(task_frontmatter(task).get("writes_only"))
    STATE.mkdir(parents=True, exist_ok=True)
    # Admission is decided and the lease written under one short lock, so two starts in the same second cannot both get in.
    with open(STATE / "nerd-admit.lock", "w") as gate:
        fcntl.flock(gate, fcntl.LOCK_EX)
        ok, why = nerd_admit(ROOT, only, f"nerd-{rid}")
        if not ok:
            print(f"nerd-run: deferred: {why}; this request waits and starts when the lease clears")
            return EX_DEFER
        lease = write_lease(ROOT, f"nerd-{rid}", "nerd.run", f"{session} · requested by {by}", os.getpid(), task, only)
    if why:
        print(f"nerd-run: note: running {why}; this session writes only {', '.join(only)}")
    if me_note:
        print(f"nerd-run: note: {me_note}")
    results = ROOT / "_queue" / "results"
    results.mkdir(parents=True, exist_ok=True)
    others = [p.stem for p, fm in live_leases(ROOT) if fm.get("kind") == "interactive"]
    if others:
        print(f"nerd-run: note: an interactive Nerd holds a lease ({', '.join(others)}); this session runs beside it")
    transcript = results / f"{rid}.transcript.jsonl"
    started = time.time()
    status, final = "ok", ""
    env = {**os.environ, "SANCHO_IN_NERD": rid, "SANCHO_SESSION": f"nerd.run {rid}", "CLAUDE_CODE_EFFORT_LEVEL": effort,
           "PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"}
    env.pop("SANCHO_QUARANTINE_READER", None)  # never inherited: only this task file's own flag sets it
    if reader:
        env["SANCHO_QUARANTINE_READER"] = "1"
    guard_lines = log_lines()
    try:
        with transcript.open("w") as out:
            p = subprocess.Popen(build_argv(PREAMBLE.format(rid=rid, by=by, session=session, task=task), effective_settings(rid, effort), model), cwd=ROOT,
                                 stdout=out, stderr=subprocess.STDOUT, start_new_session=True, env=env)
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
    if touched_legacy(transcript) and log_lines() == guard_lines:
        # the session named a legacy folder and the guard wrote nothing: the hook is not firing, so nothing enforced the never-read list
        status = "failed (quarantine guard did not fire: the session touched a legacy folder and quarantine-access.log has no new line)"
    receipt = next((l for l in reversed(final.splitlines()) if l.startswith("Receipt:")), "Receipt: (none given)")
    print(final[-3000:])
    ran = model_used(transcript)
    asked = f"model {model} effort {effort}" + (f" (the session reported {ran})" if ran and ran != model else "")
    print(f"nerd-run: {status} in {int(time.time() - started)} s{' · quarantine reader' if reader else ''} · {asked} · session {session} · transcript _queue/results/{transcript.name} · {receipt}")
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
