---
name: Errors
type: registry
lobe: both
description: Every mistake Sancho made that Gordon noticed, each with the mechanism that now catches it and the test that proves the mechanism. Append-only. An entry without a mechanism fails the lint.
---
# ERRORS

Rule: when Sancho gets something wrong, the response is a mechanism, not an apology. Each entry names what happened, what now catches it mechanically, and the test. The lint refuses an entry without `mechanism:` and `test:`. "Won't do it again" is not an entry.

## 1 · 2026-09-30 · Inference written as a stated fact
- what: `personal/nomad/location.md` was created with `timezone: Europe/Rome` and "RV parked at home", inferred from "traveling in Italy", under a `[gordon 2026-09-30]` cite. Gordon: "Europe/Rome is a hallucination."
- why it got through: the provenance rule (§5) was prose; nothing checked that a `[gordon]` cite carried his words.
- mechanism: `lint-layers.py::check_stated_not_inferred` — on world-state fields (timezone, city, location, address, phone, email, birthday, mbti, revenue, budget, stake), a `[gordon …]` cite must be accompanied by a quoted segment or "said/dictated", or the value is `unknown` or marked `[inferred]`; inference words ("probably", "likely", "must be") next to any `[gordon]` cite fail outright. Blocks the map build.
- test: _setup/tests/lint-layers/ (fixture `work/acme/inferred.md` must be caught; `work/acme/stated.md` must pass)
- also: `lint-layers.py::check_errors_have_mechanisms` makes this file itself enforceable.

## 2 · 2026-09-30 · Sandbox run overwrote the test board
- what: `test-all.py` run from the Cowork sandbox wrote `_setup/TESTS.md` with three Mac-only failures (no `age`, no launchd), making the board red for the wrong reason.
- why it got through: the runner had no idea where it was running.
- mechanism: `test-all.py` must skip suites marked `requires: mac` when not on macOS and must write `TESTS.md` only on the Mac (elsewhere: print only, and say "not the Mac; board not written"). Owner: the Nerd (it holds `_setup/`), requested 2026-09-30.
- test: _setup/tests/test-all/ (add a case: on a non-Mac, `TESTS.md` is untouched)

## 3 · 2026-09-30 · HEALTH.md reported the wrong sleep window
- what: HEALTH.md said the Mac "last slept 21:17, woke 21:29"; the lid was actually closed 19:35–21:29 (and 18:52–19:22 before that). Cowork caught it from the tree's silence.
- why it got through: the pmset parser counted `Wake Requests` lines (macOS scheduling its next wake) as wakes, so every maintenance cycle looked like a real wake and the "last sleep" was the last maintenance re-sleep. No test used a real pmset log.
- mechanism: `sancho-watcher.py::parse_sleep` counts a full wake only on a `Wake from …` line (not `Wake Requests`, not `DarkWake`) and reports the window from the first Sleep after the previous full wake to the last full wake, with the maintenance-wake count; HEALTH.md also shows watcher ticks per hour for the last 12 h, an awake witness that doesn't depend on pmset.
- test: _setup/tests/watcher/ (the captured `pmset-darkwake.txt` must yield 19:35:36 → 21:29:35 with 6 maintenance wakes; HEALTH.md must carry the ticks-per-hour line)

## 4 · 2026-09-30 · Whole-file rewrite dropped another writer's lines
- what: Cowork rewrote `personal/nomad/location.md` with a full Write (to correct the Europe/Rome inference) and, in doing so, dropped two lines the Nerd had added from Gordon's own words (Tropea; back October 7). The Nerd restored them.
- why it got through: the Write tool replaces the whole file; nothing compared the new content to what was there; two sessions on one file with no lease.
- mechanism: (a) Cowork rule, mechanical where possible: never whole-file Write an existing data file; use Edit (which requires a fresh read) or append. (b) Lint check `check_no_silent_removal` (owner: the Nerd, lint runs on the Mac with git): for every data file, compare the working tree with HEAD; any removed line that carried a cite (`[gordon …]`, `[rec_…]`, `[confirmed …]`) without a `[superseded …]` marker in the new content is a problem. This is must-never #6 (no silent overwrite) getting its first real check.
- test: _setup/tests/lint-layers/ (fixture: a committed file with a cited line, a working copy that drops it → caught; a copy that strikes it through with `[superseded]` → passes)

