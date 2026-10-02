---
name: personal-morning
type: skill
lobe: personal
shared:
description: The personal morning routine, offered once by the open skill and run on Gordon's yes: the nomad daily check (weather where he is, severe-weather and freeze warnings, which direction and how far to drive to stay inside 60/85, who is within reach that way, the verdict), today's calendar, the daily focus checksum, the food line, one mantra. Under ten lines, then written to the trip log.
why: Routine 2 from the Phase 0 captures: "say good morning Sancho and know whether today is a driving day." Weather and routing must come from a script with real data, not an MD instruction; the people overlay is the point, not a nicety (mental well-being) [rec_0c571abb1d 2026-09-22].
triggers: ["run the morning routine", "good morning Sancho" after the open skill's offer is accepted, "nomad check", "should I drive today", "what's the weather looking like"]
must_not_trigger: [the work lobe's morning (separate skill), a second run on the same day unless Gordon asks again, any afternoon open (the offer is before noon only), a plain weather question for somewhere he is not]
reads: [personal/nomad/location.md, personal/nomad/thresholds.md, "personal/nomad/brief-<date>.md (written by the nomad.brief command)", personal/nomad/people-and-places.md, "people/*.md location and want_to_see_by fields (via the generated people/_geo.json)", FOCUS.md, personal/PROJECTS.md, "personal/food/plan-<week>.md if it exists", personal/me/mantras.md, _queue/mantras-shown.md, "today's calendar through the Google Calendar connector"]
writes: ["_queue/requests/ (nomad.brief)", "personal/nomad/log/<date>.md (the day's brief and verdict)", "_queue/routines/personal-morning-<date>.md (ran, or declined)", "FOCUS.md today line when Gordon sets today's three", _queue/mantras-shown.md, "personal/nomad/location.md when Gordon says where he is"]
chain: {front: "open (offer accepted)", next: "food-routine on Sunday; weekly-review on Friday or Tuesday mini", gate: none}
test: _setup/tests/skills/personal-morning/
---
# personal-morning

One exchange, ten lines, then the day. Facts come from the brief file the Mac wrote, the calendar, and the generated focus files; nothing is composed from memory. If the brief is missing or stale, say so in one clause and give what the rest can give.

## Procedure

1. **Where.** Read `personal/nomad/location.md`. Before the nomad season starts (its date is in that file) give the weather where he is and skip the drive verdict and the candidates. If `city` is unknown or older than three days, ask first, in one line ("Where are you this morning?"), write the answer with `[gordon <date>]`, and continue. Never infer the city from the Mac's clock or the last known place.

2. **The brief.** Request the `nomad.brief` command (args: the location file's city, or lat/lon if present) and wait up to 60 s for `personal/nomad/brief-<date>.md`. The command (Mac-side, keyless in v1) writes: the next three days' highs and lows and wind where he is; active severe-weather alerts; freeze risk tonight and tomorrow night; a ring of sample points at 50, 100, 150 and 200 miles in eight directions with each point's forecast highs and lows, so the nearest in-range direction is computed, not guessed; an estimated drive time per candidate (distance over 50 mph, v1); timezone at the location and at each candidate; the people from `people/_geo.json` within 200 miles of the location and within 100 miles of each candidate, with `want_to_see_by`. If the brief is older than today or the command fails, say "no fresh weather this morning" and skip the verdict.

3. **Thresholds.** `personal/nomad/thresholds.md`: overnight low at most 60, daytime high at most 85 [rec_0c571abb1d 2026-09-22]; freeze line 32 for the plumbing; wind line for driving (Gordon sets it; until then 30 mph sustained is flagged, never decided). Routing chases cooler, not warmer.

4. **The verdict.** From the brief: inside range for the next two days → **stay**; outside range in two days with an in-range candidate → **drive in the next couple of days**, direction and miles; outside range tomorrow → **drive today**. Severe-weather warnings on the candidate leg override to "wait" with the reason; wind never overrides, it is an advisory (alerts, gusts, crosswind, calmest window; `thresholds.md` Plan A) [gordon 2026-10-02]. Freeze tonight is said regardless of the verdict.

5. **People within reach.** From the brief: anyone within reach of the chosen direction, with their `want_to_see_by` if set, and anything in `people-and-places.md` on that heading. One clause each; the list is the point of the direction, so it is never dropped for length.

6. **Calendar.** Today and tomorrow through the Google Calendar connector (read only): fixed points that pin a place or a connection window (Leah's Monday and Thursday meetings, anything with a location). One clause.

7. **Focus checksum.** From `FOCUS.md` and `personal/PROJECTS.md`: this month's three, this week's three, and the question "what are today's three?" Gordon's answer is written to the `today` line of `FOCUS.md` with the date; if he skips it, yesterday's rolls forward and the line says so.

8. **Food line.** If `personal/food/plan-<week>.md` exists: today's options from it and the midday nudge, one line. If not, nothing (the food routine is its own skill; this is not where it gets built).

9. **Mantra.** One, chosen by tag against today's focus items and the open topic, least recently shown, never the same within 14 days (`_queue/mantras-shown.md` holds the state). Last line.

10. **Say it.** Ten lines at most, spoken, no field names: place and date; weather now and the next two days; the verdict with direction and distance, or "no fresh weather"; warnings if any; who is within reach that way; calendar pins; the focus question (or today's three if already set); the food line; the mantra. If it cannot fit in ten lines the routine is doing too much [project nomad-routine, road-test rule].

11. **Write and receipt.** `personal/nomad/log/<date>.md`: the brief's summary, the verdict, who was in reach, what Gordon decided if he said; `_queue/routines/personal-morning-<date>.md` with `ran: <time>`; `FOCUS.md` today line; mantras-shown. Receipt: one line, paths only, only when Gordon asks what was written (the routine's output is the greeting; a receipt every morning is noise).

## Rules
- The city is never inferred; unknown is said.
- The verdict is computed from sample-point forecasts, never from a general sense of the region.
- Ten lines. Components Gordon never acts on are cut after two weeks (road-test rule, project file).
- Manual in v1, said as such when relevant: campground availability, connectivity at the destination, tank and propane levels. They enter the brief only if Gordon states them that morning.
- Offered once by `open`, nudged once, never a third time that day.

## Write step
Files written: the trip log entry, the routine state file, `FOCUS.md` today line, `_queue/mantras-shown.md`, `location.md` when he says where he is. Receipt: one line, paths only, on request.
