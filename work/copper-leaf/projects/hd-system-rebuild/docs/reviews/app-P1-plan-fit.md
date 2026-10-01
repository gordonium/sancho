---
name: Home Directions v4 review, app stage P1, plan fit
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of the app skeleton (step C) against the plan and the requirements: the data model table by table, the duplicate prompts and change history as they actually behave, the builder's twenty decisions, the real test, lint and analysis numbers, the rules that have no test, and what is not idiomatic; 24 numbered findings, each with file and line, the evidence, the fix and a weight
sources: ["[doc:build-handoff.md]", "[doc:plan-v2.md sections 2, 4, 5, 6, 7, 10]", "[doc:requirements.md R1 to R9]", "[doc:phase0-brief.md, Plan questions 4 onward]", "[doc:laravel-kit-spec.md D1, D9, section 4, section 7]", "[doc:build-log-app.md]", "[doc:census-part2-2026-10-01.md, counts only]", "[code:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 7eb7d60, read 2026-10-02]", "[run 2026-10-02 01:31 to 01:44 CEST: herd composer test, lint, analyse; 20 reviewer probes on invented data, in memory, from a scratch folder outside the app]"]
status: written 2026-10-02, finished 01:46 CEST, by a reviewer that did not write the code; 1 blocker, 13 should-fix, 10 minor; no code was changed, nothing was committed, nothing else was written; no client data was opened
---
# Review: app stage P1 (the skeleton), plan fit

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write the code and I changed none of it.

**The conclusion first.** The skeleton is what the plan asked for and it is well made. All eleven tables are there, the three logins work, the Dashboard and the File screen take entry by hand, the duplicate prompts never merge by themselves, and every correction is recorded with who, old and new. The tests are real: they test rules, not that pages load. One thing is wrong enough to stop on before mail is built: choosing "same" throws away what was just typed and keeps the older details, so the next stages would send an invoice to an old address. Thirteen things should be fixed, most of them before the import runs, because the tables refuse or misdescribe parts of the old data. Ten are small.

Weights: **blocker** is wrong behaviour or a wrong foundation; **should-fix**; **minor**.

## The numbers, run by me

In `/Users/gordonium/Dev/clc-laravel/hdonline-v4`, branch `feature/v4-build`, commit `7eb7d60`, working tree clean before and after, PHP 8.5.10 through Herd.

| Command | Result |
|---|---|
| `herd composer test` | passed: 302 tests, 935 assertions, 0 failed, 3.1 s |
| `herd composer lint` | passed (Pint, check only) |
| `herd composer analyse` | passed: 0 errors (Larastan level 8) |

These match the build log exactly. `git log` shows 8 commits, the last `7eb7d60`.

**How the findings were checked.** Where a finding says something happens, I ran it. The probes are three PHPUnit files of invented data, kept outside the app in the session's scratch folder and run against the app's own test setup (in-memory database, no network): `herd php vendor/bin/phpunit --do-not-cache-result <scratch>/ReviewProbeTest.php` and three more. 20 probes, all ran. Each finding quotes what its probe printed. Nothing was written inside the app folder.

---

## Blocker

### 1. "Same" keeps the older record and drops what was just typed

**Where.** `app/Actions/MergeDuplicate.php:27-38`; the wording on the screen at `resources/views/files/show.blade.php:23` and `:35`; decision 5 in the build log.

**What is wrong.** New File always makes a new client and a new property (`app/Actions/OpenFile.php:36-37`). When the prompt is answered "same", the file is moved to the older record and the newer one is marked as a duplicate. Nothing is carried across. So the email, phones, zip, state and year built that were typed today (or that Calendly will supply from the booking) disappear from the file, and the file shows whatever the older record holds. After the import the older record is usually a WordPress row from years ago. Stage E will mail the invoice and the letter to that record's email.

