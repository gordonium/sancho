#!/usr/bin/env bash
# name: test-netstate
# type: script
# description: netstate.py: an unknown network is metered while the policy date runs and not after; a listed network follows its row; `mark` records the current network; a phone-hotspot-style router is hinted. The watcher defers a [heavy] request while metered and releases it when unmetered.
# why: a wrong answer here either burns Gordon's roaming data or blocks work on good Wi-Fi.
# reads: _setup/netstate.py, sancho-watcher.py
# writes: temp files only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
fail() { echo "test-netstate: FAIL: $*"; exit 1; }
mkdir -p "$T/tree/_setup" "$T/tree/_queue/requests" "$T/state"; touch "$T/tree/CLAUDE.md"
cp "$SRC/netstate.py" "$SRC/sancho_lib.py" "$SRC/sancho-watcher.py" "$SRC/sancho-enqueue.py" "$SRC/ping.sh" "$T/tree/_setup/"
printf 'import sys; sys.exit(0)\n' > "$T/tree/_setup/lint-layers.py"
pol(){ printf -- '---\nname: x\n---\nUnknown networks: metered until %s\n\n| router | label | treat as | added |\n|---|---|---|---|\n| aa:bb:cc:dd:ee:01 | hotel | unmetered | 2026-09-30 |\n' "$1" > "$T/tree/_setup/metered-networks.md"; }
export SANCHO_ROOT="$T/tree" SANCHO_STATE="$T/state" SANCHO_SECRETS_PLAIN="$T/none" SANCHO_SECRETS_AGE="$T/none.age"
N="$T/tree/_setup/netstate.py"
pol 2999-01-01
SANCHO_NET_FINGERPRINT=66:de:f3:0c:e8:4e python3 "$N" | grep -q "METERED" || fail "unknown network not metered during policy"
grep -q "phone hotspot" "$T/state/network.json" || fail "hotspot hint missing"
SANCHO_NET_FINGERPRINT=aa:bb:cc:dd:ee:01 python3 "$N" | grep -q "hotel.*unmetered" || fail "listed unmetered network misread"
pol 2000-01-01
SANCHO_NET_FINGERPRINT=66:de:f3:0c:e8:4e python3 "$N" | grep -q "unmetered" || fail "unknown network metered after policy date"
pol 2999-01-01
SANCHO_NET_FINGERPRINT=12:34:56:78:9a:bc python3 "$N" mark "my phone" metered >/dev/null
grep -q "| 12:34:56:78:9a:bc | my phone | metered |" "$T/tree/_setup/metered-networks.md" || fail "mark did not record the network"
# watcher: heavy deferred while metered, released when unmetered
cat > "$T/tree/_setup/commands.md" <<'MD'
| command | script | timeout (s) | schedule | description |
|---|---|---|---|---|
| big | _setup/ping.sh | 10 | [heavy] | bulk |
| ping | _setup/ping.sh | 10 | | round trip |
MD
export SANCHO_NET_FINGERPRINT=66:de:f3:0c:e8:4e
python3 "$T/tree/_setup/sancho-enqueue.py" big >/dev/null; python3 "$T/tree/_setup/sancho-enqueue.py" ping >/dev/null
python3 "$T/tree/_setup/sancho-watcher.py" >/dev/null 2>&1 || fail "watcher tick failed"
[ "$(ls "$T/tree/_queue/deferred" | wc -l | tr -d ' ')" = "1" ] || fail "heavy request not deferred"
grep -q "status: deferred" "$T"/tree/_queue/results/*_big_*.md || fail "no deferred result"
grep -q "status: ok" "$T"/tree/_queue/results/*_ping_*.md || fail "light command blocked while metered"
grep -q "METERED: heavy commands deferred (1 waiting)" "$T/tree/_queue/HEALTH.md" || fail "HEALTH.md lacks the metered line"
export SANCHO_NET_FINGERPRINT=aa:bb:cc:dd:ee:01
python3 "$T/tree/_setup/sancho-watcher.py" >/dev/null 2>&1
grep -q "status: ok" "$T"/tree/_queue/results/*_big_*.md || fail "deferred request not run on unmetered network"
# the real fingerprint must work under launchd's PATH (route/arp live in /sbin, /usr/sbin; found 2026-09-30)
if [ "$(uname)" = "Darwin" ] && /sbin/route -n get default >/dev/null 2>&1; then
  o=$(env -u SANCHO_NET_FINGERPRINT PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin python3 "$N")
  echo "$o" | grep -q "offline" && fail "fingerprint reads offline under launchd's PATH: $o"
fi
echo "test-netstate: PASS"
