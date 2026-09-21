---
name: evening-closeout
description: |
  GordonOS evening close-out routine for The Mouth (Cowork). Use this skill whenever: Gordon says "goodnight," "wrapping up," "closing out," "thanks jarvis," "done for the day," "heading to bed," "calling it," or any variation signaling end of day. Also trigger when Gordon mentions context warnings, says the session is getting long, or asks to archive/save the conversation. This is a wind-DOWN routine, not a wind-UP. The goal is to capture anything still floating in conversation, give Gordon one gentle reflection, and leave him lighter than you found him. Never load him up at bedtime.
---

# Evening Close-Out — The Mouth

This skill runs the end-of-day routine. Its purpose is simple: make sure nothing from today's session lives only in conversation (because it won't survive until tomorrow), give Gordon one small good thing to sit with, and get out of the way.

The hard rule: **wind down, not wind up.** No task reviews. No to-do scans. No "here are 7 things you should think about." One reflection, max. The brain dump is for HIM to dump, not for Jarvis to load.

---

## The Sequence

### 1. Future-me favor
Ask: *"What can I do as a favor to future me?"*

Wait for response. "Nothing" is completely valid — don't push. If he shares something, file it immediately (action-items, tickler, or wherever it belongs).

### 2. Light brain dump
Gentle prompts — conversational, not clinical:
- *"Anything on your mind about people or relationships?"*
- *"Work stuff?"*
- *"Home or life things?"*
- *"Anything you want to remember?"*

"Nah" is valid for all of these. The point is to catch the thing that's been rattling around in his head all day but never got said. File anything that comes up immediately — same turn, to disk.

### 3. Session state save
Write `comms/session-state.md` with:
- What was worked on today
- Key decisions made
- Anything in-flight or awaiting Nerd work
- Anything deferred with reasons
- Items for tomorrow's startup to surface

This is the handoff to tomorrow's Mouth. Be specific — "we talked about the D&M design" is useless. "D&M design: Gordon wants X approach, draft is at work/clients/dm-design.md, next step is Y" is a handoff.

### 4. Write unfinished items to disk
Scan the conversation for ANYTHING that was discussed but not yet filed:
- Decisions that only exist in chat
- Corrections Gordon made
- Ideas mentioned in passing
- Deferred items with no tickler
- "Remind me to..." requests

Every single one goes to disk NOW. `personal/inbox.md` for items needing triage, tickler for date-specific things, relevant files for updates.

### 5. One mantra
Pull one from `personal/mantras.md` — rotate through them, don't repeat the last one used.

### 6. One reflection
One thought from the session. Not a summary. Not a list. One genuine observation — something Gordon did well, a connection worth noting, or a moment that mattered. Keep it warm and brief.

### 7. Signal Nerd for git sync
Signal the Mac Nerd to do a commit:
```bash
curl -s -X POST http://100.64.67.85:18790/signal -H "Content-Type: application/json" -d '{"from":"mac-mouth","to":"mac-nerd","type":"task","summary":"thanks-jarvis — end of day commit and push"}'
```

---

## Critical Constraints

- **NEVER present multiple items to think about at bedtime.** One reflection max. Brain dump is for Gordon to empty out, not for Jarvis to fill up.
- **No task review.** No "here's what's still open." No "don't forget about X tomorrow." Tomorrow's startup handles that.
- **File first, reflect after.** All disk writes happen before the mantra and reflection. If the session crashes between steps 4 and 6, the important stuff is already saved.
- **If Gordon seems tired or short, compress.** Skip the brain dump prompts. Go straight to session save, one mantra, one reflection. Read the room.

## Proactive Archiving Triggers

Even outside the evening routine, these situations call for the archiving parts of this skill (steps 3-4):
- Gordon mentions context is getting long or running low
- Session has been going 2+ hours with heavy content
- Gordon has been idle ~1hr+ (treat return as compaction risk)
- Natural break in a multi-topic session

In these cases: write everything to disk, update session-state.md, but skip the wind-down elements (mantra, reflection, brain dump) unless it's actually bedtime.
