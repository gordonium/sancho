---
name: Survey · hdonline base plugin
type: doc
lobe: work
description: Read-only code survey of the hdonline base plugin (v1.7.5, HEAD 42ed6ec) by a Sancho subagent, every claim cited file:line; basis for current-system.md
sources: ["[doc:~/Dev/clc-plugins/hdonline]", "[derived: sancho subagent 2026-09-30]"]
---
# Survey: hdonline (Copper Leaf: HDOnline) base plugin

Repo: `/Users/gordonium/Dev/clc-plugins/hdonline` (branch `main`, HEAD `42ed6ec` "admin-side form sending bugfix"). Read-only survey, 2026-09-30. Nothing was changed.

File aliases used below:

- `main` = `copper-leaf-hdonline.php` (1,967 lines)
- `ajax` = `copper-leaf-hdonline-ajax.inc.php` (601 lines)
- `cpt` = `cpt.php` (375 lines)
- `js` = `js/hdonline.js` (667 lines)
- `acf/<key>.php` = the five ACF PHP field-group files
- `child` = the sibling repo `hdonline-home-directions` (only consulted to confirm which base hooks are actually used; it is not surveyed here)

## 0. What it is, in one paragraph

HDOnline is a WordPress plugin that turns the site into a small back-office for a home inspector. An **Appointment** ties together a **Client** (a Contact), a **Property**, and a **Report**. The inspector opens the appointment, ticks boxes in a big "Select Notes" overlay (a library of standard paragraphs, organised by Section and Global Subsection, some with follow-up questions that change the wording), and presses **Compile Report**. Compile takes the ticked notes, orders them by section, wraps them as Gutenberg blocks, and writes them into the Report post, which then gets edited in the normal WordPress editor, viewed at `/?p=<id>`, printed, or emailed via a Gravity Form. There is a second "LOCAL" mode (a copy of the site on a laptop with no internet) where notes are ticked offline and later posted to the online site as an **Incoming** record, which the inspector matches to the right appointment. The plugin is the generic base; a child plugin (`hdonline-home-directions`) adds invoices, brokers, engineering-stamp letters and Home Directions specific layout on top via the filters listed in section 8.

## 1. Plugin header, version, constants, prefixes, dependencies, hooks

### Header and version

- Plugin Name "Copper Leaf: HDOnline", Description "Report creation from a library of standard Notes.", **Version 1.7.5**, Author "Copper Leaf Creative, Gordon Seirup", GPLv2: `main:3-10`.
- No version constant anywhere in the repo; the header is the only version. `release-notes.txt:2` agrees (1.7.5, 20260324).
- No `Requires PHP`, `Requires at least`, or text domain in the header. Text domains used ad hoc: `'my-text-domain'` (`main:63`), `'example'` (`main:1612`), `'genesis-sample'` throughout `cpt`.
- Direct-access guard is non-standard: checks `function_exists('add_action')` and calls `_e()` (`main:28-31`) rather than `ABSPATH`. `cpt`, `ajax`, the five `acf/*.php`, the five class files and `puc.php` have **no** direct-access guard at all.

### Constants

- `CLC_HDONLINE_PLUGIN_PATH` = `plugin_dir_path(__FILE__)` and `CLC_HDONLINE_PLUGIN_URL` = `plugin_dir_url(__FILE__)`: `main:35-36`.
- `HDO_IS_LOCAL` is **read** but never defined in this repo (`main:295, 579, 812, 861, 1009`). It is expected to be defined elsewhere (wp-config or theme) on the offline "LOCAL" install.
- `CLC_UPDATES_CHECKER_PLUGIN_PATH` is read (`main:41`, `puc.php:3`); provided by the Copper Leaf Updates Handler plugin.

### Prefixes

Mixed and inconsistent: `hdo_` (most functions, meta, nonces), `clc_hdo_` (enqueue functions), `copper_leaf_hdonline_` (ACFE load/save points), `cptui_register_hdo_` (CPT/tax registration), `make_hdo_` (render functions), `origin_` (heading ID filter copied from a blog post, `main:1831-1843`), and three unprefixed globals: `us_states()` (`main:343`), class names `Appointment`, `Contact`, `Note`, `Property`, `Report` (`classes/*.php`), and the JS global `myAjax` (`main:319`). Meta keys are `hdo_*` and `_hdo_*`.

### Dependencies

| Dependency | How detected | Where |
|---|---|---|
| Copper Leaf Updates Handler (bundles Plugin Update Checker v5) | `defined('CLC_UPDATES_CHECKER_PLUGIN_PATH')`; otherwise an admin notice on the Plugins screen | `main:41-66`, `puc.php:3` |
| PUC | `PucFactory::buildUpdateChecker('https://github.com/CopperLeafCreative/copper-leaf-hdonline', ...)`, slug `copper-leaf-hdonline`, release assets enabled | `puc.php:7-11`, `main:45` |
| GitHub PAT | read from option `options_clcs_github_personal_access_token` and passed to `setAuthentication()`; value lives in the DB, not the repo | `main:48-51` |
| ACF Pro + ACF Extended | `acfe/settings/php_load` and `acfe/settings/php_save/key=...` filters; field groups loaded from `acf/` via `acf_add_local_field_group` | `main:72-94`, `acf/*.php:3-5` |
| Gravity Forms | `class_exists('GFFormDisplay')` / `class_exists('GFAPI')`, `gravity_form()`, `GFAPI::get_form()`, `gform_us_states` filter, `[gravityforms]` shortcode | `main:294-311, 342-350, 814-823, 1159` |
| Theme (Genesis Sample) | text domain `genesis-sample` in `cpt`; `.site-header` hidden for logged-out users (`main:1957-1967`); `clc_die_silently()` is called 20+ times but **defined nowhere in this repo or the child** (see 9) | `main:360-380, 883-897` |
| jQuery | script dependency | `main:318, 328` |

### Hooks registered (actions, filters, shortcodes)

| Hook | Callback | Where |
|---|---|---|
| `admin_notices` | `hdonline_clc_functions_required` (only when Updates Handler absent) | `main:55` |
| `acfe/settings/php_load` | `copper_leaf_hdonline_php_load_point` (adds `acf/` with a doubled slash: `plugin_dir_path(...) . '/acf'`) | `main:72-81` |
| `acfe/settings/php_save/key=<5 group keys>` | `copper_leaf_hdonline_acfe_php_save_point` | `main:85-94` |
| `init` | `clc_hdo_acf_cpt_configs` (which only `require_once`s the AJAX file) | `main:101-105` |
| `init` | `cptui_register_hdo_cpts`, `cptui_register_hdo_taxes` | `cpt:236, 375` |
| `init` | `hdo_script_enqueuer` (registers + localizes + enqueues `hdo_script` on every request, front and admin) | `main:316-330` |
| `admin_menu` | `hdo_register_admin_pages` | `main:145` |
| `wp_enqueue_scripts` (prio 50) | `clc_hdo_enqueue_stylesheet` | `main:237` |
| `admin_enqueue_scripts` | `clc_hdo_admin_style`, `hdo_admin_page_styles` | `main:245, 258` |
| `gform_us_states` | `us_states` (state code as key) | `main:342` |
| `add_meta_boxes` (prio 30) | `hdo_add_post_meta_boxes` | `main:1605` |
| `admin_footer` | `hdo_add_select_notes_to_edit_report` (prints the whole notes selector on **every** admin page), `hdo_add_loading_gif_overlay_div` | `main:1656, 1849` |
| `wp_footer` | `hdo_add_loading_gif_overlay_div` | `main:1848` |
| `acf/save_post` | `hdo_update_related_post_titles_on_appt_save` | `main:1715` |
| `render_block` | `origin_add_id_to_heading_block` | `main:1831` |
| `wp` | `hdo_require_login` | `main:1858` |
| `admin_head` (prio 30) | `hdo_catch_edit_report_url` | `main:1873` |
| `template_redirect` | `hdo_redirect_appointments`, `hdo_redirect_old_pages` | `main:1913, 1923` |
| `wp_head` | `hdo_hide_menu_styles` | `main:1957` |
| `wp_ajax_*` / `wp_ajax_nopriv_*` (10 actions) | see section 5 | `ajax:4-30` |
| Shortcodes `hdo_inspector_dashboard`, `hdo_new_appointment_form`, `hdo_view_appointment_view`, `hdo_incoming_handler` | render functions | `main:667, 826, 1001, 1710` |

