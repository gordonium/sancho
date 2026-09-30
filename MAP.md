# Sancho · MAP
generated 2026-10-01 by build-map.py. Three zoom levels; Level 0 is the picture to remember.

## FOCUS

# FOCUS   (cap: 3 per lobe per horizon; lint-enforced; hand-set with Gordon, never generated)
## month · 2026-09
work:     Build Sancho · (open) · (open)
personal: (open) · (open) · (open)
## week · 2026-09-30
work:     scaffold + pipeline running · (open) · (open)
personal: (open) · (open) · (open)
## today · 2026-09-30
work:     scaffold the tree · first lint/index/map run · (open)
personal: (open) · (open) · (open)
exceptions this week: 0

## Level 0 · the system

```mermaid
flowchart LR
  CAP[Capture: Plaud · Zoom · calendar · dictation]
  PIPE[Pipeline on the Mac: fetch → transcribe → diarize → voiceprint]
  LAND[Landing zone: recordings/inbox]
  ING[Ingest: a session, 7 GTD buckets]
  TREE[(The tree: spine · work · personal)]
  SES[Sessions: Cowork · Claude Code · phone via Dispatch]
  Q[Queue + Mac: commands · schedules · watcher]
  OUT[Outputs: indexes · MAP · STATUS · Pushover]
  CAP --> PIPE --> LAND --> ING --> TREE
  SES <--> TREE
  SES --> Q --> PIPE
  Q --> OUT
  TREE --> OUT
```

## Level 1 · components

### The tree
```mermaid
flowchart TB
  S[spine: CLAUDE.md · people · skills · recordings · _queue · _setup]
  W[work]
  P[personal]
  S --> W
  S --> P
  W --> W_american_icon_spirits[american-icon-spirits]
  W --> W_copper_leaf[copper-leaf]
  W --> W_entomat[entomat]
  W --> W_pickleproof[pickleproof]
  W --> W_tipelodeon[tipelodeon]
  W --> W_wizard_of_ads[wizard-of-ads]
  P --> P_finances[finances]
  P --> P_food[food]
  P --> P_horizons[horizons]
  P --> P_learning[learning]
  P --> P_me[me]
  P --> P_nomad[nomad]
  P --> P_projects[projects]
  P --> P_recordings[recordings]
  P --> P_rv[rv]
```
### Skills by family
```mermaid
flowchart LR
  subgraph gtd
    open[open]
  end
  subgraph other
    checkback[checkback]
  end
  checkback --> the
  open --> the
```
### Pipeline stages
```mermaid
flowchart LR
  A[1 Plaud fetch 5-min] --> B[2 download + ledger] --> D[4 Groq transcribe] --> E[5 diarize + embed] --> F[6 voiceprint match] --> G[7 transcript + speakers.md] --> H[8 STATUS.md]
  C[5b calendar feed] --> E
  Z[Zoom poll] --> G
  H --> I[9 ingest skill]
  W[10 watchdog] -.-> H
```
### Active projects

