---
name: Home Directions v4 plan
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The rebuild plan: what v4 is, the stack decision with options and Sancho's pick, the data model, the Google Docs and email mechanics, build order with gates, the Phase 2 migration, risks, and the numbered questions for Gordon
sources: ["[doc:requirements.md]", "[doc:current-system.md]", "[doc:survey-hdonline.md]", "[doc:survey-hdonline-home-directions.md]", "[rec_8d15ed467e 2026-09-29]", "[gordon 2026-09-30]"]
status: draft for Gordon's review, 2026-10-01
---
# Home Directions v4: the plan

Draft written overnight 2026-09-30/10-01 from the code surveys, the 09-29 transcript and homedirections.net. Nothing here is built. Every fork has options and a pick; the picks are Sancho's and are the first thing to argue about. Numbered questions for Gordon are at the end; the ones that block Phase 0 are marked **blocks**.

## 1. What v4 is, in one paragraph

A small, single-tenant web app for one engineer. It hears Calendly, creates a **file** per job with a deduplicated **client** and **property**, spawns a **Google Doc letter** from a template with a self-explanatory name, generates and sends an **invoice PDF**, tracks paid, sends the letter as a read-only link with a PDF snapshot, logs every email, and lets Peter fix a name once and have it fixed everywhere. Three screens: Dashboard, File, Settings. Everything the old system did for home inspections (notes library, compile, sections, water and radon data sheets, brokers and attorneys, LOCAL mode) is not carried forward; it is archived as PDFs in Phase 2.

## 2. Stack: options and pick

| | A. WordPress plugin v4 (custom tables, no ACF) on SiteDistrict | B. Standalone Laravel app | C. Google-native (Apps Script + Sheets + Docs) |
|---|---|---|---|
| Relational integrity (R2.1, R2.3) | Possible with `$wpdb` custom tables, but everything in WP pulls toward posts and meta; the old system's root pain | Native: migrations, foreign keys, unique indexes, transactions | Sheets is not a database; dedup and joins are hand-written script |
| Calendly webhook | REST route; SiteDistrict bot protection returns 429 to automated requests (kit CLAUDE.md §10), so the webhook may be blocked | Ordinary route with signature check | Apps Script web app; works, throttled, hard to debug |
| Google Docs / Drive | PHP client; fine | PHP client; fine | Native and easiest |
| Email with logs (R5) | Provider API; WP mail plugins add noise | Provider API, queued, logged | Gmail from script; no delivery events, quota-limited |
| Testing (Sancho rule: automatic) | Possible, awkward (WP test harness) | Built in (Pest/PHPUnit, fakes for mail, queue, HTTP) | Weak |
| Hosting | Exists (SiteDistrict) | New: a small VPS or Laravel Forge/Cloud, or SiteDistrict if it runs non-WP PHP (question 3) | None |
| Who can maintain it | Gordon; Leah/Astra with the kit | Gordon with Claude Code; not Leah | Gordon |
| Long-term risk | Plugin ecosystem churn, updates as attack surface, the 2021 code's gravity | One more stack to patch; small surface; boring | Script rot, Google quota and auth changes, no versioning discipline |

**Pick: B, Laravel.** The whole point of v4 is that the data is relational and corrections propagate; that is what a framework with a real ORM gives for free and what WordPress made hard for five years. PHP keeps it in Gordon's language and the Nerd builds it under a CLAUDE.md of its own (kit rules where they apply: readability, prefixing is moot, tests mandatory). Django would be an equally sound B; Laravel wins on PHP alone. C is tempting because the letters are Google Docs anyway, but it fails the "robust and mature" brief on testing and data integrity.

Concrete: Laravel 12, PHP 8.3, **SQLite** as the database (one user, one file, trivial to back up nightly to Drive and to copy to a laptop; upgrade path to MySQL is a config line), Breeze auth (email + password; Google sign-in later if wanted), Livewire or plain Blade for the three screens (pick plain Blade + a little Alpine; less to learn), queue on the database driver, scheduler via cron. Repo `~/Dev/hdonline-v4` (its own repo, not the plugin kit). Hosting decision is question 3.

## 3. Data model

