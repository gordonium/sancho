#!/usr/bin/env bash
# name: test-skill-attribution-correction
# type: script
# description: Structural test for the attribution-correction skill: header keys, rules that must not drift, write step last.
# why: The behavioral test needs a dispatch on the Mac; this catches header and rule drift anywhere.
# reads: skills/attribution-correction/SKILL.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/attribution-correction/SKILL.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
tail -3 "$S" | grep -q "Receipt" || { echo "FAIL write step not last"; fail=1; }
grep -qiE "minutes to|hours to|should take" "$S" && { echo "FAIL time-estimate phrasing"; fail=1; }
grep -q "Present all, then fix all" "$S" || { echo "MISS present-before-fix"; fail=1; }
grep -q "pipeline.library" "$S" || { echo "MISS library rebuild"; fail=1; }
grep -q "pipeline.rematch" "$S" || { echo "MISS rematch"; fail=1; }
grep -q "90 days" "$S" || { echo "MISS 90-day pause"; fail=1; }
grep -q "never edits a line in place" "$S" || { echo "MISS strike-and-add"; fail=1; }
grep -q "not done while this list is unreviewed" "$S" || { echo "MISS gate"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-attribution-correction: PASS (structural)" || { echo "test-skill-attribution-correction: FAIL"; exit 1; }
