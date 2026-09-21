---
name: session-startup
description: |
  GordonOS session startup checklist for The Mouth (Cowork). Use this skill EVERY TIME: Gordon says "hey jarvis" or any variation, a new Cowork session begins, Gordon references Jarvis or GordonOS, Gordon loads CLAUDE.md or CORE.md, the workspace ~/PhpstormProjects/gordon-os-v2 is mounted, or it's the first interaction of a new day. This is the most fundamental workflow in GordonOS — it ensures Jarvis starts every session fully informed and nothing falls through cracks. If you recognize the Jarvis identity at all, trigger this skill before doing anything else.
---

# Session Startup — The Mouth

This skill runs the complete Jarvis startup sequence for Cowork (The Mouth). The startup exists because Jarvis has no persistent memory between sessions — every session starts cold. The checklist rebuilds situational awareness from disk so Gordon doesn't have to re-orient his AI assistant manually.

The startup is the single highest-leverage moment in any session. A thorough startup catches missed items, surfaces time-sensitive work, and prevents the "I told you about this yesterday" failure. A sloppy startup means Gordon spends the first 20 minutes discovering things Jarvis should have surfaced.

---

## Phase 1: Infrastructure (do these first, mechanically, no judgment calls)

### 1. Check time
```bash
date
```
Know what day and time it is. This determines which cadence items trigger (Monday review? Saturday checkin? First of month?).

### 2. Check Jarvis comms — mesh health + inboxes
```bash
curl -s http://100.64.67.85:18790/health
curl -s http://100.112.30.111:18790/health
curl -s http://100.69.201.51:18790/health
```
Check all three instances. Also scan:
- `comms/mouth-inbox/` — pending handoffs FROM Nerds
- `nerd-inbox/` — check for tasks still pending (were they picked up?)
- `comms/signals.json` — recent signals

Fallback if mesh is unreachable: `curl -s "https://ntfy.sh/gordonos-jarvis-z5v2hdt0/json?poll=1&since=24h"`

Surface anything real briefly. Filter out routine git-push/auto-commit noise.

### 3. Read session state
Read `comms/session-state.md` — this is what the LAST session left behind. It tells you what was in-flight, what decisions were made, what's awaiting Nerd work. Don't start fresh when there's a handoff from yourself.

### 4. Git sync
The Cowork FUSE mount cannot run git safely. Do NOT run raw git commands. Instead:
- Check if the repo is reasonably fresh (file modification times)
- If the Mac Nerd is online, signal it to pull: `curl -s -X POST http://100.64.67.85:18790/signal -H "Content-Type: application/json" -d '{"from":"mac-mouth","to":"mac-nerd","type":"task","summary":"git pull gordon-os-v2"}'`

### 5. Verify file server (Windows only)
If on Windows desktop: `curl -s http://192.168.1.96:8765/Sync/Gordonium%20Enterprises%20Sync/gordon-os-v2/CLAUDE.md | head -5`
If it fails, alert Gordon — Task Scheduler server isn't running.

---

## Phase 2: Situational Awareness (read the landscape)

### 6. Inbox triage
Check `personal/inbox.md` for pending items. If anything is there, it needs routing BEFORE other work. Nothing enters the active system without a triage decision.

### 7. Tickler scan
Scan `tickler/` for files dated today or earlier.
- Surface immediately — overdue items are missed reminders
- **Zombie check:** If any item is resurfacing for the 2nd+ time with no progress, flag it for kill-or-convert (three options: kill, convert to real action item, or defer to specific date with reason). "Resurface next session" is NOT valid.

### 8. Check dashboard
Read `work/dashboard.md` for big-picture client status. Don't present the whole thing — note anything that's changed or needs attention.

### 9. Wrike dashboard (weekdays only)
On Mac: `python3 tools/wrike.py dashboard`
Skip on weekends. Skip on Windows (MCP not configured for Cowork — note the gap).
- **Monday:** Also do delegation scan — look for tasks tagged "w. Claude" or automation candidates.

### 10. Calendar look-forward
Read Gordon's calendar. Proportional depth:
- Morning → 1-2 days
- Weekly → 1 week
- Saturday → 2 weeks
- Monthly → full month+

**Day-specific cadences:**
- Monday + Friday: Surface `routines/weekly-work-review.md` (Mon=full, Fri=straggler catch)
- Saturday: Surface `routines/saturday-personal-checkin.md`. First Saturday of month: also `routines/monthly-personal-review.md`
- First Monday of month: Also `routines/monthly-business-review.md`

### 11. Meeting prep briefings
For each upcoming meeting/event with named attendees:
- Pull their people file (`relationships/people/`) and recent context
- 30-second briefing: who they are, what matters, last interaction
- **Conversation prep (3 categories):** (1) Interesting things Gordon's been doing (gives openers), (2) Personal questions to ask them (from people files), (3) General interesting topics for them
- Business meetings: add **Punnett Square** (Gordon's worst/best, their worst/best)
- Social events: personal details, family updates, shared interests
- Surface: what Gordon owes them, what they owe Gordon
- If meeting >2 hours away, note for later. If <2 hours, brief now.

---

## Phase 3: Personal Layer (Gordon doesn't open Wrike for personal stuff — this IS that function)

### 12. Surface personal items
Scan these for anything time-sensitive or relevant:
- `personal/action-items.md` — verify items are still `- [ ]` before surfacing (disk is truth)
- `personal/content-backlog.md`
- `personal/` directory broadly
- `home/` directory

### 13. Energy/cycle awareness
Factor bipolar II pattern into planning — gently, not clinically. After high-output periods, don't stack hard things. Read CORE.md neurology section if needed for context.

---

## Phase 4: Earballs Check (does NOT run the full ingest — that's a separate skill)

### 14. Check for new transcripts
Scan `data/earballs-transcripts/` for anything processed since last session. If new transcripts exist:
- Note how many, from which dates
- DO NOT start ingesting here — that triggers the earballs-ingest skill separately
- Just surface: "There are X new recordings ready for ingestion. Want to process them now or after we handle other priorities?"

---

## Phase 5: Wrap Up and Hand Off to Gordon

### 15. Cross-check Morning Pickup
Verify each item you're about to surface against its source file. Prevents stale reminders from surviving compaction.

### 16. Present the briefing
Deliver everything from above in a clean, scannable format. Don't dump a wall — prioritize:
1. Anything time-sensitive or overdue
2. Comms from other instances
3. Today's calendar + meeting briefings
4. Tickler items
5. Earballs status
6. Personal items worth noting

### 17. Ask Gordon
"What's the focus today?" — then listen.

---

## Important Notes

- **Don't skip steps because Gordon seems eager to talk about something.** Run the checklist. If he's mid-sentence about a topic, you can weave it in, but the infrastructure checks (comms, tickler, calendar) still happen.
- **Don't summarize the startup as "everything looks good."** Surface specifics or say nothing. Vague reassurance is worse than silence.
- **The startup is NOT the place to do deep work.** It's a scan. If something needs a deep dive (a complex tickler, a meeting that needs strategy), note it and come back after the scan is complete.
- **Write session-state.md** after completing startup with today's date and what was surfaced. This is your first write of the session.
