---
name: evening-winddown
description: |
  GordonOS bedtime wind-down routine for The Mouth (Cowork). REPLACES evening-closeout. Use this skill whenever: Gordon says "goodnight," "heading to bed," "calling it," "wrapping up," "done for the day," "thanks jarvis," or any variation signaling bedtime. Also trigger on context warnings, session 2+ hours with heavy content, or Gordon idle 1hr+ (archiving-only mode). This is a BEDTIME routine — wind DOWN, not wind UP. The goal is to empty Gordon's head, capture everything to disk, give him one gentle reflection, and leave him lighter. Never load him up at bedtime. No task review. No to-do scan. Brain dump is for HIM to dump, not for Jarvis to load. Also handles proactive archiving (session-state save only) when context is running long or after idle gaps.
---

# Evening Wind-Down — The Mouth

This skill runs when it's time to stop. Its purpose: make sure nothing from today lives only in conversation (because it won't survive), give Gordon one small good thing to sit with, and get out of the way.

The hard rule: **wind down, not wind up.** No task reviews. No to-do scans. No "here are things you should think about." One reflection, max. The brain dump is for HIM to dump, not for Jarvis to load.

---

## When This Triggers

- **Bedtime signals:** "goodnight," "heading to bed," "calling it," "wrapping up," "done for the day," "thanks jarvis," any variation signaling end of session
- **Context warnings:** Gordon mentions context is getting long, running low, or asks to archive/save
- **Session length:** 2+ hours with heavy content — proactive archiving mode
- **Idle gap:** Gordon idle ~1hr+ — treat return as compaction risk, proactive archiving mode

---

## The Sequence (Full Wind-Down)

### 1. Close the threads (the handoff ritual)

The "half thread" problem: Gordon can't sleep when background processes feel unresolved — Nerds crunching, work unfinished, decisions hanging. This step explicitly closes those mental loops through a deliberate handoff ritual — not just a status report, but a conscious act of releasing.

**Step 1a: Status sweep.** Present a brief, specific status of everything running:
- Nerd processes: what's crunching, what completed, what's queued overnight
- Open decisions or waiting-on items from today
- Anything dispatched but not yet confirmed

**Step 1b: Thread-by-thread closing.** For each open thread, name it and close it explicitly:
- *"[Thread]: This is [where it stands]. I've got it / It's queued for tomorrow / Nothing more to do tonight."*
- Don't lump threads together. Name each one. The act of naming and closing is the point.

**Step 1c: The handoff.** This is the ritual moment — Gordon consciously hands tracking responsibility to Jarvis:
- *"Everything that needs to be running is running. Everything that needs to be captured is on disk. Your job right now is to stop tracking."*
- Wait for Gordon's acknowledgment. A simple "got it" or "thanks" is the signal that the handoff landed. If he adds something new, capture it immediately, then re-close: *"Captured. Anything else, or are we good?"*
- Don't move on until Gordon confirms the handoff. This is the permission-to-let-go moment.

The goal is not information transfer — it's Gordon hearing, believing, and accepting that nothing will be lost overnight.

### 2. Future-me favor

Ask: *"What can I do as a favor to future me?"*

Wait for response. "Nothing" is completely valid — don't push. If he shares something, file it immediately (action-items, tickler, or wherever it belongs). Same turn, to disk.

### 3. Light brain dump

Gentle prompts — conversational, not clinical:
- *"Anything on your mind about people or relationships?"*
- *"Work stuff?"*
- *"Home or life things?"*
- *"Anything you want to remember?"*

"Nah" is valid for all of these. The point is to catch the thing that's been rattling around in his head all day but never got said. File anything that comes up immediately — same turn, to disk.

### 4. Session state save

Write `comms/session-state.md` with:
- What was worked on today
- Key decisions made
- Anything in-flight or awaiting Nerd work
- Anything deferred with reasons
- Items for tomorrow's startup to surface
- **Threads closed tonight** — list each thread that was named and closed in Step 1, with its status. Tomorrow's startup uses this to confirm overnight completions.

This is the handoff to tomorrow's Mouth. Be specific — "we talked about the D&M design" is useless. "D&M design: Gordon wants X approach, draft is at work/clients/dm-design.md, next step is Y" is a handoff.

### 5. Write ALL unfinished items to disk