**Evidence.** Probe E1, through the real routes: an older client with email `ada.old@example.test` and a property with no zip, no state and no year; a New File typed with `ada.new@example.test`, zip 06877, CT, 1962; "same" clicked for both.
- `file client email after "same": ada.old@example.test (typed today: ada.new@example.test)`
- `file property after "same": zip=NULL state=NULL year_built=NULL (typed today: 06877, CT, 1962)`
- the file page no longer contains the new email anywhere; the kept record has 0 history rows from the merge.
The typed values are not destroyed (they sit on the duplicate row), but no screen shows them. Plan: a correction must be "right everywhere" [R2.3]; the census says email is the reliable key only from about 2010, so old rows are exactly the ones with stale or missing details. [doc:census-part2-2026-10-01.md, Contacts]

**The fix.** Keep the older record as the one kept (that part is sound: its files and its sources stay put). On "same", through the model so each change lands in the history: fill every blank on the kept record from the duplicate; where both have a value and they differ (email, the three phones, the mailing address; zip, state, year built), show the two side by side on the file with one click to use today's. Test: the E1 case, asserting the file shows today's email after one further click and that the history holds old and new.

---

## Should-fix

### 2. The prompt is asked in one direction only, by row number

**Where.** `app/Matching/ClientMatcher.php:33`, `app/Matching/PropertyMatcher.php:33` (`where('id', '<', ...)`); decision 5.

**What is wrong.** "Newer" means "higher row number". Two cases break that.
- Peter corrects a misspelt email on an older file so that it now equals a newer client's. The file he is looking at shows nothing; the prompt appears only on the other file. Probe E8: `prompts on the file he is looking at = 0; on the other file = 1`.
- Phase 2 loads older jobs after cutover. Those rows get higher numbers than clients created in the live system, so a 1995 record becomes "the newer one": the prompt shows only on the old file, and "same" would keep the 2026 record and mark the 1995 one as its duplicate. [doc:plan-v2.md section 4, "Phase 2 can load into it without changing it"]

**The fix.** Suggest in both directions (drop the `id <` condition, keep "not itself, not merged, not kept apart"). Let the action decide which record is kept by a stated rule (the one with the earliest job, falling back to the lower number), whichever file the answer is given on. Tests for both cases above.

### 3. A merge and a "keep separate" cannot be undone, and the history cannot tell which rows belong to one merge

**Where.** `app/Actions/MergeDuplicate.php`, `app/Actions/KeepApart.php`, `app/Enums/HistoryEvent.php:9-11`, `routes/web.php:30-39` (no undo route).

**What is wrong.** The plan answers the risk of a wrong merge with "reversible through the history". [doc:plan-v2.md section 10] The data needed is recorded (probe U rebuilt the list of moved files from the history alone and it matched). But there is no undo for either answer, and a merge is written as ordinary "updated" rows: `events in the history: ["created","updated"]`. An undo has to guess which rows belong together by matching ids and order, which stops being safe once a pair has been merged, undone and merged again. A wrong click on "Different: keep separate" is permanent and invisible.

**The fix.** A `merged` event on the duplicate (new value: the record kept) and one shared batch identifier on every history row a single act writes. Then stage P3 builds "undo this merge" by replaying the batch backwards, and "ask again" for a kept-apart pair by marking the `kept_apart` row as withdrawn (a mark, not a removal). Tests for both.

### 4. Hiding a file writes nothing to the history

**Where.** `app/Models/Concerns/RecordsHistory.php:23-31` (listens to `created` and `updated` only); decision 14.

**What is wrong.** Laravel's soft delete does not fire `updated`. The plan's history covers "delete and restore". [doc:plan-v2.md section 5, the change history] The build log says history is written "on every create and every changed field".

**Evidence.** Probe E2: after `delete()` the file's history is one row, `created`. After `restore()` a row appears for `hidden_at` going from a time to nothing. So a restore is recorded and the delete it reverses is not, and nobody is named as having deleted the file.

**The fix.** Listen for `deleted` and `restored` on models that use soft deletes and write `hidden` and `restored` events with the user. Test both. Do it now, before stage P3 adds the button.

### 5. `files.service` cannot hold what the old jobs are

**Where.** `database/migrations/2026_10_02_000003_create_files_table.php:22` (required); `app/Enums/Service.php:9-11`; `app/Models/File.php:113`; `app/Enums/Service.php:25-28` and `app/Models/Setting.php:44` (a config lookup per case that throws when the case has no entry).

