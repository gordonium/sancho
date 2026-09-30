#!/usr/bin/env bash
# name: test-stay-awake
# type: script
# description: on writes a caffeinate plist, bootstraps it and records state; off boots it out, removes the plist and records off. launchctl is stubbed.
# why: a stay-awake that silently stays on drains the battery; one that silently fails loses the night's run.
# reads: _setup/stay-awake.sh
# writes: temp files only
# requires: mac
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d) && [ -d "$T" ] || { echo "test-stay-awake: FAIL: no temp dir"; exit 1; }; trap 'rm -rf "$T"' EXIT
fail() { echo "test-stay-awake: FAIL: $*"; exit 1; }
printf '#!/usr/bin/env bash\necho "$@" >> %s/calls\n' "$T" > "$T/lc"; chmod +x "$T/lc"
export SANCHO_LAUNCH_AGENTS="$T/la" SANCHO_STATE="$T/st" SANCHO_LAUNCHCTL="$T/lc"
bash "$SRC/stay-awake.sh" on >/dev/null || fail "on"
plutil -lint -s "$T/la/com.sancho.caffeinate.plist" >/dev/null || fail "bad plist"
grep -q "bootstrap" "$T/calls" || fail "not bootstrapped"
grep -q "^on since" "$T/st/stay-awake" || fail "state not on"
bash "$SRC/stay-awake.sh" off >/dev/null || fail "off"
[ -f "$T/la/com.sancho.caffeinate.plist" ] && fail "plist left behind"
[ "$(cat "$T/st/stay-awake")" = "off" ] || fail "state not off"
bash "$SRC/stay-awake.sh" bogus >/dev/null 2>&1 && fail "bad arg accepted"
echo "test-stay-awake: PASS"
