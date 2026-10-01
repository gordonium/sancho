#!/usr/bin/env bash
# name: test-watcher
# type: script
# description: Against a temp tree and queue: ping round-trips with its request id; an unlisted command is refused; a terminal-only command is refused; a slow command times out; a failing one is marked failed; HEALTH.md is written and carries the lint's problems; the lock stops a second tick; the sleep window ignores Wake Requests and DarkWake; ticks per hour are shown; a request's session is echoed in its result and log, a missing one is flagged; a failure of a request naming a job warns with a registered reason; a nerd.run result for an `advance: auto` job queues job.run --auto (a manual job doesn't); a job pending on a Nerd lease is released only when no live lease remains; leases show kind and go stale when their pid is gone; a launchd request waits until the Mac has been awake 10 min; `enqueue --wait` reports a stale HEALTH.md at once.
# why: the bridge is how every Mac-side run happens; if it silently breaks, nothing runs and nobody knows.
# reads: _setup/sancho-watcher.py, sancho-enqueue.py, sancho_lib.py, ping.sh, notify.py, notify-reasons.md
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
# session: echoed in the result; a request without one says so (STATUS.md 2026-10-01)
cp "$SRC/notify.py" "$SRC/notify-reasons.md" "$T/tree/_setup/"
export PUSHOVER_USER=u PUSHOVER_TOKEN=t SANCHO_PUSHOVER_URL="file://$T/pushes"
unset SANCHO_SESSION SANCHO_REQUESTED_BY
python3 "$W" >/dev/null 2>&1; rm -f "$R"/*.md  # run the lock test's leftover ping first
python3 "$E" ping --by cowork --session "cowork hop 3" >/dev/null; python3 "$W" >/dev/null 2>&1
grep -q "^session: cowork hop 3$" "$(res ping)" || fail "session not echoed in the result: $(cat "$(res ping)")"
grep -q "session cowork hop 3" "$T/tree/_queue/log/"*.log || fail "session not in the log"
rm -f "$R"/*.md; printf -- '---\ncommand: ping\nrequested_by: cowork\n---\n' > "$T/tree/_queue/requests/20261001T000000Z_ping_aaaaaa.md"; python3 "$W" >/dev/null 2>&1
grep -q "^session: (none given; requested_by cowork)" "$(res ping)" || fail "missing session not flagged"
# a failure of a request that names a job warns (reason command-blocks-job), with the session echoed
python3 "$E" bad --by cowork --session "cowork hop 4" --job fix >/dev/null; python3 "$W" >/dev/null 2>&1
python3 -c "
import urllib.parse as u, sys
p = [u.parse_qs(l.strip()) for l in open('$T/pushes')][-1]
ok = p['priority'] == ['0'] and 'blocks job fix' in p['message'][0] and 'from cowork hop 4' in p['message'][0] and 'unregistered' not in p['message'][0]
sys.exit(0 if ok else 1)" || fail "job-blocking failure did not warn: $(tail -1 "$T/pushes")"
# a nerd.run result for an advance:auto job queues job.run --auto; a manual job does not
mkdir -p "$T/tree/_queue/jobs"; printf -- '---\njob: auto\nadvance: auto\n---\n' > "$T/tree/_queue/jobs/2026-10-01_auto.md"; printf -- '---\njob: man\n---\n' > "$T/tree/_queue/jobs/2026-10-01_man.md"
printf '| nerd.run | _setup/ping.sh | 10 | | fake Nerd |\n' >> "$T/tree/_setup/commands.md"
python3 "$E" nerd.run --by cowork --session "cowork hop 5" --job auto >/dev/null; python3 "$E" nerd.run --by cowork --job man >/dev/null
python3 "$W" >/dev/null 2>&1
q=$(grep -l "^command: job.run" "$T/tree/_queue/requests/"*.md 2>/dev/null)
[ "$(echo "$q" | grep -c .)" = "1" ] || fail "want one job.run queued, got: $q"
grep -q "args: \[2026-10-01_auto, --auto\]" "$q" && grep -q "^session: watcher after .*_nerd.run_" "$q" && grep -q "^job: 2026-10-01_auto" "$q" || fail "job.run request wrong: $(cat "$q")"
rm -f "$T/tree/_queue/requests/"*.md
# a job left waiting for a Nerd lease is re-queued only when no live Nerd lease remains
echo '{"2026-10-01_auto": {"since": 1, "why": "interactive Nerd"}}' > "$T/state/advance-pending.json"
printf -- '---\nname: nerd-interactive-x\ntype: lease\nkind: interactive\nsession: interactive\npid: %s\n---\n' $$ > "$T/tree/_queue/leases/nerd-interactive-x.md"
printf -- '---\nname: nerd-interactive-dead\ntype: lease\nkind: interactive\nsession: interactive\npid: 999999\n---\n' > "$T/tree/_queue/leases/nerd-interactive-dead.md"
python3 "$W" >/dev/null 2>&1
ls "$T/tree/_queue/requests/" | grep -q job.run && fail "pending job released while a Nerd lease is live"
grep -q "leases live: nerd-interactive-x (interactive, interactive" "$H" || fail "live lease not shown with its kind: $(grep leases "$H")"
grep -q "leases stale.*nerd-interactive-dead.*pid gone" "$H" || fail "dead-pid lease not stale: $(grep leases "$H")"
grep -q "jobs waiting for a Nerd lease to clear: 2026-10-01_auto" "$H" || fail "pending job not in HEALTH.md"
rm "$T/tree/_queue/leases/nerd-interactive-x.md"; python3 "$W" >/dev/null 2>&1
grep -q "job 2026-10-01_auto released (no Nerd lease)" "$T/tree/_queue/log/"*.log || fail "pending job not released after the lease cleared"
grep -l "^session: watcher: Nerd lease cleared" "$R"/*job.run*.md >/dev/null 2>&1 || fail "released job.run not run in the same tick"
grep -q '2026-10-01_auto' "$T/state/advance-pending.json" && fail "pending mark not dropped"
rm -f "$T/tree/_queue/requests/"*.md "$T/tree/_queue/leases/"*.md
# sleep-aware schedules (ERRORS.md #8): a launchd request waits until the Mac has been awake SETTLE_MIN; others don't
python3 -c "import json,time; f='$T/state/ticks.json'; d=json.load(open(f)); d['last']=time.time()-3600; json.dump(d,open(f,'w'))"
python3 "$E" ping --by launchd >/dev/null; python3 "$E" ping --by cowork >/dev/null; rm -f "$R"/*.md
python3 "$W" >/dev/null 2>&1
[ "$(ls "$T/tree/_queue/requests/" | wc -l | tr -d ' ')" = "1" ] || fail "launchd request not held (or the other not run) after a wake: $(ls "$T/tree/_queue/requests/")"
grep -q "1 held" "$H" || fail "held schedule not in HEALTH.md: $(grep 'awake since' "$H")"
grep -q "^session: schedule ping" "$T/tree/_queue/requests/"*.md || fail "launchd request without a schedule session"
python3 -c "import json,time; f='$T/state/ticks.json'; d=json.load(open(f)); d['awake_since']=time.time()-700; json.dump(d,open(f,'w'))"
python3 "$W" >/dev/null 2>&1
[ -z "$(ls "$T/tree/_queue/requests/")" ] || fail "launchd request still held after 10 min awake"
# --wait checks HEALTH staleness first: a stopped watcher is reported at once, not after the timeout
touch -t 202601010000 "$H"; s=$(date +%s); out=$(python3 "$E" ping --wait 15); rc=$?
[ $rc = 3 ] && echo "$out" | grep -q "watcher looks stopped" && [ $(( $(date +%s) - s )) -lt 5 ] || fail "stale HEALTH not caught before waiting (rc $rc): $out"
rm -f "$T/tree/_queue/requests/"*.md
echo "test-watcher: PASS"
