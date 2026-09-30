# Sancho build status

Read this first on any new session. Then continue from "Next step."

- **Current phase:** 4 (build). Phase 3 written 2026-09-30 (`migration-plan.md`); Phase 2 approved 2026-09-30.
- **Job file:** `_queue/jobs/2026-09-30_build-sancho.md` (stage `scaffold` done in Cowork; `mac-side` is next). Project: `work/copper-leaf/projects/build-sancho/`.
- **Last completed step (2026-09-30, Cowork):** **B0 scaffold.** Tree created per §3; `CLAUDE.md` (37 lines); templates T1–T8 in `_setup/templates/`; `_setup/sancho_lib.py`, `build-index.py`, `lint-layers.py`, `build-map.py`, `test-all.py`, `ping.sh`; `_setup/commands.md` (allowlist + registry); `FOCUS.md`; `personal/me/brief.md`, `watch.md`, `mantras.md`; business.md for six businesses + two brand files; seeds moved home (to-read ×2, goals ×7, work ICE ×7, personal ICE ×3, food and nomad projects); tests: 6 suites, all green; lint green; 66 generated files; `MAP.md` in three levels.
- 2026-09-30 later: `alaska-2027/` moved to `personal/projects/alaska-2027/` with a project.md (Gordon's say); frontmatter added to its 24 docs. Claude Code CLI installed on the silver Mac (v2.1.285, ~/.local/bin); shell wake phrases `hey sancho` / `sancho work` / `sancho nerd` in ~/.zshrc; **the mac-side build session was started by Gordon in Claude Code on 2026-09-30.** If two sessions are open (this Cowork one and that Claude Code one), the Claude Code session owns `_setup/` and `_queue/` until MAC-SETUP.md is done; Cowork stays read-only on those.
- **Next step:** **`mac-side` stage, in Claude Code on the Mac** (Cowork's shell can't do it). Instructions: `_setup/MAC-SETUP.md`. Then `pipeline` (port v3's code per §13.1; backward 7-day overlap; STATUS.md; Pushover). Then back in Cowork: the `open` skill, then `earballs-ingest`.
- **Gordon:** traveling in Italy through Oct 6; the Mac closes often. For the mac-side stage he needs to be at the Mac once (passphrase, Pushover signup, GitHub repo for Sancho-Private).

## Open for Gordon
- Pushover account (user key + app token) when convenient.
- Empty private GitHub repo for `~/Sancho-Private/` (like the kit: SSH only).

## What exists
- `_design/`: architecture (approved), decisions, postmortem, survey, migration-plan, routines-capture, rainbow-rig-shutdown, seeds (now moved; originals kept), reading copy + standalone, tree page.
- Tree: see `MAP.md` Level 0/1; `INDEX.md` everywhere; `work/PROJECTS.md`, `personal/PROJECTS.md`; `work/ice/ICE.md`, `personal/ice/ICE.md`; `_setup/TESTS.md`, `_setup/LINT.md`.
- Not yet: watcher, launchd schedules beyond the hourly autocommit, secrets, Sancho-Audio, Sancho-Private, pipeline, any skill.

## Standing notes
- Do not mount v2 or v3 in build sessions. Dev kit at `~/Dev/clc-plugins`.
- Rainbow Rig: run `rainbow-rig-shutdown.md` when online. Black Mac: retire v3 jobs when reachable (§13.5).
- Groq likely free tier; backfill drips ~6 h/day. Revisit dates: decisions-from-markers ~2026-11-01; first ICE monthly review 2026-11-02.
- Known: the Cowork mount blocks deletes unless permission is granted per session (granted once today); tests therefore work in temp copies.
