#!/usr/bin/env bash
# name: test-skill-earballs-ingest
# type: script
# description: Structural test for the earballs-ingest skill: header keys, scenario present, the seven buckets named, long-chunk speaker rule, no machine-to-human promotion, supersede-never-overwrite, move-never-copy, triage rule, no tasks for Gordon, write step last.
# why: The behavioral test needs `claude -p` on the Mac; this runs anywhere and catches header and rule drift.
# reads: skills/earballs-ingest/SKILL.md, this folder's scenario.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/earballs-ingest/SKILL.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
[ -f "$HERE/scenario.md" ] || { echo "MISS scenario.md"; fail=1; }
for b in "Next action" "Project" "Waiting for" "Reference" "Someday/maybe" "Calendar" "Trash"; do grep -q "\*\*$b\*\*" "$S" || { echo "MISS bucket $b"; fail=1; }; done
grep -q "long passages" "$S" || { echo "MISS long-chunk rule"; fail=1; }
grep -q "Nothing is marked human-confirmed except on Gordon's explicit word" "$S" || { echo "MISS promotion rule"; fail=1; }
grep -q "Supersede, never overwrite; move, never copy or delete" "$S" || { echo "MISS supersede/move rule"; fail=1; }
grep -q "only when a fact hangs on them" "$S" || { echo "MISS triage rule"; fail=1; }
grep -q "No tasks created for Gordon" "$S" || { echo "MISS no-tasks rule"; fail=1; }
grep -q "A correction cascades" "$S" || { echo "MISS cascade rule"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
tail -3 "$S" | grep -q "Receipt" || { echo "FAIL write step not last"; fail=1; }
grep -qiE "minutes to|hours to|should take" "$S" && { echo "FAIL time-estimate phrasing present"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-earballs-ingest: PASS (structural; behavioral scenario runs on the Mac)" || { echo "test-skill-earballs-ingest: FAIL"; exit 1; }
