---
name: weekly-review
type: skill
lobe: both
shared:
description: The GTD hinge, one skill with two gears per lobe: a full review (work Monday, personal Friday) that empties the inboxes, walks every active project, sets the week's three and glances up at the month and the goals; and a five-minute mini (work Thursday, personal Tuesday) inside the morning offer that only checks today's three, stalled next actions and aging waiting-fors. Driven by generated lists, never by memory; offered on cadence, never auto-run.
why: v2 had three overlapping review skills that hard-coded names and contradicted each other on timing, and the reviews stopped happening. GTD without the weekly review is a filing system. Six touchpoints a week is the ceiling [architecture §17.2, decided 2026-09-26].
triggers: ["weekly review", "let's review", "mini review", the open skill's offer on a review day accepted, "what's stalled", "what am I waiting on"]
must_not_trigger: [a question about one project (read its file), the daily focus checksum (personal-morning), the monthly or quarterly ICE review (its own procedure), any day the cadence does not name unless Gordon asks]
reads: ["<lobe>/PROJECTS.md (generated: active projects, next action age, waiting column)", FOCUS.md, "<lobe>/INDEX.md", recordings/STATUS.md, "_queue/sessions/ (notes left open)", "<lobe>/ice/ (captures since last week)", "<lobe>/reviews/<last week>.md", "<lobe>/goals.md (full review only)", personal/me/watch.md, "the week's calendar through the Google Calendar connector"]
writes: ["<lobe>/reviews/YYYY-Www.md (the receipt: what changed, exception count)", "FOCUS.md week line (and month line when it changes)", "project.md next_action / waiting / status lines Gordon changes, cited", "_queue/routines/<lobe>-review-<date>.md (ran, or declined)", "the session note"]
chain: {front: "open (offer accepted on a review day)", next: "ice-review monthly on the first full review of a month; the lobe's morning routine", gate: none}
test: _setup/tests/skills/weekly-review/
---
# weekly-review

Two gears. The full review is twenty minutes, aimed at fifteen; the mini is five. Both are read from generated files and the calendar and end in a written receipt. Sancho walks, Gordon decides; Sancho never parks, closes or creates a project on its own, and never creates a task (those are his, in Wrike and Google Tasks).

## Cadence (decided 2026-09-26)

| lobe | full | mini |
|---|---|---|
| work | Monday (ahead of Leah's meetings) | Thursday |
| personal | Friday | Tuesday |

Food planning stays Sunday (food-routine). ICE quick review monthly, deep dive quarterly, hooked onto the first full review of the month or quarter. If the minis grow, they are cut before the full reviews are.

## Full review

1. **Inboxes, emptied or counted.** Recordings waiting (`recordings/STATUS.md`): how many, oldest; offer to ingest after the review, not during. ICE captures since last week: list by name only. Session notes left open in `_queue/sessions/`: name each, close or carry. Anything in the lobe's `_queue/inbox` pointers for Gordon.
2. **Every active project, one line each**, from `PROJECTS.md`: name, next action and its age, waiting-for and its age. For each, one question at most: still active? (park or close on his word; a parked project keeps its file and gets `status: dormant` with the date); has a next action under 7 days old? (if not, he names one and Sancho writes it); is a waiting-for past 14 days? (he says chase, drop, or wait; Sancho writes it). Projects with nothing wrong are read in a single breath, not one by one.
3. **Last week's focus and exceptions.** `<lobe>/reviews/<last week>.md`: what the three were, which happened, the exception count (times the day's three were skipped or overridden). Said once, without judgment; the count is for the trend.
4. **This week's three.** From the remaining active projects and the calendar: Sancho proposes three with each project's next action; Gordon sets them. Written to `FOCUS.md` week line with the date.
5. **Glance up (full review only).** Is the month's focus still right? Which goal in `<lobe>/goals.md` does this week touch, if any? One exchange; the month line changes only on his word. On the first full review of a month, hand off to the ICE quick review; of a quarter, to the deep dive and the H3/H4 files.
6. **Blind spots.** Anything in `watch.md` that the week shows (three projects added, none closed; a waiting-for on a person he avoids chasing): said once.
7. **Receipt.** `<lobe>/reviews/YYYY-Www.md`: what changed (projects parked or closed, next actions set, waiting-fors chased or dropped), the week's three, the exception count carried forward, inbox counts. Under thirty lines. `_queue/routines/<lobe>-review-<date>.md` with `ran:`.

## Mini review

Inside the morning offer, three things and out: today's three for the lobe and whether they still make sense given the calendar; next actions older than 7 days (name, one question each); waiting-fors older than 14 days (same). Writes only what he changes, and the routine state line. No receipt file; the full review picks up the trail.

## Rules
- Generated lists drive it; if `PROJECTS.md` is stale (older than the last commit touching a project file), say so and request `index.build` first.
- One question per project at most; silence for the healthy ones.
- Sancho proposes the three; Gordon sets them. Sancho never parks or closes a project unasked.
- No tasks created; next actions are written on the project file and Gordon mirrors them where he keeps tasks.
- Twenty minutes full, five mini; over that, the lists were not ready, which is Sancho's to fix before next time.
- Offered on the cadence by `open`, nudged once, never a third time that day.

## Write step
Files written: the review receipt, `FOCUS.md` week (and month) line, changed project lines, the routine state file, the session note. Receipt: the review file path, one line.
