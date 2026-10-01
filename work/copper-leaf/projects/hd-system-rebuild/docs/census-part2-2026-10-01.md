---
name: Home Directions data census, part 2
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: What the dev clone's database holds, read over SSH on 2026-10-01 with read-only queries (counts only); the v2 tables found inside the WordPress database with their migration mapping; which fields are filled, by era; contacts, emails, inspectors, reports, invoices; the 2008 gap by month; a first look at the live v2 site; what is still missing and where it must be
sources: ["[census:hdonline-sancho.sitedistrict.com 2026-10-01, `wp db query` over SSH on host-2, SELECT only, MariaDB 10.3.17]", "[gordon 2026-10-01: 'You have SSH access to host-2 on SD ... Go ahead and census']", "[chrome 2026-10-01: hdonline.homedirections.net/hdonline/, home page only, nothing clicked]", "[doc:census-2026-10-01.md]", "[doc:phase0-brief.md Decisions]"]
status: complete for the clone; the v2 database itself and the backups have not been read
---
# Data census, part 2 (2026-10-01)

## The five findings that matter

1. **v2's own tables are inside the WordPress database.** `REPORTS` (9,442 rows) and `CONTACTS` (11,321 rows), in v2's original column layout, each row carrying the ID of the WordPress record it became. The migration to v4 can read clean columns instead of unpicking WordPress post meta.
2. **v2 was itself loaded in one go on 2014-12-10.** 8,092 of its 9,442 jobs were created that day, covering job dates from 1983 to that date. So everything before December 2014 reached v2 by a bulk load from an earlier system, and the thin years and the 2008 gap were already in what was loaded.
3. **The 2008 gap is ten months wide and has edges.** One job in December 2007, none until October 2008, then a slow restart with no type and no fee recorded until mid-2009. It is not the 2015 note-deletion Gordon described [gordon 2026-10-01]; it is a separate loss, and it looks like a change of system.
4. **The report bodies of v2 are not here.** The clone holds v2's job and contact rows, not the notes chosen for each report. Those live only in v2's own database (and its backups), which is where the 2015 damage is too.
5. **Legacy rows are substantial, not stubs:** fee, address, square footage, water supply and sewage are filled on nearly every row back to 1983.

**Gordon's caution on finding 1, the same night:** "even those tables in WP are suspect. Good data, but probably incomplete and maybe a little messy. We should dig all the way back into original MS Access database backups if we can." [gordon 2026-10-01] So `REPORTS` and `CONTACTS` are a convenient witness, not the truth: they are what v2 held in 2020, after the 2014 bulk load and whatever that load dropped. Section "What this changes", item 1, is to be read with that: migrate from them, and reconcile against every older source that can be found.

## How this was read

`wp db query` over SSH in the clone's folder on host-2, one statement per call, `SELECT` only, counts and dates only. No names, emails, addresses or phone numbers were printed. Nothing was written. WP-CLI cannot load WordPress on that host (its shell has PHP 7.3; WordPress 7.1.2 needs 7.4), as the kit's handoff predicted [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md §8], but the database command does not need WordPress loaded. The queries in `census-part2-queries.md` were adapted as they ran (MariaDB; no trailing semicolons, which the guard now refuses).

## The v2 tables in the clone

| Table | Rows | What it is |
|---|---|---|
| `REPORTS` | 9,442 | v2's jobs: one row per appointment, with `wp_appt_id` and `wp_property_id` added by the migration |
| `CONTACTS` | 11,321 | v2's contacts: one row per person per job, with `wp_contact_id` added |
| `MODERATE` | 0 | the migration's work queue for near-duplicates, now empty |

All 9,442 `REPORTS` rows are mapped to a WordPress appointment. So: **10,212 WordPress appointments = 9,442 that came from v2 + 770 created in v3** since November 2020. On the WordPress side, 9,441 appointments carry `hdo_appt_legacy_report_id`, the way back to the v2 row.

WordPress's import tool kept its history: the contacts came from a file named `homedire_hdo_a2_CONTACTS_for_import_v1.csv` on 2020-09-07 (11,258 rows read), and the inspection notes library from `homedire_hdo_a2_NOTES_...` on 2020-09-08 and 09-11. So v2's database is called `homedire_hdo_a2`. Where it is hosted is not on disk. Unconfirmed.

### When v2's rows were created

