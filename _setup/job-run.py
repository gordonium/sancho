#!/usr/bin/env python3
"""
name: job-run
type: command
description: Walk a job file (_queue/jobs/*.md) stage by stage, running each stage as a nerd.run session, advancing `current` on success, stopping at any `gate: human` stage. A failing stage gets a troubleshoot loop: up to 3 attempts; attempt 2 and later carry the evidence (test board, failing suites' output, log tail, the failed session's transcript tail) and a diagnose-first instruction; two attempts failing on identical evidence stop early (no progress). A session may end `Stage: blocked: <what Gordon must do>`, which pauses the job at a gate instead of failing it. Pushes (Gordon, 2026-10-01): warn on every stop that needs him (gate, blocked, stopped) with the evidence path; info for completions. `--auto` (queued by the watcher after a nerd.run result for the job lands, only for jobs with `advance: auto`) never re-runs a failed or blocked stage and yields to a live Nerd lease. A stage with `task_template:` and `vars:` is rendered (every `<var>` replaced) to _queue/inbox/_rendered/<job>_<stage>.md and run as the nerd.run task file, so the template's frontmatter (`quarantine_reader`, `writes_only`) governs the session. A job that says a blocked stage is not a blocked job (`on_blocked: continue`, or the sentence in its body) records a blocked stage with its reason, pushes nothing for it and moves on; it pushes one info per 25 finished stages and one warn at the end. A stage whose transcript shows a write outside its `writes_only` list stops the job with a warn, no retry. `--require-green` runs the board first and starts nothing on red. Detaches at once so the watcher stays free; progress lives in the job file.
why: Gordon wants full rounds without being the messenger; cold Cowork runs cannot schedule their next hop, so the Mac is the loop's engine (STATUS.md 2026-10-01). "Retried once seems too fragile" [gordon 2026-10-01]. State lives in the job file, never in memory (CLAUDE.md), so a crash or sleep loses nothing: rerun resumes at `current`.
reads: the job file; stage fields `task:` / `task_file:` / `note:`; _setup/nerd-run.py; _setup/test-all.py (run outside the sandbox after every attempt); _queue/log/; _queue/results/*.transcript.jsonl; _queue/leases/
writes: the job file (stage status, `current`, `history` lines in the body); _queue/inbox/_rendered/<job>_<stage>.md (rendered stage task files); _queue/results/<id>-<stage>-evidence-<n>.md; _queue/results/<request id>.job.md (final summary); a continuation request after MAX_STAGES_PER_RUN; ~/.local/state/sancho/advance-pending.json; Pushover messages
schedule:
test: _setup/tests/job-run/
"""
from __future__ import annotations
import os, re, sys, json, time, fcntl, argparse, datetime, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root, read_frontmatter, _parse_scalar, live_leases, enqueue, advance_pending, nerd_admit, EX_DEFER

ROOT = tree_root()
SETUP = ROOT / "_setup"
RESULTS = ROOT / "_queue" / "results"
NERD = os.environ.get("SANCHO_NERD_BIN", str(SETUP / "nerd-run.py"))
TEST_ALL = os.environ.get("SANCHO_TEST_ALL_BIN", str(SETUP / "test-all.py"))
STATE = Path(os.environ.get("SANCHO_STATE", Path.home() / ".local/state/sancho"))
MAX_STAGES_PER_RUN = 6
MAX_ATTEMPTS = 3
PROGRESS_EVERY = 25  # a continuing job (blocked stage is not a blocked job) pushes one info per this many finished stages
NERD_WAIT_S = int(os.environ.get("SANCHO_JOB_NERD_WAIT", "2400"))  # a nerd.run in flight finishes within its 30-min timeout
STAGE_LINE = re.compile(r"^(\s*-\s*)(\{.*\})\s*(#.*)?$")
SESSION = os.environ.get("SANCHO_SESSION") or "manual"


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


