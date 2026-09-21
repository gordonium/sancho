#!/usr/bin/env bash
# Sancho git bootstrap
# WHY:  ~/Sync/Sancho is mirrored by sync.com. A .git folder inside a synced
#       folder gets corrupted when sync copies objects mid-commit. So the
#       working tree lives in Sync and the git database lives in ~/.sancho.git,
#       outside Sync. A private GitHub remote is the history backup.
# WHAT: idempotent. Creates the separate git dir, installs the pre-commit hook,
#       makes the first commit, and (if `gh` is installed and logged in) creates
#       a private GitHub repo and pushes. Safe to re-run.
# TEST: run it twice. Second run should say "already initialized" and change nothing.
#       Then `git -C ~/Sync/Sancho log --oneline | head` shows the initial commit.
# RUN:  bash ~/Sync/Sancho/_setup/git-init.sh   (in Terminal on the Mac)

set -euo pipefail

WORKTREE="$HOME/Sync/Sancho"
GITDIR="$HOME/.sancho.git"
REMOTE_NAME="origin"
REPO_NAME="sancho"

cd "$WORKTREE"

if [ -f "$WORKTREE/.git" ] && [ -d "$GITDIR" ]; then
  echo "already initialized: $WORKTREE -> $GITDIR"
else
  git init --separate-git-dir "$GITDIR" "$WORKTREE"
  echo "initialized: working tree $WORKTREE, git dir $GITDIR"
fi

# The .git *file* (a pointer) is the only git artifact inside Sync. Keep sync.com
# from treating it as junk; nothing else to do, it's a one-line text file.

# Install hook (overwrite so updates to _setup/hooks propagate).
mkdir -p "$GITDIR/hooks"
cp "$WORKTREE/_setup/hooks/pre-commit" "$GITDIR/hooks/pre-commit"
chmod +x "$GITDIR/hooks/pre-commit"
echo "hook installed: $GITDIR/hooks/pre-commit"

git config user.name  "${GIT_AUTHOR_NAME:-Gordon}"
git config user.email "${GIT_AUTHOR_EMAIL:-gordons@wizardofads.com}"
git config core.autocrlf false
git config pull.rebase false

# First commit if the repo is empty.
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git add -A
  git commit -m "Sancho: initial commit" || echo "nothing to commit yet"
fi

# Remote: create via gh if available, otherwise print instructions.
if ! git remote get-url "$REMOTE_NAME" >/dev/null 2>&1; then
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    gh repo create "$REPO_NAME" --private --source="$WORKTREE" --remote="$REMOTE_NAME" --push
    echo "remote created and pushed: $REMOTE_NAME"
  else
    cat <<EOF

No GitHub remote yet. Either:
  1. Install GitHub CLI (brew install gh), run 'gh auth login', re-run this script; or
  2. Create a private repo named '$REPO_NAME' on github.com, then:
       git -C "$WORKTREE" remote add $REMOTE_NAME git@github.com:<you>/$REPO_NAME.git
       git -C "$WORKTREE" push -u $REMOTE_NAME main
EOF
  fi
else
  echo "remote present: $(git remote get-url "$REMOTE_NAME")"
fi

echo "done."
