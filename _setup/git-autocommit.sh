#!/usr/bin/env bash
# Sancho auto-commit
# WHY:  commits must not depend on anyone remembering. History is provenance.
# WHAT: stages everything (subject to .gitignore + pre-commit hook), commits
#       with a timestamp and a short summary of what changed, pushes if a
#       remote exists. Exits quietly when there's nothing to commit.
#       Called by: the daily launchd job (_setup/com.sancho.autocommit.plist)
#       and by the session-end skill once it exists.
# TEST: edit any .md, run this, `git log -1` shows a new commit with today's
#       timestamp. Run again immediately: prints "nothing to commit", no new commit.
# RUN:  bash ~/Sync/Sancho/_setup/git-autocommit.sh [optional message]

set -euo pipefail
WORKTREE="$HOME/Sync/Sancho"
cd "$WORKTREE"

[ -f .git ] || { echo "not a git worktree; run _setup/git-init.sh first"; exit 1; }

git add -A
if git diff --cached --quiet; then
  echo "nothing to commit"
  exit 0
fi

stamp=$(date "+%Y-%m-%d %H:%M")
changed=$(git diff --cached --name-only | wc -l | tr -d ' ')
summary=$(git diff --cached --name-only | sed 's#^\([^/]*\)/.*#\1#' | sort | uniq -c | sort -rn | head -4 | awk '{printf "%s(%s) ", $2, $1}')
msg="${1:-auto} $stamp: $changed files [$summary]"

# The pre-commit hook runs here. If it rejects, the commit fails loudly, which is the point.
git commit -q -m "$msg"
echo "committed: $msg"

if git remote get-url origin >/dev/null 2>&1; then
  git push -q origin HEAD 2>/dev/null && echo "pushed" || echo "push failed (offline?) — will retry next run"
fi
