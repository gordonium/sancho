# Sancho architecture

Phase 2 deliverable. Started 2026-09-24. Built one decision at a time with Gordon; each section is written when its decision lands and cites `decisions.md`. Sections marked PENDING have not been decided. Nothing in here is built until Gordon approves the whole document (kickoff, Phase 2: "Stop and get my approval").

Reading order for a new session: STATUS.md → this file's "Decisions so far" table → the section you need. Do not reload survey.md unless a section here says "see survey" and you need the evidence.

## Decisions so far

| # | Topic | Status | Where |
|---|---|---|---|
| A | Host execution bridge | Decided: A1 queue + watcher | §1 |
| B | Layering rule (CLAUDE.md vs data vs skills vs scripts) | Decided: B1 lint; two added layers pending Gordon | §2 |
| C | Tree: lobes, spine, work lobe for N businesses, ownership field | Decided: C-i; entity folders; ICE per lobe; PM own folder | §3 |
| D | Indexes and navigation (cascade + search path); four-tier question | Decided: cascade + FOCUS.md per lobe, cap 5 | §4 |
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
| O | Leftovers: kit follow-ups, shared skills for Astra, sensitive placement, backfill | Decided: O-1..O-4 as recommended | §15 |

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

- **Request file:** Markdown with YAML frontmatter, named `<UTC timestamp>_<job>_<6 random hex>.md`. Fields: `job` (allowlisted name), `args` (map), `requested_by` (session label, e.g. `cowork` or `claude-code`), `requested_at`. Body optional (free text for the human).
- **Result file:** same name in `results/`, frontmatter `job, status (ok|failed|refused|timeout), started_at, finished_at, exit_code, log`, body = the script's one-line summary followed by its last 40 lines of output. The request is deleted on completion (atomic rename into results, never edited in place).
- **Allowlist:** `_setup/jobs.md`, a table of `job name → script path → timeout → description`. The watcher refuses any job not in the table and writes a `refused` result. Adding a job means editing the table and the map picks it up (§14).
- **Watcher:** `_setup/sancho-watcher.py`, Python 3 stdlib, run by launchd with `WatchPaths` on `requests/` plus a 60 s `StartInterval` fallback. Lockfile so two watchers never run. Per-job timeout. Loads secrets from `~/.config/sancho/env` (mode 600), **never from anything under `~/Sync/`**. Writes `HEALTH.md` after every run and every fallback tick, so a session can always read "watcher alive as of <time>".
- **Scheduled jobs stay scheduled.** Pipeline sync (hourly), map and index regeneration (nightly and on demand), git autocommit (daily, already built in `_setup/`). The queue adds on-demand triggers to the same scripts; it does not replace timers.
- **Session protocol:** write request → poll `results/` for up to the job's timeout → read result → report one line to Gordon. If no result and `HEALTH.md` is stale, say exactly that ("the Mac-side runner hasn't checked in since 09:14; is launchd loaded?"). Never pretend a job ran.
- **Git and Sync:** `_queue/` is gitignored (ephemeral). It lives inside Sync so one mount covers it; requests are tiny and short-lived, results are useful history. Unique names plus atomic renames keep sync.com from producing conflict copies.
- **Canonical path.** All Sancho jobs go through the queue from any session type, so there is one audit trail. Running a script directly from Claude Code is for developing that script, not for doing Sancho work.

**Test.** A `ping` job that writes a result containing the request ID. `_setup/test-queue.sh` submits one and waits 30 s. Startup runs it once a day and reports the round-trip time in the health line (§8).

**What this settles elsewhere:** decision #11 (the pipeline is one script on one Mac; the session triggers it through the queue instead of running it itself); #9 (commits can be requested on demand); #12 (map regeneration is a job); the personal morning routine (weather and nomad checks are jobs with keys on the Mac side).

## 2. Layering rule (Decision B: B1, blocking lint)

**The rule, one page.** Where a thing lives is decided by how often it changes and whether a machine can enforce it. Six layers. Gordon approved the first four; the two marked † are Claude's proposed additions, pending his strike-or-keep.

| Layer | Holds | Test for belonging | Never holds |
|---|---|---|---|
| **CLAUDE.md** | Identity; the must-nevers; where things live (incl. the audio folder and ID convention); a pointer to the generated skill index; the dictation line | Changes less than monthly; needed on every session; ≤ 100 lines (tokens reported by the lint) | Procedures; facts about people or clients; health or relationship details; to-dos; a hand-maintained list of skills; anything with steps |
| **Skills** | Procedures: multi-step, triggered, with a declared trigger scope (when it fires *and when it must not*), a defined end state, and a write step | Has steps a human could follow; needs judgment somewhere; carries the why/what/reads-writes/test header | Facts; rules that must never be skipped (those are hooks); guidance it goes and reads from another file |
| **Scripts, hooks, jobs** | Anything deterministic; anything that must never be skipped; anything on a timer; anything needing a key | No judgment needed, or the cost of forgetting is unacceptable | Prose instructions to the model |
| **Data files** | Facts, with provenance in frontmatter (§5) | Someone could ask "how do you know?" and the file answers with source and date | Instructions addressed to Claude (see lint note below) |
| **Generated** † | INDEX.md at every level, the system map, HEALTH.md, status views, the skill index | Produced by a script from other files; carries a `generated_by` / `generated_at` header | Hand edits, ever. (v2's and v3's "auto-generated" indexes were hand-edited and drifted.) |
| **State** † | Ephemeral: queue requests and results, job plans, the ICE queue, the in-flight (WIP) file, session orientation notes | Has a lifecycle field: `created`, and either `expires` or `deleted_when` (e.g. "on ship") | Durable facts. If it's still true after the job ends, it gets promoted to a data file with provenance. |

