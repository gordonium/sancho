---
name: work-closeout
description: |
  GordonOS work-day closeout for The Mouth (Cowork). Use this skill whenever: Gordon says "wrapping up work," "closing the shop," "done for the day" (when clearly about work, not bedtime), "switching to personal time," it's end of work hours (~4-5pm) and Gordon signals transition, or Gordon says any variation of closing the work day. This is NOT the bedtime routine — that's evening-closeout. This skill closes the work day: captures open loops, files floating items, previews tomorrow, dispatches Nerd for overnight work, and writes a clean session-state handoff. The work day ends here; personal time begins after.
---

# Work Closeout — The Mouth

This skill closes the work day. It is NOT the bedtime routine — `evening-closeout` handles wind-down, mantras, reflection, and the gentle "nothing more to think about" exit. This skill is about making sure the work day is buttoned up: nothing is floating, nothing is forgotten, and tomorrow's Mouth has a clean handoff.

The distinction matters. Work closeout can happen at 4pm while Gordon still has a full evening ahead. Evening closeout happens at bedtime and is deliberately light. Mixing them up either loads Gordon up at bedtime (bad) or lets work items fall through cracks at day's end (also bad).

---

## Step 1: Open Loop Scan

Go through the day and surface every open loop:

### Promises made today
- To clients — anything committed in calls, emails, meetings
- To partners — WoA partners, collaborators
- To Leah — anything said in conversation that implies a to-do
- To anyone else — friends, vendors, service providers

For each: is it filed? Does it have a due date? Is it in action-items.md or Wrike? If not, file it NOW.

### Follow-ups owed
- Emails sent today that expect replies — are they tracked?
- Questions asked of others — are you waiting on answers?
- Requests made to Nerds — are they acknowledged?

### Dispatched Nerd work
Check signals for acknowledgments:
```bash
curl -s http://100.64.67.85:18790/health
```
Scan `comms/signals-mac-nerd.jsonl` and `comms/signals-desktop-nerd.jsonl` for today's signals. Are there dispatched tasks that haven't come back? Note them explicitly — don't assume they're running.

### Emails expecting replies
Scan today's sent emails (if accessible via Nerd relay) for anything that's waiting on a response. Note expected response timeframes if known.

---

## Step 2: Capture Floating Items

Scan the ENTIRE conversation for anything discussed but not yet filed:

- **Decisions** that only exist in chat — write to relevant files + session-state.md
- **Corrections** Gordon made — update the target files
- **Ideas** mentioned in passing — `personal/inbox.md` or the relevant project file
- **"Remind me" requests** — tickler file with specific date
- **Deferred items** — where do they live? If nowhere, file them now with a reason for deferral
- **New information about people** — update people files
- **Client context changes** — update client files and dashboard if needed

Use the `write-it-down` skill for each item. Every single one goes to disk. If it's not on disk, it doesn't survive to tomorrow.

---

## Step 3: Tomorrow Preview

Quick calendar glance at tomorrow:
- What meetings are scheduled?
- Any prep needed tonight or first thing in the morning?
- Any deadlines hitting tomorrow?
- Anything Gordon should know before he stops thinking about work?

Keep this brief — just enough to prevent morning surprises. Don't turn it into a planning session. If there's a meeting that needs serious prep, note it as a morning-startup item, don't try to do it now.

**Meeting prep suggestion:** If tomorrow has a non-recurring meeting with named attendees (especially new contacts or clients), suggest: *"You've got [meeting] tomorrow — want to run the Punnett Square tonight or first thing in the morning?"* This gives Gordon the option to prep the night before when it's fresh, or let morning-startup handle it. `[T058, punnett-square skill integration]`

**Standing evening suggestion:** Surface T124 (Todoist migration review) as a suggestion for personal time tonight. This is a blocking factor for Gordon self-managing personal tasks — remind DAILY until done. `[T124, triage:2026-03-30]`

---

## Step 4: Nerd Dispatch

Signal Nerd(s) for any end-of-day tasks:
- Overnight processing (earballs batch jobs, long-running scripts)
- Git sync / commit
- Any tasks that can run unattended

```bash
curl -s -X POST http://100.64.67.85:18790/signal -H "Content-Type: application/json" -d '{"from":"mac-mouth","to":"mac-nerd","type":"task","summary":"End of work day — [specific tasks]"}'
```

Write details to `nerd-inbox/` for anything non-trivial — signals are summaries only.

**Skill does NOT complete until Nerd loops are closed.** Either:
- Nerd acknowledges and tasks are confirmed running, or
- Nerd is offline and tasks are documented in nerd-inbox/ for pickup

Either way, note the state explicitly.

---

## Step 5: Write Session State

Update `comms/session-state.md` with a work-day summary:
- What was worked on today
- Key decisions made (with enough context to be useful, not just "discussed X")
- Open items — what's still in flight
- Awaiting Nerd — what was dispatched and its status
- Awaiting Gordon — anything needing his input tomorrow
- Awaiting others — client responses, partner replies, vendor follow-ups
- Tomorrow's priorities (if discussed or obvious from context)

This is the handoff to tomorrow's `morning-startup`. Be specific — "worked on client stuff" is useless. "D&M design: revised homepage wireframe per Gordon's feedback, draft at work/clients/dm-design.md, next step is Gordon reviews with Leah" is a handoff.

---

## What This Does NOT Include

- **Mantras** — that's `evening-winddown`
- **Brain dump** — that's `evening-winddown`
- **Reflection** — that's `evening-winddown`
- **Wind-down** — that's `evening-winddown`
- **Conversation archiving** — that's `evening-winddown` (or proactive archiving triggers)
- **"Thanks jarvis" git commit** — that's `evening-winddown`

This skill closes WORK. The evening skill closes the DAY. They may run back-to-back or hours apart depending on Gordon's schedule.

---

## Critical Constraints

- **Don't turn this into a planning session.** Capture and file, don't strategize. If something needs strategy, note it as a morning item.
- **Don't skip the conversation scan (Step 2).** This is where the most important stuff hides — decisions made casually mid-conversation that never got written down.
- **Don't present open loops as pressure.** "Here's what's still open" is informational, not a guilt trip. Gordon is closing work, not being audited.
- **File before presenting.** All disk writes happen before the summary. If the session crashes between steps, the captures are already saved.
