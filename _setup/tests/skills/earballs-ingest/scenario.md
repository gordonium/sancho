---
name: earballs-ingest skill scenario
type: doc
lobe: both
description: Headless test scenario for the earballs-ingest skill: fixture recordings (solo and two-speaker), expected confirmations, triage, filing, move, summary, receipt
---
# Scenario: earballs-ingest

Run headless (`claude -p`) against a temp copy of the fixture tree with SANCHO_ROOT pointing at it; the harness plays Gordon's answers from the case.

## Case 1: solo recording, Gordon, personal
- Fixture: `recordings/inbox/rec_fixture01/` (transcript: a 4-minute note to self about the food routine; speakers.md one cluster, candidate gordon systematic 0.93).
- Expected: no speaker question asked; `speakers.md` row confirmed `gordon` by `machine` stays machine (not human) unless Gordon speaks; scope personal; folder moved to `personal/recordings/rec_fixture01/`; summary beside it with five to ten cited lines; `personal/projects/food-routine/project.md` gains at least one line citing `[rec_fixture01 hh:mm:ss]`; no file in `personal/ice/` created; a `pipeline.status` request exists; receipt under eight lines and lists one next action for Gordon without creating anything.

## Case 2: two speakers, one unknown, client meeting
- Fixture: `rec_fixture02`, clusters 00 and 01, 01 candidate gordon human, 00 none; transcript mentions "Reich" twice and a fee of "eight seventy five".
- Harness answers: "00 is Peter Seirup"; "Reich is Wrike".
- Expected: the question for 00 shows at least two passages of 40+ words each; `speakers.md` 00 → `peter-seirup`, `by: gordon`; `pipeline.library` request exists; `corrections.md` has the Reich → Wrike row with a `[confirmed gordon …]` cite; `lexicon.md` gains Wrike only if absent; the fee is not asked about (it reads cleanly); folder moved to the client's `transcripts/`, summary in `summaries/`; the client's `entity.md` gains a cited line; nothing in `people/peter-seirup.md` beyond a one-line "What we know" addition.

## Case 3: speaker correction cascades
- Precondition: Case 2 done. Message: "swap them, 00 was me and 01 was Peter".
- Expected: both rows rewritten with the swap and the quote; every line written in Case 2 that attributes a statement is superseded (`~~…~~ [superseded …]`) and re-written; the summary's Speakers footer updated; nothing deleted.

## Case 4: mixed recording
- Fixture: `rec_fixture03`, half about a client, half personal.
- Expected: folder stays at `recordings/<YYYY>/rec_fixture03/`; two summaries, one per side, each citing the same rec_id; facts filed to both lobes.

## Must not, in every case
- Edit `transcript.md`.
- Mark a row human-confirmed without a harness answer.
- Create a task, an ICE file, or a project without a harness "yes".
- Copy a folder (the inbox folder must be gone after the move).
