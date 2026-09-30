# Sancho architecture

Phase 2 deliverable. Started 2026-09-24. Built one decision at a time with Gordon; each section is written when its decision lands and cites `decisions.md`. Sections marked PENDING have not been decided. Nothing in here is built until Gordon approves the whole document (kickoff, Phase 2: "Stop and get my approval").

Reading order for a new session: STATUS.md → this file's "Decisions so far" table → the section you need. Do not reload survey.md unless a section here says "see survey" and you need the evidence.

## Glossary (fixed 2026-09-26; these words mean one thing each)

| Word | Means | Lives |
|---|---|---|
| **command** | a script the Mac-side watcher is allowed to execute, with a timeout and optional schedule; the allowlist is the table `_setup/commands.md` | `_setup/` |
| **run** | one execution of a command: a request file in, a result file out | `_queue/requests/`, `_queue/results/` |
| **schedule** | a command that launchd also fires on a timer (hourly sync, nightly map); still a command, still in the table | launchd plist + the table's `schedule` column |
| **job** | a multi-stage piece of work with a state file: stages done by skills (which may request runs), human gates that wait, a `current` pointer; the kickoff's "a job is a state machine on disk" | `_queue/jobs/` |
| **skill** | a procedure Claude follows in a session, with a header, trigger scope, and a write step; `shared: astra` marks a business skill Leah's Astra consumes unchanged | `skills/` |
| **area** | GTD Horizon 2: a role or responsibility maintained rather than finished: each business, and the personal areas (food, rv, nomad, me, finances) | `work/<business>/`, `personal/<area>/` |
| **project** | GTD Horizon 1: any outcome needing more than one action ("Plan the Alaska trip", "Overhaul the plugin library"); has a job file once in motion, a lobe, an area, and a **Next Action**; **unlimited**; work projects mirror Wrike projects. (Was "endeavor" until 2026-09-26.) | `work/<business>/projects/<slug>/`, `personal/projects/<slug>/` |
| **focus** | which projects get Gordon's attention in a horizon: **3 per lobe per horizon**, nested month → week → day, set with him and checksummed daily | `FOCUS.md` (spine) |
| **next action** | GTD: the next physical, visible step on a project; one line on the project; it is a task, so it also lives in Google Tasks (personal) or Wrike (work), created by Gordon; flagged when unchanged for **1 week** | on the project file |
| **task** | a single action or a short sequence done in one or two sittings; lives in Wrike (work) or Google Tasks (personal), created by Gordon; may spawn a Sancho job; never takes a project slot | outside |
| **idea** | an ICE entry with a lifecycle; the holding tank that feeds projects; **entered only by Gordon or with his approval** | `work/ice/`, `personal/ice/` |

So: a **job** (e.g. "ship the pricing plugin") has stages; a stage is done by a **skill**; a skill may request a **run** of a **command** (e.g. `git.commit`, `pipeline.sync`); the watcher executes it because it's in the allowlist; the map shows all four kinds because each has a header. Earlier sections wrote "queue job" for what is now "command" and "run"; they have been corrected.

## Decisions so far

| # | Topic | Status | Where |
|---|---|---|---|
| A | Host execution bridge | Decided: A1 queue + watcher | §1 |
| B | Layering rule (CLAUDE.md vs data vs skills vs scripts) | Decided: B1 lint; six layers, all kept by Gordon 2026-09-24 | §2 |
| C | Tree: lobes, spine, work lobe for N businesses, ownership field | Decided: C-i; entity folders; ICE per lobe; PM own folder | §3 |
| D | Indexes and navigation (cascade + search path); four-tier question | Decided: cascade + PROJECTS.md (3 per lobe, Next Action each; replaced FOCUS and WIP lists 09-26) | §4 |
| E | Provenance and verification; HUMAN VERIFIED class | Decided: E-1 | §5 |
| F | Raw vs derived; VTT placement; audio IDs; secrets location | Decided: F-1 | §6 |
| G | Write discipline; single writer per file | Decided: G-1 leases + writes by structure | §7 |
| H | Session startup; pipeline health line; lobe selection | Decided: H-1 | §8 |
| I | Skill chaining; ICE lifecycle; WIP limit; retirement line | Decided: I-1; ICE monthly + quarterly | §9 |
| J | People and speakers; corrections flow to voiceprints | Decided: three speaker states + auto bar; contacts J-D1, mirroring accepted | §10 |
| K | Sync and git feeding provenance, startup deltas, map | Decided by composition | §11 |
| L | Built-in memory boundary | Decided 09-22: not used | §12 |
| M | Pipeline design (no handoff; SQLite ledger) | Decided: M-1; Pushover for CRITICAL | §13 |
| N | Documentation, tests, living map; hooks in Cowork vs Claude Code | Decided: N-3 sequenced (MAP.md now, HTML via ICE) | §14 |
| O | Leftovers: kit follow-ups, shared skills for Astra, personal-material placement, backfill | Decided: O-1..O-4 as recommended | §15 |
| P | Devices: the phone via Dispatch; Mac sleep as a known state; power switch | Drafted 09-26; Gordon to react | §16 |
| Q | GTD alignment: clarify buckets, Weekly Review, horizons, cadence | Decided 09-26 | §17 |
| R | Sancho's character (CLAUDE.md); brief.md + watch.md at startup | Decided 09-29 | §18 |
| S | ICE at scale: files + generated views, placement as a field | Decided 09-29 (extends §9.3) | §19 |

---

## 1. Host execution bridge (Decision A: A1)

**Problem.** A Cowork session can read and write the Sancho tree but its shell is an isolated sandbox: no `~/.ssh`, no launchd, no Mac tools, no API keys. Claude Code's shell is the Mac. Sancho must run the same from either, and the pipeline, git, the map generator, and anything needing a key all have to run on the Mac.

**Design.**

```
~/Sync/Sancho/_queue/
  requests/     <- a session drops one file per job request
  results/      <- the watcher writes one file per finished job
  log/          <- watcher log, one file per day
  HEALTH.md     <- generated: watcher last seen, jobs run today, failures
```

- **Request file (a run):** Markdown with YAML frontmatter, named `<UTC timestamp>_<command>_<6 random hex>.md`. Fields: `command` (allowlisted name), `args` (map), `requested_by` (session label, e.g. `cowork` or `claude-code`), `job` (optional: the job file this run belongs to), `requested_at`. Body optional (free text for the human).
- **Result file:** same name in `results/`, frontmatter `command, status (ok|failed|refused|timeout), started_at, finished_at, exit_code, log`, body = the script's one-line summary followed by its last 40 lines of output. The request is deleted on completion (atomic rename into results, never edited in place).
- **Allowlist:** `_setup/commands.md`, a table of `command name → script path → timeout → schedule (if any) → description`. The watcher refuses any command not in the table and writes a `refused` result. **The allowlist is also the job registry the map draws from (§14.4):** the map generator reads `jobs.md` as one of its three inputs, so every job appears on the map with its script and schedule; the lint cross-checks in both directions (every script named in `jobs.md` exists and carries a header; every script whose header says `type: job` has a row in `jobs.md`, otherwise it is unreachable and the build fails; every skill whose `writes:` includes a queue request names a job that exists). One table is therefore the security boundary, the registry, and the map's source at once; adding a job is one row plus one script with a header, and `retire-component` removes the row.
- **Watcher:** `_setup/sancho-watcher.py`, Python 3 stdlib, run by launchd with `WatchPaths` on `requests/` plus a 60 s `StartInterval` fallback. Lockfile so two watchers never run. Per-job timeout. Loads secrets from `~/.config/sancho/env` (mode 600), which is *unlocked from* an encrypted copy kept in Sync (§6.5) so a replacement Mac can be working in minutes. Writes `HEALTH.md` after every run and every fallback tick, so a session can always read "watcher alive as of <time>".
- **Scheduled jobs stay scheduled.** Pipeline sync (hourly), map and index regeneration (nightly and on demand), git autocommit (daily, already built in `_setup/`). The queue adds on-demand triggers to the same scripts; it does not replace timers.
- **Session protocol:** write request → poll `results/` for up to the command's timeout → read result → report one line to Gordon. If no result and `HEALTH.md` is stale, say exactly that ("the Mac-side runner hasn't checked in since 09:14; is launchd loaded?"). Never pretend a run happened.
- **Git and Sync:** `_queue/` is gitignored (ephemeral). It lives inside Sync so one mount covers it; requests are tiny and short-lived, results are useful history. Unique names plus atomic renames keep sync.com from producing conflict copies.
- **Canonical path.** Every Mac-side execution goes through the queue from any session type, so there is one audit trail. Running a script directly from Claude Code is for developing that script, not for doing Sancho work.

**Test.** A `ping` job that writes a result containing the request ID. `_setup/test-queue.sh` submits one and waits 30 s. Startup runs it once a day and reports the round-trip time in the health line (§8).

**What this settles elsewhere:** decision #11 (the pipeline is one script on one Mac; the session triggers it through the queue instead of running it itself); #9 (commits can be requested on demand); #12 (map regeneration is a command); the personal morning routine (weather and nomad checks are commands with keys on the Mac side).

## 2. Layering rule (Decision B: B1, blocking lint)

**The rule, one page.** Where a thing lives is decided by how often it changes and whether a machine can enforce it. Six layers. Gordon approved the first four on 2026-09-24 and kept the two marked † the same day.

| Layer | Holds | Test for belonging | Never holds |
|---|---|---|---|
| **CLAUDE.md** | Identity; the must-nevers; where things live (incl. the audio folder and ID convention); a pointer to the generated skill index; the dictation line | Needed on every session; ≤ 100 lines (tokens reported by the lint). Frequency is the aspiration, not the rule: it will churn during the build and should settle to less-than-monthly once stable; the lint reports its change count per month so the settling is visible | Procedures; facts about people or clients; health or relationship details; to-dos; a hand-maintained list of skills; anything with steps |
| **Skills** | Procedures: multi-step, triggered, with a declared trigger scope (when it fires *and when it must not*), a defined end state, and a write step | Has steps a human could follow; needs judgment somewhere; carries the why/what/reads-writes/test header | Facts; rules that must never be skipped (those are hooks); guidance it goes and reads from another file |
| **Scripts, hooks, jobs** | Anything deterministic; anything that must never be skipped; anything on a timer; anything needing a key | No judgment needed, or the cost of forgetting is unacceptable | Prose instructions to the model |
| **Data files** | Facts, with provenance in frontmatter (§5) | Someone could ask "how do you know?" and the file answers with source and date | Instructions addressed to Claude (see lint note below) |
| **Generated** † | INDEX.md at every level, the system map, HEALTH.md, status views, the skill index | Produced by a script from other files; carries a `generated_by` / `generated_at` header | Edits by anyone other than the generator, ever. (In v3, a Claude session edited CAPABILITIES.md directly instead of re-running the generator, while its header still said "auto-generated"; in v2, `memory-index.json` was simply never regenerated and froze at 16 of 35 people. Gordon did neither; sessions and neglect did.) |
| **State** † | Ephemeral: queue requests and results, job plans, the ICE queue, the in-flight (WIP) file, session orientation notes | Has a lifecycle field: `created`, and either `expires` or `deleted_when` (e.g. "on ship") | Durable facts. If it's still true after the job ends, it gets promoted to a data file with provenance. |

**Cross-layer rules.**
1. A fact lives in exactly one file; other files link to it. (Enforced: the index generator flags duplicate `name:` and duplicate aliases across frontmatter, as v2's validator did.)
2. A rule that can't fire reliably doesn't exist. Before writing a rule, name the mechanism that fires it; if there is none, it's either a skill, a hook, or nothing. (v2's own line.)
3. Client *guidelines* ("Roy prefers short emails, never use exclamation marks in his copy") are facts about preferences, so they're data. The lint distinguishes described preferences from second-person imperatives to Claude ("you must always…"); only the latter are flagged in data files.

**Enforcement (B1).** `_setup/lint-layers.py` runs as the first step of every map build (§14) and blocks the build on any violation:
- CLAUDE.md over 100 lines, or containing a numbered/bulleted step sequence longer than 3 items, or containing a name from `people/` (names belong in the brief, not the kernel).
- Any data file containing second-person imperatives ("always", "never", "you must", "do not") outside a quoted block.
- Any skill missing the header or a `triggers:`/`must_not_trigger:` pair, or containing a path to a guidance file it reads instead of carrying the procedure.
- Any generated file whose content hash differs from its last generation record (hand edit).
- Any state file past `expires`, or missing a lifecycle field.
- Duplicate `name:`/alias across frontmatter.
Output is a short list: file, line, which layer it belongs in. The lint is itself a script with the standard header and a test fixture of deliberately bad files.

**Why not softer:** v3's "few rules" section grew from 6 to 16 with no mechanism; v2 reached 1,341 lines of rules across three files and nine startup definitions. Warnings were the norm in both and were ignored.

## 3. Tree, lobes, spine (Decision C: decided 2026-09-24, revised 09-26 and 09-29)

### 3.1 The spine rule
A thing lives above the fork (in the spine) if **both lobes reference it**. Everything else lives in exactly one lobe. A lobe is a default scope, not a wall: a session starts with spine + its lobe and reaches into the other on request, without ceremony.

