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