def flat(v: str, n: int = 160) -> str:
    """A value safe inside a `{k: v, …}` stage line."""
    return re.sub(r"[,{}\"'\n]+", " ", str(v)).strip()[:n]


def set_stage(text: str, idx: int, **fields) -> str:
    lines = text.splitlines()
    ln = lines[idx]
    for k, v in fields.items():
        if v is None:
            ln = re.sub(rf",\s*{k}:\s*[^,}}]*", "", ln, count=1)
        elif re.search(rf"\b{k}:\s*[^,}}]*", ln):
            ln = re.sub(rf"\b{k}:\s*[^,}}]*", f"{k}: {v}", ln, count=1)
        else:
            end = ln.rfind("}")  # the stage map's own closing brace, not a nested `vars: {…}`
            ln = ln[:end] + f", {k}: {v}" + ln[end:] if end >= 0 else ln
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


def push(job: Path, level: str, msg: str, reason: str | None = None):
    argv = ["python3", str(SETUP / "notify.py"), level, msg[:500], f"--key=job-run:{job.stem}", f"--session=job.run {job.stem} ({SESSION})"]
    subprocess.run(argv + ([f"--reason={reason}"] if reason else []), capture_output=True, timeout=30)


def render(job: Path, st: dict) -> Path | None:
    """A stage with `task_template: <path>` and `vars: {k: v}`: the template with every `<k>` replaced, written to
    _queue/inbox/_rendered/<job>_<stage>.md and run as the nerd.run task FILE (so its frontmatter, `quarantine_reader`
    included, is the session's). None when the stage has no template."""
    if not st.get("task_template"):
        return None
    src = (ROOT / str(st["task_template"])).resolve()
    if ROOT.resolve() not in src.parents or not src.exists():
        raise SystemExit(f"job-run: stage {st.get('name')}: task_template not found inside the tree: {st['task_template']}")
    text = src.read_text(encoding="utf-8")
    vs = st.get("vars") if isinstance(st.get("vars"), dict) else {}
    for k, v in vs.items():
        if not re.fullmatch(r"[\w.-]+", str(v)):
            raise SystemExit(f"job-run: stage {st.get('name')}: var {k} is not a plain word: {v!r}")
        text = text.replace(f"<{k}>", str(v))
    out = ROOT / "_queue" / "inbox" / "_rendered" / f"{job.stem}_{st.get('name')}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    write(out, text)
    return out


def continues(job: Path) -> bool:
    """A job where a blocked stage is not a blocked job: `on_blocked: continue` in the frontmatter, or the body says so
    ("a blocked person is not a blocked job"). The stage is marked blocked with its reason, nothing is pushed for it,
    and the walk moves on."""
    fm, body = read_frontmatter(job)
    return str(fm.get("on_blocked") or "") == "continue" or bool(re.search(r"blocked \w+ is not a blocked job", body))


def progress(text: str) -> tuple[int, int, int]:
    """(finished, total, blocked) over the stages that are the job's repeated work: the templated stages when there are any
    (backfill-people: the 208 people, not the census or the review gate), else every stage without a gate. Finished counts
    done and blocked."""
    sts = [s for _, s in stages(text) if not s.get("gate")]
    work = [s for s in sts if s.get("task_template")] or sts
    blocked = sum(1 for s in work if s.get("status") == "blocked")
    return sum(1 for s in work if s.get("status") == "done") + blocked, len(work), blocked


TMP_ROOTS = ("/tmp/", "/private/tmp/", "/private/var/folders/", "/var/folders/")


