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
| wind_sustained_mph | 30 | flagged on a driving leg; not a decision rule until Gordon sets one | [gordon 2026-09-30] (component 5); number is a placeholder, unconfirmed |
| drive_speed_est_mph | 50 | v1 drive-time estimate, distance over speed | [derived: v1 design 2026-10-01] |
| reach_people_miles | 200 | people within this distance of the location are "within reach" | [derived: v1 design 2026-10-01] |
| candidate_people_miles | 100 | people within this distance of a candidate stop are listed with the direction | [derived: v1 design 2026-10-01] |
| ring_miles | 50, 100, 150, 200 | sample distances in eight compass directions for the in-range search | [derived: v1 design 2026-10-01] |

Routing chases cooler, not warmer [rec_0c571abb1d 2026-09-22].
