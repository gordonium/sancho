---
name: Home Directions v4 review, kit round 3, the attack (not completed)
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Third independent attack on the Laravel kit's guards and hooks at commit fec74fb - NOT COMPLETED. Two of the six parts were done (the earlier 1,625 cases replayed, the kit's tests rerun twice). The four parts that matter most (a fix-by-fix check of the 46 fixes, new attack cases, the failure and lock-out experiments, the honest-limit reading) were not done, because the reviewer's work was stopped by the app's safety check. No findings, and that is not a pass
sources: ["[doc:build-handoff.md]", "[doc:build-state.md]", "[doc:laravel-kit-spec.md sections 7.0, 8, 13, 15]", "[doc:guard-check-2026-10-01.md]", "[doc:reviews/kit-K1.md]", "[doc:reviews/kit-K1-cases.txt]", "[doc:reviews/kit-K3-attack.md]", "[doc:reviews/kit-K3-attack-cases.txt]", "[doc:build-log-kit.md, K1 fixes and K2 and K3 fixes]", "[doc:~/Dev/clc-laravel/ at commits 26a0dbc, d47f4ea and fec74fb, read from frozen copies made with git archive]", "[reviewer test 2026-10-02: 869 + 756 earlier case texts judged in-process against each of the three frozen copies]", "[reviewer test 2026-10-02: bash bin/test-all.sh in two frozen copies of fec74fb, one with an empty home folder]"]
status: written 2026-10-02 15:55 CEST by a reviewer that did not write the kit; INCOMPLETE - 0 blockers, 0 should-fix, 0 minor, because the attack itself was not carried out; the 46 fixes are still unreviewed; nothing in the kit was changed, staged or committed; no case file was written; the scratch folder was removed
---
# Review: the third attack on the kit's guards and hooks, at commit fec74fb (not completed)

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write the kit and I changed nothing in it. All work was done on frozen copies (`git archive`) in a scratch folder, now removed. The guards were handed text from files. No server was contacted. No hook is registered.

**The conclusion first. This review is not finished, and its empty findings list is not a pass.** I did two of the six parts: the replay of the earlier cases and the rerun of the tests. Both came back exactly as the kit's own record says. Then the app's safety check stopped my work while I was reading the guard's code to prepare new attack cases. I did not work around it. So the part this round exists for was not done: **the 46 fixes of the last round are still unreviewed.**

What that means for Gordon and for the build:
- Nothing here says the fixes are sound. Nothing here says they are not.
- The guards should not be registered on the strength of this file.
- The third attack still has to be done, by a person or by an agent whose brief the safety check accepts.

## What was done, with numbers

**1. The earlier case files, replayed (part 1 of the brief).** Done in full.

| What | Result |
|---|---|
| The kit's two fixture copies of the reviewers' case files | Byte for byte the reviewers' files (same SHA-256 as `reviews/kit-K1-cases.txt` and `reviews/kit-K3-attack-cases.txt`) |
| The first reviewer's 869 cases at fec74fb | 289 allowed, 580 refused, no crash. Wrongly allowed 37 (18 other roads, 16 inside the stated limit, 3 disguise; none tagged "must"). Wrongly refused 11. All 869 answers equal the kit's expected file |
| The second reviewer's 756 cases at fec74fb | 100 allowed, 656 refused, no crash. Wrongly allowed 18 (13 inside the stated limit, 2 disguise, 3 waiting for Gordon; none tagged "must"). Wrongly refused 10. All 756 answers equal the kit's expected file |
| The same two files at the earlier commits | At 26a0dbc: 226 wrongly allowed and 53 wrongly refused over the 869. At d47f4ea: 38 and 11 over the 869; 218 and 16 over the 756. These are the numbers both earlier reviews reported |

So the build log's claims for these 1,625 cases are true: 37 and 11, 18 and 10.

**Loosening, over these 1,625 old cases only.** I compared each case's answer at the three commits.
- Refused at d47f4ea and allowed at fec74fb: 6 cases (QD32, QD42, QD44, QE17, QH92, QH94). All six are cases the second reviewer wanted allowed. They are the same six the build log lists. None over the first reviewer's 869.
- Refused at 26a0dbc and allowed at fec74fb: 42 of the 869, all wanted allowed by the first reviewer; 10 of the 756, of which one (QG16) the second reviewer wants refused. QG16 was already allowed at d47f4ea, is the second review's finding 15, and is listed as open in the build log (a command written to a file and then run: inside the stated limit).

This shows only that the fixes did not loosen any answer **among the cases already on record**. It says nothing about new shapes. Finding new shapes was the job of the part that was not done.

**2. The kit's tests, rerun (part 6 of the brief).** Done in full.

| Run | Result |
|---|---|
| `bash bin/test-all.sh` in a frozen copy of fec74fb, this session's environment | Ran 4092 tests in 423.7s, OK, exit code 0. The copy's 129 files had the same checksum before and after |
| The same in a second frozen copy, with `HOME` pointed at an empty folder and the environment emptied | Ran 4092 tests in 435.5s, OK, exit code 0. The copy unchanged; the empty folder still held nothing |

The builder's number (4,092 tests, 0 failures, also with an empty home) is true.

## What was NOT done

| Part of the brief | State |
|---|---|
| 2. The 46 fixes, one by one: closed in every spelling? anything loosened? a new false refusal? is each case "left open with a reason" safe to leave? | **Not done.** Only the old-case comparison above |
| 3. Several hundred new attack cases | **Not done. None was written or run.** There is no case file beside this one |
| 4. Failure: does anything fail open, can a broken guard lock the Mac, is the written way out correct step by step | **Not done** |
| 5. The honest limit: is everything the guard cannot see stated where Gordon reads it, and does any sentence claim a wall that is only a hook | **Not done** |

I had read the two rules files, the hooks block, the tests' helpers and about the first 2,300 lines of `bin/guard_core.py` (its header, the address spellings, the word splitter, the comment and here-document readers) when I was stopped. I draw no finding from that reading: I ran nothing against it, and a suspicion I did not demonstrate is not a finding.

## Findings

None. **Zero findings here means "not looked for", not "none exist".**

## Refused by the app's safety check

One thing: my turn was stopped while I was reading the guard's code in preparation for part 3 (new attack cases). The notice said not to produce that content again in any wording. I did not. I finished only the test reruns that were already running, and wrote this file.

## Untouched, checked at the end

The kit repository is at fec74fb with a clean working tree and no remote. I wrote nothing in it, staged nothing and committed nothing. I did not open `hdonline-v4/`, `~/Dev/clc-plugins/`, the import data folder or Downloads. No hook was registered and nothing under `~/.claude/` was edited. In the Sancho tree only this file was written. My scratch folder (three frozen copies, two test copies, the replay outputs) was removed.
