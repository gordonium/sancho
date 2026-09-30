#!/usr/bin/env python3
"""
name: job-run
type: command
description: Walk a job file (_queue/jobs/*.md) stage by stage, running each stage as a nerd.run session, advancing `current` on success, stopping at any `gate: human` stage; a failed stage is retried once, then the job stops. Pushes are info (silent): the greeting reports job state; warn is only for timely attention (Gordon, 2026-09-30). Detaches at once so the watcher stays free; progress lives in the job file.
why: Gordon wants full rounds without being the messenger; scheduled Cowork is ruled out (decisions 2026-09-30). State lives in the job file, never in memory (CLAUDE.md), so a crash or sleep loses nothing: rerun resumes at `current`.
reads: the job file; stage fields `task:` / `task_file:` / `note:`; _setup/nerd-run.py; _setup/test-all.py (run after every stage the session calls done)
writes: the job file (stage status, `current`, `history` lines in the body); _queue/results/<request id>.job.md (final summary); one Pushover message when it stops
schedule:
test: _setup/tests/job-run/
"""
from __future__ import annotations
import os, re, sys, fcntl, argparse, datetime, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter, _parse_scalar

ROOT = tree_root()
SETUP = ROOT / "_setup"
NERD = os.environ.get("SANCHO_NERD_BIN", str(SETUP / "nerd-run.py"))
TEST_ALL = os.environ.get("SANCHO_TEST_ALL_BIN", str(SETUP / "test-all.py"))
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho"))
MAX_STAGES_PER_RUN = 6
STAGE_LINE = re.compile(r"^(\s*-\s*)(\{.*\})\s*(#.*)?$")


def now() -> str:
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def resolve(job: str) -> Path:
    p = (ROOT / job) if "/" in job else (ROOT / "_queue" / "jobs" / (job if job.endswith(".md") else job + ".md"))
    if not p.exists():
        cands = sorted((ROOT / "_queue" / "jobs").glob(f"*{job}*.md"))
        if len(cands) == 1:
            p = cands[0]
    p = p.resolve()
    if not p.exists() or (ROOT / "_queue" / "jobs").resolve() not in p.parents:
        raise SystemExit(f"job-run: no job file matching '{job}' in _queue/jobs/")
    return p


def stages(text: str) -> list[tuple[int, dict]]:
    """(line index, stage map) for every `- {…}` line under `stages:` in the frontmatter."""
    lines, out, inside = text.splitlines(), [], False
    for i, ln in enumerate(lines[1:], 1):
        if ln.strip() == "---":
            break
        if ln.startswith("stages:"):
            inside = True
            continue
        if inside:
            m = STAGE_LINE.match(ln)
            if m:
                out.append((i, _parse_scalar(m.group(2))))
            elif ln.strip() and not ln.startswith((" ", "\t")):
                inside = False
    return out


def set_stage(text: str, idx: int, **fields) -> str:
    lines = text.splitlines()
    ln = lines[idx]
    for k, v in fields.items():
        if re.search(rf"\b{k}:\s*[^,}}]*", ln):
            ln = re.sub(rf"\b{k}:\s*[^,}}]*", f"{k}: {v}", ln, count=1)
        else:
            ln = ln.replace("}", f", {k}: {v}}}", 1) if "}" in ln else ln
    lines[idx] = ln
    return "\n".join(lines) + "\n"


def set_current(text: str, name: str) -> str:
    if re.search(r"(?m)^current:", text):
        return re.sub(r"(?m)^current:.*$", f"current: {name}", text, count=1)
    return text.replace("\n---\n", f"\ncurrent: {name}\n---\n", 1)


def log(text: str, line: str) -> str:
    return text.rstrip("\n") + f"\n- {now()} job.run: {line}\n"


def write(p: Path, text: str):
    tmp = p.with_name(f".{p.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


def push(level: str, msg: str):
    subprocess.run(["python3", str(SETUP / "notify.py"), level, msg[:500], "--key=job-run"], capture_output=True, timeout=30)


def task_for(job: Path, st: dict) -> str:
    if st.get("task_file"):
        p = (ROOT / str(st["task_file"])).resolve()
        if ROOT.resolve() in p.parents and p.exists():
            return p.read_text(encoding="utf-8")
    if st.get("task"):
        return str(st["task"])
    rel = job.relative_to(ROOT)
    return (f"Do stage `{st.get('name')}` of the job in `{rel}` (note: {st.get('note', '')}). Read the job file, the project it names, "
            f"and _design/STATUS.md first. Do only this stage. When it is done and tested, say so plainly; if it cannot be finished "
            f"without Gordon, write the question under 'Open for Gordon' in _design/STATUS.md.")


STAGE_CONTRACT = ("\n\nThis is one stage of a job run by job.run. Before your Receipt line, end with exactly one line: "
                  "`Stage: done` if the stage is complete and tested, or `Stage: blocked: <why>` if it is not. Anything else counts as blocked.")


def run_stage(job: Path, st: dict, rid: str, attempt: int) -> tuple[bool, str]:
    env = {**os.environ, "SANCHO_REQUEST_ID": f"{rid}-{st.get('name')}-{attempt}", "SANCHO_REQUESTED_BY": f"job.run {job.stem}"}
    env.pop("SANCHO_REQUEST_FILE", None)
    r = subprocess.run(["python3", NERD, "--task", task_for(job, st) + STAGE_CONTRACT], env=env, capture_output=True, text=True)
    marks = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("Stage:")]
    verdict = marks[-1] if marks else "Stage: (no verdict line)"
    if r.returncode != 0 or verdict != "Stage: done":
        return False, verdict
    # a session doesn't grade its own homework (ERRORS.md #6): the board is run here, outside the sandbox
    t = subprocess.run(["python3", TEST_ALL], cwd=ROOT, capture_output=True, text=True, timeout=1200)
    if t.returncode != 0:
        fails = [l for l in t.stdout.splitlines() if "| FAIL" in l]
        return False, f"session said done but tests are red: {'; '.join(f.split('|')[1].strip() for f in fails)[:200] or t.stdout.strip()[-200:]}"
    return True, verdict + " · tests green"


