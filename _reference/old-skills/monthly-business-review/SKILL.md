---
name: monthly-business-review
description: |
  GordonOS monthly business review for The Mouth (Cowork). Triggers on the last Friday of every month, stacking WITH weekly-work-review — run both, don't absorb. The question to hold: "Is the business getting healthier, and am I spending my time on the highest-leverage work?" Covers revenue & health, client roster, strategic bets, client Zoom tour, WoA partner developments, tools & systems, strategic pulse (DPC, Evel Spirits/Entomat, SongTipper), and one strategic question that gets real thinking time. Reads work/dashboard.md + client files. Quick-check mode available: touch everything, faster pace.
---

# Monthly Business Review — The Mouth

This skill runs on the last Friday of every month, stacking with `weekly-work-review`. The weekly review is operational (what shipped, what's due, task health). This review is strategic — it zooms out to the business level.

**The question to hold throughout:**

*Is the business getting healthier, and am I spending my time on the highest-leverage work?*

---

## When This Triggers

- **Last Friday of the month** — after weekly-work-review completes
- **Manual trigger** — Gordon asks for a business review at any time

This stacks WITH weekly-work-review. Run both. Don't absorb one into the other. The weekly review provides operational context that feeds naturally into the strategic lens here.

---

## The Sequence

Read `routines/monthly-business-review.md` at trigger time for the canonical checklist (including any items added since this skill was written), then walk through:

### 1. Revenue & health

CLC / Press Managed / WoA / DPC in aggregate. What's the trend direction? Up, flat, or down? Don't need exact numbers every month — direction and velocity matter more. If Gordon has revenue data available, use it. If not, qualitative assessment based on client activity and pipeline.

### 2. Client roster health

Walk through the roster: who's growing, holding, at risk, or winding down? Cross-reference `work/clients/` files and `work/dashboard.md`. For any client marked "at risk" or "winding down," surface what's driving it and whether there's an action.

### 3. Strategic bets burn rate

What is Gordon funding right now (Dragonfly ads, direct mail experiments, tool subscriptions, etc.)? Is it paying off? This isn't a formal P&L — it's a gut check on whether the investments feel right or feel like leaks.

### 4. Client Zoom tour

Any clients overdue for a face-to-face check-in? Some clients drift to email-only and the relationship cools. Flag anyone who hasn't had a Zoom/call in a month+ unless there's a reason for that rhythm.

### 5. WoA partner group developments

Anything worth noting from the partner group? New resources, shared learnings, partner changes, group dynamics. Also check: DropMark partner video backlog progress, custom AI knowledge base for partner group — any movement?

### 6. Tools & systems check

- MDI LLMKit / Mighty Data — any progress on auto-reporting backbone?
- David McInnis NewsTrends AI — worth pursuing?
- IT list for Alex — review `personal/it-list-alex.md`, anything overdue?
- GordonOS itself — any system gaps or improvements surfaced this month?

### 7. Strategic pulse

Three standing strategic threads, each gets a pulse check:
- **DPC venture** — where does it stand this month?
- **Evel Spirits / Entomat** — any Lizzie updates?
- **SongTipper** — monthly progress check, reference `work/clients/songtipper-ads-system.md`

### 8. One strategic question gets real thinking time

Pick the one question from the review that most deserves deep thought. Not a quick answer — actual thinking time. Use the `think-first` skill's analysis mode frameworks if it helps: first principles, inversion, second-order effects. Let Gordon sit with it. This is the strategic value of the review — not the checklist, but the one question that changes direction.

---

## After the Review

- Update `work/dashboard.md` with monthly status notes
- File any strategic decisions or direction changes to relevant files
- If the strategic question produced action items, write them to `personal/action-items.md` with context
- Note next monthly review date in `routines/monthly-business-review.md`

---

## Quick-Check Mode

When time is tight or Gordon says "let's keep it quick": touch every item in the sequence, but faster pace. One sentence per item instead of a full discussion. Flag only the things that need Gordon's attention — skip items where the answer is "no change." Still update `work/dashboard.md` at the end. The strategic question (step 8) still gets real time even in quick-check mode — that's the whole point.

---

## Source Files

- `routines/monthly-business-review.md` — canonical checklist (may have items added since this skill was written; always re-read at trigger time)
- `work/dashboard.md` — big picture client status and priority hierarchy
- `work/clients/` — individual client files
- `work/partners/` — WoA partner files
- `personal/it-list-alex.md` — IT task list
- `work/clients/songtipper-ads-system.md` — SongTipper project context