**What is wrong.** v2's 9,442 jobs are 7,144 inspections, 2,181 consultations, 116 with no type and one other. [doc:census-part2-2026-10-01.md, Job types] The column refuses an empty type, and the enum knows only opinion, design and hourly. The build log says "only the `Service` enum grows", but the enum also feeds the New File list, the standard prices and the Settings texts, so new cases would be offered for new files and would throw when their price is looked up.

**Evidence.** Probe E6: `file with service null: refused (NOT NULL constraint failed: files.service)`. Probe E5: a file whose service is `inspection` opens with HTTP 500.

**The fix.** Make `service` nullable, as `mode` already is for the same reason (decision 11). Add `Inspection` and `Consultation`. Give the enum an `offered()` list of the three sold today, and use it for the New File form, the config and the Settings tests. Show "Not recorded" for an empty one. Test: a file of each old kind, and one with none, opens on the Dashboard and the File screen.

### 6. A job with no address cannot be stored without inventing one

**Where.** `database/migrations/2026_10_02_000002_create_properties_table.php:15` and `:23` (street and address key required); `..._000003_create_files_table.php:21` (property required).

**What is wrong.** 86 of v2's 9,441 dated jobs have no address (1 before 1996, 6 in 1996 to 2008, 15 in 2009 to 2014, 64 since). [doc:census-part2-2026-10-01.md, fields by era] The builder's own rule is that an invented value would be a false fact (decision 11). Probe E6: `property with no street: refused`, `file with no property: refused`.

**The fix.** Make the street and the key nullable and keep the file's property required: a property row with a town and no street is still true. The matcher already skips an empty key (`PropertyMatcher.php:27`). `oneLine()` says "Address not recorded" when there is nothing. Test it.

### 7. Old invoices have no number, and the column demands one; the number rule itself is not yet enforced anywhere

**Where.** `database/migrations/2026_10_02_000005_create_invoices_table.php:20`.

**What is wrong.** Two things. First, "current invoices dont' have any numbers" [gordon 2026-10-01, phase0-brief Q10], and cutover brings invoices across for every migrated letter [doc:plan-v2.md section 6 step 2]. With the column required, the importer must mint `HD-` numbers for invoices that never had one. Second, the column is unique, which is right, but nothing checks the shape: probe E6, `invoice number in any shape (HD-1): ACCEPTED`. No generator exists yet (that is stage P2), so the rule "year, month, three random digits, unique" has no code and no test today.

**The fix.** Make `number` nullable (uniqueness still holds for real numbers) and leave imported invoices without one, or have Gordon say that old invoices get new numbers. In P2: one generator, with tests for the shape `HD-YYMM-NNN`, for a retry when the random number is taken, and for what happens when a month's thousand is used up.

### 8. The same source can be recorded twice, so a rerun of the import can double its own records

**Where.** `database/migrations/2026_10_02_000009_create_sources_table.php:23` and `:30`; `app/Models/FileContact.php`, `app/Models/Invoice.php` (no `sources()`).

**What is wrong.** The index on system, collection and identifier is not unique. The kit requires the import to be "safe to run twice". [doc:laravel-kit-spec.md section 4, data migration row] Probe E6: `same source recorded twice for one row: ACCEPTED`. Also, every imported row must record where it came from [doc:plan-v2.md section 4], and the plan imports "who was copied" and invoices, but only Client, Property and File have the `sources()` relation.

**The fix.** A unique index on row type, row id, system, collection and identifier, with `collection` required (empty text when there is none, because an empty value defeats a unique index). One small `HasSources` trait on Client, Property, File, FileContact and Invoice. Test that the second write is refused.

### 9. The forms fill blanks with Connecticut and "site visit" without being asked

**Where.** `resources/views/files/_property-fields.blade.php:18` (`?? 'CT'`); `resources/views/components/field.blade.php:28-30` (a select has no empty choice); `resources/views/files/show.blade.php:135-137`.

