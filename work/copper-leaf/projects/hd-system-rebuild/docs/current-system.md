---
name: Home Directions current system
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: What the existing Home Directions WordPress report/letter/invoice system is and does, read from the two plugin repos on 2026-09-30; the baseline the rebuild replaces
sources: ["[doc:~/Dev/clc-plugins/hdonline]", "[doc:~/Dev/clc-plugins/hdonline-home-directions]", "[cowork 2026-09-30 checkback hop 1]"]
written_by: cowork (checkback skill, cold run, 2026-09-30 23:46 CEST)
---
# Home Directions current system

Written by a cold Cowork run from the two blobless clones the Nerd made on 2026-09-30 (HEADs 42ed6ec 2026-03-24 and 7e26a6e 2026-08-20, per `_design/STATUS.md`). Everything below is read from code; nothing is confirmed with Gordon or Peter. Where the code hints at something outside the repos (Gravity Forms field IDs, a LOCAL install, e2pdf templates), that is marked **unconfirmed**.

## In one paragraph

Two WordPress plugins. **Copper Leaf: HDOnline** (v1.7.5, generic) turns a library of standard inspection Notes into a compiled Report: an inspector opens an Appointment, ticks Notes by section, presses Compile, and the plugin writes Gutenberg blocks into the Report post. **Copper Leaf: HDOnline for Home Directions** (v1.11.7) extends it for Peter Seirup's company: intake via Gravity Forms that creates Client, Broker, Attorney, Property, Report, Invoice and Appointment posts in one go; a Consultation path that produces a letter instead of a report; an Invoice post type with fee arithmetic; letterhead, signature and engineering stamp on print; and an email form that sends report and invoice links to client, broker and attorney. Output is a web page printed to PDF by the browser. [doc:hdonline/copper-leaf-hdonline.php] [doc:hdonline-home-directions/copper-leaf-hdonline-home-directions.php]

## The two plugins

| | HDOnline (base) | HDOnline for Home Directions (extension) |
|---|---|---|
| Version / last release | 1.7.5, 2026-03-24 | 1.11.7, 2026-08-20 |
| Repo (PUC watches) | `CopperLeafCreative/copper-leaf-hdonline` | `CopperLeafCreative/copper-leaf-hdonline-home-directions` |
| Prefix | `hdo_` / `CLC_HDONLINE_` | `hdo_hd_` / `CLC_HDO_HD_` |
| Owns | CPTs, taxonomies, ACF groups, dashboard, notes selector, compile, AJAX, classes | HD ACF groups, GF intake handlers, Invoice, templates, HD filters on every base hook |
| Files | 32 (main ~1,600 lines; AJAX; 5 classes; 5 ACF PHP groups) | 35 (main ~1,200 lines; AJAX; 6 classes; 3 ACF groups; 2 single templates; `.idea/` committed) |

Both depend on the Copper Leaf Updates Handler for updates, on ACF (ACF Extended for PHP autosync, with a fallback loader added 2026-05-22 for sites without it), and on Gravity Forms. Text domain in `cpt.php` is `genesis-sample`, so the CPT code was lifted from a Genesis child theme. [doc:hdonline/release-notes.txt] [doc:hdonline-home-directions/release-notes.txt] [doc:hdonline/cpt.php]

## Data model

Six custom post types and four taxonomies, all registered in the base plugin's `cpt.php` (exported from Custom Post Type UI on 2024-03-07). [doc:hdonline/cpt.php]

| Post type | What it is | Key ACF fields (group) |
|---|---|---|
| `hdo_appointments` | The job: one inspection or consultation | `hdo_appt_date`, `_time`, `_inspector`, `_client`, `_property`, `_report`, `_notes` (Appointment Details); HD adds `_broker`, `_attorney`, `_copy_to_broker`, `_copy_to_attorney`, `_additional_contacts`, `_invoice` (HD Appointment Details) |
| `hdo_contacts` | Client, broker, attorney (taxonomy `hdo_contact_types`) | address ×6, phones ×3, fax, email, company, notes (Contact Details) |
| `hdo_properties` | The house | address ×6, notes (Property Address); HD adds `house_type`, `year_built`, `square_footage`, `water_supply`, `sewage_disposal`, `detached_structures` (HD Property Details) |
| `hdo_notes` | The library of standard findings, one per post; taxonomies `hdo_note_sections` (hierarchical, ordered) and `hdo_note_subsections` ("Global Subsections") | `hdo_note_sort_order`, `_label_before`, `_display_suggestion`, `_extensions` (repeater: question, answer type, options, extension text, abbreviation) (Note Details) |
| `hdo_reports` | The compiled report, or the consult letter; post_content is Gutenberg blocks | meta `_hdo_report_is_compiled` (0/1); `hdo_selected_note` (multi-value meta, `<note_id>|<extensions>`); HD adds `hdo_hd_include_engineering_stamp` and `_which_one` (NY or default) (HD Report Settings) |
| `hdo_invoices` | HD only in practice; one per appointment | `hdo_invoice_fee`, `_add_to_base_fee`, `_fee_adjustment`, `_repeat_client_discount`, `_additional_services`, `_additional_line_items` (repeater), `_default_fee_description`, `_paid`, `_notes` (Invoice Details) |

