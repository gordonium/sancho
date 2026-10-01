#!/usr/bin/env bash
# name: test-skill-food-routine
# type: script
# description: Structural test for the food-routine skill: header keys, the three jobs, the midday rules (no cooking at the moment, fresh, rotation), never-order rule, fifteen-minute ceiling, warm-not-clinical rule, write step last; pantry and journal seed files exist.
# why: The behavioral test needs a conversation; this catches rule drift and the voice rule anywhere.
# reads: skills/food-routine/SKILL.md, personal/food/pantry.md, personal/food/journal.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/food-routine/SKILL.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
for j in "## Job 1" "## Job 2" "## Job 3"; do grep -q "$j" "$S" || { echo "MISS $j"; fail=1; }; done
grep -q "no cooking at the moment of eating" "$S" || { echo "MISS midday rule"; fail=1; }
grep -q "rotation is the design" "$S" || { echo "MISS rotation rule"; fail=1; }
grep -q "Sancho buys nothing, orders nothing, creates no tasks" "$S" || { echo "MISS never-order rule"; fail=1; }
grep -q "Fifteen minutes is the ceiling" "$S" || { echo "MISS ceiling"; fail=1; }
grep -q "Never make him feel managed" "$S" || { echo "MISS voice rule"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
tail -3 "$S" | grep -q "Receipt" || { echo "FAIL write step not last"; fail=1; }
[ -f "$ROOT/personal/food/pantry.md" ] || { echo "MISS pantry.md"; fail=1; }
[ -f "$ROOT/personal/food/journal.md" ] || { echo "MISS journal.md"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-food-routine: PASS (structural)" || { echo "test-skill-food-routine: FAIL"; exit 1; }
