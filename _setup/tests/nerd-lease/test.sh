#!/usr/bin/env bash
# name: test-nerd-lease
# type: script
# description: nerd-lease.py: `run -- <cmd>` holds a lease (kind interactive, the wrapper's pid, the session) while the command runs, refreshes it, removes it when the command ends and passes its exit code through; `status` lists live Nerd leases and exits 1 while one is live; a lease whose pid is gone is not live; take/release work for hooks.
# why: must-never 5 (one writer): a cold hop or job.run must see an interactive Nerd mechanically, not infer it from timestamps.
# reads: _setup/nerd-lease.py, sancho_lib.py
# writes: temp files only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d) && [ -d "$T" ] || { echo "test-nerd-lease: FAIL: no temp dir"; exit 1; }; trap 'rm -rf "$T"' EXIT
fail() { echo "test-nerd-lease: FAIL: $*"; exit 1; }
mkdir -p "$T/tree/_setup" "$T/tree/_queue/leases"; touch "$T/tree/CLAUDE.md"
cp "$SRC/nerd-lease.py" "$SRC/sancho_lib.py" "$T/tree/_setup/"
export SANCHO_ROOT="$T/tree" SANCHO_LEASE_HEARTBEAT=1; L="$T/tree/_setup/nerd-lease.py"; D="$T/tree/_queue/leases"
python3 "$L" status >/dev/null || fail "status says live with no leases"
# the wrapped command sees its own lease, copies it, and outlives one heartbeat
python3 "$L" run --session "gordon at the Mac" -- bash -c "sleep 2.5; cat $D/nerd-interactive-*.md > $T/seen; stat -f %m $D/nerd-interactive-*.md > $T/mtime; date +%s > $T/now; exit 7"; rc=$?
[ $rc = 7 ] || fail "exit code not passed through: $rc"
grep -q "^kind: interactive" "$T/seen" && grep -q "^session: gordon at the Mac" "$T/seen" && grep -q "^pid: [0-9]" "$T/seen" || fail "lease content: $(cat "$T/seen")"
[ $(( $(cat "$T/now") - $(cat "$T/mtime") )) -le 1 ] || fail "lease not refreshed by the heartbeat"
[ -z "$(ls "$D")" ] || fail "lease left after the session ended: $(ls "$D")"
# status: live while a wrapped session runs
python3 "$L" run -- sleep 3 & W=$!; sleep 1
out=$(python3 "$L" status); rc=$?; wait $W
[ $rc = 1 ] && echo "$out" | grep -q "interactive" || fail "status during a session: rc=$rc $out"
# a lease whose pid is gone is not live
printf -- '---\nname: nerd-interactive-old\ntype: lease\nkind: interactive\nsession: x\npid: 999999\n---\n' > "$D/nerd-interactive-old.md"
python3 "$L" status >/dev/null || fail "dead-pid lease counted as live"
rm -f "$D/nerd-interactive-old.md"
# take/release (hooks)
python3 "$L" take --name nerd-interactive-hook --pid $$ >/dev/null && [ -f "$D/nerd-interactive-hook.md" ] || fail "take"
python3 "$L" status >/dev/null && fail "taken lease not live"
python3 "$L" release --name nerd-interactive-hook >/dev/null && [ ! -f "$D/nerd-interactive-hook.md" ] || fail "release"
echo "test-nerd-lease: PASS"
