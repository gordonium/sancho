#!/usr/bin/env bash
# name: test-skill-personal-morning
# type: script
# description: Structural test for the personal-morning skill: header keys, never-infer-city rule, computed verdict rule, ten-line cap, thresholds file referenced, nomad.brief command referenced, write step last; thresholds.md exists with the 60/85 lines.
# why: The behavioral test needs the Mac command and a fixture brief; this catches rule drift anywhere.
# reads: skills/personal-morning/SKILL.md, personal/nomad/thresholds.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/personal-morning/SKILL.md"; T="$ROOT/personal/nomad/thresholds.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
grep -q "The city is never inferred" "$S" || { echo "MISS never-infer rule"; fail=1; }
grep -q "computed from sample-point forecasts" "$S" || { echo "MISS computed verdict"; fail=1; }
grep -q "Ten lines" "$S" || { echo "MISS ten-line cap"; fail=1; }
grep -q "nomad.brief" "$S" || { echo "MISS command"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
tail -3 "$S" | grep -q "Receipt" || { echo "FAIL write step not last"; fail=1; }
grep -qiE "minutes to|hours to|should take" "$S" && { echo "FAIL time-estimate phrasing"; fail=1; }
[ -f "$T" ] && grep -q "60" "$T" && grep -q "85" "$T" || { echo "MISS thresholds.md with 60/85"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-personal-morning: PASS (structural)" || { echo "test-skill-personal-morning: FAIL"; exit 1; }