**What is wrong.** Two consequences of one default.
- On an old record with no state, the correction form arrives with Connecticut chosen. Saving any correction writes CT as if Peter had said so. On a file with no mode, no option is selected, so the browser sends the first one. Probe E4: `property with no state: the correction form preselects CT`; `mode after saving the Job panel with only the status changed: 'site'`. Probe C, a street correction sent as the form sends it: `state after the street correction: 'CT'; history: state NULL -> 'CT' by user the person signed in`. Both land in the history under his name. That is the false fact decision 11 set out to avoid.
- On New File the state also starts at CT. The stamp follows the state [doc:phase0-brief.md Q9]. A New York address typed with the select forgotten gets a Connecticut stamp.

**The fix.** On the correction forms, an empty first choice whenever the stored value is empty, and `mode` allowed to stay empty in `UpdateFileRequest`. On New File, no default state: he picks it. Tests for both.

### 10. A cancelled file stays on the working list

**Where.** `app/Models/File.php:101-105` (the `recent` scope); `app/Http/Controllers/DashboardController.php:17`.

**What is wrong.** Gordon agreed that a cancelled file "leaves the working list but stays findable". [doc:phase0-brief.md Q5] The status can be set to cancelled by hand today. Probe E3: a cancelled file is listed on the Dashboard, with "Nothing to do" beside it.

**The fix.** The Dashboard list leaves out cancelled files; "been here before" and search (P3) still show them. A test beside the existing "leaves out files that were deleted".

### 11. Nobody can see or enter the other people on a job

**Where.** `routes/web.php` (no route), `resources/views/files/show.blade.php`, `resources/views/files/create.blade.php` (no field); `app/Models/FileContact.php` (no history).

**What is wrong.** The table for brokers, attorneys and others who are copied exists and nothing uses it. Step C is "File with entry by hand". [doc:plan-v2.md section 7] The import brings 1,748 broker rows and 128 attorney rows [doc:census-part2-2026-10-01.md, Contacts], and stage E decides who gets a copy from this table. Probe E17: a broker put on a file is not shown on the file screen, and New File has no field for one. A change to who is copied is also not in the history.

**The fix.** A small panel on the File screen: add a person with a role, correct them, tick "copied", take them off (a mark, since nothing is destroyed). `RecordsHistory` on `FileContact`. Tests.

### 12. There is no way to make a login on a server