Relations are ACF relationship/post-object fields stored as post meta (arrays of IDs), read through small classes: `Appointment`, `Contact`, `Property`, `Note`, `Report` in the base; `AppointmentHD`, `ContactHD`, `PropertyHD`, `ReportHD` extend them and `InvoiceHD` stands alone. Reverse lookups (all appointments at a property, all for a client) are `WP_Query` meta queries with `LIKE` on the serialized array. [doc:hdonline/classes/] [doc:hdonline-home-directions/classes/] [doc:hdonline/copper-leaf-hdonline.php:442]

A seventh post type, `hdo_incoming`, is queried by the dashboard and matched into appointments but is **not registered in either repo**. It belongs to a "LOCAL" mode (`HDO_IS_LOCAL` constant, GF form 5, notes chosen offline and later "matched and inserted" into the online appointment). Whether a LOCAL install still exists anywhere is **unconfirmed**. [doc:hdonline/copper-leaf-hdonline.php:577] [doc:hdonline/copper-leaf-hdonline-ajax.inc.php:345]

## How a job flows

1. **Intake.** Inspector fills Gravity Forms form 1 ("New Appointment", now an admin page under the HDOnline menu since v1.7.0). On submit, `hdo_hd_process_new_appointment` creates or reuses Client (form field 15.1/17/73), Broker (22.1/26), Attorney (39), Property (77 or new), then inserts a Report post, an Invoice post and the Appointment post, wires them by meta, and sets the appointment type term (`consultation` or `inspection`, field 49). Invoice gets a default description by type: "Structural Consultation including site visit, diagnosis, prescription, and documentation letter." or "Home Inspection Fee" / "Building Inspection Fee" (commercial, field 58). Report and invoice titles are `<property> - <client> - <field 54>`. About 60 hard-coded GF field IDs; every ACF value is written twice (`key` and `_key` with a fake `field_<uniqid>` reference). [doc:hdonline-home-directions/copper-leaf-hdonline-home-directions.php:195-663]
2. **Dashboard.** `HDOnline → Inspector Dashboard` (admin, capability `upload_files`): New Appointment button, live search for Client and Property (AJAX), appointments for the looked-up client/property, 12 most recent appointments. [doc:hdonline/copper-leaf-hdonline.php:145-235,577-666]
3. **View Appointment.** Appointment, Property (HD adds house facts), Client, Broker and Attorney cards, "You've been to this Property before", additional contacts, and a Files card with Water and Radon Data Sheets rendered by the **e2pdf** plugin (shortcodes `[e2pdf-download id="1"|"2"]`, arguments passed inline). Action buttons: Select Notes, Compile Report; after compile: Edit Report, View Report, Email Report, DE-compile, Delete Appointment. For a Consultation the notes UI is hidden and the buttons read Edit/View/Email **Letter**. [doc:hdonline/copper-leaf-hdonline.php:829-1116] [doc:hdonline-home-directions/copper-leaf-hdonline-home-directions.php:761-824,1172-1195]
4. **Select Notes.** A table of contents of Sections (parent terms, ordered) and a checklist of every published Note, grouped by section and global subsection. Ticking a note (AJAX `hdo_select_note`) appends `note_id|exts` to the report's `hdo_selected_note` meta; notes with extensions pop a small question form whose answers become the `exts` string. [doc:hdonline/copper-leaf-hdonline.php:1227-1480] [doc:hdonline/copper-leaf-hdonline-ajax.inc.php:33-129]
5. **Compile.** AJAX `hdo_compile_report` walks the section hierarchy, emits an `h2` per parent section, the selected notes as Gutenberg paragraphs (label-before, text, extension answers substituted), "general information" per section from the appointment, and runs a filter per section (`hdo_section_<slug>`). HD hooks `hdo_section_bank_summary` to prepend letterhead (`images/letterhead-2025.gif`), a client/property/date header and Peter's signature with a page break, then an "Appendix to Detached Structures" with Observations/Suggestions subheads per detached structure. The result is written into `post_content` and `_hdo_report_is_compiled = 1`. Decompile flips the flag so notes can be re-picked; the content stays until recompiled. [doc:hdonline/copper-leaf-hdonline-ajax.inc.php:130-254] [doc:hdonline-home-directions/copper-leaf-hdonline-home-directions.php:929-1003]
6. **Consult letter.** No compile. The Report post is created with a "consult shell" (intro lines set at creation since v1.3.0) and Peter edits it in the block editor. [doc:hdonline-home-directions/release-notes.txt]
7. **Render and print.** `single-hdo_reports.php` and `single-hdo_invoices.php` in the HD plugin override the theme. The report template prints a TOC, the content, signature image (`/wp-content/uploads/2020/11/peter-signature-pe.jpg`), optional engineering stamp (default or NY), and inline CSS with `@media print` rules; the PDF is whatever the browser prints. pdfcrowd was retired 2023-05 for WP PDF Generator, then the PDF shortcode was removed 2023-11; the pdfcrowd class names remain in the CSS. Page passwords on reports and invoices were removed in 2026-02 (v1.6.0 / v1.10.0), so the URLs are public. [doc:hdonline-home-directions/single-hdo_reports.php] [doc:hdonline-home-directions/copper-leaf-hdonline-home-directions.php:1121-1166]
8. **Invoice.** `InvoiceHD` totals base fee + add-to-fee + adjustment, repeat-client discount, additional services and line items (fixed or percent), shows PAID or "Amount Due", and the 2026 releases added "Pay by check: Home Directions, inc." and "Pay via Zelle: homedirectionsinc@gmail.com | Maria Pia Seirup, Treasurer". Payment is recorded by hand: the `hdo_invoice_paid` checkbox. [doc:hdonline-home-directions/single-hdo_invoices.php] [doc:hdonline-home-directions/classes/invoice-hd.class.php]
9. **Email.** Gravity Forms form 4 (HD) or 3 (base), pre-filled with client name, property, report link, invoice link, client email, broker and attorney (with "Send to Broker/Attorney" pre-ticked when the appointment says copy). Delivery is GF's notifications; the plugin sends no mail itself. [doc:hdonline/copper-leaf-hdonline.php:1117-1168] [doc:hdonline-home-directions/copper-leaf-hdonline-home-directions.php:1032-1064]
10. **Delete.** AJAX `hdo_delete_appt` with an "orphan choice" for what to do with the linked report, invoice, contacts and property. [doc:hdonline-home-directions/copper-leaf-hdonline-hd-ajax.inc.php:12-110]