```
clients      id, first_name, last_name, email (unique, lowercased), phone, company, notes, created_from (calendly|manual|import), merged_into_id
properties   id, line1, line2, city, state, zip, normalized_address (unique), place_id (Google, nullable), lat, lng, notes, merged_into_id
files        id, client_id, property_id, service (opinion|design|hourly), mode (site|virtual|design), scheduled_at, status (booked|visited|drafting|sent|paid|closed|cancelled),
             price, narrative (the big paragraph), calendly_event_uri, calendly_invitee_uri, letter_doc_id, letter_folder_id, stamp (ct|ny|none), created_by, cancelled_at
invoices     id, file_id, number (HD-2026-0001), description, lines (json), subtotal, discount, total, issued_at, paid_at, pdf_path (latest), template_version
sends        id, file_id, kind (invoice|invoice_paid|letter), to, cc, subject, provider_message_id, sent_at, delivered_at, opened_at, pdf_snapshot_path, doc_revision_id
settings     key, value (invoice templates ×3, letter template doc ids, from address, stamp defaults, Calendly event-type map)
history      id, subject_type, subject_id, field, old, new, changed_by, changed_at   (the audit trail behind "fix it once")
imports      Phase 2: legacy_system, legacy_id, legacy_url, pdf_path, file_id     (old links redirect through here)
```

