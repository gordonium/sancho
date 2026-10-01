---
name: Philly Film
type: doc
business: copper-leaf
lobe: work
status: active
description: Theme (Timber/Tailwind, not a plugin) for Philadelphia Film Society, filmadelphia.org; GitHub auto-updates; v2.0.0
sources: ["[doc:~/Dev/clc-plugins/phillyfilm/style.css]", "[doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt]", "[doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md]", "[doc:~/Dev/clc-plugins/phillyfilm/functions.php]"]
---
# Philly Film (theme `phillyfilm`)

Registry entry built 2026-10-02 (batch B4) from the kit clone at `~/Dev/clc-plugins/phillyfilm/`. This is a THEME; its header lives in `style.css`, not a main PHP file. Read-only.

## What it does
- WordPress theme "Philly Film", the "Imparter" vendor theme with Tailwind, originally authored by Impart [doc:~/Dev/clc-plugins/phillyfilm/style.css:2-6]
- Timber/Twig theme; pages render from ACF Flexible Content layouts [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:9] [doc:~/Dev/clc-plugins/phillyfilm/functions.php:150]
- Templates for showtimes, now showing, festival showtimes, movies, theaters, movie categories, news and contact [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:36-41] [doc:~/Dev/clc-plugins/phillyfilm/template-festival-showtimes.php]
- Since 2.0.0 it updates itself from GitHub Releases through the Copper Leaf Updates Handler, like the Copper Leaf plugins [doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt:5] [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:10-13]
- 2.0.0 added phone and tablet site search in the slide-out menu and one shared showtime-tag badge used on every showtime listing [doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt:6-7]

## Where it runs
- Client: Philadelphia Film Society; contact Christian Layfield; site filmadelphia.org [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:1] [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:8]
- Staging: SSH alias `copperleaf-dev` (host-5), staging folder `filmadelphia-dev` under `~/sites`, WordPress root `www/` [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:48-49]
- The first 2.0.0 install on live was a manual zip upload [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:13]

## Version and history
- Current version: 2.0.0, released 2026-09-22; tag `v2.0.0` [doc:~/Dev/clc-plugins/phillyfilm/style.css:6] [doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt:4] [doc:~/Dev/clc-plugins/phillyfilm/.git (git tag, read 2026-10-02)]
- Arc 1: versions before 2.0.0 belonged to the original vendor build and were never released through Copper Leaf's mechanism; baseline of the pre-launch theme on live in August 2026 is commit `203664b` [doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt:8] [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:14-15]
- Arc 2: the September 2026 relaunch work (site improvements, client review rounds, launch tooling) [doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt:8]
- Arc 3: 2.0.0 (2026-09-22) is the first version delivered through automatic updates; no data migration [doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt:4-9]

## Rules specific to this plugin
- Prefix for new functions `phillyfilm_`; text domain `imparter_theme` [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:9] [doc:~/Dev/clc-plugins/phillyfilm/style.css:9]
- Version lives ONLY in `style.css`; branch `master` [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:10] [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:14]
- PHP floor: not stated; the kit's 7.4 floor applies [doc:~/Dev/clc-plugins/CLAUDE.md:63]
- Exception to the kit: `.gitattributes` deliberately DISABLES line-ending conversion (approved by Gordon 2026-09-21); do not add `eol=lf`; preserve each file's line endings [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:16-18] [doc:~/Dev/clc-plugins/CLAUDE.md:129]
- Build: Laravel Mix 6 / Tailwind 3, load nvm first, build from a copy outside the Sync folder, verify `dist/` changed before committing; `dist/` is committed and ships [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:19-21]
- Timber autoescape is OFF: escape at the print site with `|esc_attr` / `|esc_html`, never `|e` [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:25-29]
- Editor colours go through `sanitize_hex_color` before any `style` attribute [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:30-31]
- Showtime buttons are drawn in four places; badge markup lives once in `partials/showtime-tag-badges.twig`; desktop header and mobile menu are separate markup, so header features go in both [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:36-44]
- Staging: lint PHP over stdin before copying; deploy with `rsync --relative`; WP-CLI cannot load WordPress over SSH (shell PHP 7.3); server-local `curl` with a Chrome user agent is the reliable rendered-HTML check [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:49-56]

## Dependencies
- Timber (Composer `vendor/autoload.php`; notice if not active) [doc:~/Dev/clc-plugins/phillyfilm/functions.php:4-17]
- ACF and ACF Extended (`includes/acf.php`, `includes/acfe.php`) [doc:~/Dev/clc-plugins/phillyfilm/functions.php:128-131]
- Gravity Forms and Yoast integrations [doc:~/Dev/clc-plugins/phillyfilm/functions.php:139-140]
- Copper Leaf Updates Handler for automatic updates [doc:~/Dev/clc-plugins/phillyfilm/functions.php:44-50] [doc:~/Dev/clc-plugins/phillyfilm/functions.php:85]
- Works alongside the Filmadelphia Festival Calendar plugin, which supplies the "Festival Calendar (Matrix)" page template [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:14-16]

## Open threads
- `theater` meta printed unescaped in about ten older templates [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:63-64]
- Raw term names in text nodes in three templates (safe today because `<>` are encoded on save) [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:65-66]
- `festival-showtimes.twig` calls `movie.meta('showtimes')` repeatedly and renders the loop twice; dominant cost on festival pages [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:67-68]
- `backfill-country.php`: run detached, make resumable, defer term counting, handle banner lines [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:69-70]
- Delete `dev-tools/replay-dev-data.php` from live once launch is closed out; consider `export-ignore` for `dev-tools/` [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:57-59] [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:71]