| Created in | Rows | Job dates they cover |
|---|---|---|
| 2014 (all on 2014-12-10) | 8,092 | 1983-01-01 to 2014-12-10 |
| 2015 | 261 | |
| 2016 | 216 | |
| 2017 | 236 | |
| 2018 | 154 | |
| 2019 | 258 | |
| 2020 | 223 | to 2020-11-25 |
| 2021 | 2 | placeholder dates |

### Job types and inspectors in v2
Type: inspection 7,144; consultation 2,181; blank 116; one other.
Inspector code: P 6,613; C 1,349; F 1,197; B 156; blank or other 127. In WordPress the same jobs sit under three users: user 5 has 7,568, user 6 has 1,217, user 7 has 1,427. So the history has at least three inspectors; "Peter is the only inspector" [gordon 2026-09-30] is true of now. Who C, F and B were is not on disk.

### Which v2 job fields are filled, by era of the job date

| Field | before 1996 (288) | 1996 to 2008 (6,247) | 2009 to 2014 (1,562) | 2015 to 2021 (1,344) |
|---|---|---|---|---|
| client code | 288 | 6,247 | 1,562 | 1,344 |
| time | 288 | 6,247 | 1,562 | 1,341 |
| fee | 288 | 6,233 | 1,466 | 1,203 |
| address | 287 | 6,241 | 1,547 | 1,280 |
| city | 287 | 6,243 | 1,546 | 1,259 |
| state | 287 | 6,194 | 1,546 | 1,256 |
| zip | 195 | 2,382 | 1,532 | 1,140 |
| square footage | 287 | 6,229 | 1,235 | 975 |
| water supply | 209 | 6,195 | 1,464 | 1,097 |
| sewage disposal | 288 | 6,234 | 1,464 | 1,096 |
| year built | 168 | 2,358 | 1,256 | 995 |
| house type | 0 | 1 | 1,462 | 1,078 |
| radon flag | 286 | 4,055 | 876 | 452 |
| water test flag | 0 | 507 | 397 | 214 |
| copy to broker | 0 | 0 | 320 | 227 |
| paid | 0 | 0 | 0 | 97 |
| comment | 0 | 0 | 33 | 45 |

The paid flag was never used before 2015 and barely after. Zip is missing on about a third of the oldest rows and nearly two thirds of the 1996 to 2008 rows.

## Contacts

v2 kept one contact row per job: 9,444 client rows, 1,748 broker rows, 128 attorney rows. The migration to WordPress merged them: 11,316 rows became 9,070 WordPress contacts. The merge decisions are recorded per row (copied, merged, merged after moderation).

Properties went through the same process: 8,293 copied, 952 merged into an existing property, 113 copied after moderation. That confirms what part 1 could only suggest: **the migration deduplicated properties.**

**Email is a usable key only for recent clients.** Client rows with an email, by decade of the job:

| Decade | Client rows | With email | With a phone | With a second person named |
|---|---|---|---|---|
| 1980s | 91 | 15 | 84 | 91 |
| 1990s | 2,167 | 40 | 1,919 | 2,093 |
| 2000s | 4,539 | 1,219 | 4,226 | 4,346 |
| 2010s | 2,413 | 2,263 | 2,072 | 540 |
| 2020s | 222 | 217 | 171 | 30 |

