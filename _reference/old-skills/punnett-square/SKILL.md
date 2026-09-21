---
name: punnett-square
description: |
  Pre-Meeting Punnett Square for GordonOS. Use before any non-recurring meeting, especially with new people or clients. Also invoke when Gordon says "prep me for the meeting," "what should I think about before [meeting]," "Punnett Square," or "meeting prep." Runs the brief-me skill for all attendees, then presents the 4-quadrant outcomes framework: YOUR best/worst outcome, THEIR best/worst outcome. Exists because mushrooms removed Gordon's automatic empathy trigger — this rebuilds perspective-taking as an intentional, structured practice. The morning-startup skill suggests this automatically for upcoming non-recurring meetings.
---

# Pre-Meeting Punnett Square

Gordon used to walk into every room already sensing what everyone else was feeling and wanting. That radar was automatic — driven by anxiety and fawn response. Mushrooms resolved the anxiety (good), but the automatic empathy trigger went with it (gap). This skill rebuilds that awareness intentionally, through structure instead of instinct.

The name comes from biology's Punnett Square — a 2x2 grid of possible outcomes. Here: YOUR outcomes x THEIR outcomes.

---

## When This Triggers

- **Automatic (via morning-startup):** When Step 14 detects a non-recurring meeting on today's calendar with named attendees, morning-startup suggests: *"You've got [meeting] at [time] — want to run the Punnett Square?"*
- **Automatic (via work-closeout):** When Step 3 (Tomorrow Preview) spots a meeting needing prep, it can suggest running this for tomorrow's meetings tonight.
- **On demand:** Gordon says "prep me for the meeting," "Punnett Square," "what should I think about before [meeting]," "meeting prep," or any variation.
- **Suggested by brief-me:** After a person briefing, brief-me suggests this if Gordon is about to meet with them.

**Do NOT trigger on:**
- Recurring internal meetings where the format is known (e.g., weekly standup) — unless Gordon asks
- Social events where "outcomes" framing would be weird — use brief-me alone for those
- Meetings already in progress

---

## Step 1: Identify the Meeting

Determine which meeting to prep for:
- If Gordon names it, use that
- If invoked from morning-startup, the meeting is already identified
- If ambiguous (multiple upcoming meetings), ask: *"Which one — [meeting A] at [time] or [meeting B] at [time]?"*

Pull meeting details from calendar:
- Time, duration, location/link
- Attendees (names and emails)
- Agenda or description (if any)
- Is this a first meeting or recurring? (Recurring meetings get lighter prep)

---

## Step 2: Brief All Attendees

Invoke the `brief-me` skill for each named attendee (excluding Gordon). Run these in parallel where possible — each attendee gets their own full briefing.

If there are more than 4 attendees, brief the top 4 (by importance/relevance to Gordon) in full and list the rest with one-line summaries.

**For first-time meetings with someone new:** Always run a web search as part of the briefing. Gordon should never walk in blind.

---

## Step 3: The Punnett Square

After the briefings, present the 4-quadrant framework. This is the core of the skill — the part that rebuilds perspective-taking.

```
## Punnett Square: [Meeting Name]

### YOUR Outcomes (Gordon)
**Best case:** What's the ideal outcome for you from this meeting?
[Draft based on context — open items, goals, what's at stake. Ask Gordon to confirm or adjust.]

**Worst case:** What would make this meeting a failure for you?
[Draft based on context — what could go wrong, what you're trying to avoid.]

### THEIR Outcomes ([Other party name(s)])
**Best case:** What do THEY want out of this meeting?
[Draft based on briefing — their goals, their pressures, what they've been asking for.]

**Worst case:** What are THEY afraid of or trying to avoid?
[Draft based on briefing — their risks, their constraints, what would be bad news for them.]

### The Overlap
**Win-win zone:** Where do your best cases align?
[Identify shared goals or compatible outcomes]

**Tension zone:** Where do your interests diverge?
[Identify conflicts — where your best case is their worst case, or vice versa]

### Walking-In Posture
Based on this grid, here's what to keep in mind:
- [One line on what to lead with]
- [One line on what to listen for]
- [One line on what to avoid]
```

---

## How to Fill the Grid

**Gordon's quadrants:** Draft from context — active projects, open commitments, what he's told you he wants from this relationship. Then ASK Gordon: *"Here's what I think your best/worst case is — does that match, or is there something else driving this?"*

**Their quadrants:** This is the empathy-rebuild piece. Draft from:
- Their briefing (what they've been saying, what they've been asking for)
- Their business context (pressures, deadlines, constraints from web search)
- Their relationship history with Gordon (past friction, past wins)
- Role/position empathy — what does someone in their role typically care about?

If we don't have enough to draft their quadrants meaningfully, say so: *"I don't have enough context on what [person] is optimizing for — what's your read?"*

**The overlap analysis** is where the real value lives. It turns the meeting from "what do I want to say" into "where can we both win, and where should I be careful."

---

## Presentation Rules

- **Don't make this clinical.** The Punnett Square is a thinking tool, not a corporate framework. Keep the language conversational. Gordon should feel like he's being prepped by a sharp chief of staff, not filling out a form.
- **Draft first, then ask.** Don't interrogate Gordon with 8 questions before showing anything. Draft all four quadrants from what you know, present them, THEN ask Gordon to confirm/adjust. This is faster and shows Gordon what you're working with.
- **Flag the empathy gap explicitly.** If "their" quadrants are thin because we don't know enough, name it: *"The their-side is thin — going in, your main job is to listen for what they actually want."* This IS the skill working — making the gap visible is the point.
- **Keep it under 2 minutes to absorb.** Gordon should be able to read this in the car on the way to the meeting. If it's too long, cut.
- **Don't overload with briefing detail.** The brief-me output supports this skill but doesn't need to be re-presented in full. Reference it: *"From the briefing: [key point]."*

---

## After the Meeting

This skill doesn't have a post-meeting component (that's for a future "debrief" skill). But if Gordon debriefs naturally after a meeting:
- Capture outcomes vs. the Punnett Square predictions
- Update people files with new information
- File action items from the meeting
- Note whether the empathy read was accurate — this data improves future briefings

---

## Integration Points

| Skill | How it connects |
|-------|----------------|
| **brief-me** | Called by this skill for each attendee. Can also suggest this skill after a person briefing. |
| **morning-startup** | Step 14 (meeting prep) suggests this for non-recurring meetings with named attendees. |
| **work-closeout** | Step 3 (tomorrow preview) can suggest this for tomorrow's meetings. |
| **think-first** | The Punnett Square IS a thinking framework. Think-first can reference it for meeting-related decisions. |
| **critical-thinking** | WHO dimension naturally feeds into this. Deep dive can invoke this as a focused exercise. |

---

## Context: Why This Exists

From Gordon (T058, rec_25e26ed422, 2026-03-14): The automatic empathy trigger that used to fire before every interaction — reading the room, sensing what people need, anticipating reactions — was driven by anxiety and fawn response. Mushrooms resolved the underlying anxiety, which was the right call. But the empathy radar went dark too. This skill rebuilds that awareness through structure: *"I can't feel what they're feeling automatically anymore, so I need to think about it deliberately."* The Punnett Square is the deliberate version of what used to be instinct.