## Outside the repos (dependencies the rebuild must account for)

- Gravity Forms with forms 1 (intake), 3 and 4 (email), 5 (LOCAL intake); field IDs are hard-coded in PHP. GP Populate Anything is referenced in a commented filter. **Unconfirmed** which add-ons are licensed.
- ACF Pro and ACF Extended; `acf-export-2022-02-22.json` in each repo is the 2022 snapshot, the PHP groups are current.
- e2pdf for the Water and Radon Data Sheets (templates 1 and 2 live in the site database, not in git).
- Copper Leaf Updates Handler and Plugin Update Checker; GitHub org `CopperLeafCreative` (the Sancho repos moved to `gordonium` tonight; these two did not).
- The theme (Genesis child, by the text domain) supplies everything not in the plugin: login, admin, the front page.
- A Local install (`HDO_IS_LOCAL`) for offline note selection: **unconfirmed** whether it still exists.
- Staging: `hdonline-sancho.sitedistrict.com` was requested but the SSH alias is not set up (Nerd, 2026-09-30 22:48).

## What the code says about the pain (evidence, not diagnosis)

- Every relation is a serialized-array meta; reverse lookups are `LIKE` queries on serialized data. [doc:hdonline/copper-leaf-hdonline.php:442]
- Intake is ~470 lines of hard-coded GF field IDs writing meta pairs by hand; the form and the code must change together. [doc:hdonline-home-directions/copper-leaf-hdonline-home-directions.php:195-663]
- The "bug audit" of 2026-03-04 (v1.7.3 / v1.11.2) fixed a CPT slug typo that broke the notes selector, nonce checks that were disabled, unsanitized `$_POST`, leaked loop variables and undefined returns, all in code live since 2021. [doc:hdonline/release-notes.txt] [doc:hdonline-home-directions/release-notes.txt]
- Compile builds Gutenberg markup by string concatenation and stores the result as post content; there is no separation between report data and report rendering, so a re-render after a template change means decompile and recompile.
- PDF has been three mechanisms in five years (pdfcrowd, WP PDF Generator, browser print); print CSS carries all three. [doc:hdonline-home-directions/single-hdo_reports.php:398-448]
- Reports and invoices are public URLs since 2026-02 (passwords removed by request); anyone with the link can read them.
- Hygiene: `.idea/` is committed in the HD repo; `genesis-sample` text domain; two ACF JSON exports from 2022 that no longer match the PHP groups.

## Open threads for the Phase 1 spec
- What the 2026-09-29 meeting asked for versus what this system does; the summary is in `work/copper-leaf/clients/home-directions/transcripts/` [rec_8d15ed467e 2026-09-29].
- Which legacy data must survive: notes library (the real asset), contacts, properties, past reports and invoices as PDFs or as data.
- Whether a LOCAL/offline mode is still wanted.
- Who edits the Notes library today and how often (unconfirmed).

## History of corrections
(none yet)
