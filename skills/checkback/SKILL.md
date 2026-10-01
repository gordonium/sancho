---
name: checkback
type: skill
lobe: both
shared:
description: A cold Cowork run (one-time scheduled task) checks whether the Nerd finished what a job is waiting on, logs planned-vs-actual timing, does the job's next mechanical stage if one is ready, pushes an info per hop, and schedules the next check-back while the job is unfinished and under its hop cap.
why: Cowork and the Nerd should keep a job moving without Gordon relaying between them. A scheduled run starts with no memory, so the whole context must be the job file plus this procedure; the first hand-written check-back prompts proved that context in a prompt drifts and can't be tested.
triggers: ["a scheduled-task prompt that says: open job <name>; run checkback", "check on the Nerd", "did the Nerd finish", "where is job <name>"]
must_not_trigger: [a conversation where Gordon is present and just asked the Nerd something himself, a job with no waiting_on block, any request to create tasks for Gordon, anything outbound]
reads: [CLAUDE.md, "_queue/jobs/<job>.md", _queue/checkbacks.md, _design/STATUS.md, _queue/results/, _queue/running/, _queue/HEALTH.md, _setup/commands.md]
writes: ["_queue/checkbacks.md (one row filled or appended)", "_queue/jobs/<job>.md (hops, waiting_on statuses, stage status)", "_design/STATUS.md (one line under ### Check-backs)", "_queue/requests/ (notify.push; nerd.run when it exists)", "the next scheduled task, or none"]
chain: {front: "a handoff to the Nerd inside a job", next: "the job's next stage skill when its evidence is present", gate: "hop cap in the job file (default 24); a human gate stage stops the chain and warns"}
test: _setup/tests/skills/checkback/
---
# checkback

One hop of the Cowork↔Nerd loop. Everything here is a read of a file or a shell call; nothing is remembered between hops. Idempotent by construction: every write first checks whether it already exists.

## What the job file carries (the contract)

```
hops: 3            # hops taken so far on this job
hop_cap: 24        # Gordon's cap [gordon 2026-09-30]; chain stops here with a warn
waiting_on:
  - {what: "GitHub migration to gordonium", evidence: "STATUS.md contains 'migrated'", status: waiting, since: 2026-09-30T22:40+02:00}
  - {what: "nerd.run command", evidence: "_setup/commands.md has a row starting '| nerd.run'", status: waiting, since: ...}
next_when_done: "write work/copper-leaf/projects/hd-system-rebuild/docs/current-system.md from the clones"   # optional: a mechanical step Cowork does once everything above is done
```

`evidence` is always a file test a cold run can perform: a path exists, a file contains a string, a result file for command X with `status: ok` newer than `since`. Never "the Nerd says it's done."

## Procedure

1. **Time, mechanically.** `date "+%Y-%m-%d %H:%M %Z"` in the shell. This is `fired`.

2. **Open the job.** Read `_queue/jobs/<job>.md`. No `waiting_on` block → write one line under `### Check-backs` in STATUS.md ("checkback on <job>: nothing to wait on; stopped") and stop. `hops >= hop_cap` → step 8 with reason "cap".

3. **Check each `waiting_on` item against its evidence**, literally (grep, ls, test -f). For each item now satisfied: set `status: done`, record `done_at` as the newest timestamp that proves it (`finished_at` in the result file, the STATUS.md line's own time, or the file's mtime), and flip nothing else. Never mark an item done on a claim in prose.

4. **Log the hop.** In `_queue/checkbacks.md`: if a row exists whose `planned` matches this task's fire time, fill that row (`fired`, `found`, `nerd_done`, `idle`); otherwise append one. `nerd_done` = the latest `done_at` among items that became done since the last hop; `idle` = fired − nerd_done, or "nerd not done". `found` is a few words. Edit that row only; never rewrite the file.