**Cross-layer rules.**
1. A fact lives in exactly one file; other files link to it. (Enforced: the index generator flags duplicate `name:` and duplicate aliases across frontmatter, as v2's validator did.)
2. A rule that can't fire reliably doesn't exist. Before writing a rule, name the mechanism that fires it; if there is none, it's either a skill, a hook, or nothing. (v2's own line.)
3. Client *guidelines* ("Roy prefers short emails, never use exclamation marks in his copy") are facts about preferences, so they're data. The lint distinguishes described preferences from second-person imperatives to Claude ("you must always…"); only the latter are flagged in data files.

**Enforcement (B1).** `_setup/lint-layers.py` runs as the first step of every map build (§14) and blocks the build on any violation:
- CLAUDE.md over 100 lines, or containing a numbered/bulleted step sequence longer than 3 items, or containing a name from `people/`, or containing any word from a small sensitive-terms list.
- Any data file containing second-person imperatives ("always", "never", "you must", "do not") outside a quoted block.
- Any skill missing the header or a `triggers:`/`must_not_trigger:` pair, or containing a path to a guidance file it reads instead of carrying the procedure.
- Any generated file whose content hash differs from its last generation record (hand edit).
- Any state file past `expires`, or missing a lifecycle field.
- Duplicate `name:`/alias across frontmatter.
Output is a short list: file, line, which layer it belongs in. The lint is itself a script with the standard header and a test fixture of deliberately bad files.

**Why not softer:** v3's "few rules" section grew from 6 to 16 with no mechanism; v2 reached 1,341 lines of rules across three files and nine startup definitions. Warnings were the norm in both and were ignored.

