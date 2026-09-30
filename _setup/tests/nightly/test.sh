#!/usr/bin/env bash
# name: test-nightly
# type: script
# description: nightly.sh runs index, lint and map in order and stops at the first failure (a failing lint must not produce a map).
# why: the gate is the point of the script.
# reads: _setup/nightly.sh
# writes: temp files only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
fail() { echo "test-nightly: FAIL: $*"; exit 1; }
mkdir -p "$T/_setup"; cp "$SRC/nightly.sh" "$T/_setup/"
printf 'open("%s/order","a").write("index\\n")\n' "$T" > "$T/_setup/build-index.py"
printf 'import sys; open("%s/order","a").write("lint\\n"); sys.exit(int(open("%s/lintrc").read()))\n' "$T" "$T" > "$T/_setup/lint-layers.py"
printf 'open("%s/order","a").write("map\\n")\n' "$T" > "$T/_setup/build-map.py"
echo 0 > "$T/lintrc"; SANCHO_ROOT="$T" bash "$T/_setup/nightly.sh" >/dev/null || fail "green run failed"
[ "$(tr '\n' ' ' < "$T/order")" = "index lint map " ] || fail "order: $(cat "$T/order")"
rm "$T/order"; echo 1 > "$T/lintrc"; SANCHO_ROOT="$T" bash "$T/_setup/nightly.sh" >/dev/null 2>&1 && fail "lint failure not propagated"
grep -q map "$T/order" && fail "map built after a failing lint"
echo "test-nightly: PASS"
