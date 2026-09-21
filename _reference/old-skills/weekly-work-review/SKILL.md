---
name: weekly-work-review
description: |
  GordonOS weekly work review for The Mouth (Cowork). Triggers every Friday midday/afternoon via morning-startup. On Thursday, morning-startup checks the calendar to confirm Friday review time is available — if not, surfaces for rescheduling. This is a full work-week review: what shipped, what's due, client health, delegation opportunities, stalled items, Wrike cross-check, one priority for next week, and weekend Nerd handoff. Reads the Wrike dashboard and updates work/dashboard.md. On the last Friday of the month, monthly-business-review stacks on top — run both, don't absorb one into the other. Quick-check mode available: touch everything but at a faster pace.
---

# Weekly Work Review — The Mouth

This skill runs every Friday midday/afternoon. It's the full work-week review — the regular heartbeat that keeps client work, tasks, and commitments from drifting.

On Thursday, Jarvis checks the calendar to confirm Friday review time is available. If it's not (meetings stacked, travel day, etc.), surface it for rescheduling rather than skipping.

On the last Friday of the month, the `monthly-business-review` skill stacks on top. Run both — don't absorb or merge them. Weekly review is operational; monthly review is strategic. They serve different purposes.

---

## When This Triggers

- **Friday midday/afternoon** — triggered by morning-startup on Fridays
- **Thursday** — morning-startup checks calendar to confirm Friday review time is available. If not, surfaces for rescheduling
- **Manual trigger** — Gordon asks for a work review at any time

---

## The Sequence

Read `routines/weekly-work-review.md` at trigger time for the canonical checklist, then walk through:

### 1. What shipped this week?

Client deliverables, Wrike tasks completed, anything notable that moved from "in progress" to "done." This isn't just Wrike — include things Gordon worked on in conversations, earballs captures, emails sent, meetings that produced outcomes.

### 2. What's due next week?

Walk through next week's calendar + Wrike deadlines. Surface anything with a hard date. Flag anything that looks tight or at risk of slipping.

### 3. Client check-ins

Anyone overdue for contact? Any open loops from this week's calls or meetings? Cross-reference `work/clients/` files for last-contact dates and open items. If a client hasn't been touched in 2+ weeks and there's no reason for silence, flag it.

### 4. Delegation scan

Tasks tagged "w. Claude" or in SMALL TASK KILL that can be automated or delegated to Nerd. Look for:
- Repetitive tasks that should be scripted
- Research tasks the Nerd can handle autonomously
- File/data maintenance that doesn't need Gordon's judgment
- Weekend batch work opportunities

### 5. Stalled items

Anything in Wrike that hasn't moved in 2+ weeks. Don't just list them — for each one, ask: is this blocked, forgotten, or no longer relevant? Surface the distinction so Gordon can decide (kill, defer, or unblock).

### 6. Wrike tasks Jarvis created this week

Cross-check: did Gordon find them? Did they get actioned? If Jarvis created tasks that Gordon never saw, the pipeline has a gap. Surface it.

### 7. One priority for next week

What's the single most important thing to ship by next Friday? Not a list of 5 things. One thing. Help Gordon name it.

### 8. Hand off to weekend

Anything the Nerd can crunch over the weekend? Data processing, file cleanup, research, report generation — anything that benefits from uninterrupted compute time while Gordon's off.

---

## After the Review

- Update `work/dashboard.md` with current status
- Run Wrike dashboard: `python3 tools/wrike.py dashboard`
- File any new action items from the review to `personal/action-items.md`
- If weekend Nerd work was identified, write tasks to `nerd-inbox/` and signal the Nerd

---

## Quick-Check Mode

When time is tight or Gordon says "let's keep it quick": touch every item in the sequence, but faster pace. One sentence per item instead of a full discussion. Flag only the things that need Gordon's attention — skip items where the answer is "nothing new." Still update `work/dashboard.md` at the end.

---

## Monthly Stack

On the last Friday of the month, `monthly-business-review` runs after this review completes. Don't merge them — finish the weekly operational review first, then shift to the strategic monthly lens. The weekly review feeds context into the monthly review naturally.