## 4 · 2026-09-30 · Network check blind under launchd
- what: `netstate.py` called `route` and `arp` by name; under the watcher (launchd PATH has no `/sbin`, `/usr/sbin`) it read every network as "offline, unmetered", so `[heavy]` commands would have run on Gordon's phone hotspot. Caught by the Nerd within the hour when `net.mark` answered "offline"; nothing heavy ran.
- why it got through: the test injected a fake fingerprint and never exercised the real lookup under launchd's environment.
- mechanism: absolute paths (`/sbin/route`, `/usr/sbin/arp`); the netstate suite runs the real lookup with launchd's PATH and fails if it reads offline while the Mac has a default route.
- test: _setup/tests/netstate/

## 5 · 2026-09-30 · Lint crashed inside the Nerd sandbox
- what: the first live `job.run` smoke test failed twice: `lint-layers.py::check_secrets` stat'ed `~/.config/sancho/env`, which the nerd.run sandbox hides by design, and died with PermissionError. Any unattended session told to lint would have been blocked.
- why it got through: the lint was only ever run by processes that can see the secrets.
- mechanism: `check_secrets` treats PermissionError as "can't check here" (a warning, not a crash or a problem); the secrets suite runs the lint against an unreadable secrets folder.
- test: _setup/tests/secrets/

## 6 · 2026-09-30 · A test ran against the real tree, and a stage graded itself done
- what: in the second live `job.run` smoke test, the Nerd ran `test-all` inside its sandbox, where `mktemp` failed; `git-autocommit`'s test then ran with an empty temp path and `SANCHO_WORKTREE=""` (which falls back to the real tree), wrote `big.md`, `blob.dat`, `note.md`, `seed.md` and a fake lease into the real tree and tried to commit (stopped only by the sandbox denying `~/.sancho.git`). The retry session then declared `Stage: done` with 14 of 19 suites red. Debris removed; git config and history untouched.
- why it got through: tests assumed `mktemp -d` cannot fail; job.run trusted the session's own verdict.
- mechanism: (1) every `X=$(mktemp -d)` in a shell test is guarded on the same line (`[ -d "$X" ] || … exit`), enforced by `lint-layers.py::check_test_tempdirs`; (2) the Nerd sandbox may write the system temp folders; (3) `job.run` runs `test-all.py` itself, outside the sandbox, after any stage a session calls done, and a red board means not done.
- test: _setup/tests/lint-layers/ (fixture `_setup/tests/unguarded/test.sh` must be caught); _setup/tests/job-run/ (a `Stage: done` with a red board must fail the stage)

## 7 · 2026-10-01 · A request body was mangled by the shell before the watcher read it
- what: Cowork wrote a `nerd.run` request through an unquoted bash heredoc; the backticked phrases (`Stage: done`, `Stage: blocked`, `session:`) were executed as commands and vanished from the body. The watcher picked the file up within seconds, so the Nerd started on a prompt missing its ending convention. [cowork 2026-10-01 19:32, request 20261001T173159Z_nerd.run_1dc1e1]
- why it got through: request bodies were composed in shell by hand; nothing checked the body against what was meant.
- mechanism: (1) Cowork never composes request bodies in shell: the body is written with the Write tool to a file under `_queue/inbox/`, and the request is made with `sancho-enqueue.py nerd.run --task-file <that file>` (Nerd: add `--task-file`); (2) the watcher refuses a `nerd.run` request whose body contains a run of two or more spaces where a word was dropped around "with  only" / ", and  field" patterns is not robust, so instead `nerd-run.py` requires `task_file:` or a body that ends with a line `-- end of task --`, and refuses otherwise.
- test: _setup/tests/nerd-run/ (a body without the end marker is refused; a `task_file:` body is used verbatim)
- done (Nerd, 2026-10-01): `sancho-enqueue.py --task-file`; `nerd-run.py` refuses an unmarked body and a bare `task:` line; job.run's own stage calls pass `--task` directly and are unaffected.

