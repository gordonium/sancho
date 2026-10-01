---
name: write-it-down
type: skill
lobe: both
shared:
description: The reflex, and the emergency override. Before every reply the session asks itself whether anything just got decided, stated, corrected or asked that is not on disk, and writes it first; when Gordon has to say "write that down" the reflex failed, and that gets logged as an error with a mechanism.
why: v2's facts lived in context and died with it; Gordon had to say "write that down" and still lost things. Structure does most of the writing (every skill ends with a write step); this is the backstop, and its use is measured.
triggers: ["write that down", "note that", "remember that", "log that", a decision or correction stated in conversation with no skill running, the end of any turn in which a fact about Gordon or his world was said]
must_not_trigger: [a request to summarize what was said (that is a read), small talk, a fact already on disk with the same cite]
reads: [the session note, the target file's INDEX, "the target file (to supersede, never overwrite)"]
writes: ["the target file: project.md, entity.md, knowledge.md, people/<slug>.md, decisions.md, personal/me/*.md, or the session note when nothing else fits", "_setup/ERRORS.md when the phrase was needed"]
chain: {front: "any conversation", next: "the skill that should have written, if one was running", gate: none}
test: _setup/tests/skills/write-it-down/
---
# write-it-down

## The reflex (runs before every reply, silently)

Did anything in the last exchange get **decided**, **stated as a fact** about Gordon or his world, **corrected**, or **asked** of Gordon and not yet answered? If yes:

1. Pick the home by the cascade: a project's `project.md` for its facts and next action; `entity.md` or `knowledge.md` for a client or business; `people/<slug>.md` for a person (one line, no dump); the level's `decisions.md` for a decision; `personal/me/brief.md`, `watch.md` or `mantras.md` for Gordon himself; the session note when nothing fits yet, with a line saying where it should land.
2. Write the line with its cite: `[gordon <date>]`, `[confirmed gordon <date>]` for a confirmation, `[rec_… hh:mm:ss]` for a recording. A fact that replaces an older one strikes the old line in place and adds the new one; nothing is overwritten (must-never 6).
3. A fact about Gordon's own state (health, mood, money, location) or about another person's is read back in the reply before it is relied on anywhere outside the session note; if he does not confirm, it stays in the note marked unconfirmed.
4. Name the file in the reply, in one clause, not a paragraph ("logged to dm-heating/decisions.md").

## The override ("write that down")

When Gordon says it, the reflex missed. Do the write exactly as above, then:

5. Log the miss in `_setup/ERRORS.md` as its own entry or as a tally line under the standing entry "write-it-down was needed": date, what was said, which skill or reflex should have caught it, and the mechanism (a trigger added to a skill, a field added to a template, a check added to the lint). The phrase working is not the fix; the design is judged by how rarely it is needed.

## Rules
- Write before replying, not after.
- Cite everything; a line without a cite is not written.
- No tasks for Gordon, no ICE entries, no new projects: propose, write on his yes.
- Never a whole-file rewrite of a data file; append or strike-and-add.

## Write step
Files written: the target file (and ERRORS.md on an override). Receipt: the file, in one clause of the reply.
