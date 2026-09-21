---
name: morning-startup
description: |
  GordonOS morning startup for The Mouth (Cowork). REPLACES session-startup. Use this skill EVERY TIME: Gordon says "hey jarvis" or any variation, a new Cowork session begins, Gordon references Jarvis or GordonOS, Gordon loads CLAUDE.md or CORE.md, the workspace ~/PhpstormProjects/gordon-os-v2 is mounted, it's the first interaction of a new day, or Gordon gives any morning greeting. This is THE startup skill — the most fundamental workflow in GordonOS. It rebuilds full situational awareness from disk, runs the personal morning routine, and hands Gordon a clean briefing. If you recognize the Jarvis identity at all, trigger this skill before doing anything else.
---

# Morning Startup — The Mouth

This skill runs the complete Jarvis startup and morning routine for Cowork (The Mouth). It replaces `session-startup` as the single entry point.

Jarvis has no persistent memory between sessions. Every session starts cold. This checklist rebuilds situational awareness from disk, catches missed items, surfaces time-sensitive work, runs the personal morning routine, and prevents the "I told you about this yesterday" failure. A sloppy startup means Gordon spends the first 20 minutes discovering things Jarvis should have surfaced.

---

## Phase 1: Infrastructure (mechanical, no judgment — just do these)

### 1. Check time and date
```bash
date
```
Temporal orientation. The date determines which cadence items trigger — Monday review? Saturday checkin? First of the month? Weekend (skip Wrike)?

### 2. Check Jarvis comms — mesh health + inboxes
```bash
curl -s http://100.64.67.85:18790/health
curl -s http://100.112.30.111:18790/health
curl -s http://100.69.201.51:18790/health
```
Check all three instances (Mac, Desktop, Copper). Also scan:
- `comms/mouth-inbox/` — pending handoffs FROM Nerds
- `nerd-inbox/` — tasks still pending (were they picked up?)
- `comms/signals-mac-nerd.jsonl` and `comms/signals-desktop-nerd.jsonl` — recent signals

Fallback if mesh unreachable: `curl -s "https://ntfy.sh/gordonos-jarvis-z5v2hdt0/json?poll=1&since=24h"`

Surface anything real briefly. Filter out routine git-push/auto-commit noise.

### 3. Read session state + overnight completion report
Read `comms/session-state.md` — this is what the LAST session left behind. It tells you what was in-flight, what decisions were made, what's awaiting Nerd work. Don't start fresh when there's a handoff from yourself.

**Overnight thread check:** If session-state.md contains a "Threads closed tonight" section (written by the evening-winddown skill), verify each thread's current status. For any thread that involved overnight Nerd work, check whether it completed. Present a brief completion report during the briefing (Phase 6, Step 17): *"Overnight: [thread] — completed / still running / failed."* This closes the loop from the bedtime handoff — Gordon handed these off and needs to hear they landed.

### 4. Git sync
Cowork FUSE mount cannot run git safely. Do NOT run raw git commands. Instead:
- Check if the repo is reasonably fresh (file modification times)
- If the Mac Nerd is online, signal it to pull: `curl -s -X POST http://100.64.67.85:18790/signal -H "Content-Type: application/json" -d '{"from":"mac-mouth","to":"mac-nerd","type":"task","summary":"git pull gordon-os-v2"}'`

### 5. Verify file server (Windows only)
If on Windows desktop: `curl -s http://192.168.1.96:8765/Sync/Gordonium%20Enterprises%20Sync/gordon-os-v2/CLAUDE.md | head -5`
If it fails, alert Gordon — Task Scheduler server isn't running.

---

## Phase 2: Pipeline & Ingest

### 6. Check earballs pipeline status
**First:** Read `data/pipeline-health.json` (written by Layer 3 watchdog every 30 min). Check `sla_status`:
- **BREACH** → Surface as P1 before everything else. Dispatch Nerd to fix immediately.
- **WARNING** → Surface briefly, note what's stale.
- **OK** → Report "Pipeline healthy" and move on.
- **Missing or >6h stale** → Watchdog itself is dead. Dispatch Nerd: `python3 tools/pipeline-health-check.py --gate`

Also check `data/earballs-pipeline-statuses.md` and scan `data/earballs-transcripts/` for anything processed since last session.

If new transcripts exist:
- Note how many, from which dates
- Trigger the `earballs-ingest` skill (mechanical first step: `Read tools/skills/earballs-ingest/SKILL.md`)
- If no new transcripts, just report pipeline status briefly

### 7. Triage ALL new items
Process everything that arrived since last session:
- `comms/mouth-inbox/` — Nerd handoffs (execute on receipt per inter-instance authority rule)
- Signals from mesh — acknowledgments, completions, requests
- `tickler/` — scan for files dated today or earlier
  - Overdue items = missed reminders, surface immediately
  - **Zombie check:** If any item is resurfacing for the 2nd+ time with no progress, flag for kill-or-convert (three options: kill, convert to real action item, or defer to specific date with reason). "Resurface next session" is NOT valid.
- Nerd completions — check if dispatched work came back
- Email — check for anything requiring response (via Nerd relay)

---

## Phase 3: Open Items

### 8. Check action items
Read `personal/action-items.md`. Verify items are still `- [ ]` before surfacing — disk is truth, memory is draft. Note anything time-sensitive, overdue, or changed since last session.

### 9. Check work dashboard
Read `work/dashboard.md` for big-picture client status. Don't present the whole thing — note anything that's changed or needs attention.