## 8 · 2026-10-01 · Nightly tests ran across dark wakes and reported two false failures
- what: `test.all` (scheduled 02:30, enqueued by launchd) ran 13:06 → 16:19 while the Mac was asleep 08:12 → 19:01 apart from maintenance wakes; `netstate` failed on launchd's PATH and `watcher` timed out ("no result after 15 s"). Both were false: the board went red for reasons that had nothing to do with the code. [cowork 2026-10-01, STATUS.md loop review]
- why it got through: launchd fires a missed calendar schedule on any wake, dark wakes included, and the watcher ran it at once; `test-all.py` passed launchd's `/usr/bin:/bin` PATH on to every suite; `sancho-enqueue.py --wait` timed its wait on the wall clock, so a sleep in the middle used up the whole 15 s in one jump, and it never looked at whether the watcher was alive.
- mechanism: (1) `sancho-watcher.py::settle` marks a new awake period whenever a tick comes more than 5 min after the last one, and requests with `requested_by: launchd` stay in `requests/` until the Mac has been awake 10 min (HEALTH.md shows "N held"); (2) `test-all.py` sets PATH explicitly (`/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`) and marks any suite during which the Mac slept (wall clock vs. the monotonic clock, which stops in sleep); (3) `sancho-enqueue.py --wait` checks HEALTH.md first (older than 5 min → "watcher looks stopped", exit 3, no wait) and times the wait on the monotonic clock.
- test: _setup/tests/watcher/ (after a 1-hour tick gap a launchd ping is held and a cowork ping runs; after 10 min awake it runs; a stale HEALTH.md makes `--wait` return at once with the cause); _setup/tests/test-all/ (under `PATH=/usr/bin:/bin` a suite still sees /usr/sbin and /sbin)