Dedup rules (R2.1): clients match on email first, then on last name + phone; properties match on Google `place_id` when geocoding succeeds, else on `normalized_address` (uppercase, punctuation stripped, St/Rd/Ave/Ln expanded, ZIP5). A near match is never silently merged: the file page shows "Looks like 12 Shad Hill Rd, Smith, 2019; same property?" with one click to link or to keep separate. Merges are recorded (`merged_into_id`), never deleted (Sancho must-never 11 applies to Peter's data too).

State (CT or NY) comes from the geocoded or entered address and sets the default stamp; Peter can override per file (R3.7).

## 4. The letter: Google Docs mechanics

- **Where the docs live.** Pick: a Google Workspace account for homedirections.net with a shared drive "Home Directions Letters" (folders per year); the app acts through a service account with domain-wide delegation as peter@homedirections.net, so every doc is owned by the company, not by a robot or a person. If there is no Workspace (question 4), fallback: OAuth as Peter with the `drive.file` scope only (no verification needed for that scope; the app can only touch files it created, which is exactly right), docs in Peter's My Drive under a folder the app creates.
- **Templates.** One Google Doc per service (Opinion, Design, Hourly), maintained by Peter in Docs, listed in Settings by ID. Placeholders `{{client_name}}`, `{{client_address}}`, `{{property_address}}`, `{{date}}`, `{{stamp}}`. On file creation the app copies the template, replaces placeholders, and records **named ranges** for each placeholder so later corrections replace exactly that text and nothing else (R2.3). The stamp is an inline image the app inserts at `{{stamp}}` from the CT or NY PNG (already in the plugin repo) or nothing.
- **Name.** `YYYY-MM-DD_<Last>_<street address>_Home Directions` (R3.2). Renamed by the app when the client name or address changes.
- **Sending (R3.5, R5.3).** "Send letter" sets sharing to anyone-with-link viewer, exports a PDF of the current revision, stores it in the shared drive `sent/` folder and in `sends.pdf_snapshot_path`, emails the client the link **and** the PDF, and logs the Docs revision ID. Peter's accepted model (link shows the newest) is honoured; the snapshot exists because a stamped engineering letter that was sent should also exist as an immutable record. **Question 8** is whether the client email carries the PDF or only the link.
- **Read-only look (R3.6).** Viewer access to a Doc shows toolbars. The PDF attachment looks like a document; the "preview" link (`/preview` URL form) hides most chrome. Gordon said he would send himself one to check; the plan assumes link + PDF until then.

## 5. Invoices (R4)

Structured in the app, rendered by the app. An invoice has a number (`HD-YYYY-NNNN`), a description that starts from the service's Settings template and is edited freely on the file page, optional extra lines, a stored total, and a PDF rendered from a Blade template with the letterhead (DomPDF; swap for headless Chrome only if the look is not good enough). Every send stores the exact PDF sent. "Mark paid" stamps `paid_at`, renders a PAID copy and sends it automatically (R4.4). Resend is a button. The three dictated texts seed the Settings templates; Peter edits them there (R4.2, R4.3).

## 6. Email (R5)

Pick: **Postmark** (or Resend) on `homedirections.net` with SPF, DKIM and DMARC set up once, sending from `peter@homedirections.net` with reply-to Peter and a BCC copy to his mailbox so every send sits in his mail too. Postmark returns delivered and opened events by webhook, which fill `sends.delivered_at` and `opened_at`: that is the closest honest thing to Peter's "return receipts" (true read receipts do not exist on the open internet). If Workspace exists, sending through the Gmail API as Peter is the alternative (lands in his Sent folder natively) but gives no delivery events; the plan prefers events.

## 7. Calendly (R1)

- Webhook subscription on `invitee.created` and `invitee.canceled` (and reschedule, which Calendly delivers as cancel + create with a `rescheduled` flag), signature verified, idempotent on the invitee URI. Webhooks need a Calendly Standard plan or above (question 5). Fallback if the plan is lower: poll the API every 15 minutes, same handler.
- Settings map each Calendly event type to a service and a mode (Opinion site visit, Opinion virtual, Design). The booking form must ask the property address as a required question (question 6); the handler geocodes it and runs dedup.
- Cancel: the file goes to `cancelled` (not deleted), the Google Doc shell is trashed if it is still the unedited template copy, kept if Peter typed anything (Docs revision count > 1). Gordon said "delete"; the plan keeps a tombstone because of must-never 11 and because clients rebook.

## 8. Screens

1. **Dashboard:** New File button, search box (client, address, month), infinite-scroll list of recent files with status chips and the next action (draft letter, send invoice, mark paid, send letter).
2. **File:** client card (edit in place), property card (edit in place; "been here before" list with links), job facts (service, mode, date, price, stamp), narrative field, invoice panel (preview, send, mark paid, resend, history), letter panel (open Doc, send, history), email log, delete (two confirmations; Calendly-booked files also cancel in Calendly via API, question 7), history of changes.
3. **Settings:** the three invoice texts, the three letter template IDs, from address, stamp defaults, Calendly event-type map, users.

Users: Peter (owner), Gordon (admin), Mom (editor of docs via Google; app login optional).

## 9. Build order and gates (Phase 1)

Each step ends with automatic tests green and a working deploy on staging; Peter sees it at step 3, not at the end.

1. **Skeleton:** repo, CLAUDE.md for v4, Laravel, SQLite, auth, the three tables that matter (clients, properties, files), Dashboard and File with manual entry and dedup prompts. Usable by hand from day one.
2. **Letters:** Google integration, templates, doc creation, naming, named ranges, correction propagation, rename.
3. **Invoices and email:** numbers, templates in Settings, PDF, Postmark, send, paid, resend, logs, events. **Gate: Peter runs one real job end to end on staging.**
4. **Calendly:** webhook, event-type map, cancel/reschedule, idempotency; fallback poller.
5. **Search, history, delete, settings polish.**
6. **Parallel run:** four weeks with real jobs on v4 while the old site stays up read-only for reference. **Gate: Peter says it is easier than before (R2.2), and every send in the log matches what he meant to send.**

Hosting, DNS (`app.homedirections.net`), backups (nightly SQLite copy plus PDFs to Drive), monitoring (a Pushover on any failed job or webhook, through Sancho's `notify`), and a one-page "how to" for Peter belong to step 1 and step 6 respectively.

## 10. Phase 2: migration and retirement (R7)

Order matters: freeze, census, archive, redirect, then retire.

1. **Census on the dev clone** (login pending): counts of appointments by type and year, reports compiled vs consult letters, invoices, contacts by type, properties, notes; which fields are actually filled. Decides everything below.
2. **Freeze the live WordPress** after v4's parallel run: no new appointments there; keep it up for reading.
3. **Consult letters, last ~12 months (R7.1):** export each report's rendered HTML, import to Google Docs via the Drive API's convert-on-upload, name per R3.2, file under the client and property in v4 (files rows with `created_from = import`). Spot-check ten with Peter.
4. **Inspection reports, all (R7.2):** render each public report URL on the clone with headless Chrome to PDF (the templates already carry print CSS; every photo on its own page), store in Drive `archive/<year>/`, create a v4 file row with client, property, date, and an `imports` row mapping the old URL (`/?p=ID` and the slug URL, both) to the PDF. Same for invoices.
5. **Redirects:** `reports.homedirections.net` becomes a redirect table (a 30-line plugin on the old site, or the v4 app answering that host): old link → PDF in Drive (or a v4 page that serves it). Keep for years.
6. **Word files 1990s (R7.3):** LibreOffice headless converts .doc to PDF in bulk; file names and any index Peter kept give date and address; create file rows where the address can be parsed, "unfiled" otherwise. Search covers them.
7. **The blown-apart database (R7.4)** and **the Grayson system (R7.5)**: an investigation job first (what backups exist, what the two percent is), then a migration plan of its own. Not on the critical path to retiring WordPress.
8. **Retire:** final export of the WP database and uploads to Drive, DNS moved, plugins archived in GitHub, the SiteDistrict clone kept for a year.

## 11. Risks, and what the plan does about them

- **Google auth expiry and verification.** Service account with Workspace delegation has neither problem; OAuth-as-Peter with `drive.file` avoids verification but tokens can be revoked by a password change. The plan's default is Workspace (question 4).
- **Calendly plan lacks webhooks.** Poller fallback, same code path.
- **Bot protection blocks webhooks** if hosted on SiteDistrict. Hosting choice (question 3); a VPS has no such layer.
- **Address dedup wrong.** Never automatic merge; always a one-click confirmation; merges reversible by history.
- **Docs correction replaces the wrong text.** Named ranges, not global find-and-replace; tests with a doc that contains the client's name in the body.
- **Sent letter differs from what Peter meant.** PDF snapshot per send, revision ID logged.
- **Peter rejects a new UI.** Three screens, one obvious next action per file, and step 3's gate is his real job, not a demo.
- **Data loss in migration.** Nothing on the old site is ever changed; the clone is the source; counts reconciled before and after; old links keep working through the redirect table.
- **Bus factor.** The repo, a CLAUDE.md, tests, and a runbook; SQLite and Drive make the data portable without the app.

## 12. Questions for Gordon (numbered; **blocks** = needed before Phase 0 closes)

1. **blocks** Stack: Laravel as picked, or WordPress for the kit's sake? (Sancho: Laravel.)
2. **blocks** Google Workspace on homedirections.net: yes or no? If no, do you want to add it (about $7 per user per month; it also fixes the email question)? (Sancho: yes.)
3. **blocks** Hosting: does SiteDistrict run a non-WordPress PHP app with cron and a queue worker, and do you want it there, or a small VPS / Laravel Forge? (Sancho: VPS or Forge; keep SiteDistrict for WordPress only.)
4. Calendly: which plan, which event types exist, and does the booking form already ask for the property address?
5. Should cancelling in Calendly delete (Gordon's word) or tombstone (plan's pick) the file?
6. Deleting a file in v4: should it also cancel the Calendly event and email the client, or only remove our record?
7. Letter email: link only (Peter's "link updates" model), or link plus PDF snapshot (plan's pick)?
8. Email sending: Postmark with delivery/open events (plan's pick) or Gmail-as-Peter through Workspace (no events, native Sent folder)?
9. Stamp: derived from the property's state with an override (plan), or always a manual choice? Any jobs outside CT and NY?
10. Invoice numbering starts where? Any accounting (QuickBooks, spreadsheet) that should receive invoices or paid events?
11. Who is "Mom" in the system: Google editor only, or an app login too? Is she Maria Pia Seirup, named on the invoices?
12. Property facts to keep on the file: address only, or year built and house type too (R2.7 says streamline)?
13. Phase 2: which ~12 months of letters go to Docs (a date), and is the dev clone complete enough to be the migration source, or must the archive run against live?
14. What is "the Grayson system," and what backups exist of the database that was blown apart?
15. Website cleanup (R8): separate project under Copper Leaf, or a step in this one?

## 13. What happens next

Phase 0 is one conversation on questions 1 to 3, then the Nerd gets step 1 as a job with this document as the spec. Sancho's data census (step 10.1) runs as soon as the dev site login works in the Chrome tab.

## History of corrections
- 2026-10-01 evening (HD thread): five corrections to this draft are recorded in `phase0-brief.md` with their sources (Laravel 13 not 12; Workspace already exists on the domain per DNS; SiteDistrict is WordPress-only; Brevo already authenticated on the domain; inline question numbers in §4, §7, §8, §11 do not match the §12 list, which is the authority). The text above is left as drafted until Gordon decides questions 1 to 3; the revision folds them in.
- 2026-10-01 late (HD thread): decided and found since the draft, all to be folded into the next revision: **stack is Laravel** and **Workspace exists (Business Starter)** [gordon 2026-10-01, quoted in `phase0-brief.md`]; hosting researched with a pick (`hosting-options.md`), PHP 8.5 not 8.3 or 8.4; the census (`census-2026-10-01.md`) shows §10 is wrong about Phase 2's shape: the database already holds 10,212 jobs back to 1983 but only 774 reports, so step 4 (print the old inspection reports) covers about 100 to 130 reports, and the old reports for some 9,400 jobs are not in WordPress at all; §3's `clients.first_name, last_name` does not fit data in which 71 percent of clients are couples; the legacy data must live in the new database (R7.8), so §3 grows.
