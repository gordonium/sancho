---
name: "Copper Leaf: HDOnline"
type: doc
business: copper-leaf
lobe: work
status: active
description: HDOnline core: inspection appointments, contacts, properties and reports built from standard Notes; v1.7.5
sources: ["[doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php]", "[doc:~/Dev/clc-plugins/hdonline/release-notes.txt]"]
---
# Copper Leaf: HDOnline

Registry entry built 2026-10-02 (batch B4) from the kit clone at `~/Dev/clc-plugins/hdonline/`. No CLAUDE.md or README in the plugin; main file, `cpt.php` and release notes are the sources. Read-only.

## What it does
- "Report creation from a library of standard Notes" [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:4-5]
- Registers the data model: Notes, Contacts, Properties, Reports, Appointments and Invoices post types, with note sections/subsections, contact types and appointment types [doc:~/Dev/clc-plugins/hdonline/cpt.php:41-373]
- Inspector Dashboard, New Appointment and View Appointment are wp-admin pages since 1.7.0 / 1.7.1; the old front-end pages redirect there [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:33-38]
- New appointments are entered through a Gravity Forms form rendered in wp-admin; reports are compiled by an AJAX handler [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:8-12] [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:22]
- Exposes a base for a client layer: an empty `report.class.php` was created "so I can extend it in homedirections plugin" [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:55-56]

## Where it runs
- Extended for Home Directions, Inc. by "Copper Leaf: HDOnline for Home Directions" [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:4-5]
- Sancho's client folder: `work/copper-leaf/clients/home-directions/` ("builds and runs their report and letter-writing system") [doc:~/Sync/Sancho/work/copper-leaf/clients/home-directions/entity.md:2-10]
- No staging alias or production address is stated in the plugin's files [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:1-40]

## Version and history
- Current version: 1.7.5, released 2026-03-24; header and newest tag `v1.7.5` agree [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:6] [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:2] [doc:~/Dev/clc-plugins/hdonline/.git (git tag, read 2026-10-02)]
- Arc 1: 1.01 / 1.1 (2021-02-22) folded in "cowboy coded fixes from Live"; 1.1.0 / 1.2.0 (2022-02-22) renamed to the Copper Leaf convention and added automatic updates [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:87-103]
- Arc 2: 1.2 to 1.5 (2022 to 2024) update-checker plumbing, CPT code moved into `cpt.php`, and a report class base for the Home Directions layer [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:46-84]
- Arc 3: 1.6.0 to 1.7.5 (2026-02-26 to 2026-03-24) removed page passwords on reports and invoices, moved the dashboard into wp-admin, ran a bug audit (nonces, sanitising, CPT slug typo), and fixed Gravity Forms loading on the admin pages [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:2-43]

## Rules specific to this plugin
- No plugin CLAUDE.md, so the kit rules apply unchanged, PHP floor 7.4 [doc:~/Dev/clc-plugins/CLAUDE.md:63]
- Prefix as observed in code, not a stated rule: constants `CLC_HDONLINE_`, functions mostly `hdo_`, post types `hdo_` [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:35-36] [doc:~/Dev/clc-plugins/hdonline/cpt.php:41]
- Branch is `main` [doc:~/Dev/clc-plugins/hdonline/.git (git rev-parse, read 2026-10-02)]
- A `HDO_IS_LOCAL` constant switches the Gravity Forms form ID (5 local, 1 otherwise) [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:295] [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:812]

## Dependencies
- ACF with ACF Extended PHP autosync for field groups [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:70-89]
- Gravity Forms (`GFAPI`, `GFFormDisplay`; message if not active) [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:292-305] [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:814-815]
- Post types originally from Custom Post Type UI, now as PHP in `cpt.php` [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:47]
- Copper Leaf Updates Handler for automatic updates [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:41-63]

## Open threads
- No TODO is recorded in the release notes [doc:~/Dev/clc-plugins/hdonline/release-notes.txt]
- Relies on ACF Extended autosync; the Home Directions layer needed a fallback loader (1.11.3) for sites without ACF Extended, and this core plugin has none [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:18-19] [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:70-89]
- Guards direct access with `function_exists('add_action')` rather than the kit's required `ABSPATH` check [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:28] [doc:~/Dev/clc-plugins/CLAUDE.md:86]
- Sancho has a project `work/copper-leaf/projects/hd-system-rebuild/` for this system; not read for this entry [doc:~/Sync/Sancho/work/copper-leaf/INDEX.md]