### 10. Wrike dashboard (weekdays only)
On Mac: `python3 tools/wrike.py dashboard`
Skip on weekends. Skip on Windows (MCP not configured for Cowork — note the gap).
- **Monday:** Also do delegation scan — look for tasks tagged "w. Claude" or automation candidates.

---

## Phase 4: Personal Morning Routine

### 11. Present the morning routine checklist
Read `routines/morning-routine.md` and present the FULL morning routine as a checklist — all items at once, not drip-fed one by one. Gordon batch-responds to what he did and didn't do.

The checklist (current Phase 1 items):
- [ ] Gratitude in first thoughts + teeth brushing ("Today is a Bonus Day")
- [ ] Mood check-in: "Am I feeling expansive or contractive?"
- [ ] Breathwork
- [ ] Morning Pages
- [ ] Kitchen / coffee / eat something
- [ ] Coffee + Leah (~30 min, protected)
- [ ] "What have you eaten today?"
- [ ] Memory practice (mini memory palace, name recall, holding thoughts)
- [ ] Check the Counter List
- [ ] Calendar look-forward (1-2 days)

### 11b. Think Better curriculum prompt
After the morning routine checklist, ask: *"When in the day can you find an hour to work on the Think Better curriculum?"* (`personal/think-better.md`). First step: download Anki, create one deck, 2 min/day. Ask every morning until Gordon says it's become habit. `[T122, earballs:2026-03-14]`

### 12. Process Gordon's responses
When Gordon batch-responds:
- Use the `write-it-down` skill — log responses to disk immediately
- Track patterns over time for Saturday/monthly reviews (what's consistent, what's slipping, what's improving)
- Don't lecture or coach on missed items — just capture. Pattern feedback happens in reviews, not daily.

---

## Phase 5: Calendar & Meeting Prep

### 13. Calendar look-forward
Proportional depth based on day:
- Morning (weekday) -> 1-2 days
- Weekly -> 1 week
- Saturday -> 2 weeks
- Monthly -> full month+

### 14. Meeting prep briefings
For each upcoming meeting/event with named attendees:
- Pull their people file (`relationships/people/`) and recent context (last meeting notes, open action items, recent earballs mentions)
- 30-second briefing: who they are, what matters to them, last interaction
- **Conversation prep (3 categories):**
  1. Interesting non-work things Gordon has been doing lately (gives him openers)
  2. Personal questions to ask them (kids, hobbies, travel — from people files)
  3. General interesting topics based on who they are
- **Business meetings:** Add Punnett Square (Gordon's worst/best outcome, their worst/best outcome)
- **Social events:** Personal details, family updates, shared interests — the "West Wing chief of staff" briefing
- Surface: what Gordon owes them, what they owe Gordon
- If meeting >2 hours away, note for later. If <2 hours, brief now.

### 15. Day-specific cadence triggers
Check the date and fire the appropriate routines:
- **Thursday:** Confirm Friday review time is available on calendar
- **Friday:** Trigger `weekly-work-review` skill (surface `routines/weekly-work-review.md`)
- **Last Friday of month:** Also trigger `monthly-business-review` skill (surface `routines/monthly-business-review.md`)
- **Saturday:** Trigger `saturday-personal` skill (surface `routines/saturday-personal-checkin.md`). First Saturday of month: also trigger `monthly-personal-review` skill (surface `routines/monthly-personal-review.md`)
- **Sunday:** Trigger `sunday-routine` skill
- **Monday + Friday:** Surface `routines/weekly-work-review.md` (Mon=full review, Fri=straggler catch)
- **First Monday of month:** Also surface `routines/monthly-business-review.md`

---

## Phase 6: Priorities & Handoff

### 16. Cross-check everything
Verify each item you're about to surface against its source file. Prevents stale reminders from surviving compaction. If something in session-state.md doesn't match disk, disk wins.

### 17. Present the briefing
Deliver everything from above in a clean, scannable format. Prioritize:
1. Anything time-sensitive or overdue
2. Comms from other instances
3. Today's calendar + meeting briefings
4. Tickler items
5. Earballs status / new transcripts
6. Personal items worth noting
7. Morning routine checklist

### 18. Energy/cycle awareness
Factor bipolar II pattern into planning — gently, not clinically. After high-output periods, don't stack hard things. If yesterday's session-state shows a big output day, suggest lighter focus today. Read CORE.md neurology section if needed for context.

### 19. Write session-state.md
Update `comms/session-state.md` with today's date and what was surfaced during startup. This is the first write of the session. Skill doesn't fully complete until this is written.

### 20. Ask Gordon
"What's the focus today?" — then listen.

---

## Important Notes

- **Don't skip steps because Gordon seems eager to talk about something.** Run the checklist. If he's mid-sentence about a topic, weave it in, but the infrastructure checks (comms, tickler, calendar) still happen.
- **Don't summarize the startup as "everything looks good."** Surface specifics or say nothing. Vague reassurance is worse than silence.
- **The startup is NOT the place to do deep work.** It's a scan. If something needs a deep dive (a complex tickler, a meeting that needs strategy), note it and come back after the scan is complete.
- **If Nerd work was dispatched during startup, the skill doesn't complete until Nerd confirms.** Note what's pending in session-state.md.
- **This replaces `session-startup`.** Same infrastructure, but adds the personal morning routine (Phase 4) and reorganizes the flow. If both skills are loaded, use this one.
