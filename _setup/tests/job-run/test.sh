#!/usr/bin/env bash
# name: test-job-run
# type: script
# description: job-run.py on a fixture job (a, b, gate g, d) with a fake nerd.run: a and b run and are marked done, the walk stops at the human gate with one push and current=g; a stage that fails once is retried and passes; a stage that fails twice stops the job as failed with a push; a session without a `Stage: done` line counts as blocked; a `Stage: done` with a red test board is not done; a done job resumes past done stages; paths outside _queue/jobs are refused.
# why: job.run drives unattended rounds; a wrong advance or a silent stop is exactly what must-never 10 forbids.
# reads: _setup/job-run.py, sancho_lib.py, notify.py
# writes: temp files only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d) && [ -d "$T" ] || { echo "test-job-run: FAIL: no temp dir"; exit 1; }; trap 'rm -rf "$T"' EXIT
fail() { echo "test-job-run: FAIL: $*"; exit 1; }
mkdir -p "$T/tree/_setup" "$T/tree/_queue/jobs" "$T/state"; touch "$T/tree/CLAUDE.md"
cp "$SRC/job-run.py" "$SRC/sancho_lib.py" "$SRC/notify.py" "$T/tree/_setup/"
# fake nerd: outcome per stage from $T/plan/<stage> (lines consumed one per attempt: ok | fail | nomark)
mkdir -p "$T/plan"
cat > "$T/nerd" <<'PY'
import sys, os, re
task = sys.argv[sys.argv.index("--task") + 1]
st = re.search(r"Do stage `([^`]+)`", task).group(1)
f = os.path.join(os.environ["PLAN"], st)
lines = open(f).read().split() if os.path.exists(f) else ["ok"]
o = lines[0]; open(f, "w").write(" ".join(lines[1:] or ["ok"]))
open(os.environ["PLAN"] + "/calls", "a").write(st + "\n")
if o == "ok": print("worked\nStage: done\nReceipt: x"); sys.exit(0)
if o == "nomark": print("worked but forgot\nReceipt: x"); sys.exit(0)
print("broke\nStage: blocked: tests red"); sys.exit(0)
PY
job(){ cat > "$T/tree/_queue/jobs/2026-09-30_fix.md" <<MD
---
job: fix
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
# push endpoint
python3 - "$T" <<'PY' &
import sys, http.server
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        b = self.rfile.read(int(self.headers["Content-Length"])).decode(); open(sys.argv[1] + "/pushes", "a").write(b + "\n")
        self.send_response(200); self.end_headers(); self.wfile.write(b"{}")
    def log_message(self, *a): pass
s = http.server.HTTPServer(("127.0.0.1", 0), H); open(sys.argv[1] + "/port", "w").write(str(s.server_port)); s.serve_forever()
PY
SRV=$!; trap 'kill $SRV 2>/dev/null; wait $SRV 2>/dev/null; rm -rf "$T"' EXIT
for i in $(seq 50); do [ -s "$T/port" ] && break; sleep 0.1; done
printf 'import sys, os\nsys.exit(1 if os.path.exists(os.environ["PLAN"] + "/red") else 0)\n' > "$T/testall"
export SANCHO_TEST_ALL_BIN="$T/testall" SANCHO_ROOT="$T/tree" SANCHO_STATE="$T/state" SANCHO_NERD_BIN="$T/nerd" PLAN="$T/plan" PUSHOVER_USER=u PUSHOVER_TOKEN=t SANCHO_PUSHOVER_URL="http://127.0.0.1:$(cat "$T/port")/"
J="$T/tree/_queue/jobs/2026-09-30_fix.md"; R="$T/tree/_setup/job-run.py"
# 1. two stages then the gate; b fails once and is retried
job; echo "fail ok" > "$T/plan/b"
python3 "$R" fix --foreground | grep -q "stopped at human gate g" || fail "did not stop at gate"
grep -q "{name: a, status: done" "$J" && grep -q "{name: b, status: done" "$J" || fail "a/b not done: $(grep name: "$J")"
grep -q 'stage `a` done' "$J" && grep -q 'stage `b` done' "$J" || fail "stage-done log lines missing"
grep -q "gate: human, status: waiting" "$J" && grep -q "^current: g" "$J" || fail "gate state wrong: $(grep -E 'name: g|current' "$J")"
[ "$(grep -c '^b$' "$T/plan/calls")" = "2" ] || fail "b not retried exactly once"
grep -q "waiting+for+you" "$T/pushes" || fail "no push at the gate"
grep -q "d" "$T/plan/calls" && grep -q "^d$" "$T/plan/calls" && fail "ran past the gate"
# 2. after Gordon passes the gate, the walk resumes at d
sed -i '' 's/gate: human, status: waiting/gate: human, status: done/' "$J"
python3 "$R" fix --foreground | grep -q "all stages done" || fail "did not finish after the gate"
grep -q "{name: d, status: done" "$J" || fail "d not done"
# 3. two failures stop the job; a missing Stage line counts as a failure
job; rm -f "$T/plan/calls"; echo "nomark fail" > "$T/plan/a"
python3 "$R" fix --foreground | grep -q "stage a failed twice" || fail "double failure not stopped"
grep -q "{name: a, status: failed" "$J" || fail "a not marked failed"
grep -q "failed+twice" "$T/pushes" || fail "no push on failure"
grep -q "^b$" "$T/plan/calls" && fail "ran b after a failed"
# 4. a session that says done while the board is red is not done
job; rm -f "$T/plan/calls" "$T/plan/a"; touch "$T/plan/red"
python3 "$R" fix --foreground | grep -q "stage a failed twice" || fail "red board accepted as done"
grep -q "tests are red" "$J" || fail "job file lacks the red-board reason"
rm -f "$T/plan/red"
# 5. outside _queue/jobs refused
python3 "$R" ../../etc/passwd --foreground >/dev/null 2>&1 && fail "path outside _queue/jobs accepted"
echo "test-job-run: PASS"