No activation, deactivation or uninstall hooks. No cron. No REST routes. No custom tables.

## 2. Data model

### Custom post types (`cpt:3-236`)

All six share: `public`, `publicly_queryable`, `show_ui`, `show_in_rest`, `show_in_menu`, `show_in_nav_menus` all true; `has_archive` false; `exclude_from_search` false; `capability_type` `post`; `map_meta_cap` true; `hierarchical` false; `rest_namespace wp/v2`; `with_front` true.

| Slug | Labels | Rewrite slug | Supports | Extra | Where |
|---|---|---|---|---|---|
| `hdo_notes` | Notes / Note | `hdo_notes` | title, editor, revisions | icon `dashicons-forms` | `cpt:9-41` |
| `hdo_contacts` | Contacts / Contact | `hdo_contacts` | title, revisions | taxonomies `hdo_contact_types`; icon `dashicons-id` | `cpt:47-80` |
| `hdo_properties` | Properties / Property | `hdo_properties` | title, thumbnail, revisions | icon `dashicons-location-alt` | `cpt:86-118` |
| `hdo_reports` | Reports / Report | `reports` | title, editor, thumbnail, revisions | icon `dashicons-media-spreadsheet` | `cpt:124-156` |
| `hdo_appointments` | Appointments / Appointment | `hdo_appointments` | title, revisions | icon `dashicons-calendar-alt` | `cpt:162-194` |
| `hdo_invoices` | Invoices / Invoice | `invoices` | title, revisions | icon `dashicons-money-alt` | `cpt:200-232` |

**`hdo_incoming`** is queried (`main:628`), inserted (`main:1687`), read (`ajax:353`) and deleted (`ajax:370, 396`) but is **not registered in this repo or the child**. It must be registered on the live site by CPT UI (DB) or the theme; unconfirmed.

Note that every CPT is `public` + `publicly_queryable` + `show_in_rest`, so Contacts, Properties, Appointments, Reports and Invoices all have public front-end URLs and are exposed on `/wp-json/wp/v2/` to anyone the REST permission model allows (published posts are readable by anonymous users). Front-end access is only gated by `hdo_require_login` (`main:1859-1870`), which explicitly **exempts** `hdo_reports` and `hdo_invoices` (they are meant to be client-viewable without login since 1.6.0 removed page passwords, `release-notes.txt:43`).

### Taxonomies (`cpt:241-375`)

| Slug | Labels | Object type | Hierarchical | Where |
|---|---|---|---|---|
| `hdo_note_subsections` | Global Subsections | `hdo_notes` | no | `cpt:247-274` |
| `hdo_note_sections` | Sections | `hdo_notes` | **yes** (parent/child sections) | `cpt:280-307` |
| `hdo_contact_types` | Contact Types | `hdo_contacts` | no | `cpt:313-340` |
| `hdo_appointment_types` | Appointment Types | `hdo_appointments` | no | `cpt:346-373` |

All are public, `show_in_rest`, `show_admin_column` false, `sort` false. Term meaning in code: `hdo_note_sections` term `description` is the section's "General Information" block inserted at compile (`main:1484-1491`); term `->order` property (set by a term-ordering plugin, not by this code) drives section order (`main:1211-1216`); `hdo_appointment_types` term name `Consultation` changes "View Report" to "View Letter" (`main:524-528`).

### ACF field groups (five, identical in `acf/*.php` and `acf-export-2022-02-22.json`; all `acfe_autosync => php`)

**group_5f4e9df8137f3 "Note Details"**, location `post_type == hdo_notes` (`acf/group_5f4e9df8137f3.php:5-283`)

| Field name | Key | Type | Notes |
|---|---|---|---|
| `hdo_note_sort_order` | field_5f4e9e00ac0c0 | text | used as `meta_value_num` sort key (`main:1264`) |
| `hdo_note_extensions` | field_5f4fdc28e699f | repeater | the follow-up questions form |
| ↳ `ext_question` | field_5f4fdd08e69a1 | text, required | |
| ↳ `ext_answer_type` | field_5f4fdd1ce69a2 | radio: `radio` "Select One", `checkbox` "Select Multiple" | conditional on `ext_options` refers to value `text` which is not a choice (`:97-105`) |
| ↳ `ext_options` | field_5f4fdd54e69a3 | repeater, required | |
| ↳↳ `ext_displayed_option` | field_5f4fdd65e69a4 | text, required | |
| ↳↳ `ext_abbrv` | field_5f4fdd76e69a5 | text, required; instruction says "not actually used anywhere" but it **is** the value posted and concatenated (`main:1415`, `js:105-133`) | |
| `hdo_note_extensions_text` | field_5f593ddea5e19 | repeater | maps concatenated abbreviations to replacement text |
| ↳ `concatenated_abbreviations` | field_5f593deea5e1a | text | compared with `==` to the posted `exts` string (`ajax:92`, `main:1532`) |
| ↳ `extension_text` | field_5f593e06a5e1b | textarea (wpautop) | |
| `hdo_note_label_before` | field_5f581c65ba275 | text | sub-heading shown above the checkbox in the selector (`main:1379-1381`) |
| `hdo_note_display_suggestion` | field_5f4ff8d96693a | textarea (br) | "Consider:" lightbulb hint (`main:1383-1389`) |

**group_5f4fe18c40739 "Appointment Details"**, location `post_type == hdo_appointments` (`acf/group_5f4fe18c40739.php`)

| Field name | Key | Type | Notes |
|---|---|---|---|
| `hdo_appt_date` | field_5f4fe4489b2d4 | date_picker, required, return `Y-m-d` | sort key `meta_value_num` on a `Ymd` string (`main:456-458`) |
| `hdo_appt_time` | field_5f4fe4659b2d5 | time_picker, return `H:i:s` | displayed raw (`main:875`) |
| `hdo_appt_inspector` | field_5f4fe4b29b2d7 | **user**, required, `multiple => 1`, return object | code takes the first only (`classes/appointment.class.php:42-51`) |
| `hdo_appt_notes` | field_5f5152e729950 | textarea | |
| `hdo_appt_client` | field_5f4fe992a08b6 | relationship to `hdo_contacts`, max 1, return id | |
| `hdo_appt_property` | field_5f5120af30e0c | relationship to `hdo_properties`, max 1, return id | |
| `hdo_appt_report` | field_5f4fe8dcf8080 | relationship to `hdo_reports`, max 1, return id | |

