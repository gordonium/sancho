#!/usr/bin/env python3
"""
name: test-all
type: command
description: Run every test under _setup/tests/*/ (test.sh or test.py), write _setup/TESTS.md (the test board), exit 1 if any fails. Off the Mac, suites whose header says `requires: mac` are skipped and the board is not written (ERRORS.md #2). PATH is set explicitly, so launchd's short PATH can't fail a suite (ERRORS.md #8); a suite during which the Mac slept says so on its row. `--fail-tail N` prints the last N lines of each failing suite (job.run's evidence).
why: Tests are automatic; Gordon never runs them. This is the one entry point the watcher schedules nightly and after changes.
reads: _setup/tests/*/
writes: _setup/TESTS.md
schedule: nightly 02:30; after any commit touching _setup/ or skills/
test: _setup/tests/test-all/ (runs itself against a fixture with one passing and one failing test)
"""
import os, re, sys, time, argparse, subprocess, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent
ON_MAC = os.environ.get("SANCHO_PLATFORM", sys.platform) == "darwin"
IN_NERD = os.environ.get("SANCHO_IN_NERD")  # a sandboxed nerd.run session: its board is not the real one (localhost blocked)
# launchd starts us with /usr/bin:/bin; suites call route, arp, pmset, brew tools (ERRORS.md #8)
PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
os.environ["PATH"] = PATH + ":" + os.environ.get("PATH", "")
ap = argparse.ArgumentParser()
ap.add_argument("--fail-tail", type=int, default=0, help="print the last N output lines of each failing suite")
a = ap.parse_args()
rows, failed, skipped, tails = [], 0, 0, []
# dot-folders are tool state, not suites (Claude Code leaves .claude/.cc-writes beside files it edits)
suites = [d for d in sorted((ROOT / "tests").iterdir()) if d.is_dir() and d.name != "skills" and not d.name.startswith(".")]
suites += [d for d in sorted((ROOT / "tests" / "skills").glob("*")) if d.is_dir() and not d.name.startswith(".")] if (ROOT / "tests" / "skills").exists() else []
for d in suites:
    name = ('skill:' if d.parent.name == 'skills' else '') + d.name
    t = d / "test.sh" if (d / "test.sh").exists() else d / "test.py" if (d / "test.py").exists() else None
    if not t:
        rows.append(f"| {name} | no test file | - |"); failed += 1; continue
    if not ON_MAC and re.search(r"(?m)^#?\s*requires:\s*mac\b", t.read_text(errors="replace")[:2000]):
        rows.append(f"| {d.name} | SKIP (needs the Mac) | - |"); skipped += 1; continue
    cmd = ["bash", str(t)] if t.suffix == ".sh" else ["python3", str(t)]
    wall, mono = time.time(), time.monotonic()  # macOS: monotonic stops while asleep, wall time doesn't
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    slept = (time.time() - wall) - (time.monotonic() - mono)
    ok = r.returncode == 0
    failed += 0 if ok else 1
    last = (r.stdout.strip().splitlines() or [""])[-1][:120]
    if slept > 30:
        last += f" (the Mac slept {int(slept // 60)} min during this suite)"
    rows.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {last} |")
    if not ok and a.fail_tail:
        tails.append(f"### {name}\n" + "\n".join((r.stdout + r.stderr).rstrip().splitlines()[-a.fail_tail:]))
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
if tails:  # before the table, so the summary stays the last line (the watcher's result summary)
    print("\n\n".join(tails) + "\n")
if not ON_MAC or IN_NERD:
    where = "inside a nerd.run sandbox" if IN_NERD else "not the Mac"
    print("\n".join(rows)); print(f"test-all: {len(rows)} suites, {failed} failing, {skipped} skipped; {where}, board not written")
    sys.exit(1 if failed else 0)
(ROOT / "TESTS.md").write_text(f"# TESTS\ngenerated {stamp} by test-all.py · {len(rows)} suites · {failed} failing\n\n| suite | result | last line |\n|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
print("\n".join(rows)); print(f"test-all: {len(rows)} suites, {failed} failing")
sys.exit(1 if failed else 0)
