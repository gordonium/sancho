---
name: write-it-down
description: |
  Immediate disk-write enforcement for GordonOS. Use this skill EVERY TIME Gordon answers a question, makes a decision, gives feedback, confirms or denies something, says "yes/no/done/kill/defer/move/that's wrong/correct/flip that," responds to triage questions, or provides ANY information that changes the state of a task, file, or fact. Also trigger when Gordon answers multiple questions at once (batch responses). The core behavior is simple: WRITE TO DISK FIRST, before responding, before discussing, before asking the next question. "Noted" without a file write is a lie. If it's not on disk, it didn't happen. This is the most frequently violated rule in GordonOS and exists because context is unreliable — sessions compact, crash, and expire. Every piece of Gordon's input that lives only in conversation is data loss waiting to happen.
---

# Write It Down

This skill exists because of a simple, repeated failure: Gordon says something, Jarvis says "noted" or "got it," and then doesn't write anything to disk. The information lives only in conversation context, which compacts, crashes, or expires. The information is lost. Gordon has to repeat himself. Trust erodes.

The fix is mechanical: when Gordon gives you information, the FIRST thing you do is write it to disk. Not after discussion. Not after the next question. Not at the end of the batch. Immediately.

---

## When This Triggers

Any time Gordon provides input that changes state:

- **Task decisions:** done, defer, kill, reassign, update, "that's not mine," "that happened already"
- **Answers to questions:** "yes," "no," "Tuesday," "Leah," "skip it"
- **Corrections:** "that's wrong," "flip that," "other way around"
- **Feedback:** "that's not working," "do it differently," "stop doing X"
- **New information:** facts, dates, names, context, preferences
- **Batch responses:** Gordon answers 4 questions at once — write ALL 4 before responding

## What To Do

### 1. WRITE FIRST

Before composing your response, before asking the next triage question, before anything else — identify what needs to change on disk and change it.

Targets depend on what Gordon said:
- Task completed → mark `[x]` in `personal/action-items.md` (or use `task-ops.py complete`)
- Task deferred → update the task entry + create/update tickler file
- Task killed → mark with strikethrough or remove + note why
- Task reassigned → update ownership label in action-items.md
- Correction → update the target file with correction note
- New fact → write to the appropriate file (people, client, personal, home, etc.)
- Feedback/preference → update `comms/session-state.md` and/or the relevant standing rule or routine file
- Decision → write to `comms/session-state.md` under "Key Decisions This Session"

### 2. Confirm the write

After writing, briefly confirm what you wrote and where:
- "Updated T088 in action-items.md — marked as Leah's task."
- "Marked T093 done in action-items.md, logged to completed-items.md."

One line. Not a paragraph. Gordon doesn't need a ceremony — he needs proof it happened.

### 3. THEN continue the conversation

Only after the write is confirmed do you move on to the next question, the next topic, or any discussion.

---

## Batch Responses

When Gordon answers multiple questions at once (common during triage), process ALL answers before responding:

1. Read all answers
2. Make ALL disk writes (parallel if possible)
3. Confirm all writes in a brief list
4. Then continue with next batch of questions

Do NOT write the first answer and then ask about the rest. Write them all, confirm, move on.

---

## What "Noted" Actually Means

"Noted" with no file write = a lie. Don't say it. Either:
- Write it down and say "Written to [file]" — or
- Say "I'll write that now" and then immediately do it

If you catch yourself saying "noted," "got it," "understood," or "will do" without a file operation in the same turn, you've failed. The word is not the action. The file write is the action.