Passes the test (spine): `CLAUDE.md`; `people/` (one identity per person; Lizzie is work, a friend is personal, Leah is both); `skills/` (the thinking skills serve both sides; lobe-only skills still live here with a `lobe:` field, so there is one skill index); the earballs pipeline and its landing zone; the queue; `_setup/`, the map, the lint; calendar access.
Fails the test (lobe): clients and businesses; meal planning; the RV; health; relationships; the nomad list; **the ICE queues** (one per lobe, Gordon's call; the ICE skill itself is spine).

### 3.2 The tree

```
~/Sync/Sancho/
  CLAUDE.md                 identity, must-nevers, where things live, dictation line, pointer to skill index
  INDEX.md                  generated: one line per top-level folder
  _design/                  build-time documents (this file); archived after Phase 4
  _setup/                   git, watcher, jobs.md, lint, map generator, tests
  _queue/                   state (gitignored): requests/ results/ log/ HEALTH.md
  _quarantine/              state: migration review queue (Phase 3)
  people/                   spine data: one file per person, all roles across both lobes
  skills/                   spine: every skill, each with lobe: work | personal | both
  recordings/               spine landing zone for pipeline output (see 3.5)
    inbox/<rec_id>/           unfiled transcripts waiting for ingest
    <YYYY>/<rec_id>/          transcripts that stay in the spine (mixed-scope recordings)
    STATUS.md                 generated from the pipeline ledger: N waiting, oldest, last run
  work/
    INDEX.md
    ice/                    work ICE queue: one file per idea, lifecycle field (decision C)
    <business>/             one folder per business, flat (C-i, decided). Clients are ALWAYS nested under their business.
      business.md             frontmatter: stake, role, status; one-paragraph identity; vision (H4)
      goals.md                H3 goals for this business (empty at scaffold)
      brands/                 copper-leaf/ only: press-managed.md (a DBA, not a business; decided 09-26)
      clients/<client>/       entity folders (3.6); a client carries brands: [press-managed] if served under that brand
      partners/<partner>/     wizard-of-ads/ only, and only where there is relationship material; the bench view is the generated partners/INDEX.md (3.8)
      stakeholders/<person>/  entity folders: co-owners and stakeholders (tipelodeon/, entomat/, american-icon-spirits/)
      projects/<slug>/        H1 projects for this business (project.md, job file, docs)
      PROJECTS.md               generated: projects with status, next action, waiting
      <other business-level folders as needed: copper-leaf/plugins/ registry>
  personal/
    INDEX.md
    ice/                    personal ICE queue, same shape as work/ice/
    me/                     identity, health, neurology: loaded ONLY on explicit request, never at startup
    rv/                     the rig: systems, maintenance, storage map
    food/                   routine 1: weekly plan, pantry, cooking-for-one journal
    nomad/                  routine 2: people-and-places list, trip log, comfort thresholds
    learning/               think-better curriculum and its sessions (via ICE)
    finances/
    recordings/             personal transcripts and summaries filed from the pipeline
    <more as routines surface>

~/Sync/Sancho-Audio/        raw audio; in sync.com, outside the repo, outside the Cowork mount
  inbox/                    new recordings (from Plaud sync or dropped by hand)
  processed/<rec_id>.ogg    kept indefinitely
  ledger.sqlite             the pipeline's internal state (decision M); generated status view lives in the tree
```

### 3.3 Work lobe: N businesses without blur (decided: C-i)

Every business folder has a `business.md` whose frontmatter carries **`stake`** (`owned` | `owned-dba` | `partial` | `partner-network` | `venture` | `client-of`) plus `role`, `status` (`active` | `dormant`), and `parent` where relevant. The generated `work/INDEX.md` prints the stake on every line, so "whose business is this" is never a matter of memory. Clients nest under the business they belong to; a client file's frontmatter repeats `business:` so a search hit is self-describing.

Today's set, as it would appear in `work/INDEX.md`:
```
copper-leaf/        owned          Copper Leaf Creative (brands: Press Managed): plugins, hosting, client sites; kit at ~/Dev/clc-plugins
wizard-of-ads/      partner-network  Gordonium is one of ~85 partners; 13 clients under clients/; partners/ with baseball cards
tipelodeon/         partial 20%    Grayson Erhard founder/owner
entomat/            venture        Lizzie Mack founder; Eti, RNA partners
american-icon-spirits/  venture     Lizzie Mack leads; brands/evel-spirits.md
pickleproof/        owned, dormant
```

- **C-i. Flat by business, stake in frontmatter (chosen).** Paths are stable; the stake is a fact and facts change (SongTipper became Tipelodeon with a different stake). Frontmatter changes without breaking a single link. The index makes the stake visible. Press Managed was briefly drawn as its own folder; corrected 2026-09-26 to a brand file under `copper-leaf/`, since it is a DBA and shares the client base.

### 3.8 Wizard of Ads partners (baseball cards dropped 2026-09-29)
Every "card" fact is a person fact, so it lives in `people/<slug>.md`: MBTI, skills, how to work with them, contact pointer, and a `woa:` block (availability as of a date; accounts they're on, with their role and Gordon's). The bench view Gordon wanted is the generated `wizard-of-ads/partners/INDEX.md`: one line per partner, name · MBTI · availability · accounts · top skills, built from those person files. A `partners/<slug>/` entity folder exists only when there is relationship material to hold (partner-meeting transcripts, a deal, notes on a shared client); otherwise the partner is a person file and an index line, nothing more.
- C-ii (grouped by class in the path) was rejected: a stake change would move a folder and break links, and WoA is a partner network containing clients. C-iii (v2's single flat `clients/` with a tag) is the layout that blurred.

### 3.6 Entity folders and the one-person rule
Clients, WoA partners, and co-owners/stakeholders are all **entity folders** on one template, differing only in `kind`:

```
<business>/<clients|partners|stakeholders>/<slug>/
  INDEX.md          generated
  entity.md         frontmatter: kind (client|partner|stakeholder), business, status, since, role (Gordon's), lead (partner), people: [slugs]; body: identity paragraph
  guidelines.md     how to work with this entity: voice, rules, preferences, what never to do
  knowledge.md      what we know; splits into knowledge/<topic>.md past ~300 lines
  transcripts/      Zoom .vtt and pipeline transcripts filed here
  summaries/        one per meeting or recording, under the template
  docs/             deliverables, drafts, agreements
```

**The one-person rule (decision #8, settled here):** a person has exactly one file, `people/<slug>.md`, holding identity, contact pointers, voiceprint link, roles across both lobes, and *how to work with this person* (their preferences travel with them). An entity folder holds what is specific to the relationship in that business: the deal, the shared clients, the venture's knowledge, the recordings. So Lizzie Mack is one file in `people/`, referenced by `entomat/stakeholders/lizzie-mack/` and `american-icon-spirits/stakeholders/lizzie-mack/`, each of which holds only what belongs to that venture. A WoA partner is one file in `people/` plus `wizard-of-ads/partners/<slug>/` for the working relationship. The index generator flags any person-shaped frontmatter (`kind: person`) outside `people/`, so identity can't fork again (v2 had four partners in two places and Leah in three files).

### 3.4 Personal facts are facts (secrecy set-aside dropped 2026-09-29)
This system is for Gordon, used by Gordon. Health, neurology, relationship and finance facts are ordinary facts: they live in `personal/me/` (or wherever they belong) because that's their *area*, and they load when a question or skill needs them, like any client file. There is no sensitive-terms lint and no rule against them appearing under `work/` when they're relevant there. Three rules remain, for reasons other than secrecy: CLAUDE.md holds identity and invariants only (layering); startup loads `brief.md` and `watch.md`, not the deeper files (context, not secrecy); and *shared business* skill bodies carry no personal content, because Astra consumes them unchanged (§15.2); Gordon's own thinking skills may.

### 3.5 The hard case: one recording, both lives
The pipeline lands every recording **once**, in `recordings/inbox/<rec_id>/` (transcript, metadata, a pointer to the audio by ID). Ingest reads it once and decides scope:
- **Single-client:** the transcript folder is *moved* (not copied) to that client's `transcripts/`, and the summary is written to its `summaries/`.
- **Personal:** moved to `personal/recordings/`, summary beside it.
- **Mixed:** the transcript stays in the spine at `recordings/<YYYY>/<rec_id>/`; each side gets its own summary, scoped to its part, linking to the transcript by ID; derived facts go to each lobe with the same `rec_id` as source.
The ledger records the final location per `rec_id`, so any session can find any recording by ID without hunting. Zoom `.vtt` files skip the inbox: the filing skill (build item 13) puts them straight into the client's `transcripts/` with a summary.

### 3.7 ICE, one queue per lobe (decision C)
Ideas are captured where they belong: `work/ice/` and `personal/ice/`, one file per idea. The ICE *procedure* (capture → interval review → MVP → evaluate → mature or kill) is one skill in the spine; the review interval is a routine entry point per lobe (§8, §9). The spine rule holds: shared procedure above the fork, lobe-specific data below it.

**Still open from §3:** anything in the personal lobe draft that's wrong (it will be shaped by the routine captures).

## 4. Indexes and navigation (Decision D: decided 2026-09-24; focus reworked 09-26 and 09-29)

**Governing principle (restated 2026-09-29):** *don't preload; find on demand.* The kickoff phrased it as "every file loaded has to earn its tokens," and the reason was never cost: it was context sprawl. A session that starts with hundreds of files is v2's two-minute startup, answers get worse as the context fills (the important line is in the middle of something long), and compaction arrives sooner, which is the erosion failure from the post-mortem. So startup loads the eight reads and nothing else, and everything deeper is reached through indexes or search. **After startup, curiosity is allowed:** browsing a client folder to build broad awareness is a legitimate purpose, and the indexes exist to make it cheap. Two ways to reach a file, and every skill says which it uses: the **cascade** (navigate by structure, for known entities: "tell me about D&M") and the **search path** (navigate by content, for retrieval: "what did Roy say about radio").

### 4.1 Frontmatter schema (every file in the tree, data and skills alike)
```yaml
---
name: D&M Heating                 # display name
type: client                      # client | partner | stakeholder | business | person | guidelines | knowledge | summary | transcript | skill | script | idea | plan | doc
description: HVAC, Wichita KS; Gordon writes radio + monthly newsletter; lead partner Semple   # ≤ 120 chars, MANDATORY, used verbatim by the parent index
lobe: work                        # work | personal | both
status: active                    # active | dormant | archived   (optional)
sources: [...]                    # provenance, §5 (data files)
---
```
`updated` is **not** a frontmatter field: the generator takes it from git (`git log -1 --format=%cs -- <file>`), falling back to file mtime for untracked files. Writers can't forget it and sync.com can't corrupt it. The lint blocks any file missing `name`, `type`, `description`, or `lobe`.

### 4.2 INDEX.md format (generated, one per folder, never hand-edited)
```
# wizard-of-ads/clients · INDEX
generated 2026-09-24 03:10 by build-index.py · 13 entries

- dm-heating/ · client · active · 2026-09-10 · HVAC, Wichita KS; Gordon writes radio + monthly newsletter; lead partner Semple
- lottoedge/ · client · active · 2026-09-02 · Lottery-odds site; newsletter program; equity note in knowledge
- …
```
One line per child (folders and files alike): name, type, status, last-updated, description. Alphabetical, so a line's position is stable. A 13-client index is ~15 lines, roughly 400 tokens. **Every lobe's top INDEX.md also carries a generated "Changed since you were last here" block** (revised 2026-09-29 from a flat "ten most recent," which was too thin): every file changed in that lobe since the last clean session close, grouped by business or area, one line each with its description, up to about 40 lines, then "+N more in <area>" counts; plus a second, shorter block of the week's changes when the session gap is short. That block is what replaces v2's hand-maintained dashboard and Hot Board, and it is what startup reads (§8).

### 4.3 The cascade and its depth budget
`CLAUDE.md` → lobe `INDEX.md` → business or area `INDEX.md` → entity `INDEX.md` → one file → (only if the file cites it and the question needs the quote) a transcript.

Rules a session follows, and a skill declares in its `reads:` header (softened 2026-09-29: these bound *startup and recursion*, not curiosity):
- Read a folder's INDEX.md before its files; after that, open what the question or the purpose warrants, including reading around to build awareness of a client or an area. What's out of bounds is the unbounded recursive read (`ls -R`, "load the lobe") and preloading at startup.
- For a specific question, `entity.md` before `guidelines.md` before `knowledge.md`, and stop when it's answered; for orientation in an area, read the index, the entity, and skim the rest.
- Prefer a summary over its transcript; open the transcript when the summary cites it and the words matter, or when the purpose is to hear the source.
- Cross-lobe reach is one extra index read, no ceremony.

Budgets by question type are **soft guidance, not limits** (decided 2026-09-29: context has grown since v2 and compaction is rare; err on too much and pare down on evidence). They describe the shortest path that usually answers, so a session knows where to start, not where it must stop:
| Question | Path | Budget |
|---|---|---|
| Orientation (startup) | CLAUDE.md, lobe INDEX (with Recently changed), `recordings/STATUS.md`, `_queue/HEALTH.md` | 4 files |
| "Tell me about X" | cascade to X's INDEX, `entity.md`, `guidelines.md`; `knowledge.md` only for depth | 3–5 files |
| "Brief me for the meeting" | brief-me's declared list (entity, guidelines, last 3 summaries, people files of attendees) | ≤ 8 files |
| "What did X say about Y" | search path; read hit sections; a transcript only if the summary doesn't answer | 1–3 files, sections only |
| Anything else | start from the lobe INDEX; if a third index doesn't locate it, switch to search | ≤ 4 index reads before search |

### 4.4 The search path
Ripgrep over Markdown, scoped to spine + current lobe by default, both lobes on request. Available directly from a Cowork session (the Grep tool is ripgrep) and from Claude Code; no Mac-side job needed. Results are read as **sections** (the heading containing the hit), not whole files. Queries name the scope in the report ("searched work + spine, 14 hits in 6 files"). Transcripts are included in search but summaries rank first: the search skill reports summary hits before transcript hits. If ripgrep ever proves slow (v2 searched 3,000 files with it without complaint; v3 kept an FTS5 index as well), an FTS index job becomes an ICE item, not a day-one build.

### 4.5 How the two divide the work
Cascade answers *what is / who is / where do things stand*. Search answers *what was said / when / find me*. The rule of thumb for a session: if you can name the entity, cascade; if you can only name the words, search. Skills declare one or both.

### 4.6 The four-tier model, resolved (decided 2026-09-24)
Gordon's May 2026 model had four tiers: global kernel, environmental kernel, chunky Work/Personal modes, fine-grained files. Resolution: tier 1 = CLAUDE.md; tier 2 collapses into CLAUDE.md's "where things live" (one machine); tier 3 is replaced by the lobe INDEX.md's generated "Recently changed" block **plus one hand-managed `FOCUS.md` per lobe**; tier 4 = files on demand via the cascade. Rejected: scattered `status: focus` flags in individual files (no count, they accumulate) and a free-form mode page (v2's Hot Board).

**Projects and Focus (settled 2026-09-26, replacing the earlier FOCUS.md / IN-FLIGHT.md / capped-ENDEAVORS drafts).**

*Projects are unlimited.* Each business has as many as it has projects; personal life too. A project is a folder (`work/<business>/projects/<slug>/` or `personal/projects/<slug>/`) with `project.md` (frontmatter: name, lobe, business, status active|parked|done, wrike_project if any, **next_action** with its date, description), a job file (§9.2) once it's in motion, and whatever docs it accrues. The generated `PROJECTS.md` at each lobe root lists them all with status and next action. ICE feeds them: an approved idea becomes a stage in an existing project or a new project file. Next Actions are tasks: personal ones are Google Tasks items, work ones are Wrike tasks under the matching Wrike project; Gordon creates them; the project file carries the text and the date it was set. **Startup flags any active project with no Next Action, and any Next Action unchanged for 7 days.**

*Focus is capped: three per lobe per horizon, nested.* `FOCUS.md` in the spine, hand-set with Gordon, never generated:
```
# FOCUS
## month · 2026-10          (set at the monthly ICE review, 1st business day)
work:     plugin-library overhaul · D&M Q4 flight · Tipelodeon pricing
personal: Alaska trip · food routine · think-better term 1
## week · 2026-10-05        (set Sunday for personal, Monday for work)
work:     tag audit done · D&M scripts to Roy · pricing tiers drafted
personal: route Moab→Salt Lake with 2 visits · Sunday session #2 · think-better session 3
## today · 2026-10-07       (set in the morning routine; rolls forward if skipped)
work:     run kit.tag-audit · send D&M scripts ·  (3rd left open)
personal: call Paige about the visit · cook plan dinner #2 · session 3, 60 min
exceptions this week: 1 (Tue: emergency Society Hill fix, not on any list)
```
Rules: three lines per lobe per horizon, lint-enforced; a horizon's items must trace up (a day item belongs to a week item, a week item to a month item) or be logged as an **exception** with one word of why. Exceptions are allowed and counted, never blocked: the count is the signal at the next review that the month's focus was wrong. Each lobe INDEX.md prints its own column of FOCUS at the very top, so startup reads it first. Nothing else in the tree may claim focus.

*The daily checksum (feasibility).* The morning routine (§8.5) does one exchange: "This month: A, B, C. This week: X, Y, Z. What are today's three?" Gordon answers, often "same as yesterday" or "X, Y, and an exception: Society Hill." That is recognition, not recall, which is the cheap direction for him (post-mortem Q5); it costs under a minute and touches nine lines per lobe. The cost that could kill it is ritual creep, so: skipping a day is allowed and the day block just rolls forward with a "(rolled)" mark; the week block is set once (Sunday personal, Monday work) and the month block once; none of the three is ever set by Sancho alone.

**Project vs task.** A task is one action or a short sequence done in a sitting or two ("update the pricing plugin's help text", "buy a backpack"); it lives in Wrike or Google Tasks, Gordon creates it, and Sancho may help do it (even spawning a short job) without it touching the project list. The test, in order: Would it be finished in one or two sittings? Task. Does it need a sequence of decisions over weeks, with stages you'd want to survive a crash? Project or at least a job. Is it already on Gordon's task list? Task. Would he be sorry in a year if it never happened? Project. When the answer isn't obvious, Sancho asks rather than guessing; slots are precious, tasks are plentiful. The Next Action of a project is itself a task, and Gordon mirrors it into his task manager himself (decision 2026-09-21).

## 5. Provenance and verification (Decision E: E-1, decided 2026-09-24)

**The promise:** Sancho can answer "how do you know that?" with a source and a date, every time, and says "unconfirmed" out loud rather than sounding sure. (Post-mortem Q4: trust is the product.)

### 5.1 Source atoms
Every fact cites one or more of these, in a fixed compact grammar so the lint and the search path can parse them:

| Atom | Means | Example |
|---|---|---|
| `rec_<id>` | a pipeline recording (transcript on disk, audio by ID) | `[rec_7f0ac58436 2026-09-10]` |
| `vtt:<file>` | a Zoom transcript filed in an entity folder | `[vtt:2026-09-12_dm-heating-weekly 2026-09-12]` |
| `gordon` | Gordon said it in a session, dictated or typed | `[gordon 2026-09-24]` |
| `doc:<path>` | a document in the tree (agreement, brief, email saved as file) | `[doc:entomat/docs/operating-agreement.md]` |
| `web:<url>` | a web page, with the date fetched | `[web:example.com/about 2026-09-24]` |
| `derived:<path>` | inferred from another Sancho file (never from another inference without saying so) | `[derived:people/lizzie-mack.md]` |
| `v2:<path>` / `v3:<path>` | migrated from an old system, through the Phase 3 gate | `[v2:work/clients/dm-heating.md 2026-04-15]` |

### 5.2 Trust tiers (four, not five)
| Tier | What it is | Who made it | Written as |
|---|---|---|---|
| **raw** | transcript text as produced; audio | machine | the transcript file itself; never edited |
| **derived** | a summary, extraction, or inference made by Claude from raw or from other files | machine, with a confidence where one exists | `[rec_x date]`, `[derived:…]`; speaker matches carry `sim=0.93 refs=12` |
| **stated** | Gordon said it, first-hand, in a session. **Counts as verified by default** (decided 2026-09-24); if it sounds dubious the session double-checks with him or runs `fact-check` before filing | human | `[gordon date]` (kept distinct from `confirmed` so document-backed facts stay tellable apart) |
| **confirmed** | Gordon confirmed a specific derived or stated fact when asked, or a document backs it | human | append `[confirmed gordon date]` or `[confirmed doc:… date]` |

**HUMAN VERIFIED is its own class (Q9 #7):** `confirmed` can only be written by a session recording a human act, never by a script or a similarity score. Any machine check records what did it and its score (`verified_by: voiceprint sim=0.93`); a score of 1.000 is still `derived`. Quarantined v2/v3 material carries no tier until it passes the gate, and lives in `_quarantine/`, not the tree.

### 5.3 Where provenance lives (decided: E-1)
- **E-1. Per-fact inline cites plus a per-file `sources:` list (chosen).** Each factual sentence or bullet ends with its cite; the file's frontmatter lists every source used, so an index or search can find "everything from rec_x" without parsing bodies. This is what v2 did in its people files (73% coverage) and it worked; the gap was that nothing enforced it. Cost: writers must cite every line; the lint flags a data file whose body has uncited bullets.
- **E-2. Per-file provenance only.** Frontmatter `sources:` and nothing inline. Lighter to write; "how do you know" answers with a file, not a line, and a knowledge file with 30 sources can't say which line came from where.
- **E-3. Facts as atoms in a sidecar ledger.** Every fact a row in a separate file with source, tier, date; the Markdown is rendered from it. Cleanest provenance, heaviest machinery; v2 planned "atoms" and never built them.

### 5.4 Corrections and supersession (Q9 #6: no silent overwrite)
A fact is never edited in place. A correction appends a new line with its own cite and marks the old one: `~~Roy's station is KFDI~~ [superseded 2026-09-24 by rec_…]`. Once a file accumulates more than ten superseded lines, a housekeeping step moves them to a `history` section at the bottom, never deletes them. The search path returns superseded lines flagged as such. attribution-correction (Phase 3) follows this rule across every file the original ingest touched, using the `sources:` lists to find them, and writes the correction back to the speaker record (§10) so the voiceprint library learns too.

### 5.5 Ephemeral vs durable
A fact that stops being true on a date ("Roy is traveling until Oct 1") is ephemeral and belongs in state (a summary's open-items section, a job plan), not in `knowledge.md`. If it must be written to a data file it carries `[until 2026-10-01]`, and the lint lists expired facts on every map build so they get superseded or removed. Durable facts carry no expiry.

### 5.6 How git feeds provenance (decision K, part; revised 2026-09-29)
Commits are hourly (the existing launchd autocommit) plus one at each conversation close. `git log -S "<phrase>" -- <file>` answers *when* a fact entered to the hour; the commit message lists the sessions live in that hour (from the leases), and the session note and receipts carry the per-action trail. That's enough: the inline cite on the fact itself (§5.1) is the primary provenance; git is the tamper-evident timeline behind it.

## 6. Raw vs derived (Decision F: F-1, decided 2026-09-24; transcripts and VTTs in git)

**Already decided (kickoff):** raw audio lives in `~/Sync/Sancho-Audio/`, inside sync.com, outside the Cowork mount, outside git, kept indefinitely. The tree holds the transcript, the summary, and a recording ID. Secrets live in `~/.config/sancho/env`, never under `~/Sync/` (§1).

### 6.1 Recording ID convention (goes in CLAUDE.md's "where things live")
`rec_` + 10 lowercase hex, unchanged from v2/v3 so migrated recordings keep their IDs. Audio: `~/Sync/Sancho-Audio/processed/<rec_id>.ogg` (originals never overwritten; a silence-stripped derivative, if made, is `<rec_id>.stripped.ogg`). Anything in the tree that mentions a recording uses the ID; the ledger maps ID → recorded-at, duration, current transcript location. Zoom VTTs are not recordings; their atom is the filename `YYYY-MM-DD_<entity>_<topic>.vtt`.

### 6.2 What is raw, what is derived
| Artifact | Class | Lives | In git? |
|---|---|---|---|
| audio (`.ogg`, `.m4a`) | raw | `Sancho-Audio/processed/` | never |
| `transcript.md` (pipeline) | raw (immutable) | tree, per §3.5 | **yes (F-1)** |
| `transcript.json` (word timings, diarization segments) | raw sidecar, large (up to 2 MB) | `Sancho-Audio/processed/<rec_id>.json` | never |
| Zoom `.vtt` | raw (immutable, and *not re-derivable*: Zoom is the only source) | entity `transcripts/` | **yes (F-1)** |
| `speakers.md` per recording (cluster → person, machine score, human confirmation) | derived + confirmed | beside the transcript | yes |
| summaries | derived | entity `summaries/` or `personal/recordings/` | yes |
| knowledge, guidelines, people | derived / stated / confirmed | tree | yes |
| ledger (`ledger.sqlite`) | state | `Sancho-Audio/` | never; generated `recordings/STATUS.md` is in git |

### 6.3 Git treatment of transcripts and VTTs (DECIDED 2026-09-24: F-1, in the repo)
**Decision:** pipeline transcripts and Zoom VTTs live in the tree and in git; word-timing JSON and audio stay out. The options as weighed:
Sizes: a one-hour transcript is 50–150 KB of Markdown; v2's 696 transcripts total ~70 MB without the JSON sidecars. At Gordon's recording rate (~100 recordings/month at peak) the repo grows roughly 100–200 MB a year from transcripts alone. The pre-commit hook's 5 MB per-file cap is never hit by a transcript.
- **F-1. Transcripts and VTTs in the repo (recommended).** Text, immutable, and the thing every cite points at; git history then proves a transcript never changed after ingest, which is the strongest provenance available. VTTs especially: they can't be regenerated, so git plus sync.com plus GitHub is the right number of copies. Cost: repo size grows by a few hundred MB a year; clones get slower over years (mitigable later with shallow clones or moving old years to an archive repo).
- **F-2. Transcripts in the tree but gitignored.** Present on disk and in sync.com, absent from git history. Repo stays small. Cost: no tamper evidence for the raw layer, and a VTT deleted by mistake is gone unless sync.com's version history catches it.
- **F-3. Transcripts beside the audio in `Sancho-Audio/`, tree holds summary plus pointer.** Cleanest separation; cost: violates the requirement that a client's transcripts live in the client's folder, and the cascade would have to leave the mounted tree to read one.

### 6.5 Secrets: redundancy without plaintext (revised 2026-09-29)
Gordon's requirement: if the laptop goes in the pool, a new Mac plus sync.com should be back at work without re-authenticating everything. Sync is a backup, not a leak. That's right, with one adjustment, because the Sync folder isn't only the cloud: it is also a plaintext copy on Leah's machine, and anything a session or a script can read there is exposed if that machine is lost or compromised. The middle path:
- `~/Sync/Sancho-Secrets/sancho.env.age`: every credential Sancho needs (Groq, Plaud bearer, Hugging Face, Pushover, GitHub deploy key, anything later), **encrypted at rest with `age`** to a passphrase Gordon knows (or, if he prefers, to a key held in 1Password/Keychain). Sync mirrors it everywhere; nobody without the passphrase can read it, including Leah's machine and sync.com.
- `~/.config/sancho/env` on the Mac: the decrypted working copy, mode 600, created by the command `sancho.unlock` (asks for the passphrase once, writes the file, done). Every script reads from here.
- `sancho.lock-secrets` re-encrypts after any change, so the Sync copy is always current; the lint fails the build if the plaintext is newer than the encrypted file.
- **Recovery runbook** (`_setup/RECOVERY.md`, written in Phase 4): new Mac → install sync.com, sign in → wait for `Sancho/`, `Sancho-Audio/`, `Sancho-Secrets/` → clone `~/.sancho.git` from GitHub → run `_setup/install-mac.sh` (launchd jobs, venv, watcher) → `sancho.unlock` → open Cowork. Target: under an hour, most of it sync time.
- Never in git, never in the knowledge tree, never in a state file (v3 wrote the Plaud token into `auth-state.json`).
Is plaintext in Sync too laissez-faire? For the cloud copy, sync.com's zero-knowledge encryption makes it tolerable; for Leah's machine, it isn't, and the `age` step costs one passphrase prompt per new machine. If Gordon would rather accept the Leah's-machine exposure and skip encryption, the design degrades gracefully to a plain `sancho.env` in the same folder; the runbook is identical minus one step.

### 6.6 Sancho-Private (added 2026-09-30)
`~/Sancho-Private/`: a folder **outside Sync**, in its own small git repo with its own private GitHub remote, for material that must not leave Gordon's machines. Why its own repo rather than a corner of the main one: a folder outside `~/Sync/Sancho` can't be part of that worktree, and a separate repo keeps the content out of the main repo's history, which Leah may one day be given read access to for shared business skills. Same conventions as the tree (frontmatter, cites, indexes), same hourly autocommit script pointed at a second repo, encrypted secrets unchanged. Mounted in Cowork on request only ("open private"); the main tree never links into it, and the lint flags any path that does. Startup does not read it.

### 6.4 Size limits
Per file: the existing 5 MB pre-commit cap stands. Per recording: nothing; a nine-hour ambient recording is kept as audio and transcribed once (v2 quarantined one such file; Sancho just processes it and lets the summary be short). Repo: review at 2 GB; the likely move then is one archive repo per past year.

## 7. Write discipline (Decision G: decided 2026-09-24; G-1 leases)

**The constraint (kickoff):** nothing important survives only in context. Structure makes writes happen by default; write-it-down is the backstop.

### 7.1 Writes by structure, not by nagging
1. **Every skill ends with a write step.** The skill header declares `writes:`; the lint rejects a skill with no write step or with a write step that isn't last. A thinking skill (think-first, triz) writes its output to the entity or project it was about, or to the session note if nothing else fits. **No skill writes to ICE on its own** (decided 2026-09-29): if a skill or an ingest pass surfaces something that looks like an idea, it *proposes* it ("want this in ICE?") and writes it only on Gordon's yes. Every ICE entry comes from Gordon or is approved by him.
2. **Decisions land in a log at the level they were made.** `decisions.md` in the entity folder for client-level calls, `decisions.md` at the business level, `work/decisions.md` or `personal/decisions.md` for cross-cutting. One line each: date, decision, reason, source. Sancho's own build log is `_design/decisions.md` until Phase 4 ends, then `_setup/decisions.md`.
3. **Checkpoint writes during the conversation.** The moment a fact is confirmed, a decision made, or a correction given, the session writes it, then replies. It says what it wrote in one line ("logged to dm-heating/decisions.md"). Session end is not the write moment; it may never come.
4. **Session notes as compaction insurance.** `_queue/sessions/<session-id>.md` (state, lifecycle: deleted on clean session end after commit) holds a running list of what this session has written and what is open. If compaction or a crash hits, the next session reads it in orientation (§8) and nothing is lost that was already on disk; anything not yet written was never real.
5. **Write receipts.** Every skill's final message ends with one line naming the files it wrote; every checkpoint names its file. Compact by rule (paths only, no prose), because Gordon expects this may prove tedious and agreed to try it; if it does, the receipt collapses to a count with the paths in the session note.
6. **Commits: hourly plus session close** (corrected 2026-09-29; the earlier "per action" was too many). The launchd autocommit already built in `_setup/` runs every hour and at login; the conversation close (§8.7) requests one more through the queue. That's it. Per-action attribution comes from the session note and receipts, not from git; the hourly commit message lists the sessions that were live (from the leases) so `git log` still says who was working when.
7. **write-it-down is a reflex, not a phrase.** Gordon should never have to say "write that down" (decided 2026-09-29). The backstop is a self-check the session runs at every checkpoint and before every reply: *did anything just get decided, stated, corrected, or asked that isn't on disk?* If yes, write it, cite it `[gordon date]`, name the file. The phrase still works as an emergency override, but the design is judged by how rarely it's needed; if Gordon finds himself saying it, that's a bug in the skill that should have written, and it's logged as one.

### 7.2 Single writer per file (decided: G-1)
v2's 77% loss was three *machines* writing one tree through git auto-merge, and Sancho already prevents that structurally (one writer machine, git outside Sync). Conversation-to-conversation conflict on one Mac is a much smaller risk, so leases are justified only if they're cheap, and they are: one small file per conversation, written at open, removed at close. Their main value now isn't conflict prevention; it's the **"left open" detection** that makes one-conversation-per-topic safe: the next open sees a stale lease, reads its note, and reports what was left. Gordon (2026-09-29): keep them if cheap. They are.
- **G-1. Session leases (chosen; scope narrowed 2026-09-29).** At open a conversation writes `_queue/leases/<session-id>.md` with its lobe, its **topic scope** (the projects or entities it declared, §8.7), and its start time. A second conversation that names a project another live conversation holds is told so and asked whether to continue there or take over; conversations on different projects in the same lobe coexist silently, which is what one-conversation-per-topic needs. A lease goes stale after 2 h without a checkpoint write and the watcher expires it. Cheap, visible, and it makes the two-windows-on-one-thing mistake loud instead of silent.
- **G-2. No mechanism.** Rely on one machine and habit. It is what v3 did ("single-writer files") and it held only because nothing else was running.
- **G-3. Git branches per session.** Real isolation; cost: merges inside a sync.com folder, the exact thing that produced conflict copies before.
Daemons never write into the knowledge tree except the pipeline's landing zone and generated files; the lint flags any generated file written by anything other than its generator. Leah's machine mirrors Sancho but nothing on it writes into it (Astra has its own workspace); that is a rule in CLAUDE.md, and sync.com's conflict-copy pattern (`*-CONFLICT-*`) is a lint check so a violation shows up on the next map build.

## 8. Session startup (Decision H: decided 2026-09-24; H-1 offer once)

**Goal:** orientation, not a ritual. Under 30 seconds, four generated files, one screen of output, then Gordon's question. The morning routines are separate skills with their own entry points; startup only knows whether they've run today.

### 8.1 Trigger and lobe
"Hey Sancho" (any Sancho greeting) → personal lobe. "Hey Sancho, let's work" (any greeting plus "work") → work lobe. Switching lobes mid-session is one sentence ("switch to work"), which re-runs the lobe part of orientation only.

### 8.2 What it reads: the morning packet (widened 2026-09-29)
1. `date` from the shell, mechanically (v2 got the weekday wrong from memory).
2. CLAUDE.md (auto-loaded).
3. `personal/me/brief.md` and `personal/me/watch.md` (§18).
4. The lobe's `INDEX.md`: FOCUS block first, then "Changed since you were last here."
5. The lobe's `PROJECTS.md`: active projects with next action and waiting-for.
6. `recordings/STATUS.md`: the pipeline health line.
7. `_queue/HEALTH.md`: watcher last seen; leases; any session note left by a session that didn't close cleanly.
8. A git delta: commits since the last clean session end for this lobe, summarized by area.
9. The `project.md` of each project in today's focus, so the session starts already inside the work.
What it still doesn't do: inbox scans, calendar reads, meeting briefs, cadence dispatch, network checks. The morning routine owns the calendar, the pipeline owns its own alerts, and every-turn checks don't exist. The packet is bigger than the first draft on purpose: Gordon would rather pare down an informed session than start with a thin one. If compaction starts appearing in session notes, the packet is the first thing to trim, from the bottom of this list up.

### 8.3 What it says (revised 2026-09-29: the same facts, spoken, not a status dump)
The first draft was a field list, and Gordon called it sterile. The facts stay mandatory (date and time, lobe, today's three with next actions, pipeline and watcher state, what changed, anything left open, whether the routine has run); the rendering is a short paragraph in Sancho's own voice, under eight lines, warm through specificity rather than adjectives. Two examples, one good morning and one with a problem:

> Tuesday, September 29, 8:40 in Moab. Three things on your plate: the Alaska route (next: call Paige about the visit), Sunday's cook plan, and think-better session 3. The pipeline caught up overnight; two recordings from yesterday are waiting for you. Nothing's changed since Sunday except your food notes. Morning routine, or straight in?

> Tuesday, 8:40, and a heads-up first: the Plaud token expired last night, so nothing new has come in since Sunday; it needs re-capturing next time you're at the Mac. Otherwise: Alaska route (next: call Paige), the cook plan, session 3. Sunday's food notes are the only thing that moved. Routine, or straight in?

Rules for the rendering: lead with the date and place (the temporal check, spoken); a problem goes first, once, with what to do, **never with a time estimate** ("five minutes to…" is usually wrong and reads as forced; say what, not how long); today's three read like a list a person would say aloud, each with its next action; the change line names what actually changed, not a count of files, unless it's a lot; the last line is the routine offer or the topic question, never both. Every fact is a read of a generated file; none is composed from memory, and a stale file is said plainly ("the pipeline status is three days old, so I don't know where it stands"). No "Focus (3/5)", no "watcher ok (09:14)", no bullets: that's the map's job, not the greeting's.

### 8.4 Cold start vs. re-sync
Same six reads. The only difference is the size of the git delta and whether a dirty session note exists. Designing two startup paths was one of v2's nine definitions; Sancho has one.

### 8.5 Handing off to the morning routine (decided: H-1)
Each lobe has a morning routine skill (build items 10 and 11). Startup knows whether it has run today from a state line the routine writes (`_queue/routines/<lobe>-morning-<date>.md`, lifecycle: 1 day).
- **H-1. Offer, then nudge (chosen; persistence added 2026-09-29).** If the routine hasn't run today and it's before noon, the last line of the first open is the offer ("Run the morning routine?"). If it's declined or ignored, the next open that morning carries a one-word nudge on the greeting line ("routine: not yet"); after that, silence for the day. Point it out once, remind once, no third time (decided 2026-09-30).
- **H-2. Run it automatically** if not yet run today. Saves one exchange; it is also exactly how v2's startup grew a 20-step chain, and an afternoon re-sync would still trigger a "morning" routine unless guarded.
- **H-3. Never offer.** Gordon asks for it by name. Cleanest, and the habit he wants to build then depends entirely on him remembering, which is the thing the system exists to carry.

### 8.7 Opening and closing a conversation (added 2026-09-29; one conversation per topic is the aim)
Three things were tangled under "startup": the **morning** (first conversation of the day in a lobe), the **morning routine** (a skill, offered once), and **opening a conversation**, which happens many times a day and must cost almost nothing. Separated:

**Open (every conversation).** The packet in 8.2 loads either way, since it's cheap and it's what makes the session informed. **The first act of every open is the temporal check:** one shell call for weekday, date, local time and timezone, compared against the Mac's clock in `HEALTH.md` (the sandbox and the Mac can disagree on timezone, and the RV crosses zones; `personal/nomad/location.md` carries the current zone). Never from memory: v2 got the weekday wrong. The *output* differs: if this lobe has already had a conversation today, the greeting is two lines, not eight:
> 3:10, work. The tag audit and the D&M scripts are still on today's list; nothing's moved since 1:42. What's this one about?

(Same rules as 8.3: the temporal check spoken, today's remaining items, what changed, the topic question. A problem, if any, goes first.)
The answer to "what's this one about?" is the conversation's **topic**, and it does three things: it names the session note (`_queue/sessions/<date>_<topic>_<id>.md`), it loads the matching project or entity files if the topic names one ("D&M radio" opens the D&M folder and its job file), and it sets the conversation's **lease scope** (below). If Gordon opens with the topic already in the message ("Hey Sancho, let's work on the D&M radio scripts"), the question is skipped. If the first conversation of the day, the eight-line orientation plus the routine offer (8.3, 8.5) come first.

**Concurrent conversations.** One conversation per topic means several may be open at once in the same lobe, so the lease from §7.2 is scoped to the **projects or entities a conversation declares**, not to the whole lobe. Two conversations on different projects coexist silently; a second conversation that names a project another live conversation holds gets told ("the D&M radio conversation from 1:42 is still open; continue there, or take it over?"). Cross-cutting files (the lobe's decisions.md, FOCUS.md) are append-only or single-line edits, so they tolerate two writers; the lint's conflict-copy check is the backstop.

**Close (when Gordon says he's done, or a conversation goes quiet).** "Thanks, Sancho" / "done" / "that's it for this one": write the receipt (files written, decisions logged, next action if the topic was a project), fold the session note into the project's history or the lobe's day log, release the lease, request a commit. Two lines back: "Logged 3 files and 1 decision to dm-heating; next action: send scripts to Roy. Closed." A conversation that just stops gets closed by the next conversation that finds its stale lease (2 h), which reads the note and reports "the D&M conversation from 1:42 was left open; its note says…". Nothing is lost either way, because everything that mattered was written at the checkpoint, not at the close.

**What else an open might want (candidates, not built):** a one-line "since your last conversation" from the git delta (already in the packet); the day's calendar next event (belongs to the morning routine, not the open); a nudge if today's three haven't been set (only at the first open of the day).

### 8.6 Test
A fixture tree with known files; running startup against it must produce a greeting under eight lines that contains every mandatory fact with the expected values (the test checks facts, not wording), in under 30 s, reading only the packet in 8.2 (the test records every path opened). The packet informs the session; the greeting informs Gordon.

## 9. Skill chaining, ICE, WIP, retirement (Decision I: decided 2026-09-24; I-1 job files; ICE monthly/quarterly)

### 9.1 The skill header (every skill, enforced by the lint)
```yaml
---
name: earballs-ingest
type: skill
lobe: both                      # work | personal | both
description: Files a processed recording's facts to the right places, with speaker confirmation first
why: Recordings are the main capture channel; unfiled recordings are lost knowledge
triggers: ["ingest", "process recordings", startup shows recordings waiting and Gordon says go]
must_not_trigger: [any mention of a recording in passing; a request to search transcripts]
reads: [recordings/inbox/<rec_id>/, people/, the target entity's INDEX.md]
writes: [entity summaries/, knowledge.md, people/, decisions.md; then a commit request]
chain: {front: think-first?no, next: attribution-correction on a correction, gate: human before filing}
test: _setup/tests/skills/earballs-ingest/ (fixture recording → expected files)
---
```
Procedure lives inside the skill; no `routines/*.md` it goes and reads. The last step is always a write plus a receipt.

### 9.2 The chain pattern: a job is a state machine on disk
Multi-step work never lives in conversation. Starting a chain creates a **job file**, and every skill in the chain reads it, does one stage, writes its outputs, advances the stage, and hands back.

```yaml
# _queue/jobs/2026-09-24_dm-heating-q4-radio_a3f2.md      (state; lifecycle: archived on close)
job: dm-heating-q4-radio
lobe: work
entity: work/wizard-of-ads/clients/dm-heating/
created: 2026-09-24T15:02Z   by: cowork
stages:
  - {name: frame,     skill: think-first,          status: done,    out: docs/q4-radio-brief.md}
  - {name: approve,   gate: human,                 status: done,    at: 2026-09-24T15:40Z}
  - {name: draft,     skill: persuasive-argument,  status: active,  out: docs/q4-radio-v1.md}
  - {name: review,    skill: critical-thinking,    status: pending, repeat_until: "no FAIL", max: 3}
  - {name: file,      skill: write-it-down,        status: pending}
current: draft
```
Rules: **state passes only through the job file and written files**, never through what a skill "remembers." A loop is a stage with `repeat_until` *and* `max`; the lint rejects a loop without both. Human gates are stages that stop; the job simply waits, for hours or days, and orientation lists it under "left open." A crashed session costs nothing: the next one resumes at `current`. On close the job file is archived to `_queue/jobs/_archive/YYYY-MM/` (the kit's "plan created on approval, deleted on ship" becomes "archived on ship," since the no-data-loss rule outranks tidiness). The Copper Leaf plugin job is the same pattern with the kit's 16 stages (survey §1); Sancho holds that job file, the kit does the work.

**think-first is the front of the chain, not a tax on every request.** It fires when a chain starts (building, deciding, planning with stakes), and not on questions, lookups, single edits, or follow-ups inside an approved job. Its output is the job's first stage.

### 9.3 ICE lifecycle
One file per idea in `work/ice/` or `personal/ice/`:
```yaml
id: ice-2026-09-24-ivy-league
title: Think Better / Ivy League curriculum, session-based delivery
lobe: personal
captured: 2026-09-24   source: "[gordon 2026-09-22]; seed v2:personal/think-better.md"
status: captured        # captured → reviewed → approved-mvp | parked | killed → mvp-in-use → evaluated → mature | killed
next_review: 2026-10-08
log:
  - 2026-09-24 captured
```
Review has two gears (decided 2026-09-24): a **monthly quick review** of every open idea in the lobe (approve for MVP, park, kill; two minutes each) and a **quarterly deep dive** that also re-examines parked ideas, MVPs in use, and the killed list for patterns. Both are offered the way the morning routine is offered (§8.5): when the lobe's review is due, the morning routine adds one line ("work ICE monthly review due, 7 ideas") and the ICE skill runs on request, one idea at a time. Approve for MVP requires a free WIP slot; park sets the next review; kill logs a reason and moves the file to `ice/_killed/`, never deletes. An approved MVP gets a job file (§9.2); "evaluated" asks the four questions Gordon named: did I use it, was it useful, how did it fail, build it maturely or kill it.

### 9.4 The WIP limit (folded into projects, 2026-09-26)
The project list (§4.6) is the limit: three per lobe. During Phase 4, "Build Sancho" is one work project, and Gordon's WIP-3 rule applies *inside* it: its job file lists at most three components maturing at once, with what "mature and habitual" means for each; the scaffold exemption (decisions.md 2026-09-24) is a dated line in that job file and expires when the scaffold batch closes. The lint enforces the project cap; the build-sancho job file enforces its own three. `IN-FLIGHT.md` is not built.

### 9.5 The retirement line
Retiring is a procedure with a check, never a sentence in a doc ("retired in prose, still running" was v2's pattern for a mesh, an orchestrator, a database and two skills). `retire-component` is a command that: (1) removes the component from `_setup/commands.md` / the skill index / launchd (`launchctl bootout`) as applicable; (2) moves its files to `_setup/retired/<date>-<name>/`; (3) greps the tree for its name and lists every remaining reference; (4) appends a decisions line; (5) regenerates the map, which now shows it under "retired" for 90 days. The lint flags any live reference to a retired name. A component isn't retired until the job's result says zero references.

### 9.6 Where chain state lives (decided: I-1)
- **I-1. One job file per chain in `_queue/jobs/` (chosen).** As drawn above. Every open piece of multi-step work is visible in one folder; orientation lists them; a crash resumes from `current`. Cost: one more file type, and skills must read and write it (the lint checks that chain-capable skills declare `chain:`).
- **I-2. Stage status inside the target entity's files** (frontmatter on `docs/q4-radio-brief.md`, say). Fewer files; but work that spans entities (a recording that touches three clients) has no single home, and "what's open?" means scanning the tree.
- **I-3. Chain state in conversation, summarized at the end.** Rejected: this is the compaction failure by design.

## 10. People and speakers (Decision J: decided 2026-09-24; contacts J-D1; cards dropped 09-29)

**Rule:** one identity per person, everywhere: the tree, both lobes, the voiceprint library, the transcripts. The slug in `people/<slug>.md` is that identity; every other place refers to it by slug.

### 10.1 The person file
```yaml
---
name: Lizzie Mack
aliases: [Elizabeth Mack, Lizzie]
type: person
lobe: both
description: Founder and leader of Entomat; also leads American Icon Spirits (brand: Evel Spirits)
roles:
  - {context: work/entomat, role: founder, since: 2025}
  - {context: work/american-icon-spirits, role: lead}
location: {city: Austin TX, as_of: 2026-09-10, source: "rec_…"}      # for the nomad routine
last_seen: 2026-09-10     want_to_see_by: 2026-12-01                 # nomad people-and-places
voiceprint: {enrolled: true, refs: 11, last_enrolled: 2026-08-02, from: [rec_…, rec_…]}
sources: [...]
---
## How to work with her        (preferences travel with the person)
## What we know                (cited facts, E-1)
## Open threads
```
Facts about the *relationship in a business* go in that business's entity folder (§3.6); the person file holds the person. The index generator flags a `type: person` file anywhere but `people/`.

### 10.2 Speaker identity in the pipeline
- The voiceprint library is keyed by people slug. Enrolling a voice means: a human confirmed that cluster N in recording R is person P; that (R, N, P, who, when) record is written to the recording's `speakers.md` **and** the library is rebuilt from those records. The library is derived; the records are the truth. This fixes v3's un-enroll problem (matching by cosine 0.999 against a centroid that changes on reprocess).
- Per recording, beside the transcript:
  ```
  # speakers · rec_7f0ac58436
  | cluster | candidate (machine) | confirmed | by | when | note |
  | SPEAKER_00 | gordon sim=0.97 refs=232 | gordon | auto-solo rule | 2026-09-10 | single-cluster recording, voiceprint ≥0.90 |
  | SPEAKER_01 | roy-williams sim=0.84 refs=12 | roy-williams | gordon | 2026-09-11 | |
  | SPEAKER_02 | none ≥0.70 | unknown-02 | | | vendor; ignored 2026-09-11 (reason: one-off call) |
  ```
  The transcript body is never rewritten (raw, immutable). Summaries use a name only when the row says confirmed; otherwise "Speaker 2 (likely Roy, unconfirmed)". A cluster with no candidate is `unknown-NN` until named; a person who should never be enrolled (vendors, one-offs) is marked ignored with a reason, and the ignore is sticky against auto-tag (v3's spec, now built).
- **The library earns automation (decided 2026-09-24).** Three speaker states, each written in `speakers.md` and carried into cites:
  1. **candidate**: a machine match below the auto bar; summaries say "Speaker 2 (likely Roy, unconfirmed)".
  2. **machine-confirmed** (`[systematic]`): the auto bar is met, so the name is used for filing and in summaries, with the class recorded. The bar: person's `auto: allowed`; similarity ≥ 0.95 with ≥ 5 confirmed references (or ≥ 0.98 with 3–4); no sanity veto fires (calendar says that person wasn't there; the cluster refers to that person in the third person; the cluster has under 30 s of talk time; two clusters match the same person). Solo recordings: single cluster matching Gordon at ≥ 0.90.
  3. **human-confirmed**: Gordon (or a document) said so. The only state that can enroll a *new* reference into the library; machine-confirmed matches never feed back into the embeddings, so a wrong auto-tag can't compound.
  A correction of any auto-tag flips that person to `auto: paused` for 90 days and lists their recent auto-tags for review. `recordings/STATUS.md` carries auto-tag counts and corrections per person, and the work Weekly Review's full pass reads them, so the bar can be tuned on evidence. Summaries carry one footer line naming which speakers were machine-confirmed; the body uses names plainly.
- **Enrollment quality (revised 2026-09-30):** a person is "thin" with fewer than **5** human-confirmed references, or with references from fewer than **3 distinct recordings** (diversity matters more than count: five clips from one call teach the model one room and one microphone). Thin people are shown so in the people index and never auto-tagged; the ingest skill asks for confirmation when one appears, so profiles thicken naturally. Auto-tag requires ≥5 references across ≥3 recordings (and the bar in state 2 above). (v3: 17 of 32 people had a single reference.)

### 10.3 Corrections flow back (Q9 #7, Q4)
When Gordon says "that's not Roy, that's Mike," attribution-correction: (1) updates the `speakers.md` row (old value struck through, new row with `by: gordon`); (2) removes the wrong (R, N) record from the library source and adds the right one; rebuilds the library; (3) re-runs matching on the recordings that could actually have been affected: every recording processed **since the wrong reference was enrolled** where that person was a candidate, capped at the most recent 20, and lists the ones whose top candidate changed for Gordon to confirm (revised 2026-09-30 from "last 90 days": a bad reference can only have influenced matches made after it existed); (4) supersedes every fact filed from that recording under the wrong name, using the files' `sources:` lists (§5.4); (5) writes a decisions line and a receipt. The correction is not done until step 3's list is either empty or reviewed.

### 10.4 Contacts: Sancho is the single point of truth (decided 2026-09-24; form J-D1; Sync mirroring accepted)
Gordon's call: Sancho holds his contacts, starting with a mine of Google Contacts and a de-dupe. (v2 had 138 rows in `gordonos-people.db` from the same source; v3 had 35 people folders; the two never met.) The form (decided: J-D1), as weighed:

- **J-D1. Person files are the contacts database (recommended).** Every contact is a `people/<slug>.md`, with a `contact:` block in frontmatter (emails, phones, addresses, birthday, `google_id`, `source`, `updated`). Most of the 500-odd files will be thin (`tier: contact-only`), and the people index hides thin entries behind a count unless asked. A generated `people/CONTACTS.csv` (and vCard on demand) is the export view for syncing back to Google or Apple. De-dupe is a script over frontmatter: same email, same phone, alias collision, near-name match; it proposes merges, Gordon confirms, the merge is a supersede-and-redirect (the loser file becomes a one-line pointer, never deleted). Pros: one identity per person, really; the contact and the knowledge about them can never fork; git-diffable; the search path finds people by email. Cons: many small files; a person file now carries PII on three machines and a cloud (see below).
- **J-D2. A standalone table beside the tree** (`people/contacts.csv`, or SQLite): structured, easy to import/export and de-dupe with ordinary tools; `people/<slug>.md` exists only for people with knowledge, linked by `contact_id`. Pros: familiar shape for a contacts job. Cons: two records per person that have to agree, which is exactly the v2 smell (a people DB beside people files); SQLite is opaque to git and to grep; CSV is neither of those but still a second store.
- **J-D3. J-D1 plus a standalone DB as a cache.** Person files are truth; a script builds a SQLite or CSV from them for fast queries and for whatever contact-sync tool wants a table. This is J-D1 with the generated layer (§2) doing the "standalone DB" job, and it's what "standalone" most usefully means here.

Whichever form: the contact block is data (§2), cited like any fact (`[google-contacts 2026-09-30]`), and superseded not overwritten. **Mirroring:** the whole tree mirrors to sync.com and Leah's machine, contacts included. Gordon accepted that on 2026-09-24.

New roadmap item: **contacts import + de-dupe** (Google Takeout CSV in; proposed merges out; person files written through the gate). Counts as a WIP slot.

## 11. Sync and git (Decision K: composed from earlier sections; no new choice)

Already built and not redesigned: git database at `~/.sancho.git` outside Sync, private GitHub remote as history backup, knowledge-only repo (`.gitignore` blocks media; pre-commit rejects binaries and files over 5 MB), daily launchd autocommit. See `_setup/README.md`.

What Phase 2 adds, all by reference:
- **Provenance (§5.6):** hourly autocommit plus a commit at each conversation close; messages list the live sessions; `git log -S` answers when a fact entered to the hour; receipts and session notes carry the per-action trail.
- **Startup deltas (§8.2, item 6):** the orientation line "since Tue: 6 files changed in personal/" is `git log --since=<last clean lease close> --name-only`, summarized by top-level area. No dashboard to maintain.
- **`updated` in every index (§4.1):** taken from git, never from frontmatter.
- **The map (§14):** regenerated by a command after every commit batch and nightly; the map's "changed in the last 7 days" view is a git query.
- **In git:** transcripts and VTTs (§6, F-1), summaries, knowledge, people (incl. contact blocks, §10.4), skills, scripts, generated indexes and the map, `recordings/STATUS.md`, `_setup/`.
- **Not in git:** `_queue/` (ephemeral state; results older than 90 days pruned by the watcher), audio and JSON sidecars (`Sancho-Audio/`), the ledger, secrets (`~/.config/sancho/`).
- **Sync.com conflict copies** (`*-CONFLICT-*`) are a lint check; one appearing means a second writer got in (§7.2).
- **Files the repo refuses (found 2026-09-30, fix in Phase 4).** A file over 5 MB or binary is *not moved anywhere*: it stays in place, inside `~/Sync/Sancho`, so sync.com has already backed it up; only git declines it. The bug in what's built: `git-autocommit.sh` stages everything and lets the hook reject the whole commit, so one oversize file silently stalls every hourly commit until someone notices. Fix: the autocommit checks staged files itself, unstages offenders, commits the rest; offenders are listed in a generated `_setup/GIT-EXCLUDED.md` (path, size, reason, first seen) and surfaced in `HEALTH.md` so the greeting can say so. The pre-commit hook stays as the last line for hand commits. Nothing is moved automatically, because moving breaks every path that points at the file; a second copy beyond sync.com is a deliberate act. Rule of thumb: sync.com backs up everything in the folder; git backs up knowledge, with history and a GitHub copy; a large file loses the second, never the first.

## 12. Built-in memory boundary (Decision L: decided 2026-09-22)

Claude's account memory is not part of Sancho. Everything Sancho or the Copper Leaf kit needs to survive lives in Markdown files in the tree (job plans included). Built-in memory may hold nothing Sancho depends on; if it holds anything at all, it is a pointer to STATUS.md. Reason: durable, human-readable, survivable if Claude goes away, readable by any other system.

## 13. Pipeline design (Decision M: decided 2026-09-24; M-1, Pushover)

Decided so far: one runner, one Mac; no Mouth/Nerd *division of labour* (the host execution bridge, §1, is the one place a session hands work to the Mac, and Gordon may still call Cowork "Mouth" and Claude Code "Nerd" as nicknames); no ntfy, no Wrike; Groq transcription; SQLite as internal ledger with a generated status view; the black Mac keeps running v3's pipeline until this one is proven; sessions trigger it through the queue (§1). Speaker states and library rules: §10.2. Provenance: §5. Landing and filing: §3.5, §6.

### 13.1 Stages (one script, `_setup/pipeline/earballs.py`, stdlib + the same libraries v3 proved; each stage a function with the standard header)

| # | Stage | From v3 | Sancho change |
|---|---|---|---|
| 1 | Plaud fetch | `plaud-sync.py` keep w/ edits | **Every 5 minutes** (decided 2026-09-30; Gordon often wants a recording soon after making it), made light by fetching *incrementally*: list newest-first and stop at the first already-known ID, so a quiet run is one request instead of v3's full 16-page walk. A full reconcile once a day. Plus command `pipeline.sync` for "sync now" from the phone. Bearer token from `~/.config/sancho/env`; on 401 the health line says "Plaud token expired: re-capture" and stays red until fixed. Demo-serial filter kept. Caveat: this is Plaud's private web API with a hand-captured token, not a supported API; if they rate-limit or change it, the interval backs off automatically and the greeting says so. Voice memos also arrive this way (they're Plaud recordings); nothing is hand-dropped except non-Plaud audio. |
| 2 | Download + ingest | keep atomic rename, sha256, `rec_` IDs | Writes `Sancho-Audio/processed/<rec_id>.ogg` + ledger row. `Sancho-Audio/inbox/` remains for the rare non-Plaud file (a forwarded audio message); same path, `source: external`. |
| 3 | Silence handling | `strip_silence.py` | **dropped for the fresh pipeline (M-1, 13.3)** |
| 4 | Transcription | `transcribe.py` keep | Groq `whisper-large-v3`, chunking, retries; local faster-whisper as fallback only. Word JSON to `Sancho-Audio/processed/<rec_id>.json`. |
| 5 | Diarization + embeddings | `diarize.py` keep, then improve | pyannote pinned; embeddings to `Sancho-Audio/voiceprints/recordings/<rec_id>.npy`. **Diarization (how many speakers, and who spoke when) was v3's weakest step; Gordon: "almost always wrong."** Improvements in order of cost (13.7): pass a speaker-count prior from calendar attendees and Plaud's scene; merge over-split clusters whose voiceprints match the same person; let ingest confirm the count and re-run with it fixed; trial a hosted diarizer against pyannote on ten known recordings before choosing. |
| 5b | Calendar feed | new (v3's `calendar_hints.py` idea, fed properly) | **Kept** (decided 2026-09-30; a cross-check for diarization and a who-was-in-the-room prior). v3's cache depended on a session; Sancho fills it mechanically: a Mac-side command polls Gordon's private ICS feed (read-only, no OAuth) into `Sancho-Audio/calendar-cache/`, and stage 5 reads attendee counts and names from it. |
| 6 | Speaker match | `voiceprint.py` keep w/ edits | Library rebuilt from `speakers.md` confirmation records (§10.2); writes candidate rows and applies the auto bar. |
| 7 | Transcript write | `process.py` rewrite | `recordings/inbox/<rec_id>/transcript.md` (YAML frontmatter per §4.1, `SPEAKER_NN [t]` body), `speakers.md`, `meta.md` (Plaud metadata as data, recorded-at with offset). Ledger → `ready`. |
| 8 | Status view | new | `recordings/STATUS.md` regenerated after every run: waiting count, oldest, last sync, token state, stuck rows, auto-tag stats. This is the startup health line's source. |
| 9 | Ingest | **skill**, not code | On request (startup offers when inbox > 0): confirm speaker count and names, extract into the seven GTD buckets (§17.1), file per §3.5, supersede, receipt. Personal-state facts confirmed before filing. |
| 10 | Watchdog | `pipeline-watchdog.py` keep w/ edits | Same checks (sync freshness with wake suppression, oldest waiting, stuck rows, disk, launchd counter, backup age), **with the Mac's sleep and offline states treated as known states, not failures** (§16.3); Gordon expects false alarms at first and wants it dialed in from real behavior over the first weeks. WARN → status view only. **CRITICAL → status view + a push to Gordon's phone** (channel: 13.6). Content: one plain, actionable line ("Pipeline: 2 recordings waiting 26 h, oldest Tue 9/22. Plaud token expired; re-capture it."). Cadence: on state change, then at most once a day while red; never a repeat every cycle. Destination hardcoded to Gordon in the script; no recipient parameter exists, so it cannot message anyone else. |
| 11 | Ledger backup | keep | Nightly `sqlite3 .backup`, keep 7, in `Sancho-Audio/`. |

Dropped: FTS search (ripgrep, §4.4), autotag/rehint/ignore as separate tools (folded into stage 6 with the rules in §10.2), all comms/mesh/notify tooling. Calendar hints were on this list and were **kept** on 2026-09-30 (stage 5b).

### 13.2 The 24-hour loop and the three backlogs
- **Fresh:** anything recorded from cutover onward. SLA: transcribed within 24 h of upload; the status line turns amber at 12 h waiting, red at 24 h. Ingest is offered at every startup while the inbox is non-empty; the offer names the oldest.
- **Backlogs are a separate runner state, never in the fresh queue** (v2's own lesson). `pipeline.backfill --era fresh|good|old --limit N` processes N recordings from the chosen era into `recordings/backlog/<era>/<rec_id>/`, transcribed and speaker-matched but not ingested. **Drip rate (decided 2026-09-30):** the backfill is throttled to stay inside Groq's free tier, leaving headroom for the fresh pipeline: about six audio-hours a day, run overnight, with a daily cap the watcher enforces from the ledger's Groq usage count. At ~770 audio-hours of backlog that's roughly four months; if fresh volume ever exceeds the remaining headroom, billing gets set up then (13.8), not before. Order: era 3 (fresh backlog, May–Sep 2026) newest first, then era 2 (Mar–Jun 2026), then era 1 (Aug 2025–Feb 2026). **The first ingest job of all is the notes-to-self** (solo recordings, newest first, decisions.md 2026-09-22), which need no speaker confirmation.
- v3's 704 transcripts are re-derived from audio, not copied (kickoff Phase 3); v2's 690 real recordings need their audio (291 `.ogg` in v2's `earballs-inbox/` plus whatever Plaud still holds; Plaud retains everything).

### 13.6 The phone channel (decided: P-1 Pushover, on trial)
Gordon carries an Android phone (v3 dropped iMessage for that reason). The channel must be push, need no inbox, and be callable from a Mac script with one secret in `~/.config/sancho/env`.
- **P-1. Pushover (chosen).** One-time app purchase, a simple HTTPS POST with a user key and app token, priority levels (a CRITICAL can bypass quiet hours and require acknowledgement), reliable delivery, nothing to host. The token lives outside Sync; the script has no recipient field.
- **P-2. ntfy with an authenticated topic.** Free; worked for delivery in v2. v2's smell was an unauthenticated public topic and 4,437 identical messages, not ntfy itself. Needs either ntfy.sh's paid access-control tier or a self-hosted server; the phone app must stay installed and subscribed.
- **P-3. Email to Gordon's own address** via a fixed SMTP account. Universal; but email is where alerts go to die, and it puts an SMTP credential on the Mac for a system whose must-never list includes outbound mail. A hardcoded single recipient makes it safe, but P-1 does the job without touching mail at all.
- **P-4. SMS via a gateway (Twilio).** Works anywhere; costs per message and needs an account with a phone number; overkill for one recipient.
Whichever channel: the same script also serves the personal lobe later (the nomad routine's "drive today" nudge is the same shape), so it is built once, as `_setup/notify.py` with a `pipeline.test-notify` job that sends a test push on demand and at startup's daily self-test.

### 13.3 Silence stripping (decided: M-1)
v3 ran silero-vad and re-encoded recordings to remove silence before transcription. It saved Groq minutes and shortened long ambient recordings; it also **overwrote the original audio** (44 errors logged, originals recoverable only from Plaud) and added a fragile ffmpeg step that caused the August wedges.
- **M-1. Drop it for the fresh pipeline (chosen).** Groq handles silence; the cost is cents per hour; originals are never touched. Keep a stripped *derivative* (`<rec_id>.stripped.ogg`) as an optional pre-step only for recordings over 2 hours, never replacing the original.
- **M-2. Keep it, non-destructive.** Always produce the derivative, transcribe the derivative, keep both files. Cleaner transcripts of ambient recordings; double the audio storage; the fragile step stays in the hot path.
- **M-3. Keep it as v3 had it.** Rejected: violates no-data-loss.

### 13.4 Tests
A fixture recording set under `_setup/tests/pipeline/` (a 2-minute solo clip of Gordon, a 3-minute two-speaker clip, a silent clip, a corrupt file): the script must produce the expected `transcript.md`, `speakers.md` with the solo clip machine-confirmed as Gordon and the two-speaker clip left as candidates, a `refused` result for the corrupt file, and a correct `STATUS.md`. Runs as a command `pipeline.test`; startup reports the last test date.

### 13.5 Cutover (revised 2026-09-30: no parallel week)
Plaud is the durable upstream and retains everything, so a forward overlap buys nothing. Sancho's pipeline starts on the silver Mac **as the first Phase 4 build**, wherever the Mac is (Gordon is in Italy through Oct 6; Plaud's cloud and Groq are reachable from anywhere), with a **backward overlap**: the first sync pulls everything from seven days before the black Mac's last known transcript (2026-09-17) forward, so anything v3 processed but Sancho didn't is re-derived here, and nothing depends on reaching the black Mac. The black Mac's v3 jobs get retired whenever it's next reachable (procedure like `rainbow-rig-shutdown.md`) and its Plaud token revoked; until then it's a second consumer of the same cloud, harmless. v3's earlier transcripts stay as the backlog eras (13.2).

### 13.6 Zoom (added 2026-09-30)
Gordon wants Zoom transcripts pulled automatically, and the recordings too. Zoom's cloud recordings API (a Server-to-Server OAuth app on his account, `recording:read`) lists finished recordings; a Mac-side command polls it every 15 minutes and downloads, per meeting: the **VTT transcript** (Zoom's cloud transcript carries *participant names as speaker labels*, which is better than any diarizer and a free source of human-quality voiceprint labels), the **audio-only M4A**, and the **MP4 video**. Storage: video and audio in `Sancho-Audio/zoom/<YYYY-MM-DD>_<topic>/` (outside git; check sync.com quota, since video is gigabytes a month); the VTT goes through the same landing zone as a recording (`recordings/inbox/`, `source: zoom`) and ingest files it to the client's `transcripts/` with a summary. Requires cloud recording and cloud transcript enabled on the Zoom plan; if the account lacks them, the fallback is the existing drag-in path (build item 13). Zoom audio can also run through diarization and voiceprint enrollment with the VTT's names as ground truth, which is the cheapest way to thicken the library.

### 13.7 Making diarization less wrong (added 2026-09-30)
Why it fails: overlapping speech, phone or car audio, more than four people, and no prior on how many. In order of cost:
1. **Give it a count.** Calendar attendees (stage 5b), Plaud's scene metadata, and the ingest step's confirmation ("were there three of you?") each supply `num_speakers`; pyannote is markedly better constrained than free. v3 exposed `--num-speakers` and never fed it.
2. **Merge by voiceprint.** Two clusters whose embeddings match the same enrolled person at ≥0.85 are one speaker; v3 flagged over-splits and left them.
3. **Let the human fix it once.** Ingest shows the speaker count and talk-time per cluster; Gordon corrects it in one word; the recording re-diarizes with the count fixed and the confirmed count becomes a reference for that meeting series.
4. **Trial a hosted diarizer** (pyannoteAI's hosted model, Deepgram, or AssemblyAI) against local pyannote on ten recordings Gordon knows well; compare speaker counts and a spot-check of turns; adopt only if it's clearly better, since it adds a paid dependency and sends audio off-machine. An ICE item with a deadline, not a day-one build.

### 13.8 Groq: are we on the free tier?
Probably yes, and it matters. Groq's free tier for Whisper allows about 20 requests a minute, 2,000 a day, and roughly 8 hours of audio a day, with a 10-second minimum billed per request; the paid rate is about $0.111 per audio hour for whisper-large-v3 and $0.04 for the turbo model ([eesel](https://www.eesel.ai/blog/groq-pricing), [CloudZero](https://www.cloudzero.com/blog/groq-pricing/), [freellm](https://freellm.net/models/groq/whisper-large-v3)). v3 logged 60 failed Groq attempts and 24 "groq exhausted" audits; free-tier limits are a plausible cause, and a backfill of 1,400 recordings would hit them at once. Recommendation: set up billing before the backfill starts; at Gordon's volume (~100 recordings a month, call it 80 hours) the fresh pipeline costs under $10 a month at the large-v3 rate. Verify the tier in the Groq console rather than trusting this.

### 13.9 Solo recordings against Gordon's voiceprint
Yes, and it's already in the design (§10.2, state 2): a single-cluster recording is auto-confirmed as Gordon only if its embedding matches his library entry at ≥0.90. One cosine similarity; it catches the case v3 missed, a solo recording of someone else silently tagged as Gordon.

## 14. Documentation, tests, living map (Decision N: decided 2026-09-24; N-3 sequenced)

**The requirement (kickoff, amended 2026-09-30):** every component carries a header (why, what, reads, writes, how to test); nothing ships without a test; a script regenerates a visual map daily; if a component isn't on the map, it isn't done. **Gordon does not design or run tests.** His words: he is the executive, Sancho is the manager; he says do the job, and it is Sancho's job to do it *and* to make sure it keeps being done correctly. His involvement starts when he sees a result that's wrong and asks why. At that point Sancho produces all the evidence (the test board, the run logs, the receipts, the diff between what the test checks and what actually failed), and the troubleshooting is joint. The consequence for design: **every test runs automatically** on its schedule and after every change to its component; a test that exists only as instructions for a person ("open the app and check that…") does not count as a test, because nothing runs it; if a check can only be done by eye, the design turns it into something a script can check, or it is written down as a known gap; and the standing question for Sancho after any failure Gordon notices is "why did the end result fail while the tests passed?", which is itself logged, because that gap is where the next test comes from.

### 14.0 What "automatic" means here
- Scripts, hooks, the lint, the pipeline, startup: tested by the queue on a schedule (nightly `test.all`) and on change (any commit touching a component's files triggers its tests through the watcher). Results land in the generated `TESTS.md` and in `HEALTH.md`; a red test appears in the greeting once and stays in the status view until green.
- Skills: the headless fixture runs (14.2) execute nightly for every skill and after any edit to a skill file. Gordon never invokes them.
- The one thing Gordon does: notice. When something he sees is wrong, he asks, and the answer is evidence, not reassurance: what ran, what it checked, what it saw, what the gap is, and a proposed new test that would have caught it.

### 14.1 The header, enforced
Every skill, script, job, template, and folder convention carries the same frontmatter block (§9.1 shows the skill form; scripts carry it as a docstring in the same key order: `name, type, description, why, reads, writes, test`, plus `triggers`/`must_not_trigger` for skills and `schedule` for jobs). The lint (§2) blocks the map build on a missing or empty key. Templates live in `_setup/templates/` and `new-component` is a command that copies the right template into place with the header pre-filled, so the cheap path is the compliant path.

### 14.2 What "tested" means
| Component | Test is | Runs as | Passes when |
|---|---|---|---|
| Script / job | `_setup/tests/<name>/` with fixture inputs and expected outputs; pytest-style | command `test.<name>`; all of them nightly as `test.all` | outputs match; exit 0 |
| Skill | a fixture folder (a mini tree plus a scenario file: the user's message, the expected files written, the expected trigger behaviour) | a headless Claude Code run (`claude -p`) against the fixture, launched by command `test.skill.<name>`; compares written files to expected and checks that the skill fired on its `triggers` and stayed silent on its `must_not_trigger` list | files match on the fields that matter (frontmatter, cites, receipts), and both trigger checks pass |
| Hook / lint | a fixture of deliberately bad files | `test.lint` | every bad file is caught, every good file passes |
| Template / convention | the lint itself is its test | with `test.lint` | |
| Pipeline | §13.4 | `pipeline.test` | |
| Startup | §8.6 | `test.startup` | eight lines, correct values, no extra reads, < 30 s |
`_setup/TESTS.md` is generated: one line per component, last run, last result. Startup's health line includes "tests: all green as of <date>" or names the failures. **A skill's own header `test:` must point at a folder that exists; the lint checks it.**

### 14.3 Which hooks fire where (the kickoff's question)
| Mechanism | Claude Code session | Cowork session | Mac, no session |
|---|---|---|---|
| `~/.claude/settings.json` PreToolUse / PostToolUse hooks | fire | **do not fire** (different tool names, different host) | n/a |
| git pre-commit hook (`~/.sancho.git/hooks/`) | fires on commit | fires, because commits run on the Mac through the queue | fires for the daily autocommit |
| launchd schedules (watcher, pipeline, map, autocommit) | run | run | run |
| Command allowlist (`_setup/commands.md`) | enforced by the watcher | enforced by the watcher | enforced |
| The lint (blocks the map build) | via queue | via queue | nightly |
| Skill `must_not_trigger` | model discipline plus the trigger test | same | n/a |
Consequence: **nothing Sancho must never skip is enforced by a session hook.** Every hard rule lives in git hooks, the watcher's allowlist, the lint, or a launchd job, because those fire whichever session (or none) is running. Session hooks are a Claude Code convenience only, used for the Copper Leaf kit's live-site guard, which is why plugin work stays in Claude Code (decisions.md 2026-09-22).

### 14.4 The living map
Generated by `_setup/build-map.py` from three inputs, no hand-maintained registry: (1) every file's frontmatter (name, type, description, lobe, reads, writes, chain, triggers, schedule, test); (2) `_setup/commands.md` and the launchd plists; (3) git (`updated`, "changed in last 7 days"). It runs after every commit batch and nightly, as the last step after the lint and the index build.

**Resolution (decided 2026-09-30): three zoom levels, and the top one is the point.** Gordon needs to see, understand and *remember* the big parts and how they interact; the wiring exists for when something breaks.
- **Level 0, the system** (one diagram, at most eight boxes, fits on a phone): Capture (Plaud, Zoom, calendar) → Pipeline (on the Mac) → Landing zone → Ingest (a session) → the Tree (spine, work, personal) ← Sessions (Cowork, Code, phone via Dispatch) ↔ the Queue/Mac (commands, schedules, watcher) → Outputs (indexes, map, Pushover). Each arrow is one sentence. This is the picture to hold in your head.
- **Level 1, the components** (one diagram per Level-0 box): the pipeline's stages; the tree's lobes and areas; the skills grouped by family (thinking, GTD, ingest, routines) with their chain links; the commands and schedules; the devices. Each node is a component with a header; each still has one line of description.
- **Level 2, the wiring** (tables, not diagrams): reads and writes per skill and command; triggers and must-not-triggers; the test board; the retired list; dangling-reference results. This is where a "why did it fail" investigation starts, and Gordon rarely needs to look at it unprompted.
`MAP.md` holds all three, Level 0 first, each Level-1 diagram under its own heading, Level 2 as collapsed tables at the end. The HTML render (§14.5, later) adds click-to-zoom from a Level-0 box into its Level-1 diagram and from a component into its wiring row; until then, headings and the table of contents do the zooming. FOCUS is printed above Level 0; "changed this week" below it.
- Diagrams as Mermaid source inside `MAP.md` (renders in GitHub, Obsidian, PhpStorm, and in an Artifact).
- A dangling-reference check: any `reads:`/`writes:`/`chain:` target that doesn't exist fails the build. **A component not reachable from the map (no header, or header not parsed) fails the build.** That's the mechanical form of "if it isn't on the map, it isn't done."

### 14.5 Where the map renders (decided: N-3, sequenced)
`MAP.md` now (scaffold, in git). `MAP.html` later: a render of MAP.md only, gitignored (it inlines Mermaid.js), regenerated nightly, entered in `personal/ice/` and built when it wins a WIP slot. Options as considered:
- **N-1. `MAP.md` with Mermaid, opened wherever Gordon already reads Markdown.** Zero extra tooling; GitHub renders it on the private repo; the Cowork session can publish it as an Artifact on request for a clickable version. Cost: Mermaid gets crowded past ~60 nodes, so the map is several diagrams (tree, skills and chains, pipeline, jobs), not one.
- **N-2. A generated self-contained `MAP.html`** (inline SVG or Mermaid.js, collapsible sections) written beside `MAP.md` and opened in the browser. Prettier and navigable at scale; one more generator to maintain, and HTML in the knowledge repo is a slight oddity.
- **N-3. Both**, `MAP.md` as source of truth and `MAP.html` as a nightly render. Best view, most machinery; defer the HTML until N-1 proves too small.

## 15. Leftovers (Decision O: decided 2026-09-24)

### 15.1 Copper Leaf kit follow-ups (from the handoff's §17)
Already done: repo `CopperLeafCreative/clc-plugin-dev-kit`, private, pushed. Still open, each with a recommendation:
1. **Leah's access:** write (she will add lessons learned; the kit's rules file is the place). Recommended: write, with `main` protected against force-push and the `wip/*` branches left force-pushable.
2. **How Leah receives it:** as a Claude Code plugin bundling the three skills and both hooks, installed the way she installs Astra; the repo doubles as the plugin source with a `.claude-plugin/` manifest. Windows port (Python path, Task Scheduler, clones outside Sync) is a job in the kit, not in Sancho.
3. **Where the kit's job plan lives:** `~/Sync/Sancho/_queue/jobs/` like every other job (decisions.md 2026-09-22: all memory in files). The kit's Core Development Rule step 3 ("save the plan to memory") is repointed to write the job file; Sancho's registry entry for the kit records that. The kit stays self-contained otherwise.
4. **Sancho's registry for the kit:** `work/copper-leaf/plugins/` with one file per plugin (repo, main file, prefix, version locations, related plugins, staging site, SSH alias, WP-CLI works?, error log verified?, quirks) and `_registry.md` generated from them. First entry of type tooling: the kit itself. Sancho **tracks** plugin jobs through the 16 stages as job files and **launches** the kit's skills; it never runs a stage itself.
5. **Lessons source of truth:** the kit's `CLAUDE.md` §12 for anything about plugin development; Sancho holds a pointer, never a copy.

### 15.2 Shared skills for Astra (revised 2026-09-30: business skills, not thinking skills)
Gordon's call: think-first, critical-thinking, triz, punnett-square, brief-me and fact-check-anyone are **his personal skills** and are not shared with Astra; they may carry his context freely. What Astra shares are **business skills**, mainly Copper Leaf and Press Managed operations: the plugin kit's three (already shared as a plugin), and the coming ones (site updates with post-update tests, reporting, billing, whatever the review of Leah's work surfaces; `_design/seeds/work-ice.md`). The sharing mechanism is the same one drafted earlier, applied to those: no user-specific content in a shared skill's body; per-user parameters in `skills/_params/<user>.md` at the same relative path in both workspaces; Leah consumes the files unchanged. Shared skills carry `shared: astra` in their header; the lint flags a shared skill whose body names anyone in `people/` or reads from `personal/`. (This reverses the kickoff's assumption that the thinking skills would be the shared set.)

### 15.3 Personal material placement (revised 2026-09-29; see §3.4)
`personal/me/` for health, neurology, identity; relationship material under `personal/`, by area not by secrecy. Never in CLAUDE.md (layering) and never in a shared skill body (Astra). The 120 relationship files under v3's `work/projects/` and v2's `health/` route to `personal/` in Phase 3 through the gate because that's where they belong, not because they're hidden.

### 15.4 Backfill plan (settled in §13.2)
Three eras, separate runner, notes-to-self first, newest first. v2's raw `.ogg` and Plaud's cloud are the audio sources; old summaries are never copied forward.

### 15.5 Decided 2026-09-24
O-1 write access for Leah, `main` protected; O-2 plugin from the same repo; O-3 all 16 stages tracked as job files; O-4 `skills/_params/<user>.md`.

## 16. Devices, and the phone in particular (added 2026-09-26)

### 16.1 What Dispatch is, and what it changes
Dispatch (Cowork, beta, Pro/Max) is one continuous Cowork conversation shared between the Claude desktop app and the Claude mobile app: a message sent from the phone runs on the Mac, with the Mac's files, connectors, plugins and apps, and the result comes back to the phone. Requirements: the desktop app open and the Mac awake, both devices online. ([Help Center](https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork), [DataCamp](https://www.datacamp.com/tutorial/claude-cowork-dispatch), [XDA](https://www.xda-developers.com/claudes-dispatch-feature-turned-my-phone-into-a-remote-control-for-my-entire-workflow/))

So **the phone is not a device that runs Sancho; it is a remote for the one that does.** That is good news for the design: everything in §1–§15 already runs from a Cowork session on the Mac, which is exactly what Dispatch drives. "Hey Sancho" from the phone starts the same eight-line orientation; a command requested from the phone runs on the Mac; a Pushover alert closes the loop the other way. Nothing needs a second runner, a mesh, or a phone-side install beyond the Claude app, the Plaud app, Pushover, and sync.com.

### 16.2 The device table
| Device | Role | Writes into Sancho? | Notes |
|---|---|---|---|
| Silver Mac | the runner: Cowork and Claude Code sessions, watcher, pipeline, git, map | yes (the only writer) | must be awake and have the desktop app open for Dispatch and for launchd jobs to run on time |
| Phone (Android) | remote: Dispatch in, Pushover out; Plaud app uploads to Plaud cloud; sync.com app can drop a file into `Sancho-Audio/inbox/` | never directly; only through the Mac session | dictation is the main input, so the dictation line applies doubly |
| Plaud device | capture | no | uploads to Plaud cloud; the Mac pulls hourly |
| Leah's machine | sync.com mirror; Astra's own workspace | never (rule in CLAUDE.md; conflict-copy lint) | shared business skills read from here by relative path (§15.2) |
| Black Mac | v3 pipeline until cutover (§13.5) | no | retired with its Plaud token after seven matching days |
| Rainbow Rig | cold storage only | never | v2 daemons to be disabled on next boot (`rainbow-rig-shutdown.md`) |

### 16.3 What the phone forces on the design (the one real consequence)
Dispatch and every launchd job depend on **the Mac being awake with the app open.** In an RV on battery, the Mac will sleep, and v3's audit log shows what that looks like: bursts of activity with multi-day gaps, indistinguishable from a broken pipeline. Two rules follow:
1. **Sleep is a state the system knows about, not a failure it guesses at.** The watchdog already reads `pmset -g log` for wake times (v3's wake suppression); Sancho's `HEALTH.md` and the startup line say "Mac slept 14 h, pipeline resumed 09:12" rather than "pipeline late." CRITICAL pushes fire only when the Mac has been awake long enough to have caught up and hasn't.
2. **Gordon decides the power stance, per situation, with one switch.** A command `mac.stay-awake on|off` toggles `caffeinate` (or `pmset` display-off-but-awake) and records the state in HEALTH.md; the personal morning routine can offer it when the calendar shows he'll be away from the RV. On shore power: on. On battery: off, and the phone lives with delayed answers. This is a design decision Gordon makes daily by circumstance, so it must be one word, not a settings dive.

### 16.6 Full Sancho from the phone when the Mac is closed (added 2026-09-30; proposed)
Gordon's real case: when he reaches for the phone, the Mac is usually closed and offline. Dispatch needs a running desktop app, so "the Mac is the backbone" means "no Sancho when the Mac sleeps," which isn't good enough. Two tiers, built in this order:

**Tier 1, now: a runner-less phone mode.** Most phone use is reading and capturing, and neither needs a Mac:
- *Read:* the Sancho repo is on GitHub; the Claude mobile app with the GitHub connector can read it directly. A phone conversation can brief him on a client, read a project's next action, search summaries, and answer "what did Roy say about radio" from the transcripts in git. Read-only, no Mac, no runner; the tree's structure (indexes, cites) makes it usable that way.
- *Capture:* three ways, easiest first. (1) **Plaud**, device or app: the Plaud phone app records from the phone's own microphone when the device isn't handy (verify on Gordon's plan), uploads to the same cloud, and the recording flows through the full pipeline with speaker ID and filing; one tap, nothing new to learn. (2) **Dictate into the Sancho conversation** in the Claude app: this is text, not audio, so no transcription step; the session writes it as a `_queue/inbox/` note through the GitHub connector and the runner ingests it when the Mac wakes. Best for a quick thought that should be words, not a recording. (3) **Android recorder → sync.com app → `Sancho-Audio/inbox/`**, for the rare non-Plaud audio. Plaud is the default; it's already the path and it keeps the audio.
- *What it can't do:* run the pipeline, run commands, regenerate indexes. The greeting on the phone says so in one line ("Mac's asleep; I can read and capture, not run").

**Tier 2, later: an always-on runner, and the rule that keeps two runners from becoming v2.** The Rainbow Rig in Colorado (online, powered, retired from everything else) can host a second copy of the runner: the Claude desktop app open for Dispatch, the watcher, the pipeline, the schedules. That reopens multiple machines, and the v2 failure was three machines writing one tree with no rule about who was allowed to. The rule that makes it safe:
- **Exactly one machine holds the *runner role* at a time.** The role is a file in Sync (`_setup/RUNNER.md`: which machine, since when, heartbeat), written only by the machine taking it, and a machine takes it only when the other's heartbeat is stale or on an explicit handoff command. The runner is the only machine that runs schedules, executes commands, runs the pipeline, and **commits to git**. The non-runner's launchd (or Task Scheduler) jobs check the role file and do nothing. Two runners writing is therefore impossible by construction, not by discipline.
- **Sync carries the tree, git is per machine, GitHub is the meeting point.** Each machine has its own `.sancho.git`; only the runner commits and pushes; the standby pulls on taking the role. Conversation leases and session notes ride along in Sync as they do today.
- **Handoff is one word from the phone** ("Sancho, run from the Rig") or automatic when the Mac's heartbeat is stale for an hour. The greeting always names the runner.
- **Costs to be honest about:** the Rig is Windows (v3's pipeline is Mac-shaped: launchd, MPS; it's a port), it needs the Claude desktop app signed in and awake permanently, Sync.com latency means a file written on the Mac appears on the Rig seconds to minutes later, and secrets must be unlocked on both. A Mac mini on the Rig's shelf would remove the port and most of the risk, at a price. This tier is an ICE item for later (Gordon, 2026-09-30: dig into the Rig after the Mac is stable). Tier 1 is approved for a trial now.

### 16.4 Phone-shaped output
Startup's eight lines already fit a phone screen; every skill's receipt is one line; brief-me's briefing is capped at two minutes' reading. A `phone` note in a skill header is not needed: the rule is that nothing Sancho says needs a wide screen, and the lint's line caps on generated views enforce it. Things that don't work from the phone and are stated plainly when asked: anything needing the built-in browser pane, approving a folder mount, watching the plugin kit test a staging site in Chrome.

### 16.5 Two phone paths worth building early
- **Voice memo → Sancho:** a memo recorded on the phone (not Plaud) is shared to the sync.com app into `Sancho-Audio/inbox/`; the pipeline treats it like any recording (`source: external`). No new code; the inbox watcher already exists in §13.1 stage 2.
- **"Where am I" for the nomad routine:** Dispatch carries no location. For now the message says it ("in Moab"); the routine writes `personal/nomad/location.md` with a date, and every other consumer reads that file. A phone-side automation that posts location to the sync.com folder is an ICE item, not a day-one build.

## 17. GTD alignment (added 2026-09-26)

GTD is five steps (capture, clarify, organize, reflect, engage) over six horizons. Sancho already has most of the parts; this section names which part plays which role, so the vocabulary and the mechanics stop being two things.

### 17.1 The five steps, mapped
| GTD step | What it means | In Sancho | Gap to close |
|---|---|---|---|
| **Capture** | everything out of the head into a trusted inbox | Plaud → pipeline; voice memos → `Sancho-Audio/inbox/`; dictation in session ("write that down"); ideas → ICE | none new; the trusted-inbox rule is that every capture path lands somewhere startup can count |
| **Clarify** | for each captured thing: what is it, is it actionable, what's the next action | **the ingest skill is the clarify step for recordings.** Its extraction passes become GTD's buckets exactly: next action (handed to Gordon for his task manager) · project (new or existing `project.md`) · waiting-for · reference (knowledge, people) · someday/maybe (ICE) · calendar (surfaced, Gordon books it) · trash | rewrite earballs-ingest's passes around these buckets (Phase 3) |
| **Organize** | put clarified things where they belong | projects folders (H1); areas = business and personal-area folders (H2); reference = knowledge and people; someday = ICE parked; **Waiting For is a status, never a list of its own** (decided 2026-09-26): on a task it's the Wrike/Google Tasks "Waiting For" status Gordon already uses; on a project it's the `waiting:` field on `project.md` (who, what, since); on a job it's a stage with `gate: waiting`. The generated `PROJECTS.md` shows the waiting column; there is no separate WAITING-FOR file. Calendar = Google Calendar; next actions = Wrike and Google Tasks | `waiting:` in the project template; flagged at 14 days at startup and walked in every review |
| **Reflect** | look at the whole system on a rhythm | daily: the focus checksum (§4.6); **weekly: the Weekly Review skill, one per lobe**; monthly: ICE quick review + month focus; quarterly: ICE deep dive + Horizons 3 and 4 | **the Weekly Review skill is the missing piece**; it goes on the Phase 3 build list as a new skill, not a port of weekly-work-review |
| **Engage** | do the work, choosing by context, time, energy, priority | today's three per lobe at the top of orientation; the project's next action is the unit of doing | none |

**Sancho's standing role (decided 2026-09-26, goes in CLAUDE.md):** keep GTD running for *maximum effectiveness, not maximum strictness*. Offer the daily checksum and the weekly, monthly and quarterly reviews on their cadence; when Gordon is visibly working in a chaotic way (three topics in one message, tasks started mid-task, a project with no next action being worked on anyway), say so once, plainly, and offer the fix; remind once more if nothing changed; never a third time that day (decided 2026-09-30). The measure is whether the reviews happen and the exception count falls, not whether every rule was obeyed.

### 17.2 The Weekly Review skill (to be built; shape only)
One skill, parameters `lobe` and `--mini`. **Cadence (decided 2026-09-26):** Work full review **Monday**, mini **Thursday** (both ahead of Gordon's meetings with Leah); Personal full review **Friday**, mini **Tuesday**; food planning stays **Sunday**; ICE monthly and quarterly. A mini is five minutes inside that morning's routine offer: today's three, stalled next actions, aging waiting-fors, nothing else. Six touchpoints a week is the ceiling; if the minis grow, they get cut before the full reviews do. Full-review steps, each ending in a write: (1) empty the inboxes: recordings waiting, ICE captures since last week, anything in `_queue/sessions/` left open; (2) walk every active project in the lobe: still active? has a next action? is it under 7 days old? is a waiting-for aging?; park or close what's dead; (3) read last week's focus and its exception count; (4) set this week's three; (5) glance up: month focus still right? any goal (H3) this week touches?; (6) receipt: what changed, written to `personal/reviews/YYYY-Www.md` or `work/reviews/`. Target: 20 minutes, driven by generated lists (`PROJECTS.md`, `STATUS.md`, ICE due list), never by memory. It is offered, like the morning routine (§8.5), never auto-run.

### 17.3 The horizons in the tree
| Horizon | Where it lives | Reviewed |
|---|---|---|
| Ground: next actions | Wrike / Google Tasks (Gordon's); `next_action:` on each project file | daily (focus), weekly |
| H1: projects | `work/<business>/projects/<slug>/`, `personal/projects/<slug>/`; generated `PROJECTS.md` per lobe | weekly |
| H2: areas | `work/<business>/` and `personal/<area>/`; each area's `INDEX.md` shows its projects, so an area with none is visibly idle | monthly |
| H3: goals (1–2 yr) | `work/<business>/goals.md`, `personal/goals.md`; each project file names the goal it serves (or "none, hobby") | quarterly |
| H4: vision (3–5 yr) | `personal/horizons/vision.md`; work vision per business in `business.md` | quarterly |
| H5: purpose and principles | CLAUDE.md identity section; `personal/me/principles.md` | yearly, or when it changes |
Work bottom-up: the build order clears the ground (pipeline, ingest, tasks handed off) before projects, before the higher horizons; H3–H5 files are created empty at scaffold and filled in the first quarterly review, not before.

### 17.4 Wrike and Google Tasks
Work projects mirror Wrike projects (`wrike_project:` on the project file); next actions mirror Wrike tasks; personal next actions are Google Tasks. Gordon writes to both; Sancho writes to neither (decision 2026-09-21). **Read-only access** to both would let the Weekly Review and the stall flag work from live data instead of the date on the project file (v2 had a Wrike API tool; a Google Tasks connector may exist). That is an ICE item for the work lobe, not a day-one build; until then the project file's `next_action` date is the signal and Gordon's task manager is the truth.

## 18. Who Sancho is, and what it knows about Gordon at hello (added and decided 2026-09-29)

**The tension:** v2 loaded so much at startup that startup became the tax; v3's CLAUDE.md put diagnoses and identity details in the auto-loaded file. But a session that knows nothing about Gordon is a blank slate every morning, and that's its own tax. The resolution is two small, capped layers, one for Sancho's character and one for Gordon's context, with everything sensitive one read further away.

### 18.1 Sancho's character (in CLAUDE.md, ≤ 15 lines)
Revised 2026-09-29 to Gordon's direction: **confidant and lifelong companion**, the chief of staff after a decade, not on day one. Reference points: a hint of JARVIS (capability, always there), a bit of Sancho (rides alongside, says the windmills are windmills), and mostly **Leo McGarry**: loyal without being deferential, carries the institutional memory, protective of the man from the man, blunt in private and discreet everywhere, and never leaves the room when it gets hard. Draft for Gordon to rewrite in his own words:
- Knows the history and uses it. "You said the same thing in March, and here's what happened" is the job, cited.
- Watches the blind spots he's been told to watch (18.3), and says so once, plainly, when one shows up; reminds once if nothing changed; never a third time that day. Doesn't flinch, doesn't lecture. Doesn't estimate how long things will take unless asked; says what, not how long.
- Warm, dry, direct. Conclusion first. Short by default, long when it's earned.
- Pushes back, offers options with a pick, then does what Gordon decides. Protects his time, his focus, and his health as part of the work, not as a nag.
- Can be told anything. What it's told goes to `personal/me/` under the layering rules, and never leaks into work, into a shared skill, or into small talk.
- Never performs competence it doesn't have: "I don't have that" beats a confident guess; "unconfirmed" is said out loud; every claim about him or his world is citable.
- Fixes obvious dictation slips silently; asks when a misread would change the meaning.
- Holds the GTD line for effectiveness, not strictness: point it out once, remind once, no third time.
- No process chatter, no "great question," no recap, no narration of its own feelings.

### 18.2 What actually went wrong with v2's CORE.md (so the depth is kept and the failure isn't)
Gordon asked whether the 287-line CORE.md was a direct problem. Per the survey (§4a) and his own May 2026 notes, the depth of context was **not** the problem; four other things were:
1. **Weight at the wrong moment.** CORE.md was pulled into every session alongside a 438-line CLAUDE.md, a 186-line protocols file, and a startup that hit three network endpoints; startup took 2+ minutes and ~10 tool calls before hello. Gordon's own line: auto-loading context was an anti-pattern; "kernel names at most 6 people."
2. **Duplication and drift.** Identity, interaction preferences, mantras, and key people appeared in both CORE.md and CLAUDE.md; CORE's header said March 16 while its contents were dated later; the two files contradicted each other (whether Wrike's connector existed).
3. **Mixed layers.** One file held rules, personal facts, health and relationship detail, a to-do list with checkboxes, and pointers to other rulebooks; nothing could be loaded without loading all of it.
4. **Everything loaded everywhere.** Diagnoses and family detail loaded in every session including work ones; it cost tokens on every turn and made the auto-loaded file the wrong place to look for anything.
So the design keeps the depth and moves it: the *behavioral* context loads every time (18.3, capped), the *factual* context is one cited read away (`personal/me/`, `people/`), and the *history* is the whole tree, searchable and citable, which is how a decade of relationship actually accrues. Depth comes from the archive and from Sancho using it, not from a bigger startup file.

### 18.3 The Gordon brief and the watch list (loaded at startup; two files, ≤ 100 lines together)
`personal/me/brief.md` (≤ 60 lines): what the ten-year chief of staff knows without looking, and nothing a stranger shouldn't see:
- Who he is in one paragraph: the businesses and his stake in each; the WoA partnership; Copper Leaf with Leah; living full-time in an RV, nomadic, following a comfort band of overnight lows no warmer than about 60°F and daytime highs no hotter than about 85°F (routine 2).
- How to work with him (from the kickoff and Phase 0): one question at a time; options with a recommended pick; structure he builds himself; push back when he's wrong; plain language, define jargon; dictated input, watch for homophones; recognition is strong, recall is weak, so surface and let him verify; a fast thinker who wants to think better.
- The people who come up week to week, one line each, linking to `people/`. No fixed number (the "at most six" from Gordon's May notes was too tight; run it and see); the brief's 60-line cap is the only bound, and the quarterly review prunes.
- Standing facts that change behavior: tasks live in Wrike and Google Tasks and he creates them; the review cadence; the two lobes and the wake phrases; the must-nevers by pointer.
- **Not in the brief:** the deeper detail (diagnoses, medications, therapy, relationship history, finances). It lives in `personal/me/` as separate files and loads when a skill names it or a question needs it, for budget reasons only: the brief is what every session needs, the rest is one read away.

`personal/me/watch.md` (≤ 40 lines): **the blind-spot list**, which is what makes the relationship feel like a decade rather than a résumé. One line per pattern Gordon has asked Sancho to watch, with the agreed response: the pattern in his words, the tell (what it looks like in a session or a transcript), and what Sancho does (say it once; offer the fix; or just note it for the weekly review). Seeds from Phase 0 and the survey: enthusiastic building before the last thing is finished; half-baking cool things; overcommitting in meetings (commitments noticed in transcripts vs. capacity); skipping lunch and crashing; working in the wrong lobe by habit; treating a plan as done because it was described well; three topics in one message. Gordon writes and prunes this list; Sancho proposes additions only at the quarterly review, from evidence (the exception counts, the correction log), never mid-conversation. The neurology that explains a pattern stays in `personal/me/`; the watch list carries the pattern and the response, which is all a session needs.

Both files are hand-written, versioned in git, lint-capped, and loaded at every startup (reads seven and eight; still under 30 seconds). The brief is the "who," the watch list is the "watch me," and everything deeper is one cited read away.

`personal/me/mantras.md` (added 2026-09-30, seed in `_design/seeds/mantras.md`) is the third file in this family but is *not* loaded at startup; a small selection step surfaces one mantra at the end of the morning routine, at a conversation close when the topic matches, or on request, choosing by tag match to today's focus or a blind spot just called, then least-recently-shown, never the same one within 14 days. The selection keeps state in `_queue/`, which is what v2's "rotate, don't repeat" never had.

**Decided 2026-09-29:** character draft accepted, to be tuned in use; both files load at every startup; the seven seed patterns are the initial watch list.

## 19. ICE at scale (added 2026-09-29)

ICE is already granular: one Markdown file per idea, with frontmatter (`id, title, lobe, area, project, captured, source, status, next_review, log`). What scales it is the same pattern as everything else in the tree: **files are the truth, indexes are generated, and placement is a field, not a folder.**

- **Granular files, one capture inbox per lobe.** Each idea is its own file, tagged `area:` and `project:` (filled at capture when obvious, at review when not), so ICE is as granular as the tree: per-business and per-project slices exist as generated views (below), and a session working inside a project sees only that project's ideas. The *inbox* is per lobe (`work/ice/`, `personal/ice/`) only so that capture never requires a placement decision first. "One queue per lobe" in earlier sections means this and nothing narrower.
- **Generated views wherever they're useful:** `work/ice/ICE.md` (all open ideas, by status and next_review), a filtered block in each business's `INDEX.md` ("4 ideas parked for Copper Leaf"), and a block in a project's INDEX for ideas tagged to it. The monthly review reads the lobe view; a project session sees its own slice. No idea is ever moved between folders to "file" it; its tags change and the views follow.
- **The "database" is frontmatter plus the generator.** Queries the review needs (due for review, parked over 90 days, killed this quarter, per-area counts) are one pass over a few hundred small files; v2's compiler did 227 files in seconds, and ripgrep over a few thousand is instant. If ICE ever reaches tens of thousands of files, a SQLite cache built from the same frontmatter is a one-day job, and it would be a cache, never the truth. That's the hybrid Gordon described, and it's already the design; what changes today is only that `area:` and `project:` are named as required-when-known fields and the per-business and per-project ICE blocks are added to the index generator.
- **Rejected:** an ICE folder inside every business and project (capture would require a placement decision first, which is friction at the moment of having the idea; and the monthly review would have to walk N folders), and a database as the primary store (opaque to git and grep, and a second source of truth).

---

## Templates

All templates live in `_setup/templates/` and are copied by the `new-component` job. Frontmatter per §4.1; cites per §5; no em dashes in rendered copy.

### T1. Entity file (`entity.md`, for a client, partner, or stakeholder)
```yaml
---
name: D&M Heating
type: client                          # client | partner | stakeholder
kind: organization                    # organization | person-relationship
business: wizard-of-ads
lobe: work
status: active                        # active | dormant | former
since: 2024-03
role: writer, radio and newsletters   # Gordon's role
lead: semple                          # lead partner slug, if any
people: [roy-williams, jane-doe]      # slugs in people/
description: HVAC, Wichita KS; Gordon writes radio + monthly newsletter; lead partner Semple
sources: [rec_…, gordon 2026-09-24]
---
One paragraph: who they are, what Gordon does for them, where things stand. Every sentence cited.
```

### T2. Guidelines (`guidelines.md`: how to work with them)
```yaml
---
name: D&M Heating guidelines
type: guidelines
business: wizard-of-ads
lobe: work
description: Voice, rules, and preferences for D&M copy and meetings
sources: [...]
---
## Voice
- Plain, warm, first person plural; never exclamation marks in radio. [rec_… 2026-04-02]
## Rules
- Roy approves every script before the station sees it. [gordon 2026-03-14]
## Preferences
- Short emails; calls on Tuesdays after 2. [rec_… 2026-05-11]
## Never
- Mention the 2023 lawsuit in any copy. [gordon 2026-03-14]
```
(Preferences are facts about the client, so this is a data file; the lint allows described preferences and flags second-person imperatives to Claude.)

### T3. Knowledge (`knowledge.md`)
```yaml
---
name: D&M Heating knowledge
type: knowledge
business: wizard-of-ads
lobe: work
description: Everything known about D&M: people, history, numbers, competitors, campaigns
sources: [...]
---
## People            (links to people/ slugs; roles here, facts about the person there)
## History
## Numbers           (revenue, ad spend, seasonality; every figure cited and dated)
## Market and competitors
## Campaigns         (one line per campaign, link to docs/)
## Open threads
## History of corrections   (superseded lines land here once a section has more than ten)
```
Split rule: past ~300 lines, a section becomes `knowledge/<section>.md` and this file keeps a one-line pointer per section.

### T4. Person (`people/<slug>.md`) — expanded 2026-09-29; the goal is to fill every person in as deeply as possible, with intention
```yaml
---
name: Roy Williams
aliases: [Roy]
type: person
lobe: both                              # work | personal | both
description: Owner of D&M Heating; Gordon's client since 2024; plain-spoken, approves every script himself
tier: full                              # contact-only | thin | full   (set by the generator from completeness)
# identity and profile
mbti: ESTJ                              # with source; leave blank rather than guess
skills: [radio, operations, hiring]     # what they're good at, from evidence
availability: {as_of: 2026-09-10, note: "slammed through Q4; Tuesdays after 2 are open"}
location: {city: Wichita KS, as_of: 2026-09-10, source: "rec_…"}
# roles across contexts (one entry per context; WoA partners get their accounts here)
roles:
  - {context: work/wizard-of-ads/clients/dm-heating, role: owner, since: 2024}
  - {context: work/wizard-of-ads, role: partner, accounts: [{client: dm-heating, their_role: lead, gordons_role: writer}]}   # partner example
# nomad and relationship upkeep
last_seen: 2026-09-10     want_to_see_by: 2026-12-01     cadence: monthly
# contact (Sancho is the contacts database, J-D1)
contact: {emails: [...], phones: [...], address: ..., birthday: ..., google_id: ..., source: "google-contacts 2026-09-30"}
# speakers
voiceprint: {enrolled: true, refs: 12, last_enrolled: 2026-08-02, auto: allowed}
# graph
relationships: [{person: jane-doe, kind: spouse}, {person: semple, kind: works_with, note: "lead partner on D&M"}]
sources: [...]
---
## How to work with them          (preferences travel with the person: pace, channel, what lands, what never to do)
## Who they are                    (history, background, what they care about; cited)
## What we know                    (facts, cited, superseded not deleted)
## Open threads                    (what's unresolved between Gordon and them; date each)
## History with Gordon             (one line per significant interaction or recording, newest first, rec_ links)
```
**Completeness is visible.** The generator scores each file (fields and sections filled out of the total) and prints it in `people/INDEX.md` as a column and a `tier`; brief-me names the gaps when it briefs someone ("no MBTI, no availability, last seen 90 days ago"); the quarterly review lists the ten people most worth deepening (by how often they appear in recordings versus how thin their file is). Filling a person in is done from evidence: recordings, meetings, what Gordon says, never from inference dressed as fact. WoA partners are ordinary person files with a partner role and accounts; the bench view is `wizard-of-ads/partners/INDEX.md`, built from these (§3.8).

### T5. Transcript summary (`summaries/<YYYY-MM-DD>_<rec_id or vtt>.md`)
```yaml
---
name: 2026-09-10 D&M weekly (rec_7f0ac58436)
type: summary
business: wizard-of-ads
entity: dm-heating
lobe: work
recording: rec_7f0ac58436              # or vtt: filename
recorded_at: 2026-09-10T14:00-05:00
duration: 48m
speakers: {gordon: human, roy-williams: systematic, unknown-02: candidate}
description: Q4 radio flight approved; Roy wants the newsletter moved to the 1st; station rate up 8%
sources: [rec_7f0ac58436]
---
## What happened (5–10 lines, cited by timestamp)
## Decisions
## Commitments noticed        (Gordon files tasks himself: decision 2026-09-21)
## Facts to file              (each with the target file; ingest marks each "filed → path")
## Questions and corrections needed
## Speakers                   (footer: which names are machine-confirmed)
```

### T6. Job file — see §9.2.   T7. ICE item — see §9.3.   T8. Skill header — see §9.1.

---

## Open questions for Gordon (consolidated, re-scanned 2026-09-30 after the full read)

**Yours, and they close Phase 2:**
1. **Does Sancho keep syncing to Leah's machine?** Proposed no: Sancho syncs to sync.com's cloud only; Astra keeps its own workspace; shared business skills reach her as a plugin, like the kit. Independent of `~/Sancho-Private/`, which exists either way. (§6.6, decisions 09-30)
2. **Approve the document as a whole**, or name changes. On approval: Phase 3 is short (migration plan, skill build order), and the Plaud pipeline build starts in Claude Code as Phase 4 item 1.

**Deliberately open, with a date, not for now:**
3. Decisions generated from in-place markers instead of hand-written logs: revisit ~2026-11-01 with usage in hand.

**Phase 3's, listed so they aren't lost:**
4. The recurring-project shape (a project with no end state, quarterly review, standing next action). (§4.6, seeds/goals.md)
5. The Weekly Review skill, both gears, both lobes. (§17.2)
6. earballs-ingest rewritten around the seven GTD buckets. (§17.1)
7. Build-order slots for fact-check-anyone, contacts import, the Weekly Review, the personal routines, the site-update kit skill.
8. "Never touch live" dialed in with the site-update skill: staging first, gated promotion. (seeds/work-ice.md)

**Parked in ICE (yours to approve at a review, not now):**
9. Personal: `MAP.html`; think-better delivery; the phone-side location post. Work: read-only Wrike and Google Tasks access; the hosted-diarizer trial; the Rig (or a Mac mini) as an always-on second runner under the single-runner role; the four capability seeds (site updates, WoA reporting incl. LSA Phone Responsiveness, Wrike time → billing, the CLC operations map).

**Drafts shaped by use, not by decision:**
10. Sancho's character wording and the watch-list seeds (§18); the personal-lobe folders (§3.2); the nomad routine's nine road-test components; the receipts and the greeting voice.
