---
name: Nomad thresholds
type: data
lobe: personal
description: The comfort, plumbing and driving thresholds the nomad daily check computes against; Gordon's numbers, cited; the routine never changes them
sources: ["[rec_0c571abb1d 2026-09-22]", "[gordon 2026-09-21]", "[gordon 2026-09-30]"]
---
# Nomad thresholds

| threshold | value | meaning | source |
|---|---|---|---|
| overnight_low_max_f | 60 | an overnight low above this is out of range | [rec_0c571abb1d 2026-09-22] |
| daytime_high_max_f | 85 | a daytime high above this is out of range | [rec_0c571abb1d 2026-09-22] |
| freeze_f | 32 | a night at or below this is a plumbing warning, separate from comfort | [gordon 2026-09-30] (component 6) |
| wind_sustained_mph | 30 | advisory only, never decides [gordon 2026-10-02: "keep wind speeds as an advisory and look for a better Plan A"]; Plan A below | [gordon 2026-10-02] |
| drive_speed_est_mph | 50 | v1 drive-time estimate, distance over speed | [derived: v1 design 2026-10-01] |
| reach_people_miles | 200 | people within this distance of the location are "within reach" | [derived: v1 design 2026-10-01] |
| candidate_people_miles | 100 | people within this distance of a candidate stop are listed with the direction | [derived: v1 design 2026-10-01] |
| ring_miles | 50, 100, 150, 200 | sample distances in eight compass directions for the in-range search | [derived: v1 design 2026-10-01] |

Routing chases cooler, not warmer [rec_0c571abb1d 2026-09-22].

## Wind: Plan A (2026-10-02)
Wind never sets the verdict; it is said as an advisory with the leg [gordon 2026-10-02]. Better signals than one fixed number, in order:
1. **Official alerts on the leg:** an NWS Wind Advisory, High Wind Warning or Blowing Dust warning on any point of the candidate leg is said first and by name (US only; elsewhere the national service where Open-Meteo or a keyless feed has it).
2. **Gusts, not just sustained:** the leg's forecast max gust (Open-Meteo `wind_gusts_10m_max`) beside the sustained figure.
3. **Crosswind, not just speed:** the wind's component across the direction of travel for the leg's heading, which is what moves a high-sided RV; a 30 mph tailwind is not a 30 mph crosswind.
4. **Time of day:** the hours of the forecast's lowest gusts on driving days ("calmest window 7 to 11am").
Gordon's experience on the road replaces these numbers as it comes in.
