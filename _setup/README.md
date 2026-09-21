# _setup: Sancho's git and automation

**Why this folder exists:** Sancho is a git repo whose working tree lives inside a sync.com folder. That combination corrupts if done the obvious way, so the setup is slightly unusual and lives here where it can be re-run and understood.

**The shape:**

```
~/Sync/Sancho/          working tree (synced by sync.com, on 3 machines + cloud)
~/Sync/Sancho/.git      a one-line pointer FILE, not a folder
~/.sancho.git/          the real git database (this Mac only, never synced)
github.com/<you>/sancho private remote = history backup
```

**Rule:** the repo is knowledge only. Markdown, VTT, JSON, scripts. No audio, no images, nothing over 5 MB. Enforced twice: `.gitignore` (known media extensions) and `hooks/pre-commit` (size cap + binary check). Raw audio lives in `~/Sync/Sancho-Audio/`, which is synced for backup but is not part of the repo.

## Files

| File | Does | Test |
|---|---|---|
| `git-init.sh` | One-time bootstrap. Separate git dir, hook install, first commit, GitHub remote. Idempotent. | Run twice; second run changes nothing. |
| `hooks/pre-commit` | Rejects big or binary files at commit time. | Stage a 6 MB junk file; commit must fail. |
| `git-autocommit.sh` | Commit + push everything, timestamped. Quiet if nothing changed. | Edit a file, run, see new commit. Run again, "nothing to commit". |
| `com.sancho.autocommit.plist` | launchd job: runs autocommit daily at 23:30. | `launchctl list \| grep sancho` |

## First-time install (Terminal on the Mac)

```bash
chmod +x ~/Sync/Sancho/_setup/*.sh ~/Sync/Sancho/_setup/hooks/*
bash ~/Sync/Sancho/_setup/git-init.sh
cp ~/Sync/Sancho/_setup/com.sancho.autocommit.plist ~/Library/LaunchAgents/
sed -i '' "s#__HOME__#$HOME#g" ~/Library/LaunchAgents/com.sancho.autocommit.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.sancho.autocommit.plist
```

`git-init.sh` prints the two manual steps for the GitHub remote. The GitHub CLI (`gh`) is deliberately not on this Mac (so nothing can publish a Release by accident); don't install it.

## If the Mac dies

sync.com has the working tree. GitHub has the history. On a new Mac: restore `~/Sync/Sancho` from sync.com, then `git clone --separate-git-dir ~/.sancho.git <remote> /tmp/x`, copy `/tmp/x/.git` pointer over, and you're back. (Write this out properly once the remote exists.)
