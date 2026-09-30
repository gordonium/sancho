# Migration plan and build order (Phase 3)

Written 2026-09-30, the day the architecture was approved. Companion to `architecture.md`; cites it by section. Ordered batch list at the end.

## 1. The gate (nothing moves without passing it)

**Facts.** A fact enters the live tree only with a source atom (§5.1), a date, and a tier (§5.2). Anything from v2 or v3 without a traceable source goes to `_quarantine/<origin>/<path>.md` with its original text intact and a header saying where it came from; it is reviewed by Gordon one file at a time and either promoted (with `[v2:path date]` cites and, where he confirms, `[confirmed gordon date]`) or killed (moved to `_quarantine/_killed/`, never deleted). Quarantine is a forcing function, not a parking lot: the weekly work review shows its count, and a batch isn't closed while its quarantine is non-empty.

**Skills.** Reviewed one at a time: read the old SKILL.md as text (the copies in `_reference/old-skills/`), keep the idea, rewrite to Sancho's header and rules (§9.1: self-sufficient, no external guidance files, no v2 paths, no Mouth/Nerd, no Wrike/ntfy, scoped triggers with `must_not_trigger`, a write step, a test). Gordon has the final say on each; his say is one word per skill at review.

**Transcripts and voiceprints.** Raw audio migrates by script (v2's `earballs-inbox/*.ogg` plus everything Plaud still holds, which is everything); derived transcripts are **re-derived** by Sancho's pipeline under the new templates, never copied forward. v3's voiceprint library is not imported as embeddings; human-confirmed (recording, cluster, person) records are re-created as ingest confirms speakers, and the library is rebuilt from those (§10.2). v3's 626 enrollment lines are evidence for which recordings to confirm first.

**Verification per batch (kickoff Phase 4):** (a) indexes and map regenerate cleanly with the new files on them; (b) Gordon spot-checks five random migrated facts against their cited source; (c) any skill touched in the batch passes its automatic tests. A batch that fails any of the three is fixed before the next starts.

## 2. What migrates, from where, in what order

| Batch | Source | Destination | Gate notes |
|---|---|---|---|
| **B0 Scaffold** | nothing migrates | the tree, templates, lint, indexes, map, queue, commands, CLAUDE.md, brief/watch/mantras skeletons, seeds moved to their homes | WIP-3 exempt (decision 09-24) |
| **B1 Pipeline** | Plaud cloud (all history), v2 `earballs-inbox/*.ogg` | `Sancho-Audio/`, ledger, `recordings/` | fresh first; backlog eras drip (§13.2) |
| **B2 Clients (WoA)** | v2 `work/clients/*` (34 entities), v3 `work/clients/` (3), v2 `work/dashboard.md` for stake and lead | `work/wizard-of-ads/clients/<slug>/` entity folders | the 13 live clients first; dormant ones as `status: former` with one file; every `key_facts` line becomes a cited line or quarantine |
| **B3 Businesses** | v2 `work/copper-leaf-creative.md`, `press-managed.md`, `dpc-venture.md`, `entomat-*.md`; v3 `work/tipelodeon/` (best-kept file in either system) | `work/<business>/business.md`, `brands/`, `stakeholders/` | Tipelodeon's `v2_pointers` and CONFIRMED flags map straight onto tiers |
| **B4 Copper Leaf registry** | handoff doc, kit `README`, each plugin repo's `CLAUDE.md`, v2 `work/wp-dev-kb.md` (pointer only) | `work/copper-leaf/plugins/<plugin>.md`, `_registry.md` generated | kit's `CLAUDE.md` stays source of truth for dev rules |
| **B5 People** | v2 `relationships/people/` (101, minus ~13 junk extractor files), v3 `memory/people/` (35), v3 `_dmz/v2-imports/` (36 raw), Google Contacts export | `people/<slug>.md` on T4 | contacts import + de-dupe is its own project; person facts cited or quarantined; junk files killed outright |
| **B6 WoA partners** | v2 `work/partners/` (18) | `people/<slug>.md` with `woa:` block; `wizard-of-ads/partners/<slug>/` only where relationship material exists | bench view generated |
| **B7 Personal** | v2 `personal/*` (44), `home/`, `health/`, `travel/`; v3 `memory/scratch/` (43, incl. 43 MB of audio chunks → `Sancho-Audio/`), v3 `work/projects/gordon-leah-relationship/` (120 files → `personal/`) | `personal/<area>/`, `personal/me/`, `personal/projects/` | Gordon reviews these himself; Sancho files, he approves; mantras and principles via the mantras seed |
| **B8 Work docs and playbooks** | v2 `work/playbooks/`, `reference/`, `specs/`, `handoffs/`, `strategy/`, `builds/` (the self-diagnosis docs go to `_design/archive/` as history) | the matching business or client `docs/`; system history to `_design/archive/` | untouched content is fine as `type: doc` with a `[v2:path]` cite |
| **B9 Backlog ingest** | Sancho's re-derived transcripts | client `summaries/`, people, knowledge | notes-to-self first, newest first (decision 09-22); then eras 3 → 2 → 1 |

Clients before people before personal, per the kickoff. B0 and B1 are not migrations; they're the build that the migrations need.

## 3. Skill build order (the kickoff's list, updated with everything decided since)

Rules: one thing at a time inside "Build Sancho" (WIP-3 applies within it: at most three components maturing at once, scaffold exempt); every component ships with its header, its automatic test, and a place on the map, or it isn't done; the personal routines come early because habit is the point.

| # | Component | Kind | Depends on | Notes |
|---|---|---|---|---|
| 0 | **Scaffold** (B0): tree, templates, `lint-layers.py`, `build-index.py`, `build-map.py`, `commands.md`, watcher, `notify.py`, `unlock`, CLAUDE.md, brief/watch/mantras skeletons, FOCUS.md, Build-Sancho job file, `~/Sancho-Private/` repo, autocommit fix (§11) | scripts + files | nothing | Cowork can write all files and test the pure-Python scripts in its sandbox; watcher, launchd, secrets and the Private repo need Claude Code on the Mac |
| 1 | **earballs pipeline** (`_setup/pipeline/`): Plaud fetch 5-min incremental, download, Groq transcription, diarization with count priors, voiceprint match with the three states, transcript + `speakers.md` + `meta.md`, `STATUS.md`, watchdog, Pushover, ledger backup, ICS calendar poll, backfill drip | scripts | 0; Claude Code on the Mac; Groq/HF/Plaud/Pushover secrets | ported from v3's code per §13.1; starts with the backward 7-day overlap; Zoom poll (§13.6) as 1b once the Zoom app exists |
| 2 | **open / startup** (§8): temporal check, morning packet, greeting voice, lease, session note, close | skill | 0 | the first skill, because every other skill runs inside a conversation it opens |
| 3 | **earballs-ingest** (rewrite): speaker confirmation, seven GTD buckets, filing per §3.5, supersession, receipts; proposes ICE entries, never writes them | skill | 1, 2 | keeper #1 in the kickoff |
| 4 | **write-it-down** (reflex) + **attribution-correction** (five steps incl. library rebuild and re-match window) | skills | 3 | keepers #2 and #4; small |
| 5 | **Personal morning routine** incl. the nomad daily check (routine 2, all components, road-test) and the daily focus checksum | skill + commands (weather, routing) | 2; weather/routing keys | new design; habit target |
| 6 | **Food routine** (routine 1): Sunday session, pantry, cooking-for-one journal | skill | 2 | new design |
| 7 | **Weekly Review** (both gears, both lobes) + the monthly/quarterly ICE reviews + Waiting-For and stall flags | skill | 2, FOCUS, PROJECTS.md | the GTD hinge |
| 8 | **think-first** (front of chains) → **brief-me** (source manifest, completeness gaps) → **fact-check-anyone** (new) → **critical-thinking** → **punnett-square** → **triz** | personal skills | 2 | keepers, one at a time, no Astra constraints |
| 9 | **Work morning routine** | skill | 2, 7 | fresh design, not a port |
| 10 | **Zoom transcript filing** (build item 13) and the **Zoom poll** | skill + command | 1 | VTT names as voiceprint ground truth |
| 11 | **Contacts import + de-dupe** (Google Takeout CSV → people files, merges proposed) | command + skill | 0, B5 | its own project; WIP slot |
| 12 | **Map HTML render**, **Rig as second runner**, **hosted diarizer trial**, **read-only Wrike/Google Tasks**, the four work capability seeds | ICE | reviews | not scheduled |

The **recurring-project shape** (needed by "Claude best"): a project file with `recurring: monthly|quarterly` and no `done` state; its job file has one repeating stage; the review treats its next action like any other; it never counts against focus unless it's in focus. Added to the project template at scaffold.

## 4. Seeds → homes at scaffold
`seeds/to-read.md` → `personal/learning/to-read.md` and `work/to-read.md` (split by lobe). `seeds/goals.md` → `personal/goals.md`, with a pointer from each business's `goals.md`. `seeds/work-ice.md` → four files in `work/ice/`. `seeds/mantras.md` → `personal/me/mantras.md` (structure) plus a capture session for content. `routines-capture.md` → `personal/projects/food-routine/` and `personal/projects/nomad-routine/` project files with their job files. `postmortem.md`, `survey.md`, this plan, and `architecture.md` → stay in `_design/` (archived after Phase 4).

## 5. Phase 4 first steps, in order
1. Scaffold the tree and the pure-Python scripts from Cowork; test lint, index and map builders against the fixture tree in the sandbox.
2. In Claude Code on the Mac: create `~/Sync/Sancho-Audio/`, `~/Sync/Sancho-Secrets/` (age), `~/Sancho-Private/` (repo), install the watcher and its launchd job, fix the autocommit, run the `ping` command end to end.
3. In Claude Code: port the pipeline (§13.1), first sync with the backward overlap, first `STATUS.md`, first Pushover test.
4. Back in Cowork: the open/startup skill, then ingest; first real ingest on the newest recording; first spot-check.
5. Batch B2 begins.
