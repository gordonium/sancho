#!/usr/bin/env bash
# name: test-build-index
# type: script
# description: Builds indexes for the lint fixture tree and checks the expected lines and the manifest exist.
# why: Indexes are the cascade; a generator that silently drops entries breaks navigation.
# reads: _setup/tests/lint-layers/fixture/
# writes: generated files inside the fixture (cleaned up)
# test: (this is the test)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"; FIX=$(mktemp -d); cp -R "$HERE/../lint-layers/fixture/." "$FIX/"
(SANCHO_ROOT="$FIX" python3 "$ROOT/build-index.py" >/dev/null) || { echo "test-build-index: FAIL (crash)"; exit 1; }
fail=0
grep -q "good.md · doc" "$FIX/work/acme/INDEX.md" || { echo "MISS good.md line"; fail=1; }
grep -q "NO DESCRIPTION" "$FIX/work/acme/INDEX.md" || { echo "MISS naked.md flagged NO DESCRIPTION"; fail=1; }
[ -f "$FIX/_setup/index-manifest.json" ] || { echo "MISS manifest"; fail=1; }
rm -rf "$FIX"
[ $fail -eq 0 ] && echo "test-build-index: PASS" || { echo "test-build-index: FAIL"; exit 1; }