**Where.** `database/seeders/UserSeeder.php:20-24`; `routes/console.php` (only the skeleton's `inspire`).

**What is wrong.** The seeder rightly refuses to run outside local and testing, and says "a server gets its users another way". There is no other way: no command, no screen, and the kit forbids tinker on a server. [doc:laravel-kit-spec.md section 6, item 5] Step C's gate is "usable by hand on staging". [doc:plan-v2.md section 7] There is also no way to change a password or switch a login off.

**The fix.** One artisan command, `hd:user`, that creates or updates a person by email with a role and a password typed at a hidden prompt, with tests. It covers password changes until Settings has its users panel. A `deactivated_at` column when that panel is built, since a user with history rows can never be removed.

### 13. One status line for two things that happen in either order

**Where.** `app/Enums/FileStatus.php:25-35`; `app/Http/Requests/UpdateFileRequest.php:33`; decision 20.

**What is wrong.** The status runs booked, visited, drafting, sent, paid, closed. Sending the letter and being paid are separate events and payment often comes first. The "next thing to do" is read off the status alone, and the status is typed by hand. Probe S: a file marked paid by hand, with no invoice row and no letter, shows `next step = "Close the file"`. Once P2 adds `invoices.paid_at`, "paid" will be recorded in two places that can disagree.

**The fix.** For P2 to settle before it builds on this: work out the next step from facts (invoice sent, invoice paid, letter sent), let the status follow those events, and keep the hand-set choices to the ones only a person knows (visited, closed, cancelled).

### 14. Important rules with no test

**Where.** `tests/`.

**What is wrong.** The suite is good (see "The tests, judged" below). These rules have nothing guarding them:
- **Nothing is destroyed.** Only the file's soft delete is tested. Probe D: `Client::delete()` removes the row; `HistoryEntry::delete()` removes the audit row; `File::forceDelete()` removes the file for good. No guard, no test.
- **The shape of the tables.** `SchemaTest` checks that columns exist. Nothing tests that an invoice number is unique, that a file has one invoice, that a Calendly booking can exist once, or that a file cannot point at a client that is not there. (All four hold today; probe E6. A later migration could drop any of them unnoticed.)
- **Old-shaped rows on the screens.** The factory always fills mode, price and description. No test opens a file that lacks them, which is how finding 9 got through.
- **Hide and restore in the history** (finding 4), **what a merge does with differing details** (finding 1), **cancelled files on the list** (finding 10).
- **The lazy-loading guard on "been here before".** The build log says list tests seed at least two rows so a lazy load fails the suite. `tests/Feature/Files/FileScreenTest.php:251-272` puts one visible file in each of the two lists, and Laravel's guard only fires on two or more. A lazy load there would pass.

**The fix.** A `deleting` guard on Client, Property, Invoice, Send and HistoryEntry that throws, and one on File's force delete, each with a test. A constraint test per rule above. A `legacy()` factory state (no mode, price, description, state, zip) used on the Dashboard and File screen tests. A second file in each "been here before" list.

---

## Minor

### 15. Holes in the address key

**Where.** `app/Support/AddressKey.php:57` and `:66`; `app/Matching/PropertyMatcher.php:58`, `:67-70`; decision 6.

Leaving state and zip out of the key is right for this data: zip is missing on nearly two thirds of the 1996 to 2008 rows. The holes are elsewhere. Probes E10 and M:
- an apostrophe becomes a space: `[12 st johns rd|ridgefield] vs [12 st john s rd|ridgefield]`, so "St. John's Rd" never meets "St Johns Road";
- a bare unit number: `[12 main st 2|...] vs [12 main st unit 2|...]`;
- a state typed into the town box: `[...|ridgefield] vs [...|ridgefield ct]`;
- a hamlet against its town (`s salem` against `lewisboro`): only the geocoded key can solve that one;
- when two records disagree on the state the match is hidden, so one mistyped state hides a true match (`CT on one and NY (a slip) on the other: prompts = 0`).

**The fix.** Delete apostrophes before other punctuation becomes a space; treat a second line that is only a number as a unit; strip a trailing state from the town. When the states disagree, still suggest, and say so in the reason ("Same address, different state on record").

### 16. Client matches that are missed

**Where.** `app/Matching/ClientMatcher.php:57`; `app/Models/Client.php:136`; `app/Support/Phone.php:22`.

The name key is the first person's name only, and phones are compared whole. Probe M: an old record "Cal & Dee Reed" and a new booking by Dee Reed on the same phone: `prompts = 0`. A second person is named on about 96 percent of client rows up to 2009. [doc:census-part2-2026-10-01.md] An old number without its area code against the same number with it: `prompts = 0`.

**The fix.** Compare the new name with both people on the old record; compare the last seven digits when either number has only seven. The rule "a name alone is never enough" stays.

### 17. "Keep separate" does not follow a merge

**Where.** `app/Models/KeptApart.php:40-49`; decision 4.

The table itself is the right tool: history is a record, not a place to look things up. One gap. Probe E9: A is kept apart from B, then B is merged into C; A is asked again, about C. Arguably fair, since C is another row, but he has already answered it once.

**The fix.** When a record is merged, copy its kept-apart pairs onto the record kept (inside the same transaction, same batch).

### 18. Old-shaped records refuse a correction until unrelated blanks are filled

**Where.** `app/Validation/ClientFields.php:23`, `:36`; `app/Validation/PropertyFields.php:24-26`; `app/Http/Requests/UpdateFileRequest.php:36`.

Probe F, on rows shaped like old ones: correcting only the email of a client that has a display name and no last name is refused (`last_name ... required`, and the zip format if the stored zip is not five digits); correcting only the street of a property with no town or state is refused (`city`, `state` required); saving an invoice description on a file with no price is refused (`price required`). Each error is shown, so he can get through, but R2.2's one-step fix becomes several. Whether real zips are malformed I did not look; that is for the import rehearsal to count.

**The fix.** On the correction forms only, require a field when it was already filled; leave New File strict.

### 19. Two things the importer must know about the Client model

**Where.** `app/Models/Client.php:132-139`, `:146-158`; `app/Models/Concerns/RecordsHistory.php:16-17`.

- A display name that is set and differs from the composed one is treated as typed by a person and never follows a correction. Probe E16: imported as "Smyth, John", surname corrected to Smith, display name stays `Smyth, John`. The importer should leave the display name empty unless the old system truly had a separate one.
- The matching keys, the display name and the history are all written by model events. An import that inserts in bulk for speed skips them: the name key would be empty and those clients would never be suggested. Probe H: three kinds of change that bypass the model `wrote 0 history rows`.

**The fix.** Say both in the P4 plan; a test in P4 that an imported client is found by the matcher.

### 20. One invoice per file (decision 9)

**Where.** `..._000005_create_invoices_table.php:19`; `app/Models/File.php:75-78`.

Sound for the two flat-fee services. Hourly design work is billed "during [period]" [R4.3], which reads as more than one invoice on one project. With this rule a second period needs a second file, which means a second client and property row and two "same" clicks each time. Probe E6: `second invoice for one file: refused`.

**The fix.** Ask Gordon in the morning. If the answer is "sometimes", drop the unique rule now, while no data exists, and make the relation "the latest invoice".

### 21. `sends` has one recipient and no failure

**Where.** `..._000006_create_sends_table.php:21`.

The plan's columns are all there. Two things P2 will meet: brokers and attorneys who are copied, and the copy to the office mailbox [doc:plan-v2.md section 5, Mail], have no place unless each recipient is its own row; and a bounce, which is the most useful thing a "return receipt" can say, has no column.

**The fix.** P2 decides one row per recipient or a `cc` column, and adds `failed_at` with a reason.

### 22. The history cannot say which source a Phase 2 replacement came from

**Where.** `..._000008_create_history_table.php:17-26`.

The plan wants Phase 2 to "replace a WordPress-sourced value with a better one from an older source and show that it did", without changing the tables. [doc:plan-v2.md section 4] A history row can show old and new, but its only "who" is a user. `sources` is per row, not per field.

**The fix.** A nullable `source_id` on `history`, added now while it costs nothing.

### 23. No indexes on the columns that link the tables

**Where.** `..._000003_create_files_table.php:20-21`; `..._000004_...:19`; `..._000006_...:19`.

SQLite does not index a foreign key by itself. Measured, it does not matter yet. Probe E12, with 9,000 clients, 9,000 properties and 10,200 files: Dashboard 5 ms (3 queries), File screen 5 ms (9 queries), the plan for "files of one client" is a full scan. Search in P3 will join on these.

**The fix.** Index `files.client_id`, `files.property_id`, `file_contacts.file_id`, `sends.file_id` in one migration.

### 24. Idiomatic Laravel: three small things

**Where.** `app/Http/Controllers/FileClientMatchController.php` and `FilePropertyMatchController.php`; `app/Matching/ClientMatcher.php` and `PropertyMatcher.php`; the `merged_into` columns; `config/database.php:43-46`.

The code is idiomatic and reads well: thin controllers, form requests, policies by attribute, actions, enums, a morph map, strict models. Nothing fights the framework. Three things the next stages will live with:
- The two match controllers are the same file twice, and the two matchers share their whole skeleton. Fixing finding 2 means making each change twice. One controller and one base matcher would do.
- The column `merged_into` and the relation `mergedInto` become the same key when a model is turned into an array, so the loaded relation overwrites the id (probe A: with the relation loaded, `merged_into` in the array is an array, not a number). Harmless on Blade pages; a surprise the first time a model is sent as JSON. `merged_into_id` is the convention.
- SQLite is left at its defaults (`busy_timeout`, `journal_mode` empty, deferred transactions) while sessions, cache and the queue all write to the same file. Stage E adds a queue worker and stage F a job every 15 minutes. Laravel's own advice for that is write-ahead logging, a busy timeout and immediate transactions. This belongs to the deploy reviewer; noted so it is not lost.

---

## The data model against plan section 4

| Table | Verdict |
|---|---|
| `users` | As planned; `role` for the three. No way to create one on a server (finding 12). |
| `clients` | As planned: two people, display name, email (indexed), three phones, mailing address, company, notes, `merged_into`. Names nullable for old rows. Sound. |
| `properties` | As planned, with both keys and `year_built` nullable. Street and key are required: finding 6. |
| `files` | Every planned column, `invoice_description` included; both Calendly identifiers unique; `hidden_at` as the soft delete; list index on date and id. `service` required and three-valued: finding 5. Link columns not indexed: finding 23. |
| `file_contacts` | Role, name, email, phone, copied. Unused by any screen, no history, no sources relation: findings 8 and 11. |
| `invoices` | Number unique, description as issued, lines, subtotal, discount, total, issued, paid, paid by, PDF. Number required and unshaped: finding 7. One per file: finding 20. |
| `sends` | Every planned column. One recipient, no failure: finding 21. |
| `settings` | Key and value; code defaults behind it. Sound. |
| `history` | Who, what, old, new, when, by short type names. No hide event, no merge event or batch, no source: findings 3, 4, 22. |
| `sources` | System, collection, identifier, imported, verified, by whom; any row type. Not unique: finding 8. |
| `old_links` | Old address unique, new address or a record. Sound. |
| `kept_apart` (added) | Sound; finding 17. |

Foreign keys are enforced (probe E6: a file pointing at a client that does not exist is refused). No delete cascades anywhere, which is right for "nothing is destroyed".

## The twenty decisions

| # | Decision | Verdict |
|---|---|---|
| 1 | Blade and Tailwind, one small script | Sound. Closes nothing: letters, PDFs, Brevo, Calendly and search are all server work. |
| 2 | Login by hand | Sound for three people. Needs finding 12. |
| 3 | Work on `feature/v4-build` | Sound; it is kit decision D2. |
| 4 | The `kept_apart` table | Sound. Findings 3 and 17. |
| 5 | Ask on the newer record; "same" keeps the older | Keeping the older is right; dropping the newer's details is the blocker (finding 1); "newer" by row number is finding 2. |
| 6 | Address key without state and zip | Sound for this data. Holes in finding 15. |
| 7 | No geocoder yet | Sound; the column and the rule are ready. |
| 8 | `file_contacts` holds its own names | Sound, and it matches v2, which kept one contact row per job. Cost: a broker's corrected email is right on one file only. Finding 11. |
| 9 | One invoice per file | Open question for hourly work: finding 20. |
| 10 | `sources.collection` | Sound and needed. Finding 8. |
| 11 | Nullable mode, price, description, names | Sound, and not carried far enough: findings 5, 6, 7, 9. |
| 12 | `scheduled_at` required | Sound: the census found the post date is the job date on 10,209 of 10,212 appointments. Probe E6 confirms the column refuses an empty one, so the importer must list a job with no date, not guess one. |
| 13 | UTC stored, New York shown | Sound. P3's month search must cut the month on the firm's clock; P4 must read old dates as New York dates. |
| 14 | Soft delete on `hidden_at` | Sound. Finding 4. Stage F must look among hidden files too when Calendly reports a booking again, or the unique rule will stop it with an error. |
| 15 | History recorded now, shown later | Sound. Findings 3 and 4. |
| 16 | Whole cents; defaults in config | Sound. Prices live only in config, so a fee change is a deploy; the plan's Settings lists texts, not prices. For hourly work `files.price` holds the hourly rate, not a total: P2 must say where the hours go. |
| 17 | Invented seeded logins, refused on a server | Sound. Finding 12. |
| 18 | Boost required, not installed | Sound; matches D8. |
| 19 | Larastan level 8 | Sound; it passes. |
| 20 | Status set by hand | Fine as a stopgap. Findings 10 and 13. |

None of the twenty closes a door the plan needs open.

## The tests, judged

They test behaviour. Of the 302, the bulk are rules stated both ways: every matcher rule has a match and a non-match; the merge is tested for moved files (hidden ones included), flat chains and refused nonsense; corrections are tested for the saved value, the history row with old, new and user, and the same value showing on a second file; New File is tested for defaults per service, stamp per state, the firm's clock and refused input by field; the list is tested for order, paging to the end and working with scripts off. The route test fails when a route is added without a guest check and a policy check. Three are page-load checks at most. What is missing is in finding 14.

## Outside my lens, noted once

`storage.local` (`/storage/{path}`, Laravel's signed file route) is on, and `AccessTest` exempts it. Stage E will store invoice and letter PDFs. Whether those can be reached by address is the security reviewer's question.
