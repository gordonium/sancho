#!/usr/bin/env python3
"""
name: sancho-enqueue
type: script
description: Write one request file to _queue/requests/ (the documented name and frontmatter), optionally wait for its result and print it. Used by launchd schedules and by sessions that have a shell.
why: Every Mac-side run goes through the queue so there is one audit trail (architecture §1); schedules enqueue instead of running scripts directly, so nightly runs show up in results/ and HEALTH.md like any other.
reads: _queue/results/ (when --wait)
writes: _queue/requests/<UTC stamp>_<command>_<6 hex>.md
schedule:
test: _setup/tests/watcher/
"""
from __future__ import annotations
import os, sys, time, secrets, argparse, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from sancho_lib import tree_root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command")
    ap.add_argument("args", nargs="*", help="positional args passed to the script")
    ap.add_argument("--by", default=os.environ.get("SANCHO_REQUESTED_BY", "claude-code"))
    ap.add_argument("--job", default="")
    ap.add_argument("--wait", type=int, default=0, help="seconds to wait for the result")
    ap.add_argument("--body", default="", help="free text below the frontmatter (nerd.run reads its task here)")
    a = ap.parse_args()
    q = tree_root() / "_queue"
    (q / "requests").mkdir(parents=True, exist_ok=True)
    t = datetime.datetime.now(datetime.timezone.utc)
    name = f"{t.strftime('%Y%m%dT%H%M%SZ')}_{a.command}_{secrets.token_hex(3)}.md"
    fm = [f"command: {a.command}", f"args: [{', '.join(a.args)}]", f"requested_by: {a.by}",
          f"requested_at: {t.replace(microsecond=0).isoformat()}"] + ([f"job: {a.job}"] if a.job else [])
    tmp = q / "requests" / f".{name}.tmp"
    tmp.write_text("---\n" + "\n".join(fm) + "\n---\n" + (a.body.rstrip() + "\n" if a.body else ""), encoding="utf-8")
    os.replace(tmp, q / "requests" / name)  # atomic: the watcher never sees a half-written request
    print(f"queued {name}")
    if a.wait:
        res = q / "results" / name
        end = time.time() + a.wait
        while time.time() < end:
            if res.exists():
                print(res.read_text(encoding="utf-8"))
                return 0 if "status: ok" in res.read_text() else 1
            time.sleep(1)
        print(f"no result after {a.wait} s; check _queue/HEALTH.md for when the watcher last ran")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