Fields the base code reads on appointments that are **defined only in the child** (`hdonline-home-directions/acf/group_5f4ffb1a73e43.php`): `hdo_appt_additional_contacts` (relationship to `hdo_contacts`, unlimited, return object; read at `classes/appointment.class.php:71`), `hdo_appt_invoice` (`main:1886`), `hdo_appt_broker`. `hdo_appt_contact` (`main:1889`) is defined nowhere.

**group_5f4fea07dc5da "Contact Details"**, location `post_type == hdo_contacts` (`acf/group_5f4fea07dc5da.php`): `hdo_contacts_company` (text), `hdo_contacts_address`, `hdo_contacts_address_2`, `hdo_contacts_city` (text), `hdo_contacts_state` (select of 51 two-letter codes, `:98-150`), `hdo_contacts_zip` (**number**, so leading-zero ZIPs and ZIP+4 cannot be stored), `hdo_contacts_country` (text, default `USA`), `hdo_contacts_phone_home` / `_work` / `_cell` / `hdo_contacts_fax` (text), `hdo_contacts_email` (email), `hdo_contacts_notes` (textarea). Name is the post title.

**group_5f4fe1dbe8af3 "Property Address"**, location `post_type == hdo_properties` (`acf/group_5f4fe1dbe8af3.php`): `hdo_property_address`, `hdo_property_address_2`, `hdo_property_city`, `hdo_property_state` (free text, unlike contacts), `hdo_property_zip` (text), `hdo_property_notes` (text). Title is the display name (`classes/property.class.php:38`).

**group_5f4fe5600ce37 "Invoice Details"**, location `post_type == hdo_invoices`, hides `the_content` (`acf/group_5f4fe5600ce37.php`): `hdo_invoice_default_fee_description` (text), `hdo_invoice_fee` (number, required), `hdo_invoice_add_to_base_fee`, `hdo_invoice_fee_adjustment` (number), `hdo_invoice_paid`, `hdo_invoice_repeat_client_discount` (true_false), `hdo_invoice_additional_services` (checkbox: Water Test, Radon in Air, Radon Pickup Discount; return label), `hdo_invoice_additional_line_items` (repeater: `line_description` text, `line_type` radio fee/discount, `line_discount_type` radio percent/dollars, `line_amount` number, `line_percent` number), `hdo_invoice_notes` (textarea). **Nothing in the base plugin reads any invoice field**; the group is defined here but consumed only by the child.

### Post meta read or written outside ACF

| Key | On | Written | Read | Shape |
|---|---|---|---|---|
| `hdo_selected_note` | hdo_reports | `add_post_meta` (`ajax:45, 359`), `update_post_meta` with prev value (`ajax:77`), `delete_post_meta` with value (`ajax:105`) | `get_post_meta($id, 'hdo_selected_note')` non-single (`main:1122, 1467`, `ajax:139`) | **multiple rows per report**, each a string `"<note_id>|<exts>"`, e.g. `"123|"` or `"123|ab"` |
| `_hdo_report_is_compiled` | hdo_reports | `update_post_meta(..., '1')` (`ajax:192`), `delete_post_meta` (`ajax:234`) | `get_post_meta(..., non-single)[0]` (`main:523, 985, 1034`) | string `'1'` or absent |
| `hdo_incoming_selected_notes` | hdo_incoming | `add_post_meta` (`main:1693`) | `get_post_meta(..., true)` (`ajax:353`) | dash-joined string of `"<note_id>|<exts>"` values |
| `hdo_local_report_id` | hdo_incoming | `add_post_meta` (`main:1695`) | never read | int |
| `hdo_gf_entry_id` | hdo_appointments | never written here (child writes it) | `classes/appointment.class.php:67` | int |
| `hdo_appt_client`, `hdo_appt_property`, `hdo_appt_report`, `hdo_appt_invoice` | hdo_appointments | via ACF | raw `LIKE` meta queries against the serialized array (`main:453-481`, `ajax:274-306`) | ACF relationship = serialized PHP array of ID strings |

### Options, transients, roles

- Options: only `options_clcs_github_personal_access_token` is read (`main:48`); it belongs to the Updates Handler's ACF options page. Nothing written.
- Transients: none. Object cache: none.
- Roles/capabilities: no custom roles. Every gate is `upload_files` (Author and above) (`main:152-185, 200, 212, 224, 1865, 1927`, `ajax:429, 490, 568`).

## 3. Entities and relationships

```
Contact (hdo_contacts)  <--hdo_appt_client (max 1)---------  Appointment (hdo_appointments)
Contact                 <--hdo_appt_additional_contacts (n)-  Appointment      [child-defined field]
Property (hdo_properties) <--hdo_appt_property (max 1)------  Appointment
Report (hdo_reports)    <--hdo_appt_report (max 1)----------  Appointment
Invoice (hdo_invoices)  <--hdo_appt_invoice (max 1)---------  Appointment      [child-defined field]
Note (hdo_notes) --terms--> Section (hdo_note_sections, hierarchical), Global Subsection (hdo_note_subsections)
Report --meta hdo_selected_note (many rows)--> "note_id|exts"
Incoming (hdo_incoming) --meta hdo_incoming_selected_notes--> "note_id|exts-note_id|exts-..."
```

- **The Appointment is the hub.** All links are ACF relationship fields stored **on the appointment** as serialized arrays. Nothing points the other way: to find the appointment(s) for a report, property or contact the code runs `hdo_get_appointment_ids_from_meta()` (`main:442-497`), a `LIKE` search over `wp_postmeta` with three alternative serializations (`"123"`, `i:123;`, plain `123`). `post_parent` is never used.
- **Ownership:** appointments and reports get their titles and slugs rewritten from `Property title - Client title - Date` on every ACF save of an appointment (`main:1715-1743`). Reports are otherwise ordinary posts. Contacts and properties are shared across appointments and are only trashed at delete time if fewer than two appointments reference them ("orphan" logic, `ajax:271-320`).
- **Lifecycle/status values.** There is no status field. The only state is `_hdo_report_is_compiled` = `'1'` on the report (`ajax:192`): absent means "selecting notes", present means "compiled, edit in Gutenberg". Decompile empties `post_content` and deletes the flag (`ajax:227-234`). Delete uses `wp_trash_post` for appointment/report/client/property (`ajax:266-323`) but `wp_delete_post(..., false)` for incoming (`ajax:370, 396`), which still trashes because `$force_delete` is false. All posts use `post_status = publish`; the incoming handler inserts as `publish` (`main:1686`).
- **Appointment type** comes from the `hdo_appointment_types` term; `Consultation` is special-cased (`main:524`).
- **Inspector** is a WP user, first of a multi-user field (`classes/appointment.class.php:42-51`).
- **Class model.** `Appointment`, `Contact`, `Property`, `Note`, `Report` are read-only value objects hydrated in the constructor by a `WP_Query` on `p => $id` (`classes/*.class.php`). `Report` is deliberately empty, existing only so the child can `extends` it (`classes/report.class.php:3-15`, `release-notes.txt:56`). Each class declares some properties but assigns others dynamically (`$this->name`, `$this->company`, `$this->text`, `$this->appointmentType`, `$this->gform_entry_id`, `$this->additionalContactsIDs`), which is deprecated in PHP 8.2.

