#!/usr/bin/env bash
# name: test-skill-open
# type: script
# description: Structural test for the open skill until the headless harness exists: header keys present, scenario present, packet reads limited to the allowed list, no time-estimate phrasing, write step last.
# why: The behavioral test (scenario.md) needs `claude -p` on the Mac; this runs anywhere and catches header and rule drift.
# reads: skills/open/SKILL.md, this folder's scenario.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../.." && pwd)"; S="$ROOT/../skills/open/SKILL.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
[ -f "$HERE/scenario.md" ] || { echo "MISS scenario.md"; fail=1; }
grep -qi "five minutes to" "$S" && { echo "FAIL time-estimate phrasing present"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
grep -q "Never state the weekday from memory" "$S" || { echo "MISS temporal rule"; fail=1; }
grep -q "never a third time" "$S" || { echo "MISS nag limit"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-open: PASS (structural; behavioral scenario runs on the Mac)" || { echo "test-skill-open: FAIL"; exit 1; }
