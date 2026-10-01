#!/usr/bin/env bash
# name: test-job-run
# type: script
# description: job-run.py on a fixture job (a, b, gate g, d) with a fake nerd.run and a push sink: a and b run and are marked done, the walk stops at the human gate with one warn and current=g; troubleshoot loop: a stage that fails once with a fixable cause passes on attempt 2, and attempt 2's task carries the evidence file and the diagnose-first instruction; a stage that fails identically twice stops at 2 with a warn naming the evidence; three different failures stop after 3; `Stage: blocked: <what>` pauses at a gate (status blocked, warn) instead of failing; a missing verdict line counts as failed; a `Stage: done` with a red board is not done; a done job resumes past done stages; --auto refuses a job without `advance: auto`, leaves a failed stage alone, and yields to a live interactive Nerd lease (job marked pending for the watcher); paths outside _queue/jobs are refused.
# why: job.run drives unattended rounds; a wrong advance or a silent stop is exactly what must-never 10 forbids.
# reads: _setup/job-run.py, sancho_lib.py, notify.py, notify-reasons.md
# writes: temp files only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d) && [ -d "$T" ] || { echo "test-job-run: FAIL: no temp dir"; exit 1; }; trap 'rm -rf "$T"' EXIT
fail() { echo "test-job-run: FAIL: $*"; exit 1; }
mkdir -p "$T/tree/_setup" "$T/tree/_queue/jobs" "$T/tree/_queue/leases" "$T/state"; touch "$T/tree/CLAUDE.md"
cp "$SRC/job-run.py" "$SRC/sancho_lib.py" "$SRC/notify.py" "$SRC/notify-reasons.md" "$T/tree/_setup/"
# fake nerd: outcome per stage from $T/plan/<stage> (tokens consumed one per attempt: ok | fail | failN | nomark | blocked)
mkdir -p "$T/plan"
cat > "$T/nerd" <<'PY'
import sys, os, re
task = sys.argv[sys.argv.index("--task") + 1]
st = re.search(r"Do stage `([^`]+)`", task).group(1)
f = os.path.join(os.environ["PLAN"], st)
lines = open(f).read().split() if os.path.exists(f) else ["ok"]
o = lines[0]; open(f, "w").write(" ".join(lines[1:] or ["ok"]))
open(os.environ["PLAN"] + "/calls", "a").write(st + "\n")
open(os.environ["PLAN"] + "/task-" + os.environ["SANCHO_REQUEST_ID"].rsplit("-", 2)[-2] + "-" + os.environ["SANCHO_REQUEST_ID"].rsplit("-", 1)[-1], "w").write(task)
if o == "ok": print("worked\nStage: done\nReceipt: x"); sys.exit(0)
if o == "nomark": print("worked but forgot\nReceipt: x"); sys.exit(0)
if o == "blocked": print("need the passphrase\nStage: blocked: Gordon types the age passphrase in Terminal\nReceipt: x"); sys.exit(0)
print(f"broke\nStage: failed: cause {o}"); sys.exit(0)
PY
job(){ cat > "$T/tree/_queue/jobs/2026-09-30_fix.md" <<MD
---
job: fix
${1:-}
stages:
  - {name: a, status: active, note: "first"}
  - {name: b, status: pending, note: "second"}
  - {name: g, gate: human, status: pending, note: "Gordon checks five facts"}
  - {name: d, status: pending, note: "after gate"}
current: a
---
# Fix
MD
}
printf 'import sys, os\nif os.path.exists(os.environ["PLAN"] + "/red"): print("| x | FAIL | boom |"); sys.exit(1)\nprint("all green")\n' > "$T/testall"
export SANCHO_TEST_ALL_BIN="$T/testall" SANCHO_ROOT="$T/tree" SANCHO_STATE="$T/state" SANCHO_NERD_BIN="$T/nerd" PLAN="$T/plan" PUSHOVER_USER=u PUSHOVER_TOKEN=t SANCHO_PUSHOVER_URL="file://$T/pushes" SANCHO_JOB_NERD_WAIT=2
J="$T/tree/_queue/jobs/2026-09-30_fix.md"; R="$T/tree/_setup/job-run.py"; RES="$T/tree/_queue/results"
pushes(){ python3 -c "import sys,urllib.parse as u; [print(u.parse_qs(l.strip())['priority'][0], u.parse_qs(l.strip())['message'][0]) for l in open('$T/pushes')]" 2>/dev/null; }
# 1. two stages then the gate; b fails once with a fixable cause and passes on attempt 2
job; echo "fail ok" > "$T/plan/b"
python3 "$R" fix --foreground | grep -q "stopped at human gate g" || fail "did not stop at gate"
grep -q "{name: a, status: done" "$J" && grep -q "{name: b, status: done" "$J" || fail "a/b not done: $(grep name: "$J")"
grep -q 'stage `a` done' "$J" && grep -q 'stage `b` done' "$J" || fail "stage-done log lines missing"
grep -q "gate: human, status: waiting" "$J" && grep -q "^current: g" "$J" || fail "gate state wrong: $(grep -E 'name: g|current' "$J")"
[ "$(grep -c '^b$' "$T/plan/calls")" = "2" ] || fail "b not retried exactly once"
ls "$RES"/*-b-evidence-1.md >/dev/null 2>&1 || fail "no evidence file for b's failed attempt"
E=$(ls "$RES"/*-b-evidence-1.md); for s in "## Verdict" "## Test board" "## Watcher log" "## Session transcript"; do grep -q "$s" "$E" || fail "evidence lacks $s"; done
grep -q "attempt 2 of 3" "$T/plan/task-b-2" && grep -q "b-evidence-1.md" "$T/plan/task-b-2" && grep -q "Cause:" "$T/plan/task-b-2" || fail "attempt 2 lacks evidence/diagnose-first: $(tail -5 "$T/plan/task-b-2")"
grep -q "attempt 2" "$T/plan/task-a-1" && fail "attempt 1 got a retry brief"
pushes | grep -q "^0 Job 2026-09-30_fix is waiting for you at g" || fail "no warn at the gate: $(pushes)"
grep -q "^d$" "$T/plan/calls" && fail "ran past the gate"
# 2. after Gordon passes the gate, the walk resumes at d
sed -i '' 's/gate: human, status: waiting/gate: human, status: done/' "$J"
python3 "$R" fix --foreground | grep -q "all stages done" || fail "did not finish after the gate"
grep -q "{name: d, status: done" "$J" || fail "d not done"
pushes | tail -1 | grep -q "^-1 Job 2026-09-30_fix: all stages done" || fail "completion not an info push: $(pushes | tail -1)"
# 3. identical failure twice stops at 2 (no progress); a missing verdict line counts as failed
job; rm -f "$T/plan/calls" "$T/pushes"; echo "fail fail ok" > "$T/plan/a"
python3 "$R" fix --foreground | grep -q "identical failure on attempts 1 and 2" || fail "identical failures not stopped early"
[ "$(grep -c '^a$' "$T/plan/calls")" = "2" ] || fail "a ran $(grep -c '^a$' "$T/plan/calls") times, want 2"
grep -q "{name: a, status: failed" "$J" || fail "a not marked failed"
pushes | grep -q "^0 Job 2026-09-30_fix stopped at a: .*Evidence: _queue/results/.*-a-evidence-2.md" || fail "no warn with evidence path: $(pushes)"
grep -q "^b$" "$T/plan/calls" && fail "ran b after a failed"
job; rm -f "$T/plan/calls"; echo "nomark fail2 fail3 ok" > "$T/plan/a"
python3 "$R" fix --foreground | grep -q "failed 3 attempts" || fail "three different failures did not stop after 3"
[ "$(grep -c '^a$' "$T/plan/calls")" = "3" ] || fail "a not tried 3 times"
# 4. blocked pauses at a gate, not a failure; a manual rerun after Gordon acts resumes it
job; rm -f "$T/plan/calls" "$T/pushes"; echo "blocked ok" > "$T/plan/a"
python3 "$R" fix --foreground | grep -q "blocked at a: Gordon types the age passphrase" || fail "blocked not paused"
grep -q "{name: a, status: blocked, note: \"first\", blocked: Gordon types the age passphrase in Terminal}" "$J" || fail "blocked state: $(grep 'name: a' "$J")"
pushes | grep -q "^0 Job 2026-09-30_fix paused at a; needs you: Gordon types" || fail "no warn on blocked: $(pushes)"
[ "$(grep -c '^a$' "$T/plan/calls")" = "1" ] || fail "blocked stage retried"
grep -q "unregistered" "$T/pushes" && fail "job.run sent a warn with an unregistered reason: $(pushes)"
python3 "$R" fix --foreground | grep -q "stopped at human gate g" || fail "manual rerun after blocked did not resume"
grep "{name: a, status: done" "$J" | grep -q "blocked:" && fail "blocked field left on a done stage"
grep -q "{name: a, status: done" "$J" || fail "a not done after the manual rerun"
# 5. a session that says done while the board is red is not done
job; rm -f "$T/plan/calls" "$T/plan/a"; touch "$T/plan/red"
python3 "$R" fix --foreground | grep -q "stage a failed" || fail "red board accepted as done"
grep -q "tests are red" "$J" || fail "job file lacks the red-board reason"
rm -f "$T/plan/red"
# 6. --auto: only for advance: auto; never re-runs a failed stage; yields to an interactive Nerd's lease
job; rm -f "$T/plan/calls"
python3 "$R" fix --foreground --auto | grep -q "not \`advance: auto\`" || fail "auto ran a manual job"
[ -e "$T/plan/calls" ] && fail "auto on a manual job called the Nerd"
job "advance: auto"; sed -i '' 's/{name: a, status: active/{name: a, status: failed/' "$J"
python3 "$R" fix --foreground --auto | grep -q "left at failed stage a" || fail "auto re-ran a failed stage"
[ -e "$T/plan/calls" ] && fail "auto called the Nerd for a failed stage"
job "advance: auto"; printf -- '---\nname: nerd-interactive-x\ntype: lease\nkind: interactive\nsession: interactive\npid: %s\n---\n' $$ > "$T/tree/_queue/leases/nerd-interactive-x.md"
python3 "$R" fix --foreground --auto | grep -q "waiting: interactive Nerd" || fail "auto did not yield to the interactive lease"
[ -e "$T/plan/calls" ] && fail "auto ran a stage beside an interactive Nerd"
grep -q '"2026-09-30_fix"' "$T/state/advance-pending.json" || fail "job not marked pending for the watcher"
rm "$T/tree/_queue/leases/nerd-interactive-x.md"
python3 "$R" fix --foreground --auto | grep -q "stopped at human gate g" || fail "auto did not walk once the lease cleared"
grep -q '"2026-09-30_fix"' "$T/state/advance-pending.json" && fail "pending mark not cleared after the walk"
# 7. outside _queue/jobs refused
python3 "$R" ../../etc/passwd --foreground >/dev/null 2>&1 && fail "path outside _queue/jobs accepted"
echo "test-job-run: PASS"
