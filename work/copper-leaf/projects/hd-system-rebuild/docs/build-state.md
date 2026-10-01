---
name: Home Directions v4 build state
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Where the overnight build stands: each track's stages, which agent has which, what passed review; kept by the planning thread so the run survives a loss of memory
sources: ["[doc:build-handoff.md]", "[gordon 2026-10-02]"]
status: live during the build that started 2026-10-02 00:55
---
# Build state

Started 2026-10-02 00:55 on "Approved, GO!" [gordon 2026-10-02]. Rules and scope: `build-handoff.md`. Each stage goes build, then review (findings in `docs/reviews/`), then fix. The orchestrating thread updates this file every time an agent reports; it starts the next stage of a track only when the one before is fixed and its tests pass.

## Stages

| Track | Stage | What | Status |
|---|---|---|---|
| Kit | K1 | scaffold (rules file, per-project template and lint, lessons, ledger, installer) and both guards with tests | building since 00:55 |
| Kit | K2 | gate script, ship script, project template | waiting |
| Kit | K3 | skills, plan-gate and model-and-effort hooks, updates calendar and "what is due", parity skill | waiting |
| App | P1 | step C: skeleton, tables, three logins, Dashboard and File by hand, duplicate prompts | building since 00:55 |
| App | P2 | steps D and E: letters, invoices with real PDFs, mail, against stand-ins | waiting |
| App | P3 | steps F and G: Calendly, search, change history, delete and restore, Settings and Connections | waiting |
| App | P4 | import and letter conversion as code, then the rehearsal on the real history; demonstration set; browser tests | waiting |
| Paperwork | W1 | account checklists, backup setup, cutover runbook, dress-rehearsal script | building since 00:55 |
| Paperwork | W2 | one-page how-tos for Peter and Maria Pia (after P3, from the real screens) | waiting |
| All | Z | final summary in `build-log.md`, one line in `project.md` | waiting |

## Log of hand-offs
- 00:55 K1, P1 and W1 started.