def stray_writes(transcript: Path, allowed: list[str], job: Path) -> list[str]:
    """Paths a session's Write/Edit calls (and any mv/cp it ran) touched outside `allowed` (tree-relative). Temp folders
    and the job file itself do not count. Read from the transcript, so other writers on the Mac (pipeline, watcher) are not blamed.
    Limit: a write made by a script the session ran is not seen."""
    ok = {str(a) for a in allowed} | {str(job.relative_to(ROOT))}
    bad = []
    try:
        lines = transcript.read_text(errors="replace").splitlines()
    except OSError:
        return bad
    for ln in lines:
        try:
            ev = json.loads(ln)
        except ValueError:
            continue
        content = (ev.get("message") or {}).get("content") if isinstance(ev, dict) and ev.get("type") == "assistant" else None
        for item in content if isinstance(content, list) else []:
            if not (isinstance(item, dict) and item.get("type") == "tool_use"):
                continue
            inp = item.get("input") or {}
            if item.get("name") in ("Write", "Edit", "NotebookEdit"):
                p = os.path.normpath(os.path.join(ROOT, str(inp.get("file_path") or inp.get("notebook_path") or "")))
                inside = p.startswith(str(ROOT) + os.sep)
                rel = os.path.relpath(p, ROOT) if inside else p
                if rel not in ok and (inside or not p.startswith(TMP_ROOTS)) and rel not in bad:
                    bad.append(rel)
            elif item.get("name") == "Bash" and re.search(r"(?:^|[;&|]\s*)(mv|cp)\s", str(inp.get("command") or "")):
                bad.append("Bash: " + " ".join(str(inp.get("command")).split())[:80])
    return bad


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


STAGE_CONTRACT = ("\n\nThis is one stage of a job run by job.run. Before your Receipt line, end with exactly one of these lines: "
                  "`Stage: done` if the stage is complete and tested; `Stage: failed: <cause>` if you could not finish it and another "
                  "attempt could; `Stage: blocked: <what Gordon must do>` only if nothing more can happen without Gordon (this pauses the job "
                  "at a gate and warns him). A missing line counts as failed. job.run re-runs the test board itself, outside your sandbox.")


CONTINUE_NOTE = (" In THIS job a blocked stage does not pause the job: the stage is recorded as blocked with your reason, nobody is "
                 "pushed, and the job moves on to the next stage; so write what you can first, then say what is blocked.")


def retry_brief(attempt: int, prev_verdict: str, evidence: Path) -> str:
    return (f"\n\nThis is attempt {attempt} of {MAX_ATTEMPTS} for this stage. The previous attempt failed: {prev_verdict}\n"
            f"Evidence (read it first): {evidence.relative_to(ROOT)} (test board, failing suites' output, log tail, the failed session's last 40 lines).\n"
            "Diagnose first: before changing anything, write one line starting `Cause:` naming what made the previous attempt fail, "
            "citing the evidence. Then fix that cause, and only that, unless the evidence shows more.")


def verdict_of(out: str) -> tuple[str, str]:
    marks = [l.strip() for l in out.splitlines() if l.strip().startswith("Stage:")]
    v = marks[-1] if marks else "Stage: (no verdict line)"
    if v == "Stage: done":
        return "done", v
    if v.startswith("Stage: blocked"):
        return "blocked", v
    return "failed", v


def board() -> tuple[bool, str]:
    """The test board, run here (outside the sandbox): a session doesn't grade its own homework (ERRORS.md #6)."""
    try:
        t = subprocess.run(["python3", TEST_ALL, "--fail-tail", "30"], cwd=ROOT, capture_output=True, text=True, timeout=1200)
    except subprocess.TimeoutExpired:
        return False, "test-all timed out after 1200 s"
    return t.returncode == 0, t.stdout.strip()


def signature(text: str) -> str:
    """Failure evidence with the noise taken out (temp paths, times, counts of seconds), to tell 'no progress' from 'different failure'."""
    text = re.sub(r"/(?:private/)?(?:var/folders|tmp)/\S+", "<tmp>", text)
    text = re.sub(r"\d{4}-\d\d-\d\d[ T]\d\d:\d\d(:\d\d)?\S*", "<time>", text)
    text = re.sub(r"\b\d+(\.\d+)? ?s\b", "<n>s", text)
    return text.strip()


