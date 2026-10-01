---
name: Check-back log
type: state
description: Every one-time scheduled check-back, planned vs actual, and the idle gap between the Nerd finishing and Cowork noticing; used to dial in estimates
lobe: both
---
# Check-back log

One row per scheduled check. Times Europe/Rome unless noted. `nerd_done` from the result file or STATUS.md timestamp; `idle` = fired − nerd_done (negative means the Nerd was not done yet).

| set_at | planned | fired | job/handoff | found | nerd_done | idle | note |
|---|---|---|---|---|---|---|---|
| 2026-09-30 22:55 | 2026-10-01 00:08 | cancelled | migration + nerd.run + HD current-system | | | | far too generous (Gordon); Gordon deleted it, we were talking |
| 2026-09-30 23:05 | 2026-10-01 02:30 | cancelled | same, second | | | | same |
| 2026-09-30 23:28 | 2026-09-30 23:45 | 2026-09-30 23:46 | migration + nerd.run + HD current-system (quick turn) | all three done; current-system.md written (hop 1) | 2026-09-30 23:38 | +8 min | log says halve (17→10 min) but the 00:25 task already exists; reused it, none created |
| 2026-09-30 23:29 | 2026-10-01 00:25 | 2026-10-01 00:25 | same (longer) | notify.push still not on the allowlist; Nerd alive, idle (nothing running since 23:56); nerd.run request queued for it (hop 2) at 00:27; the Nerd finished it while this hop was still open (result ok 00:29:42, row verified before close) | 2026-10-01 00:29 | -4 min | last interval 56 min, hop-1 idle +8 → halve → 28 min; the 00:53 task could not be created (scheduled-task creation declined: nobody present to approve); chain ends with nothing left to wait on |
| 2026-10-01 00:27 | 2026-10-01 00:53 | not created | notify.push via nerd.run (hop 3) | | | | creation declined in the cold run (needs approval); moot: the Nerd was done at 00:29 |
