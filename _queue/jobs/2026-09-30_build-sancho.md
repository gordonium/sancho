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
  - {name: mac-side,        status: active,  note: "watcher + launchd, Sancho-Audio, Sancho-Secrets (age), Sancho-Private repo, autocommit fix, ping round-trip (Claude Code)"}
  - {name: pipeline,        status: pending, note: "port v3 code per §13.1; backward 7-day overlap; STATUS.md; Pushover test (Claude Code)"}
  - {name: open-skill,      status: pending, note: "temporal check, morning packet, greeting voice, lease, session note, close"}
  - {name: ingest-skill,    status: pending, note: "speaker confirmation, seven GTD buckets, filing, receipts"}
  - {name: first-ingest,    gate: human,     status: pending, note: "Gordon spot-checks five facts"}
  - {name: batch-B2,        status: pending, note: "WoA clients"}
current: mac-side
---
# Build Sancho
The one work project that is also the system. Stages per _design/migration-plan.md §5.
