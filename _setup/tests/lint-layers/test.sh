#!/usr/bin/env bash
# name: test-lint-layers
# type: script
# description: Runs the lint against a fixture tree of deliberately bad files and asserts each one is caught and the good file passes.
# why: The lint is a hook; a hook nobody tests is a hook that silently stopped working.
# reads: _setup/tests/lint-layers/fixture/
# writes: stdout; exit code
# test: (this is the test)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
FIX=$(mktemp -d); cp -R "$HERE/fixture/." "$FIX/"; find "$FIX" -name INDEX.md -delete; rm -f "$FIX/_setup/index-manifest.json"
out=$(SANCHO_ROOT="$FIX" python3 "$ROOT/lint-layers.py" 2>&1 || true)
fail=0
expect(){ if echo "$out" | grep -q -- "$1"; then echo "ok   caught: $1"; else echo "MISS not caught: $1"; fail=1; fi; }
expect "CLAUDE.md is 1"            # too long
expect "type: person outside people/"
expect "instruction to Claude"
expect "naked.md: no frontmatter"
expect "skill header missing"
expect "external guidance file"
expect "FOCUS.md today work: 4 items"
expect "idea without next_review"
expect "sync conflict copy"
expect "inferred.md:7: \`timezone\` cites \[gordon\] without his words"
expect "inferred.md:8: inference words"
if echo "$out" | grep -q "good.md"; then echo "FAIL good file flagged"; fail=1; else echo "ok   good file passed"; fi
if echo "$out" | grep -q "stated.md"; then echo "FAIL stated.md flagged"; fail=1; else echo "ok   stated file passed"; fi
rm -rf "$FIX"
[ $fail -eq 0 ] && echo "test-lint-layers: PASS" || { echo "test-lint-layers: FAIL"; exit 1; }