## 4. Admin pages, front-end pages, templates, redirects

### Admin pages (`main:145-232`)

| Slug / URL | Menu | Cap | Renders | Actions offered |
|---|---|---|---|---|
| `admin.php?page=hdo-dashboard` | top-level "HDOnline", position 3, `dashicons-clipboard`; submenu "Inspector Dashboard" | `upload_files` | `make_hdo_inspector_dashboard()` (`main:577-666`) | "New Appointment" link; incoming-match forms (online only); live search boxes (`main:547-573`); lookup results for `?hdo_lookup_id=&hdo_lookup_type=Client|Property` (`main:763-806`); "Recent Appointments" list of 12 (`main:697-724`). LOCAL mode instead lists last 20 appointments each with View / Send to Online / Delete (`main:579-624`). |
| `admin.php?page=hdo-view-appointment&hdo_appt_id=N` | hidden (parent `null`) | `upload_files` | `make_hdo_view_appointment_view()` (`main:829-1000`) | Title; action buttons (`main:1005-1113`): before compile **Select Notes** + **Compile Report**; after compile **Edit Report** (post.php), **View Report** (`/?p=`), **Email Report** (opens GF form 3 overlay), **DE-compile Report**; always **Delete Appointment**. Panels: Appointment (date, time, inspector, notes, Edit link), Property, Client, "You've been to this Property before", Additional Contacts. Appends the full notes selector overlay when not compiled (`main:985-997`). |
| `admin.php?page=hdo-new-appointment` | submenu "New Appointment" | `upload_files` | `make_hdo_new_appointment_form()` (`main:810-825`) | Gravity Form **id 1** (or **5** when `HDO_IS_LOCAL`) rendered with `gravity_form()`; the GF submission handler that actually creates the posts lives in the child, not here. |

Hook suffixes used for CSS gating: `toplevel_page_hdo-dashboard`, `admin_page_hdo-view-appointment`, `hdonline_page_hdo-new-appointment` (`main:264-268`).

`hdo_admin_page_url($page, $args)` (`main:115-136`) is the URL helper; still, `/wp-admin/post.php?post=...&action=edit` is hard-coded in five places (`main:877, 889, 935, 953, 1066`).

### Post editor additions

- Sidebar metabox "HDOnline Actions:" on `hdo_reports`, `hdo_invoices`, `hdo_properties`, `hdo_appointments` (`main:1605-1647`): "View Appointment" link, plus "Add a Note" opener on reports. Filter `hdo_report_actions_metabox_filter`, action `hdo_report_actions_metabox`.
- The full notes-selector overlay is echoed into `admin_footer` on every admin screen (`main:1651-1656`); it is only meaningful on the report edit screen (mode `add`).
- `hdo_catch_edit_report_url` (`main:1873-1908`): on the edit screen for reports/invoices/properties without `hdo_appt_id`, finds the first linked appointment and redirects to the same URL plus `&hdo_appt_id=`. It runs on `admin_head`, after output has begun, so `wp_safe_redirect` may fail with headers-already-sent depending on buffering.

### Front-end pages, shortcodes, redirects

- Shortcodes `[hdo_inspector_dashboard]`, `[hdo_new_appointment_form]`, `[hdo_view_appointment_view]` still exist (`main:667, 826, 1001`) for the pre-1.7.0 front-end pages; `hdo_redirect_old_pages` (`main:1923-1953`) now sends the front page, `/view-appointment/` and `/new-appointment/` to the admin equivalents for users with `upload_files`.
- `[hdo_incoming_handler]` (`main:1672-1710`) is the receiving end of "Send to Online": expected on the page at `https://reports.homedirections.net/incoming/` (`main:1129`).
- Single `hdo_appointments` URLs redirect to the admin View Appointment page (`main:1913-1919`).
- `hdo_require_login` (`main:1858-1870`): every front-end request except `hdo_reports`, `hdo_invoices` and page ID **11874** redirects non-`upload_files` visitors to login. So reports and invoices are public by URL.
- `hdo_hide_menu_styles` hides `.site-header` for logged-out visitors (`main:1957-1967`).
- Report rendering itself uses the theme's single template; the base plugin ships no templates (the child ships `single-hdo_reports.php` and `single-hdo_invoices.php`). The base contributes `render_block` heading IDs for a TOC (`main:1831-1843`) and JS handlers for `#hdo-toc-toggle` / `#hdo-report-the-toc` (`js:448-458`), whose markup is produced by the child.

## 5. AJAX actions (`ajax`)

All are registered for logged-in users; `nopriv` variants print "You can't do that without logging in." and die (`ajax:4-18`). Unless noted, the handler checks a nonce but **no capability**, reads `$_REQUEST` **unsanitized**, and echoes hand-built JSON only when `HTTP_X_REQUESTED_WITH` is `xmlhttprequest` (so a non-XHR request performs the write and returns an empty body).

| Action | Nonce | Cap | Inputs | Effect | Output |
|---|---|---|---|---|---|
| `hdo_select_note` (`ajax:33-127`) | `hdo_select_note` | none | `mode` (`select`/`add`), `report_id`, `note_id`, `old_value`, `exts`, `has_exts` | **select mode:** old_value `none`/empty -> `add_post_meta(report, hdo_selected_note, "note|exts")`; old_value set and `exts` given -> `update_post_meta` replacing the old row; old_value set and no `exts` -> `delete_post_meta` of that row. **add mode:** no write; returns the note text (plain or matching extension row) run through `hdo_guten_note()` for clipboard paste. | `{status: saved|savefailed|updated|updatefailed|deleted|deletefailed|addplain|addext|add, val}` |
| `hdo_add_note` (`ajax:22`) | n/a | n/a | n/a | **Hooked to a function that does not exist.** JS never calls it. A crafted request would throw a TypeError on PHP 8. | none |
| `hdo_compile_report` (`ajax:130-215`) | `hdo_compile_report` | none | `report_id`, `appointment_id` (both `intval`) | Builds the report body (section 6) and `wp_update_post` into `post_content`; sets `_hdo_report_is_compiled = '1'`; instantiates **`AppointmentHD`** (a child class) to rebuild the action buttons. | `{status: compiled|metafailed|updatefailed, val: buttons html}` |
| `hdo_decompile_report` (`ajax:219-251`) | `hdo_decompile_report` | none | `report_id` (raw) | Sets `post_content = ''`, deletes `_hdo_report_is_compiled`. All Gutenberg edits are lost; selected-note rows are kept. | `{status: decompiled|metadeletefailed|deletefailed}` |
| `hdo_delete_appt` (`ajax:255-341`) | `hdo_delete_appt` | none | `appointment_id` (raw), `orphan_choice` (`'true'`/`'false'`), `is_local` | Filter `hdo_delete_appointment` (child trashes invoice); trashes report; if orphan_choice, trashes client and property when fewer than 2 appointments reference each; trashes the appointment if no failures or if `is_local == '1'` (the JS sends `true`, which never equals `'1'`). | `{status: deleted|failed|partialfail, val}` |
| `hdo_match_incoming` (`ajax:345-386`) | `hdo_match_incoming` | none | `incoming_id`, `appointment_id` (raw) | Splits `hdo_incoming_selected_notes` on `-` and `add_post_meta`s each as `hdo_selected_note` on the appointment's report (no duplicate check); trashes the incoming post. | `{status: success|deletefailure}` |
| `hdo_delete_incoming` (`ajax:390-411`) | `hdo_delete_incoming` | none | `incoming_id` (`intval`) | Trashes the incoming post. | `{status: deleted|deletefailure}` |
| `hdo_search_contacts` (`ajax:421-470`) | `hdo_search_contacts` | `upload_files` | `search_term` (sanitized, min 2), `show_all` | `WP_Query s=` on `hdo_contacts`, 10 or unlimited. Read only. | `wp_send_json_success([{id,name}])` |
| `hdo_search_properties` (`ajax:482-549`) | `hdo_search_properties` | `upload_files` | `search_term`, `show_all` | meta `LIKE` on `hdo_property_address` OR `hdo_property_city`. Read only. | `wp_send_json_success([{id,label}])` |
| `hdo_get_linked_appointments` (`ajax:560-602`) | `hdo_get_linked_appointments` | `upload_files` | `lookup_id` (absint), `lookup_type` `contact`/`property` | `hdo_get_appointment_ids_from_meta`. Read only. | `wp_send_json_success([{id,title,url}])` |