def tail_lines(p: Path, n: int, width: int = 400) -> str:
    try:
        return "\n".join(l[:width] for l in p.read_text(errors="replace").splitlines()[-n:])
    except OSError:
        return "(not found)"


def write_evidence(rid: str, name: str, attempt: int, verdict: str, nerd_out: str, board_text: str) -> Path:
    RESULTS.mkdir(parents=True, exist_ok=True)
    p = RESULTS / f"{rid}-{name}-evidence-{attempt}.md"
    logs = sorted((ROOT / "_queue" / "log").glob("*.log"))
    body = (f"---\ncommand: job.run evidence\nstage: {name}\nattempt: {attempt}\nwritten_at: {now()}\n---\n"
            f"# Evidence: stage `{name}`, attempt {attempt}\n\n## Verdict\n{verdict}\n\n"
            f"## Test board (run by job.run outside the sandbox)\n```\n{board_text[-6000:] or '(not run)'}\n```\n\n"
            f"## nerd-run output (tail)\n```\n{nerd_out.strip()[-3000:]}\n```\n\n"
            f"## Watcher log (tail)\n```\n{tail_lines(logs[-1], 20) if logs else '(no log)'}\n```\n\n"
            f"## Session transcript (last 40 lines, each cut at 400 chars)\n```\n{tail_lines(RESULTS / f'{rid}-{name}-{attempt}.transcript.jsonl', 40)}\n```\n")
    p.write_text(body, encoding="utf-8")
    return p


def stage_writes(job: Path, st: dict):
    """The `writes_only` a stage's session will declare (only a rendered task file carries it to nerd-run)."""
    rendered = render(job, st)
    return read_frontmatter(rendered)[0].get("writes_only") if rendered else None


