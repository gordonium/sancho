---
name: Home Directions v4 review, app stages W10 and W11 (the serious P3 findings; letter revisions)
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of W10 (a booking moved twice, a written-in Doc never trashed, the cutover one-click tie, login notices, the bookings-off notice) and W11 (letter revisions, sending the latest published revision, Revision 1 for converted letters, the payment date, "Receipt", "Before v4", the mail-log wording, the template-line refusal), weighted toward what a client can read by link and what Send sends; 10 numbered findings, each with file and line, evidence, fix and weight; then what holds and the three checks' numbers
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, 8e278ec..738bbd8, 8 commits, 86 files]", "[doc:build-handoff.md sections 3 and 4]", "[doc:build-state.md, 12:35 Oct 3]", "[doc:phase0-brief.md, letter revisions, Gordon 2026-10-03]", "[doc:build-log-app.md, W10 and W11]", "[doc:reviews/app-P3-plan-fit.md findings 1 to 3, app-P3-safety.md findings 1 to 3]", "[doc:runbook-cutover.md lines 89 and 185]", "[doc:current-system.md, How a job flows]", "[run: herd composer test, lint, analyse in a scratch copy at 738bbd8, 2026-10-03 13:25 to 13:45 CEST]", "[run: 11 probe tests in 1 file on invented data with the stand-ins, scratch copy only]"]
status: written 2026-10-03 about 13:55 CEST by a reviewer on Opus 5.5 (effort level not visible to it) that did not write the code, changed nothing in either repository (app tree clean at 738bbd8), committed nothing, called no Google service, sent no mail, and did not open the real .env, legacy.sqlite or the rehearsal database. 0 blockers, 2 should-fix, 8 minor. Counts, file numbers and record IDs only; no name, address, secret or letter text. The scratch copy and its probes were deleted afterwards.
---
# Review: app stages W10 and W11

Reviewer: Claude, model `claude-opus-5-5` (Opus 5.5). I cannot see my effort level. I did not write this code and changed none of it.

**Range.** 8e278ec..738bbd8: W10's six commits (d8cea98, 1001a1d, 5da9f59, 18ce102, 5724934, 38ac306) and W11's two (4c7eaf4, 738bbd8). 86 files, 2,796 lines added.

## In a minute

- **No blocker.** No path makes a working Doc readable by link: the one Doc-sharing call in the app is `SendLetter.php:67`, on the revision's frozen copy, and publishing takes the link off a working Doc an earlier send had shared. Numbering is safe (one number per file, worked out inside the file's lock, unique in the database). Send always takes the highest-numbered revision.
- **Should-fix 1:** the send of a Revision 1 that came "from the old system" skips every check that publishing makes, and `hd:start-revisions` gives such a Revision 1 to any imported file that holds a Doc, a letter made in v4 included. A probe mailed the unwritten template, "[Write the letter here.]" and all, and made it readable by link.
- **Should-fix 2:** W10's cutover tie assumes the jobs still to come were imported from v3. The import leaves out every job dated after the day it runs, as "dated in the future", the same words as the test records. On cutover day the tie step finds no file for those bookings; what v3 held for them stays behind.
- **Minor, 8:** the frozen copy's lock can be lifted by any editor of the letters folder; a failed send can leave a copy shared while the screen says nobody can read it; an edit typed during a send can go out; the payment date has no floor and its refusal is hidden; "Before v4" is shown for steps that never happened; and three smaller ones.
- **Checks:** 1,510 tests passed (6,763 assertions), 0 failed; lint passed; analysis 0 errors.

## How the evidence was made

- **Scratch copy.** `git archive 738bbd8` into the session's temp folder, plus `vendor`, `node_modules` and `public/build`. A fresh `.env` from `.env.example` with a new key, the stand-in letters and Calendly, and an empty scratch SQLite file. Nothing was read from the real `.env`.
- **PHP.** The scratch folder is not a Herd site, so plain `herd composer` there picks PHP 8.4 and Composer's platform check refuses. `herd composer --site=hdonline-v4 <script>` runs the same scripts with that site's PHP 8.5.10 in the scratch folder.
- **Probes.** 11 Pest tests in one file, on invented people and the stand-ins, `Http` faked where Brevo was needed. Each records what the code does today; all 11 passed (74 assertions). They are named A to J below, D in two parts.

---

## Should-fix