The three v1.7.0 handlers (search, search, linked) are the only ones written to the CLAUDE.md standard (nonce + cap + `wp_send_json_*`). The nonces for those three are localized once per page in `myAjax` (`main:323-325`); the others are emitted per button as `data-nonce` (`main:603, 736, 744, 1020, 1044, 1060, 1080, 1375, 1398`).

## 6. The report flow

### 6.1 Creating a report

The base plugin never creates a report post. The Report post and the Appointment post are created by the Gravity Forms submission handler in the child (base only renders form 1/5, `main:810-825`). Base assumes an appointment already has `hdo_appt_report` set; if it does not, `hdo_get_mode_and_report_id_in_select_notes()` returns `select:` with an empty ID (`main:1455-1456`) and every checkbox posts `report_id=""`.

### 6.2 Selecting notes ("Select Notes" overlay)

- `hdo_make_notes_to_select()` (`main:1250-1325`) builds the overlay `#hdo-select-notes-wrapper`: a TOC (`main:1227-1246`), then every published `hdo_notes` post (up to 5,000, sorted by `hdo_note_sort_order` as number, `main:1260-1267`) bucketed as `[section name][global subsection name][sort order] = note_id` (`main:1283-1289`). Two notes with the same sort order in the same bucket overwrite each other silently.
- Section order and hierarchy come from `hdo_make_array_of_sections()` (`main:1188-1223`): top-level `hdo_note_sections` terms keyed by `$term->order`, children nested with a `parent_name` key. Two terms with the same `order` overwrite. `ksort` orders numerically.
- Each note becomes `hdo_make_note_selection_form()` (`main:1354-1442`): an optional "label before" sub-heading, a clickable div `#note-<id>.hdo-note-checkbox-action` with `data-mode`, `data-report_id`, `data-note_id`, `data-old_value` (`none` or the stored `"id|exts"` string), `data-has_exts`, and a hidden `.hdo-revealed` panel holding the "Consider:" suggestion and, when the note has extensions, a form of radio/checkbox questions named `<note>-extension_<n>` whose values are the `ext_abbrv` strings (`main:1391-1431`).
- **Mode** is decided by URL (`main:1446-1459`): on `post.php?post=<report>&action=edit` mode is `add` (paste into Gutenberg via clipboard, nothing saved); otherwise mode is `select` with the report ID taken from `$_GET['hdo_appt_id']` (persisted to `hdo_selected_note` meta). Note the `else` branch runs on every admin page that is not a post edit screen, calling `get_field('hdo_appt_report', $_GET['hdo_appt_id'])` with an unset key.
- Previously selected notes are pre-checked from `hdo_get_notes_selected()` (`main:1463-1478`), keyed by note ID.
- Clicking a checkbox: `js:4-85` posts `hdo_select_note`; on `saved` marks it checked and stores the returned `"id|exts"` in `data-old_value`; on `deleted` unchecks. Submitting an extension form: `js:88-186` concatenates the checked abbreviation values of up to **four** questions (`js:100-133`; a fifth question is ignored) and posts with `exts`; on `updated` stores the new value.
- In `add` mode the response HTML is written into a hidden textarea, `select()`ed and `document.execCommand("copy")` (`js:52-78, 168-183`); the user then pastes into the block editor. `insertAtCursor` on `js:67` is a bare identifier that does nothing.

### 6.3 Compile ("compile report")

`hdo_compile_report()` (`ajax:130-215`):

1. Reads all `hdo_selected_note` rows, splits each on `|`, looks up the note's section, global subsection and sort order, and buckets them (`ajax:139-155`).
2. Walks `hdo_make_array_of_sections()` (after filter `hdo_compile_sections`). For each parent section emits `<!-- wp:heading --><h2 id="<slug>">` then each child via `hdo_make_this_section_for_compiling()`, then that child's "General Information" (`ajax:160-178`). Slugs are `strtolower(str_replace(' ', '-', ...))` with commas stripped, computed the same way in five places (`main:1233, 1298, 1331, 1514`, `ajax:163`).
3. `hdo_make_this_section_for_compiling()` (`main:1502-1567`) emits `<h3 id=slug>` then, for each global subsection that has notes, `<h4>` + the notes; then emits an empty `<h4>` for **every** global subsection that had no notes (`main:1547-1561`), so every section shows all global subsection headings. Each note's text is `get_the_content(null, false, $note_id)` or, when `exts` is non-empty, the `extension_text` whose `concatenated_abbreviations` equals `exts` (`main:1525-1538`); if no row matches, `$note_to_insert` carries over the **previous** note's text.
4. `hdo_guten_note()` (`main:1570-1587`) converts paragraphs to `<!-- wp:paragraph {"className":"hdo-selected-note"} -->` blocks and prepends `<span class="hdo-note-title-in-note">Note Title</span>` to the first paragraph.
5. `hdo_get_general_information_for_section()` (`main:1482-1498`) wraps the section term's description in a `wp:html` block; filter `hd_compiling_general_information`.
6. Per-section filter `hdo_section_<slug_with_underscores>` runs twice per section (inside `main:1563-1564` and again in `ajax:176-177`); the child uses `hdo_section_bank_summary` to add a header and signature (`ajax:175` comment).
7. `hdo_compiled_report` filter on the whole string (receives raw `$_REQUEST`), `hdo_report_postarr` filter on the post array, then `wp_update_post` and set `_hdo_report_is_compiled = '1'` (`ajax:180-192`).
8. Builds fresh action buttons using `new AppointmentHD(...)` (`ajax:195`), a class only the child defines; the JS ignores `val` and just reloads (`js:216-218`).

