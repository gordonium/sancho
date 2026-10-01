#!/usr/bin/env python3
"""
name: sancho-enqueue
type: script
description: Write one request file to _queue/requests/ (the documented name and frontmatter, including `session:`, the sender), optionally wait for its result and print it. `--task-file` names a task file for nerd.run instead of a shell-composed body (ERRORS.md #7). `--wait` first checks HEALTH.md: a stale watcher is reported at once instead of after the timeout, and the wait is timed on the clock that stops while the Mac sleeps (ERRORS.md #8).
why: Every Mac-side run goes through the queue so there is one audit trail (architecture §1); schedules enqueue instead of running scripts directly, so nightly runs show up in results/ and HEALTH.md like any other.
reads: _queue/results/ and _queue/HEALTH.md (when --wait)
writes: _queue/requests/<UTC stamp>_<command>_<6 hex>.md
schedule:
test: _setup/tests/watcher/
"""
from __future__ import annotations
import os, sys, time, secrets, argparse, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root

HEALTH_STALE_S = 300  # the watcher rewrites HEALTH.md every tick (≤ 60 s while awake)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command")
    ap.add_argument("args", nargs="*", help="positional args passed to the script")
    ap.add_argument("--by", default=os.environ.get("SANCHO_REQUESTED_BY", "claude-code"))
    ap.add_argument("--session", default="", help="who is sending: cowork hop N / interactive / nerd.run <id> / schedule <name>")
    ap.add_argument("--job", default="")
    ap.add_argument("--wait", type=int, default=0, help="seconds to wait for the result")
    ap.add_argument("--task-file", default="", help="nerd.run: a task file inside the tree (preferred to --body)")
    ap.add_argument("--body", default="", help="free text below the frontmatter; nerd.run needs it to end with the line '-- end of task --'")
    a = ap.parse_args()
    root = tree_root()
    q = root / "_queue"
    session = a.session or os.environ.get("SANCHO_SESSION") or (f"schedule {a.command}" if a.by == "launchd" else a.by)
    if a.task_file:
        p = (root / a.task_file).resolve()
        if root.resolve() not in p.parents or not p.is_file():
            print(f"sancho-enqueue: --task-file must be a file inside the tree: {a.task_file}")
            return 2
        a.task_file = str(p.relative_to(root.resolve()))
    (q / "requests").mkdir(parents=True, exist_ok=True)
    t = datetime.datetime.now(datetime.timezone.utc)
    name = f"{t.strftime('%Y%m%dT%H%M%SZ')}_{a.command}_{secrets.token_hex(3)}.md"
    fm = [f"command: {a.command}", f"args: [{', '.join(a.args)}]", f"requested_by: {a.by}", f"session: {session}",
          f"requested_at: {t.replace(microsecond=0).isoformat()}"] + ([f"job: {a.job}"] if a.job else []) \
        + ([f"task_file: {a.task_file}"] if a.task_file else [])
    tmp = q / "requests" / f".{name}.tmp"
    tmp.write_text("---\n" + "\n".join(fm) + "\n---\n" + (a.body.rstrip() + "\n" if a.body else ""), encoding="utf-8")
    os.replace(tmp, q / "requests" / name)  # atomic: the watcher never sees a half-written request
    print(f"queued {name}")
    if a.wait:
        h = q / "HEALTH.md"
        stale = h.exists() and time.time() - h.stat().st_mtime > HEALTH_STALE_S
        if stale:
            print(f"watcher looks stopped: HEALTH.md last written {int((time.time() - h.stat().st_mtime) / 60)} min ago; "
                  "the request stays queued and runs when the watcher next ticks")
            return 3
        res = q / "results" / name
        end = time.monotonic() + a.wait  # monotonic: a Mac that sleeps mid-wait doesn't spend the wait asleep
        while time.monotonic() < end:
            if res.exists():
                print(res.read_text(encoding="utf-8"))
                return 0 if "status: ok" in res.read_text() else 1
            time.sleep(1)
        print(f"no result after {a.wait} s; check _queue/HEALTH.md for when the watcher last ran")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
