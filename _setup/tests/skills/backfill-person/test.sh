#!/usr/bin/env bash
# name: test-skill-backfill-person
# type: script
# description: Structural test for the backfill-person skill: header keys, quarantine-only legacy access, cite-every-line, no-merge rule, sensitive-to-open-threads rule, write step last; and the backfill-people job task template exists.
# why: The behavioral test needs a dispatch; this catches drift in the rules that keep legacy text and guesses out of people files.
# reads: skills/backfill-person/SKILL.md, _setup/templates/nerd-task-backfill-person.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/backfill-person/SKILL.md"; T="$ROOT/_setup/templates/nerd-task-backfill-person.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
grep -q "through the quarantine only" "$S" || { echo "MISS quarantine rule"; fail=1; }
grep -q "Every line cites; a line without a cite is not written" "$S" || { echo "MISS cite rule"; fail=1; }
grep -q "No merge of two slugs without Gordon" "$S" || { echo "MISS no-merge rule"; fail=1; }
grep -q "No set-aside by topic" "$S" || { echo "MISS no-set-aside rule"; fail=1; }
grep -qiE "sensitive attribute|anything sensitive|until Gordon confirms it; the private tree" "$S" && { echo "FAIL a topic set-aside crept back in (decision 2026-09-29, ERRORS.md #10)"; fail=1; }
grep -q "Supersede, never overwrite; existing lines stay" "$S" || { echo "MISS supersede rule"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
tail -3 "$S" | grep -q "Receipt" || { echo "FAIL write step not last"; fail=1; }
[ -f "$T" ] || { echo "MISS nerd task template $T"; fail=1; }
grep -q "end of task" "$T" || { echo "MISS end marker in template"; fail=1; }
grep -qiE "minutes to|hours to|should take" "$S" && { echo "FAIL time-estimate phrasing"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-backfill-person: PASS (structural)" || { echo "test-skill-backfill-person: FAIL"; exit 1; }