### 6.4 After compile: TOC, render, print, email

- The compiled body is ordinary Gutenberg content. `render_block` filter adds `id` attributes to every `core/heading` on the whole site (`main:1831-1843`) so anchor links work; the child draws the TOC.
- **View Report** is `/?p=<report_id>` in a new tab (`main:1067`, `main:525-527`). The report is publicly readable (section 4).
- **Email Report** reveals `#hdo-send-email-wrapper` (`js:441-444`), a Gravity Form **id 3** rendered via `[gravityforms id="3" field_values="hdo_email_client_name=...&hdo_email_prop_addr=...&hdo_email_report_link=<permalink>&hdo_email_client_email=..."]` (`main:1091-1108, 1145-1165`). Values are not URL-encoded, so an ampersand or quote in a name breaks the shortcode. Sending is done by GF notifications; nothing in this plugin sends mail.
- **Print** is not implemented in the base beyond CSS.
- **DE-compile** wipes `post_content` and the flag, returning to selection (`ajax:219-251`, confirm text in `js:233`).

### 6.5 "Incoming" and "Send to Online" (LOCAL mode)

- On a LOCAL install (`HDO_IS_LOCAL` true) the dashboard lists appointments with a **Send to Online** form (`main:1117-1141`) that POSTs `report_id`, `lock=narf`, `nickname` (report title) and `selected_notes` (the `hdo_selected_note` rows joined by `-`) to `https://reports.homedirections.net/incoming/`. The button only renders if `fsockopen("google.com", 80)` succeeds (`main:1660-1668`), which runs on every dashboard load.
- The online site's `/incoming/` page carries `[hdo_incoming_handler]` (`main:1672-1710`), which accepts any POST whose `lock` equals the literal `narf`, inserts an `hdo_incoming` post titled `"<nickname> | Received: <timestamp>"`, and stores the notes string and local report ID as meta. No nonce, no login, no capability; the `hdo_require_login` gate exempts page ID 11874 (`main:1861`), presumably this page.
- Online dashboard then shows "Match Incoming from LOCAL to Appointments:" (`main:626-654, 727-759`), a per-incoming form with a dropdown of the 20 most recent appointments and a "Match & Insert Notes" button, plus "Delete this Incoming". Matching (`ajax:345-386`) appends every note row to the chosen appointment's report and trashes the incoming record; JS then navigates to that appointment (`js:360-362`).

### 6.6 "Been here before"

The View Appointment panel "You've been to this Property before:" (`main:901-929`) runs `hdo_get_appointment_ids_from_meta($appointment->propertyID, 'hdo_appt_property')`, removes the current appointment, filters via `hdo_view_appt_other_appt_ids`, and lists each via `hdo_appointments_lines_by()` (`main:501-537`): type, title, View Appointment link, View Report/Letter link when compiled or Consultation, and "View all Appointments for this Property" (a dashboard lookup URL). The v1.7.3 fix for a report link leaking between iterations is `main:519-521`.

## 7. The JS (`js/hdonline.js`)

One jQuery `ready` block, enqueued on every front-end and admin page (`main:316-330`), dependent on `jquery`, no version string, no `in_footer`. Localized object `myAjax` = `{ajaxurl, dashboard_url, view_appointment_url, nonce_search_contacts, nonce_search_properties, nonce_get_linked_appointments}` (`main:319-326`).

Behaviours:

- Note checkbox click -> `hdo_select_note` (`js:4-85`); extension form submit -> `hdo_select_note` with `exts` (`js:88-186`); compile (`js:190-225`, `confirm`, reload on success); decompile (`js:229-263`); delete appointment with orphan prompt (`js:268-316`, redirects to `myAjax.dashboard_url`); match incoming (`js:321-376`, redirects to `myAjax.view_appointment_url + "&hdo_appt_id=" + id`); delete incoming (`js:381-415`); overlay open/close which also hides `#adminmenu`, `#adminmenuback`, `#wpadminbar` (`js:419-438`); email overlay (`js:441-444`); TOC toggle (`js:448-454`); hash-change scroll offset of 130px (`js:456-458`); live search with 300 ms debounce, Enter = show all (`js:466-596`); result click -> `hdo_get_linked_appointments` (`js:604-653`); click-outside closes dropdowns (`js:661-665`).

Endpoints: only `myAjax.ajaxurl` (admin-ajax). No hard-coded URLs remain in live code; the retired `/inspector-dashboard/` and `/view-appointment/` paths are in a comment (`js:363-369`).

Hard-coded IDs/limits: extension question names `_extension_1` to `_extension_4` (`js:100-103`); DOM IDs `#hdo-add-note-response`, `#hdo-select-notes-wrapper`, `#hdo-report-the-toc`, `#hdo-toc-toggle`.

Quality: all the click-handler variables (`action`, `nonce`, `report_id`, `note_id`, `old_value`, `mode`, `has_exts`, `appointment_id`, `is_local`, `incoming_id`) are assigned without `var`, so they are implicit globals (`js:7-17, 200-207, 240-245, 278-285, 391-396`). `console.log(orphan_choice)` on `js:289` runs before `orphan_choice` is declared (hoisted `var`, logs `undefined`). `is_local != true` (`js:287`) compares the string `"true"` to boolean `true`, so the orphan prompt shows even on LOCAL. Handlers bound with `.click()` only attach to elements present at ready time; the AJAX-rebuilt action buttons from compile are never used because the page reloads. `document.execCommand("copy")` is deprecated. Results are injected with string concatenation; server escapes `name`/`label`/`title` with `esc_html` first (`ajax:464, 543, 595`).

## 8. Extension points used by the child plugin

Base classes extended by the child: `AppointmentHD extends Appointment`, `ContactHD extends Contact`, `PropertyHD extends Property`, `ReportHD extends Report` (`hdonline-home-directions/classes/*-hd.class.php:5`). The base itself hard-depends on `AppointmentHD` at `ajax:195`, so the base cannot compile a report without the child installed.

Filters and actions the base exposes (all in `main` unless noted), with a mark for those the child actually hooks (confirmed by grep of the child repo):