def wait_for_nerd(only=None) -> str | None:
    """None when no Nerd holds the tree; otherwise who does. An interactive Nerd is not waited for (it may run all day);
    a nerd.run in flight is, up to NERD_WAIT_S (must-never 5: one writer), unless this stage's `only` (its writes_only)
    cannot meet the running session's (nerd_admit: two at once at most)."""
    end = time.monotonic() + NERD_WAIT_S
    while True:
        live = live_leases(ROOT)
        inter = [p.stem for p, fm in live if fm.get("kind") == "interactive"]
        if inter:
            return f"interactive Nerd ({inter[0]})"
        if not live or nerd_admit(ROOT, only)[0]:
            return None
        if time.monotonic() >= end:
            return f"nerd.run still running ({live[0][0].stem})"
        time.sleep(min(30, max(1, NERD_WAIT_S // 10)))


def attempt_stage(job: Path, st: dict, rid: str, attempt: int, brief: str) -> tuple[str, str, str, str]:
    """Run one attempt. Returns (kind done|blocked|failed, verdict, nerd output, board text)."""
    name = st.get("name")
    env = {**os.environ, "SANCHO_REQUEST_ID": f"{rid}-{name}-{attempt}", "SANCHO_REQUESTED_BY": f"job.run {job.stem}",
           "SANCHO_SESSION": f"job.run {job.stem} stage {name} attempt {attempt}"}
    env.pop("SANCHO_REQUEST_FILE", None)
    tail = STAGE_CONTRACT + (CONTINUE_NOTE if continues(job) else "") + brief
    rendered = render(job, st)
    if rendered:
        argv = ["python3", NERD, "--task-file", str(rendered.relative_to(ROOT)), "--append", tail]
    else:
        argv = ["python3", NERD, "--task", task_for(job, st) + tail]
    r = subprocess.run(argv, env=env, capture_output=True, text=True)
    if r.returncode == EX_DEFER:  # another session got in between the wait and the start: not an attempt, the watcher resumes the job
        return "busy", (r.stdout.strip().splitlines() or ["a Nerd session"])[-1][:200], r.stdout, ""
    kind, verdict = verdict_of(r.stdout)
    only = read_frontmatter(rendered)[0].get("writes_only") if rendered else st.get("writes_only")
    if only:
        stray = stray_writes(RESULTS / f"{rid}-{name}-{attempt}.transcript.jsonl", only if isinstance(only, list) else [only], job)
        if stray:
            return "scope", f"stage wrote outside its scope ({'; '.join(stray)[:300]}); allowed: {', '.join(map(str, only if isinstance(only, list) else [only]))}", r.stdout, ""
    if "quarantine guard did not fire" in r.stdout:
        return "scope", "the quarantine guard did not fire in a session that read a legacy folder (see nerd-run's line in the evidence)", r.stdout, ""
    if kind == "blocked":
        return kind, verdict, r.stdout, ""
    if r.returncode != 0 and kind == "done":
        kind, verdict = "failed", f"nerd-run failed: {(r.stdout.strip().splitlines() or ['(no output)'])[-1][:200]}"
    green, btext = board()
    if kind == "done" and not green:
        fails = [l.split("|")[1].strip() for l in btext.splitlines() if "| FAIL" in l]
        kind, verdict = "failed", f"session said done but tests are red: {'; '.join(fails)[:200] or btext[-200:]}"
    if kind == "done":
        verdict += " · tests green"
    return kind, verdict, r.stdout, btext


def run_stage(job: Path, st: dict, rid: str) -> tuple[str, str, Path | None]:
    """The troubleshoot loop. Returns (done|blocked|failed|busy, last verdict, evidence path or None)."""
    name = st.get("name")
    brief, prev_sig, evidence = "", None, None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        busy = wait_for_nerd(stage_writes(job, st))
        if busy:
            return "busy", busy, evidence
        kind, verdict, out, btext = attempt_stage(job, st, rid, attempt, brief)
        if kind in ("done", "blocked", "busy"):
            return kind, verdict, evidence
        evidence = write_evidence(rid, name, attempt, verdict, out, btext)
        if kind == "scope":  # not a thing another attempt fixes: the job stops and Gordon is warned
            write(job, log(job.read_text(encoding="utf-8"), f"stage `{name}` attempt {attempt}: {flat(verdict, 300)}; evidence {evidence.relative_to(ROOT)}"))
            return "failed", verdict, evidence
        sig = signature(btext if btext and "FAIL" in btext else verdict)
        text = log(job.read_text(encoding="utf-8"), f"stage `{name}` attempt {attempt} failed ({flat(verdict)}); evidence {evidence.relative_to(ROOT)}")
        write(job, text)
        if sig == prev_sig:
            return "failed", f"identical failure on attempts {attempt - 1} and {attempt} (no progress): {verdict}", evidence
        prev_sig = sig
        brief = retry_brief(attempt + 1, verdict, evidence)
    return "failed", f"failed {MAX_ATTEMPTS} attempts: {verdict}", evidence


def stage_idx(text: str, name: str) -> int:
    return next(i for i, s in stages(text) if s.get("name") == name)


def walk(job: Path, rid: str, auto: bool) -> tuple[str, bool]:
    """Returns (outcome, stopped_for_a_problem)."""
    text = job.read_text(encoding="utf-8")
    fm, _ = read_frontmatter(job)
    ran = 0
    cont = continues(job)
    label = str(fm.get("job") or job.stem)

    def tally(t: str) -> str:
        done, total, blocked = progress(t)
        return f"{label}: {done}/{total}, {blocked} blocked"

    while ran < MAX_STAGES_PER_RUN:
        sts = stages(text)
        cur = str(fm.get("current") or "")
        pos = next((i for i, (_, s) in enumerate(sts) if s.get("name") == cur), None)
        if pos is None:
            pos = next((i for i, (_, s) in enumerate(sts) if s.get("status") not in ("done", "skipped")), None)
        if pos is None or (sts[pos][1].get("status") in ("done", "skipped") and pos + 1 >= len(sts)):
            write(job, log(text, "all stages done"))
            if cont and progress(text)[2]:
                push(job, "warn", f"Job {job.stem} finished ({tally(text)}); the blocked ones need you.", reason="job-gate")
            else:
                push(job, "info", f"Job {job.stem}: all stages done.")
            return "all stages done", False
        idx, st = sts[pos]
        name, status = st.get("name"), str(st.get("status") or "")
        if status in ("done", "skipped") or (cont and status == "blocked"):
            if pos + 1 >= len(sts):  # a continuing job whose last stage is blocked
                write(job, log(text, f"all stages walked ({tally(text)})"))
                push(job, "warn", f"Job {job.stem} finished ({tally(text)}); the blocked ones need you.", reason="job-gate")
                return f"all stages walked ({tally(text)})", False
            nxt = sts[pos + 1][1].get("name")
            text = set_current(text, nxt)
            fm["current"] = nxt
            continue
        if auto and status in ("blocked", "failed", "waiting"):
            # the warn went out when it stopped; an automatic pass neither re-runs it nor pushes again
            write(job, log(text, f"auto: stage `{name}` is {status}; left for Gordon or a manual job.run"))
            return f"left at {status} stage {name}", False
        if str(st.get("gate") or "") == "human":
            text = set_current(set_stage(text, idx, status="waiting"), name)
            write(job, log(text, f"stopped at human gate `{name}`"))
            push(job, "warn", f"Job {job.stem} is waiting for you at {name}{' (' + tally(text) + ')' if cont else ''}: {st.get('note', '')}", reason="job-gate")
            return f"stopped at human gate {name}", False
        text = set_current(set_stage(text, idx, status="active", blocked=None), name)
        write(job, log(text, f"stage `{name}` started"))
        kind, last, evidence = run_stage(job, st, rid)
        text = job.read_text(encoding="utf-8")  # the stage's session may have edited the job file itself
        idx = stage_idx(text, name)
        ev = f" Evidence: {evidence.relative_to(ROOT)}" if evidence else ""
        if kind == "busy":
            advance_pending(STATE, job.stem, last)
            write(job, log(text, f"stage `{name}` not started: {last} holds the tree; the watcher resumes this job when the lease clears"))
            push(job, "info", f"Job {job.stem}: waiting for {last} before stage {name}.")
            return f"waiting: {last}", False
        if kind == "blocked":
            what = flat(re.sub(r"^Stage:\s*blocked:?\s*", "", last), 200) or "(no reason given)"
            text = set_stage(text, idx, status="blocked", blocked=what)
            if cont:  # a blocked stage is not a blocked job: record it, push nothing, move on
                write(job, log(text, f"stage `{name}` blocked, recorded, job continues: {what}"))
                text = job.read_text(encoding="utf-8")
                fm["current"] = name  # the next pass steps over it
                ran += 1
                if progress(text)[0] % PROGRESS_EVERY == 0:
                    push(job, "info", tally(text))
                continue
            write(job, log(text, f"stage `{name}` blocked, paused for Gordon: {what}"))
            push(job, "warn", f"Job {job.stem} paused at {name}; needs you: {what}.{ev}", reason="job-gate")
            return f"blocked at {name}: {what}", False
        if kind == "failed":
            text = set_stage(text, idx, status="failed")
            write(job, log(text, f"stage `{name}` stopped: {flat(last, 300)}.{ev}"))
            push(job, "warn", f"Job {job.stem} stopped at {name}: {last[:200]}.{ev}", reason="job-stopped")
            return f"stage {name} failed: {last[:200]}", True
        text = set_stage(text, idx, status="done")
        write(job, log(text, f"stage `{name}` done ({flat(last)})"))
        fm, _ = read_frontmatter(job)
        text = job.read_text(encoding="utf-8")
        ran += 1
        if cont and progress(text)[0] % PROGRESS_EVERY == 0:
            push(job, "info", tally(text))
    req = enqueue(ROOT, "job.run", [job.stem] + (["--auto"] if auto else []), "job.run", f"job.run continuation of {rid}", job.stem)
    write(job, log(job.read_text(encoding="utf-8"), f"{MAX_STAGES_PER_RUN} stages in one run; continuation queued ({req.name})"))
    if not cont:  # a continuing job reports every PROGRESS_EVERY stages instead of every run
        push(job, "info", f"Job {job.stem}: {MAX_STAGES_PER_RUN} stages done in one run; continuing.")
    return f"paused after {MAX_STAGES_PER_RUN} stages; continuation queued", False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("job", help="job file name or path under _queue/jobs/")
    ap.add_argument("--foreground", action="store_true", help="walk here instead of detaching (tests, debugging)")
    ap.add_argument("--auto", action="store_true", help="queued by the watcher: only for jobs with `advance: auto`; never re-runs a failed or blocked stage")
    ap.add_argument("--require-green", action="store_true", help="run the test board first (outside any sandbox); on red, start nothing and warn")
    a = ap.parse_args()
    job = resolve(a.job)
    rid = os.environ.get("SANCHO_REQUEST_ID") or datetime.datetime.now().strftime("manual-%Y%m%dT%H%M%S")
    if a.auto and str(read_frontmatter(job)[0].get("advance") or "manual") != "auto":
        print(f"job-run: {job.stem} is not `advance: auto`; nothing done")
        return 0
    if not a.foreground:
        subprocess.Popen(["python3", __file__, str(job), "--foreground"] + (["--auto"] if a.auto else []) + (["--require-green"] if a.require_green else []), cwd=ROOT, start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env={**os.environ, "SANCHO_REQUEST_ID": rid})
        print(f"job-run: started on {job.relative_to(ROOT)} in the background ({'auto' if a.auto else 'manual'}; session {SESSION}); progress is written to the job file; a push comes when it stops")
        return 0
    STATE.mkdir(parents=True, exist_ok=True)
    lock = open(STATE / f"job-run.{job.stem}.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"job-run: {job.stem} is already being walked")
        return 1
    advance_pending(STATE, job.stem, drop=True)
    if a.require_green:
        busy = wait_for_nerd()  # the board is only authoritative with no Nerd mid-write (and outside its sandbox)
        green, btext = (False, f"not run: {busy} holds the tree") if busy else board()
        fails = "; ".join(l.split("|")[1].strip() for l in btext.splitlines() if "| FAIL" in l) or btext[-200:]
        write(job, log(job.read_text(encoding="utf-8"), "start check: test board " + ("green" if green else f"red, job not started ({flat(fails, 200)})")))
        if not green:
            push(job, "warn", f"Job {job.stem} not started: the test board is red ({fails[:200]}).", reason="job-stopped")
            (RESULTS / f"{rid}.job.md").parent.mkdir(parents=True, exist_ok=True)
            (RESULTS / f"{rid}.job.md").write_text(f"---\ncommand: job.run\nstatus: failed\njob: {job.relative_to(ROOT)}\nsession: {SESSION}\n"
                                                  f"finished_at: {now()}\noutcome: not started, board red\n---\n{btext[-3000:]}\n")
            print(f"job-run: not started: test board red ({fails[:200]})")
            return 1
    outcome, problem = walk(job, rid, a.auto)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{rid}.job.md").write_text(f"---\ncommand: job.run\nstatus: {'failed' if problem else 'ok'}\njob: {job.relative_to(ROOT)}\n"
                                          f"session: {SESSION}\nfinished_at: {now()}\noutcome: {flat(outcome, 300)}\n---\n{outcome}\n")
    print(f"job-run: {outcome}")
    return 1 if problem else 0


if __name__ == "__main__":
    sys.exit(main())
