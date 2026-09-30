---
name: Survey · hdonline-home-directions child plugin
type: doc
lobe: work
description: Read-only code survey of the hdonline-home-directions child plugin (v1.11.7, HEAD 7e26a6e) by a Sancho subagent, cited file:line; what the child adds, the templates, invoice math, history, 16 open questions
sources: ["[doc:~/Dev/clc-plugins/hdonline-home-directions]", "[derived: sancho subagent 2026-09-30]"]
---
# Survey: hdonline-home-directions (Copper Leaf: HDOnline for Home Directions) child plugin

Repo: `/Users/gordonium/Dev/clc-plugins/hdonline-home-directions` (branch `main`, HEAD `7e26a6e` "pay by check on invoices", clean tree). Read-only survey, 2026-09-30. Nothing was changed. This survey assumes the base survey (`survey-hdonline.md`, same folder) has been read; it does not repeat what the base does, only what this layer adds, overrides or contradicts.

File aliases used below:

- `main` = `copper-leaf-hdonline-home-directions.php` (1,202 lines)
- `ajax` = `copper-leaf-hdonline-hd-ajax.inc.php` (141 lines)
- `reports` = `single-hdo_reports.php` (456 lines)
- `invoices` = `single-hdo_invoices.php` (267 lines)
- `js` = `js/hdonline-home-directions.js` (59 lines)
- `css` = `copper-leaf-hdonline-home-directions.css` (43 lines)
- `classes/<name>` = `classes/<name>-hd.class.php`
- `acf/<key>` = the three ACF PHP field-group files
- `base:main`, `base:ajax`, `base:cpt` = the base plugin files, as aliased in the base survey
- `cpt.php`, `acf-cpt.php` and `classes/note-hd.class.php` are empty (a bare `<?php` or zero bytes: `cpt.php:1-3`, `acf-cpt.php:1-3`, `classes/note-hd.class.php` is 0 bytes)

## 1. What this layer adds, in one paragraph