def walk(job: Path, rid: str) -> str:
    text = job.read_text(encoding="utf-8")
    fm, _ = read_frontmatter(job)
    ran = 0
    while ran < MAX_STAGES_PER_RUN:
        sts = stages(text)
        cur = str(fm.get("current") or "")
        pos = next((i for i, (_, s) in enumerate(sts) if s.get("name") == cur), None)
        if pos is None:
            pos = next((i for i, (_, s) in enumerate(sts) if s.get("status") not in ("done", "skipped")), None)
        if pos is None:
            text = log(text, "all stages done")
            write(job, text)
            push("info", f"Job {job.stem}: all stages done.")
            return "all stages done"
        idx, st = sts[pos]
        name = st.get("name")
        if st.get("status") in ("done", "skipped"):
            nxt = sts[pos + 1][1].get("name") if pos + 1 < len(sts) else None
            if not nxt:
                text = log(text, "all stages done")
                write(job, text)
                push("info", f"Job {job.stem}: all stages done.")
                return "all stages done"
            text = set_current(text, nxt)
            fm["current"] = nxt
            continue
        if str(st.get("gate") or "") == "human":
            text = set_stage(text, idx, status="waiting")
            text = set_current(text, name)
            text = log(text, f"stopped at human gate `{name}`")
            write(job, text)
            push("info", f"Job {job.stem} is waiting for you: {name}. {st.get('note', '')}")
            return f"stopped at human gate {name}"
        text = set_current(set_stage(text, idx, status="active"), name)
        text = log(text, f"stage `{name}` started")
        write(job, text)
        ok, last = run_stage(job, st, rid, 1)
        if not ok:
            text = log(job.read_text(encoding="utf-8"), f"stage `{name}` failed once ({last[:160]}); retrying")
            write(job, text)
            ok, last = run_stage(job, st, rid, 2)
        text = job.read_text(encoding="utf-8")  # the stage's session may have edited the job file itself
        idx = next(i for i, s in stages(text) if s.get("name") == name)
        if not ok:
            text = set_stage(text, idx, status="failed")
            text = log(text, f"stage `{name}` failed twice; stopped ({last[:160]})")
            write(job, text)
            push("info", f"Job {job.stem} stopped: stage {name} failed twice. {last[:200]}")
            return f"stage {name} failed twice"
        text = set_stage(text, idx, status="done")
        text = log(text, f"stage `{name}` done ({last[:160]})")
        write(job, text)
        fm, _ = read_frontmatter(job)
        ran += 1
    push("info", f"Job {job.stem}: paused after {MAX_STAGES_PER_RUN} stages in one run; run job.run again to continue.")
    return f"paused after {MAX_STAGES_PER_RUN} stages"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("job", help="job file name or path under _queue/jobs/")
    ap.add_argument("--foreground", action="store_true", help="walk here instead of detaching (tests, debugging)")
    a = ap.parse_args()
    job = resolve(a.job)
    rid = os.environ.get("SANCHO_REQUEST_ID") or datetime.datetime.now().strftime("manual-%Y%m%dT%H%M%S")
    if not a.foreground:
        subprocess.Popen(["python3", __file__, str(job), "--foreground"], cwd=ROOT, start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env={**os.environ, "SANCHO_REQUEST_ID": rid})
        print(f"job-run: started on {job.relative_to(ROOT)} in the background; progress is written to the job file; a push comes when it stops")
        return 0
    STATE.mkdir(parents=True, exist_ok=True)
    lock = open(STATE / f"job-run.{job.stem}.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"job-run: {job.stem} is already being walked")
        return 1
    outcome = walk(job, rid)
    res = ROOT / "_queue" / "results" / f"{rid}.job.md"
    res.parent.mkdir(parents=True, exist_ok=True)
    res.write_text(f"---\ncommand: job.run\njob: {job.relative_to(ROOT)}\nfinished_at: {now()}\noutcome: {outcome}\n---\n{outcome}\n")
    print(f"job-run: {outcome}")
    return 0 if "failed" not in outcome else 1


if __name__ == "__main__":
    sys.exit(main())
