#!/usr/bin/env bash
# name: test-git-autocommit
# type: script
# description: In a temp repo with one oversize file, one binary and one note, autocommit must commit the note, exclude the other two, list them in GIT-EXCLUDED.md, keep first-seen stable, and stay quiet on a rerun.
# why: architecture §11: one oversize file must never stall every commit again.
# reads: _setup/git-autocommit.sh
# writes: a temp repo only
# test: (this is the test)
set -u; HERE="$(cd "$(dirname "$0")" && pwd)"; SCRIPT="$HERE/../../git-autocommit.sh"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
fail() { echo "test-git-autocommit: FAIL: $*"; exit 1; }
cd "$T" && git init -q && git config user.email t@t && git config user.name t && mkdir -p _setup _queue/leases
echo seed > seed.md && git add -A && git commit -qm seed
echo "a note" > note.md
head -c 6000000 /dev/zero | tr '\0' 'a' > big.md
printf '\x00\x01\x02binary' > blob.dat
touch _queue/leases/sess-abc.md
out=$(SANCHO_WORKTREE="$T" bash "$SCRIPT" test 2>&1) || fail "exit $?: $out"
git ls-files --error-unmatch note.md >/dev/null 2>&1 || fail "note.md not committed"
git ls-files --error-unmatch big.md >/dev/null 2>&1 && fail "big.md was committed"
git ls-files --error-unmatch blob.dat >/dev/null 2>&1 && fail "blob.dat was committed"
grep -q "| big.md |.*over 5 MB" _setup/GIT-EXCLUDED.md || fail "big.md not listed"
grep -q "| blob.dat |.*binary" _setup/GIT-EXCLUDED.md || fail "blob.dat not listed"
git log -1 --format=%s | grep -q "sessions: sess-abc" || fail "commit message lacks live session"
[ -f big.md ] || fail "big.md was moved or deleted"
first=$(grep "| big.md |" _setup/GIT-EXCLUDED.md)
out2=$(SANCHO_WORKTREE="$T" bash "$SCRIPT" test 2>&1) || fail "rerun exit $?: $out2"
echo "$out2" | grep -q "nothing to commit" || fail "rerun committed again: $out2"
[ "$(grep "| big.md |" _setup/GIT-EXCLUDED.md)" = "$first" ] || fail "first-seen changed on rerun"
# a tracked file that grows past the cap is unstaged, not deleted from git
head -c 6000000 /dev/zero | tr '\0' 'b' > note.md
SANCHO_WORKTREE="$T" bash "$SCRIPT" test >/dev/null 2>&1 || fail "grown-file run failed"
git cat-file -e HEAD:note.md 2>/dev/null || fail "grown tracked file was staged as a deletion"
echo "test-git-autocommit: PASS"
