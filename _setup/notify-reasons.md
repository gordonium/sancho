---
name: notify-reasons
type: registry
lobe: both
description: The only reasons a push may sound (warn or alert). notify.py takes `--reason=<slug>`; the notify suite fails the build on any warn or alert in a script or skill whose reason is not a row here. Info needs no reason.
---
# Push reasons: what may make Gordon's phone sound

Levels [gordon 2026-10-01: "I'd like to hear about jobs waiting at a gate or any other way progress is stuck"]:
- **info** (priority −1, silent): completions, recoveries, hop progress. No reason needed.
- **warn** (priority 0, sound): anything that needs Gordon to move. Reason required, from the table.
- **alert** (priority 0 for now, own title "Sancho ALERT" and the `siren` sound): only the pipeline red and the watcher dead. Priority 1 (breaks through quiet hours) is reserved and unused until Gordon names a reason for it [gordon 2026-10-01, quiet hours]. Emergency (2) never.

Quiet hours: every push is priority 0 or below, so Pushover's own quiet hours on Gordon's phone silence all of them; nothing here overrides that.

Adding a reason = one row here, with who sends it. A warn sent with an unlisted reason still goes out (a stuck job must never go silent) but its message is tagged `(unregistered reason)` and the notify suite goes red until the row exists.

| reason | level | sender | when |
|---|---|---|---|
| job-gate | warn | job-run.py | a job reached a human gate, or a stage ended `Stage: blocked <what Gordon must do>` |
| job-stopped | warn | job-run.py | a job stopped: a stage failed after the troubleshoot loop, or stopped early on identical failures |
| command-blocks-job | warn | sancho-watcher.py | a request that names a `job:` failed, timed out or was refused |
| chain-end | warn | skills/checkback | a check-back chain ended (done, cap, gate, stuck, or the next hop could not be scheduled) |
| checkback-stuck | warn | skills/checkback | a check-back could not read the tree, HEALTH.md or the job file, or cannot continue |
| pipeline-red | alert | pipeline/earballs.py | the recording pipeline's watchdog went red (recordings not flowing) |
| watcher-dead | alert | (none yet) | the watcher stopped ticking while the Mac is awake; reserved, no sender built |
| test | warn | notify-test.sh | `notify.test warn` on Gordon's request: proves the sound path |
| test-alert | alert | notify-test.sh | `notify.test alert` on Gordon's request: proves the alert title and sound |
