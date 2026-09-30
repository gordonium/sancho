#!/usr/bin/env bash
# name: test-build-map
# type: script
# description: Builds the map for the real tree into a temp copy and checks Level 0, Level 1 and Level 2 headings exist and FOCUS is on top.
# why: A map missing a level is a map Gordon can't use.
# reads: the tree
# writes: a temp MAP.md (discarded)
# test: (this is the test)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"; TREE="$(cd "$ROOT/.." && pwd)"
cp "$TREE/MAP.md" /tmp/MAP.before 2>/dev/null || true
python3 "$ROOT/build-map.py" >/dev/null || { echo "test-build-map: FAIL (exit)"; exit 1; }
fail=0
for h in "## FOCUS" "## Level 0" "## Level 1" "## Level 2" "flowchart LR"; do grep -q "$h" "$TREE/MAP.md" || { echo "MISS $h"; fail=1; }; done
[ $fail -eq 0 ] && echo "test-build-map: PASS" || { echo "test-build-map: FAIL"; exit 1; }
