---
name: attribution-correction
type: skill
lobe: both
shared:
description: When Gordon corrects who said something ("that's not Roy, that's Mike", "swap them", "that was Leah"), fix the speaker row, the voiceprint library, every recording the bad reference could have touched, and every fact filed under the wrong name; present everything before fixing; never finish with an unreviewed re-match list.
why: v2's attribution drift was the post-mortem's first wound; its correction skill fixed the files and never the voiceprint, so the same mistake recurred. Here the library learns, the window of damage is computed, and the cascade follows the sources: lists.
triggers: ["that's not <name>", "that was <name> not <name>", "swap them", "flip that", "wrong speaker", "that's me", a speaker correction given during earballs-ingest]
must_not_trigger: [a correction of a misheard word (that is corrections.md, in earballs-ingest), a correction of a fact that is not about who said it, a machine candidate Gordon merely declines to confirm]
reads: ["the recording's speakers.md, transcript.md, summary", "every file whose sources: lists that rec_id (ripgrep)", recordings/STATUS.md, "people/<old>.md and people/<new>.md"]
writes: ["speakers.md (old row struck, new row by: gordon)", "people/<old>.md voiceprint: auto paused 90 days", "every affected file: superseded lines + corrected lines", "the summary's Speakers footer", "_queue/requests/ (pipeline.library, pipeline.rematch)", "the entity's or lobe's decisions.md", "the session note"]
chain: {front: "earballs-ingest, or any conversation where a correction lands", next: "earballs-ingest resumes if it was mid-pass", gate: "human: the re-match list (step 4) is reviewed by Gordon before the correction is called done"}
test: _setup/tests/skills/attribution-correction/
---
# attribution-correction

Present all, then fix all, then prove the library learned. A correction is one event with five steps; it is not done until the last list is empty or reviewed.

## Procedure

1. **Pin the correction.** Restate it in one line with the recording's handle (date, length) and the clusters: "Fri 9/19 2:10pm, 44 min: SPEAKER_01 was Leah, not Roy." Ask only if the clusters are ambiguous (a "swap" with three speakers). Write it to the session note before anything else.

2. **Speaker row.** In `speakers.md`: strike the old row's `confirmed` value (`~~roy-williams~~`), add the new value with `by: gordon`, the date, and a note quoting the correction `[confirmed gordon <date>]`. If the old row was machine-confirmed, note which reference(s) produced the match (the `candidate` column and `recordings/STATUS.md`).

3. **Library and the paused flag.** Set `voiceprint: {auto: paused, until: <date + 90 days>}` on `people/<old>.md`, with a line naming the correction. Request `pipeline.library` (rebuild from human-confirmed rows; the wrong reference is gone because the row changed). Then request `pipeline.rematch --person <old-slug> --since <enrollment date of the wrong reference>`: every recording processed since the bad reference existed where that person was a candidate, all of them, newest first; the pipeline batches a long list under its own throttle rather than truncating it [gordon 2026-10-01: "everything potentially bad must be re-examined"]. Until that command exists, list those recordings by hand from `recordings/STATUS.md` and say so.

4. **Re-match review (gate).** When the result lands, show Gordon only the recordings whose top candidate changed, each with the handle, the old and new candidate, and two long passages. His answers go through step 2 for each. The correction is not done while this list is unreviewed; if the Nerd has not answered within the conversation, the session note carries the open list and the next open says so.

5. **Cascade through the files.** `rg -l "rec_<id>"` across the tree, plus the recording's own summary. In every hit, re-read the whole transcript with the new attribution (a swap changes who promised what, who decided, who holds the opinion), then for each line that depended on the old attribution: strike it in place `~~…~~ [superseded <date> by attribution-correction, rec_<id>]` and write the corrected line with its cite. People files: a fact filed under the wrong person moves to the right person the same way. Nothing is deleted. One line in the entity's `decisions.md` (or the lobe's): date, the correction, files touched, source.

6. **Write and receipt.** Session note `written:` list; receipt under six lines: the row changed, the paused flag, the two requests, the files superseded (count and paths), and the re-match list's state (empty, reviewed, or waiting).

## Rules
- Present before fixing: the cascade list is shown as a list of files before any of them is written when more than three are affected.
- A correction strikes and adds; it never edits a line in place.
- The library is rebuilt on every correction; a correction that skips step 3 is the v2 bug.
- The 90-day pause is on the person who was wrongly matched, not on the person who was actually speaking.
- Machine-confirmed rows never become human-confirmed by this skill unless Gordon states the name.

## Write step
Files written: `speakers.md`, `people/<old>.md`, each superseded file, the summary, `decisions.md`, the two requests, the session note. Receipt: one line, paths only, then the re-match list state.