### 1. Sending an old-system Revision 1 skips the publish checks, and `hd:start-revisions` gives one to letters made in v4

**Where.**
- `app/Actions/SendLetter.php` 57 to 61: when the latest revision exists and is not frozen, `freezeTheOldOne()` is called directly.
- `app/Actions/PublishRevision.php` 77 to 98, `freezeTheOldOne()`: its only check is that the Doc's revision still equals the one noted (line 87). It does not bring the Doc into step (`PrepareLetter`), and does not make the checks `publish()` makes at 106 to 117: the stamp in the letter, a `{{tag}}` still showing, the template's "[Write the letter here.]". The stamp-image check at 57 to 59 is skipped too.
- `app/Console/Commands/StartRevisionsCommand.php` 38 to 43 selects files with a Doc and any `sources` row. Its own docblock (16 to 20) says "hold a converted Doc"; nothing checks that. Every imported job has a `sources` row, and an imported job with no old letter offers "Create the letter" (`files/show.blade.php` 354 to 361).

**What is wrong.**
- **(a)** Run again after a letter has been made in v4 on an imported job, the command labels that letter "from the old system: the version the client already has". The first "Send Revision 1" then freezes and mails whatever the Doc holds. The template line, a missing stamp and unfilled tags all go through. The command calls itself safe to run any number of times, and the W11 log says so.
- **(b)** A converted letter whose stamp could not be placed: the conversion keeps such a letter on purpose (`ConvertedDoc.php` 65 to 76), with `letter_stamp_problem` noted. The Letter box says "The stamp could not be placed in the Doc, so the letter has none and cannot be sent yet." "Send Revision 1" sends it anyway, stampless. Publishing the same letter would first place the stamp, then check.

**Evidence.**
- Probe A, an imported file with a v4-made, unwritten letter:
  - control: Send refused, 0 mails;
  - `hd:start-revisions`: Revision 1 "from the old system";
  - Send: accepted, 1 mail, and the frozen copy holds "[Write the letter here.]" and is readable by link.
- Probe B, a converted-style file whose fields say the stamp is not in the letter (`letterCarriesItsStamp()` false): "cannot be sent yet" on the screen, Send accepted, 1 mail. The control file, published instead, had its stamp placed again before the check.
- Probe I: with the stamp image taken out of Settings, the old-revision send still goes. That is harmless there, because the Doc already holds the stamp picture, but it shows the check is not made.
- On the rehearsal data the command picked exactly the 30 converted files (W11 log). So nothing wrong exists today; the risk is the next run, and every converted letter with a stamp problem.

**The fix.**
1. One method, used by `publish()` and `freezeTheOldOne()` alike, for the stamp image, the stamp in the letter, the tags and the template line. Run `PrepareLetter` first in both. If that write moves the Doc on, the old revision is "edited since", and the person publishes a new one, which is the right outcome.
2. Have the command select only converted files: a source with collection `hdo_reports`, or the v2 report collection, or an "Imported letter" history line.
3. A test for each: the template line, a stamp problem, a v4-made letter on an imported job.

### 2. The cutover import leaves out the jobs still to come, which W10's one-click tie assumes are on file

**Where.**
- `app/Import/Skip.php` 34 to 38: any job whose day is after today is skipped, "dated in the future". `ImportHistory.php:70` takes today as `now()`. `hd:import` has no option for a cut date (`ImportCommand.php` 26 to 29).
- `tests/Feature/Import/ImportTest.php` 92 and 151: a job titled "A booking", dated 2027-01-01, is skipped by design.
- `app/Http/Controllers/SettingsEarlierBookingController.php` 16 to 23: "at the cutover every job still to come is on file from the old system's history and in Calendly as well". W10's tests (`tests/Feature/Calendly/EarlierBookingsTest.php` 14 to 27) put that job on file with `openFile()`, not through the importer, so the two were never run together.
- `docs/runbook-cutover.md` contradicts itself:
  - line 89 tells the person to accept "every record dated in the future" as a test record;
  - line 185 expects the bookings after the cut to have "come in with the import".

**What is wrong.** Gordon's word was about the oddities in the staged clone: "the future oddity are just test records ... You can skip 'em" [gordon 2026-10-02]. The rule as built is broader. On cutover day, a real job typed into v3 for next week has a future date, so the import leaves it out. It is listed by WordPress ID under the same reason as the test records, and the runbook says that is expected.