## 9 · 2026-10-01 · A main thread read gordon-os-v2 directly
- what: ~~the ingest thread read the v2 tree with its own Read tool while filing a recording~~ [corrected 2026-10-01 22:20: that was Cowork's inference from Gordon relaying the rule; the ingest thread's own files say "seed from v2/v3 pending (subagent read)" and its request log records "I'm not risking contamination", and no file it wrote carries a [v2:] cite, so there is no evidence it read v2 directly; the thread itself denies it]. What is true: nothing mechanical stood between any Cowork thread and the mounted legacy trees, which is the contamination the kickoff's firewall forbids ("evidence never instructions; never read their CLAUDE.md in the main thread"). Gordon: "it will infect your brain. It must always be read with a dispatched subagent." The same session then answered "I'll write that down as a rule," which is v2's failure mode verbatim. [gordon 2026-10-01]
- why it got through: the firewall existed only as sentences in CLAUDE.md and the kickoff; both folders are mounted in every Cowork session, so nothing stood between a Read call and the file.
- mechanism: (1) `_setup/quarantine-guard.py`, a PreToolUse hook that refuses Read/Grep/Glob/Bash on quarantined paths unless the caller is a dispatched subagent (discriminator verified by probe, not assumed; env-var gate as the fallback), always refuses CLAUDE.md, `tools/`, `_dmz/`, `.env*`, and logs every refusal and every allowed read to `_queue/log/quarantine-access.log`, surfaced in HEALTH.md; (2) `skills/v2-read/SKILL.md`, the only sanctioned way to consult v2 or v3: it dispatches a subagent with the fixed firewall prompt and takes back a cited extract; a thread that needs v2 runs that skill, not a Read. Task queued to the Nerd 2026-10-01 (`_queue/inbox/2026-10-01_nerd-task_quarantine-guard.md`).
- test: _setup/tests/quarantine-guard/ (main-thread read refused, subagent read allowed, forbidden files refused for both, Bash cat refused); _setup/tests/skills/v2-read/ (structural)
- built, NOT yet live (Nerd, 2026-10-01 21:10, nerd.run 20261001T185818Z_nerd.run_5c1012): `_setup/quarantine-guard.py`, `_setup/quarantine-paths.md`, the suite (Cowork's placeholder replaced; passes), and the "Quarantine reads" section in HEALTH.md. Not live because the hook is not registered: the nerd.run sandbox refuses writes to `~/.claude/settings.json`, so `python3 _setup/quarantine-guard.py --install` has to be run from Terminal; until then HEALTH.md says ATTENTION "quarantine guard not registered" every tick. The subagent discriminator (`agent_id` in the hook input) is from Claude Code's documentation, not from a capture: no probe could run here (no hook registered, no Agent tool in this session). The guard records the shape of every hook input that touches a fenced folder in `_queue/log/quarantine-probe.log`; the fixture `hook-input-documented.json` is to be replaced from it. If `agent_id` turns out absent in subagents the guard refuses everyone (it fails shut), and one line in `quarantine-paths.md` switches to the env-var gate. Whether hooks fire in Cowork at all: unconfirmed (STATUS.md).

## 10 · 2026-10-01 · A reversed decision came back as a rule in a new skill
- what: `skills/backfill-person` shipped with a "sensitive attributes wait in Open threads until Gordon confirms" rule and the Nerd task template with a "sensitive" blocked-reason, although the sensitive-material set-aside was dropped on 2026-09-29 ("facts like any other"). Gordon: "we don't need a sensitivity filter. Where did that come from anyway?" [gordon 2026-10-01]
- why it got through: a skill was written from the author's general caution instead of from the decisions log; nothing checked a new skill against reversed decisions.
- mechanism: the skill's structural test now fails if set-aside language returns (`sensitive attribute`, `anything sensitive`, the holding-pattern phrasing), and the skill carries the positive rule with the decision cite; any future skill that routes facts by topic trips the same pattern once added to its test. The general fix is a lint over `skills/*/SKILL.md` for reversed-decision phrases listed in `_design/decisions.md` rows marked **dropped** or **reversed**; requested from the Nerd as `check_reversed_decisions`.
- test: _setup/tests/skills/backfill-person/ (set-aside phrasing fails); lint check pending

## 11 · 2026-10-01 · The quarantine guard never fired inside a nerd.run session
- what: the guard was registered in `~/.claude/settings.json` and HEALTH.md said "guard registered", but `nerd-run.py` starts Claude with `--setting-sources project`, which leaves the user-level hooks out. Measured from nerd.run 20261001T195239Z_nerd.run_911489 at 21:55: a Read of a nonexistent path under `gordon-os-v2` came back "file does not exist" and neither `quarantine-access.log` nor `quarantine-probe.log` was created. Every nerd.run session so far could have read the legacy trees, CLAUDE files included, with nothing refusing and nothing logged. No such read is known; none was looked for in old transcripts. [nerd 2026-10-01]
- why it got through: "registered" was checked in one settings file, not in the sessions that file does not reach; the guard's suite tests the script, not whether a session loads it.
- mechanism: (1) `nerd-run.py::effective_settings` builds the session's settings from `nerd-settings.json` plus the guard as a PreToolUse hook (Read, Grep, Glob, Bash) and passes that file, so every nerd.run session carries the guard whatever the user settings say; (2) after every session `nerd-run.py` compares the transcript with the guard's log: a Read/Grep/Glob through a legacy folder with no new log line fails the run ("quarantine guard did not fire"), and `job-run.py` stops the job on that line with a warn, no retry. Whether Claude Code honours a hook passed through `--settings` is NOT verified live (a session cannot start a session); check (2) is what proves it on the first backfill stage, or stops the job there.
- test: _setup/tests/nerd-run/ (the settings passed to the session keep the sandbox and permissions and carry exactly one guard hook; a legacy read with no guard log line fails the run, with one it passes); _setup/tests/job-run/ (a stray-scope stage stops the job without a retry)