The base plugin knows how to pick standard paragraphs and compile them into a report. This child plugin is everything that makes it Home Directions: it takes the "New Appointment" Gravity Form and turns one submission into a Client, an optional Broker and Attorney, a Property, a Report, an Invoice and an Appointment all wired together (`main:195-663`); it adds the Invoice, Broker, Attorney, "copy to broker/attorney", property vitals (year built, square footage, house type, water, sewage, detached structures) and an engineering-stamp switch to the data (`acf/*`); it draws the report page the client sees (logo, cover photo, "Prepared for", property details, table of contents, the compiled body, and for consultation letters Peter Seirup's signature and CT or NY P.E. stamp) with print CSS so a browser print becomes the PDF (`reports`); it draws the invoice page with line items, hard-coded prices for water and radon tests, discounts and a PAID state (`invoices`); it adds a "letter to the lender" wrapper around the Bank Summary section and an optional "Appendix to Detached Structures" at compile time (`main:929-999`); it hides certain subheadings and "General Information" blocks depending on the property (`main:901-1028`); it adds Files links (contract and data-sheet PDFs via the e2pdf plugin) and broker/attorney panels to the View Appointment screen (`main:669-824`); and it points the "Email Report" form at a different Gravity Form that can also copy the broker and attorney (`main:1032-1064`).

## 2. Header, version, dependency on the base, hooks, overrides

### Header and version

- Plugin Name "Copper Leaf: HDOnline for Home Directions", Description "Extends Copper Leaf: HDOnline with customizations for Home Directions, inc.", **Version 1.11.7**, Author "Copper Leaf Creative, Gordon Seirup", GPLv2: `main:3-10`. `release-notes.txt:2` agrees (1.11.7, 20260820).
- No version constant; the header is the only version. No `Requires Plugins`, `Requires PHP`, text domain (ad hoc `'my-text-domain'` at `main:62`).
- Constants: `CLC_HDO_HD_PLUGIN_PATH`, `CLC_HDO_HD_PLUGIN_URL` (`main:34-35`). `CLC_HDO_HD_PLUGIN_URL` is used once, for the stamp image (`reports:174`).
- Direct-access guard is the same non-standard `function_exists('add_action')` check as the base (`main:27-30`). No file other than `main` has any guard; `ajax`, `cpt.php`, `acf-cpt.php`, the six class files, `puc.php`, both templates and the three `acf/*.php` files have none.
- `.gitattributes` is `* text=auto` only (`.gitattributes:2`); the repo rule in `clc-plugins/CLAUDE.md` section 8 asks for `* text=auto eol=lf`.

### How it depends on the base, and what breaks without it

There is **no explicit check** that the base plugin is active. The dependency is expressed three ways, none of them guarded:

1. Each extended class does `include_once( ABSPATH . '/wp-content/plugins/copper-leaf-hdonline/classes/<x>.class.php')` (`classes/appointment:3`, `classes/contact:3`, `classes/property:3`, `classes/report:3`). This hard-codes the installed folder name `copper-leaf-hdonline` (the repo folder is `hdonline`, the PUC slug is `copper-leaf-hdonline`, `puc.php:10` of the base) and hard-codes `wp-content/plugins` instead of `WP_PLUGIN_DIR`. If the base is absent the include emits a warning and `class AppointmentHD extends Appointment` is a fatal "Class not found" at plugin load (`classes/appointment:5`), so **the whole site's plugin load fails**, not just this feature.
2. Global base functions are called with no `function_exists` guard: `hdo_extract_id_from_acf_field` (`classes/appointment:40-42`), `hdo_get_appointment_ids_from_meta` (`main:934`, `reports:8`, `invoices:17`), `hdo_make_contact_details_output` (`main:675, 687`, `reports:122`), `hdo_guten_note` is not used here. Only `hdo_admin_page_url` is guarded (`main:183, 656`).
3. Every hook in this plugin is a base filter or action (section 2, "Hooks"), so without the base nothing fires; with the base but without this child, the base fatals at compile (`base:ajax:195` news up `AppointmentHD`). The two plugins are mutually dependent.

A fourth dependency, **`clc_die_silently()`**, is called 30+ times (`main:456, 749, 949-953`, `reports:112-135`) and is defined in **neither** repo (grep of `/Users/gordonium/Dev/clc-plugins` for `function clc_die_silently` finds nothing). It must live in the Genesis child theme or an mu-plugin on the live site. Unconfirmed. Without it: fatal on View Appointment, on every report page, and inside the GF submission handler when a new property is created (`main:456`). Its inferred contract from every call site is `clc_die_silently( $value, $before, $after )` returning `$before . $value . $after` when `$value` is non-empty, else `''`.

Other runtime dependencies: Copper Leaf Updates Handler (`CLC_UPDATES_CHECKER_PLUGIN_PATH`, `main:40-56`, `puc.php:3`); PUC v5 pointed at `https://github.com/CopperLeafCreative/copper-leaf-hdonline-home-directions`, slug `copper-leaf-hdonline-home-directions`, release assets enabled (`puc.php:7-11`, `main:44`); the GitHub PAT read from option `options_clcs_github_personal_access_token` (`main:47`, value lives in the DB, [secret omitted]); ACF Pro (`acf_add_local_field_group`, `get_field`, `have_rows`); ACF Extended for autosync (`main:72-92`) with a fallback loader on `acf/init` when class `acfe` is absent (`main:95-101`, added 1.11.3); Gravity Forms (`gform_after_submission_1` and `_5`, `rgar()` at `main:478`); e2pdf plugin shortcodes (`main:782-804`); Genesis (`genesis()` at `reports:455`, `invoices:266`).

### Hooks registered by the child

| Hook | Callback | Where | What it does |
|---|---|---|---|
| `admin_notices` | `hdo_hd_clc_functions_required` (only if Updates Handler absent) | `main:54-65` | notice on Plugins screen |
| `acfe/settings/php_load` | `copper_leaf_hdonline_home_directions_php_load_point` (adds `acf/` with a doubled slash) | `main:72-81` | ACFE autosync load |
| `acfe/settings/php_save/key=` group_5f4ffb1a73e43, group_5f4fee784989f, group_65205410841a4 | `..._acfe_php_save_point` | `main:85-92` | ACFE autosync save |
| `acf/init` | `..._load_field_groups_fallback` (requires `acf/group_*.php` when `acfe` class missing) | `main:95-101` | 1.11.3 fallback |
| `init` | `clc_hdo_hd_appointments_acf_cpt_configs` (requires empty `cpt.php` and `ajax`) | `main:113-117` | |
| `wp_enqueue_scripts` (50), `admin_enqueue_scripts` | `clc_hdo_hd_css`, `clc_hdo_hd_admin_css` (same handle `clc_hdo_hd_css`, same file) | `main:121-131` | |
| `init` | `hdo_hd_script_enqueuer` (registers, localizes `myAjax`, enqueues on every request) | `main:135-142` | see section 8 for the `myAjax` collision |
| `gform_after_submission_5` | `hdo_hd_process_new_appointment_local` | `main:154-190` | LOCAL form: report + appointment only |
| `gform_after_submission_1` | `hdo_hd_process_new_appointment` | `main:195-663` | the online New Appointment handler |
| `hdo_view_appt_other_appts_output` | `hdo_hd_view_appt_add_broker_and_attorney` | `main:669-702` | Broker and Attorney panels |
| `hdo_view_appt_appt_guts` | `hdo_hd_view_appt_appt_details` | `main:706-735` | type, copy-to flags, fee |
| `hdo_view_appt_property_guts` | `hdo_hd_view_appt_property_details` | `main:739-757` | vitals |
| `hdo_view_appt_property_output` | `hdo_hd_view_appt_add_files` | `main:761-824` | Files panel |
| `hdo_report_actions_metabox_filter` | `hdo_hd_actions_meta_box` | `main:853-880` | clipboard buttons, consult CSS |
| `hdo_compile_button_args` | `hdo_hd_compile_button_mods` | `main:884-895` | id `hdo-hd-compile-report`, `data-detached` |
| `hdo_compile_subhead` | `hdo_hd_suppress_subheads` | `main:901-914` | |
| `hdo_global_subsections_included` | `hdo_hd_remove_suggestions_from_summary` | `main:917-923` | |
| `hdo_section_bank_summary` | `hdo_hd_add_bank_summary_header_and_signature` | `main:929-970` | lender letter |
| `hdo_compiled_report` | `hdo_hd_add_to_compiled` | `main:974-999` | detached appendix |
| `hd_compiling_general_information` | `hdo_hd_general_information_intelligence` | `main:1003-1028` | |
| `hdo_email_form_args` | `hdo_hd_email_form_args` | `main:1032-1064` | GF form 4, broker/attorney |
| `acf/save_post` | `hdo_hd_update_related_post_titles_on_appt_save` | `main:1069-1089` | retitle invoice |
| `single_template` | `hdo_hd_single_templates` | `main:1121-1168` | plugin templates for reports and invoices |
| `hdo_view_appt_report_action_buttons` | `hdo_hd_alter_hdo_action_buttons_for_consults` | `main:1172-1185` | Letter buttons |
| `hdo_make_select_notes_in_view_appt` | `hdo_hd_skip_select_notes_for_consults` | `main:1189-1198` | |
| `hdo_delete_appointment` (registered with `add_action`, applied as a filter by the base) | `hdo_hd_delete_appointment` | `ajax:12-103` | trash invoice, orphan broker/attorney |
| `hdo_delete_appt_client_orphan_check` | `hdo_hd_check_brokers_and_attys` | `ajax:111-141` | widen client orphan check |
| `the_content` | `hdo_draw_report` | `reports:4-452` | registered inside the template file |
| `the_content` | `hdo_draw_invoice` | `invoices:3-262` | registered inside the template file |

Filters the child itself exposes: `hdo_hd_view_appt_file_links_array` (`main:786`) and `hdo_report_toc_array` (`reports:65`, but the return value is discarded so it can never change anything).

No activation, deactivation, uninstall, cron, REST, shortcodes, custom tables, options written, or AJAX actions of its own (the two in `ajax:4, 8` are commented out).

### What it overrides or contradicts in the base

- Email form: base uses Gravity Form **3** (`base:main:1096`); the child forces **4** (`main:1039`) and adds broker/attorney fields and an invoice link.
- Compile button: base id `hdo-compile-report` and its JS handler (`base:main:1040`, base JS); the child renames it `hdo-hd-compile-report` (`main:892`) so the base JS no longer binds and the child JS takes over with the extra `detached_pass` parameter (`js:4-58`).
- Consultation appointments: the base already relabels "View Report" as "View Letter" in the "been here before" list (`base:main:524-528`); the child removes Select Notes and Compile for consults and relabels edit/view/email buttons as Letter (`main:1173-1185`), and suppresses the notes selector (`main:1190-1198`).
- Templates: the base ships none; the child claims `single_template` for `hdo_reports` and `hdo_invoices` from the plugin folder, falling back to the theme (`main:1121-1168`).
- `myAjax` localized object: both plugins define it (`base:main:319-326`, `main:138`); see section 8.
- Report and appointment title rewrite: base rewrites report and appointment titles on appointment save (`base:main:1715-1743`); the child adds the invoice (`main:1069-1089`) and explicitly declines to do the same on property save (comment "FOLLY!", `main:1094`).
- The base's comment at `base:ajax:175` points at "LINE 812" of this file and the child's comment at `main:928` points at "LINE 165" of the base; both line references are stale.

## 3. Data model additions

### CPTs and taxonomies

**None registered here.** `cpt.php` and `acf-cpt.php` are empty (`cpt.php:1-3`, `acf-cpt.php:1-3`). The Invoice CPT `hdo_invoices` is registered by the base (`base:cpt:200-232`) and only populated and rendered here. The child depends on these **term values** existing in the live DB (created by name on first use or pre-existing):

- `hdo_contact_types`: `client`, `broker`, `attorney` (`main:207, 217, 277, 290, 300, 362, 375, 385, 447`). `ContactHD->contactTypes` is keyed `term_id => slug` (`classes/contact:17-27`).
- `hdo_appointment_types`: the GF value `$entry['49']` is `consultation` or `inspection` (`main:542-544, 594`), but every comparison in code is against the term **name** `Consultation` with a capital C (`main:867, 1175, 1192`, `reports:18, 143`, via `base:classes/appointment:64`). This works only if a term named "Consultation" with slug `consultation` already exists so `tax_input` resolves by slug. Unconfirmed.
- `hdo_note_sections` names and slugs the child hard-codes: `sewage-disposal`, `water-supply`, `termites`, `summary` (`main:904, 908, 919`), `bank-summary` (`main:932`, `css:1`, `reports:348-355`), and the names `Water Supply System`, `Sewage Disposal System`, `General` (`main:1006-1021`). `hdo_note_subsections` name containing `Suggestions` (`main:908`) and the lowercase literal `suggestions` (`main:920`).

### ACF field groups (three, in `acf/*.php`; `acf-export-2022-02-22.json` holds only the first two and is stale)

**group_5f4ffb1a73e43 "HD Appointment Details"**, location `post_type == hdo_appointments`, position normal (`acf/group_5f4ffb1a73e43.php:5-174`)

| Field name | Key | Type | Details |
|---|---|---|---|
| `hdo_appt_invoice` | field_5f57bfb3d35cc | relationship to `hdo_invoices`, min 1, max 1, return id | `:9-33` |
| `hdo_appt_broker` | field_5f4ffb1a8bb21 | relationship to `hdo_contacts`, no max, return id, width 75 | `:34-58`; code takes the first (`classes/appointment:41`) |
| `hdo_appt_copy_to_broker` | field_5f4ffb1a8bd03 | true_false, message "Email Report to the Broker", default 0 | `:59-77` |
| `hdo_appt_attorney` | field_5f4ffb1a8bb61 | relationship to `hdo_contacts`, no max, return id | `:78-102` |
| `hdo_appt_copy_to_attorney` | field_5f4ffb1a8bd3d | true_false, message "Email Report to the Attorney" | `:103-121` |
| `hdo_appt_additional_contacts` | field_5f528e139e21c | relationship to `hdo_contacts`, no max, return **object** | `:122-146`; read only by the base (`base:classes/appointment:71`) |

**group_5f4fee784989f "HD Property Details"**, location `post_type == hdo_properties` (`acf/group_5f4fee784989f.php:5-182`)

| Field name | Key | Type | Choices / details |
|---|---|---|---|
| `hdo_property_year_built` | field_5f4fee7858442 | number | `:9-29`; compared as `> '1980'` at `main:1020` |
| `hdo_property_square_footage` | field_5f4fee7858483 | text | `:30-48` |
| `hdo_property_house_type` | field_5f4fee78584be | select, allow_null, return label | Antique, Cape, Colonial, Commercial, Condo, Contemporary, Cottage, Custom, Ranch, Restaurant, Split-Level, Townhouse, Two-Family, Other (`:62-77`); `Commercial` is special-cased (`main:793`, `reports:67`); the GF handler writes `$entry['58']` and compares it to lowercase `commercial` (`main:545`) |
| `hdo_property_water_supply` | field_5f4fee78584fa | radio, allow_null, return label | City, Well, Community Well (`:99-103`); `City` special-cased (`main:1012`) |
| `hdo_property_sewage_disposal` | field_5f4fee7858535 | radio, no null, return label | City Sewer, Septic, Cesspool (`:124-128`); `City Sewer` special-cased (`main:1016`) |
| `hdo_property_detached_structures` | field_5f4fee7858571 | text | `:136-154`; by convention a comma-separated list, split at `main:985-986` |

**group_65205410841a4 "HD Report Settings"**, location `post_type == hdo_reports`, position **side**, label placement left (`acf/group_65205410841a4.php:5-89`)

| Field name | Key | Type | Details |
|---|---|---|---|
| `hdo_hd_include_engineering_stamp` | field_65205412a9d79 | true_false, message "Include Engineering Stamp in Consult Letter", default 0 | `:9-28` |
| `hdo_hd_include_engineering_stamp_which_one` | field_65e9101819cfb | radio `ct` "Connecticut", `ny` "New York", return value, conditional on the stamp being on | `:29-61` |

All three groups: `show_in_rest => 0`, `acfe_autosync => php`.

### Post meta written outside ACF's own save path

The GF handler writes every field with `update_post_meta` directly and writes the ACF **reference** key as `'field_' . uniqid()` (a random string that is not a real field key) for every field except the inspector (`main:181, 221-265, 304-352, 389-437, 467-511, 552-578, 606-646`). Only `_hdo_appt_inspector` gets the real key `field_5f4fe4b29b2d7` (`main:602`). Consequence: on any post created by the form and never re-saved in the admin, ACF cannot resolve the field from the reference, so `get_field()` returns the **raw, unformatted** meta (arrays of ID strings, `'1'`/`''` instead of booleans, values instead of labels). The code mostly tolerates this (`hdo_extract_id_from_acf_field`, loose `== true`), but it is a migration hazard: see section 10.

| Key | On | Written | Read | Shape |
|---|---|---|---|---|
| `hdo_gf_entry_id` | hdo_appointments | `main:649` | base `classes/appointment:67` | GF entry id, no `_` reference (comment "NOT an ACF field", `main:648`) |
| `hdo_appt_inspector` | hdo_appointments | `main:601` | base | hard-coded `array("5")`: **user ID 5 is always the inspector** |
| `hdo_appt_client`, `_property`, `_report`, `_invoice`, `_broker`, `_attorney` | hdo_appointments | `main:605-626` | classes | `array( $id )` where `$id` is an **int** from `wp_insert_post` or a **string** from `preg_replace` on the GF value (`main:274, 360, 445, 513`); ACF admin saves write arrays of strings |
| `hdo_appt_date` | hdo_appointments | `main:629` | base | raw GF value `$entry['54']` in whatever format form 1 uses; ACF's own format is `Ymd`; both shapes coexist until the appointment is re-saved |
| `hdo_appt_time` | hdo_appointments | `main:633` | base | raw GF value `$entry['57']` |
| `hdo_appt_copy_to_broker`, `_attorney` | hdo_appointments | `main:637, 641` | `classes/appointment:44-45` | raw GF checkbox value `$entry['69.1']` / `['70.1']` (a label string or `''`), not `'1'`/`'0'` |
| `hdo_contacts_*` (12 keys) | hdo_contacts | `main:220-265, 303-352, 388-437` | base | raw strings; `hdo_contacts_zip` is an ACF number field but receives the GF text |
| `hdo_property_*` (11 keys) | hdo_properties | `main:466-511` | classes | raw strings; `hdo_property_house_type` from `$entry['58']` |
| `hdo_invoice_default_fee_description` | hdo_invoices | `main:551` | `classes/invoice:40` | one of three fixed sentences (`main:543-548`), or **undefined** if `$entry['49']` is neither value |
| `hdo_invoice_fee`, `_add_to_base_fee`, `_fee_adjustment` | hdo_invoices | `main:555-563` | `classes/invoice:42-44` | raw GF values `$entry['63'], ['67'], ['68']`; `hdo_add_up_fee` treats anything non-numeric (for example a currency-formatted string) as 0 (`main:829-843`) |
| `hdo_invoice_repeat_client_discount` | hdo_invoices | `main:567` | `classes/invoice:45` | raw GF checkbox value `$entry['64.1']` |
| `hdo_invoice_additional_services` | hdo_invoices | `main:571-577` | `classes/invoice:46` | array of GF checkbox values from `65.1` to `65.5` (five GF choices vs three ACF choices), or **null** when none chosen (`$add_services_array` never initialised, `main:574`) |
| `hdo_invoice_paid`, `hdo_invoice_notes`, `hdo_invoice_additional_line_items` | hdo_invoices | never by code | `classes/invoice:41, 47-48` | set by hand in the admin only (`main:580-583` comment) |
| `hdo_hd_include_engineering_stamp`, `_which_one` | hdo_reports | admin only | `classes/report:18-19` | `'1'`/`'0'`, `'ct'`/`'ny'` |
| `post_password` | hdo_reports, hdo_invoices | historically (1.9.2 to 1.10.0, `release-notes.txt:41-68`); no code remains | | may still be set on old rows; unconfirmed |

Options: only `options_clcs_github_personal_access_token` is read (`main:47`). Nothing is written.

### The Report's data as stored (base plus child)

A Report (`hdo_reports`) row consists of:

- `post_title` and `post_name`: `"<Property title> - <Client name> - <date>"`. Created by the child from GF with the **raw** GF date string (`main:520`), later rewritten by the base on every appointment save with the **pretty** date `F j, Y` (`base:main:1726-1741`, `base:classes/appointment:53-55`). So titles come in two date styles depending on whether the appointment was ever re-saved. Slug changes with title.
- `post_status` `publish` from creation (`main:523`), public by URL (`base:main:1861`).
- `post_content`: empty at creation for both inspections and consultations (`main:521-527`; the "intro lines" for consults added in 1.3.0 were removed in 1.11.2, `release-notes.txt:29, 140`). For inspections, filled by Compile with Gutenberg blocks: `h2` per parent section, `h3` per section, `h4` per global subsection (minus the ones the child suppresses), `wp:html` General Information blocks (minus the ones the child suppresses), `hdo-selected-note` paragraphs each starting with a hidden `span.hdo-note-title-in-note`, the lender letter wrapped around Bank Summary (`main:941-966`), and optionally the detached-structures appendix (`main:979-993`). Photos and any edits are added by hand in Gutenberg afterwards. For consultations, the entire letter is hand-written in Gutenberg.
- `_thumbnail_id`: the cover photo (`reports:117`).
- `hdo_selected_note` (many rows, `"<note_id>|<exts>"`) and `_hdo_report_is_compiled` = `'1'` (base).
- `hdo_hd_include_engineering_stamp` and `hdo_hd_include_engineering_stamp_which_one` (child), only honoured on consultation letters (`reports:143-182`).
- Historically `post_password` (retired).
- No pointer back to the appointment; the appointment's `hdo_appt_report` serialized array is the only link, found by `LIKE` (`reports:8`).

## 4. The extended classes

All five non-empty class files follow the base pattern: run a `WP_Query` on `p => $id` inside the constructor and populate properties with `get_field`. Each also calls the parent constructor, so hydrating one `AppointmentHD` costs two `WP_Query`s plus a `get_field` per property, and View Appointment hydrates `AppointmentHD` at least four separate times (`main:671, 708, 763, 866`).

**`AppointmentHD extends Appointment`** (`classes/appointment:5-53`). Declares `$invoiceID, $brokerID, $attorneyID, $additionalContactsIDs, $copyToBroker, $copyToAttorney` (`:7-12`; `additionalContactsIDs` is also set by the base parent). Adds `invoiceID`, `brokerID`, `attorneyID` via `hdo_extract_id_from_acf_field(get_field(...))` (`:40-42`, the 1.11.1 fix), `copyToBroker`, `copyToAttorney` raw from `get_field` (`:44-45`), and an **undeclared** `includeEngineeringStamp` read from the appointment post (`:47`), which is wrong: that field lives on the report (`acf/group_65205410841a4.php:63-70`), so this property is always empty and nothing reads it (`ReportHD` is what the template uses, `reports:15, 160`). Null-id early return returns the undefined `$appointment` (`:16-18`). No methods beyond the constructor.

**`ContactHD extends Contact`** (`classes/contact:5-53`). Adds `$contactTypes` (`term_id => slug` map of `hdo_contact_types`, `:17-27`) and two write methods, `setContactType($postID, $contactType)` and `addContactType(...)`, which call `wp_set_post_terms` with append `true` and `false` respectively (`:31-51`). Note the names are backwards relative to the append flag (`setContactType` appends, `addContactType` replaces). Neither method is called anywhere in either repo (dead code; the GF handler uses `wp_set_object_terms` directly, `main:217, 277`).

**`InvoiceHD`** (`classes/invoice:3-58`). Standalone; extends nothing and includes nothing. Declares `$paid, $fee, $addToFee, $feeAdjustment, $repeatClientDiscount, $additionalServices, $additionalLineItems, $notes` (`:5-12`) and sets undeclared `$invoiceID`, `$name`, `$feeDescription`, `$insp_fee` (`:21, 39-40, 53`). `insp_fee` = `round( hdo_add_up_fee(fee, addToFee, feeAdjustment), 0, PHP_ROUND_HALF_DOWN )` (`:53`), computed even when the query found nothing. The `WP_Query` omits `fields => ids` unlike the others (`:24-28`). `additionalLineItems` is loaded (`:47`) but the invoice template re-reads the repeater with `have_rows` instead (`invoices:37`).

**`NoteHD`**: the file is empty (0 bytes) but is `include_once`d (`main:108`). Harmless.

**`PropertyHD extends Property`** (`classes/property:5-52`). Adds `yearBuilt, squareFootage, houseType, waterSupply, sewageDisposal, detachedStructures` (`:7-12, 41-46`) and re-sets `$this->name = get_the_title()` (`:40`), which the base already did. Null-id early return returns the undefined `$property` (`:17-19`).

**`ReportHD extends Report`** (`classes/report:5-23`). Adds `includeEngineeringStamp` and `whichStamp` (`:7-8, 18-19`). This is the only place `Report` (an empty class in the base) is extended, and the only reader of the HD Report Settings group.

## 5. The report template `single-hdo_reports.php` in detail

The file defines `hdo_draw_report()` and hooks it on `the_content` (`reports:4, 452`), then calls `genesis()` (`reports:455`) so the theme's loop runs and the filter fires on the main query's content only (`reports:6`). Everything below is string-built with no escaping.

### Data gathered (`reports:8-15`)

Appointment found by `LIKE` on `hdo_appt_report` and `[0]` taken (`:8-9`, warning and empty page if none). Then `AppointmentHD`, `PropertyHD`, `ContactHD` (client), `InvoiceHD`, `ReportHD`.

### Two modes: Consultation letter vs inspection report (`reports:18-94`)

- **Consultation** (`appointmentType == 'Consultation'`, `:18-30`): title "Consultation Letter", wrapper class `hdo-consultation`, the word "Letter" in the inspector links. No TOC. The PDF button lines are all commented out (`:21, 24-27`).
- **Inspection** (`:31-94`): title "Building Inspection Report" when `houseType == 'Commercial'`, else "Home Inspection Report" (`:67-71`). Builds the **table of contents** by `parse_blocks` on the post content, taking every `core/heading` with `attrs.level < 4` (h2 and h3; h2 headings usually carry no `level` attr so this reads an undefined key), slugifying the text the same way compile did (`:40-45`), and skipping `observations`, `suggestions` and blanks (`:43`). When the invoice has "Water Test" it appends two external links to homedirections.net pages (interpreting water test results, radon in water); "Radon in Air" appends the radon-in-air page (`:50-59`). "Cover Page" is prepended (`:62`). `hdo_report_toc_array` filter result is discarded (`:65`). The TOC is rendered as a fixed bar `#hdo-report-toc` (Font Awesome bars SVG inline, `:79-84`) with a hidden full-screen `#hdo-report-the-toc` overlay (`:88-92`); the base JS toggles it and offsets hash scrolling by 130px (`base:js:448-458`). The bar carries class `pdfcrowd-hide` so it is hidden in print (`:76, 429`).

### Inspector links (`reports:96-101`)

When logged in: "Inspector Dashboard | View Appointment | Edit Report/Letter", the first two via `hdo_admin_page_url` (escaped), the third a hard-coded `/wp-admin/post.php?post=...&action=edit`. Hidden in print.

### Cover page (`reports:103-140`)

`#hdo-report-wrapper` > `#hdo-report-cover-page`:

1. Header row: `images/home-directions-logo.png` (`:109`) left; right-aligned title, address line "`address address2, city state`" (`:112`), and the pretty date (`:113`).
2. `.hdo-report-thumbnail`: the post thumbnail at size `large` (`:117`), the cover photo.
3. Two columns: "Prepared for:" with the client block from the base's `hdo_make_contact_details_output` (`:122`), which includes the contact's **internal notes** in `<p class="hdo-notes">` (`base:main:380`) that the template then hides with CSS (`:316-318`) rather than omitting; and "Property Details" with the italic line "As provided at time of booking." (`:126`), the address block, and one line each for Building Type, Year Built, Square Footage, Water Supply, Sewage Disposal, Detached Structures, each omitted when empty via `clc_die_silently` (`:127-135`).

A page-break shortcode for the print plugin is commented out (`:141`).

### Body

`$content` is the post content as WordPress rendered it, headings carrying `id`s from compile and from the base's `render_block` filter (`base:main:1831-1843`). The template contributes no section or photo markup of its own; sections, subsections, notes and photos are all in `post_content`.

### Signature and stamp (consultations only, `reports:143-182`)

Wrapped in `div.nobreak`: "Sincerely," then an image block hard-coded to the uploads library, `/wp-content/uploads/2020/11/peter-signature-pe.jpg` with attachment id 12303 (`:151-153`; this file is **not** in the plugin, it is site data), then "Peter Seirup, P.E." with "CT License #13055" and "NY License #89793" (`:156`). If `ReportHD->includeEngineeringStamp == '1'` (`:160`): `whichStamp == 'ny'` picks `peter-seirup-engineering-stamp_NY_WEB_20240306.png`; `'ct'` **or anything else** (including empty, for reports stamped before the NY option existed in 1.9.0) picks `peter-seirup-engineering-stamp_WEB_20231106.png` (`:162-168`). The stamp floats right with `margin-top: -189px` so it overlaps the signature block (`:398-401`). The stamp is never shown on inspection reports even though the ACF group appears on every report.

Image inventory in `images/`: used are `home-directions-logo.png` (`reports:109`), `letterhead-2025.gif` (`main:943`, `invoices:137`), `peter_signature.gif` (`main:961`, the Bank Summary letter), the two stamps above, and `monkey-jumping.gif` (`css:15`, loading overlay). **Unused**: `letterhead2.gif` (superseded in 1.9.6, `release-notes.txt:50`) and `peter-seirup-engineering-stamp_WEB_20231006.png` (superseded in 1.8.1, `release-notes.txt:80`).

### Inline styles and print handling (`reports:185-442`)

A `<style>` block is appended **after** the content (`:448`) so that printing picks it up (1.8.0 decision, `release-notes.txt:84`). Notable rules: fixed TOC bar and overlay (`:188-241`); hides the theme title, header, footer, entry meta, `.site-inner` margins (`:279-281, 385-396`); hides `.hdo-note-title-in-note` (`:283-285`) and `.hdo-notes` (`:316-318`); hides `h2#bank-summary` with `visibility: hidden; height: 0` (`:348-355`), which tells us Bank Summary is a **parent** section whose h2 is unwanted because the lender letter supplies its own heading; `h3#summary` gets a top rule and 60px padding (`:361-365`); `h3#sewage-disposal`, `#water-supply`, `#termites` lose their bottom border (`:374-378`), matching the subheads the child suppresses at compile. Print rules (`:409-437`): **every `img` gets `page-break-before` and `page-break-after: always` and `max-height: 1000px`**, so each photo in the body lands on its own page, except `img.nobreak` (logo, signature, stamp); `.nobreak` avoids inside breaks; admin bar, header, entry header, `.pdfcrowd-hide`, PDF buttons, links bar and footer are hidden. There is no PDF generator in the code any more; "PDF" is the browser's print dialog. The `pdfcrowd-hide` class name survives from the retired pdfcrowd integration (1.5.0).

### Conditional logic summary

| Condition | Effect | Where |
|---|---|---|
| appointment type Consultation | letter title, no TOC, signature + optional stamp, wrapper class, `Letter` wording | `reports:18-30, 143-182` |
| house type Commercial | "Building Inspection Report" | `reports:67-69` |
| invoice has Water Test / Radon in Air | external "interpreting results" links in TOC | `reports:50-59` |
| logged in | inspector links bar | `reports:96-101` |
| stamp on, which one ny / else | NY vs CT (default) stamp image | `reports:160-168` |
| each property vital non-empty | its line on the cover page | `reports:130-135` |

## 6. The invoice template `single-hdo_invoices.php`

`hdo_draw_invoice()` on `the_content`, main query only (`invoices:3-5, 262`), then `genesis()` (`:266`).

- **Relation to appointment and report:** `InvoiceHD(get_the_ID())` (`:7`); the appointment is found by `LIKE` on `hdo_appt_invoice` and `[0]` taken (`:17-18`); from it the property and client (`:20-22`). The invoice has no link to the report; both hang off the appointment.
- **Paid state:** `$invoice->paid === true` gives "PAID" and wrapper class `hdo-paid`; otherwise "Amount Due" (`:9-15`). Strict `=== true` means a raw `'1'` (bogus-reference case) would show "Amount Due"; in practice `paid` is only ever set in the admin so ACF formats it to a real boolean. No CSS for `.hdo-paid` exists in this plugin.
- **Line 1:** `feeDescription` (one of the three fixed sentences) with `total_inspection_fee = round(fee + addToFee + feeAdjustment, 0, HALF_DOWN)` (`:32-35`).
- **Repeater `hdo_invoice_additional_line_items`** (`:37-70`): `line_type == 'discount'` and `line_discount_type == 'dollars'` adds an italic line and `(amount)` and accumulates `total_discounted` (`:47-52`); `'percent'` defers the item and its `line_percent` (`:54-58`); `line_type == 'fee'` adds the line and its amount to both the shown list and the `$fees` subtotal (`:61-67`).
- **Additional services with prices hard-coded in the template** (`:72-92`): "Water Test" becomes "Water Chemical Analysis (including Bacteria, Lead, Radon, Uranium, Arsenic)" at **465**; "Radon in Air" becomes "Radon Gas Test" at **250**; "Radon Pickup Discount" becomes "Radon Gas Pickup Discount" at **(125)**. Any other stored value is silently ignored.
- **Totals** (`:94-128`): `service_fees_total` = sum of service prices; `sub_total_fees` = base fee plus repeater fee lines (services **excluded**); percent discounts are computed on `sub_total_fees` only and rounded HALF_UP (`:104-114`); the 10% repeat-client discount likewise on `sub_total_fees` (`:116-123`); `grand_total = service_fees_total + sub_total_fees - total_discounted` (`:128`). All money is whole dollars; there is no formatting (no `$1,234`, no cents), no tax, no invoice number (the post ID and title are the only identifiers), no date paid.
- **Layout** (`:133-175`): letterhead `images/letterhead-2025.gif`; date; "Bill to:" client name and address (raw, with a stray space if `address2` is empty, `:144`); "For:" `<appointmentType> at: <property address> on <date>`; a bordered two-column block of descriptions and prices (`ul`s in parallel, so they only line up if each `li` is one line); the total line; then `$invoice->notes` (raw, unfiltered) followed by "Pay by check: Home Directions, inc." and a "Pay via Zelle" line naming a Gmail address and the treasurer (`:170-174`, added 1.11.4 to 1.11.7).
- Inline CSS (`:177-254`) fixes width 690px, hides theme chrome. A print-to-PDF shortcode is commented out (`:130-131`).
- The `have_rows` calls use `$appointment->invoiceID` rather than `get_the_ID()` (`:37-38`), so if the appointment lookup fails the repeater is read from post `null`.

## 7. AJAX handlers

**The child registers no AJAX actions.** The only two `add_action("wp_ajax_...")` lines are commented out (`ajax:4, 8`). The file instead hooks two points inside the base's `hdo_delete_appt` handler, so they inherit the base's security posture (nonce, no capability check, raw `$_REQUEST`):

| Hook | Function | Inputs | Effects |
|---|---|---|---|
| `hdo_delete_appointment` (`ajax:12-103`) | `hdo_hd_delete_appointment($failures, $appointment, $orphan_choice)` | the base's `Appointment`, re-hydrated as `AppointmentHD` (`:15`); `orphan_choice` string `'true'`/`'false'` | Always `wp_trash_post` the invoice (`:17-20`). If orphans are to be removed: count appointments referencing the broker in **any** of client/broker/attorney with `LIKE` on the raw id (`:28-53`); trash the broker if fewer than 2 (`:55-60`); same for the attorney (`:65-97`). Returns the failures array with `invoice-failed`, `broker-failed`, `attorney-failed` codes. |
| `hdo_delete_appt_client_orphan_check` (`ajax:111-141`) | `hdo_hd_check_brokers_and_attys($args, $appointment)` | | Replaces the base's client-orphan query with one that also searches `hdo_appt_broker` and `hdo_appt_attorney`, so a person who is a client on one job and a broker on another is not trashed. |

Notes: `LIKE` on an unquoted id matches `12` inside `120` (`:36, 73, 123`); when `brokerID` is null the `LIKE` value is empty and matches every appointment, so nothing is trashed, which is safe by accident; `wp_reset_postdata()` after a `fields => ids` query is a no-op.

The child's JS posts to the **base** action `hdo_compile_report` with an extra `detached_pass` parameter (`js:43`), which the base passes through untouched in `$_REQUEST` to the `hdo_compiled_report` filter (`base:ajax:180`) where the child reads it (`main:977`).

## 8. The JS and CSS

### `js/hdonline-home-directions.js` (59 lines)

One `ready` block binding `#hdo-hd-compile-report` click (`js:4`), the id the child sets on the compile button (`main:892`). Flow: `confirm('Are you sure you want to Compile the Report?')` (`:7`), show `.hdo-loading-overlay` (`:12`), read `data-action`, `data-nonce`, `data-report_id`, `data-appointment_id`, `data-detached` (`:14-23`, five `console.log`s left in), and if `data-detached == 'true'` a second `confirm('Create an Appendix to Detached Structures with subheadings?')` (`:25-29`) that sets `detached_pass` to `'true'`/`'false'` (`:32-36`). Posts to `myAjax.ajaxurl` with `action, nonce, report_id, appointment_id, detached_pass` (`:39-43`) and reloads on `status == "compiled"` (`:46-48`). `action`, `nonce`, `report_id`, `appointment_id`, `detached` are assigned without `var` (implicit globals, `:14-22`). Endpoint: only `myAjax.ajaxurl`. Hard-coded: the DOM id, the two prompt strings.

**`myAjax` collision (likely bug, unconfirmed on the live site).** The base localizes `myAjax` with six keys on handle `hdo_script` (`base:main:319-326`); the child localizes `myAjax` with only `ajaxurl` on handle `hdo_hd_script` (`main:138`). Both register on `init` at priority 10 and both enqueue on every request. Plugins load alphabetically, so the base's inline `var myAjax = {...}` prints first and the child's prints second and **replaces** it before either `ready` handler runs. If that ordering holds on the live site, `myAjax.dashboard_url`, `myAjax.view_appointment_url` and the three search nonces are `undefined` in the base JS, which would break the delete-appointment redirect, the match-incoming redirect and the 1.11.0 live search (they would post an undefined nonce). Verify by viewing page source on the dashboard and checking which `var myAjax` is last.

### `copper-leaf-hdonline-home-directions.css` (43 lines)

Enqueued front and admin under one handle (`main:121-131`). `#hdo-select-notes-child-section-bank-summary` is flexed so Bank Summary's child sections sit side by side in the selector (`css:1-8`; this confirms Bank Summary is a parent term with children). `.hdo-hd-send-to` tightens the Gravity Form 4 "send to" fields (`:10-12`). `.hdo-loading-overlay` swaps in `images/monkey-jumping.gif` (`:14-16`). View Appointment panels are set to 33% width and reordered: client 5, broker 6, attorney 7, other appointments full width (`:20-38`); the fee is shown at 2em (`:40-43`). No stylesheet exists for the report or invoice; those styles are inline in the templates (1.8.0).

## 9. History from `release-notes.txt`

Thirty-eight entries from 1.01 (2021-02-22) to 1.11.7 (2026-08-20). The arc:

- **2021-02 (1.01, 1.1):** "cowboy coded fixes from Live", always show data sheets, fix invoice link in email, die-silently on empty vitals, inspector links on the report (`release-notes.txt:158-169`).
- **2022-02 (1.1.2 to 1.3.1):** rename to "Copper Leaf:" convention (a version 1.1.1 is skipped for a "potential zombie"), PUC auto-updates, ACF autosync plus the JSON export, and a page-password problem "blocking print-to-PDF" that was "no longer replicable"; intro lines seeded into consult letters at creation (`:134-155`).
- **2022-07 to 2022-12 (1.3.2 to 1.4.1):** PAT moved into the DB, PUC 5.0 (`:118-131`).
- **2023 (1.5.0 to 1.8.1):** pdfcrowd retired for "WP PDF Generator"; PUC via CLC Functions then the Updates Handler; the engineering stamp option and ACF group (1.7.0), stamp repositioned (1.7.1), report styles moved inline for printing and the print-to-PDF shortcode removed (1.8.0), a larger stamp image (1.8.1) (`:79-115`).
- **2024-03 (1.9.0, 1.9.1):** NY stamp added, then its filename fixed (`:71-76`).
- **2024-11 (1.9.2 to 1.9.5):** the password saga: a utility to "paint" existing letters with a password, set at creation instead of compile; then commented out; then a utility to strip passwords from invoices and stop setting them; then commented out (`:53-68`).
- **2025-05 (1.9.6, 1.9.7):** new letterhead without the "Home Inspections by Professional Engineers" line; "letter" added to the invoice description (`:45-50`).
- **2026-02 to 2026-03 (1.10.0 to 1.11.2):** page passwords removed entirely; dashboard moved into wp-admin and raw AJAX searches added "(Claude)"; contacts and property "disassociation" fix "(Claude patched Classes)"; a bug audit fixing two ACF reference-key typos, a loop bug in `ContactHD`, undefined variables in the invoice template, and removing the consult intro lines (`:22-42`).
- **2026-05 (1.11.3):** fallback loader because ACF fields did not appear on a site without ACF Extended (`:18-19`).
- **2026-06 to 2026-08 (1.11.4 to 1.11.7):** four releases touching only invoice payment text and layout: payment note, treasurer's name, pay-by-check, layout tweak (`:2-15`). Git shows each as a pair of identically named commits (`git log`: "pay by check on invoices" twice, "Zelle on invoices" twice, "Claude bug audit" twice), consistent with a code commit plus a version-bump commit.

**Recurring pain:** (1) page passwords on reports and invoices, touched in 2022, 2024 (four releases) and 2026; (2) getting a PDF out (pdfcrowd, WP PDF Generator, `[wp_objects_pdf]`, PrintFriendly, `bws_pdfprint`, all now commented out or gone, `reports:21-27, 141`, `invoices:130-131`), settled on browser print with inline CSS; (3) the engineering stamp (three image files, four releases); (4) invoice wording, four releases in three months of 2026; (5) ACF loading and relationship-field shape (autosync, ACFE fallback, the disassociation fix, reference-key typos).

## 10. Smells and risks

### Fatal or data-affecting

1. **No base-plugin guard; hard-coded include path.** `classes/*:3` include the base by literal path `ABSPATH . '/wp-content/plugins/copper-leaf-hdonline/...'`; absent base means a fatal at load. Renaming either plugin folder, or a non-standard `WP_CONTENT_DIR`, breaks it.
2. **`clc_die_silently()` is undefined in both repos** (section 2). A theme swap kills reports, View Appointment and new-property creation.
3. **Hard-coded inspector user ID 5** on every new appointment (`main:601`). A rebuilt site with different user IDs assigns every appointment to the wrong user.
4. **Bogus ACF reference keys** written as `'field_' . uniqid()` for every form-created field (`main:181-646`). Posts never re-saved in the admin return raw meta from `get_field()`. A migration reading `_hdo_*` reference keys to discover field types will find garbage; it must go by field **name**.
5. **Mixed value shapes** for the same key: relationship arrays holding ints (fresh `wp_insert_post`) or strings (GF-selected, after `preg_replace`) versus ACF's arrays of strings (`main:274, 360, 445, 513, 605-626`); `hdo_appt_date` in GF format versus ACF `Ymd`; `hdo_appt_copy_to_*` and `hdo_invoice_repeat_client_discount` as GF label strings versus ACF `'1'`/`'0'`; `hdo_invoice_additional_services` as serialized array versus `''`/null (`main:574-577`); `hdo_contacts_zip` text in a number field.
6. **`preg_replace('/[^0-9,.]/', '', ...)`** on the selected client/broker/attorney/property values (`main:274, 360, 445, 513`) keeps commas and dots, so a populated value like `1,234` stays non-numeric and `get_the_title('1,234')` returns nothing; the appointment is then created with a broken link.
7. **`wp_safe_redirect` without `exit`** in both GF handlers (`main:184-187, 656-660`); Gravity Forms continues to its own confirmation, which may send a second redirect or output.
8. **Undefined `$default_description`** when `$entry['49']` is neither `consultation` nor `inspection` (`main:542-551`): the invoice description is saved as null.
9. **`hdo_hd_update_related_post_titles_on_appt_save`** calls `wp_update_post(array('ID' => $appointment->invoiceID, ...))` with no check that `invoiceID` is set (`main:1082-1087`); with a null ID `wp_update_post` falls back to the global post, so on an appointment without an invoice the wrong post may be retitled. Unconfirmed; worth a test.
10. **Lender letter placement depends on term order.** `hdo_section_bank_summary` fires at `base:ajax:176-177` with `$slug` = the parent slug and `$output` = **everything compiled so far**, and the child wraps that whole string in letterhead and signature (`main:941-966`). Since Bank Summary is a parent term (`css:1`, `reports:348`), the letter renders correctly only if Bank Summary is the **first** section in `hdo_note_sections` order; any section ordered before it is swallowed into the letter. Also, for a parent-less top-level section `$slug` is unset there, so the filter name is `hdo_section_` (base bug, harmless here).
11. **Invoice "Edit" link passes the invoice ID as `hdo_appt_id`** (`main:811`: `&hdo_appt_id='.$appointment->invoiceID`), so the base's metabox "View Appointment" link on the invoice edit screen points at the wrong post, and the base's auto-redirect that would have fixed it is skipped because the parameter is present (`base:main:1873-1908`).
12. **`myAjax` overwritten** by the child's one-key localization (`main:138`), section 8.
13. **Client internal notes shipped in public report HTML** and merely hidden with CSS (`reports:122, 316-318`, `base:main:380`). Reports are public by URL (`base:main:1861`).
14. **e2pdf shortcode attributes are malformed** (`data-set"..."` and `flatten"2"` lack `=`; `arg3=` unquoted at `main:784`) and interpolate names and addresses unescaped (`main:782-804`). Works only because e2pdf's parser is lenient. Template IDs 1 to 4 are site data.

### Missing checks and security

15. Everything the child renders is unescaped string concatenation: names, addresses, notes, ACF text, GF entry values written straight to meta (`main:220-646`), `$invoice->notes` printed raw on a public page (`invoices:171`).
16. The delete hooks inherit the base's missing capability check (`ajax:12-103`); any logged-in user with the nonce can trash invoices, brokers and attorneys.
17. The GF handlers trust every `$entry` value and hard-code 60+ field IDs of form 1 (`main:198-645`) and the four literal checkbox labels `Create a New Client`, `Create New Broker`, `Create New Attorney`, `Create New Property` (`main:198, 283, 368, 454`). Renaming a choice in the form editor silently switches every submission to "use existing" with an empty ID.
18. Hard-coded URLs and IDs: `/wp-admin/post.php?post=` in seven places (`main:678, 690, 811, 1178`, `reports:99`), `/?p=` view links (`main:811, 1179`), the uploads signature `id 12303` (`reports:151-152`), GF form ids 1, 4, 5 (`main:190, 663, 1039`), e2pdf ids 1 to 4 (`main:782-799`), three homedirections.net URLs (`reports:52-57`), the Zelle address and treasurer (`invoices:173`), service prices 465, 250, 125 (`invoices:77-88`), the three canned sentences (`main:859-861`), P.E. licence numbers (`reports:156`), and the year threshold `1980` (`main:1020`).

### PHP 8 issues

19. Undefined variables used with `.=` or read before assignment: `$broker_output`, `$atty_output` (`main:697`), `$data_sheets_list_items` (`main:813`), `$add_services_array` (`main:574`), `$default_description` (`main:551`), `$output` (`reports:75`), `$toc_list`, `$consult_pdf_button`, `$consult_class`, `$inspector_links`, `$signature` (`reports:90, 104-106, 448`), `$appointment_ids[0]` when empty (`reports:9`, `invoices:18`, `main:935`), `$this_block['attrs']['level']` on h2 blocks (`reports:40`), `$request['detached_pass']` when the base JS posts (`main:977`). Warnings on 8.x; none are TypeErrors, but `implode` on a non-array is (`main:788` is guarded).
20. Constructors returning undefined variables on a null id (`classes/appointment:17`, `classes/invoice:18`, `classes/property:18`).
21. Dynamic properties (deprecated 8.2): `AppointmentHD->includeEngineeringStamp` (`classes/appointment:47`), `InvoiceHD->invoiceID, name, feeDescription, insp_fee` (`classes/invoice:21, 39-40, 53`), `PropertyHD->name` (`classes/property:40`, already dynamic in the base).
22. `$property->yearBuilt > '1980'` compares a number field to a string (`main:1020`); numeric strings compare numerically so it works, but an empty value compares as a string and passes through.
23. `hdo_hd_single_templates` reads `$post->post_type` with `global $post` possibly null on 404s (`main:1124-1127`).

### Dead code and duplication

24. Empty `cpt.php`, `acf-cpt.php`, `note-hd.class.php`; the `init` function exists only to require the empty `cpt.php` and the `ajax` file (`main:113-117`).
25. Commented-out blocks: `gppa_query_limit` (`main:146-149`), the per-service data-sheet switch (`main:769-780`), the property-save retitle (`main:1093-1115`), the AJAX registrations (`ajax:4, 8`), the PDF buttons (`reports:21-27, 73, 86, 141`, `invoices:130-131`), debug dumps (`main:268, 355, 440, 652-654`, `classes/invoice:32`, `classes/property:33`, `reports:36`).
26. `ContactHD::setContactType` and `addContactType` are never called and have their names crossed (`classes/contact:31-51`).
27. `AppointmentHD->includeEngineeringStamp` reads the wrong post (`classes/appointment:47`); `ReportHD` is the working copy.
28. The three contact-creation blocks (`main:198-271, 283-357, 368-442`) are the same 60 lines with different field IDs; the two GF handlers duplicate report/appointment creation (`main:156-181, 518-527, 586-614`).
29. `hdo_hd_remove_suggestions_from_summary` pushes lowercase `'suggestions'` (`main:920`) but the base compares term **names** with case-sensitive `in_array` (`base:main:1548`), so it only works if the term is literally lowercase; in practice the second rule in `hdo_hd_suppress_subheads` (`main:908`) catches the "Suggestions" subhead by `strpos` anyway, so the first function is probably redundant. The comment on `main:899` says "Bank Summary" but the code targets sewage, water and termites.
30. `$invoicefee=$invoicefee;` style no-op assignments (`main:830, 835, 840`); `wp_reset_postdata()` after `fields => ids` queries.
31. `apply_filters('hdo_report_toc_array', ...)` with the result thrown away (`reports:65`).
32. `acf-export-2022-02-22.json` lacks the 2023 Report Settings group; it is a stale duplicate of two of the three PHP files.
33. `hdo_hd_process_new_appointment_local` (`main:154-190`, GF form 5) creates a report and appointment with only a title; the base's "Send to Online" path later posts notes by report id. It shares nothing with the online handler.

### Migration hazards specific to this layer

34. Everything in items 4 and 5 above (reference keys, mixed shapes, two date formats, label strings in boolean fields).
35. The **invoice's arithmetic lives in the template**, not in data: service prices and the 10% discount rate are code (`invoices:75-89, 116-123`). Historical invoices will re-render at today's prices; there is no stored total.
36. **Report identity is by title and slug**, both rewritten on appointment save (base) and invoice title likewise (`main:1080-1087`). Any external link to a report or invoice can go stale.
37. Section semantics are encoded in **term names and slugs** hard-coded here (item "CPTs and taxonomies" in section 3). A rebuild must carry the exact names `Water Supply System`, `Sewage Disposal System`, `General`, `Bank Summary`, `Summary`, `Termites`, `Sewage Disposal`, `Water Supply` and the subsection `Suggestions`, or re-map them.
38. Consultation letters are free-form Gutenberg with a hard-coded signature block that references an uploads attachment (`reports:151-152`) and licence numbers (`reports:156`); the stamp choice is per report meta.
39. `hdo_gf_entry_id` ties appointments to Gravity Forms entries (`main:649`); the GF entries hold the original submitted values (including the raw fee fields) that were never copied to ACF, for example the five service choices.
40. The `hdo_contact_types` terms `client`, `broker`, `attorney` are appended, never removed, so a contact can hold all three (`main:277, 362, 447` with append `true`); do not assume one type per contact.

## 11. Open questions (for the client or the live database)

1. Where is `clc_die_silently()` defined on the live site (theme, mu-plugin)? Is it the only site-side function the plugins rely on?
2. Is the installed base folder literally `copper-leaf-hdonline` (`classes/*:3`)?
3. User ID 5: is that Peter, and is he the only inspector? Are there any appointments with a different inspector (the ACF field allows several)?
4. Counts: appointments, reports, invoices, contacts by type (client / broker / attorney / multi-typed), properties, notes, incoming. How many appointments are `Consultation` vs `inspection`, and how many report posts have `_hdo_report_is_compiled`?
5. `hdo_note_sections` order and hierarchy: is "Bank Summary" a parent term, is it first in order, what are its children, and is there a term-order plugin providing `$term->order`?
6. Do any reports or invoices still carry a `post_password` (rows created 2022 to 2026-02)?
7. What format does Gravity Form 1 store for the date field 54 and the fee fields 63/67/68 (currency strings would zero out `hdo_add_up_fee`)? What are the five choice values of field 65, and do they equal the ACF labels `Water Test`, `Radon in Air`, `Radon Pickup Discount`?
8. What fraction of appointments, contacts, properties and invoices were ever re-saved in the admin (real `field_` reference keys) versus form-created only (`field_<uniqid>`)? This decides how much raw-versus-formatted normalisation a migration needs.
9. How many properties have `hdo_property_detached_structures` filled, and in what format (commas, "and", free text)?
10. Is the engineering stamp used on any inspection reports (the field shows there but the template ignores it), and how many reports have it on with `which_one` empty (pre-1.9.0 defaults to CT)?
11. Are the e2pdf templates 1 to 4 and Gravity Forms 1, 3, 4, 5 still present and in use? Is form 3 (base email form) dead now that the child forces form 4?
12. Is the live search on the admin dashboard actually working (item 12, the `myAjax` collision)?
13. Which PDF path does Peter really use today: browser print, a plugin, something else? Does he ever email the invoice link, and does anyone pay from it?
14. Invoice prices: are 465 / 250 / 125 current, and how often are the repeater line items and the repeat-client discount used? Are there invoices whose stored data no longer reproduces the amount originally sent?
15. Attachment 12303 (`peter-signature-pe.jpg`) and the two orphaned images: still present, still correct?
16. Are contacts, properties and appointments reachable anonymously via `/wp-json/wp/v2/hdo_contacts` and front-end URLs on the live site (base CPT flags), and is that acceptable given brokers' and attorneys' details are stored there?
