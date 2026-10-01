#!/usr/bin/env bash
# name: test-skill-weekly-review
# type: script
# description: Structural test for the weekly-review skill: header keys, the cadence table (Mon/Thu work, Fri/Tue personal), the 7-day and 14-day thresholds, generated-lists rule, never-parks rule, no-tasks rule, both gears, write step last.
# why: The behavioral test needs a fixture tree and a conversation; this catches drift in cadence and rules anywhere.
# reads: skills/weekly-review/SKILL.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/weekly-review/SKILL.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
grep -q "| work | Monday" "$S" && grep -q "Thursday" "$S" && grep -q "| personal | Friday" "$S" && grep -q "Tuesday" "$S" || { echo "MISS cadence"; fail=1; }
grep -q "7 days" "$S" && grep -q "14 days" "$S" || { echo "MISS thresholds"; fail=1; }
grep -q "Generated lists drive it" "$S" || { echo "MISS generated rule"; fail=1; }
grep -q "never parks or closes a project unasked" "$S" || { echo "MISS never-parks rule"; fail=1; }
grep -q "No tasks created" "$S" || { echo "MISS no-tasks rule"; fail=1; }
grep -q "## Full review" "$S" && grep -q "## Mini review" "$S" || { echo "MISS gears"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
tail -3 "$S" | grep -q "Receipt" || { echo "FAIL write step not last"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-weekly-review: PASS (structural)" || { echo "test-skill-weekly-review: FAIL"; exit 1; }
