---
name: Pending pipeline requests and moves from ingest
type: doc
lobe: both
description: Requests the earballs-ingest skill would write to _queue/requests/ and folder moves it would make, held here because the Sancho build thread owns _queue/ (2026-10-01) and client folders are being backfilled; the build thread or Gordon clears them
sources: ["[gordon 2026-10-01]"]
---
# Pending from ingest (held, not done)

| when | recording | what | why held |
|---|---|---|---|
| 2026-10-01 | rec_0b2f65c077 | pipeline.library (new human-confirmed rows: gordon, peter-nevland, karen-dodge, jeff-goff, tim-silva, kevin-skalure, dustin) | _queue/ owned by the build thread |
| 2026-10-01 | rec_0b2f65c077 | move folder → work/wizard-of-ads/clients/dm-heating/transcripts/ ; summary.md → clients/dm-heating/summaries/2026-09-10_rec_0b2f65c077.md ; then pipeline.status | client folder does not exist yet; Gordon: "don't create anything yet" |
| 2026-10-01 | rec_564c0541a8 | pipeline.library (gordon, peter-nevland rows) | _queue/ owned by the build thread |
| 2026-10-01 | rec_564c0541a8 | move folder + summary to the Ignite client folder once Gordon picks copper-leaf vs wizard-of-ads; then pipeline.status; people/isaac.md, people/nathan.md | home undecided; folders don't exist |
| 2026-10-01 | — | _setup/ERRORS.md entry: ingest chat stated "husband-and-wife owners" for D&M with no source (rec_0b2f65c077 speaker-ID message). Mechanism: the ingest skill's test should fail any speaker-ID message whose claim about a person lacks a timestamp cite or the word unconfirmed | _setup/ owned by the build thread |
| 2026-10-01 | rec_9c3c3bbece | pipeline.library (gordon, grayson-erhard rows); pipeline.status (moved to work/tipelodeon/transcripts/) | _queue/ owned by the build thread |
| 2026-10-01 | rec_640701d84d | pipeline.library (gordon, leah rows); pipeline.status (moved to recordings/2026/rec_640701d84d/) | _queue/ owned by the build thread |
| 2026-10-01 | rec_640701d84d | client lines ready in summary-work.md "Facts to file": Racquet Depot (Bruce's Parkinson's worse, why the payment terms are generous; Gordon: file under RD client notes), Jabas Labs (ACH), ChanceLight (hours) | Copper Leaf client folders don't exist yet (backfill thread) |
| 2026-10-01 | rec_640701d84d | pipeline flag: Plaud recorded_at for 9/22–9/24 recordings carries +02:00 while Gordon's calendar has him in Colorado until ~9/24 (wedding in Estes Park 9/22). Check the timezone source before any timestamp-derived fact | pipeline is the build thread's |
| 2026-10-01 | — | RULE from Gordon: gordon-os-v2 (and v3) is never read directly by a session; only a dispatched subagent reads it and returns cited extracts. Needs a skill (e.g. v2-extract) + a must-never line in CLAUDE.md | skills/ and CLAUDE.md belong to the build thread |
| 2026-10-01 | — | SKILL request from Gordon: person-backfill. When ingest meets a person with no people/ file (or a thin one), dispatch the v2-extract subagent for that person's v2/v3 files, return cited lines, Gordon confirms, then seed people/<slug>.md. First targets: leah, james-gilbert | skills/ belongs to the build thread |
| 2026-10-01 | rec_0b2f65c077 | create people/peter-nevland.md, karen-dodge.md, jeff-goff.md, tim-silva.md, kevin-skalure.md, dustin (surname unknown) from the template | same; facts to file listed in the recording's summary.md |

## written (this ingest thread; stands in for _queue/sessions/<id>.md, which the build thread owns)
- 2026-10-01 rec_0b2f65c077: recordings/inbox/rec_0b2f65c077/speakers.md · corrections.md · summary.md · transcript.md (description only) · recordings/lexicon.md · recordings/inbox/_pending-requests.md
- 2026-10-01 rec_564c0541a8: recordings/inbox/rec_564c0541a8/speakers.md · corrections.md · summary.md · transcript.md (description only) · recordings/lexicon.md · recordings/inbox/_pending-requests.md
- 2026-10-01 rec_9c3c3bbece: work/tipelodeon/transcripts/rec_9c3c3bbece/{speakers,corrections,transcript}.md · work/tipelodeon/summaries/2026-09-11_rec_9c3c3bbece.md · work/tipelodeon/business.md · people/grayson-erhard.md · recordings/inbox/_pending-requests.md
- 2026-10-01 rec_640701d84d: recordings/2026/rec_640701d84d/{speakers,corrections,summary-work,summary-personal,transcript}.md · people/leah.md · people/james-gilbert.md · people/peter-seirup.md · work/wizard-of-ads/business.md · personal/finances/joint-account.md · recordings/lexicon.md · recordings/inbox/_pending-requests.md