5. **Is the Nerd alive?** Read `_queue/HEALTH.md`: watcher last seen within 10 min and Mac awake → alive. Anything in `_queue/running/` older than its command's timeout in `commands.md` → stuck. Not alive → the chain waits, not fails: skip to step 7 with the longer interval.

6. **If everything is done:** run `next_when_done` if the job names one and it is mechanical (writing a doc from files, filing, a request); otherwise set the current stage `done`, advance `current`, and if the next stage has `gate: human` stop the chain (step 8, reason "gate"). If work remains for the Nerd, write the request (`nerd.run` when that command exists in `commands.md`; until then a note under "Requests to the Nerd" in STATUS.md) and add a new `waiting_on` item with file-testable evidence.

7. **Next hop.** `hops += 1` in the job file. Interval from the log, not from feel: take the last five rows of `checkbacks.md` for this job that have a `nerd_done`; if the median `idle` is positive (we were late) halve the last interval; if the Nerd was not done at the last hop, double it; clamp to 10–60 min; no history → 10 min for the first hop, 30 for the second. If this hop itself queued short Nerd work (`nerd.run`), wait in-hop up to 5 min for the result before scheduling anything; most Nerd turns finish in two minutes [checkbacks.md 2026-10-01]. Do not create a new task per hop: a new task has no stored approvals, so a cold run cannot create it. Instead each job has **one** standing task (`sancho-checkback-<job>`), and the hop re-arms it with `update_scheduled_task` (`fireAt` = next time); the approval for that update is granted once (Gordon clicks "Run now" or approves the first live hop) and is stored on the task for every later run; with Gordon's tools set to auto-allow [gordon 2026-10-01] no prompt appears at all, and the standing task is still the shape, for one task per job rather than one per hop. The task's whole prompt is: "You are Sancho. Read /Users/gordonium/Sync/Sancho/CLAUDE.md. Open job `_queue/jobs/<job>.md`; run the checkback skill at `skills/checkback/SKILL.md`. Do not create tasks for Gordon; send nothing outbound." Add a row to `checkbacks.md` with `set_at` and `planned`. If the job is done or the chain stopped, create nothing. If creating the task fails (approval needed in a cold run), treat it as chain end: step 8 with reason "cannot schedule"; never end silently.

8. **Push.** Every hop that changed something (an item done, a stage advanced, a request written): `notify.push info "<job>: <one line>"` via a request file (until `notify.push` is on the allowlist, skip and say so in the STATUS line). Chain end for any reason (done, cap, gate, stuck, stopped): `notify.push warn --reason=chain-end "<job>: <reason>; <what Gordon needs to do>"` (reasons are registered in `_setup/notify-reasons.md`). Info per hop, warn at the end [gordon 2026-09-30].

9. **Write.** One line under `### Check-backs` in STATUS.md's "Nerd's replies" section: "- <job> hop <n> fired <time>: <found>; next <planned or 'none: reason'>". Receipt: the checkbacks.md row and the job file path. Stop.

## Rules
- Evidence is a file test. A claim in prose, including the Nerd's own, is not evidence.
- The chain is open-ended within the cap; the cap is the job's, not the skill's.
- Never rewrite `checkbacks.md`, the job file, or STATUS.md wholesale; edit the row or append the line.
- Never create a scheduled task that repeats. One standing one-time task per job, re-armed per hop, left disarmed when the chain ends.
- Never ask Gordon anything from a cold run; a question is a warn push and a line in STATUS.md, and the chain stops.
- If the tree, HEALTH.md or the job file can't be read, do nothing but the STATUS line ("checkback on <job>: could not read <path>") and `notify.push warn --reason=checkback-stuck "<job>: could not read <path>"`.

- Before any dispatch or edit that touches the tree, read `_queue/leases/`; a path inside another live lease's `writes_only` is not written from here (must-never 5, ERRORS.md #12).

## Write step
Files written: the `checkbacks.md` row, the job file (hops, waiting_on statuses, stage), the STATUS.md line, any request files, the next task or none. Receipt: one line, paths only.