## 3. Tree, lobes, spine (Decision C) — DRAFT, one choice open

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
    <business>/             one folder per business, flat (C-i, decided)
      business.md             frontmatter: stake, role, status, parent; one-paragraph identity
      clients/<client>/       entity folders (3.6): only for businesses that have clients
      partners/<partner>/     entity folders: WoA partners Gordon works with (wizard-of-ads/ only)
      stakeholders/<person>/  entity folders: co-owners and stakeholders (tipelodeon/, entomat/, evel-spirits/)
      <other business-level folders as needed: plugins/ registry, projects/>
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
copper-leaf/        owned          Copper Leaf Creative: plugins, client sites; kit at ~/Dev/clc-plugins
press-managed/      owned-dba      parent: copper-leaf
wizard-of-ads/      partner-network  Gordonium is one of ~85 partners; 13 clients under clients/
tipelodeon/         partial 20%    Grayson Erhard founder/owner
entomat/            venture        Lizzie Mack founder; Eti, RNA partners
evel-spirits/       venture        piece of American Icon Spirits
pickleproof/        owned, dormant
```

- **C-i. Flat by business, stake in frontmatter (chosen).** Paths are stable; the stake is a fact and facts change (Press Managed went from company to DBA; SongTipper became Tipelodeon with a different stake). Frontmatter changes without breaking a single link. The index makes the stake visible. Press Managed is its own folder with `parent: copper-leaf`.
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

**The one-person rule (decision #8, settled here):** a person has exactly one file, `people/<slug>.md`, holding identity, contact pointers, voiceprint link, roles across both lobes, and *how to work with this person* (their preferences travel with them). An entity folder holds what is specific to the relationship in that business: the deal, the shared clients, the venture's knowledge, the recordings. So Lizzie Mack is one file in `people/`, referenced by `entomat/stakeholders/lizzie-mack/` and `evel-spirits/stakeholders/lizzie-mack/`, each of which holds only what belongs to that venture. A WoA partner is one file in `people/` plus `wizard-of-ads/partners/<slug>/` for the working relationship. The index generator flags any person-shaped frontmatter (`kind: person`) outside `people/`, so identity can't fork again (v2 had four partners in two places and Leah in three files).

### 3.4 Sensitive material
`personal/me/` holds health, neurology and identity facts. Nothing in it loads at startup; CLAUDE.md carries no line from it; a skill that needs it (critical-thinking's SELF dimension, the food routine's constraints) says so in its `reads:` header and loads the one file it needs. Relationship material lives under `personal/` too, never under `work/`. The lint's sensitive-terms check keeps it out of CLAUDE.md and out of `work/`.

### 3.5 The hard case: one recording, both lives
The pipeline lands every recording **once**, in `recordings/inbox/<rec_id>/` (transcript, metadata, a pointer to the audio by ID). Ingest reads it once and decides scope:
- **Single-client:** the transcript folder is *moved* (not copied) to that client's `transcripts/`, and the summary is written to its `summaries/`.
- **Personal:** moved to `personal/recordings/`, summary beside it.
- **Mixed:** the transcript stays in the spine at `recordings/<YYYY>/<rec_id>/`; each side gets its own summary, scoped to its part, linking to the transcript by ID; derived facts go to each lobe with the same `rec_id` as source.
The ledger records the final location per `rec_id`, so any session can find any recording by ID without hunting. Zoom `.vtt` files skip the inbox: the filing skill (build item 13) puts them straight into the client's `transcripts/` with a summary.

### 3.7 ICE, one queue per lobe (decision C)
Ideas are captured where they belong: `work/ice/` and `personal/ice/`, one file per idea. The ICE *procedure* (capture → interval review → MVP → evaluate → mature or kill) is one skill in the spine; the review interval is a routine entry point per lobe (§8, §9). The spine rule holds: shared procedure above the fork, lobe-specific data below it.

**Still open from §3:** anything in the personal lobe draft that's wrong (it will be shaped by the routine captures).

## 4. Indexes and navigation (Decision D: decided; focus cap number pending)

**Governing principle:** every file loaded has to earn its tokens. Nothing loads the tree wholesale. Two ways to reach a file, and every skill says which it uses: the **cascade** (navigate by structure, for known entities: "tell me about D&M") and the **search path** (navigate by content, for retrieval: "what did Roy say about radio").

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
One line per child (folders and files alike): name, type, status, last-updated, description. Alphabetical, so a line's position is stable. A 13-client index is ~15 lines, roughly 400 tokens. **Every lobe's top INDEX.md also carries a generated "Recently changed" block**: the ten most recently updated files in that lobe with their descriptions. That block is what replaces v2's hand-maintained dashboard and Hot Board, and it is what startup reads (§8).

### 4.3 The cascade and its depth budget
`CLAUDE.md` → lobe `INDEX.md` → business or area `INDEX.md` → entity `INDEX.md` → one file → (only if the file cites it and the question needs the quote) a transcript.

Rules a session follows, and a skill declares in its `reads:` header:
- Never list a folder without reading its INDEX.md first; never read a folder's files to "see what's there."
- Read `entity.md` before `guidelines.md` before `knowledge.md`; stop as soon as the question is answered.
- Never open a transcript when a summary exists, unless the summary cites it and the question needs the words.
- Cross-lobe reach is one extra index read, no ceremony.

Budgets by question type (files, not tokens, because files are what a session can count):
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

**FOCUS.md (one per lobe, the only hand-written navigation file in the system):**
```
# work · FOCUS   (cap: 5; lint-enforced)
- wizard-of-ads/clients/dm-heating/        added 2026-09-24   Q4 radio flight
- copper-leaf/plugins/                     added 2026-09-20   ship pricing plugin
```
Rules: a discrete list, **hard-capped** (cap number to be set by Gordon; 5 proposed, distinct from the WIP-3 build limit in §9); each line is a pointer to an existing file or folder plus the date it was added and a few words of why; adding a sixth means removing one first. The lint blocks the map build when the list is over cap or any pointer dangles, and warns when an entry is older than 60 days. The lobe INDEX.md prints the focus block verbatim at its top, above "Recently changed," so startup reads focus first. Nothing else in the tree may claim focus.

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

### 5.6 How git feeds provenance (decision K, part)
Every write to the tree is committed with a message naming the session type and the trigger (`cowork 2026-09-24: ingest rec_7f0…`). `git log -S "<phrase>" -- <file>` then answers *when* a fact entered and *which session* wrote it, without any extra bookkeeping. The daily autocommit already exists; the session-end and ingest write steps request a commit through the queue so the attribution is per action, not per day.

## 6. Raw vs derived (Decision F: F-1, decided 2026-09-24; transcripts and VTTs in git)

**Already decided (kickoff):** raw audio lives in `~/Sync/Sancho-Audio/`, inside sync.com, outside the Cowork mount, outside git, kept indefinitely. The tree holds the transcript, the summary, and a recording ID. Secrets live in `~/.config/sancho/env`, never under `~/Sync/` (§1).

### 6.1 Recording ID convention (goes in CLAUDE.md's "where things live")
`rec_` + 10 lowercase hex, unchanged from v2/v3 so migrated recordings keep their IDs. Audio: `~/Sync/Sancho-Audio/processed/<rec_id>.ogg` (originals never overwritten; a silence-stripped derivative, if made, is `<rec_id>.stripped.ogg`). Anything in the tree that mentions a recording uses the ID; the ledger maps ID → recorded-at, duration, current transcript location. Zoom VTTs are not recordings; their atom is the filename `YYYY-MM-DD_<entity>_<topic>.vtt`.

### 6.2 What is raw, what is derived
| Artifact | Class | Lives | In git? |
|---|---|---|---|
| audio (`.ogg`, `.m4a`) | raw | `Sancho-Audio/processed/` | never |
| `transcript.md` (pipeline) | raw (immutable) | tree, per §3.5 | **the open choice** |
| `transcript.json` (word timings, diarization segments) | raw sidecar, large (up to 2 MB) | `Sancho-Audio/processed/<rec_id>.json` | never |
| Zoom `.vtt` | raw (immutable, and *not re-derivable*: Zoom is the only source) | entity `transcripts/` | the open choice |
| `speakers.md` per recording (cluster → person, machine score, human confirmation) | derived + confirmed | beside the transcript | yes |
| summaries | derived | entity `summaries/` or `personal/recordings/` | yes |
| knowledge, guidelines, people | derived / stated / confirmed | tree | yes |
| ledger (`ledger.sqlite`) | state | `Sancho-Audio/` | never; generated `recordings/STATUS.md` is in git |

### 6.3 Git treatment of transcripts and VTTs (the open choice)
Sizes: a one-hour transcript is 50–150 KB of Markdown; v2's 696 transcripts total ~70 MB without the JSON sidecars. At Gordon's recording rate (~100 recordings/month at peak) the repo grows roughly 100–200 MB a year from transcripts alone. The pre-commit hook's 5 MB per-file cap is never hit by a transcript.
- **F-1. Transcripts and VTTs in the repo (recommended).** Text, immutable, and the thing every cite points at; git history then proves a transcript never changed after ingest, which is the strongest provenance available. VTTs especially: they can't be regenerated, so git plus sync.com plus GitHub is the right number of copies. Cost: repo size grows by a few hundred MB a year; clones get slower over years (mitigable later with shallow clones or moving old years to an archive repo).
- **F-2. Transcripts in the tree but gitignored.** Present on disk and in sync.com, absent from git history. Repo stays small. Cost: no tamper evidence for the raw layer, and a VTT deleted by mistake is gone unless sync.com's version history catches it.
- **F-3. Transcripts beside the audio in `Sancho-Audio/`, tree holds summary plus pointer.** Cleanest separation; cost: violates the requirement that a client's transcripts live in the client's folder, and the cascade would have to leave the mounted tree to read one.

### 6.4 Size limits
Per file: the existing 5 MB pre-commit cap stands. Per recording: nothing; a nine-hour ambient recording is kept as audio and transcribed once (v2 quarantined one such file; Sancho just processes it and lets the summary be short). Repo: review at 2 GB; the likely move then is one archive repo per past year.

## 7. Write discipline (Decision G: decided 2026-09-24; G-1 leases)

**The constraint (kickoff):** nothing important survives only in context. Structure makes writes happen by default; write-it-down is the backstop.

### 7.1 Writes by structure, not by nagging
1. **Every skill ends with a write step.** The skill header declares `writes:`; the lint rejects a skill with no write step or with a write step that isn't last. A thinking skill (think-first, triz) writes its output to the entity it was about, or to the lobe's `ice/` if it produced an idea, or to a session note if nothing else fits.
2. **Decisions land in a log at the level they were made.** `decisions.md` in the entity folder for client-level calls, `decisions.md` at the business level, `work/decisions.md` or `personal/decisions.md` for cross-cutting. One line each: date, decision, reason, source. Sancho's own build log is `_design/decisions.md` until Phase 4 ends, then `_setup/decisions.md`.
3. **Checkpoint writes during the conversation.** The moment a fact is confirmed, a decision made, or a correction given, the session writes it, then replies. It says what it wrote in one line ("logged to dm-heating/decisions.md"). Session end is not the write moment; it may never come.
4. **Session notes as compaction insurance.** `_queue/sessions/<session-id>.md` (state, lifecycle: deleted on clean session end after commit) holds a running list of what this session has written and what is open. If compaction or a crash hits, the next session reads it in orientation (§8) and nothing is lost that was already on disk; anything not yet written was never real.
5. **Write receipts.** Every skill's final message lists the files it wrote. Every checkpoint says the file. This is the visibility Q6 asked for.
6. **Commits per action, not per day.** The write step requests a commit through the queue (§1) with a message naming session and trigger; the daily autocommit is the safety net.
7. **write-it-down, scoped.** Gordon says "write that down" and the backstop skill files whatever was just said to the right place with a `[gordon date]` cite, and reports where. It never decides on its own to file; the structure above already does that.

### 7.2 Single writer per file (decided: G-1)
v2 lost 77% of a state file to three writers and merge auto-resolution. Sancho is one machine and mostly one session, but two sessions (Cowork and Claude Code, or two Cowork windows) can be open at once, and sync.com adds Leah's machine as a silent third path for the same bytes.
- **G-1. Session leases (recommended).** At orientation a session writes `_queue/leases/<session-id>.md` with its lobe and start time. A second session that sees a live lease on the same lobe announces it ("another session has the work lobe since 09:14") and runs read-only for that lobe until Gordon says otherwise or the lease goes stale (2 h without a checkpoint write). Leases are state with lifecycle; the watcher expires them. Cheap, visible, and it makes the two-window mistake loud instead of silent.
- **G-2. No mechanism.** Rely on one machine and habit. It is what v3 did ("single-writer files") and it held only because nothing else was running.
- **G-3. Git branches per session.** Real isolation; cost: merges inside a sync.com folder, the exact thing that produced conflict copies before.
Daemons never write into the knowledge tree except the pipeline's landing zone and generated files; the lint flags any generated file written by anything other than its generator. Leah's machine mirrors Sancho but nothing on it writes into it (Astra has its own workspace); that is a rule in CLAUDE.md, and sync.com's conflict-copy pattern (`*-CONFLICT-*`) is a lint check so a violation shows up on the next map build.

## 8. Session startup (Decision H: decided 2026-09-24; H-1 offer once)

**Goal:** orientation, not a ritual. Under 30 seconds, four generated files, one screen of output, then Gordon's question. The morning routines are separate skills with their own entry points; startup only knows whether they've run today.

### 8.1 Trigger and lobe
"Hey Sancho" (any Sancho greeting) → personal lobe. "Hey Sancho, let's work" (any greeting plus "work") → work lobe. Switching lobes mid-session is one sentence ("switch to work"), which re-runs the lobe part of orientation only.

### 8.2 What it reads (and nothing else)
1. `date` from the shell, mechanically (v2 got the weekday wrong from memory).
2. CLAUDE.md (auto-loaded).
3. The lobe's `INDEX.md`: FOCUS block first, then "Recently changed."
4. `recordings/STATUS.md`: the pipeline health line.
5. `_queue/HEALTH.md`: watcher last seen; leases; any session note left by a session that didn't close cleanly.
6. A git delta: commits since the last clean session end for this lobe (timestamp from the last lease close), summarized as counts per area, not file lists.
That's it. No inbox scans, no calendar reads, no meeting briefs, no cadence dispatch, no network checks; the morning routine owns the calendar, the pipeline owns its own alerts, and every-turn checks don't exist.

### 8.3 What it says (template, ≤ 8 lines)
```
Thu Sep 24, 2026 · personal lobe
Focus (3/5): food routine · nomad list · think-better session 1
Pipeline: 2 recordings waiting, oldest Tue 9/22 · watcher ok (09:14)
Since Tue: 6 files changed in personal/, 1 in people/
Left open last session: none          (or: "session abc12 closed dirty; note says: …")
Morning routine: not yet run today
What are we doing?
```
Every line is a read of a generated file; none is composed from memory. If a file is missing or stale, the line says so instead of guessing ("pipeline status is 3 days old; the map job may be down").

### 8.4 Cold start vs. re-sync
Same six reads. The only difference is the size of the git delta and whether a dirty session note exists. Designing two startup paths was one of v2's nine definitions; Sancho has one.

### 8.5 Handing off to the morning routine (decided: H-1)
Each lobe has a morning routine skill (build items 10 and 11). Startup knows whether it has run today from a state line the routine writes (`_queue/routines/<lobe>-morning-<date>.md`, lifecycle: 1 day).
- **H-1. Offer once (recommended).** If the routine hasn't run today and it's before noon, the last line of orientation is the offer ("Run the morning routine?"). Gordon answers yes or ignores it; startup never asks twice in a day.
- **H-2. Run it automatically** if not yet run today. Saves one exchange; it is also exactly how v2's startup grew a 20-step chain, and an afternoon re-sync would still trigger a "morning" routine unless guarded.
- **H-3. Never offer.** Gordon asks for it by name. Cleanest, and the habit he wants to build then depends entirely on him remembering, which is the thing the system exists to carry.

### 8.6 Test
A fixture tree with known files; running startup against it must produce the eight-line template with the expected values, in under 30 s, reading no file outside the list in 8.2 (the test records every path opened).

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

### 9.4 The WIP limit
`_setup/IN-FLIGHT.md`: one list, cap 3, each line a component with `started` date, its job file, and what "mature and habitual" means for it. The lint blocks the map build over cap; an ICE approval or a new build item that has no free slot is refused with the list shown. The Phase 4 scaffold exemption (decisions.md 2026-09-24) is a dated line at the top of this file and expires when the scaffold batch closes.

### 9.5 The retirement line
Retiring is a procedure with a check, never a sentence in a doc ("retired in prose, still running" was v2's pattern for a mesh, an orchestrator, a database and two skills). `retire-component` is a queue job that: (1) removes the component from `_setup/jobs.md` / the skill index / launchd (`launchctl bootout`) as applicable; (2) moves its files to `_setup/retired/<date>-<name>/`; (3) greps the tree for its name and lists every remaining reference; (4) appends a decisions line; (5) regenerates the map, which now shows it under "retired" for 90 days. The lint flags any live reference to a retired name. A component isn't retired until the job's result says zero references.

### 9.6 Where chain state lives (decided: I-1)
- **I-1. One job file per chain in `_queue/jobs/` (chosen).** As drawn above. Every open piece of multi-step work is visible in one folder; orientation lists them; a crash resumes from `current`. Cost: one more file type, and skills must read and write it (the lint checks that chain-capable skills declare `chain:`).
- **I-2. Stage status inside the target entity's files** (frontmatter on `docs/q4-radio-brief.md`, say). Fewer files; but work that spans entities (a recording that touches three clients) has no single home, and "what's open?" means scanning the tree.
- **I-3. Chain state in conversation, summarized at the end.** Rejected: this is the compaction failure by design.

## 10. People and speakers (Decision J) — DRAFT, one choice open

**Rule:** one identity per person, everywhere: the tree, both lobes, the voiceprint library, the transcripts. The slug in `people/<slug>.md` is that identity; every other place refers to it by slug.

### 10.1 The person file
```yaml
---
name: Lizzie Mack
aliases: [Elizabeth Mack, Lizzie]
type: person
lobe: both
description: Founder and leader of Entomat; also leads American Icon Spirits (Evel Spirits)
roles:
  - {context: work/entomat, role: founder, since: 2025}
  - {context: work/evel-spirits, role: lead}
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
  A correction of any auto-tag flips that person to `auto: paused` for 90 days and lists their recent auto-tags for review. The monthly ICE review shows auto-tag counts and corrections per person, so the bar can be tuned on evidence. Summaries carry one footer line naming which speakers were machine-confirmed; the body uses names plainly.