| Hook | Args | Where | Child hooks it |
|---|---|---|---|
| `hdo_contact_output` | `$html` | `main:379` | |
| `hdo_delete_button_args` | `$args, $appointment` | `main:606, 1023` | |
| `hdo_view_appt_appt_title` | `$title, $appointment` | `main:857` | |
| `hdo_view_appt_appt_guts` | `$html, $appointment` | `main:882` | yes |
| `hdo_view_appt_property_guts` | `$html, $appointment` | `main:896` | yes |
| `hdo_view_appt_other_appt_ids` | `$ids, $appointment` | `main:909` | |
| `hdo_view_appt_other_appt_guts` | `$html, $appointment` | `main:922` | |
| `hdo_view_appt_client_guts` | `$html, $appointment` | `main:932` | |
| `hdo_view_appt_additional_contact_items` | `$html, $appointment` | `main:958` | |
| `hdo_view_appt_appt_output`, `_property_output`, `_client_output`, `_other_appts_output`, `_add_contacts_output` | `$output_so_far, $appointment` (cumulative string) | `main:967-979` | `_property_output`, `_other_appts_output` |
| `hdo_make_select_notes_in_view_appt` | `$bool, $appointment` | `main:993` | yes |
| `hdo_view_appt_report_action_buttons_local` | `$array, $appointment` | `main:1028` | |
| `hdo_compile_button_args` | `$args, $appointment` | `main:1047` | yes |
| `hdo_decompile_button_args` | `$args, $appointment` | `main:1063` and **again for the delete button** at `main:1083` (copy-paste; delete args pass through the decompile filter) | |
| `hdo_view_appt_report_action_buttons` | `$array, $appointment` | `main:1088` | yes |
| `hdo_email_form_args` | `$args, $appointment` | `main:1105` | yes |
| `hdo_section_heading` | `$html, $id_string` | `main:1301` | |
| `hd_compiling_general_information` | `$html, $section, $appointment` (note the `hd_` not `hdo_` prefix) | `main:1494` | yes |
| `hdo_compile_subhead` | `$html, $slug, $report_id` | `main:1520, 1550, 1557` | yes |
| `hdo_global_subsections_included` | `$array, $slug` | `main:1545` | yes |
| `hdo_section_<slug>` (dynamic) | `$html, $slug, $report_id` | `main:1564`, `ajax:177` | `hdo_section_bank_summary` |
| `hdo_compile_sections` | `$sections` | `ajax:158` | |
| `hdo_compiled_report` | `$html, $_REQUEST` | `ajax:180` | yes |
| `hdo_report_postarr` | `$postarr, $appointment` | `ajax:187` | |
| `hdo_delete_appointment` | `$failures, $appointment, $orphan_choice` (applied as a filter; the child registers with `add_action` and returns the array, which works because actions and filters share one table) | `ajax:264` | yes |
| `hdo_delete_appt_client_orphan_check` | `$args, $appointment` | `ajax:284` | yes |
| `hdo_report_actions_metabox_filter` | `$html, $appointment_id, $post_type` | `main:1641` | yes |
| `hdo_report_actions_metabox` (action) | none | `main:1645` | |

Global functions the child calls: `hdo_extract_id_from_acf_field()`, `hdo_get_appointment_ids_from_meta()`, `hdo_make_ajax_button()`, `hdo_admin_page_url()`, `hdo_guten_note()`, `clc_die_silently()` (the last is defined in neither repo).

Template hooks: none in the base; the child supplies `single-hdo_reports.php` and `single-hdo_invoices.php`.

## 9. Smells and risks

### Security

1. **Unauthenticated write endpoint.** `[hdo_incoming_handler]` creates posts for any POST with `lock=narf` (`main:1673`), a shared secret in source. Rate-unlimited; anyone can fill the Incoming queue.
2. **No capability checks** on `hdo_select_note`, `hdo_compile_report`, `hdo_decompile_report`, `hdo_delete_appt`, `hdo_match_incoming`, `hdo_delete_incoming` (`ajax:33-411`). Any logged-in user (Subscriber) with a valid nonce (which the localized script and the selector overlay hand out on every admin page, `main:1656`, `main:1375`) can trash appointments, wipe report content, or write meta to any post ID.
3. **Unsanitized `$_REQUEST`** written to meta and used as post IDs: `ajax:44-45, 76-77, 105, 225, 261, 351-353, 370`. `report_id` in `hdo_select_note` is any post ID, so meta can be attached to arbitrary posts.
4. **Unescaped output** throughout the render functions: post titles, ACF text, `$_GET['hdo_lookup_type']` echoed raw (`main:799`), `$_GET['hdo_appt_id']` trusted after `is_numeric` only (`main:838`), attribute values built by string concat in `hdo_make_ajax_button` (`main:1174-1180`).
5. **Public CPTs and REST**: all six CPTs are `public` + `show_in_rest` (`cpt`), and `hdo_require_login` exempts reports and invoices (`main:1861`). Client PII (contacts) is reachable at `/wp-json/wp/v2/hdo_contacts` for anyone if the CPT is published, subject to WP's default REST rules (titles only, since ACF groups have `show_in_rest => 0`). Unconfirmed on the live site; flag for the rebuild.
6. `hdo_is_online()` opens a socket to `google.com:80` on every LOCAL dashboard load (`main:1660-1668`).
7. `us_states()` is an unprefixed global (`main:343`).

### Correctness bugs

8. `wp_ajax_hdo_add_note` is hooked to an undefined function (`ajax:22`).
9. `hdo_compile_report` instantiates `AppointmentHD` (`ajax:195`), a child-only class: fatal without the child.
10. `hdo_appointments_lines_by()` builds `$other_appointment_output_array` only inside the loop and returns it unset for an empty input (`main:516-535`); callers `is_array()` guard it (`main:787, 914`).
11. `hdo_make_this_section_for_compiling` carries `$note_to_insert` across iterations when an extension key has no matching text row (`main:1525-1538`).
12. Both `hdo_make_this_section_for_compiling` (`main:1563-1564`) and `hdo_compile_report` (`ajax:176-177`) apply `hdo_section_<slug>`; for a child section the filter runs on the child slug then again on the parent slug, and the child plugin's bank-summary filter can therefore be applied twice depending on term layout.
13. `hdo_match_incoming` appends notes without de-duplication; matching twice doubles every note (`ajax:357-368`).
14. `$is_compiled[0]` is read from a non-single `get_post_meta` without checking the array is non-empty (`main:523-528, 985-987, 1034-1036`); PHP 8 emits a warning on undefined offset.
15. `hdo_get_mode_and_report_id_in_select_notes()` reads `$_GET['action']` and `$_GET['hdo_appt_id']` without `isset` (`main:1449, 1455`); its `else` branch runs on every admin screen because the selector is printed in `admin_footer` site-wide (`main:1656`).
16. `HDO_IS_LOCAL` decides GF form ID 5 vs 1 and hides features; it is never defined here, so a mis-set constant silently changes behaviour (`main:295, 579, 812, 861, 1009`).
17. Delete logic: `is_local == '1'` (`ajax:322`) never matches the JS value `true`; `hdo_decompile_button_args` is applied to the delete button (`main:1083`).
18. `hdo_catch_edit_report_url` redirects from `admin_head` (`main:1873-1908`), after headers are normally sent.
19. Section arrays keyed by `$term->order` (`main:1211-1216`) depend on a term-order plugin adding that property; without it every key is `null`/`''` and sections collapse into one. `hdo_make_array_of_sections` ordering of children uses the same collision-prone keying.
20. Appointment date sort uses `meta_value_num` on ACF's `Ymd` string (`main:456-458`); works by accident of the storage format.
21. `hdo_make_notes_to_select()` loads up to 5,000 notes, runs `get_the_terms` twice and `get_field` once per note, then `new Note()` (a `WP_Query` + `have_rows` loops) per note again in `hdo_make_note_selection_form` (`main:1260-1291, 1369`). That whole block is rendered into `admin_footer` on every admin page (`main:1656`), including the Plugins and Posts screens.
22. Every render helper reads relationship links via `LIKE` on serialized meta (`main:453-481`); ID 12 vs 120 is guarded by quoting, but the plain `=` branch (`main:474-478`) and the child's un-quoted `LIKE` (`ajax:274-283`) are not.
23. `hdo_update_related_post_titles_on_appt_save` runs on `acf/save_post` for any post type and returns early otherwise, but for appointments it rewrites the **report's slug** too, breaking previously shared report URLs whenever the client or property name changes (`main:1715-1743`; the author's own note at `main:1747-1748`).
24. `hdo_require_login` exempts hard-coded page ID `11874` (`main:1861`); the old dashboard page ID `10389` is mentioned in a comment (`main:1931`). GF form IDs 1, 3, 5 are hard-coded (`main:295, 307, 812, 1096`). The remote URL `https://reports.homedirections.net/incoming/` is hard-coded (`main:1129`).
25. `copper_leaf_hdonline_php_load_point` appends `plugin_dir_path(__FILE__) . '/acf'` producing a double slash (`main:76`); harmless on Linux.

