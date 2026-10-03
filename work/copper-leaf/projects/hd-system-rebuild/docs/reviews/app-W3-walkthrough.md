---
name: Home Directions v4 check W3, the everyday screens on the real history
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Smoke run of the everyday screens over the real imported records (all 10,206 files, the Dashboard and its scroll, 199 searches, the old invoices' PDFs, the change history, Settings), the timings in the app and through Herd's web server, a static check of the built stylesheet against today's views, and Peter's everyday actions on one invented file made in the app and left deleted; 9 numbered findings with weights, counts and record IDs only
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 1063e6c, served at http://hdonline-v4.test on the rehearsal database]", "[doc:build-handoff.md sections 3 and 4]", "[doc:build-state.md, 00:50 Oct 3]", "[doc:build-log-app.md, W1 and W2]", "[doc:plan-v2.md section 5]", "[run: throwaway PHP scripts through the app's own HTTP kernel, read-only (SQLite query-only on the checker's connection, total_changes 0), 2026-10-03 01:25 to 01:50 CEST]", "[run: Herd's web server with a session made by the app's own session store for local login #1, 2026-10-03 01:38 to 01:45 CEST]", "[run: Tailwind 4.3.3 compile of today's views from the app's node_modules, output kept outside the repository]"]
status: written 2026-10-03 01:55 CEST by a checker on Opus 5.5 (effort level not visible to it) that wrote no app code, changed nothing in the app repository (git status clean at 1063e6c) and committed nothing. 1 blocks normal use (a setup step, not code), 2 should fix, 6 minor. Counts, record IDs, field names and class names only; no name, address, email, phone, letter or invoice text of a real record appears here. The throwaway scripts were deleted afterwards.
---
# W3: the everyday screens on the real history

## In a minute

**Does the app work on Gordon's real history when used as it should be? Yes, with one setup step before letters go out.**

- All **10,206** imported files open: 10,206 answers of 200, **no exception**, every section of the File screen present. Where the old data has a gap, the screen says so ("None on file", "Address not recorded", "Not recorded"); only **1** screen shows a required part blank (finding 8).
- The Dashboard loads and scrolls through **all 10,206** files in the database's order, no file twice, none missing. **199 searches** (44 months from 1983 to 2026, 10 other ways of typing a month, 5 years, 40 surnames, 20 full names, 40 streets, 40 whole address lines) each listed exactly the files they should.
- Settings loads with every section. Nothing is slow: the slowest screen took **40 ms** inside the app and **33 ms** through the web server (the two-second line is 50 times that).
- On one **invented** file, every everyday action worked through the real web server: New File by hand, corrections, the invoice description, the letter (stand-in), sending the letter and the invoice, the PDFs, mark paid, resend, delete and restore. The file is **left deleted**, so it is not on Peter's Dashboard; it is under "Deleted files".
- **The one thing that stops a normal action is setup, not code:** the Connecticut and New York stamp images are not in Settings, so a letter carrying a stamp is refused (with a clear message) until they are uploaded (finding 1).
- **Should fix:** saving an old client whose state is stored as words quietly empties the state (34 clients, finding 2); the stylesheet predates the newer screens (25 classes in 10 views, details only, one rebuild, finding 3).
- **Minor:** old emails a browser refuses stop "Save the client" on 119 clients until fixed; an unhandled mail refusal that today's data cannot reach; "Create the letter" offered on every old file; old properties with a state in words; gaps in the old data; on this Mac the message log reads "sent to" the client's own address although nothing left the Mac.

## Findings

### 1. The stamp images are not in Settings, so a letter with a stamp cannot be sent. Weight: blocks normal use until set up (no code change)
- **What:** "Send the letter" on a file whose stamp is Connecticut or New York is refused: "This letter is to carry the Connecticut stamp and there is no image for it in Settings yet, so nothing was sent. Add the image in Settings, or choose "No stamp" on the file to send the letter without one." The Letter panel already warns: "no image for it in Settings yet, so the letter carries none and cannot be sent".
- **On how many:** every new file at a CT or NY property (the stamp follows the state; most of Peter's work). The Settings table on the rehearsal database is empty (0 rows), so no stamp image is set.
- **Evidence:** the walkthrough on the invented file (CT property): refused, one WARNING in `storage/logs/laravel.log` with that text; after setting the file's stamp to "No stamp" the letter went (to the log mailer).
- **Where:** not a defect. `app/Models/Setting.php` `stampImage()`; Settings, "Stamp images".
- **What it needs:** Gordon or Peter uploads the two stamp images in Settings. Nothing for the code fixer unless the images are handed over.

### 2. "Save the client" on an old client whose state is stored as words empties the state. Weight: should fix
- **What:** the state field on the File screen is a list of two-letter codes. Where the old record holds something else ("ct", "CT ", a full name, an abbreviation), no entry is selected, the browser sends the empty first entry, the correction rules read that as a change, empty passes, and the save stores no state. Nothing tells Peter. The change history keeps the old value, so it can be put back by hand.
- **On how many:** 34 clients on 41 files (files 40, 3972, 4628, 4700, 5048, 7412 and others; clients 39, 455, 524, 3475, 4044, 4106 and others). In 10 of the 34 the stored value differs from a code only by letter case or spaces.
- **Evidence:** for every one of the 10,206 files, the client, property, job, invoice-description and contact forms were read off the rendered page as a browser sends them (33,257 forms) and run through the app's own form-request validation in memory, then laid over the record unsaved: on exactly these 41 the client form passes validation and would change one field, `state`. Nothing was saved.
- **Where:** `resources/views/files/_client-fields.blade.php:34` (options are codes only), `app/Validation/Corrections.php:38` (the empty value counts as a change), `app/Http/Controllers/FileClientController.php:21` (saves it).
- **Fix idea:** offer a stored value that is not a code as its own entry ("as recorded"), the way the Job form keeps an old kind of job in its list; and read "ct" and "CT " as CT. The property form has the same list but refuses instead (finding 6).

### 3. The stylesheet was built before most screens existed. Weight: should fix (cosmetic; one command)
- **What:** `public/build/assets/app-C9a8RWUE.css` (2026-10-02 01:23) defines 255 classes. Compiling today's views with the app's own Tailwind 4.3.3 gives 28 classes the built file lacks; 3 of those are words in PHP code, not classes (`inline`, `invisible`, `border-collapse`), so **25 classes in 10 Blade views** are missing: `files/show` (9), `settings/edit` (11), `files/delete` (4), `stand-in/letter` (5), `stand-in/calendly` (4), `files/_contact-fields` (2), `files/_answers` (1), `files/_rows` (1), `dashboard` (1, the Calendly trouble alert), `components/layout` (1, the "could not be sent" alert).
- **By screen, as rendered:** Dashboard, New File, Login, Set your password: none missing. File screen: 6 classes on 5 to 9 elements (`font-normal`, `hover:text-red-900`, `pb-2`, `self-end`, `space-y-0.5`, `space-y-3`: the history's explanation shows bold, list spacing, the "copied" checkbox alignment). A deleted file: 6 (the red banner's border and heading colours). Delete question: 4 (its list loses bullets and indent). Settings: 4. Deleted-files list: 1 (the badge's ring). Stand-in Calendly: 1. Stand-in Doc ("Open the Doc" on this Mac): 5 (`font-serif`, `p-8`, `text-[15px]`, `whitespace-pre-wrap`, `break-all`): no padding, and **the letter's line breaks are lost**.
- **Not unstyled:** the screens keep their layout, colours and type; these are details.
- **Fix:** `npm run build` in the app folder. `public/build` is git-ignored, so a server builds its own.

### 4. Old emails a browser will not accept stop "Save the client". Weight: minor
- **What:** the email field is a browser email field. An old value with two addresses, no "@" or a space inside fails the browser's own check, so the client form will not submit at all until the email is corrected or cleared. Nothing is lost and the browser points at the field, but Peter cannot correct, say, a phone number without first fixing an email he may not have.
- **On how many:** 119 clients on 137 files (85 hold two addresses, 17 have no "@", 14 a space inside, 3 other; e.g. files 3112, 3348, 3712, 3736, 4152, 5100). Also 18 people on jobs (contacts) on 18 files, 5 of them marked copied (e.g. files 5340, 4977, 8445).
- **Where:** `resources/views/files/_client-fields.blade.php:26`, `resources/views/files/_contact-fields.blade.php:17` (`type="email"`).
- **Fix idea:** a plain text field when the stored value is not one valid address (the server's own rule still applies to a change), or move a second address into the notes at import.

### 5. A mail address the mailer refuses is not caught. Weight: minor (not reachable with today's data in normal use)
- **What:** the outbox catches transport refusals and `CannotSend` only. An address that Symfony's mail library refuses throws while the message is being built, after the message-log lines are written: the person gets an error page (500) and the lines stay "not confirmed" ("It may have gone").
- **Evidence:** with invented addresses of each shape above, through Laravel's own mail building on the in-memory array mailer: two addresses on one line, no "@", a space inside: `Symfony\Component\Mime\Exception\RfcComplianceException`; two addresses on two lines: `InvalidArgumentException`; none of them a transport exception.
- **On how many:** 0 of the 647 unpaid old invoices (the old ones that can be numbered and sent) have such a client email. It can be reached by a letter on an old file where one of the 5 copied contacts above is copied, or by a client record that keeps an old email through a merge.
- **Where:** `app/Mailing/Outbox.php:93-104`; `app/Mail/FileMail.php:112` (`recipientsOf`).
- **Fix idea:** check each address in `recipientsOf` and refuse with `CannotSend`, as for a missing address.

### 6. Old properties whose state is stored as words: the property form refuses until a state is picked. Weight: minor
- **On how many:** 11 properties on 13 files (5048, 5736, 5740, 5697, 5745, 5765 and others). Saving the property form gives the state field's error; nothing is lost; Peter picks the state. 142 properties have no state at all, and those save fine.
- **Where:** `resources/views/files/_property-fields.blade.php:19`. Same fix as finding 2.

### 7. "Create the letter" is offered on every imported file. Weight: minor (decide before go-live)
- **On how many:** 10,206 files ("This file has no letter yet." and the button). Pressing it starts a new letter from today's template for a job years old; with Google connected it makes a new Doc in the letters folder. The old letters live in v3, and the 438 since 2022-06-21 are to come by the conversion.
- **Where:** `resources/views/files/show.blade.php:473-477`.
- **Fix idea:** on a file from an earlier system, say where its letter is instead of offering to make one.

### 8. Gaps in the old data that show on the screens. Weight: minor (data; repair is Phase 2)
- **A required part blank, 1 screen:** file 9762 has a paid invoice with no wording, so its Invoice description panel shows an empty paragraph above the total. The other 19 files with no wording are unpaid and show an empty text box, which is right.
- **No price:** 48 files show "Not recorded" (e.g. 9568, 9572, 9584).
- **"Give this invoice a number":** offered on all 647 unpaid old invoices; for 63 of them there is nothing to bill and it refuses with a clear message ("This invoice has no price or no wording yet ..."). The other 584 print a PDF (see "The invoice PDF on old files" below).
- **Zip codes with four digits:** 4,019 clients on 4,681 files (CT 3,809, NJ 121, MA 63, others): the leading zero was lost in the old system and the import copied it. It shows in the mailing address and would print on an invoice or letter address block.
- **No address:** 84 properties have no address at all ("Address not recorded"); 2 of the 584 numberable unpaid invoices would print "Services at: on <date>" (files 9658, 9712).

### 9. On this Mac a message is shown as sent to the client's own address. Weight: minor (setup)
- **What:** mail is on the log mailer and no trap address is set (`HD_MAIL_TRAP` empty), so the app routes each message to the address on the file and the log mailer writes it to `storage/logs/laravel.log`; nothing leaves the Mac. The File screen then reads "Letter sent to ..." and "Paid copy sent to ..." with the client's address, and the history records it. Pressing Send on a real file this morning would read as if the real client had been mailed.
- **Evidence:** the walkthrough: 4 messages, 8 lines (client and office copy), none marked "trapped"; 4 messages in the log.
- **Fix idea:** set `HD_MAIL_TRAP` in the local `.env` to an address of Gordon's (every line then reads "trapped; meant for ..."). Gordon's choice; this check did not touch `.env`.

## What was checked, in numbers

**Requests:** about 11,190 through the app (about 11,070 through its HTTP kernel, about 120 through Herd's web server). Every one answered 200, except as designed: 62 answers of 404 (the old invoices' PDF address, below) and the 302 redirects after each form, login and log-out. **No 500 anywhere.**

**Exceptions:** none from app code in any answer. In `storage/logs/laravel.log`, nothing from use of the site on the real data. Written during this check: 1 WARNING (finding 1, by design), 4 DEBUG (the invented file's 4 messages on the log mailer), and 3 ERROR lines thrown by the checker's own throwaway scripts (1 `TypeError`, 2 `DOMException`), not app code. Older lines in the same file: 1 ERROR from W1's own check script (a `TypeError` in its use of `SessionGuard`), and 122 EMERGENCY plus many WARNING lines from test runs on 2026-10-02 between 01:00 and 07:00 UTC (environments "laravel" and "testing"); none came from the site.

**The File screen, all 10,206 imported files** (so every decade and every kind): 1980s 91, 1990s 2,167, 2000s 4,541, 2010s 2,415, 2020s 992; inspections 7,244, consultations 2,839, no kind recorded 123; 86 at a property with no street (84 with no address at all); 12 whose job named no client record (the import's stand-in client); 7,135 with a second person; 9,559 with a paid invoice and 647 unpaid; 1,885 with other people on the job.
- Status: 200 on 10,206. Exceptions: 0. Sections missing (client, property, people on the job, job, invoice description, invoice, letter, messages, change history, delete link): 0. Checked against the database: the second person shown where there is one, "Been here before" shown where there are other files (3,605), every person on the job listed, the job's date and time, kind and status as stored: 0 mismatches.
- Fallbacks shown, not blanks: client email "None on file" 5,555 files, phone 3,816, mailing address 932; property "Address not recorded" 84; invoice total "Not recorded" 48.
- Prompts: "This client may already be on file" on 905 files, "This property may already be on file" on 237: by design. Over the whole import the matcher suggests a twin for 697 clients (438 by the same email, 322 by name and phone, 188 by name and mailing address; at most 7 on one record) and 181 properties (all by the same address; at most 2).
- **The change history panel:** on all 10,206, folded, 1 to 3 entries (8,066 / 1,970 / 170), each made by "The import"; the count in its heading matches the list on every file.
- The forms, "Save" pressed with nothing changed, in memory (finding 2): the job form (10,206) and the invoice-description form (647) pass and change nothing; the client form: 41 would empty the state, 137 blocked by the browser; the property form: 13 refused (state); contacts: 18 blocked by the browser.
- Size: median 39 KB a page, largest 64 KB.

**The Dashboard:** 200, 25 files, New File and the search box present. Its scroll: 409 pages, 10,206 files, none twice, in exactly the database's order (newest first).

**Searches** (search words were taken from the data and are not written here; checked against the database):

| Search | How many | Right |
|---|---|---|
| A month, one per year from 1983 to 2026 ("May 2024" form) | 44 | 44: the count shown and every file listed (0 to 64 files a month) |
| The same months typed other ways ("5/2024", "2024-05", "05-2024", "may of 24", "Sept. 2019", "Sept '19", "oct 2010", "in March of 1998", a whole sentence) | 10 | 10 |
| A year by itself (1985, 1995, 2007, 2015, 2024) | 5 | 5 |
| A client's surname | 40 | 40: every file of a client with that surname listed (1 to 92 found) |
| A client's first and last name | 20 | 20: all that client's files listed |
| A street without its number | 40 | 40: every file on that street listed (1 to 88 found) |
| A whole address line, number and all | 40 | 40: that property's files listed |

**Other screens:** deleted files 200; New File 200; Settings 200 with all eight sections (3 invoice texts, 3 letter-template fields, 2 stamp uploads, 3 logins listed, 5 connections); stand-in Calendly 200; the "Delete this file?" question for 51 files spread through the history, 200 with its form (nothing deleted).

**The invoice PDF on old files:**
- The address "Look at the PDF" uses answers 404 on all 61 old files tried (spread through the history). That is the app's own rule: an old invoice has no number, so nothing would "go out". No old File screen offers the link (0 of 10,206).
- The path Peter can take is "Give this invoice a number", then the PDF. Done in memory for **all 647** unpaid old invoices, nothing saved, by the action's own rule: 584 PDFs made, 63 nothing to bill (finding 8), 0 errors; about 44 ms each. On the 584: the client's name with no address under it on 448 (no street on file; by design the block collapses to the name), no property address on 2.
- 107 paid old invoices, the same way: 107 PDFs, 0 errors (not a path Peter has today; a check of the template on old data).
- The invented file's invoice PDF through the web server: 200; its 8 stored PDFs (letter, invoice, paid copies) all present and valid.

## Timings (anything over two seconds would be a finding; nothing came near)

| Screen | Inside the app (median / slowest) | Through Herd's web server, logged in (median / slowest) |
|---|---|---|
| Dashboard | 3.5 ms / 13.5 ms (n 11) | 10 ms / 12 ms (n 10) |
| Month search | 2.5 ms / 3.7 ms (n 44) | 9 ms / 9 ms (n 10) |
| Surname search | 9 ms / 13 ms (n 40) | 16 ms / 17 ms (n 10); the commonest surname 17 ms |
| Full-name search | 18 ms / 31 ms (n 20) | |
| Street search | 25 ms / 34 ms (n 40) | 24 ms / 33 ms (n 5) |
| Whole address line | 31 ms / 40 ms (n 40) | |
| File screen | 18 ms / 38 ms (n 10,206) | 17 ms / 23 ms (n 16, including the largest pages and the busiest client and property) |
| Settings | 6 ms (n 1) | 9 ms / 10 ms (n 3) |
| New File form | 3 ms (n 1) | 7 ms / 7 ms (n 3) |
| A scroll page of the Dashboard | 6 ms at most (n 408) | |
| Form posts in the walkthrough | | 75 ms at most (mark paid, which makes and keeps a PDF) |

## The everyday actions, on one invented file

Through Herd's web server like a browser, logged in as local login #1 (the owner), every form sent with its own token: **20 steps, all ended in 200.**

1. New File by hand: client "Test Walkthrough", property "1 Example Street, Testville, CT", opinion, a visit tomorrow. Opened as **file #10207** (client #8694, property #9113); no "may already be on file" prompt; the letter made at once (stand-in Doc); invoice **HD-2610-096**.
2. Corrections: the client's mobile phone, the property's year built, the job's time: each "Saved", each in the history.
3. Invoice description and price ($375.00): saved, shown on the invoice.
4. The letter: brought up to date after the corrections; "Open the Doc" (stand-in page) 200; "Send the letter" with the CT stamp refused (finding 1); the file's stamp set to "No stamp"; letter sent; status Booked to Sent.
5. The invoice: "Look at the PDF" 200; sent; "The PDF as sent" 200; marked paid (the paid copy went with it; status Sent to Paid); paid copy sent again.
6. Delete (two steps): gone from the Dashboard, found under "Deleted files", opened read-only with the red banner and no forms but Restore. Restore: back on the Dashboard.
7. Change history before the final delete: 13 entries, 26 lines, from "Client entered ... File opened ... Invoice made ... Letter created" to "File restored".
8. **Then marked deleted again, as the app does (a mark), so it is not on Peter's Dashboard.** It stays under "Deleted files".

Mail: 4 messages (letter, invoice, paid copy, paid copy again), each to the invented address and the office copy, all written to `storage/logs/laravel.log` by the log mailer. Nothing left this Mac (see finding 9).

## What this check left behind, and what it did not do

- **In the rehearsal database, all invented:** file #10207 (deleted), client #8694 and property #9113 (reachable only through that deleted file), its invoice HD-2610-096 (one of October 2026's 1,000 numbers), 8 message lines, 32 history lines, and 2 session rows for logins that were logged out (no session of this check is still logged in). Its 8 PDFs are on the records disk and its stand-in Doc in the stand-in store, both in git-ignored folders.
- **No real record was written:** every read-only run had SQLite's query-only mode on its connection and ended with 0 changes; sessions were kept in memory. `.env` and `legacy.sqlite` untouched; the importer not run; no file in the app repository changed (git status clean at 1063e6c); nothing committed.
- **Not done, by the brief's rules:** no form was sent for a real record (the forms were replayed in memory only); the "may already be on file" prompt for a returning real client on New File (it would mean making a record with a real person's details); Calendly's stand-in booking; the login form with a password (a session was made through the app's own session store instead, and logged out afterwards).