- **Enrollment quality:** a person with fewer than 3 human-confirmed references is "thin": shown so in the people index, never auto-tagged; the ingest skill asks for confirmation when such a person appears, so thin profiles thicken naturally. (v3: 17 of 32 people had a single reference.)

### 10.3 Corrections flow back (Q9 #7, Q4)
When Gordon says "that's not Roy, that's Mike," attribution-correction: (1) updates the `speakers.md` row (old value struck through, new row with `by: gordon`); (2) removes the wrong (R, N) record from the library source and adds the right one; rebuilds the library; (3) re-runs matching on every recording from the last 90 days where the wrong person was a candidate, and lists the ones whose top candidate changed for Gordon to confirm; (4) supersedes every fact filed from that recording under the wrong name, using the files' `sources:` lists (§5.4); (5) writes a decisions line and a receipt. The correction is not done until step 3's list is either empty or reviewed.

### 10.4 Contacts: Sancho is the single point of truth (decided 2026-09-24; form J-D1; Sync mirroring accepted)
Gordon's call: Sancho holds his contacts, starting with a mine of Google Contacts and a de-dupe. (v2 had 138 rows in `gordonos-people.db` from the same source; v3 had 35 people folders; the two never met.) The form is the open choice:

- **J-D1. Person files are the contacts database (recommended).** Every contact is a `people/<slug>.md`, with a `contact:` block in frontmatter (emails, phones, addresses, birthday, `google_id`, `source`, `updated`). Most of the 500-odd files will be thin (`tier: contact-only`), and the people index hides thin entries behind a count unless asked. A generated `people/CONTACTS.csv` (and vCard on demand) is the export view for syncing back to Google or Apple. De-dupe is a script over frontmatter: same email, same phone, alias collision, near-name match; it proposes merges, Gordon confirms, the merge is a supersede-and-redirect (the loser file becomes a one-line pointer, never deleted). Pros: one identity per person, really; the contact and the knowledge about them can never fork; git-diffable; the search path finds people by email. Cons: many small files; a person file now carries PII on three machines and a cloud (see below).
- **J-D2. A standalone table beside the tree** (`people/contacts.csv`, or SQLite): structured, easy to import/export and de-dupe with ordinary tools; `people/<slug>.md` exists only for people with knowledge, linked by `contact_id`. Pros: familiar shape for a contacts job. Cons: two records per person that have to agree, which is exactly the v2 smell (a people DB beside people files); SQLite is opaque to git and to grep; CSV is neither of those but still a second store.
- **J-D3. J-D1 plus a standalone DB as a cache.** Person files are truth; a script builds a SQLite or CSV from them for fast queries and for whatever contact-sync tool wants a table. This is J-D1 with the generated layer (§2) doing the "standalone DB" job, and it's what "standalone" most usefully means here.

