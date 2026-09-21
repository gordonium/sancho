---
name: saturday-personal
description: |
  Saturday morning personal check-in for GordonOS. Triggered by morning-startup detecting Saturday. No client work. No Wrike. Just Gordon stuff. Two parts: (1) GordonOS system review — 10-15 min audit of what shipped, what broke, system health, and improvements to consider, (2) Personal projects — walk through the standing review list in routines/saturday-personal-checkin.md, surface research results, price alerts, personal projects, media, bigger projects, and calendar look-forward. One personal project gets 30-60 min of focused thought or action. Quick-check mode: touch everything, faster pace. First Saturday of month: monthly-personal-review stacks on top (run both, don't absorb).
---

# Saturday Personal Check-in

Saturday morning is Gordon's time. No client work. No Wrike. Just the system and personal projects.

This skill is triggered by morning-startup detecting Saturday. It reads from `routines/saturday-personal-checkin.md` at trigger time for the current standing review list.

---

## When This Triggers

- **Saturday morning** — detected automatically during morning-startup sequence
- **First Saturday of month:** also trigger `monthly-personal-review` skill (stacks on top — run both separately, don't absorb one into the other)

---

## Part 1 — GordonOS & Jarvis System Review

*Budget 10-15 min. Run this first, before personal projects.*

**The question to hold:** Is the system getting faster, smarter, and more trustworthy — or just bigger?

### Step 1: Pulse check

Open with a 2-3 sentence summary: what changed in GordonOS this week, what patterns emerged, anything worth flagging. Then ask:

*"Anything bugging you about how the system is working?"*

### Step 2: Walk the checklist

1. **What shipped** — any new rules, tools, automations this week? Are they landing?
2. **What broke or slipped** — unexpected compactions, missed items, wrong attributions, sync failures? Patterns matter more than one-offs.
3. **CLAUDE.md health** — still lean and scannable? If it's feeling long, propose a split.
4. **Nerd queue** — open tasks growing or shrinking? Anything stale?
5. **Earballs backlog** — queue trending up or down? If growing, schedule a quick-confirm session.
6. **Improvements to consider** — surface items from `personal/open-questions.md` → GordonOS Architecture section. Review what's on deck, then pick what to implement.
7. **Anything to retire** — tools, rules, or workflows not pulling their weight?
8. **Opus version check** — is the current model still the latest Opus? If Anthropic has shipped a newer version, flag it for update across all instances.

Full improvement backlog lives in `personal/open-questions.md` → GordonOS Architecture section.

---

## Part 2 — Personal Projects

### Step 1: Read the standing review list

Read `routines/saturday-personal-checkin.md` for the current state. The review list there is the source of truth — it has the actual items, statuses, and source tags.

### Step 2: Walk through each section

Present each section from the routine file:

1. **Research results to review** — anything ready for decision or action?
2. **Price alerts** — TSLA, BTC, DOGE — check current prices and any major news
3. **Personal projects** — any movement this week? Anything newly actionable?
4. **Media & entertainment** — watchlist, reading, things to check out
5. **Bigger projects** — longer-arc items that need periodic attention
6. **Calendar look-forward (2 weeks)** — scan the next two weeks for trips, deadlines, meetings that need prep. Surface anything that needs action now to avoid a crunch later.

### Step 3: Pick one

One personal project gets 30-60 min of focused thought or action. Let Gordon choose, or suggest one that seems ripe.

### Step 4: Check open questions

Scan `personal/open-questions.md` for any deep threads that are ready for attention. Surface but don't pressure.

---

## Quick-Check Mode

Touch everything, faster pace. Don't pressure Gordon to hit every item every week — the goal is to keep the most important things visible and make progress on one or two.

**Remember:** This is Gordon's fountain brain in action. The pile will always grow. The goal isn't to empty it — it's to keep the most important things visible.

---

## First Saturday of Month

When it's the first Saturday, stack the `monthly-personal-review` skill on top. Run both:

1. Saturday personal (this skill) — system review + personal projects
2. Monthly personal review — deeper health, relationships, aspirations check

They are separate skills with separate checklists. Don't merge them.