### PHP 8 issues

26. Dynamic properties on the value classes (`$this->name`, `$this->company`, `$this->text`, `$this->appointmentType`, `$this->gform_entry_id`, `$this->additionalContactsIDs`): deprecated in 8.2 (`classes/appointment.class.php:57, 64, 68, 83`; `classes/contact.class.php:50`; `classes/note.class.php:41-42`; `classes/property.class.php:38`).
27. Undefined-variable string concatenation with `.=` on first use: `$local_appts_actions` (`main:594`), `$incoming_output` (`main:659` when no incoming), `$output` in `hdo_make_notes_to_select_table_of_contents` (`main:1233`), `hdo_make_notes_to_select_section` (`main:1332`), `hdo_get_general_information_for_section` (`main:1488`), `hdo_compile_report` (`ajax:164`), `$additional_contact_items` (`main:951`), `$other_appointment_output` (`main:975`), `$checked`, `$data_has_ext`, `$label_before`, `$display_suggestion`, `$reveal_suggestion` (`main:1360, 1372, 1380, 1384, 1388, 1436, 1439`), `$selected_notes_ids_array` (`main:1476`), `$notes_to_select` (`main:1289`), `$appointment_options`/`$appointment_links` (`main:686, 714`), `$global_subsections_included` (`main:1544, 1548`), `$send_result` in every AJAX handler. Warnings under 8.x, and `implode()` on `null` (`main:721`, when there are no appointments) is a TypeError under 8.0+.
28. `list($mode, $report_id) = explode(":", ...)` when the function returned `null` (`main:1356, 1465`): `explode(":", null)` is deprecated in 8.1.
29. `date_create($raw_date)` with an empty date returns `false`; `date_format(false, ...)` is a TypeError in 8 (`classes/appointment.class.php:53-55`).
30. Constructors `return` values (`classes/appointment.class.php:18`, `classes/report.class.php:10`); harmless but meaningless.
31. `@fsockopen` suppression (`main:1661`).

### Dead code and duplication

32. Commented-out meta-box scaffolding (`main:1595-1603`), a 75-line commented "false start" (`main:1747-1821`), commented debug echoes (`main:1157, 1161`, `ajax:361-365`), a `$debug` block that can never fire (`main:831-850`), the empty `Report` class (`classes/report.class.php`), `hdo_local_report_id` written but never read (`main:1695`).
33. Two copies of every stylesheet: `css/copper-leaf.css` == `css/hdonline.css` and `css/copper-leaf-select-notes.css` == `css/hdonline-select-notes.css` (byte-identical); `copper-leaf-admin.css` and `hdonline-admin.css` differ. Both sets are enqueued (`main:238-249, 275-290`).
34. The slugify expression `strtolower(str_replace(',', '', str_replace(' ', '-', $x)))` is repeated at `main:1233, 1237, 1242, 1298, 1311, 1331, 1514` and `ajax:163`, and does not match `sanitize_title_with_dashes()` used for the heading IDs at render (`main:1841`), so TOC anchors can miss for names with punctuation.
35. The "generic" base and the Home Directions child are entangled: base needs `AppointmentHD` (`ajax:195`), `clc_die_silently` (undefined here), child-only ACF fields (`hdo_appt_additional_contacts`, `hdo_appt_invoice`), hard-codes the HD domain (`main:1129`) and HD-specific copy ("...for HD consults", `main:1091`; `hd_compiling_general_information`).
36. Three copies of "recent appointments" queries with different limits (`main:581-587, 671-694, 697-724`).
37. `hdo_add_select_notes_to_edit_report` prints the selector overlay on every admin page (`main:1651-1656`); `hdo_script_enqueuer` enqueues jQuery and the plugin JS on every front-end and admin request from `init` (`main:316-330`).

### Migration hazards (stored data shapes a rebuild must read)

38. `hdo_selected_note`: many rows per report, value `"<note_id>|<abbrev-string>"`; the abbreviation string is the concatenation of `ext_abbrv` values in question order with no delimiter (`js:133`, `main:1415`) and must equal a `concatenated_abbreviations` row exactly (`main:1532`, `ajax:92`). Abbreviations that are prefixes of each other are ambiguous by design.
39. `_hdo_report_is_compiled` = `'1'` string, single row (created via `update_post_meta`, `ajax:192`).
40. `hdo_incoming_selected_notes`: single string, rows joined by `-` (`main:1124`), so a `-` inside an abbreviation would break splitting (`ajax:355`).
41. ACF relationship fields on appointments are serialized arrays of numeric **strings** normally, but comments and code (`main:447-452`, `classes/appointment.class.php:39-45`) document that some rows were saved as ints or plain values by direct `update_post_meta` (the child does this at `hdonline-home-directions/copper-leaf-hdonline-home-directions.php:617`). Any migration must normalise all three shapes.
42. Section/subsection identity is by **term name** (`main:1289`, `ajax:147-152`, `main:1484` uses `get_term_by('name', ...)`); renaming a term silently orphans notes at compile.
43. Appointment/report titles and slugs are derived and rewritten on save (`main:1726-1741`); external links to reports are slug-based.
44. `hdo_gf_entry_id` on appointments links back to Gravity Forms entries (`classes/appointment.class.php:67`).
45. `hdo_incoming` is an unregistered post type in code; the rows exist in `wp_posts` regardless (`main:1684-1690`).
46. The old front-end page IDs (10389 front page, 11874 incoming) and GF form IDs (1, 3, 5) are environment data, not code.

### Release-notes "bug audit" (v1.7.3, `release-notes.txt:15-25`)

Items claimed fixed and confirmed present in code: `hdo_notes` slug (`cpt:34`), `$view_report` reset (`main:519-521`), `orderby`/`meta_key` at top level (`main:456-458`), `get_the_terms` guards (`classes/note.class.php:44-49`, `ajax:146-149`, `main:1283-1286`), constructor early returns (`classes/contact.class.php:26-28` etc.), removed `hdo_parse_blocks_to_draw_report_toc` (no longer present), nonce in `hdo_compile_report` (`ajax:132`), nonce in `hdo_delete_incoming_func` (`ajax:392`), compile nonce name (`main:1044`), sanitized incoming inputs (`main:1678-1680`). The audit did not add capability checks or input sanitization to the older AJAX handlers, which remain as described in section 5.