Whichever form: the contact block is data (§2), cited like any fact (`[google-contacts 2026-09-30]`), and superseded not overwritten. **Privacy consequence to state plainly:** the whole tree mirrors to sync.com and Leah's machine, so the contacts of everyone Gordon knows will too. If that's not wanted, `people/` contact blocks could live in a sibling folder outside Sync (like `Sancho-Audio/`) and be joined by slug; that costs the one-file identity. Gordon to decide.

New roadmap item: **contacts import + de-dupe** (Google Takeout CSV in; proposed merges out; person files written through the gate). Counts as a WIP slot.

## 11. Sync and git (Decision K: composed from earlier sections; no new choice)

Already built and not redesigned: git database at `~/.sancho.git` outside Sync, private GitHub remote as history backup, knowledge-only repo (`.gitignore` blocks media; pre-commit rejects binaries and files over 5 MB), daily launchd autocommit. See `_setup/README.md`.

What Phase 2 adds, all by reference:
- **Provenance (§5.6):** every write is committed through the queue with a message naming session and trigger; `git log -S` answers when a fact entered and which session wrote it. The daily autocommit remains the net.
- **Startup deltas (§8.2, item 6):** the orientation line "since Tue: 6 files changed in personal/" is `git log --since=<last clean lease close> --name-only`, summarized by top-level area. No dashboard to maintain.
- **`updated` in every index (§4.1):** taken from git, never from frontmatter.
- **The map (§14):** regenerated by a queue job after every commit batch and nightly; the map's "changed in the last 7 days" view is a git query.
- **In git:** transcripts and VTTs (§6, F-1), summaries, knowledge, people (incl. contact blocks, §10.4), skills, scripts, generated indexes and the map, `recordings/STATUS.md`, `_setup/`.
- **Not in git:** `_queue/` (ephemeral state; results older than 90 days pruned by the watcher), audio and JSON sidecars (`Sancho-Audio/`), the ledger, secrets (`~/.config/sancho/`).
- **Sync.com conflict copies** (`*-CONFLICT-*`) are a lint check; one appearing means a second writer got in (§7.2).

