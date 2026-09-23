# Sancho build status

Read this first on any new session. Then continue from "Next step."

- **Current phase:** 2 (architecture), opened 2026-09-22. Phase 1 closed 2026-09-22 (Gordon reacted; no changes). Phase 0 closed 2026-09-21.
- **Phase 2 step 1:** host execution bridge decision (options presented to Gordon; awaiting his pick). Then work through the kickoff's 12 decisions plus the 13 items below, one at a time, writing each to decisions.md and `_design/architecture.md` as it lands.
- **Waiting on the Rig:** `_design/rainbow-rig-shutdown.md` has the PowerShell checklist; run it when Gordon says the Rig is online.
- **Last completed step:** 2026-09-22: v2 surveyed (four read-only subagents; main thread never read v2 content). survey.md is now complete: dev kit (1), 19 skills (2), maps (3, 3a), instruction files (4, 4a), pipeline (5, 5a), data (6, 6a), v3 vs v2 (7), self-diagnosis (8, 8a), buried treasure (9, 9a), smells (10).
- **Next step:** Gordon reacts to the Phase 1 readout. Then **Phase 2: architecture**. First decision to settle: the host execution bridge (survey 1, finding 5). Deliverable: `_design/architecture.md` per the kickoff's 12 decisions plus the items below.

## Resolved 2026-09-22
- v2 daemons were on the Rainbow Rig; Gordon retired it the evening of 09-21. Last v2 write 18:56 MDT 09-21; nothing since. v2 is inert.
- Ivy League: a full curriculum exists (`v2/personal/think-better.md`, 319 lines); the week-by-week plan was lost to a corrupt docx; no delivery mechanism was ever built. survey.md 6a has the detail. ICE item, personal lobe, likely high priority.
- Backlog has three eras (old / good period Mar–Jun 2026 / fresh); survey.md 5a. Boundary confirmed as March 2026. Real recordings start 2025-08-22 (the "2023" ones are Plaud demos with fake dates); survey.md 5a.
- **Rainbow Rig will come back online.** E: drive was swapped, so v2's scheduled tasks lose their scripts, but if Sync.com on that machine rebuilds `E:\Sync\...` the tasks could resume. Gordon to disable the Task Scheduler entries and sign Sync.com out on the Rig before or at first boot. Not verifiable from here.

## Mount situation
- v2 and v3 both mounted this session, read-only. v3's `CLAUDE.md` was injected on mount (firewall incident logged); Gordon advised to rename it in the Sync copy and delete its `.env`. v2's is already renamed; nothing injected.
- Do not mount v2 or v3 in Phase 2 sessions. Everything needed is in survey.md.
- Dev kit: `~/Dev/clc-plugins`, on GitHub as `CopperLeafCreative/clc-plugin-dev-kit`, tree clean.

## Items Phase 2 must cover beyond the kickoff's 12 decisions
1. Host execution bridge: which Sancho actions run on the Mac and how a Cowork session asks (queue folder + Mac-side watcher is the leading candidate).
2. Four-tier context model vs. index cascade (options in chat 2026-09-22; deferred).
3. SQLite stays as pipeline ledger (decided); design the generated Markdown status view.
4. Human-verified vs. machine-confidence as first-class fields on speakers and facts; corrections must flow back to the voiceprint library.
5. Pipeline health line at startup ("N waiting, oldest from <date>"), and no alert channel nobody reads.
6. Retirement line per component (v2.5 idea): how a skill/script/folder is turned off so it's actually off.
7. Single writer per file; no daemon writes into the knowledge tree.
8. Secrets never under `~/Sync/`.
9. Ownership field on every business (own / partial / client); people in one place with roles.
10. ICE lifecycle incl. a kill path; WIP limit of 3 enforced by a file.
11. Backfill plan: v2 holds 696 transcripts (2023-10 to 2026-04, speakers unresolved) and 291 raw `.ogg`; v3 holds 704 (2026-03 to 2026-09). Notes-to-self first, newest first.
12. Kit's GitHub-home follow-ups (Leah access, branch protection, plugin packaging); where the kit's job plan file lives.
13. Lobe placement of sensitive material (health, relationships) and what never loads at startup.

## Key decisions so far (full log in decisions.md)
All memory in local MD; SQLite is pipeline ledger only; plugin dev in Claude Code only; Astra sharing work-side only; tasks notice-and-hand-off; WIP limit 3; wake phrase "Hey Sancho" (personal default, "let's work"); 11 must-nevers; ICE; one machine (silver Mac); black Mac runs v3 pipeline until cutover; kit repo `clc-plugin-dev-kit`.

## Routine capture
`routines-capture.md`: Food; Nomad daily check (more components pending from Gordon).

## Resolved carry-forwards
Ivy League outline: never written; seed is v2 `personal/think-better.md`; ICE item. Plaud fetch: v3's `plaud-sync.py`, hourly launchd, bearer token by hand. Retrieval: v2's `memory-compiler.py` (frontmatter → JSON index + FTS5), borrow the idea. v2's self-account: survey 8a.