Then, under Connections, its Calendly booking says "No file here without a booking has this time or this email address." "Open a file for it" makes a new file from Calendly's details. Whatever v3 held for that job stays behind: a changed price or wording, the people copied, a letter begun early. A job typed into v3 and not booked through Calendly does not reach v4 at all.

How many real jobs v3 will hold for dates after the cut is not known. Peter enters each job by hand in v3 [doc:current-system.md, How a job flows, 1]. The staged clone held 9 future-dated records, which Gordon called test records.

**Evidence.** The code and the test above. No probe was needed: the importer's own test asserts the skip.

**The fix** (a decision for Gordon, then a small change):
- Skip a future date only when it is implausible, for example more than 18 months ahead (this still skips the year-8888 record), or add an `--as-of`/`--keep-upcoming` option for the cutover run. The whole-word "test" rule stays.
- List the upcoming jobs that were kept, so the tie step can be checked against them.
- A test with a job dated next week.
- Correct runbook lines 89 and 185.

---

## Minor

### 3. The frozen copy's lock can be lifted by any editor of the letters folder
- **Where:** `app/Letters/GoogleLetterDocs.php` 706 to 709 sets `contentRestrictions: [{readOnly: true, reason}]` without `ownerRestricted`. The copies live in "Published revisions (frozen copies)", inside the letters folder, which is shared with the office Gmail account as Editor (build-state 10:00 Oct 3).
- **What is wrong:** by Drive's documented rules, an editor can unlock a restricted file unless `ownerRestricted` is true (not verified against Google here). Peter or Maria Pia, opening a frozen copy from Drive, can press Unlock and edit it. The client's link then shows words that were never published, while the PDF and the screen say otherwise. W11 recorded this as its decision 3.
- **Fix:** add `'ownerRestricted' => true` to the restriction, so only the owning account (office@) can lift it. Assert it in the freeze test. The how-tos now say to edit only the working letter.

### 4. A send that fails, followed by a failed unsharing, leaves the copy readable by link, unrecorded, and the screen says nobody can read it
- **Where:** `app/Actions/SendLetter.php` 95 to 100: `closeIfItNeverLeft()` wraps the unsharing in `rescue()`. Nothing is written down when it fails. `files/show.blade.php:280` then shows "Not sent from here. Nobody outside the firm can read it."
- **Evidence:** probe C. Brevo refused the letter (400) and the unsharing failed (`FlakyLetterDocs`). The copy was still shared, 0 message lines stood (all failed), and the File screen showed that sentence.
- **Weight:** minor. Nobody was given the link, and it takes two failures at once. The same happens when the sharing's answer is lost and the unsharing fails.
- **Fix:** note on the revision that its copy may be shared (`shared_at`). Show "shared by link, not sent" instead of the sentence. Try the unsharing again on the next File screen view or send, or in `hd:unshare-pictures`. A test.

### 5. An edit typed during the copy goes out; Send does not wait for a publish in progress
- **Where:** `PublishRevision.php:87` reads the Doc's revision and line 91 copies the Doc as it is then. The same holds in `publish()` (lines 120 and 131). `SendLetter::handle` (51 to 61) reads the latest revision outside the file's lock.
- **What is wrong:**
  - Something typed between the look and the copy is frozen under the earlier state. On the old-system path it goes straight to the client, labelled the version the client already has. On the publish path, the screen then says "Edited since".
  - A Send pressed while a Publish is still running sends the revision before it.
  - Two Sends on a never-published letter: the second is refused with "nothing new to publish", a confusing answer to a Send.
- **Evidence:** probe J. A Doc store that types half a sentence just before the copy is made: Send accepted, the frozen "Revision 1 (from the old system)" holds the half sentence, 1 mail.
- **Fix:** after the copy, read the working Doc's revision again. If it moved, trash the copy and refuse with "The Doc changed while it was being published; try again". Run `SendLetter` inside `OneAtATime`.

### 6. The payment date has no floor; the button does not name it; a refusal is hidden
- **Where:** `app/Http/Requests/MarkPaidRequest.php:23` (`before_or_equal` today, no lower bound). `files/show.blade.php` 500 to 515: the `<details>` has no `open` when `paid_on` has an error, and the button reads "Yes, <client> has paid <amount>". `resources/views/pdf/invoice.blade.php:79` prints "Paid <date>" on the receipt.
- **Evidence:**
  - Probe D1: 1990-01-01 is accepted, recorded, and the receipt mailed at once.
  - Probe D2: a refused day comes back inside the folded box, with no notice where the page opens; nothing recorded.
  - Probe H: the button does not repeat the day.
