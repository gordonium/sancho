---
name: "Copper Leaf: Wizard Academy LearnDash Customizations"
type: doc
business: copper-leaf
lobe: work
status: active
description: LearnDash tweaks for Wizard Academy's Ad Writers' Guild: lesson video (Wistia or YouTube), comments, mail; v1.9.0
sources: ["[doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php]", "[doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt]"]
---
# Copper Leaf: Wizard Academy LearnDash Customizations

Registry entry built 2026-10-02 (batch B4) from the kit clone at `~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/`. The plugin has no CLAUDE.md or README; its main file and release notes are the sources. Read-only.

## What it does
- LearnDash customizations "mostly for Ad Writers' Guild", migrated from ASBI in 2022 [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:4-5]
- Prints the video at the top of a LearnDash lesson: YouTube when the lesson's "YouTube URL" field is filled, otherwise Wistia; a YouTube URL that cannot become a player falls back to Wistia, and the YouTube player is cached for a week [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:3-4] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:113-114]
- Adds assignment comment handling and two notification shortcodes (`awmc_student_comment_notification`, homework notification) [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:319-321] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:430-431] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:489]
- Sets site mail From to "Wizard Academy" at noreply@wizardacademy.org, takes Reply-To from the main plugin's `wa_get_vc_reply_to()`, and adjusts LearnDash ProPanel outgoing email [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:528-542] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:571] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:20]
- Adds JavaScript that fixes quiz scroll padding [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:16] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:589-590]

## Where it runs
- Client: Wizard Academy (Ad Writers' Guild lessons) [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:5]
- Production site address is not stated in the plugin; it sends mail as noreply@wizardacademy.org [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:529]
- Staging: this plugin has no CLAUDE.md naming one; the companion plugin Wizard Academy (Deux) names alias `wizardacademy-dev` [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:6]

## Version and history
- Current version: 1.9.0, released 2026-09-21; header and newest tag `v1.9.0` agree [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:6] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:2] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/.git (git tag, read 2026-10-02)]
- Arc 1: 1.1 to 1.4 (June to July 2022) brought it into git, cleaned up the ASBI code for Wizard Academy, and added a Wistia padding option [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:47-63]
- Arc 2: 1.5 to 1.7 (2022 to 2024) moved updates onto Plugin Update Checker and then the Copper Leaf Updates Handler, and replaced a hard-coded Reply-To with the main plugin's lookup [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:19-40]
- Arc 3: 1.8.0 (2026-02-17) quiz scroll fix; 1.9.0 (2026-09-21) YouTube lesson video, an empty-Wistia fix and output hardening, carrying the unreleased 1.8.1 [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:2-16]

## Rules specific to this plugin
- No plugin CLAUDE.md, so the kit rules apply unchanged, PHP floor 7.4 [doc:~/Dev/clc-plugins/CLAUDE.md:63]
- Prefix as observed in code, not a stated rule: constants `CLC_WA_LD_`; functions mixed (`wa_`, `awmc_`, `wpb_`, `ld_`, one `wasabi_`) [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:35-36]
- The lesson fields it reads ("YouTube URL", "Wistia Video ID", "Portal Size Override") are defined in Wizard Academy (Deux), `acf/learndash-lesson-custom-fields.json`; either plugin can be updated first [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:8] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:3]

## Dependencies
- LearnDash (hooks `learndash-lesson-content-tabs-before`, `learndash-assignment-row-after`, ProPanel email filter) [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:113] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:319] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:571]
- ACF (`get_field()` on lesson fields) [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:99-119]
- Wizard Academy (Deux): field definitions and `get_vice_chancellor_email()` [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:544]
- Copper Leaf Updates Handler for automatic updates [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:41-63]
- Wistia and YouTube as video sources [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:204] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:246]

## Open threads
- The release notes record no open TODO; 1.8.1 was never released on its own and is carried by 1.9.0 [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:8]
- The plugin guards direct access with `function_exists('add_action')` rather than the kit's required `ABSPATH` check; the handoff lists this pattern as a pre-existing follow-up [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:28] [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:254]
- The admin stylesheet is registered as `wa_learnda1sh_wp_admin_css` but enqueued as `wa_learndash_wp_admin_css` (handle typo; observed, not tested) [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:82-83]
