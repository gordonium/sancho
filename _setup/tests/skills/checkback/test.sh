#!/usr/bin/env bash
# name: test-skill-checkback
# type: script
# description: Structural test for the checkback skill: header keys, scenario present, evidence-is-a-file-test rule, no recurring tasks, cap read from the job, info-per-hop/warn-at-end, idempotent edits, write step; plus the job template carries hops/hop_cap/waiting_on.
# why: The behavioral test needs `claude -p` on the Mac; this runs anywhere and catches header, contract and rule drift.
# reads: skills/checkback/SKILL.md, _setup/templates/job.md, this folder's scenario.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/checkback/SKILL.md"; J="$ROOT/_setup/templates/job.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
[ -f "$HERE/scenario.md" ] || { echo "MISS scenario.md"; fail=1; }
grep -q "Evidence is a file test" "$S" || { echo "MISS evidence rule"; fail=1; }
grep -q "Never create a scheduled task that repeats" "$S" || { echo "MISS one-time rule"; fail=1; }
grep -q "hop_cap" "$S" || { echo "MISS hop cap"; fail=1; }
grep -q "Info per hop, warn at the end" "$S" || { echo "MISS push levels"; fail=1; }
grep -q "never rewrite the file" "$S" || { echo "MISS idempotent edit rule"; fail=1; }
grep -q "Never ask Gordon anything from a cold run" "$S" || { echo "MISS cold-run question rule"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
grep -qiE "minutes to|hours to|should take" "$S" && { echo "FAIL time-estimate phrasing present"; fail=1; }
for k in "hops:" "hop_cap:" "waiting_on:"; do grep -q "^$k" "$J" || { echo "MISS job template $k"; fail=1; }; done
[ $fail -eq 0 ] && echo "test-skill-checkback: PASS (structural; behavioral scenario runs on the Mac)" || { echo "test-skill-checkback: FAIL"; exit 1; }