Among client rows that have an email, 2,708 emails occur once and 428 occur on two or more rows (the largest groups are 17 and 19, which will be an agent's or an office's address, not a person's).

**The "couple" finding in part 1 needs narrowing.** v2 has columns for a second person (`FirstName2`, `LastName2`), filled on about 96 percent of client rows up to 2009 and on 14 to 22 percent since. So a second named person is the rule in the old data and the exception now. The data model needs room for two people on a client; it does not need a household structure.

In WordPress today: 9,741 contacts; 4,682 have an email (4,429 distinct); 3,359 a mobile number; 2,983 a work number; 910 a company.

## The current system's own records (v3, since 2020-11-24)

- 778 appointments; 771 linked to a report and to a form entry.
- **Reports: 774, of which 106 are compiled inspection reports** (6 in 2020, 65 in 2021, 34 in 2022, 1 in 2024) **and about 668 are consult letters.** This replaces part 1's estimate of 100 to 130 compiled.
- Report bodies average about 30,000 characters of markup in the inspection years and about 7,000 to 8,000 since 2023.
- The stamp choice is recorded on 331 reports.
- Appointments, invoices and properties have no body text at all. There are no old reports hiding in them.
- 3,638 media attachments; 14,391 revisions holding 85 MB.
- Invoices: every legacy invoice is marked paid (9,434, set by the migration). In v3, 131 are marked paid, 216 unpaid, and about 430 have no paid value at all. The paid flag is not being kept.
- Property facts in v3-era rows (632 properties): year built on 420, square footage on 358, sewage on 164, water supply on 126. That fits Peter's "I leave those blank now". [rec_8d15ed467e 2026-09-29 18:57]
- Form entries: 2,569 since 2020-09-08 (new appointment 870; the email form 1,045).
- Links between records are stored two ways: plain IDs on the migrated rows, serialized arrays on rows made in v3. Any reader must handle both. [doc:survey-hdonline.md §9 item 41]

**The post date is the job date.** Checked: the year in the appointment-date field equals the post year on 10,209 of 10,212 appointments. Part 1's year table stands.

## The 2008 gap, by month

| Month | Jobs |
|---|---|
| 2007-09 | 26 |
| 2007-10 | 38 |
| 2007-11 | 20 |
| 2007-12 | 1 |
| 2008-01 to 2008-09 | 0 |
| 2008-10 | 6 |
| 2008-11 | 4 |
| 2008-12 | 2 |
| 2009-01 | 8 |
| 2009-02 | 15 |
| 2009-03 | 19 |
| 2009-04 | 18 |
| 2009-05 | 18 |
| 2009-06 | 48 |

None of the twelve 2008 rows has a type or a fee; 89 of 2009's 263 have no type. At the surrounding rate of 20 to 40 jobs a month, the ten empty months are roughly 200 to 350 jobs. An estimate. What happened in December 2007 is not on disk; the shape (a clean stop, a gap, a restart with fewer fields) is what a change of system looks like. Whether that is the move off the Access booking database is a question for Gordon. (Answered the same night: "2008 is probably when v1 launched, replacing the Access DB." [gordon 2026-10-01] Probable, in his word; the file dates in `legacy-sources.md` agree.)

## A first look at v2, live

`hdonline.homedirections.net/hdonline/` answers (after a brief automatic browser check) with "Home Directions, inc. - Proprietary Report Editing System by Gordonium Enterprises - v2". Its front page has a "Select Client" list of the latest 100 jobs, the newest from November 2020, a "New Client" link and a "Manage Notes" link. **Nothing was clicked or submitted.** Given the bug Gordon described, in which unchecking a note in one report deleted it from every report [gordon 2026-10-01], v2 is to be read from its database, not operated through its pages. The tab is closed.

## What is still missing, and where it must be

| Wanted | Where it is | State |
|---|---|---|
| v2 report bodies: the notes chosen per report, and the notes library as it was | v2's database, `homedire_hdo_a2` | live, not read; host unknown |
| The notes deleted by the 2015 bug | backups of that database from before and after | location unknown |
| v1 "legacy" | backups | location unknown; "might be able to re-assemble" [gordon 2026-10-01] |
| The Access booking database and the Word files | Gordon's or Peter's disks | location unknown |
| Jobs from December 2007 to mid-2009 | possibly the Access database or v1 | unknown |
| How the 2020 migration mapped and merged | the "CLC HDOnline Data Migrator Utility" plugin on the clone | readable over SSH; not yet read |

## What this changes

1. **Migration source.** For the 9,442 legacy jobs, v4 reads `REPORTS` and `CONTACTS` (clean columns, with the WordPress IDs as a cross-check), not post meta. For the 770 v3 jobs it reads WordPress.
2. **The data model gains what v2 already had:** a second person on a client; an inspector on a job (three in the history); the fee as charged; the property facts as recorded then. And it keeps each record's old identifiers (v2 report ID, client code, WordPress post ID) so that every old link and every later audit can find its row.
3. **Dedup:** email for clients from about 2010 on; name and phone and address before that. The 2020 merge decisions are evidence, to be reviewed, not redone blind.
4. **Phase 2's real work is an audit of sources outside this database**, as Gordon said: v2's own database and every backup of it, v1, Access, Word. That needs a list of where the backups are. It is the next thing to ask him for.
5. **Report printing:** 106 compiled reports and about 540 consult letters older than the year that moves to Google Docs. For the 9,442 older jobs the report has to come from v2 (rendered from its database), not from WordPress.
6. **"Paid"** is not history worth migrating as fact: before 2015 it was never recorded, and the migration set every legacy invoice to paid.
