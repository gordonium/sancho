#!/usr/bin/env bash
# name: test-install-mac
# type: script
# description: Every com.sancho.*.plist renders to a valid plist with no __HOME__ left, every script it names exists, and each gets bootout+bootstrap. launchctl is stubbed.
# why: a plist pointing at a renamed script fails silently inside launchd.
# reads: _setup/install-mac.sh, _setup/com.sancho.*.plist
# writes: temp files only
# requires: mac
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
fail() { echo "test-install-mac: FAIL: $*"; exit 1; }
printf '#!/usr/bin/env bash\necho "$@" >> %s/calls\n' "$T" > "$T/lc"; chmod +x "$T/lc"
SANCHO_LAUNCH_AGENTS="$T/la" SANCHO_LAUNCHCTL="$T/lc" bash "$SRC/install-mac.sh" >/dev/null || fail "install failed"
n=$(ls "$SRC"/com.sancho.*.plist | wc -l | tr -d ' ')
[ "$(ls "$T/la" | wc -l | tr -d ' ')" = "$n" ] || fail "not every plist installed"
[ "$(grep -c bootstrap "$T/calls")" = "$n" ] || fail "not every plist bootstrapped"
grep -l __HOME__ "$T/la"/* && fail "__HOME__ left unrendered"
checked=0
for p in "$T/la"/*.plist; do
  i=0; while s=$(plutil -extract "ProgramArguments.$i" raw -o - "$p" 2>/dev/null); do
    i=$((i+1)); case "$s" in "$HOME/Sync/Sancho/"*) ;; *) continue;; esac
    rel="${s#$HOME/Sync/Sancho/}"; [ -e "$SRC/../$rel" ] || fail "$(basename "$p") points at missing $rel"; checked=$((checked+1))
  done
done
[ "$checked" -ge "$n" ] || fail "only $checked script paths checked for $n plists"
echo "test-install-mac: PASS"
