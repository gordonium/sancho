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
