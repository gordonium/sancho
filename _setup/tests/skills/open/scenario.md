---
name: open skill scenario
type: doc
lobe: both
description: Headless test scenario for the open skill: fixture tree, three user messages, expected facts in the greeting, expected files written
---
# Scenario: open

Run headless (`claude -p`) against a temp copy of the fixture tree with SANCHO_ROOT pointing at it and a fake `date` on PATH returning `Tuesday 2026-09-29 08:40 CEST`.

## Case 1: first open of the day, personal
- Message: "Hey Sancho"
- Expected facts in the greeting (order-insensitive, wording free): weekday Tuesday and date 2026-09-29; place from personal/nomad/location.md; the three personal focus items from FOCUS.md with each project's next action; the pipeline line from recordings/STATUS.md verbatim in meaning ("2 waiting, oldest 09-27" in the fixture); "nothing changed" (fixture git log empty); no stale lease; ends with the routine offer and NOT the topic question.
- Expected files: `_queue/leases/<id>.md` with lobe personal (only after the topic is given); no session note yet.
- Must not: read any file outside the packet list (the harness records opened paths); exceed 8 lines; contain "Focus (" or "watcher ok (".

## Case 2: second open, work, topic given
- Precondition: `_queue/routines/work-morning-2026-09-29.md` exists (routine ran).
- Message: "Hey Sancho, let's work on the D&M radio scripts"
- Expected: two lines; no routine offer; a lease with scope containing `work/wizard-of-ads/clients/dm-heating/`; a session note named `2026-09-29_dm-radio-scripts_*.md`; the D&M `entity.md` opened after the greeting, not before.

## Case 3: stale lease found
- Precondition: a lease for work scope `work/wizard-of-ads/clients/dm-heating/` with `checkpoint` 3 h old and a session note with one written file.
- Message: "Hey Sancho, let's work"
- Expected: greeting mentions the left-open conversation and what its note says; the lease is moved to `_closed/` with `closed: stale …`; the note is marked closed.

## Case 4: close
- Message: "thanks, Sancho" in an open conversation whose note lists two written files.
- Expected: receipt appended to the note; note moved to `_queue/sessions/_closed/`; lease moved to `_queue/leases/_closed/`; a `git.commit` request file exists in `_queue/requests/`; reply is two lines ending "Closed."

## Trigger checks
- Fires on: "Hey Sancho", "hey sancho, what's on today", "switch to work", "done".
- Stays silent on: "Sancho is the name of the system" (third person), a follow-up message inside a job, the Nerd's build prompt (already states its task).
