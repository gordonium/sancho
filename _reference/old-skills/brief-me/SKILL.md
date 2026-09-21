---
name: brief-me
description: |
  "Brief Me About..." — West Wing-style briefing skill for GordonOS. Use when Gordon says "brief me about [person/company/topic]," "what do we know about...," "prep me for [person]," "who is [name]," "fill me in on [topic]," or any variation requesting background on a person, company, or subject. Deep-searches the GordonOS knowledge base (people files, client files, partner files, transcripts, action items, open questions, memory DB), runs a fresh internet search for new context, and delivers a concise, actionable briefing. The West Wing model: chief of staff briefs the president before he walks into a room.
---

# Brief Me About...

Gordon walks into every room prepared. This skill makes that automatic — search everything we know, search the web for anything new, and deliver it in a format that makes him sharp without overwhelming him.

---

## When This Triggers

- Gordon says "brief me about [X]," "what do we know about [X]," "prep me for [person]," "who is [name]," "fill me in on [topic]," "catch me up on [X]"
- The `punnett-square` skill calls this for each meeting attendee
- The `morning-startup` skill's meeting prep (Step 14) can invoke this for named attendees
- Gordon asks to review context before a call, meeting, or event

**Do NOT trigger on:**
- Simple factual lookups ("what's their email?") — just answer directly
- Requests to read a specific file ("read the DM Heating file") — just read it
- When Gordon clearly already knows the context and is asking a specific question

---

## Inputs

Identify the **subject** — who or what Gordon wants briefed on:

1. **Person** — a name (client contact, partner, friend, family, professional contact)
2. **Company/Client** — a business name
3. **Topic** — a subject area, project, or initiative

If ambiguous, ask: *"Brief you on [person] the individual, or [company] the client?"*

---

## The Search — Exhaustive, Then Curated

### Layer 1: GordonOS Knowledge Base (always run all of these)

Search in this order. Each source gets checked regardless of whether earlier sources found hits:

| Source | What to search | How |
|--------|---------------|-----|
| **People files** | `relationships/people/*.md` | Glob for name match, then read matching files |
| **Client files** | `work/clients/*.md` | Glob for name/company match, then read |
| **Partner files** | `work/partners/*.md` | Glob for name match, then read |
| **Leah file** | `relationships/leah.md` | If subject is Leah or involves her |
| **Memory DB** | `python3 tools/memory-db.py search "<subject>"` | Always — catches cross-references |
| **Action items** | `personal/action-items.md` | Grep for name/topic — open commitments involving them |
| **Open questions** | `personal/open-questions.md` | Grep for name/topic — unresolved threads |
| **Earballs transcripts** | `data/earballs-transcripts/` | Grep recent transcripts (last 30 days first, then broader if thin) for mentions |
| **Session state** | `comms/session-state.md` | Recent context involving them |
| **Ticklers** | `tickler/` | Upcoming reminders involving them |
| **Work dashboard** | `work/dashboard.md` | If client/business related |

**Search strategy:** Start with exact name match, then try partial matches, nicknames, and company associations. If searching for a person, also search for their company. If searching for a company, also search for key contacts.

### Layer 2: Fresh Internet Search (when appropriate)

Run a web search when:
- The subject is a person Gordon is meeting with (especially if new or infrequent contact)
- The subject is a company (check for recent news, updates, leadership changes)
- The knowledge base results are thin or stale (>30 days since last update)
- Gordon explicitly asks for fresh context

**What to search for:**
- Person: name + company, LinkedIn profile, recent news/mentions, professional background
- Company: recent news, leadership changes, company updates, industry context
- Topic: recent developments, relevant articles, expert perspectives

**What NOT to do:**
- Don't search for people Gordon knows intimately (Leah, close family) — that's creepy, not helpful
- Don't search for GordonOS-internal topics — the KB is the source of truth for those
- Don't spend more than 30 seconds on web search — this is supplemental, not primary

---

## The Briefing — Output Format

Structure depends on subject type:

### Person Briefing

```
## [Name] — Brief

**Who:** [Role/title, company, relationship to Gordon — one line]
**Last interaction:** [Date and context, from transcripts/session-state/action-items]
**Relationship temperature:** [Warm/neutral/cold/new — based on frequency and recency of contact]

### What We Know
[Key facts from KB: personal details, family, interests, professional background, history with Gordon. Organized by relevance, not source.]

### Open Threads
[Active items involving this person: action items, open questions, pending commitments — from either side]

### Recent Context
[Anything from the last 30 days: transcript mentions, email threads, meeting notes, signals]

### Fresh Intel
[Web search results if run: recent news, company updates, LinkedIn changes, anything notable]

### Conversation Prep
1. **Non-work openers:** [2-3 personal topics Gordon could bring up — kids, hobbies, recent trips, shared interests]
2. **Questions to ask them:** [2-3 thoughtful questions based on what we know about their life/work]
3. **What Gordon owes them:** [Any commitments or follow-ups Gordon has pending]
4. **What they owe Gordon:** [Any commitments or deliverables expected from them]
```

### Company/Client Briefing

```
## [Company] — Brief

**What:** [Industry, size, relationship to Gordon — one line]
**Key contacts:** [Names and roles of people Gordon interacts with]
**Status:** [Active client / prospect / past client / partner — from dashboard/client file]

### Current State
[Where things stand: active projects, recent work, billing status, health of relationship]

### Open Threads
[Action items, pending deliverables, open questions — both directions]

### Recent Activity
[Last 30 days: meetings, calls, emails, transcript mentions]

### Fresh Intel
[Web search results if run: company news, market changes, competitor moves]

### Key Context
[Anything Gordon should keep in mind: sensitivities, preferences, political dynamics, history of issues]
```

### Topic Briefing

```
## [Topic] — Brief

**What this is:** [One-line definition/context]
**Why it matters to Gordon:** [Relevance — which project/client/goal does this connect to]

### What We Know
[Everything from KB, organized by relevance]

### Open Threads
[Action items, open questions, pending decisions]

### Fresh Intel
[Web search results if run]

### Key Connections
[How this topic connects to other things Gordon is working on — associative links]
```

---

## Presentation Rules

- **Lead with what matters most.** If there's an open commitment or time-sensitive item, that goes first — before the biographical background.
- **Flag stale information.** If the most recent data is >30 days old, say so: *"Last context we have is from [date] — may want to check in."*
- **Don't dump raw file contents.** Synthesize across sources. Gordon doesn't need to know which file something came from — he needs the picture.
- **Keep it scannable.** Headers, bullets, short sentences. Gordon should be able to absorb this in 60-90 seconds.
- **Be honest about gaps.** "We don't have anything on [X]" is more useful than padding with filler.
- **Proportional depth.** A quick "who is this person?" gets 3-4 lines. Pre-meeting prep gets the full template. Match depth to context.

---

## After the Briefing

- If the briefing surfaced stale or missing information, note it: *"Their people file hasn't been updated since [date] — want me to update it after your meeting?"*
- If Gordon is about to meet with them, suggest the `punnett-square` skill: *"Want to run the Punnett Square for this meeting?"*
- If the briefing revealed open commitments Gordon forgot about, surface them clearly — this is exactly the kind of thing that builds trust when handled well.

---

## What This Replaces

- Ad-hoc "let me check the people file" lookups — now systematized
- The "I should have known that" moments — everything is checked, every time
- Morning-startup's Step 14 (meeting prep briefings) can invoke this skill for each attendee rather than doing its own lighter version
