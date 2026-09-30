#!/usr/bin/env bash
# name: test-watcher
# type: script
# description: Against a temp tree and queue: ping round-trips with its request id; an unlisted command is refused; a terminal-only command is refused; a slow command times out; a failing one is marked failed; HEALTH.md is written and carries the lint's problems; the lock stops a second tick; the sleep window ignores Wake Requests and DarkWake; ticks per hour are shown.
# why: the bridge is how every Mac-side run happens; if it silently breaks, nothing runs and nobody knows.
# reads: _setup/sancho-watcher.py, sancho-enqueue.py, sancho_lib.py, ping.sh
# writes: temp files only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d) && [ -d "$T" ] || { echo "test-watcher: FAIL: no temp dir"; exit 1; }; trap 'rm -rf "$T"' EXIT
fail() { echo "test-watcher: FAIL: $*"; exit 1; }
mkdir -p "$T/tree/_setup" "$T/tree/_queue/requests" "$T/tree/_queue/leases" "$T/state"
touch "$T/tree/CLAUDE.md"
cp "$SRC/sancho-watcher.py" "$SRC/sancho-enqueue.py" "$SRC/sancho_lib.py" "$SRC/ping.sh" "$T/tree/_setup/"
printf 'import sys\nprint("PROBLEM: fixture/bad.md: no frontmatter"); sys.exit(1)\n' > "$T/tree/_setup/lint-layers.py"
printf '#!/usr/bin/env bash\nsleep 5\n' > "$T/tree/_setup/slow.sh"
printf '#!/usr/bin/env bash\necho boom; exit 3\n' > "$T/tree/_setup/bad.sh"
cat > "$T/tree/_setup/commands.md" <<'MD'
| command | script | timeout (s) | schedule | description |
|---|---|---|---|---|
| ping | _setup/ping.sh | 10 | | round trip |
| slow | _setup/slow.sh | 1 | | times out |
| bad | _setup/bad.sh | 10 | | fails |
| secret.thing | _setup/ping.sh | 10 | Terminal only | asks for a passphrase |
MD
export SANCHO_ROOT="$T/tree" SANCHO_STATE="$T/state" SANCHO_SECRETS_PLAIN="$T/none" SANCHO_SECRETS_AGE="$T/none.age"
W="$T/tree/_setup/sancho-watcher.py"; E="$T/tree/_setup/sancho-enqueue.py"
for c in ping nope slow bad secret.thing; do python3 "$E" "$c" --by test >/dev/null || fail "enqueue $c"; done
python3 "$W" >/dev/null 2>&1 || fail "watcher tick exited non-zero"
R="$T/tree/_queue/results"
res() { grep -l "^command: $1\$" "$R"/*.md 2>/dev/null | head -1; }
p=$(res ping); [ -n "$p" ] || fail "no ping result"
grep -q "status: ok" "$p" || fail "ping not ok"
id=$(basename "$p" .md); grep -q "pong $id" "$p" || fail "ping result lacks its request id"
grep -q "status: refused" "$(res nope)" || fail "unlisted command not refused"
grep -q "status: refused" "$(res secret.thing)" || fail "terminal-only command not refused"
grep -q "status: timeout" "$(res slow)" || fail "slow command did not time out"
grep -q "status: failed" "$(res bad)" && grep -q "exit_code: 3" "$(res bad)" || fail "failing command not marked failed/exit 3"
for k in command status started_at finished_at exit_code log; do grep -q "^$k:" "$p" || fail "result missing $k"; done
[ -z "$(ls "$T/tree/_queue/requests")" ] || fail "requests not consumed"
[ -z "$(ls "$T/tree/_queue/running" 2>/dev/null)" ] || fail "claimed requests left in running/"
H="$T/tree/_queue/HEALTH.md"; [ -f "$H" ] || fail "no HEALTH.md"
grep -q "watcher last seen" "$H" && grep -q "runs today: 5 (4 failed)" "$H" || fail "HEALTH.md content: $(sed -n 4,8p "$H")"
grep -q "lint: 1 problem" "$H" && grep -q "fixture/bad.md: no frontmatter" "$H" || fail "lint problems not surfaced in HEALTH.md"
# enqueue --wait round trip with a concurrent tick
( sleep 1; python3 "$W" >/dev/null 2>&1 ) & out=$(python3 "$E" ping --wait 15) || fail "enqueue --wait: $out"; wait
# the lock: a held lock makes a tick exit without running
python3 -c "import fcntl,time,sys; f=open('$T/state/watcher.lock','w'); fcntl.flock(f, fcntl.LOCK_EX); time.sleep(3)" &
sleep 0.5; python3 "$E" ping >/dev/null; o=$(python3 "$W"); wait
echo "$o" | grep -q "another watcher tick" || fail "lock not honoured: $o"
# sleep window from a real pmset capture with maintenance wakes and "Wake Requests" lines (ERRORS.md #3)
sw=$(python3 -c "
import importlib.util as u
s=u.spec_from_file_location('w','$SRC/sancho-watcher.py'); w=u.module_from_spec(s); s.loader.exec_module(w)
r=w.parse_sleep(open('$HERE/pmset-darkwake.txt').read()); print(r.get('sleep'), r.get('wake'), r.get('dark_wakes'))")
[ "$sw" = "2026-09-30 19:35:36 2026-09-30 21:29:35 6" ] || fail "sleep window from pmset capture: $sw"
grep -q "watcher ticks per hour" "$H" || fail "HEALTH.md lacks the ticks-per-hour line"
echo "test-watcher: PASS"
