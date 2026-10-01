---
name: "Copper Leaf: HDOnline for Home Directions"
type: doc
business: copper-leaf
lobe: work
status: active
description: Home Directions, Inc. layer on HDOnline: appointment and report settings, letters, invoices, stamps; v1.11.7
sources: ["[doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php]", "[doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt]"]
---
# Copper Leaf: HDOnline for Home Directions

Registry entry built 2026-10-02 (batch B4) from the kit clone at `~/Dev/clc-plugins/hdonline-home-directions/`. No CLAUDE.md or README in the plugin; main file and release notes are the sources. Read-only.

## What it does
- "Extends Copper Leaf: HDOnline with customizations for Home Directions, inc." [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:4-5]
- Adds Home Directions field groups: HD Appointment Settings, HD Property Settings, HD Report Settings [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:85-87]
- Supplies the single templates for reports (letters) and invoices, including letterhead, engineering stamp options (a NY stamp since 1.9.0) and invoice payment language [doc:~/Dev/clc-plugins/hdonline-home-directions/single-hdo_reports.php] [doc:~/Dev/clc-plugins/hdonline-home-directions/single-hdo_invoices.php] [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:2-15] [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:75-95]
- Generates contracts through e2pdf templates (residential and commercial) and modifies pre-loaded Gravity Forms fields to send email [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:792-797] [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:1031]
- Keeps related post titles in step when an appointment is saved [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:1069]

## Where it runs
- Client: Home Directions, Inc. [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:5]
- Sancho's client folder: `work/copper-leaf/clients/home-directions/` [doc:~/Sync/Sancho/work/copper-leaf/clients/home-directions/entity.md:2-10]
- No staging alias or production address is stated in the plugin's files [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:1-40]

## Version and history
- Current version: 1.11.7, released 2026-08-20; header and newest tag `v1.11.7` agree [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:6] [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:2] [doc:~/Dev/clc-plugins/hdonline-home-directions/.git (git tag, read 2026-10-02)]
- Arc 1: 1.01 to 1.4 (2021 to 2022) live fixes folded in, Copper Leaf naming, automatic updates, page-password handling around print-to-PDF [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:118-168]
- Arc 2: 1.5 to 1.9 (2023 to 2025) pdfcrowd retired for WP PDF Generator, engineering stamp options, report styles inlined for printing, invoice and letterhead wording [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:45-115]
- Arc 3: 1.10 to 1.11.7 (2026-02-26 to 2026-08-20) followed the core plugin's admin move and bug audit, added an ACF fallback loader, then a run of invoice tweaks [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:2-43]

## Rules specific to this plugin
- No plugin CLAUDE.md, so the kit rules apply unchanged, PHP floor 7.4 [doc:~/Dev/clc-plugins/CLAUDE.md:63]
- Prefix as observed in code, not a stated rule: constants `CLC_HDO_HD_`, functions mostly `hdo_` / `hdo_hd_` [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:34-35] [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:1069]
- Branch is `main` [doc:~/Dev/clc-plugins/hdonline-home-directions/.git (git rev-parse, read 2026-10-02)]
- Release order with HDOnline matters when a change spans both (the 2026-03-04 bug audit shipped as hdonline 1.7.2 / 1.7.3 alongside this plugin's 1.11.1 / 1.11.2) [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:22-33] [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:15-29]

## Dependencies
- Copper Leaf: HDOnline (calls `hdo_admin_page_url()` when present) [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:183]
- ACF, with ACF Extended autosync and a fallback loader when ACF Extended is absent [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:70-97]
- Gravity Forms [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:145]
- e2pdf (contract templates) and WP PDF Generator by wpexperts.io [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:794] [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:115]
- Copper Leaf Updates Handler for automatic updates [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:40-62]

## Open threads
- No TODO is recorded in the release notes [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt]
- A commented-out password utility (`hdo_paint_with_passwords()`) and an invoice-password remover remain in history; page passwords were removed in 1.10.0 [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:41-66]
- Guards direct access with `function_exists('add_action')` rather than the kit's required `ABSPATH` check [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:27] [doc:~/Dev/clc-plugins/CLAUDE.md:86]
- Sancho has a project `work/copper-leaf/projects/hd-system-rebuild/` for this system; not read for this entry [doc:~/Sync/Sancho/work/copper-leaf/INDEX.md]
