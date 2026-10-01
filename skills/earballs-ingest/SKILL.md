---
name: earballs-ingest
type: skill
lobe: both
shared:
description: Files one processed recording: speakers confirmed with transcript chunks shown, mishearings triaged to the ones that sit on a fact, content clarified into the seven GTD buckets, facts filed with cites and superseded never overwritten, transcript moved to its home, summary written, receipt given. The clarify step of GTD for recordings.
why: Recordings are Gordon's main capture channel; v2 and v3 lost them to attribution drift and unfiled transcripts. One recording, one pass, every fact citable to a timestamp.
triggers: ["ingest", "process recordings", "file that recording", the greeting shows recordings waiting and Gordon says go, a check-back or job stage named ingest]
must_not_trigger: [a recording mentioned in passing, a request to search transcripts ("what did Roy say"), a transcript whose speakers Gordon has not confirmed when the recording is not solo, any recording in recordings/backlog/ unless a backlog ingest job names it]
reads: ["recordings/inbox/<rec_id>/{transcript,speakers,meta}.md", recordings/lexicon.md, people/INDEX.md, "the target lobe's INDEX.md and PROJECTS.md", "the target entity's INDEX.md and project.md or entity.md", "the recording's corrections.md if present", personal/me/watch.md]
writes: ["recordings/<home>/<rec_id>/speakers.md (confirmations)", "recordings/<home>/<rec_id>/corrections.md", recordings/lexicon.md, "the entity's summaries/<date>_<rec_id>.md (T5)", "project.md / entity.md / knowledge.md / people/<slug>.md lines with cites", "_queue/requests/ (pipeline.library when a speaker is newly human-confirmed; pipeline.status after the move)", "the transcript folder moved to its home", "the session note's written: list"]
chain: {front: "open (a conversation is open)", next: "attribution-correction on a speaker correction; a project's own skill if a new project is approved", gate: "human: speaker confirmation for any non-solo recording; human: the first ingest is spot-checked (five facts)"}
test: _setup/tests/skills/earballs-ingest/
---
# earballs-ingest

One recording per pass. Never from memory: every fact cites `[rec_<id> hh:mm:ss]`. The raw transcript is never edited; corrections live beside it. Gordon's words win over the machine's at every step, and nothing the machine said becomes "human-confirmed" without his saying so (must-never 7).

## Procedure

1. **Pick.** The recording named, else the newest in `recordings/inbox/` that is solo or has human-confirmed speakers, else the newest overall. More than one requested → a job file `_queue/jobs/<date>_ingest.md` with one stage per recording; this skill does one stage. Read its `transcript.md`, `speakers.md`, `meta.md`, and `recordings/lexicon.md`. Lead with the human-readable handle in chat ("Tue 9/22 02:27, 5 min, solo"), never the ID.

2. **Speakers (gate).** For every cluster in `speakers.md` not yet human-confirmed: show two or three **long** passages of that cluster (whole turns, a paragraph each, not snippets: Gordon identifies people by how they talk), the machine candidate if any with its state, and ask who it is. A solo recording whose single cluster matches Gordon's voiceprint at 0.90 or better is confirmed as Gordon without asking; otherwise ask. Write each answer into `speakers.md` at once (`confirmed`, `by: gordon`, date, note with the quoted confirmation). A new person gets `people/<slug>.md` from the template with only what was said, nothing inferred. If any row became human-confirmed, request `pipeline.library`. **A correction cascades:** when Gordon swaps or renames a speaker, re-read the whole transcript with the new attribution before step 4; every claim that depended on who said it is re-derived, not patched.

3. **Mishearings (triage, don't bog down).** Candidates: `## suspects` in `meta.md` if the pipeline wrote one, plus anything that reads wrong against `lexicon.md` or `people/INDEX.md`. Show Gordon only the suspects that sit on a fact: a name, a client, a place, a number, a date, a decision, anything that would be cited. Mundane mishearings are fixed silently in the summary or ignored. Answers go to `corrections.md` beside the transcript (`[hh:mm:ss] "heard" → "meant" [confirmed gordon <date>]`); a correction that will recur (a name, a product) is added to `lexicon.md`; a one-off is not. [gordon 2026-09-30]

4. **Scope (§3.5).** Decide from content: **single-client** (one client or business), **personal**, or **mixed**. Unclear → ask, with the two candidate homes named. The home decides where the folder moves and where the summary lives: client `transcripts/` + `summaries/`; `personal/recordings/<rec_id>/`; mixed stays at `recordings/<YYYY>/<rec_id>/` with one summary per side.

5. **Clarify into the seven buckets.** Walk the transcript once, by timestamp, and sort every substantive item:
   - **Next action** → listed for Gordon in the receipt ("you'll want a task for…"); never created for him (must-never 2).
   - **Project** → an existing `project.md` gets the fact, decision or next action with its cite; a new project is *proposed* and created only on Gordon's yes.
   - **Waiting for** → the project's `waiting:` field (who, what, since).
   - **Reference** → `knowledge.md`, `entity.md`, `guidelines.md`, or a person's file: one line each, cited, superseding an older line with `~~…~~ [superseded <date> by rec_…]` rather than editing it (must-never 6). People files grow by a line, not a dump.
   - **Someday/maybe** → proposed for ICE in the receipt; written only on yes.
   - **Calendar** → surfaced in the receipt; Gordon books it.
   - **Trash** → nothing written; the summary's "What happened" may mention it in a clause.
   A fact about a person's state (health, mood, location, money) or about Gordon himself is read back and confirmed before it is filed anywhere outside the summary. A blind spot from `watch.md` that shows in the recording is said once, in the receipt.

6. **Summary (T5).** `summaries/<YYYY-MM-DD>_<rec_id>.md` (or beside the transcript for personal and mixed) from `_setup/templates/summary.md`: frontmatter filled; "What happened" in five to ten lines, each cited by timestamp; Decisions; Commitments noticed; **Facts to file**, each with its target path and marked `filed → <path>` as step 5 wrote it; Questions and corrections needed; Speakers footer with states. The summary is the index card; the transcript is the record.

7. **Move and register.** Move the whole `recordings/inbox/<rec_id>/` folder to its home (never copy, never delete; `corrections.md` travels with it). Update the transcript's `description` to say ingested and where the summary is. Request `pipeline.status` so `recordings/STATUS.md` and the ledger learn the new location.

8. **Write and receipt.** Append every path written to the session note's `written:` list. Receipt, under eight lines: the home path; the summary path; facts filed (count, and the files); next actions for Gordon's task manager; proposals awaiting his yes (projects, ICE); questions. For the first ingest of all (`first-ingest` stage of the build job) add five filed facts with their cites for Gordon to spot-check; the stage is done on his word.

## Rules
- Chunks shown for speaker identification are long passages. A one-line snippet is not identification.
- Nothing is marked human-confirmed except on Gordon's explicit word in this conversation.
- Suspect words are asked about only when a fact hangs on them.
- Supersede, never overwrite; move, never copy or delete.
- One recording per pass; a batch is a job with one stage each.
- No tasks created for Gordon; no ICE entries without his yes; no new project without his yes.

## Write step
Files written: `speakers.md`, `corrections.md`, `lexicon.md` (recurring corrections only), the summary, the target data files (cited lines), the moved transcript folder, the `pipeline.library` and `pipeline.status` requests, the session note. Receipt: one line, paths only, then the spot-check list when this is the first ingest.
