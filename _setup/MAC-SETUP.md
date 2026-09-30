---
name: Mac-side setup (Claude Code handoff)
type: doc
lobe: both
description: What a Claude Code session on the silver Mac builds next: the watcher, launchd schedules, Sancho-Audio, encrypted secrets, Sancho-Private, the autocommit fix, and the ping round-trip. Stage "mac-side" of the Build Sancho job.
sources: ["_design/architecture.md §1 §6.5 §6.6 §11 §16.3", "_design/migration-plan.md §5"]
---
# Mac-side setup · handoff to Claude Code

Cowork's shell is a sandbox; these steps need the Mac itself. Run in Claude Code with `~/Sync/Sancho` as the working folder. Read `CLAUDE.md`, then `_design/STATUS.md`, then this file. Every script gets the standard header and a test under `_setup/tests/<name>/`; run `python3 _setup/test-all.py` before calling any step done. Do not touch `alaska-2027/`, `_reference/`, or anything under `~/Sync/Gordonium Enterprises Sync/`.

## 1. Folders and repos
- `mkdir -p ~/Sync/Sancho-Audio/{inbox,processed,voiceprints/recordings,voiceprints/speakers,calendar-cache,zoom}` and `~/Sync/Sancho-Secrets`.
- `~/Sancho-Private/`: `git init`, a README with frontmatter, its own private GitHub remote (Gordon creates the empty repo, as he did for the kit; SSH only, no `gh`). Copy `_setup/git-autocommit.sh` there as a second install pointed at that path.
- Confirm `~/.sancho.git` is live: `git -C ~/Sync/Sancho status -sb`; if the launchd autocommit isn't loaded, load it per `_setup/README.md`.

## 2. Secrets (§6.5)
- Install `age` (`brew install age`). Create `~/Sync/Sancho-Secrets/sancho.env.age` from a plaintext template with these names: `GROQ_API_KEY`, `PLAUD_BEARER_TOKEN`, `HUGGINGFACE_TOKEN`, `PUSHOVER_USER`, `PUSHOVER_TOKEN`, `ZOOM_ACCOUNT_ID`, `ZOOM_CLIENT_ID`, `ZOOM_CLIENT_SECRET`, `CALENDAR_ICS_URL`. Passphrase chosen by Gordon at the prompt; never written anywhere.
- Commands `sancho.unlock` (decrypt → `~/.config/sancho/env`, mode 600) and `sancho.lock-secrets` (re-encrypt after edits). Lint rule: plaintext newer than the `.age` file fails the build.
- The existing values: Groq/Plaud/HF are in v3's `.env` in the Sync copy of jarvis-v3 (read them once from there, then delete that `.env` from the Sync copy; the black Mac keeps its own). Pushover: Gordon signs up and pastes user + app token. Zoom and calendar: later.

## 3. The watcher (§1)
- `_setup/sancho-watcher.py`: stdlib; reads `_setup/commands.md` as the allowlist; polls `_queue/requests/` (launchd `WatchPaths` + 60 s `StartInterval`); one lockfile; per-command timeout; loads env from `~/.config/sancho/env`; writes `_queue/results/<same name>.md` with `command, status, started_at, finished_at, exit_code, log` and the last 40 lines of output; deletes the request by atomic rename; writes `_queue/HEALTH.md` after every run and tick (watcher last seen, Mac awake/slept via `pmset -g log`, runs today, failures, leases present, stale session notes).
- launchd: `com.sancho.watcher.plist` (WatchPaths on requests/, StartInterval 60, RunAtLoad). Also schedules from `commands.md`: `index.build`+`lint`+`map.build` nightly 02:00 (one plist, `_setup/nightly.sh`), `test.all` 02:30, `git.commit` hourly (already exists).
- Test: submit a `ping` request file, see the result within 60 s; `_setup/tests/watcher/` does this against a temp queue.

## 4. Autocommit fix (§11)
- In `git-autocommit.sh`: before committing, list staged files over 5 MB or binary (reuse the hook's checks), `git restore --staged` each, write them to `_setup/GIT-EXCLUDED.md` (generated: path, size, reason, first seen), commit the rest. Commit message lists live sessions from `_queue/leases/`. Add `_setup/tests/git-autocommit/` with a temp repo containing one oversize file: commit must succeed and exclude it.

## 5. notify.py (§13.6)
- `_setup/notify.py <level> <message>`: Pushover POST, single hardcoded recipient from env, priority by level, dedupe by state file (fire on state change, then at most daily). Command `notify.test`. Test with a fake endpoint.

## 6. mac.stay-awake (§16.3)
- Command `mac.stay-awake on|off` toggling `caffeinate` under launchd; state in HEALTH.md.

## 7. Report
Update `_queue/jobs/<date>_build-sancho.md` (stage `mac-side` → done, `pipeline` → active), `_design/STATUS.md`, and `_design/decisions.md`; run `python3 _setup/build-index.py && python3 _setup/lint-layers.py && python3 _setup/build-map.py && python3 _setup/test-all.py`; commit. One-line receipt to Gordon.
