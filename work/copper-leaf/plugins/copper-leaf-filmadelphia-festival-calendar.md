---
name: "Copper Leaf Creative: Filmadelphia Festival Calendar"
type: doc
business: copper-leaf
lobe: work
status: active
description: Festival schedule page (day x time across five theater lanes) for Philadelphia Film Society, filmadelphia.org; v1.0.0
sources: ["[doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/copper-leaf-filmadelphia-festival-calendar.php]", "[doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt]", "[doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md]"]
---
# Copper Leaf Creative: Filmadelphia Festival Calendar

Registry entry built 2026-10-02 (batch B4) from the kit clone at `~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/`. Read-only; the plugin's own files win where this page and they disagree.

## What it does
- Draws the festival schedule as a two-dimensional grid, day by time across five fixed theaters; desktop gets a horizontal "Marquee Grid" timeline, mobile gets the "Timeline Hybrid" view [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/copper-leaf-filmadelphia-festival-calendar.php:4-5]
- Desktop features: films placed at true start time, a NOW marker, hover cards with synopsis and Tickets link, strand filter and an "At a glance" overview; the opening state is server-rendered and a +/- 7 day JSON payload makes navigation instant [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:29-37]
- Days outside the payload load through the REST route `/wp-json/pfs/v1/showtimes`; a diagnostics page sits at Tools > Festival Calendar [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:38-39]
- Delivered as a page template ("Festival Calendar (Matrix)", slug `cffc-festival-calendar`), not a block, because the theme renders pages from ACF Flexible Content and never prints post_content; the plugin is dormant until a page uses that template [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:14-17]
- Strands (colour-coded programme categories) are editable per calendar page in a "Strands" table, pre-filled with seven built-ins [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:12]

## Where it runs
- Client: Philadelphia Film Society (filmadelphia.org); contact named in the plugin file: Christian Layfield [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:8]
- Production: went live on filmadelphia.org with the September 2026 site launch [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:5]
- Staging: SSH alias `copperleaf-dev` (host-5), site folder `filmadelphia-dev` under `~/sites`, WordPress root `www/` [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:21-23]
- Unreconciled: the kit handoff lists `filmadelphia-dev` among the SSH aliases as well as `copperleaf-dev`; the plugin file names `filmadelphia-dev` only as the folder [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:63]
- Staging demo page ID 57312; browser testing runs through Gordon's real Chrome because the host's bot filter blocks the in-app browser [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:29-30]

## Version and history
- Current version: 1.0.0, released 2026-09-21; header and newest tag `v1.0.0` agree [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/copper-leaf-filmadelphia-festival-calendar.php:6] [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:4] [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/.git (git tag, read 2026-10-02)]
- Arc 1: 0.1.0 built from the Claude Design "PFS Showtimes Redesign" handoff of 2026-08-18, staging only [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:24-27]
- Arc 2: 0.1.2 and 0.1.3 (2026-08-25, 2026-09-03) fixed the NOW marker timezone and the overview closing; 0.2.0 (2026-09-21) made strands editable and swapped the second Bourse lane to BOURSE 2 (venue 1547) at the client's request [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:11-22]
- Arc 3: 1.0.0 (2026-09-21) is the first production release; versions 0.1.0 to 0.2.0 only ever ran on staging [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:4-9]

## Rules specific to this plugin
- Prefix `cffc_` for functions, hooks, fields and handles; classes `Filmadelphia_Festival_*` [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:9]
- Version lives in the `Version:` header AND the `FILMADELPHIA_FESTIVAL_CALENDAR_VERSION` constant (it busts the CSS/JS cache; bump on every asset change) [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:10-12]
- Branch is `main`, not `master` [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:13]
- PHP floor: not stated in the plugin file, so the kit's 7.4 floor applies [doc:~/Dev/clc-plugins/CLAUDE.md:63]
- Staging shell PHP is 7.3, so WP-CLI cannot load WordPress over SSH; `wp eval-file` runs only in the hosting panel's web terminal, which Gordon drives [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:24-26]
- Lint each changed file with `php -l` over stdin BEFORE copying it to staging [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:27-28]
- `dev/` is staging-only tooling; never deploy it to production (`--exclude dev`) [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:31]
- A fresh clone's first parity dry run lists the main file and the ACF JSON because staging holds CRLF bytes; line endings only, confirm with a diff [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:32-35]
- Never invent content: no fallback runtime, label or strand is displayed as if real [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:39-40]
- Lanes match on the per-screen Agile `venue_id`, not the theater name; mapping 1544 Mainstage, 1545 Greenfield, 1546-1550 Bourse 1-5, 1551-1552 East 1-2 [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:41-45]
- The calendar must be scoped to a festival term (`movie-category` holds about 190 terms) [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:50-51]
- Do not modify `pfs-data-import` or `copper-leaf-filmadelphia-calendar-view` [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:57]

## Dependencies
- ACF: the settings field group loads from the plugin's own `/acf` folder [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/copper-leaf-filmadelphia-festival-calendar.php:93-96]
- Timber/Twig: the plugin tells Timber where its Twig templates live [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/copper-leaf-filmadelphia-festival-calendar.php:169]
- Copper Leaf Updates Handler for automatic updates (admin notice if missing) [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/copper-leaf-filmadelphia-festival-calendar.php:56-83]
- Reads existing data only: showtimes, movies and theaters post types fed by `pfs-data-import`; no options, meta keys, tables or cron hooks of its own [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:41-43]
- Theme: Philly Film (`phillyfilm`), which renders pages from ACF Flexible Content [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:15-16] [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:1]

## Open threads
- `festival-schedule.class.php` does not prime meta, so each screening queries on its own; one `update_meta_cache()` call would batch it, "worth doing before a real festival page goes live" [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:61-63]
- `includes/diagnostics.php` lists the default strands, not a page's edited ones [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:64-65]
- Recolouring and removing a strand row were not UI-tested [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:66-67]
- After the first real festival import, check Tools > Festival Calendar for screenings in the unmatched bucket [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:47-49]
- From the 0.1.0 pre-live list, not marked closed in later notes: strand colours were approximations needing client confirmation, and fonts are Google stand-ins pending licensed brand faces [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:54-58]
