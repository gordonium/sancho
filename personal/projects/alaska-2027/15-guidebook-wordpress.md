---
name: Guidebook & WordPress — structure
type: doc
lobe: personal
description: Alaska 2027 planning: Guidebook & WordPress — structure
sources: ["[gordon 2026-09-25 planning session]"]
---
# Guidebook & WordPress — structure

Goal: a private site for friends with guidebook-quality day pages, a printable PDF
version, and a blog during the trip that sits next to the plan (planned vs. actual).

## Content model
**Pages:** Overview · Map · The Rig · Aurora Plan · Budget · Booking Calendar · Packing · About

**Custom post type `trip_day`**
| Field | Notes |
|---|---|
| `day_offset` | D+n for the front half |
| `fixed_date` | For the back half (Aug 3–23) |
| `leg` | Taxonomy: A–H, Hinge, Aurora, Cassiar, Washington, Home |
| `from`, `to`, `miles` | |
| `overnight` | → `place` |
| `overnight_alts` | → `place` (multiple) |
| `flags` | BOOK · FC · FLOAT · CALL-DARK · HEAT · FUEL-GAP · GROCERY · WATER |
| `fuel_note`, `water_note`, `grocery_note` | |
| `highlights` | The "do" list |
| `actual_miles`, `actual_overnight` | Filled in on the road |

**Custom post type `place`** — campgrounds, tours, points of interest:
type · reservable / window · hookups · price tier · lat/lng · website · notes

**Blog posts** — normal posts, each linked to a `trip_day`. Day pages show a
"From the road" section listing them.

## ★ One setting re-dates the whole book
Store the front half as D+n, plus a site option **`departure_date`**. Every front-half
page renders its real date from that. Change the date once and the site and the PDF
re-date themselves. The back half keeps its fixed dates.

## Templates
- **Day card:** header (D+n / date, leg, from → to, miles) · overnight box with
  alternates · flag chips · fuel / water / grocery strip · things to do · photo ·
  "From the road" posts
- **Leg page:** leg map + table of its days
- **Print view:** one `/print/` template that runs front matter → legs → days → appendices.
  **Paged.js** handles the book layout: page numbers, running headers, table of contents.
  Export with the browser's Save as PDF or headless Chrome.

## Map & live tracking
Leaflet with the route as GeoJSON. **Embed Garmin inReach MapShare** for live position
during the trip.

## Privacy
Site-wide login or password, noindex. Friends get accounts or a shared password.

## Images
Your own photos for the blog. Public-domain NPS / USFWS / USGS images for planning
pages, with credits. (Parks Canada and Yukon images are Crown copyright — ask or skip.)

## Build approach
A small custom plugin for the CPTs, taxonomy, fields, and print template (your
wheelhouse), or ACF if that's faster.

## Source of truth
Markdown in this repo stays canonical while the itinerary is still moving (through
~spring). Then: convert the route tables to a structured `data/days.yaml` and import it
via WP-CLI or the REST API. After import, WordPress is canonical.

## Needed from Gordon when it's time
- Site URL and hosting
- How I connect: SSH + WP-CLI, or a REST application password
- Theme preference
- Who gets access
