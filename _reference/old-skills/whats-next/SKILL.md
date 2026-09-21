---
name: whats-next
description: |
  Universal "what's next?" scan for all Jarvis instances. Triggers when Gordon says "what's next," "what now," "next," or any variation. Also fires proactively at conversational lulls — after completing a task, at idle moments, or at natural transitions. This skill is environment-aware: each instance only surfaces items IT can act on. The Nerd skips calendar/personal/routine items. The Mouth skips pipeline processing. Cross-instance items only appear if this instance is blocked waiting on the other. Mechanical items get auto-executed and reported as done. Output is fast and tight: item count + top 3, ranked by priority.
---

# What's Next

Fast priority scan. Not a rebuild — a pivot. 30 seconds to determine what this instance should do next.

---

## When This Triggers

- **Explicit:** Gordon says "what's next," "what now," "next," "what should we do," "what else," or any variation
- **Proactive:** After completing a task, at conversational lulls, when Gordon goes idle briefly, or at natural topic transitions
- **Proactive tone:** Keep it conversational, not formal. "While we're between things — 4 items on deck, top one is..."

---

## Environment Awareness

**Detect your role before scanning.** Platform + context determines what you check:

| Instance | Platform | Checks | Skips |
|----------|----------|--------|-------|
| **Mac Nerd** | darwin, Claude Code | nerd-inbox, pipeline, git state, earballs, processing tasks | Calendar, personal routine, Wrike dashboard, client check-ins |
| **Desktop Nerd** | win32, Claude Code | nerd-inbox, pipeline, git state, earballs, processing tasks | Calendar, personal routine, Wrike dashboard, client check-ins |
| **Mac Mouth** | darwin, Cowork | mouth-inbox, calendar, action-items, ticklers, Wrike, client work, personal items | Pipeline processing, earballs transcription, code execution |
| **Desktop Mouth** | win32, Cowork | mouth-inbox, calendar, action-items, ticklers, Wrike, client work, personal items | Pipeline processing, earballs transcription, code execution |

**Cross-instance items:** Only surface if YOU are blocked waiting on the other instance. "Desktop Nerd hasn't responded on rec_b93617d643 — sent 2 hours ago" is useful. "Desktop Nerd is processing 3 recordings" is not (that's their problem, not yours).

---

## The Scan

Run ALL applicable checks. Order matters — this is the priority stack:

### Priority 1: Urgent / Blocking
- **Comms check:** `curl -s http://100.64.67.85:18790/health` (mesh). Any signals waiting for this instance?
- **Inbox:** Check `nerd-inbox/` (Nerd) or `comms/mouth-inbox/` (Mouth) for dispatches addressed to this instance
- **Blocked items:** Anything this instance sent to another instance that hasn't come back

### Priority 2: Time-Sensitive
- **Ticklers:** `tickler/` — anything dated today or overdue
- **Calendar:** (Mouth only) Upcoming meetings/deadlines within 2 hours
- **Pipeline alerts:** (Nerd only) Failed or stalled processing jobs

### Priority 3: Dispatched Work
- **Inbox tasks:** Unexecuted dispatches in nerd-inbox or mouth-inbox
- **Action items tagged to this role:** Items in `personal/action-items.md` marked as Nerd job, Mouth task, etc.

### Priority 4: Available Work
- **Earballs pipeline:** (Nerd) New recordings to process, reconciliations pending
- **Stale items:** Action items not touched in 2+ weeks that this instance could move

### Priority 5: Proactive
- **Earballs inbox:** (Nerd) New files to ingest
- **Plaud sync:** (Nerd) Check for new recordings to download
- **System health:** Anything that looks off (stale ticklers piling up, pipeline anomalies)

---

## Auto-Execute

If any item in the scan is purely mechanical and needs zero Gordon input, **do it and report it as done:**

- Process earballs recordings → do it, report "Processed 3 recordings"
- Execute a nerd-inbox dispatch that's unambiguous → do it, report "Executed: [dispatch summary]"
- Archive completed inbox dispatches (status: completed) → move to `nerd-inbox/_completed/` or `comms/mouth-inbox/_completed/`, report "Archived: [list]"
- Git commits are handled by auto-sync — never surface uncommitted files or offer to commit
- Reconcile transcripts → do it, report "Reconciled 2 transcripts"
- Plaud sync → do it, report "Synced 4 new recordings"

**Do NOT auto-execute:**
- Anything involving sending email or messages to people
- Anything that deletes files
- Anything ambiguous or requiring judgment
- Commits (always ask)

---

## Output Format

**First response — always this structure:**

```
**[N] actionable items.** Top [3 or fewer]:

1. **[Priority tag]** [One-line description] → [action: what you'll do or what Gordon needs to decide]
2. **[Priority tag]** [One-line description] → [action]
3. **[Priority tag]** [One-line description] → [action]

[If auto-executed items]: Already handled: [brief list of what was done silently]
```

**Priority tags:** `BLOCKING` `TIME-SENSITIVE` `DISPATCHED` `AVAILABLE` `PROACTIVE`

**If nothing:** "Clean board — nothing pending for [instance name]."

**If Gordon wants more:** He asks. Don't dump the full list unprompted.

---

## Rules

- **Speed over thoroughness.** This is a 30-second scan, not a 5-minute audit. Check the sources, count the items, rank the top 3, present. Don't read every file in detail — scan for existence and recency.
- **Be honest about what you can't check.** If the mesh is down, say so. If you can't reach Wrike, say so. Don't pretend the board is clean when you couldn't check half the sources.
- **Don't duplicate morning-startup.** Morning-startup is a full boot. This is a fast pivot. If it's the first interaction of the day, morning-startup fires instead — don't run both.
- **Proactive ≠ nagging.** At conversational lulls, surface results once. If Gordon ignores it, don't repeat. One proactive fire per lull, max.
- **Auto-execute boldly but report transparently.** If you did something silently, always report it. Gordon should never wonder what changed.