## 12. Built-in memory boundary (Decision L: decided 2026-09-22)

Claude's account memory is not part of Sancho. Everything Sancho or the Copper Leaf kit needs to survive lives in Markdown files in the tree (job plans included). Built-in memory may hold nothing Sancho depends on; if it holds anything at all, it is a pointer to STATUS.md. Reason: durable, human-readable, survivable if Claude goes away, readable by any other system.

## 13. Pipeline design (Decision M) — DRAFT, one choice open

Decided so far: one runner, one Mac, no Mouth/Nerd, no ntfy, no Wrike; Groq transcription; SQLite as internal ledger with a generated status view; the black Mac keeps running v3's pipeline until this one is proven; sessions trigger it through the queue (§1). Speaker states and library rules: §10.2. Provenance: §5. Landing and filing: §3.5, §6.

### 13.1 Stages (one script, `_setup/pipeline/earballs.py`, stdlib + the same libraries v3 proved; each stage a function with the standard header)

| # | Stage | From v3 | Sancho change |
|---|---|---|---|
| 1 | Plaud fetch | `plaud-sync.py` keep w/ edits | Hourly launchd job + queue job `pipeline.sync`. Bearer token from `~/.config/sancho/env`; on 401 the health line says "Plaud token expired: re-capture" and stays red until fixed. Demo-serial filter kept. Window: newest known minus 7 days. |
| 2 | Download + ingest | keep atomic rename, sha256, `rec_` IDs | Writes `Sancho-Audio/processed/<rec_id>.ogg` + ledger row. Also watches `Sancho-Audio/inbox/` for hand-dropped files (Zoom audio, voice memos): same path, `source: external`. |
| 3 | Silence handling | `strip_silence.py` | **the open choice, 13.3** |
| 4 | Transcription | `transcribe.py` keep | Groq `whisper-large-v3`, chunking, retries; local faster-whisper as fallback only. Word JSON to `Sancho-Audio/processed/<rec_id>.json`. |
| 5 | Diarization + embeddings | `diarize.py` keep as-is | pyannote pinned; embeddings to `Sancho-Audio/voiceprints/recordings/<rec_id>.npy`. |
| 6 | Speaker match | `voiceprint.py` keep w/ edits | Library rebuilt from `speakers.md` confirmation records (§10.2); writes candidate rows and applies the auto bar. |
| 7 | Transcript write | `process.py` rewrite | `recordings/inbox/<rec_id>/transcript.md` (YAML frontmatter per §4.1, `SPEAKER_NN [t]` body), `speakers.md`, `meta.md` (Plaud metadata as data, recorded-at with offset). Ledger → `ready`. |
| 8 | Status view | new | `recordings/STATUS.md` regenerated after every run: waiting count, oldest, last sync, token state, stuck rows, auto-tag stats. This is the startup health line's source. |
| 9 | Ingest | **skill**, not code | On request (startup offers when inbox > 0): confirm speakers, extract, file per §3.5, supersede, receipt. Eight extraction passes trimmed from v3's ten; health-sensitive facts always confirmed before filing. |
| 10 | Watchdog | `pipeline-watchdog.py` keep w/ edits | Same checks (sync freshness with wake suppression, oldest waiting, stuck rows, disk, launchd counter, backup age). WARN → status view only. **CRITICAL → status view + a push to Gordon's phone** (channel: 13.6). Content: one plain, actionable line ("Pipeline: 2 recordings waiting 26 h, oldest Tue 9/22. Plaud token expired; re-capture it."). Cadence: on state change, then at most once a day while red; never a repeat every cycle. Destination hardcoded to Gordon in the script; no recipient parameter exists, so it cannot message anyone else. |
| 11 | Ledger backup | keep | Nightly `sqlite3 .backup`, keep 7, in `Sancho-Audio/`. |

