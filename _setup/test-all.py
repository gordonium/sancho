#!/usr/bin/env python3
"""
name: test-all
type: command
description: Run every test under _setup/tests/*/ (test.sh or test.py), write _setup/TESTS.md (the test board), exit 1 if any fails.
why: Tests are automatic; Gordon never runs them. This is the one entry point the watcher schedules nightly and after changes.
reads: _setup/tests/*/
writes: _setup/TESTS.md
schedule: nightly 02:30; after any commit touching _setup/ or skills/
test: _setup/tests/test-all/ (runs itself against a fixture with one passing and one failing test)
"""
import subprocess, sys, datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parent
rows, failed = [], 0
suites = [d for d in sorted((ROOT / "tests").iterdir()) if d.is_dir() and d.name != "skills"]
suites += [d for d in sorted((ROOT / "tests" / "skills").glob("*")) if d.is_dir()] if (ROOT / "tests" / "skills").exists() else []
for d in suites:
    t = d / "test.sh" if (d / "test.sh").exists() else d / "test.py" if (d / "test.py").exists() else None
    if not t:
        rows.append(f"| {('skill:' if d.parent.name == 'skills' else '') + d.name} | no test file | - |"); failed += 1; continue
    cmd = ["bash", str(t)] if t.suffix == ".sh" else ["python3", str(t)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    ok = r.returncode == 0
    failed += 0 if ok else 1
    last = (r.stdout.strip().splitlines() or [""])[-1][:120]
    rows.append(f"| {('skill:' if d.parent.name == 'skills' else '') + d.name} | {'PASS' if ok else 'FAIL'} | {last} |")
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
(ROOT / "TESTS.md").write_text(f"# TESTS\ngenerated {stamp} by test-all.py · {len(rows)} suites · {failed} failing\n\n| suite | result | last line |\n|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")
print("\n".join(rows)); print(f"test-all: {len(rows)} suites, {failed} failing")
sys.exit(1 if failed else 0)