- **What is wrong:** a slipped year goes on the client's receipt, which leaves at once. Putting it right means "Take the payment back" and a second receipt.
- **Fix:**
  - refuse a day before the job's own date (or more than a year back) with a plain message;
  - name the day on the button ("... has paid $875 on Oct 9");
  - open the box when `paid_on` has an error.

### 7. "Before v4" is shown for steps that may never have happened
- **Where:** `app/Models/File.php` 211 to 217: every file with a `sources` row gets "Before v4" for "Letter sent", and for "Invoice sent" when it has an invoice, wherever v4 has no date.
- **Evidence:** probe E. An imported job dated next week, with no letter and an invoice never sent: the board shows "Before v4" twice, beside "This file has no letter yet." and "Create the letter".
- **Which files:**
  - the 21 imported jobs whose old letter is empty (W5);
  - any job still to come at the cut (finding 2);
  - every unpaid old invoice (647 of 10,206 imported invoices are unpaid; nothing says they were sent).
- **Fix** (Gordon's choice; Peter's walkthrough item 7 in `tweaks-2026-10-03-peter.md` leans to showing nothing):
  - "Before v4" for the letter only where the old system holds one (`hasALetterNotImportedYet()` or a converted Doc) and the job is past;
  - for the invoice, only where the job is past;
  - otherwise "Not yet".

### 8. On a deleted file, "PDF of Revision N" and "The PDF as sent" lead to a 404
- **Where:** `routes/web.php` 110 and 113: neither route takes `withTrashed()`. The File screen of a deleted file is shown (line 74) and lists both links.
- **Evidence:** probe F. A deleted file shows "PDF of Revision 1"; its link answers 404.
- **Fix:** `->withTrashed()` on those two GET routes (they only read), or hide the links on a deleted file.

### 9. `--again --discard-edits` keeps a revision published here as the latest
- **Where:** `app/Import/ConvertOldLetter.php` 93 to 106 refuses `--again` only for a file sent from v4, or one written in without `--discard-edits`. `LetterRevision::startFromTheOldSystem` (69 to 79) leaves a file with two revisions alone.
- **What is wrong:** a converted letter on which Peter published Revision 2, re-converted with `--discard-edits`, keeps Revision 2 as the latest. Send then sends the edits that were meant to be thrown away, and the fresh Doc reads "Edited since Revision 2". Read in the code, not probed.
- **Fix:** refuse `--again` for a file with a revision published here, unless a flag of its own is given; say what becomes of the revisions.

### 10. A login change whose notices fail says nothing on the screen
- **Where:** `app/Actions/TellTheLogins.php:34` rescues each notice. The controllers' statuses ("Saved ...'s login.", "Login made for ...") do not change.
- **What is wrong:** where mail is not live and no trap address is set (a staging server), or Brevo is down, nobody is told. The person who made the change is not told that the others were not. The Settings history still has the line.
- **Fix:** return the failures from `TellTheLogins` and add "The others could not be told: <reason>" to the status. A test.

---

## What holds

### What a client can read by link
- **One Doc-sharing call.** The only Doc-sharing call is `SendLetter.php:67` on `$revision->doc_id`, the frozen copy; the only other "anyone" permission is the image lending (`GoogleLetterDocs.php:321`), unchanged since W9 (searched in `app/`). `allowFileDiscovery` is never set.
- **The working Doc stays private.** Publishing does not write in it. `PublishRevision.php` 138 to 141 takes the link off a working Doc shared by a send from before revisions. The W11 tests assert the working Doc is unshared after publishing and after sending; W11 showed on real Google that a copy does not inherit link sharing.
- **Only what was sent is shared.** Probe G: two revisions published and sent leave both copies readable by their links (by design: each client email links its own revision). A revision never sent, and the working Doc, are not readable by link.
- **The copy's mark** (`revision-` and a hash of file, Doc, number and Doc revision) cannot be confused with a working Doc's mark (a UUID).

