---
name: "Copper Leaf Creative: Wizard Academy (Deux)"
type: doc
business: copper-leaf
lobe: work
status: active
description: Wizard Academy's core plugin on WooCommerce + ACF: classes, rosters, videos, subscriptions, partners; v3.4.11
sources: ["[doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php]", "[doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt]", "[doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md]", "[doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLEANUP-TODO.md]"]
---
# Copper Leaf Creative: Wizard Academy (Deux)

Registry entry built 2026-10-02 (batch B4) from the kit clone at `~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/`. Read-only; the plugin's own files win where this page and they disagree.

## What it does
- "Bringing it all together to sell & deliver video content, classes, and courses" [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:4-5]
- Sells classes as WooCommerce products (category 25) and processes orders into class rosters, with room and gate codes, rooming and 24-hour emails, and a printable roster [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:97] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:3-4] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:56]
- Delivers paid video content (videos, video series, subscriptions such as Ask the Wizards) from Wistia or YouTube, plus donations, coupon restrictions and a Content Dashboard [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:19-31] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:631-700]
- Partner Connection (v3.4.0): a student names a partner at purchase or invites one from My Account, with magic-link emails and an admin metabox [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:54-55] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:69-77]
- Owns the ACF field groups for its blocks, CPTs and settings, including the LearnDash lesson fields read by the LearnDash Customizations plugin, and has its own migrations framework [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:101-123] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:8] [doc:~/Dev/clc-plugins/CLAUDE.md:51]

## Where it runs
- Client: Wizard Academy [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:4]
- Staging: https://wizardacademy-dev.sitedistrict.com, SSH alias `wizardacademy-dev`, plugin in the site's `www/wp-content/plugins/copper-leaf-wizard-academy-deux/` [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:6]
- Staging host is host-2 per the kit handoff [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:63]
- Production site address is not stated in this plugin's files [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:1-10]

## Version and history
- Current version: 3.4.11, released 2026-09-21; header and newest tag `v3.4.11` agree [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:6] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:2] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/.git (git tag, read 2026-10-02)]
- Arc 1: 0.1 (2021-09-28) through 2.23 (2025-12-18), about 150 small releases growing classes, videos, coupons, donations and emails out of "original handwritten code" [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:104] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:834-838]
- Arc 2: 2.24.0 to 3.3.x (2026-02-13 onward) "the beginning of the big refactor": migration suite, Video Ratings removed (3.0.0), production-guarded MCP abilities (3.1.0), a two-checkbox production override for migrations (3.3.0) [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:63-101]
- Arc 3: 3.4.0 Partner Connection (2026-05-22), webhook customer-ID and duplicate-roster fixes through 3.4.9 (June 2026), then 3.4.10 YouTube lesson field and 3.4.11 security and caching release (2026-09-21) [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:2-56]

## Rules specific to this plugin
- Prefix `wasabi_` for functions and hooks, `WA_` for classes; JS namespace `wasabiPartner`; CSS `.wasabi-partner-` [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:5] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:60-61]
- PHP floor 7.4; no 8.0+ syntax such as `match`; no ternaries (Readability Rule) [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:96]
- Version source of truth is the `Version:` line in the main file [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:4]
- Architecture rules, do not change: no raw user IDs in front-end HTML (opaque ref tokens); purchase path is trust-and-execute; My Account path is an invitation flow; emails deferred via `wp_schedule_single_event()`; tokens stored as SHA-256 hashes; magic links are GET-then-POST; ACF partner field hidden, not removed; `$order->get_customer_id()` in payment hooks; per-line-item idempotency [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:65-77]
- State changes in Partner Connection must still write the `wasabi_partner_log` audit table [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:86]
- Uses `$wpdb->prepare()` for all queries; vanilla JS (no jQuery) for new code [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:59-60]
- Has a `migrations/` system that the kit's migration rule says to use [doc:~/Dev/clc-plugins/CLAUDE.md:51] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:39]
- All four of the kit's production lessons came from this plugin (partner log table, YouTube vs Wistia data check, webhook customer ID, duplicate roster) [doc:~/Dev/clc-plugins/CLAUDE.md:179-182]

## Dependencies
- WooCommerce (orders, My Account, coupons); HPOS compatibility not required yet [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:93]
- ACF Pro [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:94]
- Gravity Forms filters (`controllers/gravity-filters.contr.php`) [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:203]
- LearnDash, via the lesson field group it defines for the companion plugin [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:116]
- Copper Leaf Updates Handler for automatic updates [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:50-72]
- Companion: Copper Leaf: Wizard Academy LearnDash Customizations [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:8]
- Dev only: PHPUnit 9 (`composer.json`, `tests/`) [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/composer.json:3]

## Open threads
- Slated for retirement in the next code update: "Generate Random Room Codes" (Gordon decided 2026-09-26 it is not used); keep the Print Room Codes button and the `options_warc_*` options [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:115-126]
- Recommended after 3.4.11: generate new room codes and change the gate, kitchen, Spence door and gym codes; whether that was done is not recorded [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:3]
- Deferred data cleanup: orphaned `_wa_video_rating` meta (from 3.0.0) [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLEANUP-TODO.md:8-10]
- Gravity Forms Product Details retirement on production, and orphaned GF order item meta [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLEANUP-TODO.md:14-21]
- Partner Connection follow-ups: watch `wam_partner_needs_confirmation` flags clear, remove the confirmation banner after 90 days, retire the external My Account endpoint plugin, resolve 'conflict' users by hand [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLEANUP-TODO.md:25-32]
- Retired order fields still passed empty for backward compatibility, to be removed later [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLEANUP-TODO.md:34-42]
- Handoff follow-up: `Undefined array key "page"` in `controllers/wa-classes.contr.php` line 111; 3.4.11 reports fixing "thousands of PHP warnings" in nearby code, but this exact item is not named as closed [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:249] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:11]
- The CLAUDE.md body is still the Partner Connection QA brief (v3.4.0) "kept for reference"; refreshing it is a plugin-ship cleanup step [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:10] [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:104]