- **Plan the Alaska trip (2027)** (personal/nomad) · next: Read 07-open-questions.md and pick the first one to close
- **Food routine to habit** (personal/food) · next: Design the Sunday session skill (build order #6); first session picks four dinners
- **Nomad daily check** (personal/nomad) · next: Design the personal morning routine incl. the nomad check (build order #5)
- **Build Sancho** (work/copper-leaf) · next: Claude Code on the Mac: watcher, launchd, Sancho-Audio, Sancho-Secrets, Sancho-Private, autocommit fix, ping
- **Home Directions system rebuild** (work/copper-leaf) · next: Gordon reviews docs/plan.md and answers questions 1 to 3 (stack, Workspace, hosting); then Sancho runs the data census on the dev clone (needs the Chrome login) and the Nerd gets step 1 as a job

## Changed this week

- .gitignore
- CLAUDE.md
- FOCUS.md
- INDEX.md
- MAP.md
- _design/STATUS.md
- _design/Sancho-Architecture-standalone.html
- _design/architecture.md
- _design/build-reading-copy.py
- _design/decisions.md
- _design/migration-plan.md
- _design/postmortem.md
- _design/routines-capture.md
- _design/sancho-architecture.html
- _design/sancho-tree.html
- _design/seeds/goals.md
- _design/seeds/mantras.md
- _design/seeds/to-read.md
- _design/seeds/work-ice.md
- _quarantine/.gitkeep
- _queue/checkbacks.md
- _queue/jobs/2026-09-30_build-sancho.md
- _queue/jobs/_archive/.gitkeep
- _queue/jobs/_archive/2026-09-30_jobrun-smoke.md
- _setup/ERRORS.md
- _setup/GIT-EXCLUDED.md
- _setup/LINT.md
- _setup/MAC-SETUP.md
- _setup/README.md
- _setup/TESTS.md
- _setup/build-index.py
- _setup/build-map.py
- _setup/com.sancho.autocommit-private.plist
- _setup/com.sancho.nightly.plist
- _setup/com.sancho.pipeline.plist
- _setup/com.sancho.tests.plist
- _setup/com.sancho.watcher.plist
- _setup/commands.md
- _setup/git-autocommit.sh
- _setup/hooks/INDEX.md
- _setup/index-manifest.json
- _setup/install-mac.sh
- _setup/job-run.py
- _setup/lint-layers.py
- _setup/metered-networks.md
- _setup/nerd-run.py
- _setup/nerd-settings.json
- _setup/netstate.py
- _setup/nightly.sh
- _setup/notify-test.sh
- _setup/notify.py
- _setup/ping.sh
- _setup/pipeline/INDEX.md
- _setup/pipeline/earballs.py
- _setup/pipeline/earballs.sh
- _setup/pipeline/install-venv.sh
- _setup/pipeline/requirements.txt
- _setup/retired/INDEX.md
- _setup/sancho-enqueue.py
- _setup/sancho-lock-secrets.sh
- … +346 more

## Level 2 · wiring

<details><summary>Skills: triggers, reads, writes, tests</summary>

| skill | lobe | triggers | must not | reads | writes | test |
|---|---|---|---|---|---|---|
| checkback | both | a scheduled-task prompt that says: open job <name>; run checkback, check on the Nerd, did the Nerd finish, where is job <name> | a conversation where Gordon is present and just asked the Nerd something himself, a job with no waiting_on block, any request to create tasks for Gordon, anything outbound | CLAUDE.md, _queue/jobs/<job>.md, _queue/checkbacks.md, _design/STATUS.md, _queue/results/, _queue/running/, _queue/HEALTH.md, _setup/commands.md | _queue/checkbacks.md (one row filled or appended), _queue/jobs/<job>.md (hops, waiting_on statuses, stage status), _design/STATUS.md (one line under ### Check-backs), _queue/requests/ (notify.push; nerd.run when it exists), the next scheduled task, or none | _setup/tests/skills/checkback/ |
| open | both | Hey Sancho, hey sancho, any greeting addressed to Sancho, let's work, switch to work, switch to personal, done, thanks Sancho, that's it for this one, close | a message that continues an open conversation, a question inside a job, the word sancho used in the third person, a Nerd build session that already stated its task | CLAUDE.md, personal/me/brief.md, personal/me/watch.md, personal/nomad/location.md, <lobe>/INDEX.md, <lobe>/PROJECTS.md, recordings/STATUS.md, _queue/HEALTH.md, _queue/leases/, _queue/sessions/, _queue/routines/<lobe>-morning-<date>.md, the project.md of each project in today's focus, git log since the last clean close | _queue/leases/<session-id>.md, _queue/sessions/<date>_<topic>_<id>.md, on close: a receipt in the session note, the note folded into the project's history or the lobe's day log, the lease removed, a git.commit request in _queue/requests/ | _setup/tests/skills/open/ |

</details>

<details><summary>Commands and schedules (from _setup/commands.md)</summary>

| ping | _setup/ping.sh | 10 | | round-trip test: writes a result containing the request id |
| index.build | _setup/build-index.py | 120 | after commits; nightly 02:00 | regenerate every INDEX.md, PROJECTS.md, ICE.md, people and skill indexes |
| lint | _setup/lint-layers.py | 120 | before every map build; nightly | layering, caps, headers, generated-file integrity, stale next actions |
| map.build | _setup/build-map.py | 120 | after index.build; nightly | regenerate MAP.md (three zoom levels) |
| docs.reading-copy | _design/build-reading-copy.py | 60 | on demand | rebuild the architecture reading copy and standalone HTML |
| test.all | _setup/test-all.py | 600 | nightly 02:30; after commits touching _setup/ or skills/ | run every test suite; write TESTS.md; exit 1 on any failure |
| git.commit | _setup/git-autocommit.sh | 120 | hourly (launchd direct, not via the queue); at conversation close | commit and push the tree (skips oversize files, lists them in GIT-EXCLUDED.md) |
| nightly | _setup/nightly.sh | 300 | nightly 02:00 (com.sancho.nightly enqueues it) | index.build, then lint, then map.build; stops at the first failure |
| notify.test | _setup/notify-test.sh | 30 | | args [info] / [warn] / [alert]: send one test push to Gordon's phone at that level |
| notify.push | _setup/notify.py | 30 | | args [info or warn or alert, <message>]: one Pushover push to Gordon; warn only when he must act soon, info for FYI ("Warn means WARN", decisions 2026-09-30); deduped per key; a comma in the message arrives whole |
| mac.stay-awake | _setup/stay-awake.sh | 20 | | args [on] / [off] / [status]: keep the Mac from idle-sleeping (caffeinate under launchd) |
| sancho.unlock | _setup/sancho-unlock.sh | 60 | Terminal only | decrypt Sancho-Secrets/sancho.env.age to ~/.config/sancho/env (asks for the passphrase) |
| sancho.lock-secrets | _setup/sancho-lock-secrets.sh | 60 | Terminal only | re-encrypt ~/.config/sancho/env after an edit (asks for the passphrase twice) |
| pipeline.sync | _setup/pipeline/earballs.sh | 3000 | every 5 min (com.sancho.pipeline, launchd direct) | "sync now": Plaud list, download, transcribe, diarize, write recordings/inbox/, STATUS.md; args [sync, --full] for a full reconcile |
| pipeline.backfill | _setup/pipeline/earballs.sh | 7200 | on demand until the fresh overlap is through; [heavy] | args [backfill, --era, auto, --limit, 20]: backlog into recordings/backlog/<era>/, capped at 6 audio-hours a day |
| pipeline.reprocess | _setup/pipeline/earballs.sh | 3000 | | args [reprocess, rec_x, --num-speakers, N]: re-diarize with a confirmed count; writes transcript.vN.md, supersedes speakers.md |
| pipeline.library | _setup/pipeline/earballs.sh | 600 | after ingest confirms speakers | args [library]: rebuild the voiceprint library from human-confirmed speakers.md rows |
| pipeline.status | _setup/pipeline/earballs.sh | 60 | | args [status]: regenerate recordings/STATUS.md |
| net.status | _setup/netstate.py | 20 | every watcher tick (in-process) | which network, metered or not (router fingerprint vs _setup/metered-networks.md) |
| net.mark | _setup/netstate.py | 20 | | args [mark, <label>, metered or unmetered]: record the network the Mac is on now |
| nerd.run | _setup/nerd-run.py | 1900 | | headless Claude Code (the Nerd) for the task in the request (`task:`, `task_file:`, or body); allowlisted tools, OS sandbox, no MCP, no push/commit/web; one at a time; transcript in _queue/results/ |
| job.run | _setup/job-run.py | 60 | | args [<job name or file>]: walk a job file stage by stage via nerd.run (detached; progress in the job file); stops at a human gate or after two failures of a stage, with one push |

</details>

<details><summary>Scripts</summary>

- `_setup/netstate.py` · Which network the Mac is on and whether it is metered. Fingerprint = the default gateway's MAC (macOS hides the Wi-Fi name without Location permission). Policy from _setup/metered-networks.md; unknown networks are metered while the policy date runs. `mark <label> metered|unmetered` records the current network.
- `_setup/sancho-enqueue.py` · Write one request file to _queue/requests/ (the documented name and frontmatter), optionally wait for its result and print it. Used by launchd schedules and by sessions that have a shell.
- `_setup/sancho-watcher.py` · One tick of the host execution bridge. Runs every allowlisted request in _queue/requests/, writes one result per request to _queue/results/, then rewrites _queue/HEALTH.md. Exits; launchd calls it again on any change to requests/ and every 60 s.
- `_setup/sancho_lib.py` · Shared helpers for Sancho's build scripts: find the tree, read YAML-ish frontmatter without PyYAML, walk files, ask git for last-updated dates.
- `_setup/pipeline/earballs.py` · The recording pipeline. Plaud fetch (incremental every 5 min, full reconcile daily) → download → Groq transcription → pyannote diarization + embeddings → voiceprint match → transcript.md / speakers.md / meta.md in recordings/inbox/ → recordings/STATUS.md → watchdog push. Also backfill, reprocess, library rebuild.
- `_setup/build-index.py` · Regenerate every INDEX.md in the tree (one line per child from frontmatter), each lobe's PROJECTS.md, the ICE views, the people index with completeness, and the skill index. Never hand-edited outputs.
- `_setup/build-map.py` · Regenerate MAP.md, the living map, in three zoom levels: Level 0 the system (one Mermaid diagram, ≤8 boxes), Level 1 components per box, Level 2 wiring tables (reads/writes/triggers/tests/commands/retired). Built only from frontmatter, commands.md and git; no hand-kept registry. Fails if a component has no parsable header or a reads/writes/chain target does not exist.
- `_setup/job-run.py` · Walk a job file (_queue/jobs/*.md) stage by stage, running each stage as a nerd.run session, advancing `current` on success, stopping at any `gate: human` stage; a failed stage is retried once, then the job stops. Pushes are info (silent): the greeting reports job state; warn is only for timely attention (Gordon, 2026-09-30). Detaches at once so the watcher stays free; progress lives in the job file.
- `_setup/lint-layers.py` · Enforce the layering rule (architecture §2), the focus caps, the header rule, generated-file integrity, project next-action and waiting-for freshness, and dangling references. Exit 1 on any violation so the map build fails.
- `_setup/nerd-run.py` · Run one headless Claude Code session (the Nerd) on the Mac for a task given in the request (frontmatter `task:`, `task_file:` inside the tree, or the request body). Fixed tool allowlist, OS sandbox (writes only in the tree and the kit; network only GitHub and Anthropic), no MCP connectors, no outbound messaging, timeout, lease while running, transcript kept, one-line receipt.
- `_setup/notify.py` · Send one Pushover message to Gordon. Level sets priority (info -1, warn 0, alert 1). Rule (Gordon, 2026-09-30): "Warn means WARN": warn makes his phone sound and is only for things needing his attention soon (today: the pipeline red, i.e. recordings not flowing). Everything else is info (silent, in-app) or nothing; no chatter. Deduped per key: sends when the message for a key changes, otherwise at most once a day.
- `_setup/test-all.py` · Run every test under _setup/tests/*/ (test.sh or test.py), write _setup/TESTS.md (the test board), exit 1 if any fails. Off the Mac, suites whose header says `requires: mac` are skipped and the board is not written (ERRORS.md

</details>

<details><summary>LINT.md</summary>

# LINT
generated 2026-10-01 by lint-layers.py

**0 problems, 0 warnings**

## Problems (block the build)

## Warnings

</details>

<details><summary>TESTS.md</summary>

# TESTS
generated 2026-09-30 23:59 by test-all.py · 19 suites · 0 failing

| suite | result | last line |
|---|---|---|
| build-index | PASS | test-build-index: PASS |
| build-map | PASS | test-build-map: PASS |
| git-autocommit | PASS | test-git-autocommit: PASS |
| install-mac | PASS | test-install-mac: PASS |
| job-run | PASS | test-job-run: PASS |
| lint-layers | PASS | test-lint-layers: PASS |
| nerd-run | PASS | test-nerd-run: PASS |
| netstate | PASS | test-netstate: PASS |
| nightly | PASS | test-nightly: PASS |
| notify | PASS | test-notify: PASS |
| ping | PASS | test-ping: PASS |
| pipeline | PASS | test-pipeline: PASS |
| sancho_lib | PASS | test-sancho_lib: PASS |
| secrets | PASS | test-secrets: PASS |
| stay-awake | PASS | test-stay-awake: PASS |
| test-all | PASS | test-test-all: PASS |
| watcher | PASS | test-watcher: PASS |
| skill:checkback | PASS | test-skill-checkback: PASS (structural; behavioral scenario runs on the Mac) |
| skill:open | PASS | test-skill-open: PASS (structural; behavioral scenario runs on the Mac) |

</details>

<details><summary>Retired (90 days)</summary>

- INDEX.md
</details>
