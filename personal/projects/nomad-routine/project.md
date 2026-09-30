---
name: Nomad daily check
type: project
lobe: personal
area: nomad
status: active
recurring:
goal:
wrike_project:
next_action: {text: "Design the personal morning routine incl. the nomad check (build order #5)", set: 2026-09-30}
waiting: []
job:
description: Nomad daily check; captured 2026-09-21, components added 2026-09-30
sources: ["[gordon 2026-09-21]", "[gordon 2026-09-30]"]
---
# Nomad daily check
**Big picture.** Gordon lives in his RV full-time. Years ago he found a map on Imgur: a 9,000-mile, 12-month road trip through North America that chases an average of 70°F. He is not doing that exact trip; he's taking the concept and overlaying it with **where his favorite and most important people are**, so he keeps his social exposure during a solo adventure. That social contact is very important to his mental well-being. This routine is as much about people as weather.

**What he wants every morning.** He says "good morning, Sancho" and gets:
1. **Weather** for the next couple of days where he is.
2. **How far and in what direction to drive** to stay in his ideal temperature range.
3. **Cross-reference against his people-and-places list** (people he wants to see, places he wants to visit), so the direction of travel is chosen with visits in mind, not just temperature.
4. A verdict: **drive today, drive in the next couple of days, or stay**, to keep the adventure going and comfortable.

**Temperature range (confirmed):** overnight low no warmer than ~60°F, daytime high no hotter than ~85°F. Routing chases cooler, not warmer.

**Additional components (decided 2026-09-30, from Claude's prompts; Gordon kept all but mail forwarding; "sounds like too much, but they're all useful; road-test and tweak"):**
5. Wind and severe-weather warnings for the drive itself (distinct from comfort temperatures; an RV in crosswind is a driving decision).
6. Freezing nights, for the plumbing: a separate threshold from the 60/85 comfort range.
7. Drive time, fuel, and range for the day's candidate leg.
8. Connectivity at the destination: cell coverage and Starlink line-of-sight.
9. Campground or hookup availability and reservations at the destination.
10. Propane, water, and tank levels as a "can I stay put another day" input (entered by hand for now; sensor integration is an ICE item if it ever matters).
11. Time-zone change on the candidate leg (feeds the temporal check and the calendar).
12. Fixed points from the calendar: Leah's Monday and Thursday meetings, anything else that pins a location or a connection window.
13. Anything happening at the destination worth arriving for (events, people passing through).
Dropped: mail and package forwarding (Gordon's call).

**Road-test rule:** the first version reports all of these in one short paragraph after the weather and direction; after two weeks of use, anything Gordon never acts on is cut. The output stays under ten lines regardless; if it can't, the routine is doing too much.

**Skill inputs implied:** a weather source with wind and overnight lows; a routing source for time/fuel; a coverage source (or a manual note); a campground source (or manual); tank levels by hand; the calendar; `personal/nomad/location.md`; the people-and-places list. Which of these need a Mac-side command with a key (weather, routing) and which are manual for v1 is a Phase 3 decision.

**Inputs (first sketch).** Current location (how does Sancho know? phone location, a manual "I'm in X," or the RV's own GPS); weather forecast source (needs an API or web lookup); the people-and-places list (lives in the personal lobe, references `people/` in the spine, with locations and "want to see by" dates); the calendar (commitments that fix location on given days); Gordon's driving tolerance per day (max hours/miles).

**Outputs.** One short morning brief: where you are, the next 2–3 days' highs and lows, the nearest direction/distance that gets back into range, who's within reach along that direction, and the verdict. Written to disk as a dated log entry so the trip has a record.

**Done and habitual looks like:** he says good morning, reads five lines, and knows whether today is a driving day. He never has to open a weather app or think about the map.

**Notes for Phase 2.**
- Wake phrase (decided 2026-09-22): "Hey Sancho" opens the personal lobe by default; "Hey Sancho, let's work" opens the work lobe. Any Sancho greeting counts. See decisions.md.
- This is the personal morning routine's core, or a skill it calls. It shouldn't be a separate ritual on top of a ritual (Q2 failure).
- Weather and geocoding need a script with a real data source, not an MD instruction. Which source, and whether it works from a Cowork session, is a Phase 2 question.
- The people-and-places list is a first concrete consumer of the spine's `people/` design (decision #8): people need a `location` field and a "last seen / want to see" field.

---
