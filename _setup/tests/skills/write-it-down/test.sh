#!/usr/bin/env bash
# name: test-skill-write-it-down
# type: script
# description: Structural test for the write-it-down skill: header keys, rules that must not drift, write step last.
# why: The behavioral test needs a dispatch on the Mac; this catches header and rule drift anywhere.
# reads: skills/write-it-down/SKILL.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/write-it-down/SKILL.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
tail -3 "$S" | grep -q "Receipt" || { echo "FAIL write step not last"; fail=1; }
grep -qiE "minutes to|hours to|should take" "$S" && { echo "FAIL time-estimate phrasing"; fail=1; }
grep -q "Write before replying, not after" "$S" || { echo "MISS write-first"; fail=1; }
grep -q "a line without a cite is not written" "$S" || { echo "MISS cite rule"; fail=1; }
grep -q "the reflex missed" "$S" || { echo "MISS override-as-error"; fail=1; }
grep -q "ERRORS.md" "$S" || { echo "MISS errors log"; fail=1; }
grep -q "Never a whole-file rewrite" "$S" || { echo "MISS no-rewrite rule"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-write-it-down: PASS (structural)" || { echo "test-skill-write-it-down: FAIL"; exit 1; }
