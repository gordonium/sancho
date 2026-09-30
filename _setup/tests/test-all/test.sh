#!/usr/bin/env bash
# name: test-test-all
# type: script
# description: test-all.py must exit non-zero when a suite fails and write TESTS.md.
# why: the runner is the root of the test board.
# reads: a temp fixture
# writes: temp files
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; ROOT="$(cd "$HERE/../.." && pwd)"
T=$(mktemp -d); mkdir -p "$T/tests/p" "$T/tests/f"; cp "$ROOT/test-all.py" "$T/"
printf '#!/usr/bin/env bash\necho ok\n' > "$T/tests/p/test.sh"; printf '#!/usr/bin/env bash\nexit 1\n' > "$T/tests/f/test.sh"
python3 "$T/test-all.py" >/dev/null 2>&1; rc=$?
[ $rc -ne 0 ] && grep -q "| f | FAIL" "$T/TESTS.md" && grep -q "| p | PASS" "$T/TESTS.md" && echo "test-test-all: PASS" || { echo "test-test-all: FAIL rc=$rc"; exit 1; }
