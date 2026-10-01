---
name: commands
type: registry
lobe: both
description: The allowlist of scripts the watcher may run, with timeouts and schedules; also the map's command table
---
# Commands: the allowlist and the registry
The watcher runs only what is listed here. Adding a command = one row here + one script with a header. The map draws its command table from this file. `schedule` blank = on demand only. "Terminal only" = listed for the map, refused by the watcher (it needs a passphrase at a prompt). Request args: a list is passed as positional arguments. Every request carries `session:` (cowork hop N / interactive / nerd.run <id> / schedule <name>); results, logs and pushes echo it. Requests from launchd wait until the Mac has been awake 10 min (ERRORS.md #8). Nerd sessions hold a lease in `_queue/leases/` (`nerd-<id>.md`; interactive ones via `_setup/nerd-lease.py run -- claude`). Schedules are launchd plists that enqueue a request (`sancho-enqueue.py`), so every scheduled run leaves a result; the hourly autocommit is the one exception, run by launchd directly so commits never depend on the watcher.

| command | script | timeout (s) | schedule | description |
|---|---|---|---|---|
| ping | _setup/ping.sh | 10 | | round-trip test: writes a result containing the request id |
| index.build | _setup/build-index.py | 120 | after commits; nightly 02:00 | regenerate every INDEX.md, PROJECTS.md, ICE.md, people and skill indexes |
| lint | _setup/lint-layers.py | 120 | before every map build; nightly | layering, caps, headers, generated-file integrity, stale next actions |
| map.build | _setup/build-map.py | 120 | after index.build; nightly | regenerate MAP.md (three zoom levels) |
| docs.reading-copy | _design/build-reading-copy.py | 60 | on demand | rebuild the architecture reading copy and standalone HTML |
| test.all | _setup/test-all.py | 600 | nightly 02:30; after commits touching _setup/ or skills/ | run every test suite; write TESTS.md; exit 1 on any failure |
| git.commit | _setup/git-autocommit.sh | 120 | hourly (launchd direct, not via the queue); at conversation close | commit and push the tree (skips oversize files, lists them in GIT-EXCLUDED.md) |
| nightly | _setup/nightly.sh | 300 | nightly 02:00 (com.sancho.nightly enqueues it) | index.build, then lint, then map.build; stops at the first failure |
| notify.test | _setup/notify-test.sh | 30 | | args [info] / [warn] / [alert]: send one test push to Gordon's phone at that level |
| notify.push | _setup/notify.py | 30 | | args [info or warn or alert, --reason=<slug>, <message>]: one Pushover push to Gordon; info (silent) for completions and progress; warn (sound) when he must move, with a reason registered in _setup/notify-reasons.md; alert only for pipeline red / watcher dead, at priority 0 for now so quiet hours hold [gordon 2026-10-01]; the request's session is echoed; deduped per key; a comma in the message arrives whole |
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
| nerd.run | _setup/nerd-run.py | 1900 | | headless Claude Code (the Nerd) for the task in the request (`task_file:`, or a body ending with the line `-- end of task --`; ERRORS.md #7); allowlisted tools, OS sandbox, no MCP, no push/commit/web; one at a time; lease while running; transcript in _queue/results/; a result for a job with `advance: auto` queues job.run --auto |
| job.run | _setup/job-run.py | 60 | | args [<job name or file>] (or [<job>, --auto], queued by the watcher): walk a job file stage by stage via nerd.run (detached; progress in the job file); up to 3 attempts per stage with evidence and diagnose-first, stopping early on an identical failure; `Stage: blocked` pauses at a gate; warn on every stop, info on completion |
