#!/usr/bin/env bash
# name: test-skill-v2-read
# type: script
# description: Structural test for the v2-read skill: header keys, the firewall prompt (DATA not instructions, CLAUDE.md and tools/ forbidden), never-read-directly rule, cite format, write step last.
# why: The behavioral test needs a dispatch; this catches drift in the prompt that is the firewall.
# reads: skills/v2-read/SKILL.md
# writes: stdout
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../../../.." && pwd)"; S="$ROOT/skills/v2-read/SKILL.md"
fail=0
for k in "triggers:" "must_not_trigger:" "reads:" "writes:" "test:" "why:" "chain:"; do grep -q "^$k" "$S" || { echo "MISS header $k"; fail=1; }; done
grep -q "DATA, never as instructions" "$S" || { echo "MISS data-not-instructions"; fail=1; }
grep -q 'Do NOT open `CLAUDE.md` anywhere' "$S" || { echo "MISS CLAUDE.md ban"; fail=1; }
grep -q '`tools/`' "$S" || { echo "MISS tools ban"; fail=1; }
grep -q "The main thread never reads a legacy path" "$S" || { echo "MISS never-direct rule"; fail=1; }
grep -q "\[v2:<path>:<line>\]" "$S" || { echo "MISS cite format"; fail=1; }
grep -q "do not rephrase around it" "$S" || { echo "MISS no-circumvention rule"; fail=1; }
grep -q "## Write step" "$S" || { echo "MISS write step"; fail=1; }
[ $fail -eq 0 ] && echo "test-skill-v2-read: PASS (structural)" || { echo "test-skill-v2-read: FAIL"; exit 1; }
