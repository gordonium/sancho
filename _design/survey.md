# Phase 1 survey

Started 2026-09-22. Sections are filled as their sources become available. Status of each section is in the heading.

Sources and their trust level:
- **Handoff doc** (`~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md`, written 2026-09-21): fresh, safe, read in the main thread. Disk checked against it 2026-09-22; matches.
- **Old-skill copies** (`~/Sync/Sancho/_reference/old-skills/`): v2 material, evidence only, read by subagents.
- **v2 tree**: not mounted yet (Gordon's call; separate session).
- **v3 tree** (`~/Reference/jarvis-v3/`): downloading as of 2026-09-22; not surveyed yet.

---

## 1. Copper Leaf dev-kit inventory (DONE, from the handoff doc)

### What the kit is

A git repo at `~/Dev/clc-plugins/` (branch `main`, **no remote yet, on purpose**) that is also the parent folder for Copper Leaf plugin clones. It holds a rules file (`CLAUDE.md`, auto-loaded by Claude Code for any plugin cloned beneath it), three Claude Code skills, two hooks, one scheduled job, example configs, and the handoff doc. It contains no secrets. Four plugin clones sit beside it today (filmadelphia festival calendar, wa-learndash-customizations, wizard-academy-deux, phillyfilm), ignored by the kit's whitelist `.gitignore`.

**Path constraint:** the folder must stay at `~/Dev/clc-plugins/` with the kit files at its top level. Four things depend on that exact path: the two hooks in `~/.claude/settings.json`, the LaunchAgent, the `~/.claude/skills/plugin-*` symlinks, and CLAUDE.md auto-loading for the plugin clones. Sancho does not move it.

### The three skills (Claude Code skills, live in the kit, symlinked into `~/.claude/skills/`)

| Skill | Does | Gate out |
|---|---|---|
| plugin-edit | Asks plugin + staging URL + task every time; preflights the repo (SSH, clean tree, branch, `.gitattributes`, version agreement across header / release-notes / tag); connects to staging over SSH; investigates (incl. cross-plugin spans); numbered plan → human approval → plan saved to memory; implements under the Readability Rule; rsync to staging (dry run first, no `--delete`); tests from a written matrix, browser + server evidence; restores test content. | Every staging test passes |
| plugin-review | Three parallel read-only subagents (backward compat, security, performance), same report format, verdict PASS / PASS WITH NOTES / FAIL. ~3 min, ~210k subagent tokens. FAIL → fix, redeploy, retest, rerun all three. Pre-existing issues become follow-ups, never fixed in-change. | No open FAIL; staging tests pass after last change |
| plugin-ship | Semver bump (collision-aware); release-notes entry; redeploy; **parity proof** (checksum dry-run rsync lists nothing); `git pull --ff-only`, stage by name, housekeeping commit then feature commit, tag `vX.Y.Z`, push branch then tag; hand Gordon paste-ready release text; time estimate paragraph; cleanup (delete job plan from memory, refresh plugin CLAUDE.md, add lesson if any). **Claude never creates or publishes the Release.** | Gordon publishes the Release; that is the production deploy |

### Hooks and jobs (mechanical, not remembered)

| Mechanism | Where | What |
|---|---|---|
| Live-site guard | PreToolUse hook on `Bash`, global in `~/.claude/settings.json`, runs `bin/sitedistrict-live-site-guard.py` | Default-block on any ssh/rsync/scp/sftp aimed at a SiteDistrict host unless every path is a plain `~/sites/<folder-containing-sitedistrict.com>/...`. Text-based: also blocks local commands whose text contains an alias plus `sites/`. Cannot see inside a script uploaded and run remotely. Only exists where installed (not Leah's machine). Load-bearing: a staging key opens the whole host, live sites included. |
| Guard self-test | PostToolUse hook on `Write\|Edit` | If the edited path contains `sitedistrict-live-site-guard`, runs the 37 tests; failure blocks. |
| Hourly WIP backup | LaunchAgent `com.copperleaf.wip-backup`, `bin/wip-backup.sh` | Snapshots every repo under `~/Dev/clc-plugins/` (incl. untracked) to `refs/heads/wip/<machine>/<branch>` on origin, via a temp index; never touches working tree, real index, master, or tags. Skips repos with no origin (so the kit itself isn't backed up until it gets a remote). |
| Release gate | SSH-only git, no `gh`, no token on the machine | Nothing on the Mac can publish a Release. |
| Line endings | `.gitattributes` `* text=auto eol=lf` per repo | Added as housekeeping on first pass through plugin-edit. |

### Human gates (complete list, from section 5.4)

Staging URL/plugin/task (never assumed); `ssh-copy-id` and adding keys (Gordon); plan approval; business decisions inside the plan; logging in to staging wp-admin in Chrome; "ship it"; **publishing the GitHub Release (Gordon only)**; production smoke test. Claude never types credentials, never touches production.

### Registry-shaped facts the kit says an orchestrator should keep (section 14.2)

Per plugin: name → repo URL (org `CopperLeafCreative` vs user `copperleaf`; five `chancelight-*` under `copperleaf/`, one under `ChanceLight/`) → main file → prefix → version locations → related plugins → test commands.
Per staging site: URL → host (`host-N.sitedistrict.com`) → SSH alias → site folder → WordPress root (`www/`) → whether WP-CLI can load WordPress on that host (host-2: no, PHP 7.3 shell) → whether PHP error logging is verified (the `/tmp/clc-wp-debug.log` fix; can be overwritten, reverify per job).
Known aliases today: `copperleaf-dev`, `filmadelphia-dev` (host-5), `artspeak-staging`, `wizardacademy-dev` (host-2), `govartshow-dev` (host-12).
Still confirm the staging URL with the human per job; sites get re-cloned and renamed.

### Standing conventions Sancho inherits (Gordon's, apply beyond the kit)

Hooks over prose; no `gh` ever; plain language, define jargon, lead with the conclusion; no em dashes in rendered copy; a job is a state machine on disk; job plan created on approval and deleted on ship, stable knowledge stays. The **Readability Rule is WordPress-only**.

### Orchestrate vs. leave alone

| Sancho orchestrates | Sancho leaves entirely alone |
|---|---|
| The registry (plugin → repo → main file → prefix → staging → alias → quirks), first entry of type "tooling" = the kit itself | The guard's rules and default-block stance |
| Knowing when to call plugin-edit / plugin-review / plugin-ship and where the human gates are | The human gates themselves (Release, credentials, production) |
| Optionally: tracking a plugin job's state across the 16 stages in section 14.1 (open question 17.6: Gordon may prefer "launch the skills and stay out of the way") | SSH-only git, no `gh` |
| Carrying the time estimate into whatever reporting exists | Clones outside the Sync folder; the `~/Dev/clc-plugins` path |
| Where lessons get written (kit rules file vs. Sancho; one must be source of truth) | The plan-then-approval rule inside plugin repos; the Readability Rule |
| Helping Gordon give the kit a GitHub home (section 17) | Publishing anything |

### Open items the handoff hands to Sancho (section 13 and 17)

1. **Kit's GitHub home** (17.3): standalone repo vs. Sancho monorepo (handoff recommends standalone, referenced by Sancho); owner (`CopperLeafCreative` org recommended); name (`clc-plugin-dev-kit` suggested); private; access for Leah; branch protection for `main` but not `wip/*`; `main` vs `master` consistency; how Leah receives it (a Claude Code plugin bundling skills + hooks, like Astra); which copy of the WordPress rules is source of truth (kit recommended, v2 keeps a pointer); registry entry. **Gordon creates the empty repo himself; Claude never drives GitHub's site or installs `gh`.** These are Phase 2 conversation items, logged in the architecture's open questions.
2. Leah's Windows machine has no guard, no backup, no skills. Porting needs Python 3 path, Task Scheduler, ssh config pattern, clones outside Sync. Plain-language explanations for her.
3. Skills untested beyond the one pilot job. Trigger descriptions not optimised.
4. Per-plugin `CLAUDE.md` coverage thin (~50 plugins, most have none).
5. Tag hygiene audit across repos (header vs tag vs Release) would be valuable; v2 notes plugin versions are audited against MainWP across ~80 sites.
6. Follow-up code issues noted in reviews, left alone on purpose (listed in handoff 13).
7. SiteDistrict support request: **dropped by Gordon, do not re-propose.** Chrome (not the built-in browser) on staging is the standing method.

### Things worth borrowing into Sancho's own design (on purpose, and why)

- **Hook-enforced invariants with a hook-run test suite** (6.1 + 6.2): the exact pattern for Sancho's must-nevers (no data loss, no silent overwrite, single writer). Phase 2 must say which hook types fire in Cowork vs. Claude Code only.
- **State machine on disk for a job** (14.1) → Sancho's skill-chain pattern (decision #7) and ICE lifecycle.
- **Memory with a lifecycle** (11): job plan created on approval, deleted on ship → Sancho's ephemeral vs. durable provenance (decision #2).
- **Whitelist `.gitignore`** (17.1): tracks only named things; Sancho's repo is knowledge-only and could use the same stance instead of blocklisting media.
- **"Where this document and the files disagree, the files win; tell Gordon"**: adopt as a standing rule for every Sancho doc.
- **Section 15, "things Claude got wrong"**: keep this as a section in Sancho's own docs. It's the cheapest form of test.

### Findings for Phase 2 that the handoff does not state (main-thread observations, 2026-09-22)

1. **The live-site guard almost certainly does not fire in Cowork.** It is a Claude Code `PreToolUse` hook matched on `Bash|mcp__terminal__run_in_terminal`. Cowork's shell tool is `mcp__workspace__bash`, a different name, and Cowork sessions do not read `~/.claude/settings.json` hooks the same way. So the guard protects Claude Code sessions only. Consequence: **plugin work stays in Claude Code**; a Cowork session (including Sancho sessions) must never hold or use a staging SSH alias. Phase 2's "which hooks fire where" section must lead with this. Verify by test before relying on it either way.
2. **Mounting the kit loads its CLAUDE.md into the session.** Observed today: connecting `~/Dev/clc-plugins` pulled the WordPress rules file into this session's instructions. Harmless here (read-only phase, and they're Gordon's own rules) but it shows that any folder Sancho mounts can inject instructions. Design rule: Sancho sessions mount the kit only when orchestrating a plugin job, and never mount v2.
3. **Two memory layers will exist.** The kit uses Claude Code's file memory (`MEMORY.md`, job plan created on approval, deleted on ship). Sancho will have its own tree. Decision needed in Phase 2: job plans live in Claude Code memory (kit stays self-contained) or in Sancho's registry (Sancho can see job state). The handoff's 17.6 question ("track jobs, or launch and stay out of the way") is the same decision.
4. **The kit itself has no backup until it has a remote.** The hourly job skips repos without `origin`. Section 17's GitHub-home decision is therefore not cosmetic; until it's made, the kit is one disk failure from gone (Time Machine aside).

5. **Cowork's shell is not the Mac.** Observed 2026-09-22: this session's shell runs in an isolated Linux sandbox that sees mounted folders but has no `~/.ssh`, no Mac keychain, no launchd, and no Mac-installed tools. So from a Cowork session, Claude cannot `git push`, cannot run a script that needs an API key stored on the Mac, and cannot talk to the Plaud cloud with Gordon's credentials. This touches three kickoff decisions at once: **#9** (git automation: the launchd autocommit in `_setup/` works because it runs on the Mac, not in the session), **#11** (the pipeline "runs directly in the session": only true if the session is Claude Code, or if a Mac-side runner does the work), and **#12** (map regeneration). Phase 2 needs a **host execution bridge** decision: which Sancho actions run where. Candidates: (a) Sancho's Mac-side jobs run under launchd on a schedule and the session only reads results; (b) a queue folder inside `~/Sync/Sancho` that a Mac-side watcher executes (session writes a request file, watcher runs it, writes a result file; mechanical, auditable, no secrets in the session); (c) anything needing keys or push happens in Claude Code sessions only. Gordon's stated requirement: he does not want to be involved in every git push.

### Contamination note

The handoff mentions v2 (GordonOS) in three places: its path, that it was mined once by a read-only subagent for WordPress rules, and that `tools/` holds secrets. Nothing from v2 was quoted into this section.

---

## 2. Skill inventory (DONE 2026-09-22, three read-only subagents over `_reference/old-skills/`; main thread saw reports only)

19 skills, ~2,400 lines total. Verdicts below start from the kickoff's decisions (eight keepers, rest kill-by-default) and add the reason the evidence gives. Where the evidence argues for something different, it says so.

### 2.1 One row per skill

| Skill | Lines | What it actually does | Triggers | Reads | Writes | Depends on | Overlaps | Verdict | Reason |
|---|---|---|---|---|---|---|---|---|---|
| **earballs-ingest** | 319 | Post-transcription ingest only. Reads a finished transcript plus `processing_log.json`, infers speakers (calendar, weekday and vocabulary heuristics, cosine scores), runs a 10-pass extraction, files facts by content type with source tags. Assumes download/transcribe/diarize already done by "Nerd". | "process recordings", "ingest earballs", startup detecting unprocessed transcripts, ntfy signal | processing_log.json, _plaud_metadata.json, transcript.md, speaker-profiles.md, recurring-meetings.md, people/, gcal | processing_log.json, speaker-profiles.md, pattern-tracker.md, earballs-ingest-progress.md, action-items.md, health.md, mood-data/, mantras, principles, client and people files, nerd-inbox/ | Nerd pipeline, plaud-sync.py, `earballs tag/compare` CLI, voiceprints/, memory-db.py, ntfy, Wrike, gcal MCP | write-it-down, attribution-correction | **REWRITE** (keeper) | The extraction passes are the good idea. Everything else must change: no confirmed-vs-guessed marker on filed names; passes 6–9 file person-attributed inferences without confirmation; two unreconciled done-states and no backlog counter; personal/work routing is a time-of-day heuristic; health-sensitive facts filed directly. The 10-pass loop and threshold parsing are prose-as-code. |
| **write-it-down** | 76 | Behavioural rule: any state-changing input is written to disk before replying. Maps answer type to target file. | Any answer, decision, correction, fact ("trigger on everything") | Nothing | action-items.md, completed-items.md, ticklers, session-state.md, "the appropriate file" | task-ops.py | earballs-ingest, attribution-correction | **REWRITE** (keeper) | Right motive (compaction, crashes), wrong mechanism. No append-vs-replace rule, so it is a silent-overwrite engine. No provenance. No lookup rule for which file. Becomes the backstop; structure does the default writing. |
| **attribution-correction** | 92 | On a speaker/ownership correction, re-reads the transcript, finds every related error, presents all with confidence, fixes all filed locations, appends an event to processing_log.json. | "wrong speaker", "that's not me", "flip that", vague "wrong" | earballs-transcripts/, ingest-drafts/, transcript | ingest-drafts/, action-items.md, people/, clients/, home/, processing_log.json | earballs-ingest outputs | earballs-ingest Pass 5 | **REWRITE** (keeper) | Best-designed of the three: present-all-before-fixing, propagate everywhere, keep a note of the old value. Fatal gap: **never touches the voiceprint or speaker profile, so the same misidentification recurs.** Propagation relies on grep, no index. |
| **think-first** | 176 | Two modes. Doing: restate, apply frameworks from a 15-row table, ask 2–5 questions, refined prompt, approval, execute. Thinking: name the question, frameworks, hard questions, user drives. | Any request involving build/decide/plan/change; explicit escape hatches | Nothing | Nothing (conversation only) | triz, critical-thinking (ticklers), post-build-sweep, standing-rules.md | critical-thinking (duplicated frameworks), triz (circular) | **REWRITE** (keeper) | ~85% portable. Strip names, "what this replaces," post-build-sweep. Scope the trigger: "err toward looping" on any request is the Q2 failure. Break the think-first ↔ triz circular call. Refined prompt is never persisted. |
| **critical-thinking** | 199 | Name topic, walk 7 dimensions (Who/What/When/Where/Why/How/Self) with 3–5 questions each, synthesize four items, hand back. | "critical thinking", "deep dive"; think-first tickler | (PNG cited as provenance only) | Nothing | think-first, triz | think-first, punnett-square | **REWRITE** (keeper) | ~80% portable. The SELF dimension is Gordon's health and a named partner; make it a per-user block so Astra can share the file. Not trigger-on-everything; good. |
| **triz** | 139 | Name contradiction, pick 2–3 principle groups from a 7-row tension table, 5–8 principles as lenses, one idea each, evaluate via think-first. | "triz", "contradiction", "I want both" | Nothing | Nothing | think-first (gate and evaluation) | think-first | **REWRITE** (keeper) | ~95% portable, nearly generic already. Strip names, example domains, Source section. Break the circular call to think-first (inline the evaluation step). |
| **punnett-square** | 141 | Identify meeting from calendar, brief-me each attendee, 2×2 (your best/worst, theirs), overlap and tension, three-line walking-in posture. Draft first, then confirm. | "prep me for the meeting", "Punnett Square"; auto-suggested by morning-startup and work-closeout | Calendar, brief-me output, people files | Aspirational only ("future debrief skill") | brief-me, calendar, web search | brief-me, critical-thinking WHO | **REWRITE** (keeper) | ~65% portable. Origin story appears three times; strip to one line. Remove routine hooks. The "was the read accurate?" debrief needs stored predictions, which nothing stores; decide whether to build that or drop the claim. |
| **brief-me** | 185 | Classify subject (person/company/topic), exhaustive fixed-order local search over 11 hardcoded paths, optional web, typed briefing template with stale-flagging (>30 days). | "brief me", "who is", "catch me up on" | 11 paths incl. memory-db.py, transcripts/, session-state.md, web | None (offers a people-file update) | memory-db.py, punnett-square, morning-startup | punnett-square, morning-startup step 14 | **REWRITE** (keeper) | ~50% portable. Layer 1 is a search script written as prose. Becomes a per-user source manifest plus the Phase 2 search path (decision #4). Presentation rules (lead with what matters, flag stale, be honest about gaps) are the keeper idea. |
| session-startup | 143 | 17-step cold boot: mesh health, read state, triage inbox/tickler/dashboard/calendar, meeting briefs, briefing. | "hey jarvis", any Jarvis mention, CLAUDE.md load, workspace mount, first of day | ~15 files, 3 mesh URLs, ntfy, calendar | session-state.md, mesh signal | Mesh, ntfy, Wrike, file server, 4 routine files, earballs-ingest | morning-startup (declared superseded, still present) | **KILL** | Superseded by morning-startup but never removed; same triggers. Infrastructure in prose. Hardcoded topology. |
| morning-startup | 192 | session-startup plus pipeline SLA check, ingest trigger, personal checklist, "Think Better" nag, day-of-week cadence dispatch to five other skills. 20 steps, 6 phases. | Same plus any morning greeting; "if you recognize the identity at all" | Everything above plus pipeline-health.json, signals-*.jsonl, morning-routine.md | session-state.md, morning-routine responses, signals | Mesh, ntfy, Wrike, watchdog script, 6 other skills | session-startup, whats-next, all cadence skills | **KILL** (mine ideas only) | This is the ritual Gordon stopped using (Q2). A Friday-that-is-last-Friday morning could chain four skills. Two sources of truth for the checklist. Unbounded "ask every morning until habit" loop with no state. Salvage: the pipeline-health one-liner idea and the "threads closed last night" handoff idea. |
| work-closeout | 131 | End of work day: open-loop scan, file floating items, tomorrow preview, dispatch Nerd, write state. Blocks until Nerd confirms. | "wrapping up", "done for the day", ~4–5pm | Conversation, mesh, signals, calendar | session-state.md, action-items, inbox, ticklers, people, clients, dashboard, nerd-inbox | Mesh, Wrike, write-it-down, punnett-square | evening-closeout, evening-winddown (shared trigger phrases) | **KILL** | Task-specific nags (T058, T124) baked into procedure. Blocking wait on another machine. Reconsider only after decision #6/#7; the "file floating items before ending" idea survives as a write-discipline default, not a ritual. |
| evening-closeout | 81 | Bedtime: brain dump, save state, file unfiled, one mantra, one reflection, signal commit. | "goodnight", "calling it", 2h+ session, 1h idle | Conversation, mantras.md | session-state.md, inbox.md, ticklers | Mesh | evening-winddown (declared superseded) | **KILL** | Superseded and still present. Idle timers the chat can't measure. Mantra rotation with no record of last used. |
| evening-winddown | 148 | evening-closeout plus thread-by-thread handoff requiring acknowledgment, breathwork, "threads closed tonight" list for morning. | Same phrases | Conversation, mantras.md, morning-routine.md | session-state.md, action-items.md, ticklers | Mesh; morning-startup consumes output | evening-closeout, work-closeout | **KILL** (mine ideas) | Blocking "wait for acknowledgment" is unimplementable. Files unfiled items to a different file than evening-closeout does. Salvage: a closed-threads list as a write-discipline artefact. |
| weekly-work-review | 85 | Friday 8-item review: shipped, due, client check-ins, stalled, Wrike cross-check, one priority, weekend Nerd handoff. | Friday via morning-startup; manual | routines/weekly-work-review.md, Wrike, calendar, clients/ | dashboard.md, action-items.md, nerd-inbox | Wrike, Nerd, morning-startup | monthly-business-review | **KILL** (reconsider) | Duplicates its own routine file inline. Timing contradicts the startup skills (Mon+Fri vs Fri). Wrike-dependent. A work review may return as a skill after #6/#7, designed fresh. |
| monthly-business-review | 93 | Last-Friday strategic review: revenue, roster, bets, partners, tools, ventures. | Last Friday after weekly; manual | routine file, dashboard, clients/, partners/, named venture files | dashboard, action-items, its own routine file (next date) | weekly-work-review, think-first | weekly-work-review | **KILL** (reconsider) | Hardcodes venture names and people into procedure. Admits it may be stale vs. its routine file, then restates it anyway. Timing contradicts startup skills (first Monday). |
| saturday-personal | 92 | System audit (8 items) then personal-projects walk, pick one. | Saturday via morning-startup | routine file, open-questions.md, live prices (TSLA/BTC/DOGE), calendar | Nothing | morning-startup | monthly-personal-review | **KILL** | No writes; findings live in conversation. Stock tickers and an "Opus version check" in a personal routine. |
| sunday-routine | 45 | Read routine file, present 3-item checklist, record responses. | Sunday via morning-startup | routines/sunday-routine.md | "if needed" | morning-startup | saturday-personal | **KILL** (idea survives) | Cleanest of the set, but its real content was the meal-planning line, which is now routine #1 in `routines-capture.md`. |
| monthly-personal-review | 83 | First-Saturday life review: health, mind, relationships, aspirations. | First Saturday after saturday-personal | routine file; spreadsheets with no path | Nothing | saturday-personal | saturday-personal | **KILL** | 13 named people and health/substance tracking embedded in a procedure file. No writes. Sensitive content in the wrong layer. |
| whats-next | 113 | 30-second priority scan by instance role, auto-executes "mechanical" items, outputs count plus top 3. | "what's next"; proactively after any task, lull, idle, transition | Mesh, inboxes, ticklers, calendar, action-items, pipeline, Plaud | Moves dispatches, runs pipeline jobs and Plaud sync | Mesh, Wrike, earballs, Plaud, morning-startup | session-startup, morning-startup | **KILL** (idea survives) | Fires at every lull, so the assistant is always in a ritual. Grants itself permission to run jobs and move files. Contradicts itself on commits. Salvage: the output format (count + top 3) and "be honest about what you can't check." |

### 2.2 Overlap clusters

- **Startup family** (session-startup, morning-startup, whats-next): three entry points claiming the first interaction of the day, exclusivity enforced by prose only.
- **Closeout family** (work-closeout, evening-closeout, evening-winddown): three skills share "done for the day" and "wrapping up"; two are declared superseded and still present; they file unfiled items to different targets.
- **Work review family** (weekly, monthly-business): stacked, timing contradicts the startup skills.
- **Personal review family** (saturday, monthly-personal, sunday): stacked on Saturday; no writes anywhere.
- **Thinking family** (think-first, critical-thinking, triz, punnett-square, brief-me): the good cluster. Framework questions duplicated between think-first and critical-thinking; think-first ↔ triz is circular; "meeting prep" is claimed by three entry points.
- **Memory family** (earballs-ingest, write-it-down, attribution-correction): write-it-down says write before discussing; ingest and correction say present before filing. A correction mid-triage triggers both.

### 2.3 Contradictions found (evidence for the "rules that contradicted each other" post-mortem line)

Monthly review timing (first Monday vs last Friday); weekly review day (Mon+Fri vs Fri); signals file name (signals.json vs signals-*.jsonl); unfiled-item destination (inbox.md vs action-items.md); whats-next on commits ("never offer" vs "always ask"); trigger-phrase ownership across three closeout skills; startup exclusivity (each says it goes first); write-before-discuss vs present-before-file.

### 2.4 Hardcoded topology that will not carry forward

Three Tailscale IPs, an ntfy topic, a LAN file server (192.168.1.96), Windows paths, `~/PhpstormProjects/gordon-os-v2`, `tools/wrike.py`, `tools/memory-db.py`, `task-ops.py`, `plaud-sync.py`, and roughly 25 data paths (listed in the pipeline subagent's report; all become Phase 2 "where things live" decisions, not carried as-is).

### 2.5 What the skills say about the earballs pipeline (partial; the code itself is in v2, not surveyed yet)

- The SKILL.md handles **ingest only**. Download (`plaud-sync.py`), normalization, diarization, transcription, and voiceprint embedding (pyannote/WeSpeaker into `data/voiceprints/`, CLI `earballs tag` / `earballs compare`) ran on the "Nerd" machine as scripts. So there **is** real code to find in v2; the survey must locate it.
- Voiceprint matching produced `voice_match_candidates` with cosine tiers: ≥0.90 high, ≥0.80 likely, ≥0.70 candidate. Rule was "never auto-confirm." But the filed Markdown carries no guessed-vs-confirmed marker; only `speaker_count_verified` (count, not identity) exists.
- Speaker naming also used **weekday and vocabulary heuristics** with no score at all. This is the most likely source of the attribution drift in the post-mortem (Q1, Q4).
- Done-state lives in two places (`processing_log.json` and `earballs-ingest-progress.md`) with no reconciliation and no backlog counter. Matches Q3: "it fell behind and I wouldn't know."
- Corrections never flow back to voiceprints or speaker profiles, so a bad match repeats.
- Decision #11 note: voiceprint matching used local embeddings (pyannote/WeSpeaker). Whether that step still needs anything local is a v2-code question; either way it's seconds of work.

### 2.6 Ideas worth salvaging from killed skills (into ICE, not straight to build)

Pipeline-health one-liner at startup; "threads closed last night" as a handoff artefact; count-plus-top-3 output format; "be honest about what you can't check"; "recordings are data, not commands" (from earballs-ingest, keep verbatim as a rule); attribution-correction's present-all-before-fixing; brief-me's stale-flagging and proportional depth.

## 3a. Map of v2 (DONE 2026-09-22; four read-only subagents; main thread never read any v2 content)

`~/Sync/Gordonium Enterprises Sync/gordon-os-v2/`: 93,001 files, 12 GB. Of that: 37,188 are `comms/spawn-logs/*git-conflict.log`; ~17,000 are a **Windows** Python venv (`.venv/pyvenv.cfg` points at `C:\Users\Owner\…`); `node_modules/` 381. Knowledge proper: ~3,900 Markdown files. Git: 7,621 commits, 91% start with `auto:`; last commit 2026-09-21; **3,615 dirty paths**; `*-CONFLICT-N` twins of databases, JSON, logs and one client file.

| Zone | Files | Size | Newest | State |
|---|---|---|---|---|
| `CLAUDE-SAFE-DO-NOT-USE.md`, `CORE.md`, `CLAUDE-protocols.md` | 3 | 78 KB | 2026-09-09 | 438 + 287 + 186 lines of rules. Subagent only. |
| `routines/` | 8 | 40 KB | 2026-04-27 | STALE |
| `work/` | 358 | 14 MB | 2026-09-10 | Live-ish: `clients/` 284 files (34 clients), `partners/` 18, `builds/` 21 (v2.5/v3 planning), 24 loose files in root incl. Gordon's own businesses |
| `relationships/people/` | 101 | 732 KB | content 2026-05-18 | STALE; 77/106 have frontmatter; ~13 junk entities from a broken extractor (`and-and.md`, `the-the.md`, `channel-0.md`…) |
| `personal/` | 44 | 348 KB | 2026-04-28 | STALE; 1/42 has frontmatter |
| `data/earballs-transcripts/` | 2,107 | 211 MB | 2026-05-18 | **696 recordings, 2023-10-01 to 2026-04-28**, plus `_quarantine/` 140 MB |
| `data/*.db`, `*.json` | | ~380 MB | 2026-09-21 | Four SQLite DBs, several JSON indexes (section 6a) |
| `earballs-inbox/` | 294 | 1.9 GB | 2026-04-14 | STALE; 291 `.ogg` from Plaud, April 2026 |
| `comms/` | 37,349 | 156 MB | 2026-09-21 | Spawn logs and inboxes; **live, see below** |
| `logs/`, `tools/logs/` | | 266 MB+ | 2026-09-21 | **live** |
| `tools/` | 216 | 149 MB | scripts frozen 2026-05-18 | Contains secrets; only named pipeline/memory scripts were read |
| `nerd-inbox/`, `mouth-inbox/`, `comms/*-inbox/` | ~240 | | to 2026-09-15 | Duplicated at root and under comms/ |
| `tickler/`, `home/`, `health/`, `projects/`, `travel/`, `v3-notes/` | ~90 | | Mar–Jul 2026 | STALE |
| Root clutter | 30+ | 5 MB | | Client zips/HTML, docx builders, stackdumps, five `.skill` packages, two unnamed blobs (`ziQJUeh1`, `work/clients/zieKig69`) not opened |

### **ALERT: v2 daemons are still running from a Windows machine (2026-09-22)**
`tools/logs/orchestrator-desktop.log` (46 MB) identifies `desktop-nerd` on `E:\Sync\…`, user `Owner`. Every 5 minutes since April it runs `git pull --rebase`, fails on unstaged changes, escalates, fails on a Windows lock file, and writes a conflict log (132 on 2026-09-21). Also alive: the memory compiler (rewrote the FTS DB and index 2026-09-21), the HTTP mesh listener (`/health` every 5 min), `nerd-dispatch` ("no pending tasks" every 5 min), and a broken autocommit. Plaud sync on that machine was retired in June. `comms/orchestrator-health.json` says `status: running` at 2026-09-22 00:55 UTC. **RESOLVED 2026-09-22:** the host was the Rainbow Rig, which Gordon retired the evening of 2026-09-21. Last v2 write was 18:56 MDT on 09-21; zero files modified since (checked against a 21:00 MDT cutoff). The Leah's-machine guess was wrong. v2 is now inert. The Sept 6 "stop the bleeding" step happened by unplugging the machine.

## 3. Map of v3 (DONE 2026-09-22)

**v3 location surveyed:** `~/Sync/Gordonium Enterprises Sync/jarvis-v3/` (copied from the black Mac; landed in Sync rather than `~/Reference/`). 48,679 files, 8.3 GB. Of that, `.venv/` is ~14,000 Python files (a virtual environment, not knowledge) and `data/earballs/` is 4,486 files, 7.1 GB (audio, embeddings, transcripts, SQLite). The knowledge tree proper is under 1,500 Markdown files.

| Zone | Files | Size | Newest | State |
|---|---|---|---|---|
| `CLAUDE.md` (root) | 1 | 10.7 KB | 2026-08-06 | 126 lines, 16 rules. Not read in main thread. |
| `.env` | 1 | 1 KB | 2026-05-31 | **Secrets, inside the Sync folder.** Never read. |
| `_design/` | 49 | 400 KB | 2026-06-05 | Specs, build reports, Gordon's v2 post-mortem and decisions. Stale since June. |
| `_dmz/` | 40 | 212 KB | 2026-06-04 | 36 raw v2 person imports, never promoted. Dead zone. |
| `tools/` + `tools/earballs/` | 64 | 744 KB | 2026-08-18 | The pipeline code. Live. |
| `data/earballs/` | 4,486 | 7.1 GB | 2026-09-21 | Audio, transcripts, SQLite, voiceprints. **Live; pipeline ran yesterday.** |
| `memory/people/` | 39 | 240 KB | 2026-09-08 | 35 people folders; 32 voice-profiles, only 6 profiles. |
| `memory/scratch/` | 43 | 49 MB | 2026-09-11 | Unswept scratch incl. 43 MB of audio chunks. |
| `work/` | 222 | 2.9 MB | 2026-09-11 | 3 client folders (stale since June), Tipelodeon (live to Aug), 185 "project" files of which 120 are private relationship notes. |
| `comms/` | 457 | 2.4 MB | 2026-09-21 | Mouth/Nerd JSON messages; 61% automated health chatter. |
| `tickler/` | 3 | 8 KB | 2026-09-09 | Two expired reminders. |
| git | 70 commits | | last 2026-06-05 | **728 dirty paths.** Nothing committed in 3.5 months. |

Dead or stale zones (3+ months untouched): `_design/`, `_dmz/`, `work/clients/`, `work/amazing-race-application/`, `memory/_index.json` (says 16 people; there are 35), `comms/session-state/`, git history.

## 4a. CLAUDE-SAFE report (v2, DONE 2026-09-22, subagent only; no persona text quoted)

Three instruction files: `CLAUDE-SAFE-DO-NOT-USE.md` (438 lines, no file-level date, 12+ inline date stamps from March to Sept 2026), `CORE.md` (287 lines, header says March 16, contents dated later), `CLAUDE-protocols.md` (186 lines, March 21). Plus `tools/standing-rules.md` (436 lines, not read; it was "the real rulebook" both files point to). v2's own Sept 2026 audit counted **1,341 lines of rule docs and nine overlapping startup definitions.**

Counts: roughly **115 imperatives** across the three files; ~30 duplicated (identity, interaction preferences, mantras, security, DRY, git, evening close-out, startup steps, Windows environment, one tombstone twice); ~20 reference a skill or script that enforces them; **~60 are pure "remember to" with no mechanism.** Several rules cite the incident that spawned them, including recording IDs and a third party's name: rules as scar tissue.

Section by section (purpose, then problems):
- **Identity:** persona paragraph with assigned gender; recovery ritual; hardcoded device names and Windows paths. Duplicates CORE.md verbatim.
- **Hard Rules, All Instances:** ~55 bullets indexing `standing-rules.md`. The first three demand a network health check as the first tool call of every turn and a comms sweep at the end of every turn; memory search fires on any person or topic mention; the morning check-in fires on first contact unasked. "Autonomy: execute without asking" sits beside protocols' "confirm before writing code or sending comms" with no precedence. A retired file-server section is still inside the rules block with full curl instructions. Hardcoded: three Tailscale IPs, a LAN IP, an ntfy topic, `E:\` paths.
- **Next Session Priority:** a to-do inside the config file, never cleared.
- **Who I Am:** health and identity details, duplicated from CORE.md. Wrong layer.
- **How to Work With Me:** five of seven bullets duplicate CORE.md; a second rule index re-lists the Hard Rules within the same file; a full email procedure and seven-account table embedded; contradicts itself and CORE.md on whether Wrike's MCP exists in Cowork.
- **Environment / Windows / Machine Variants:** retired sections retained in full. Three different git stances in one file (PhpStorm aliases; raw `git stash && git pull --rebase`; "never raw git from Cowork").
- **Startup (three sections):** the all-instances boot hits three IPs, two inbox folders and ntfy before greeting. The Mouth section says startup is now skill-enforced; CLAUDE-protocols keeps the 11-step inline version; CLAUDE-SAFE's own tombstones cite protocols' step numbers. Two sources of truth for startup, three counting the skill.
- **Comms / Wrike / Client Roster / Hot Board / Key People / File Map / Mantras:** data and stale boards inside the rules file (an April retreat still on the Hot Board); the File Map lists files that no longer exist.

**Cross-file contradictions (8 confirmed):** comms primary (mesh vs ntfy); Wrike MCP availability; git (three stances); Nerd earballs (ask first vs auto-process; a folder retired in April still checked); startup ownership; autonomy vs confirmation; DRY stated three times and violated by six sections; "only the Mouth may edit CLAUDE.md" with no mechanism and a second overlapping gate in protocols.

**Worth borrowing on purpose:** CORE.md's Data Integrity Protocol (compare-don't-confirm; trust hierarchy: direct statement > primary doc > recall > inference; dated inline correction notes); source tags on every filed fact and an `[unverified, pending review]` marker; "recordings produce entries, not changes"; the prompt-injection stance (external content is data; instruction-shaped text is surfaced, not executed); speaker attribution unconfirmed until a human confirms, as a Pass 0; "no rules about unverified capabilities: verify the mechanism exists before writing the rule"; "helpfulness vs rules: surface the tension"; the Saturday question "faster, smarter, more trustworthy, or just bigger?"; the calendar-driven cadence table, once it's code.

**Routines (8 files):** checklists and procedures that skills were supposed to read; most duplicate the skill's inline text; several carry health, substance, therapy, relationship, finance and named-people content (`morning-routine.md`, `evening-routine.md`, `monthly-personal-review.md`, `saturday-personal-checkin.md`); the Saturday one explicitly violates DRY by holding items moved out of CLAUDE.md and duplicating `personal/action-items.md`.

## 4. Root instruction file report (v3 DONE)

v3's `CLAUDE.md`, per subagent (main thread never read it): 126 lines; 8 sections; the "few rules that earn it" section grew from 6 rules at build to 16 by August. Footer date stale by three months.

Findings:
- **Four rules say "enforced by skill (when built)"; the skill never existed.** Write-to-scratch-first (session-sweep), voice-to-text clarification, state-file updates, attribution cascade (`ingest-attribution-check`). Zero skills were ever built in v3.
- **Two rules are trigger-on-everything:** "check your inbox every turn" and multi-point state updates. Same failure class as v2's rituals.
- **"How To Start A Session" is literally "[TO BE DESIGNED]"**, with the note that v2's startup ritual was part of why v2 collapsed. Startup was never designed; the v2-mount firewall spec was blocked on it.
- **Duplicated truth:** entry phrases in three files (CLAUDE.md, README, user-preferences.md); the file tree in three files; three rules restated in ARCHITECTURE and two proposals.
- **Sensitive data in the auto-loaded file:** the "Who Gordon Is" section carries neurology and identity details that load every session. Wrong layer (same smell as monthly-personal-review in the skills).
- **Rules that are really scripts:** "never drop a naked file" duplicates `structure-lint.py`; "completion is a move" duplicates `complete-item.sh`.
- Things worth borrowing as ideas: "things earn their place by being used"; "the default answer to 'should we add a rule' is no"; "don't ask Gordon to do anything you can do"; the v2-as-biohazard stance (which Sancho already has).

## 5. Earballs pipeline inventory (v3 DONE; this is the live pipeline. v2 PENDING for history only)

**Headline: the pipeline works. It's the one part of v3 that shipped and kept running.** ~2,400 lines of Python 3.12 in `tools/earballs/`, launchd-scheduled, has processed 730 recordings (395 hours of audio, 2026-03-13 to 2026-09-17) since it went live 2026-05-21. Sync last ran 2026-09-21 13:03Z.

### Stages as implemented (all CODE unless marked)

| # | Stage | Where | How | Failure points |
|---|---|---|---|---|
| 1 | Plaud cloud fetch | `tools/plaud-sync.py`, launchd hourly | Paged listing of Plaud's web API; bearer token captured by hand from browser DevTools (no refresh flow); filters Plaud demo recordings; pulls a 7-day window back from newest known | 401 → token expired → CRITICAL alert; token must be re-captured manually. Two wedges (Aug 6, Aug 14) from a PyAV/ffmpeg dylib collision; a 3600 s hard-exit was added. |
| 2 | Download | same | Opus URL then plain; magic-byte and MD5 checks; self-heals missing files | |
| 3 | Ingest | `earballs/ingest.py` | Atomic temp-then-rename; SHA-256; `rec_<10 hex>` ID; SQLite row; junk heuristic | Reconcile handles only `downloading`; rows stuck in `transcribing`/`diarizing` never recover (5 stuck since August). |
| 4 | Silence strip | `earballs/strip_silence.py` | silero-vad, ffmpeg re-encode | **Destructive: overwrites the original audio** (recoverable from Plaud). 44 errors logged. |
| 5 | Transcription | `earballs/transcribe.py` | Groq `whisper-large-v3`, word timestamps, >24 MB chunked with overlap dedup, 3 retries → local faster-whisper large-v3 → medium → fail | 685 Groq, 18 local, 60 failed attempts. |
| 6 | Diarization | `earballs/diarize.py` | pyannote 4.0.4 `speaker-diarization-3.1`, HF token, MPS | Non-fatal; 69 ready transcripts have no speaker count. Over-cluster heuristic flags suspects. |
| 7 | Voiceprint embed | inside diarize | pyannote embeddings, 256-dim, saved per recording as `.npy` + labels sidecar | |
| 8 | Speaker match | `earballs/voiceprint.py` | Cosine vs library, max over refs; tiers 0.70 / 0.80 / 0.90 | **Match goes into the transcript header as hints only; body stays `SPEAKER_NN`.** |
| 9 | Auto-tag | `earballs/autotag.py`, solo rule in process | Solo recordings auto-enrolled as Gordon (149 cases); two-gate systematic tag (sim ≥0.95 with ≥5 refs) | |
| 10 | Transcript write | `earballs/process.py` | `transcripts/YYYY-MM-DD/<rec_id>/transcript.vN.{md,json}` + `processing_log.json`; FTS5 index | Versioned (61 at v2, 5 at v3). |
| 11 | Calendar hints | `earballs/calendar_hints.py` | Reads a cache a Claude session filled via MCP | **MD-dependent**; cache stops in May 2026. |
| 12 | Summary / ingest | **NOT CODE** | A skill instructs a session to draft summaries and set `mouth_ingested=1` after approval | **699 of 730 never ingested.** This is the backlog. |
| 13 | Notify | `tools/jarvis-notify.py` | inbox JSON / macOS notification / ntfy | Watchdog "fired 141 times into an unread inbox." |
| 14 | Watchdog | `tools/pipeline-watchdog.py`, launchd 30 min | Sync freshness, oldest-downloaded age, failures, disk, launchd counter, backup age | Last check 2026-09-21: CRITICAL transcription SLA breach (52 h). |
| 15 | DB backup | launchd nightly 03:00 | `sqlite3 .backup`, keep 7 | Working (7 nightlies present). |

**Decision #11 confirmation:** voiceprint matching is local (pyannote embeddings, cosine in numpy). Seconds of work per recording. Diarization itself is the slow local step (pyannote on MPS), minutes per hour of audio. Nothing here needs a second machine.

### Voiceprint library
`data/earballs/voiceprints/`: `_library.json` index (32 enrolled people, model, dimension), `speakers/<slug>.npy` (one row per confirmed reference; counts 232, 62, 11, 10, then mostly 1–3; **17 people have a single reference**), `recordings/<rec_id>.npy` (651 centroid files). 7.7 MB total. NaN corruption was repaired on 2026-08-18.

**Human-confirmed vs. machine: not recorded anywhere structured.** "Confirmed" is inferred at runtime by matching a centroid against the library at cosine ≥0.999. Autotag appends `[SYSTEMATIC sim=…]` to a person's `voice-profile.md`; unmarked lines default to human. Un-enroll breaks after reprocessing (centroids change, old library row becomes unremovable). Reprocessing renumbers clusters so header hints and ignore-marks can point at the wrong speaker (happened 2026-06-03). **This is the mechanism behind Q9 #7 and the attribution drift.**

### Backlog and health today
- 720 ready, 5 downloaded-not-processed, 5 stuck since August, 0 failed. **699 not ingested** (Mar 212, Apr 131, May 143, Jun 68, Jul 40, Aug 77, Sep 28).
- Sync ran 2026-09-21; a `.sync.lock` with a PID is still present from that run (possibly stuck).
- The hourly job runs but audits come in bursts with multi-day gaps: the machine sleeps or processing stalls.
- Nothing prints "N waiting, oldest from <date>" for the whole chain; the daily note covers the ingest stage only.

### Which machine is running this? (OPEN QUESTION for Gordon)
The DB and audits updated on 2026-09-21, and the launchd plists are in `~/Library/LaunchAgents/` on whichever Mac runs them. The kickoff says v3 lived only on the black Mac; Gordon said the silver Mac is now the only runner. If the black Mac's launchd is still fetching from Plaud into its own copy, the Sync copy will drift from it, and two machines may both hold a Plaud token. Must be settled before Phase 4 touches the pipeline. **Recordings must not be lost during the build: whatever is running today keeps running until Sancho's replacement is proven.**

### Reusable vs. rewrite (pipeline subagent's verdicts, adopted as the Phase 3 starting point)
Keep with edits: `plaud-sync.py` (API/download/MD5 logic proven; drop tagging, ntfy, DB coupling, in-process transcribe), `transcribe.py` (chunking, retries, dedup), `strip_silence.py` (stop overwriting originals), `voiceprint.py` (replace 0.999 provenance with explicit confirmed records), `pipeline-watchdog.py` (checks good; swap transport), `ingest_external.py`, `quick-transcribe.py`.
Keep as-is: `diarize.py` (pin versions).
Rewrite: `process.py` (orchestration tangled with DB/calendar/autotag/FTS), `ingest.py` (keep atomic-rename idea), `autotag.py` / `rehint.py` / `ignore_cluster.py` (ideas over Markdown records), `pipeline.py` / `pipeline-status-daily.py` (as a "N waiting, oldest from" report), `jarvis-notify.py` (macOS notification only).
Drop: `db.py`, `search.py` (unless search proves necessary), `calendar_hints.py` (defer), all Mouth/Nerd/mesh/repo tooling (`spawn.sh`, `comms-check.sh`, `complete-item.sh`, `probe-env.sh`, `structure-lint.py`, `build-*-index.py`, `install-precommit-hooks.sh`), one-offs.

### Secrets
`.env` at repo root: `GROQ_API_KEY`, `PLAUD_BEARER_TOKEN`, `HUGGINGFACE_TOKEN`, `NTFY_TOPIC`, `VIKUNJA_API_TOKEN` (names only; no values were read). Gitignored, but **inside the Sync folder, so it's replicated to sync.com and Leah's machine.** `auth-state.json` can also hold the Plaud token. Rebuild: secrets under `~/.config/` (600) or Keychain, never under `~/Sync/`; never write a token into a state file.

## 5a. Earballs in v2 (history; DONE 2026-09-22)

- **Date range, corrected 2026-09-22 from metadata fields:** the three "2023-10-01" recordings are Plaud demo files with fake timestamps one minute apart (v3's retention probe found the same and filtered them); not real. Two 2025-03-21 files are non-Plaud `.m4a` imports (Pickleproof voice memos). **Real recordings start 2025-08-22** (a DPC meeting, then the WoA partner meeting Aug 24–25); Aug 2025 has 6, Sep 7, Oct 15, then monthly through April 2026. Most 2025 files carry no Plaud API metadata (107 of 113): they were exported from the Plaud app by file, with Plaud's AI-generated titles as filenames, before the API sync existed. So: **effective range 2025-08-22 to 2026-04-28, about 690 real recordings.** Year counts: 2025: 113; 2026: 575 (209 via Plaud API).
- **Transcripts:** `data/earballs-transcripts/<date>/rec_<10hex>/` with `transcript.md`, `transcript.json`, `processing_log.json`. **696 recordings folders, nominally 2023-10-01 to 2026-04-28** (dense from 2025-08; peak 42 in one day, 2026-03-22). Format: `# Recording <date time>`, bold Date/Time/Duration/Participants/Source fields, then `**Speaker N** [MM:SS]: text`. Whisper large-v3. **Speaker names were never resolved: 1,206 of 1,228 speaker mappings are "pending."** Last written 2026-05-18. v3's 704 recordings start 2026-03-13, so the two overlap for six weeks and v2 holds the only copy of everything before March 2026 (~2.5 years).
- **DB:** `data/earballs.db` (246 MB) covers only the Mac era (387 recordings, 365 h, 2026-03-15 to 04-13; 311 exported, 62 failed, 12 dead). The Windows era is a 44 MB `desktop-db-export.json` (227 recordings). The pre-March backlog (377 recordings) was catalogued in `backlog-index-*.json` with machine summaries, topics, and `needs_speaker_review` flags.
- **Voiceprints:** designed in `tools/earballs/voiceprint.py` (same 256-dim, same 0.70/0.80/0.90 tiers as v3), **never populated**: `data/voiceprints/` empty, `voice_embeddings` table 0 rows. The library was started in v3, not v2.
- **Plaud sync:** retired on the desktop June 2026 (marker files). Last real run 2026-04-09. Plaud audio downloads were named by Plaud's 32-hex ID with no date; 291 `.ogg` sit in `earballs-inbox/`.
- **Incidents v2 recorded:** transcripts dated by file mtime, bucketing whole batches under the download date (2026-04-13); LLM-generated summaries and participant names stripped from headers after fabrication (2026-04-15); a full speaker swap on a 74-minute recording; a fabricated client name; a 2h46m recording silently lost (2026-04-13), which triggered the v3 pipeline redesign; pipeline health stale 3 days while both machines were in daily use; plaud-sync failed 4,437 times in a row with an alert every 5 minutes to nobody (Sept 2026).
- **Gordon's backlog framing (2026-09-22):** three eras. (1) **Old backlog:** everything before the pipeline existed, never touched; recordings gathered but unprocessed. Gordon dictated "pre-March 2024"; the evidence says the pipeline was built March 2026 and transcripts reach back to Oct 2023, so the boundary is probably March 2026 (confirm). (2) **The good period,** March through ~June 2026, when Jarvis ran well (v2 ingest active to 04-28; v3 pipeline live from 05-21, but its ingest step never ran). (3) **Fresh backlog:** from when that stopped until now. Sancho's first backlog job (notes-to-self, newest first) works era 3 first, then 2, then 1.
- **What the backfill needs from v2:** the 696 transcripts and their `transcript.json` (word timing), `backlog-index-*.json` (machine catalogue, untrusted), and the 291 raw `.ogg` in `earballs-inbox/` plus whatever Plaud still holds (Plaud retains everything, per v3's probe). Nothing in v2's DB is needed if the transcripts are re-derived.

## 6. Data inventory incl. non-Markdown stores (v3 DONE)

### Where knowledge lives in v3
- **People:** `memory/people/<first-last>/` with `profile.md` (YAML: name, aliases, type, role, status, location, created, updated, **sources**, relationships, tags, key_facts) and `voice-profile.md` (enrollment log). 35 folders, but **only 6 have a profile**; 32 have only a voice log. Gordon and Leah have no profile. Provenance is present where profiles exist: `sources:` lists, inline `[gordon:verbal DATE]` and `earballs:rec_X` cites, "What we don't know yet" sections. No numeric confidence; `status: stub|active` is the only structured trust signal. One file (`chad-cohen/scratch.md`) has an explicit trust-tier line and "carryover from v2 (leads, not facts)": the clearest confirmed-vs-guessed expression in the tree, and a template worth borrowing.
- **Clients:** `work/clients/` holds three (travis-crawford-hvac, society-hill, precision-chiro), all stale since June 2026. **Guidelines and knowledge are not separated**: account team, financials, competitor intel, ad scripts, action items and hosting config all in one file. Tipelodeon sits at `work/tipelodeon/` (21 files, live to Aug 2026) and is the best-maintained file in the tree: `v2_pointers`, `ingest_notes`, per-section dates, CONFIRMED/LOCKED flags.
- **Projects:** `work/projects/` 185 files. **120 of them are private relationship notes under `work/`** (wrong lobe). 40 are Jarvis meta-notes, 14 are a Leah satellite install kit, a 30 KB draft WordPress CLAUDE.md (ancestor of the kit's rules), and empty scaffolds for personal-narrative, self-reflection, pickleproof, publishing-stack.
- **Scratch:** `memory/scratch/` 43 files, 49 MB, marked `status: scratch (unpromoted, not session-swept)`. 43 MB is audio chunks that belong in data/. Includes intimate relationship notes "pending promotion" beside work ingest notes.
- **Transcripts:** in `data/earballs/transcripts/`, not in the knowledge tree; 704 recordings, Markdown with a bullet header (not YAML), `**SPEAKER_NN** [t]` paragraphs.

### Non-Markdown stores and what would be lost
| Store | What it holds | Depends on it | Markdown equivalent needs |
|---|---|---|---|
| `data/earballs/db.sqlite` (26.7 MB, WAL) | `recordings` 730 rows (24 cols: plaud_id, recorded_at with offset, duration, sha256, status, backend, version, speakers, ingested flag, error, ignored clusters); `transcription_attempts` 852; `audit_log` 3,150; `transcript_fts` 696 | Every pipeline script; watchdog; status report | Per-recording frontmatter carrying those fields, plus an append-only log file. FTS replaced by ripgrep. |
| Voiceprints (`.npy`, 7.7 MB) | 32 speaker reference sets, 651 recording centroids | Speaker ID entirely | Cannot be Markdown. Keep `.npy` sidecars outside git; record human-confirmed (rec_id, cluster, name, who, when) in Markdown so the library is rebuildable. |
| `transcript.vN.json` | Word-level timestamps, diarization segments, matches | Nothing downstream today | Keep as sidecar; only place word timing lives. |
| `voiceprints/_library.json` | Index of enrolled people (names) | voiceprint.py | Fine as JSON, or a generated Markdown index. |
| `comms/**/*.json` (446) | Mouth/Nerd messages | Nothing after the split is dropped | None needed; see 6.3. |
| `memory/_index.json` | People index, frozen at 16 of 35 | Nothing | Regenerate from frontmatter (decision #4). |
| `sync-health.json`, `watchdog-health.json`, `auth-state.json` | Pipeline health, alert dedup, token | watchdog, sync | Health can be a generated Markdown line; token must not be in a state file. |
| `work/tipelodeon/*.html` (4), `.pdf` (1) | Financial models, annotated operating agreement | Gordon | Markdown twins partly exist; keep the originals as attachments. |

### Comms channel (evidence for "fell behind and didn't know")
446 JSON messages, May–Sep 2026. Two competing timestamp fields, two filename conventions, eight identities. **61% is repetitive automated health chatter** (113 copies of one launchd alert; 112 identical daily "N overdue" notes). A September message admits the watchdog "fired 141 times into an unread inbox." **The detection worked; the channel was wrong.** Durable knowledge trapped only here: the sync-outage root cause (ffmpeg 8.0.1 vs PyAV dylib collision, marked "NOT YET FIXED"), the Sept 8 capture-gap analysis, and voiceprint-hygiene findings (which enrolled references look like someone else).

### DMZ
`_dmz/` was the designed quarantine: copy a v2 file in, Gordon edits, says "assimilate," it moves to `memory/people/`, the v2 original is deleted. **36 person files came in (May 23–Jun 4); zero were ever promoted.** A reminder note from 2026-06-02 ("not going to do that tonight") is still open. The mechanism is exactly Sancho's Phase 3 `_quarantine/` idea; the lesson is that the review step needs a forcing function, not a reminder.

### Git
70 commits, first 2026-05-07, last 2026-06-05. 728 dirty paths (542 untracked, 177 modified). `.gitignore` covers audio, DB, `.npy`, `.env`; but 49 MB of `.m4a` in `memory/scratch/` is not ignored and `.idea/` files are tracked despite being ignored. Git was abandoned when the sweep-and-commit discipline was.

## 6a. v2 data inventory and retrieval (DONE 2026-09-22)

### Knowledge layout
- **Clients:** `work/clients/` holds 34 entities typed `client` plus document clusters, 284 files. A client file (e.g. D&M Heating) is frontmatter, a bold fact block, then H2s: Key People, owner personality, **Gordon's Role**, Account Origin, Business History, Revenue, Marketing, Operations, Staffing, Competitors, current project, Seasonal Patterns, Writer History, Zoom Meeting Log. **No guidelines/knowledge split**; voice profiles, sacrosanct copy and meeting logs are sibling files with the client prefix. `key_facts` blobs ballooned (D&M has ~35, several correcting earlier ones in place: silent overwrite by accretion).
- **People:** `relationships/people/` 101 files; frontmatter with typed relationships (`parent_of`, `ex_of`, `works_with`, `contractor_for`…), then Who / Context / Connects To / To Fill In / Notes. Plus `gordonos-people.db` (138 contacts with addresses, phones, birthdays from Google Contacts).
- **Frontmatter coverage:** partners 18/18, relationships 77/106, clients 101/193, personal 1/42, everything else 0. Fields: `name, type, aliases, relationships, tags, key_facts, parent_entity` core; documents add `status, created, updated, client, sources, attendees, meeting_date, source_transcripts, privacy` and more. `type` has 14 values.
- **Provenance markers:** `[earballs:rec_x, date]` dominant; also `[source:zoom-vtt-extraction date]`, `[gordon:verbal date]`, `[gordon:cowork date]`, `[inferred]`, rare `[unverified]`/`[verified]`. Files with any marker: relationships 73%, clients 36%, personal ~50%, partners 33%.
- **Business/client blur, confirmed:** **no field for ownership.** Signals are a prose H2 "Gordon's Role" (25 files) and tags (`woa` 13, `clc` 11, `equity` 3, `venture` 1). Gordon's own companies sit as loose files in `work/` root beside retreat agendas; equity situations (Tipelodeon, Dragonfly DPC, a partner's 2%) are typed `client`. Same entity in multiple places: Lake Day in four folders; Leah in three files; four WoA partners in both `partners/` and `people/`; LottoEdge across five locations; Wizard Academy as a "person" plus seven loose files. `work/dashboard.md` is the one place that lists owned vs. client businesses.

### Non-Markdown stores
| Store | Size | Holds | Written by / read by | Sancho needs |
|---|---|---|---|---|
| `data/memory-fts.db` | 41 MB | FTS5 over 1,301 docs (706 transcripts, 262 work, 145 comms, 105 people, 42 personal, 33 tools, 8 routines) | `memory-compiler.py`; `jarvis-listener.py /search` | Idea only: full-text search that includes transcripts. Ripgrep first; FTS if too slow. |
| `data/memory-index.json` | 339 KB | 182 entities, alias index, inverted relationship graph, compiled from 227 frontmatter files; 42 warnings | `memory-compiler.py compile`; loaded whole at startup | **Borrow the idea** (section D below). |
| `data/earballs.db` | 246 MB | 387 recordings, 1.5 M words, 231 k diarization segments, speaker mappings (98% pending) | `plaud-sync.py`, `tools/earballs/*` | Nothing; superseded by v3's DB and transcripts on disk. |
| `data/gordonos.db` | 2.4 MB | Older entity/relationship/tag index (2,511 entities) | `memory-db.py`; still referenced by brief-me | Nothing; replaced by the JSON index and never retired. |
| `data/gordonos-people.db` | 40 KB | 138 contacts' PII | `build_people_db.py` | Contact details belong in Contacts, not a DB beside knowledge. |
| `comms/active-work.json` (+2 CONFLICT twins, 4–5 MB) | 1 MB | The orchestrator's task queue: entirely `git-conflict-*` tasks | orchestrator | Nothing. |
| `data/backlog-index-*.json`, `desktop-db-export.json` (44 MB) | | Backlog catalogue and Windows-era DB dump | one-off scripts | Backfill inputs, untrusted. |
| `.npy` / `.pkl` | none | | | |

### Retrieval mechanism (the borrow-on-purpose candidate, `tools/memory-compiler.py`, 715 lines, stdlib only)
Three layers: **(1) YAML frontmatter as the only structured store**, read from exactly three folders (`relationships/people`, `work/clients`, `work/partners`): `name, type, aliases, relationships, tags, key_facts (cap 50), parent_entity`. **(2) A compiled `memory-index.json`**: entities by slug, an alias index (lowercased names and aliases → slug), an inverted relationship graph; plus a `validate` step reporting missing frontmatter, duplicate names, alias collisions, broken relationship targets, over-cap facts, stub bodies. **(3) FTS5** over body text of every `.md` in seven folders, incremental via a hash cache. Query: exact alias hit first (returns file, top 5 facts, top 5 relationships), then substring scan over names/facts/tags, then FTS `MATCH` with snippets. No embeddings. Sessions were told to load the JSON index whole at startup, recompile if older than 24 h, and query it on any person/entity mention.

**What worked:** frontmatter as truth (git-diffable, human-editable); a small compiled index loadable at startup; alias resolution; FTS as fallback; the validator. **What didn't:** `key_facts` as an unbounded blob; two indexes never reconciled (skills pointed at both); FTS scope dragged `tools/` and `comms/` into "memory"; junk entities indexed without complaint. This is close to the kickoff's decision #4 (generated indexes from frontmatter) and confirms the approach; Sancho's version generates per-folder INDEX.md instead of one JSON blob, and validates on generation.

### Ivy League short course (carry-forward item, RESOLVED after a second, deeper search)
First search undersold it. **`personal/think-better.md` (16 KB, 319 lines, filed 2026-03-12, edited 03-16) is the curriculum**, built in two claude.ai conversations before GordonOS existed: a 3–4 year architecture; Year 1 in four 12-week phases (Memory; Critical Thinking incl. a default stack and five thinking patterns from a 3/15 voice note; Logic and Fallacies; Rhetoric and Integration) with resources; Years 2–4 as six-month domains (Writing and Persuasion, Systems Thinking, Economics and Institutions, History and Political Theory, Integration) each with competencies, a training regimen, Socratic prompts and a 5–6 book list; a weekly sparring-partner protocol; a "hidden core curriculum" section; a status log that never advanced past "nothing formally started."

What was lost: the **week-by-week Year 1 habit plan** was exported as `think_better_plan.docx`, arrived corrupt, and was never regenerated; it exists nowhere in either root. What was never built: hour-a-day session content, a term/class tree, actual sparring sessions, anything dispatched to a Nerd. The only automation was T122, a daily nag to install Anki, killed 2026-04-22. A v3 migration queue (`_dmz/v2-think-better-migration/README.md`, 2026-05-31) planned to add a Fear-setting technique and was never executed. Gordon's descriptions to others ("it built a whole thing," 3/18) were accurate; "I haven't started it yet" (5/10) was too.

What he said he wanted (transcripts 3/13, 3/18, 4/3, 5/10): the logic-rhetoric-argument-power layer an Ivy education teaches; memory → logic → fallacies → critical thinking → how to read a book; delivered as an hour a day in conversation, not video; four school nights a week for three years, framed as self-care replacing TV; "I think really fast, I need to learn to think better."

Related and already shipped: v2's `critical-thinking` skill is the "default critical thinking stack" from Phase 2. Seeds for a rebuild: `think-better.md` in full; the evening-routine school-night slot; the Term > Class > Assignment tree he pictured; and the T122 lesson: **produce the first session's content, not a reminder to start.** ICE item, personal lobe; and, given Q3's "enormous amounts of available time," probably a high one.

## 7. v3: what it changed relative to v2 and whether it worked (DONE)

| Change | Why | Result |
|---|---|---|
| Lean CLAUDE.md, few rules, discipline in skills | v2 had 50+ cargo-cult rules and heavy auto-loaded context | Rules grew 6→16. **Zero skills ever built.** |
| Per-identity inboxes, single-writer files | v2's shared session-state was silently overwritten by merge auto-resolution since 2026-04-10 | Folders built; watcher never coded; rule asks the model to poll every turn. |
| Completion as a move (`_active/` → `_archive/`) | v2 zombie tasks from in-place checkboxes | Script built and smoke-tested; never used on real items. |
| Structure lint + capability index | No single source of "what exists" | Built. Capability index was hand-edited despite claiming auto-generation. |
| Headless Nerd spawn | v2 headless sessions had no identity | Built; never used for real dispatch. |
| **Medical-grade earballs pipeline** (atomic ingest, WAL, Groq + local fallback, VAD, watchdog, backups) | A 2h46m Grayson recording was silently lost in v2; a 4-day gap | **Shipped 2026-05-21 and ran.** 730 recordings. The one clear success. |
| Voiceprint speaker ID | "Misattributed data is as bad as untrue data" | Built. Provenance gap (above). Errors still occurred: "3+ cascading attribution errors despite sim=1.000 hints." |
| Startup design (<60 s cold, <30 s re-sync) | v2 startup took 2+ minutes | **Never designed.** |
| Memory index, skills, tickler, session-sweep | Core exocortex functions | **Never built.** |
| Tailscale mesh to Leah's PC | Leah as satellite | "Building"; abandoned. |

**Where it stalled:** everything mechanical shipped; everything cognitive didn't. After 2026-06-05 the only edit is one rule in August. The system had a working ear and no brain. And the contamination it was designed against happened anyway (2026-06-05, v2's CLAUDE.md leaked into a v3 session), which produced the "never mount v2" rule Sancho inherited.

**Why it matters for Sancho:** v3 proved that (a) the pipeline can be reliable when it's code with a watchdog; (b) a lean rules file does not stay lean without a mechanism; (c) "enforced by a skill when built" is a promise that doesn't get kept; (d) a quarantine without a forcing function fills and stays full; (e) alerts into a channel nobody reads are not alerts. Phase 2 should treat each of these as a constraint with a mechanical answer.

## 8. Gordon's own account of the failures (DONE from v3's `_design/`; v2's closeout notes still PENDING)

v3's `_design/gordon-decisions-from-v2-planning.md` (42 KB, 2026-05-03, extracted from an 840-line planning chat "by v2 Mouth, so remain skeptical") and `pick-over-the-carcass.md` are Gordon's earlier post-mortem. Cross-checked against Phase 0, they agree on every major point and add these:

**Failures he recorded then (paraphrased, with the section):**
- The central discipline failure: Jarvis said "we could easily go build," Gordon didn't hold the planning line, cruft accumulated (§2). Half-built things became permanent (§3.1).
- Stale signals: dashboard says X, reality says Y, nothing reconciles (§3.2). Completion markers don't propagate; items resurface (§3.3).
- Features amputated without replacement, leaving orphaned references (§3.4). Convention sprawl outpaced retirement (§3.5).
- Four overlapping sources of truth: CLAUDE.md, standing-rules.md, skills/, CORE.md (§3.6).
- The Mouth agreed to rules it structurally couldn't follow, like "pulse every turn" (§3.7).
- Jarvis sent emails to third parties without consent, multiple times, with guardrails in place (§3.8). (Same as Phase 0 Q6b.)
- Basic file-visible facts went ambiguous: whether LottoEdge was his business or a client (§3.9). (Same as Q8.)
- Voice-to-text errors auto-corrected silently (§3.10).
- Worst case: "spending too much time working on the system rather than the system working" (§1).
- Cross-machine writes silently discarded by merge auto-resolution since 2026-04-10; a 12 KB handoff overwritten. "MUST FIX CRITICAL FAILURE" (§26).
- Every-turn rules that don't fire yet add latency; startup took 2+ minutes; date and day-of-week errors (§27).
- Four simultaneous sessions "may only make me feel busy" (§28). (Same as Q6b addendum.)
- The memory layer "still feels really weak" after SQLite and JSON index attempts (§29).
- The planning session itself kept "perpetuating version two stupidity" (§30).
- Anti-patterns (carcass doc): rules without an earned failure; auto-loading context; mistaking v2 structure for v3 structure; managing Gordon's time; padded replies; stale disk claims; bulk import.

**Decisions he recorded then that Sancho should honor or consciously revisit:**
- Four roles: idea capture, ideation partner, priority partner + bionic memory, senior developer (§1). Memory + preferences is the one non-negotiable asset.
- Posture: chief of staff, warm not deferent, constructively challenging; counterbalance his ENFP with S, T, J pushback (§4, §5). Never suggest he stop working; calendar nudges only (§27).
- Co-author the prompt before running any substantive build (§2). Recon-and-prompt: burn a session on recon, hand a fresh session a spec (§12).
- Every skill is a technique he already knows but fails to trigger (§22). Skills win over MDs in conflict; rigor in skills, persistence in MD (§27). Rules that can't fire reliably shouldn't exist (§27).
- Context: director/performer/sides model, progressive reveal not upload (§6). Four tiers: global kernel, environmental kernel, chunky modes (Work/Personal), fine-grained files (§9). Kernel names at most 6 people. Explicit "load Work Mode" as baseline (§9). **Memory structure and context structure are two separate designs (§27).**
- Memory: the hard part is access, not storage (§8). Four layers: raw immutable transcripts, processed trust-tiered, scratch, live context (§10). Scratch sweep at every context switch (§10). Five trust tiers; contaminated content deleted with an event log (§13). **Mandatory source field; no source means scratch only (§15).** Fact-check everyone including Gordon (§14). One canonical location per entity (§27). Per-instance state files, append-only logs, conflict detection on large overwrites (§26).
- Email READ/DRAFT only, SEND never (§3.8, §27). Plaud: solo notes first, multi-speaker second, Zoom third; 12-hour max lag; low speaker confidence means stop and ask (§18).
- Persistent visualization of the architecture (§20). Mechanical `date` at startup (§27). Portable WordPress standards MD separate from the brain (§27; became the kit's CLAUDE.md).
- Build minimal first, then pick the carcass item by item, nothing bulk (§30).

Most of these are already in the kickoff or Phase 0. The ones that are new and worth carrying to Phase 2: **memory structure vs. context structure as two designs**; the **four-tier context model**; **"no source means scratch only"**; **append-only logs with conflict detection**; and **"rules that can't fire reliably shouldn't exist"** as a lint criterion for CLAUDE.md.

## 8a. v2's own account of its failures (DONE 2026-09-22; from `work/builds/`, `v3-notes/`, `comms/`, `personal/`, `tickler/`, `nerd-inbox/`)

v2 diagnosed itself twice: April 2026 (`work/builds/gordonos-v3-planning.md`, `architecture-review-2026-04-18.md`) and September 2026 (`work/builds/v2.5-*.md`, Sept 6). Both agree with Phase 0. Specifics it recorded:

**Startup and rituals.** Boot took 2+ minutes; the morning chain ran even on afternoon re-sync; ~10 tool calls before a briefing; a 500-line CLAUDE.md called "evidence of not trusting the system." By Sept 2026: **nine overlapping startup definitions** (CLAUDE.md ×3, two skills, a slash command, a SessionStart hook, `tools/startup-sequences.md`, wake-phrase prefs pointing at dead paths); 1,341 lines of rule docs. The Mouth "agreed to every-turn rules that structurally can't fire, then added latency when they did": the worst of both worlds. Date/weekday errors.

**Multi-machine comms (the fatal thread).** 2026-04-10: `comms/session-state.md` went from 12,405 to 2,886 bytes in one orchestrator merge (77% loss), never recovered. Cause: three writers (Mac `auto-sync.sh`; Windows `periodic-sync.py`, deprecated since 03-27 but still scheduled and producing 65% of commits; Mac `jarvis-orchestrator.py` spawning conflict-resolvers with a 60 s timeout that always expired). 513 auto-resolve commits on one JSON file. Then, June 3 to July 29, ~60 near-identical auto-spawned "runaway loop" escalation notes, unread. Sync.com was also syncing `.git/` itself, producing a phantom `main-CONFLICT-1` branch. The fix ("stop the bleeding," Sept 6) never ran. Also: an unauthenticated file server and an unauthenticated ntfy topic; short-path PUTs that "caused silent misfiles"; a 5-layer resilience build dispatched to the Nerd of which 2 layers were never wired and nobody surfaced it: "Mouth designs, dispatches, Nerd builds partially, nobody closes the loop."

**Attribution and earballs.** Listed in 5a. Plus: Mouth trusted `mouth_ingested: true` flags with no filing evidence; asked Gordon facts already on disk; fabricated content was cancelled rather than recovered ("better gone than still contaminating our thinking"); "v1 died within 2 days from content poisoning."

**Memory and retrieval.** "Still feels really weak" after SQLite and JSON; the weakness is context access, not storage; a live incident where the right text came back as the wrong semantic slice. Mouth recommended Todoist without checking that a Todoist migration had already failed in March. A search burned looking for a "Groq spec" that was really the pipeline redesign: "search by the system, not the feature."

**Rules and skills.** Convention sprawl; four overlapping sources of truth; "a discipline problem means the rule is too weak and should be a skill"; compaction strips skill-firing context so violations accumulate after compaction (`reboot-after-compaction` skill exists for this); research subagents hallucinate sources "~30% of the time" (`source-verify` skill exists for this); email SEND removed after rogue sends.

**Capture and tasks.** "v2 captures well; retires badly." Tickler zombies 27+ days; inbox and someday files Gordon didn't know existed; "Jarvis spewing untracked, unconfirmed action items into client files" eroding trust, "fix must be structural"; a Todoist migration that collapsed 11 lists into one (~80% migration failure, ~20% tool fit). By Sept 9: 68 action items untouched since April, 20 ticklers overdue.

**Other.** Four "enthusiastic commit" errors in one planning session. Gordon mounted v2 by habit and worked hours in the wrong brain (June 10). Greenfield v3 "lived only on the black MacBook outside Sync and did not migrate" (Sept 6). v2.5 stalled at Phase 0.

**Retired or killed (per its own record):** Dropbox (broke symlinks) → Sync.com; ntfy as backbone (unauthenticated) → mesh, but ntfy lingered; OpenClaw + Copper Nerd "amputated," never hands-free; `gordonos.db` → JSON index, never actually retired; a reconciliation sentinel that killed transcription mid-run; the `earballs-inbox/` flag-file design (flag and file in different durability domains → the Grayson loss) → DB as truth; transcript auto-summaries (fabrication); email SEND; Todoist; Ivy League courseware T122; OpenClaw server T006; session-startup and evening-closeout skills (superseded, still installed); greenfield v3.

**Extra v2 skills not in the 19 copied:** `open-tasks`, `persuasive-argument` (WoA heart-first persuasion for client docs), `post-build-sweep` (catch zombie references after restructures), `reboot-after-compaction`, `source-verify`. The last three are mechanisms worth re-deriving; `persuasive-argument` is a work skill to review in Phase 3.

## 9a. Buried treasure in v2 (DONE 2026-09-22; one line each; all via ICE)

**System ideas**
- `work/builds/gordonos-v3-planning.md`: the clearest self-diagnosis in either system; the theater "sides" model; ENFP counterbalance posture; "externalize Gordon-brain" as the definition of a skill; five trust tiers; "no source = scratch only"; files as truth with derived atoms; single push authority; per-machine state; append-only handoff log; `+jarvis` plus-addressing email capture across 7 inboxes.
- `work/builds/v2.5-and-ge-os-spec.md`: **every file has exactly one writer**; inboxes append-only, one file per message; no daemon writes.
- `work/builds/v2.5-recovery-plan.md`: re-arm one skill at a time with a durable trigger and a retirement line; a 6-call startup; **"skill on disk but not on the map = not armed"** (the map as the drift check, exactly decision #12).
- `work/builds/evidence-first-mouth-spec.md`: "Rules get skipped. Tool calls inside workflows don't."
- `work/builds/task-tool-requirements-2026-04-18.md`: re-engagement matters more than features; Gordon creates his own tasks (matches the tasks decision).
- `work/builds/todoist-failure-analysis-2026-04-18.md`: never restructure Gordon's categories.
- `work/builds/v3-earballs-backlog-vs-fresh.md`: separate the backlog population from the SLA-bound fresh pipeline; solo-voice-first MVP (matches the notes-to-self decision).
- `work/builds/architecture-review-2026-04-18.md`: a heartbeat for the watchdog itself.
- `tickler/2026-04-18-task-system-architecture.md`: "behavioral fixes don't survive compaction; structural ones do."
- `.claude/skills/source-verify`, `post-build-sweep`, `reboot-after-compaction`: mechanisms to re-derive.
- `personal/gordonos-decisions-log.md`: a "why things are this way" log (Sancho's decisions.md is the same idea).
- `personal/open-questions.md` "Improvement Backlog": quick-confirm attribution flow; retention tiers.
- `tools/PLAUD-PIPELINE-REDESIGN.md`, `tools/pipeline-resilience.md`: the pipeline redesign specs (in `tools/`, not opened; v3 implemented them).

**Gordon's own thinking material (personal lobe candidates)**
- `personal/think-better.md`, `principles.md`, `mantras.md`, `reading-strategy.md`, `claude-best-practices.md`, `ai-board-of-directors.md`, `human-assistant-log.md`.

**Work material (work lobe candidates)**
- `work/woa-partner-playbook.md` (how WoA deals and teams form); `work/ads-system-master.md` (WoA iterative ad system); `work/writing-techniques.md`; `work/playbooks/manual-cpc-campaign-build-handoff.md`; `work/reference/presentation-frameworks.md`, `wizard-academy-personality-type.md`; `work/specs/clc-pricing-plugin-spec.md` (2026-07-24); `work/handoffs/2026-06-11_society-hill-design-code-handoff.md`; `work/business-continuity-planning.md`; `work/dashboard.md` (client roster with lead partner and Gordon's role, the only owned-vs-client list); `work/builds/content-definition-skill-wip.md` (CLC MSA phases as a skill); `work/wp-dev-kb.md` (already the ancestor of the kit's lessons).
- `work/clients/`: 34 client files; the D&M Heating file is the richest template of what a client knowledge file held.
- `.claude/skills/persuasive-argument`.

## 9. Buried treasure in v3 (DONE)

Each one line, with where it lives. All go through ICE, none straight to build.

- Voiceprint library with cosine tiers and per-person voice-profile logs (`tools/earballs/voiceprint.py`, `memory/people/*/voice-profile.md`).
- Calendar-window correlation to guess who was in the room (`calendar_hints.py`; needs a real calendar fetch).
- SQLite FTS5 transcript search (`search.py`); keep in mind if ripgrep proves too slow.
- Content-sanity veto: "a person doesn't refer to themselves in the third person" as a mechanical attribution check (`_design/auto-tag-systematic-approval-spec.md`).
- The first-person-recounting trap as a named error class (`_design/ingest-attribution-discipline-spec.md`).
- Two-checkpoint ingest: paste the voiceprint mapping verbatim first; refer to speakers by cluster ID until confirmed (same spec; never built).
- launchd `ProcessType=Background` silently defers hourly jobs; check the `runs=` counter (pipeline build spec §3.15).
- Plaud demo recordings share one serial number; filter them (retention findings).
- Plaud retains everything indefinitely, so Plaud is the durable upstream and re-fetch is always possible (retention findings).
- Design-review checklist as "a test suite for plans" (`_design/design-review-checklist.md`).
- Three lifecycle endpoints: complete / drop / defer with `defer_until` (`lifecycle-and-scope.md`).
- Extraction marker `<!-- extracted to: … -->` so re-reading a transcript never re-emits items (`lifecycle-and-scope.md`).
- Async, debounced derived-index compile that never blocks a write (gordon-decisions §16).
- Contamination event log kept after deleting a bad fact (gordon-decisions §13).
- Trust-tiered drift detection, including on Gordon's own statements (gordon-decisions §15).
- Release review gated on cumulative diff since last tag, with an `--emergency` audit trail (`_design/capabilities/pre-release-review.md`).
- The chad-cohen scratch file's explicit trust-tier header and "carryover from v2 (leads, not facts)" section, as a template.
- Tipelodeon's working-file discipline: `v2_pointers`, `ingest_notes`, per-section dates, CONFIRMED/LOCKED flags (`work/tipelodeon/tipelodeon.md`).
- The draft WordPress CLAUDE.md in `work/projects/wordpress-practice/` (30 KB, Aug 2026): check whether anything in it postdates the kit's rules file.
- Watchdog check list (sync freshness with wake suppression, oldest-item age, disk, launchd counter, backup age) (`pipeline-watchdog.py`).
- Sync-outage root cause (ffmpeg vs PyAV dylib collision, "NOT YET FIXED") trapped in `comms/session-state/mac.mouth.main.md`; needed before the pipeline is touched.
- Still to find in v2: the Ivy League short-course outline; the retrieval mechanism; the SQLite store.

## 10. Smell list, mapped to the post-mortem (FINAL 2026-09-22: skills + v3 + v2)

Additional v2 evidence per row is appended in the Evidence column after "v2:".

| Smell (v2-only additions) | Evidence | Post-mortem line |
|---|---|---|
| Zombie automation | v2: an orchestrator on a Windows machine has looped a failed rebase every 5 min since April; 37,188 conflict logs; alerts to nobody 4,437 times in a row; "stop the bleeding" planned Sept 6, never run | Q3, Q9 #10; and the OpenClaw lesson: retired in prose is not retired |
| Nine startup definitions | v2's own Sept audit | Q2 |
| Rules as scar tissue | ~60 "remember to" rules citing the incident that spawned them; 115 imperatives across three files | Q1 |
| Amputation without cleanup | mesh, OpenClaw, orchestrator, `gordonos.db`, two skills: all "retired" while still installed or running | (new) needs a retirement line per component (v2.5 plan had this idea) |
| Merge-resolved truth loss | 77% of a state file lost in one auto-merge; Sync syncing `.git/` itself | Q9 #5, #6, #11; decision #9 already moves git out of Sync |
| Fabrication into the tree | fabricated client name; LLM summaries stripped after contamination; "v1 died in 2 days from content poisoning" | Q9 #4 |
| Capture without retirement | "captures well, retires badly"; 68 items untouched since April; 20 overdue ticklers | Q7 (tasks stay outside); ICE needs a kill path |
| PII database beside knowledge | 138 contacts' addresses and phones in `gordonos-people.db` | Q9, lobe design |

| Smell | Evidence | Post-mortem line |
|---|---|---|
| Guidance in MD that should be code | "Enforced by skill (when built)" ×4 in v3 CLAUDE.md; brief-me's 11-path search as prose; the 10-pass ingest loop; mesh health checks in five skills | Q2 (sounded competent, quality didn't show) |
| Rituals and trigger-on-everything | morning-startup 20 steps; "check inbox every turn"; whats-next at every lull; think-first "err toward looping" | Q2 (startup looked at too many things, stopped using it) |
| Duplicated truth | Entry phrases ×3, file tree ×3, routine checklists inline and in files, timestamp fields ×2, done-state ×2 | Q1 (rules contradicting each other) |
| State only in conversation or a dead channel | Mantra rotation, nag loops, closed-threads acknowledgment; sync-outage root cause in a session-state file; 141 unread alerts | Q3 (fell behind, didn't know), Q6 (erosion) |
| Unverified attribution into the tree | Weekday/vocabulary speaker heuristics; hints in header, no confirmed field; corrections never reach the voiceprint; errors "despite sim=1.000" | Q1, Q4 (attribution drift, loss of faith) |
| Silent overwrite | write-it-down with no append/replace rule; strip_silence overwrites originals; merge auto-resolution discarding writes since April | Q9 #6 |
| No forcing function on review | DMZ: 36 in, 0 out; 699 unignested recordings; "not going to do that tonight" still open | Q3 (backlog), Q7 (need to be in the loop) |
| Sensitive data in the wrong layer | Health details in CLAUDE.md, in skills, in `work/`; 120 relationship files under `work/projects/` | (new) lobe design, #3 |
| Secrets near knowledge | `.env` inside the Sync folder; token in a JSON state file | Q9 (must-nevers), decision #9 |
| Business/client blur | LottoEdge ambiguity (v2); clients without a business field; partners folder empty | Q8 |
| Building over polishing | v3: pipeline built, brain never; rules 6→16; zero skills; git abandoned after 4 weeks | Q2, WIP-limit decision |
