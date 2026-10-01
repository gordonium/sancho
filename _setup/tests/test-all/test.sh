#!/usr/bin/env bash
# name: test-test-all
# type: script
# description: test-all.py must exit non-zero when a suite fails and write TESTS.md; off the Mac or inside a nerd.run sandbox the board is untouched; under launchd's short PATH suites still get /usr/sbin and /sbin; --fail-tail prints failing suites' output with the summary still last.
# why: the runner is the root of the test board.
# reads: a temp fixture
# writes: temp files
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"; unset SANCHO_IN_NERD  # the fixture board is a temp file; the guard is tested below
T=$(mktemp -d) && [ -d "$T" ] || { echo "test-test-all: FAIL: no temp dir"; exit 1; }; mkdir -p "$T/tests/p" "$T/tests/f"; cp "$ROOT/test-all.py" "$T/"
printf '#!/usr/bin/env bash\necho ok\n' > "$T/tests/p/test.sh"; printf '#!/usr/bin/env bash\nexit 1\n' > "$T/tests/f/test.sh"
python3 "$T/test-all.py" >/dev/null 2>&1; rc=$?
[ $rc -ne 0 ] && grep -q "| f | FAIL" "$T/TESTS.md" && grep -q "| p | PASS" "$T/TESTS.md" && echo "test-test-all: PASS (board)" || { echo "test-test-all: FAIL rc=$rc"; exit 1; }
# off the Mac: requires-mac suites skip, board untouched (ERRORS.md #2)
T2=$(mktemp -d) && [ -d "$T2" ] || { echo "test-test-all: FAIL: no temp dir"; exit 1; }; mkdir -p "$T2/tests/m" "$T2/tests/p"; cp "$ROOT/test-all.py" "$T2/"
printf '#!/usr/bin/env bash\n# requires: mac\nexit 1\n' > "$T2/tests/m/test.sh"; printf '#!/usr/bin/env bash\necho ok\n' > "$T2/tests/p/test.sh"
echo "old board" > "$T2/TESTS.md"
out=$(SANCHO_PLATFORM=linux python3 "$T2/test-all.py" 2>&1); rc=$?
[ $rc -eq 0 ] && [ "$(cat "$T2/TESTS.md")" = "old board" ] && echo "$out" | grep -q "SKIP" && echo "test-test-all: PASS" || { echo "test-test-all: FAIL off-Mac rc=$rc: $out"; exit 1; }
echo "old board" > "$T2/TESTS.md"; SANCHO_IN_NERD=r1 python3 "$T2/test-all.py" >/dev/null 2>&1
[ "$(cat "$T2/TESTS.md")" = "old board" ] || { echo "test-test-all: FAIL: board written from inside a nerd.run session"; exit 1; }
# launchd's short PATH (ERRORS.md #8): suites still find /usr/sbin and /sbin tools; --fail-tail shows a failing suite's output, summary stays last
mkdir -p "$T/tests/path"; printf '#!/usr/bin/env bash\ncase ":$PATH:" in *:/usr/sbin:*) case ":$PATH:" in *:/sbin:*) echo ok; exit 0;; esac;; esac\necho "PATH=$PATH"; exit 1\n' > "$T/tests/path/test.sh"
printf '#!/usr/bin/env bash\necho first detail\necho second detail\nexit 1\n' > "$T/tests/f/test.sh"
mkdir -p "$T/tests/.claude/.cc-writes"  # tool state, not a suite
out=$(env PATH=/usr/bin:/bin python3 "$T/test-all.py" --fail-tail 5 2>&1)
echo "$out" | grep -q "| path | PASS" || { echo "test-test-all: FAIL: suite lacks /usr/sbin:/sbin under launchd's PATH: $out"; exit 1; }
echo "$out" | grep -q "^### f" && echo "$out" | grep -q "first detail" || { echo "test-test-all: FAIL: --fail-tail did not show the failing suite: $out"; exit 1; }
echo "$out" | tail -1 | grep -q "^test-all: " || { echo "test-test-all: FAIL: summary not the last line"; exit 1; }
echo "$out" | grep -q "| .claude |" && { echo "test-test-all: FAIL: a dot-folder was run as a suite"; exit 1; }
rm -rf "$T" "$T2"
