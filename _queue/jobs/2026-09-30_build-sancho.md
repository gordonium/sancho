---
job: build-sancho
lobe: work
entity: work/copper-leaf/projects/build-sancho/
created: 2026-09-30
by: cowork
wip_limit: 3            # components maturing at once inside this job; scaffold exempt (decision 2026-09-24)
scaffold_exemption: "until B0 closes"
stages:
  - {name: scaffold,        status: done,    note: "tree, templates, lint, index, map, commands, FOCUS, brief, watch, job file (Cowork)"}
  - {name: mac-side,        status: done,    note: "done 2026-09-30: watcher + launchd, Sancho-Audio, Sancho-Secrets (age), Sancho-Private repo, autocommit fix, ping round-trip; Pushover keys still to add (Claude Code)"}
  - {name: pipeline,        status: active,  note: "port v3 code per §13.1; backward 7-day overlap; STATUS.md; Pushover test (Claude Code)"}
  - {name: open-skill,      status: done,    note: "skills/open built 2026-09-30 (Cowork); checkback skill added 2026-09-30 and ran cold twice 09-30/10-01"}
  - {name: ingest-skill,    status: done,    note: "skills/earballs-ingest built 2026-10-01 (Cowork): chunks, triage, seven buckets, corrections.md, lexicon, move, summary"}
  - {name: first-ingest,    gate: human,     status: done,    note: "rec_0c571abb1d ingested 2026-10-01; Gordon confirmed all five spot-check facts [confirmed gordon 2026-10-01]"}
  - {name: batch-B2,        status: pending, note: "WoA clients"}
current: batch-B2
hops: 2
hop_cap: 24
waiting_on:
  - {what: "GitHub migration to gordonium (both repos)", evidence: "_design/STATUS.md contains the word 'migrated' under Nerd's replies", status: done, since: 2026-09-30T22:40+02:00, done_at: 2026-09-30T23:27+02:00}
  - {what: "nerd.run command on the allowlist", evidence: "_setup/commands.md has a row starting '| nerd.run'", status: done, since: 2026-09-30T22:48+02:00, done_at: 2026-09-30T23:38+02:00}
  - {what: "Home Directions clones present", evidence: "~/Dev/clc-plugins/hdonline and hdonline-home-directions exist with files", status: done, since: 2026-09-30T22:48+02:00, done_at: 2026-09-30T22:42+02:00}
  - {what: "notify.push command on the allowlist (requested in STATUS.md 23:30; nerd.run request 20260930T222724Z_nerd.run_b0c118 queued by hop 2 at 00:27)", evidence: "_setup/commands.md has a row starting '| notify.push'", status: done, since: 2026-09-30T23:46+02:00, done_at: 2026-10-01T00:29:42+02:00}
next_when_done: "done 2026-09-30 23:46 (hop 1): work/copper-leaf/projects/hd-system-rebuild/docs/current-system.md written from the two clones"
---
# Build Sancho
The one work project that is also the system. Stages per _design/migration-plan.md §5.