Dropped: calendar-hints (needs a session to fill a cache; revisit when a calendar job exists), FTS search (ripgrep, §4.4), autotag/rehint/ignore as separate tools (folded into stage 6 with the rules in §10.2), all comms/mesh/notify tooling.

### 13.2 The 24-hour loop and the three backlogs
- **Fresh:** anything recorded from cutover onward. SLA: transcribed within 24 h of upload; the status line turns amber at 12 h waiting, red at 24 h. Ingest is offered at every startup while the inbox is non-empty; the offer names the oldest.
- **Backlogs are a separate runner state, never in the fresh queue** (v2's own lesson). `pipeline.backfill --era fresh|good|old --limit N` processes N recordings from the chosen era into `recordings/backlog/<era>/<rec_id>/`, transcribed and speaker-matched but not ingested. Order: era 3 (fresh backlog, May–Sep 2026) newest first, then era 2 (Mar–Jun 2026), then era 1 (Aug 2025–Feb 2026). **The first ingest job of all is the notes-to-self** (solo recordings, newest first, decisions.md 2026-09-22), which need no speaker confirmation.
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
A fixture recording set under `_setup/tests/pipeline/` (a 2-minute solo clip of Gordon, a 3-minute two-speaker clip, a silent clip, a corrupt file): the script must produce the expected `transcript.md`, `speakers.md` with the solo clip machine-confirmed as Gordon and the two-speaker clip left as candidates, a `refused` result for the corrupt file, and a correct `STATUS.md`. Runs as a queue job `pipeline.test`; startup reports the last test date.

### 13.5 Cutover
Run Sancho's pipeline against a copy of `Sancho-Audio/inbox/` for one week beside the black Mac's v3; compare recording counts and transcripts per day; when seven consecutive days match, retire v3's launchd jobs on the black Mac (procedure like `rainbow-rig-shutdown.md`) and revoke its Plaud token. Until then, both run.

## 14. Documentation, tests, living map (Decision N) — DRAFT, one choice open

**The requirement (kickoff):** every component carries a header (why, what, reads, writes, how to test); nothing ships without a test Gordon can run; a script regenerates a visual map daily; if a component isn't on the map, it isn't done.

### 14.1 The header, enforced
Every skill, script, job, template, and folder convention carries the same frontmatter block (§9.1 shows the skill form; scripts carry it as a docstring in the same key order: `name, type, description, why, reads, writes, test`, plus `triggers`/`must_not_trigger` for skills and `schedule` for jobs). The lint (§2) blocks the map build on a missing or empty key. Templates live in `_setup/templates/` and `new-component` is a queue job that copies the right template into place with the header pre-filled, so the cheap path is the compliant path.

### 14.2 What "tested" means
| Component | Test is | Runs as | Passes when |
|---|---|---|---|
| Script / job | `_setup/tests/<name>/` with fixture inputs and expected outputs; pytest-style | queue job `test.<name>`; all of them nightly as `test.all` | outputs match; exit 0 |
| Skill | a fixture folder (a mini tree plus a scenario file: the user's message, the expected files written, the expected trigger behaviour) | a headless Claude Code run (`claude -p`) against the fixture, launched by queue job `test.skill.<name>`; compares written files to expected and checks that the skill fired on its `triggers` and stayed silent on its `must_not_trigger` list | files match on the fields that matter (frontmatter, cites, receipts), and both trigger checks pass |
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
| launchd jobs (watcher, pipeline, map, autocommit) | run | run | run |
| Queue-job allowlist (`_setup/jobs.md`) | enforced by the watcher | enforced by the watcher | enforced |
| The lint (blocks the map build) | via queue | via queue | nightly |
| Skill `must_not_trigger` | model discipline plus the trigger test | same | n/a |
Consequence: **nothing Sancho must never skip is enforced by a session hook.** Every hard rule lives in git hooks, the watcher's allowlist, the lint, or a launchd job, because those fire whichever session (or none) is running. Session hooks are a Claude Code convenience only, used for the Copper Leaf kit's live-site guard, which is why plugin work stays in Claude Code (decisions.md 2026-09-22).

### 14.4 The living map
Generated by `_setup/build-map.py` from three inputs, no hand-maintained registry: (1) every file's frontmatter (name, type, description, lobe, reads, writes, chain, triggers, schedule, test); (2) `_setup/jobs.md` and the launchd plists; (3) git (`updated`, "changed in last 7 days"). It runs after every commit batch and nightly, as the last step after the lint and the index build, and writes:
- `MAP.md` at the tree root: the folder tree to depth 3 with counts; the skill table (name, lobe, triggers, chain links); the chain diagrams; the pipeline stage diagram; the job and schedule table; the test board; the retired list (90 days); FOCUS and IN-FLIGHT verbatim; "changed this week."
- Diagrams as Mermaid source inside `MAP.md` (renders in GitHub, Obsidian, PhpStorm, and in an Artifact).
- A dangling-reference check: any `reads:`/`writes:`/`chain:` target that doesn't exist fails the build. **A component not reachable from the map (no header, or header not parsed) fails the build.** That's the mechanical form of "if it isn't on the map, it isn't done."

### 14.5 Where the map renders (decided: N-3, sequenced)
`MAP.md` now (scaffold, in git). `MAP.html` later: a render of MAP.md only, gitignored (it inlines Mermaid.js), regenerated nightly, entered in `personal/ice/` and built when it wins a WIP slot. Options as considered:
- **N-1. `MAP.md` with Mermaid, opened wherever Gordon already reads Markdown.** Zero extra tooling; GitHub renders it on the private repo; the Cowork session can publish it as an Artifact on request for a clickable version. Cost: Mermaid gets crowded past ~60 nodes, so the map is several diagrams (tree, skills and chains, pipeline, jobs), not one.
- **N-2. A generated self-contained `MAP.html`** (inline SVG or Mermaid.js, collapsible sections) written beside `MAP.md` and opened in the browser. Prettier and navigable at scale; one more generator to maintain, and HTML in the knowledge repo is a slight oddity.
- **N-3. Both**, `MAP.md` as source of truth and `MAP.html` as a nightly render. Best view, most machinery; defer the HTML until N-1 proves too small.

## 15. Leftovers (Decision O) — DRAFT, four small choices

### 15.1 Copper Leaf kit follow-ups (from the handoff's §17)
Already done: repo `CopperLeafCreative/clc-plugin-dev-kit`, private, pushed. Still open, each with a recommendation:
1. **Leah's access:** write (she will add lessons learned; the kit's rules file is the place). Recommended: write, with `main` protected against force-push and the `wip/*` branches left force-pushable.
2. **How Leah receives it:** as a Claude Code plugin bundling the three skills and both hooks, installed the way she installs Astra; the repo doubles as the plugin source with a `.claude-plugin/` manifest. Windows port (Python path, Task Scheduler, clones outside Sync) is a job in the kit, not in Sancho.
3. **Where the kit's job plan lives:** `~/Sync/Sancho/_queue/jobs/` like every other job (decisions.md 2026-09-22: all memory in files). The kit's Core Development Rule step 3 ("save the plan to memory") is repointed to write the job file; Sancho's registry entry for the kit records that. The kit stays self-contained otherwise.
4. **Sancho's registry for the kit:** `work/copper-leaf/plugins/` with one file per plugin (repo, main file, prefix, version locations, related plugins, staging site, SSH alias, WP-CLI works?, error log verified?, quirks) and `_registry.md` generated from them. First entry of type tooling: the kit itself. Sancho **tracks** plugin jobs through the 16 stages as job files and **launches** the kit's skills; it never runs a stage itself.
5. **Lessons source of truth:** the kit's `CLAUDE.md` §12 for anything about plugin development; Sancho holds a pointer, never a copy.

### 15.2 Shared thinking skills for Astra
think-first, critical-thinking, triz, punnett-square, brief-me, and fact-check-anyone are written with **no user-specific content in the skill body**. Everything personal (the SELF dimension, the source manifest for brief-me, names, the one-line "why this exists") comes from a per-user parameter file the skill reads by a fixed relative path: `skills/_params/<user>.md` in Sancho, and the same path inside Astra's workspace. Leah consumes the skill files unchanged; Astra's current forks retire when hers are re-pointed. Work-side only (decisions.md 2026-09-22). The lint flags a shared skill whose body contains a name from `people/`.

### 15.3 Sensitive material placement (settled in §3.4)
`personal/me/` for health, neurology, identity; relationship material under `personal/`; never under `work/`, never in CLAUDE.md, never in a skill body; the lint's sensitive-terms list guards all three. The 120 relationship files under v3's `work/projects/` and v2's `health/` route to `personal/` in Phase 3 through the gate.

### 15.4 Backfill plan (settled in §13.2)
Three eras, separate runner, notes-to-self first, newest first. v2's raw `.ogg` and Plaud's cloud are the audio sources; old summaries are never copied forward.

### 15.5 Decided 2026-09-24
O-1 write access for Leah, `main` protected; O-2 plugin from the same repo; O-3 all 16 stages tracked as job files; O-4 `skills/_params/<user>.md`.

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

### T4. Person (`people/<slug>.md`)
See §10.1. Sections: How to work with them; What we know; Open threads. Contact block per §10.4. `tier: contact-only` for thin entries.

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

## Open questions for Gordon (consolidated)

All section-level choices are decided (see the table at the top and decisions.md). Remaining:
1. `MAP.html` goes in the personal ICE queue unless Gordon says work. (§14.5)
2. The personal-lobe tree is a draft to be reshaped by the routine captures. (§3.2)
3. **Approve the whole document to close Phase 2, or name what to change.**