### Revisions: numbers, loss, sending
- **Numbers.**
  - The next number is worked out inside the file's lock, on a fresh read (`OneAtATime.php:42` refreshes the file and its loaded relations).
  - `letter_revisions` is unique on (file_id, number).
  - "Nothing new to publish" is refused.
  - A lost answer finishes the same copy through its mark.
  - No code changes a number or deletes a revision (`IsNeverDestroyed`).
- **Send takes the latest.**
  - `latestRevision` is `ofMany('number', 'max')`.
  - The mail carries that revision's own PDF (`LetterMail::pdfPath`) and its copy's `/preview` link.
  - The message log line records `letter_revision_id`.
  - From Revision 2 the subject says "(Revision N)".
  - Edits not published do not go (`tests/Feature/Letters/LetterRevisionsTest.php:94`).
- **A refused send closes the copy again** unless the revision has left before (`tests/Feature/Letters/SendLetterTest.php:233`), except as in finding 4.
- **The template line** is refused at publishing and at a first send (`LetterRevisionsTest.php:124`), except as in finding 1.

### W10
- **The cutover tie.**
  - Only a person ties.
  - A file that already has a booking, or is deleted, is refused (`DecideEarlierBookingRequest.php:25`), and so is a second file for one appointment (controller line 42).
  - A cancelled booking is noted on the tied file, unless its letter has gone.
  - "Bring them in" skips any booking that has a likely file.
  - The Dashboard counts them.
  - 11 tests.
- **Logins.**
  - Every login that is on, and the old address on a change of address, is mailed when a login is added, switched off or on, given another address or role, or has its password set.
  - Nobody changes their own role (`SaveUserRequest.php:33`) or switches off their own login.
  - A password set is a Settings-history line without a value.
  - The reset is throttled (6 a minute).
  - A switched-off login is signed out on its next request (`LoginIsOn`).
- **Bookings off.** From the press, the Dashboard tells everybody, with since when and by whom. After a day, the 15-minute check raises it once a day until bookings are on again. Switching on clears it. Before bookings were ever on, nothing is said (W10's decision 5).
- **A written-in Doc** is never trashed on a cancellation, and `--again` honours the mark. A booking moved twice keeps one file in all 24 orders of its notices. Read and spot-checked, not probed; their tests (29 moved-twice cases, the written-in cases) pass within the 1,510.

### W11's smaller items
- **The payment day** is never later than today, on the server and in the field's `max`. Today records now; an earlier day records noon on the firm's clock. The receipt prints that day.
- **"Receipt"** is used on every screen and in the message log and change history; "paid copy" remains only in code comments.
- **The mail-log wording** ("written to this machine's mail log only ... the client was sent nothing") shows for the letter, the invoice and the receipt wherever the mailer is the log mailer.

## Still open from earlier reviews (not re-weighted here)
- W10's own "Left" list: "Leave it" and "Leave them all" write no line anywhere (P3 plan-fit 13); a hand-cancelled file keeps its date on a later move (plan-fit 4); no rate limit on adding logins (P3 safety 9); W10's two questions (only Gordon manages logins? an "off on purpose" setting?).
- W5-W8 finding 6: this Mac and the rehearsal share the production Drive. The setting that names "Published revisions (frozen copies)" lives in the rehearsal database, so production will make a second folder of that name beside it.
- W11 put its plan in the log after the code, and migrated the rehearsal database itself (backup taken, said plainly). Both are process notes for the orchestrating thread.

## The checks

Run in the scratch copy at 738bbd8 with Herd's PHP 8.5.10 (`herd composer --site=hdonline-v4 ...`), 2026-10-03 13:25 to 13:45 CEST.

| Command | Result |
|---|---|
| `herd composer test` (with the browser suite) | **1,510 passed, 6,763 assertions, 0 failed**, 32 s. The agent-format summary says "warnings: 1" with no detail, as earlier stages noted. |
| `herd composer lint` (Pint) | **passed** |
| `herd composer analyse` (Larastan level 8) | **passed, 0 errors**. Run again cold with a fresh cache folder: 0 errors. |

The 11 probes (one file, 74 assertions) passed as written to record the behaviour above. They were never part of the app and are deleted with the scratch copy.

## Not done

No Google, Calendly or Brevo call was made. So `ownerRestricted` (finding 3) and Drive's handling of the lock are unverified, and the real Docs and the rehearsal database were not looked at. The app was not served.
