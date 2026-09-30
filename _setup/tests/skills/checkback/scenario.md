---
name: checkback skill scenario
type: doc
lobe: both
description: Headless test scenario for the checkback skill: fixture job with waiting_on items, fake results and HEALTH, expected log row, job edits, push level and next task
---
# Scenario: checkback

Run headless (`claude -p`) against a temp copy of the fixture tree with SANCHO_ROOT pointing at it, a fake `date` returning `2026-10-01 00:25 CEST`, and a stub for the scheduled-task tool that records what would be created.

## Case 1: one item done, one waiting
- Fixture: job `x` with `hops: 0`, `hop_cap: 24`, two `waiting_on` items; a result file `…_ping_…md` with `status: ok`, `finished_at` 00:10, satisfying item 1; HEALTH.md watcher seen 00:24, awake.
- Expected: item 1 `status: done`, `done_at` 00:10; item 2 unchanged; `checkbacks.md` gains or fills one row with `fired` 00:25, `nerd_done` 00:10, `idle` 15 min; job `hops: 1`; one info push request; exactly one one-time task created, planned within 10–60 min; one STATUS.md line.

## Case 2: everything done, next stage is a human gate
- Expected: current stage marked done, `current` advanced, no task created, a warn push naming what Gordon needs to do, STATUS line ends "next none: gate".

## Case 3: cap reached
- Fixture: `hops: 24`.
- Expected: no evidence checks needed; no task; warn push with reason cap; one STATUS line.

## Case 4: Nerd asleep
- Fixture: HEALTH.md watcher last seen 3 h ago.
- Expected: items unchanged, no push (nothing changed), next task at the longer clamp (60 min), STATUS line says waiting on the Mac.

## Case 5: run twice
- Run Case 1 twice with the same fixture clock.
- Expected: second run adds no second row, no second task, no second STATUS line, no second push.

## Must not, in every case
- Rewrite `checkbacks.md`, the job file or STATUS.md wholesale (the harness diffs untouched lines).
- Mark any item done on a prose claim (fixture STATUS.md contains "migration done, honest" in prose without the evidence string).
- Create a cron task.
