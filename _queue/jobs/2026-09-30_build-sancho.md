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
  - {name: open-skill,      status: pending, note: "temporal check, morning packet, greeting voice, lease, session note, close"}
  - {name: ingest-skill,    status: pending, note: "speaker confirmation, seven GTD buckets, filing, receipts"}
  - {name: first-ingest,    gate: human,     status: pending, note: "Gordon spot-checks five facts"}
  - {name: batch-B2,        status: pending, note: "WoA clients"}
current: pipeline
hops: 1
hop_cap: 24
waiting_on:
  - {what: "GitHub migration to gordonium (both repos)", evidence: "_design/STATUS.md contains the word 'migrated' under Nerd's replies", status: done, since: 2026-09-30T22:40+02:00, done_at: 2026-09-30T23:27+02:00}
  - {what: "nerd.run command on the allowlist", evidence: "_setup/commands.md has a row starting '| nerd.run'", status: done, since: 2026-09-30T22:48+02:00, done_at: 2026-09-30T23:38+02:00}
  - {what: "Home Directions clones present", evidence: "~/Dev/clc-plugins/hdonline and hdonline-home-directions exist with files", status: done, since: 2026-09-30T22:48+02:00, done_at: 2026-09-30T22:42+02:00}
  - {what: "notify.push command on the allowlist (requested in STATUS.md 23:30; the checkback chain pushes through it)", evidence: "_setup/commands.md has a row starting '| notify.push'", status: waiting, since: 2026-09-30T23:46+02:00}
next_when_done: "done 2026-09-30 23:46 (hop 1): work/copper-leaf/projects/hd-system-rebuild/docs/current-system.md written from the two clones"
---
# Build Sancho
The one work project that is also the system. Stages per _design/migration-plan.md §5.
