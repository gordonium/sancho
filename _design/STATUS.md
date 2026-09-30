# Sancho build status

Read this first on any new session. Then continue from "Next step."

- **Current phase:** 4 (build). Phase 3 written 2026-09-30 (`migration-plan.md`); Phase 2 approved 2026-09-30.
- **Job file:** `_queue/jobs/2026-09-30_build-sancho.md` (`scaffold` and `mac-side` done; `pipeline` active). Project: `work/copper-leaf/projects/build-sancho/`.
- **Last completed step (2026-09-30, Cowork):** **B0 scaffold.** Tree created per §3; `CLAUDE.md` (37 lines); templates T1–T8 in `_setup/templates/`; `_setup/sancho_lib.py`, `build-index.py`, `lint-layers.py`, `build-map.py`, `test-all.py`, `ping.sh`; `_setup/commands.md` (allowlist + registry); `FOCUS.md`; `personal/me/brief.md`, `watch.md`, `mantras.md`; business.md for six businesses + two brand files; seeds moved home (to-read ×2, goals ×7, work ICE ×7, personal ICE ×3, food and nomad projects); tests: 6 suites, all green; lint green; 66 generated files; `MAP.md` in three levels.
- 2026-09-30 later: `alaska-2027/` moved to `personal/projects/alaska-2027/` with a project.md (Gordon's say); frontmatter added to its 24 docs. Claude Code CLI installed on the silver Mac (v2.1.285, ~/.local/bin); shell wake phrases `hey sancho` / `sancho work` / `sancho nerd` in ~/.zshrc; **the mac-side build session was started by Gordon in Claude Code on 2026-09-30.** If two sessions are open (this Cowork one and that Claude Code one), the Claude Code session owns `_setup/` and `_queue/` until MAC-SETUP.md is done; Cowork stays read-only on those.
- **2026-09-30 evening, Claude Code: `mac-side` done.** Watcher live under launchd (ping round-trip 9 s; `_queue/HEALTH.md` every tick); schedules enqueue (nightly 02:00 index+lint+map, tests 02:30); autocommit hourly, excludes oversize/binary to `_setup/GIT-EXCLUDED.md`, logs push failures (they had failed silently since 09-22; 5 commits pushed); secrets locked in `Sancho-Secrets/sancho.env.age`, unlock verified, v3 `.env` deleted from the Sync copy; `~/Sancho-Private` on GitHub (copperleaf/sancho-private) with its own hourly autocommit; `notify.py`, `mac.stay-awake`, `install-mac.sh`; 13 test suites green. Decisions logged 2026-09-30 (Mac-side build calls).
- **2026-09-30 evening, Claude Code: `pipeline` stage underway.** Pushover live (test push received; info level is silent by design). `_setup/pipeline/earballs.py` ported (fetch, download, Groq, pyannote, voiceprint match with the three states, transcript/speakers/meta writer, STATUS.md, watchdog push, ledger backup, backfill, reprocess, library rebuild); venv at `~/.local/share/sancho/venv`; test suite `pipeline` green against fake Plaud/Groq/Pushover. First real full reconcile: 1,046 Plaud recordings (21 fresh since 09-10, 11.4 h; 1,025 backlog, ~848 h). Decisions logged 2026-09-30 (pipeline port calls); era boundaries provisional, a question for Gordon.
- **Next step:** finish `pipeline`: first fresh batch through diarization, launchd `com.sancho.pipeline` installed, then backfill schedule. Then back in Cowork: the `open` skill, then `earballs-ingest`.
- **Gordon:** traveling in Italy through Oct 6; the Mac closes often. For the mac-side stage he needs to be at the Mac once (passphrase, Pushover signup, GitHub repo for Sancho-Private).

## Requests to the Nerd (from Cowork, 2026-09-30 evening)
- `test-all.py`: skip suites marked `requires: mac` off-macOS and write `TESTS.md` only on the Mac (ERRORS.md #2).
- Watcher: run `lint-layers.py` on files changed since the last tick (or the whole tree; it's fast) and post any problems into `HEALTH.md`, so a bad write shows at the next greeting rather than the next nightly.
- `sancho-private` remote: Gordon is creating a new personal GitHub account; move both remotes there when he gives the name (Leah holds the `copperleaf` credentials).

## Open for Gordon
- What the backlog eras mean (§13.2 overlaps; dates used provisionally).
- Pick two short real recordings for the pipeline's fixture set (Gordon solo; two speakers), §13.4.

## What exists
- `_design/`: architecture (approved), decisions, postmortem, survey, migration-plan, routines-capture, rainbow-rig-shutdown, seeds (now moved; originals kept), reading copy + standalone, tree page.
- Tree: see `MAP.md` Level 0/1; `INDEX.md` everywhere; `work/PROJECTS.md`, `personal/PROJECTS.md`; `work/ice/ICE.md`, `personal/ice/ICE.md`; `_setup/TESTS.md`, `_setup/LINT.md`.
- Not yet: pipeline, any skill, `_setup/RECOVERY.md`.

## Standing notes
- Do not mount v2 or v3 in build sessions. Dev kit at `~/Dev/clc-plugins`.
- Rainbow Rig: run `rainbow-rig-shutdown.md` when online. Black Mac: retire v3 jobs when reachable (§13.5).
- Groq likely free tier; backfill drips ~6 h/day. Revisit dates: decisions-from-markers ~2026-11-01; first ICE monthly review 2026-11-02.
- Known: the Cowork mount blocks deletes unless permission is granted per session (granted once today); tests therefore work in temp copies.
