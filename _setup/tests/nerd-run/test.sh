#!/usr/bin/env bash
# name: test-nerd-run
# type: script
# description: nerd-run.py with a fake claude binary: the task reaches the prompt; the run is confined (settings file, project-only setting sources, no MCP, dontAsk, no permission bypass, web/push/commit/rm denied); a lease exists during the run and is gone after; the transcript is kept; the receipt line is reported; a hung session is killed at the timeout; a task_file outside the tree is refused; the settings file sandboxes writes and network.
# why: this command lets a request file start an unattended Claude Code session; its confinement must be proven, not assumed.
# reads: _setup/nerd-run.py, _setup/nerd-settings.json
# writes: temp files only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SRC="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d) && [ -d "$T" ] || { echo "test-nerd-run: FAIL: no temp dir"; exit 1; }; trap 'rm -rf "$T"' EXIT
fail() { echo "test-nerd-run: FAIL: $*"; exit 1; }
mkdir -p "$T/tree/_setup" "$T/tree/_queue" "$T/state"; touch "$T/tree/CLAUDE.md"
cp "$SRC/nerd-run.py" "$SRC/sancho_lib.py" "$SRC/nerd-settings.json" "$T/tree/_setup/"
cat > "$T/claude" <<'PY'
#!/usr/bin/env python3
import sys, json, os, time
open(os.environ["FAKE_ARGV"], "w").write(json.dumps(sys.argv[1:]))
open(os.environ["FAKE_ENV"], "w").write(os.environ.get("SANCHO_IN_NERD", ""))
open(os.environ["FAKE_LEASES"], "w").write(" ".join(os.listdir(os.path.join(os.getcwd(), "_queue/leases"))))
if os.environ.get("FAKE_HANG"): time.sleep(60)
print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": "did the thing\nReceipt: _setup/x.md"}))
PY
chmod +x "$T/claude"
export SANCHO_ROOT="$T/tree" SANCHO_STATE="$T/state" SANCHO_CLAUDE_BIN="$T/claude" SANCHO_KIT="$T/kit" FAKE_ARGV="$T/argv.json" FAKE_LEASES="$T/leases.txt" FAKE_ENV="$T/innerd.txt"
R="$T/tree/_queue/req.md"; printf -- '---\ncommand: nerd.run\ntask: rebuild the widget index\nrequested_by: cowork\n---\n' > "$R"
out=$(SANCHO_REQUEST_FILE="$R" SANCHO_REQUEST_ID=r1 python3 "$T/tree/_setup/nerd-run.py") || fail "run failed: $out"
echo "$out" | grep -q "nerd-run: ok" && echo "$out" | grep -q "Receipt: _setup/x.md" || fail "no ok/receipt: $out"
python3 - "$T/argv.json" "$T/tree/_setup/nerd-settings.json" <<'PY' || exit 1
import json, sys
a = json.load(open(sys.argv[1])); s = " ".join(a)
def need(c, m):
    if not c: print(f"test-nerd-run: FAIL: {m}"); sys.exit(1)
need("rebuild the widget index" in a[a.index("-p") + 1], "task not in prompt")
need("--dangerously-skip-permissions" not in a, "permission bypass present")
need(a[a.index("--permission-mode") + 1] == "dontAsk", "permission mode not dontAsk")
need(a[a.index("--setting-sources") + 1] == "project", "user settings not excluded")
need("--strict-mcp-config" in a and a[a.index("--mcp-config") + 1] == '{"mcpServers":{}}', "MCP not disabled")
need(a[a.index("--settings") + 1].endswith("nerd-settings.json"), "settings file not passed")
den = a[a.index("--disallowedTools") + 1:]
for d in ("WebFetch", "WebSearch", "Bash(git push *)", "Bash(git commit *)", "Bash(rm *)", "Bash(curl *)"):
    need(d in den, f"{d} not denied")
st = json.load(open(sys.argv[2]))
sb = st.get("sandbox", {})
need(sb.get("enabled") is True, "sandbox not enabled in nerd-settings.json")
need(sb.get("allowUnsandboxedCommands") is False, "unsandboxed escape hatch not closed")
PY
grep -q "nerd-r1.md" "$T/leases.txt" || fail "no lease during the run"
[ "$(cat "$T/innerd.txt")" = "r1" ] || fail "session not marked SANCHO_IN_NERD"
[ -z "$(ls "$T/tree/_queue/leases")" ] || fail "lease left behind"
[ -s "$T/tree/_queue/results/r1.transcript.jsonl" ] || fail "transcript not kept"
# timeout kills a hung session
out=$(FAKE_HANG=1 SANCHO_REQUEST_FILE="$R" SANCHO_REQUEST_ID=r2 python3 "$T/tree/_setup/nerd-run.py" --timeout 2) && fail "hung run reported ok"
echo "$out" | grep -q "timeout after 2 s" || fail "no timeout: $out"
# task_file outside the tree is refused
printf -- '---\ncommand: nerd.run\ntask_file: ../../etc/passwd\n---\n' > "$R"
out=$(SANCHO_REQUEST_FILE="$R" SANCHO_REQUEST_ID=r3 python3 "$T/tree/_setup/nerd-run.py" 2>&1) && fail "outside task_file accepted"
echo "$out" | grep -q "inside the tree" || fail "wrong refusal: $out"
echo "test-nerd-run: PASS"