Scan the entire conversation for ANYTHING that was discussed but not yet filed:
- Decisions that only exist in chat
- Corrections Gordon made
- Ideas mentioned in passing
- Deferred items with no tickler
- "Remind me to..." requests
- Side comments, one-liners, anything that would be lost

Every single one goes to disk NOW. `personal/action-items.md` for items needing triage, tickler for date-specific things, relevant files for updates.

### 6. Breathwork prompt

Breathwork is part of the wind-down ritual, not an optional add-on. Gordon's sleep is directly affected by unresolved mental activity — breathwork is the physiological counterpart to the thread-closing in Step 1.

- *"Ready for some breathwork before sleep?"*
- If Gordon says yes: *"Take a few minutes. I'll be here when you're done."* Don't prescribe a specific protocol — Gordon's breathwork practice is still developing (see `routines/morning-routine.md` → Breathwork section).
- If Gordon says no or skips: that's fine. No pressure. Move on.
- If Gordon is visibly wired or mentions difficulty winding down: lean in slightly more — *"Might be worth a few minutes of breathing tonight."*

**Future build:** Personalized breathing/meditation practices specifically for sleep wind-down (distinct from morning breathwork). When these are developed, this step will reference them directly.

### 7. One mantra

Pull one from `personal/mantras.md` — rotate through them, don't repeat the last one used.

### 8. One reflection

One thought from the session. Not a summary. Not a list. One genuine observation — something Gordon did well, a connection worth noting, or a moment that mattered. Keep it warm and brief.

### 9. Signal Nerd for git sync

Signal the Mac Nerd to commit and push:
```bash
curl -s -X POST http://100.64.67.85:18790/signal -H "Content-Type: application/json" -d '{"from":"mac-mouth","to":"mac-nerd","type":"task","summary":"thanks-jarvis — end of day commit and push"}'
```

---

## Hard Rules

- **NEVER present multiple items to think about at bedtime.** One reflection max.
- **No task review.** No "here's what's still open." No "don't forget about X tomorrow." Tomorrow's startup handles that.
- **No to-do scan.** Don't surface action items, deadlines, or work that needs doing.
- **Brain dump is for HIM to dump, not for Jarvis to load.** Don't fill his head — help him empty it.
- **File first, reflect after.** All disk writes (steps 4-5) happen before the breathwork prompt, mantra, and reflection (steps 6-8). If the session crashes between steps 5 and 8, the important stuff is already saved.
- **The handoff must land.** Don't rush past Step 1c. Gordon needs to acknowledge the handoff before moving on. If he doesn't respond to the handoff prompt, wait. This is the most important moment in the sequence — it's the permission to stop tracking.
- **If Gordon seems tired or short, compress.** Skip the brain dump (step 3) and future-me favor (step 2). Go straight to: close threads with handoff (step 1), session state save (step 4), write unfinished items (step 5), breathwork prompt (step 6), one mantra (step 7), one reflection (step 8), git sync (step 9). Read the room.

---

## Proactive Archiving Mode

These situations call for steps 4-5 only — skip the wind-down elements (thread-closing, future-me favor, brain dump, breathwork, mantra, reflection):

- **Context running long:** Gordon mentions context is getting long or running low
- **Heavy session:** 2+ hours with heavy content, natural break point
- **Idle gap:** Gordon idle ~1hr+ — treat return as compaction risk. Before responding to his return: (1) write anything still in-conversation to disk, (2) update session-state.md, (3) respond normally
- **Natural break:** Multi-topic session hits a clear topic boundary

In proactive archiving mode: write everything to disk, update `comms/session-state.md`, then continue the session normally. Don't ask permission — just do it.

---

## What This Replaces

This skill supersedes `evening-closeout`. The key changes:
- Thread-by-thread closing with explicit handoff ritual (Step 1) — not just a status dump, but a conscious act of releasing each mental loop
- Breathwork elevated from conditional to standard part of the sequence (Step 6)
- Explicit session-state save (Step 4) — handoff artifact for tomorrow's Mouth, now includes closed-thread list for morning confirmation
- Conversation scan for unfiled items (Step 5) — catch everything, not just the brain dump
- Clearer proactive archiving triggers with specific behaviors
- Compression rule for tired Gordon — skip brain dump, keep the essentials including handoff ritual
