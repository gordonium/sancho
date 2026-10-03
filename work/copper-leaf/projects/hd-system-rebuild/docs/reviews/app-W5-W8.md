---
name: Home Directions v4 review, app stages W5 to W8 (Google, the conversions, the File screen)
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of W5 to W8 (the board and Gordon's other File-screen changes, hd:google-connect, the real Google letters class, hd:dress-template, hd:convert-letters, hd:convert-v2-reports), weighted toward Google safety, then the conversions, then the File screen; 16 numbered findings, each with file and line, what is wrong, the evidence actually run, the fix and a weight; then what was checked and holds, and the three checks' numbers
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, 4b4866f..0e89dc9, 16 commits, 124 files]", "[doc:build-handoff.md sections 3 and 4]", "[doc:build-state.md, 09:00 and 10:35 Oct 3]", "[doc:phase0-brief.md, Gordon 2026-10-03]", "[doc:plan-v2.md sections 5 and 6]", "[doc:laravel-kit-spec.md 8.2]", "[doc:build-log-app.md, W5 to W8]", "[run: herd composer test, lint, analyse in a scratch copy at 0e89dc9, 2026-10-03 11:13 to 11:33 CEST]", "[run: 6 probe tests in 4 files on invented data with made-up Google answers, scratch copy only]", "[run: a byte search for the client secret and refresh token, values held in memory only, counts printed]", "[run: read-only counts and IDs from legacy.sqlite and the rehearsal database (SQLite read-only and immutable modes)]"]
status: written 2026-10-03 about 11:45 CEST by a reviewer on Opus 5.5 (effort level not visible to it) that did not write the code, changed nothing in either repository (app tree clean at 0e89dc9), committed nothing, called no Google service and sent no mail. 1 blocker, 6 should-fix, 9 minor. Counts, file numbers and record IDs only; no secret, name, address or letter text appears here. The scratch copy and its probes were deleted afterwards.
---
# Review: app stages W5 to W8 (Google, the conversions, the File screen)

Reviewer: Claude, model `claude-opus-5-5` (Opus 5.5). I cannot see my effort level. I did not write this code and changed none of it.

**Range.** The brief named "fb6190d's parent..0e89dc9", but fb6190d is W5's last commit; W5 started at 4b4866f. I reviewed **4b4866f..0e89dc9** so that all of W5 (the board, `hd:google-connect`) is in: 16 commits, 124 files, 6,629 lines added.

## In a minute

- **Google, mostly sound.** The client secret and the refresh token live in `.env` and nowhere else: a byte search of the app folder and its git history, the kit repository, the data folder, the temp folders, the Sancho tree and its git history and the two agent-transcript folders found **no copy**. Nothing prints, logs, stores, shows or sends them to a browser. The scope is `drive.file` alone. Nothing shares a Doc or folder with a person. "Send the letter" makes only that letter readable by link, last.
- **One blocker.** The picture "shared by link for a moment" is **not always unshared**: one failed unsharing stops the rest, a sharing whose answer is lost is never taken back, and Ctrl-C or a killed job skips the clean-up. Nothing records which pictures were lent, so nothing ever finds a stranded one. Shown with made-up Google answers (finding 1).
- **The conversions** read their sources read-only and refuse a wrong source. `legacy.sqlite` and the backups are untouched, and anything already converted is skipped. Nothing real is in a tracked path. But: `--again` puts a Doc that Peter has written in into the trash (2); photos inside tables, and letters made only of photos, are left out without a count (3); a photo not loaded yet gives a false line in the Doc (4); a picture batch whose answer is lost can put every picture in twice (5).
- **The File screen** is as Gordon asked: board, Letter above Job, the large description box, the date in the header, "Not imported yet", old invoices sent without a number, other people as text. One dead end (1 invoice) and small marks (13 to 15).
- **Checks:** 1,426 tests passed (5,853 assertions), 0 failed; lint passed; analysis 0 errors.

## How the evidence was made

- **Scratch copy.** The app at 0e89dc9 was copied with `git archive`, plus `vendor`, `node_modules` and the built assets, into the session's temp folder. It got a fresh `.env` made from `.env.example` with a new app key: no Google line and nothing copied from the real `.env`. The probes are Pest tests there, using invented images and made-up Google answers in the shapes the app's own tests use. `Http::preventStrayRequests()` was on, so nothing could reach Google.
- **The secret search.** A small script read the two values from the real `.env` into memory. It counted their bytes (plain, URL-encoded and JSON-escaped) in the folders named above and printed paths and counts only.
- **Real data.** Read-only counts and IDs from `legacy.sqlite` (opened `mode=ro`) and the rehearsal database (opened `immutable`), and the conversion outputs in `storage/app/private/conversion/`, which hold counts and file numbers.

---

## Blocker

### 1. A picture lent to Google can stay readable by anyone with its link

**Where.**
- `app/Letters/GoogleLetterDocs.php` 220 to 252, `lend()`: the "anyone, reader" permission is made at 246 to 249. It reaches the caller's list only if Google's answer arrives.
- 261 to 268, `takeBack()`: one `DELETE` after another. The first failure throws and the rest are never asked.
- 150 to 174, `writeBody()`: every picture of a body is lent before the batch. All stay shared through the batch and through the one-by-one retries, each up to 120 s.
- The same pattern at 185 to 206 (`write`) and 361 to 383 (`dress`).
- `app/Letters/GoogleSession.php` 168 to 193: every failure is thrown, a 404 included.
- No lent picture is written down anywhere. No command traps Ctrl-C (no `trap()` in `app/Console/Commands/`). `app/Jobs/KeepLetterCurrent.php:32` gives a queued letter 120 s before the worker kills it.

**What is wrong.** The class's own promise (lines 48 to 52: shared "for the moment of insertion … and the sharing removed again") holds only when every call succeeds and the process lives to the end. A picture stays public in four ways:
- **(a)** One unsharing fails (a dropped line, a 5xx). The pictures after it in the list are never unshared. The error from the `finally` also replaces the real result, so a body that went in well is reported as a failed conversion.
- **(b)** Google makes the permission and its answer is lost. The app never learns the permission exists.
- **(c)** The process dies between lending and unsharing. Ctrl-C during `hd:convert-letters`, which runs for hours at cutover, does this. So does a queue worker killing a job at its timeout.
- **(d)** Two runs lend the same image at once, for example a conversion and a new file both using the Connecticut stamp. Drive keeps one "anyone" permission per file (the app's tests model its ID as `anyoneWithLink`). The first run removes it from under the second, whose own removal then gets 404 and stops its list as in (a).

The stamps, logo and signature are the same Drive file each time, so the next successful use removes a stranded permission on them. **A client's photo is lent once per conversion and never again, so nothing ever removes its sharing.** The cutover will lend about 1,100 photos over several hours, on a line that dropped twice today. "Test Google" does not look at sharing.

**Evidence** (scratch copy, made-up answers, three pictures a, b, c, lent last first):
- Probe 1, the first unsharing fails with "Could not resolve host": shared c, b, a; unsharing tried for c only; thrown "Google could not be reached to stop sharing the image". **b and a stay shared**, and the good body counts as failed.
- Probe 2, the third sharing's answer times out: unsharing sent for c and b only. **a stays shared**, and nothing knows it.
- Probe 3, the first unsharing answers 404: one unsharing tried, thrown "(404)". **The other two stay shared.**
- Ctrl-C: an artisan command in the scratch copy, `try { sleep } finally { write a file }`, stopped with SIGINT, exited 130 **without running its `finally`**. Laravel's command class subscribes to no signals.
- Now: today's conversion outputs and `laravel.log` show no failure at a sharing or unsharing call. The failures were at "copy the template" (3) and "make the Doc" (3), before any picture was lent. W7 asked Drive at about 10:40 that none of 54 pictures was shared. **So nothing points to a picture shared now, but that cannot be checked from here without calling Google.**

**The fix.**
1. `takeBack()` tries every permission, treats 404 as already removed, collects failures, and never throws over the original result.
2. Before asking Google to share an image, write its Drive ID down (a small table or a Setting list). Strike it off only once the sharing is gone. A sweep removes the "anyone" permission of every image still on the list: at the start of every `lend()`, at the start of each `hd:convert-*` and `hd:dress-template` run, and from the scheduler. This covers (b) and (c).
3. `trap()` SIGINT and SIGTERM in the three commands so the letter in hand is cleaned up before they exit.
4. A cache lock per image around lend, insert and unshare, so two runs never share one permission (d).
5. A check, in "Test Google" or a command, that lists every file in the pictures folder shared with anyone and offers to unshare it.
6. A test for each of (a) to (d).

---

## Should-fix

### 2. `--again` puts a Doc that a person has written in into the trash

**Where.**
- `app/Import/ConvertOldLetter.php` 82 to 88 and 104 to 110.
- `app/Import/ConvertV2Report.php` 69 to 75 and 92 to 97.
- `app/Import/ConvertedDoc.php` 86 to 106.

The only refusal is a letter that has been sent from v4.

**What is wrong.** The converted Docs are meant for Peter to "continue to revisit and edit" [gordon 2026-10-01]. `--again`, on one file or on a whole `--since`, trashes whatever Doc a file has and makes a fresh one from the old record. It does not ask whether anybody has written in that Doc since. It says nothing about it, and Drive empties its trash after 30 days. The old Doc's ID survives in the change history (23 such lines on the rehearsal database), so it can be fished out by hand within that time.

**Evidence.** Probe 5, stand-in store, invented letter:
1. Converted.
2. A paragraph typed into the Doc as Peter would; the revision moved.
3. `--again`: the command succeeded, the edited Doc is in the trash, and the new Doc lacks the paragraph.

Today 20 Docs were re-made with `--again` (15 at W7, 5 after batch 2), each before anybody had written in it.

**The fix.** Refuse `--again` for a file whose Doc's latest revision differs from `letter_revision` (somebody wrote in it), unless an explicit `--discard-edits` is given. Print the file numbers whose Docs went to the trash. Same in both commands. A test.

### 3. The conversion leaves photos out without counting them

**Where, and what.**
- **(a) Photos inside a table.** `app/Letters/Body/OldLetterMarkup.php` 284 to 314: each cell's pictures are collected (292 to 293) and dropped. A table of photos only is counted as an "empty table dropped", and its photos are not even on the dry run's list of photos wanted.
  - The same silent drop happens for a picture in a heading (180 to 194) or a caption (215 to 223), and for words inside a figure outside its caption (199 to 213, text nodes skipped at 202). Those have 0 cases in the real letters.
- **(b) Letters made only of photos.** The import's note `report_has_text` (`app/Import/ImportHistory.php` 162 to 165) strips every tag, pictures included. A letter with photos and no words is therefore marked as having nothing:
  - its File screen offers "Create the letter";
  - `--latest` and `--since` never select it (`app/Console/Commands/ConvertLettersCommand.php` 111 to 115);
  - yet the converter itself would take it (`ConvertOldLetter.php:71` keeps `<img>`).

**Evidence.**
- Probe 4, invented letters:
  - a table of two photos gave 0 pictures placed, 0 photos needed, 0 missing, and 1 "empty table dropped";
  - a table of words with a photo gave 0 pictures and 1 "table kept".
- On the real letters since 2022-06-21: **5 letters hold 12 photos inside tables**, files 9773 (4), 9808 (1), 9824 (3), 9825 (3) and 9933 (1). Three of those tables have no words at all. None is converted yet.
- **2 letters are photos with no words**, files 9873 and 10032, both noted `report_has_text: false`.

**The fix.**
- Place a cell's pictures after the table's lines and count them; do the same for headings and captions; keep a figure's loose words.
- Make `hasText()` keep `<img>` as the converter does, then run the import's note again so the two files say "Not imported yet" and are converted.
- A test for each.

### 4. A photo not yet in the app's store: the letter is converted anyway, with a line saying the old system does not hold it

**Where.** `app/Letters/Body/OldLetterMarkup.php:35` and 239 to 243, and `app/Console/Commands/ConvertLettersCommand.php:162`, which labels the count "photos the old files do not hold". The test is only "is it in `storage/app/records/old-photos/`", not "is it in the old files".

**What is wrong.** A run before the photos are loaded makes complete-looking Docs with "[A photo was here. The old system's files do not hold it.]" in italics. That is false: the backup holds them. A later run without `--again` skips those files as "already converted".

**Evidence.** Today's batch 2 (`20261003-084243-run.json`): 13 letters converted, "photos the old files do not hold: 11". All 11 were in the backup. The five letters were re-made with `--again` once the photos had been copied in (build-state 10:47).

**The fix.**
- By default, skip (counted, listed by file) a letter whose wanted photo is not in the store; `--without-missing-photos` lets it go on.
- When it does go on, the line in the Doc says only "A photo was here; it was not brought over", and the count is "photos not in the app's photo store".
- The dry run's list stays the to-do.

### 5. After a picture batch whose answer is lost, every picture is put in again with no revision check, so pictures can come out twice

**Where.** `app/Letters/GoogleLetterDocs.php` 144 to 171. The picture batch (145 to 148) carries no `writeControl`. On any failure, "unreachable" included, each picture is sent again by itself (163 to 170). The words batch (135 to 138) and the fill (199 to 202) do use `requiredRevisionId`.

**What is wrong.** A timeout does not mean Google did nothing. If the batch went in and its answer was lost (it has 120 s, and the line dropped twice today), each picture goes in a second time. Because the indexes were worked out before the first batch, each second copy lands one place off for every picture before it. The conversion then reports no problem.

**Evidence.** Probe 6: the words went in, the picture batch timed out, and the singles were accepted. Result: 3 picture batches sent, **4 insertions for 2 pictures, 0 with a revision check**, nothing reported refused.

**The fix.** Read the revision after the words batch and send it as `requiredRevisionId` with the picture batch and with each single. After "unreachable", read the Doc again and count its inline pictures before retrying, or fail the letter so the Doc goes to the trash and the next run makes it cleanly.

### 6. This Mac holds the production Google credential, and the rehearsal's Docs are in the production folder (a decision for Gordon)

**Where.**
- `.env`: the three Google values are set, and `HD_LETTERS_DRIVER=google`.
- Settings `google.letters_folder`: the folder shared with the office Gmail account Peter and Maria Pia use.
- `laravel-kit-spec.md` 8.2: "The production Google credential exists on the production server only."
- `plan-v2.md` section 5, "Google access": staging uses a separate test account that owns nothing real.

**What is wrong.** Connecting now was Gordon's call ("Let's get Google connected now"), and it worked. Two consequences are not yet planned for:
- **Reach.** Any session on this Mac that can run artisan can read every Doc the app made. That is 30 real letters and reports today, and every converted letter after the full run. This is the risk the spec's rule exists for.
- **Duplicates at cutover.** The rehearsal database's 30 converted Docs, 3 test Docs and the pictures sit in the folder Peter will work in. A fresh import into production knows none of them, so the real run makes a second Doc for each of those 30 files (4604, 8695, 9541, 9755, 9911, 9917, 10182 to 10199 and 10201 to 10206). If Peter writes in a rehearsal Doc before then, his words end up in the copy production does not know.

**The fix** (pick one now and write it into the cutover runbook):
- **(a)** At cutover, production adopts the rehearsal's Docs for those files. A small command copies `letter_doc_id`, `letter_mark`, `letter_name`, `letter_revision`, `letter_filled` and `letter_sent_at` from the rehearsal database.
- **(b)** The runbook trashes them first by their marks. Until then, Peter is told not to write in them.

Either way, once the server holds its own consent, revoke this Mac's refresh token or move the Mac to a test account, as 8.2 asks.

### 7. The build's test Docs are still readable by link, and the test files are still on the Dashboard

**Where.**
- The "Build tests" folder inside the letters folder: 3 Docs, those of files 10208 and 10209 shared by link.
- On the rehearsal database, files 10208 to 10210 are not hidden (`hidden_at` empty) and are the newest three on the Dashboard.
- File 10207 (deleted) still points at a stand-in Doc, so "Open the Doc" on it leads nowhere now.

**What is wrong.** The two shared test letters hold invented text. Each carries the logo, Peter's signature scan and a PE stamp, and anyone who has the link can read them. Their addresses are in `storage/logs/laravel.log` (2 each, from the log mailer). Their IDs are in `build-log-app.md`, which is tracked in git and synced. This is not client data, which is why it is not weighted a blocker. But nothing needs them public now.

**The fix.** Trash the three test Docs and the folder, by hand in Drive or with the app's Google class. Mark files 10208 to 10210 deleted, and clear 10207's stand-in letter fields.

---

## Minor

### 8. The unused signed stamp address still serves the PE stamps without a login
- **Where:** `routes/web.php:52`, `GET /stamps/{stamp}` (signed, 30 minutes, no login). `app/Letters/LetterContent.php:118` still makes such an address on every fill.
- **What is wrong:** nothing hands it to Google since W5 (the README says so). `config/hd.php:192` still says Google fetches the photos "by a signed address".
- **Fix:** remove the route, its controller and the signed address (the stand-in reads the path), and correct the comment.

### 9. "Send the letter" leaves the link sharing on when the mail then fails
- **Where:** `app/Actions/SendLetter.php:73` shares, then `:78` posts. A refusal from the mail service throws `CannotSend` after the Doc is already readable by link. The same happens if `shareByLink`'s own answer is lost.
- **What is wrong:** nobody holds the link, so exposure is small, but the file does not know its Doc is public. This is unchanged since P2.
- **Fix:** on a plain refusal, take the sharing off again, or say on the file that the Doc is shared though no letter went.

### 10. A new consent does not revoke the old refresh token
- **Where:** `app/Console/Commands/GoogleConnectCommand.php` 111 to 116. `--again` overwrites `GOOGLE_REFRESH_TOKEN` in `.env`.
- **What is wrong:** the old token stays valid until it is revoked or goes six months unused.
- **Fix:** after the new token is saved, post the old one to Google's revoke endpoint, and say so without showing either.

### 11. Settings accepts a template link the app cannot open
- **Where:** `app/Http/Requests/UpdateSettingsRequest.php:34` checks only that the link is a Doc's.
- **What is wrong:** with `drive.file`, a template Peter makes or copies himself cannot be opened by the app. Every new letter then fails until somebody runs "Test Google" and reads why.
- **Fix:** on save, ask Google whether the app can open the Doc (`nameOf`). If not, refuse with: "The app can use only the template it made: edit that one in Google Docs."

### 12. "Letter sent" on a converted file is a guess shown as a fact
- **Where:** `resources/views/files/show.blade.php:234` and the board, read from `letter_sent_at`. It is set to the old record's last-edit time (`ConvertOldLetter.php:117`) or to the job's day (`ConvertV2Report.php:104`).
- **What is wrong:** the screen shows the old record's last-edit time, to the minute, as when the letter was sent. The builders recorded this as a decision (W6 decision 2, W8 decision 3).
- **Fix:** keep the tick, but label the date "from the old system" (for example "Letter: last edited in the old system Mar 3, 2024").

### 13. An old paid invoice with no amount or no wording reaches a dead end
- **Where:** `app/Exceptions/CannotSend.php:79`, together with `show.blade.php` 343 to 345 (a paid invoice's panel has no form).
- **What is wrong:** "Send the paid copy again" refuses with "Enter both under Invoice description", but for a paid invoice there is no form to enter them in. That is 1 invoice on the rehearsal data; the other 63 such invoices are unpaid and have the form.
- **Fix:** a different message for paid invoices ("The old system recorded no amount or wording for this paid invoice"), or allow both to be entered on an old paid one.

### 14. A file whose booking was cancelled looks like any other in search results
- **Where:** `resources/views/files/_rows.blade.php` 22 to 27 shows only the four ticks.
- **What is wrong:** the search line says such files are included, but nothing marks which ones they are.
- **Fix:** a small "Booking cancelled" badge beside the ticks.

### 15. People the old system marked "copied" are copied when an old letter is sent again, and nobody can take them off
- **Where:** `app/Mail/FileMail.php` 120 to 128. `show.blade.php:277` says they will be copied, but with the forms gone there is no way to stop it.
- **How many:** 588 imported files have such a person, 1 of the 30 converted files does, and 0 of the 434 the cutover will convert.
- **Fix:** on an imported file, a tick box per person, unticked, before "Send the letter again".

### 16. The orchestrating thread's state file names a client and two streets (not the app)
- **Where:** `docs/build-state.md` lines 29, 31, 40, 53 and 54 name a client's surname and two of the family's street names. That file is tracked in git, pushed and synced, and handed to every agent.
- **What is wrong:** the handoff allows counts and IDs only (section 3). The builders' own log and the app repository hold none (the diff and all 16 commit messages were searched).
- **Fix:** use file numbers there.

---

## What holds

### Google
- **Where the secrets live.** In `.env` only, read only by `app/Letters/GoogleSession.php` (and written once by `GoogleConnectCommand.php:113` through `EnvFile`).
  - The byte search found no copy in 684 app files, the app's and the kit's git objects, 59 files of the data folder, 6,310 + 12,439 temp files, 494 transcript files, 1,224 files of the Sancho tree, or its 22 MB of git objects. The dump folder beside `legacy.sqlite` was not opened.
  - `laravel.log` has 0 lines with `ya29.`, `Bearer `, `client_secret`, `refresh_token`, `1//0` or `GOCSPX`.
  - No HTTP logging hook exists. The Connections panel shows one sentence (`GoogleSession::standing()`, `settings/edit.blade.php` 214 to 223).
  - The short-lived access token is kept encrypted for 45 minutes: 1 row in the cache table, an encrypted payload.
  - Settings hold folder and template IDs only.
  - The command's test asserts that neither the token, the secret nor the access token is printed.
- **Scopes.** `drive.file` alone, offline, `prompt=consent`, PKCE S256 (`GoogleSession.php` 90 to 102). The redirect goes back to 127.0.0.1 on a random port (`ConsentListener.php:28`). The state is compared with `hash_equals` (`GoogleConnectCommand.php:107`). Every scope asked for must be granted (`GoogleSession.php` 133 to 137). `--docs-scope` is never needed (W7).
- **Nothing shares with a person.** The only permission the code makes is `type: anyone, role: reader`, in two places: `lend()` (line 248, removed afterwards; finding 1) and `shareByLink()` (line 457, Send). No user, group or domain permission exists in the code, and `allowFileDiscovery` is never set, so a shared Doc is not findable by search.
- **What Send exposes.** The letter only, last of all: after the stamp and tags are checked and after the PDF and revision are made. The `/preview` link and the PDF are mailed. No real letter has been sent: the message log's letter lines are all on the invented files 10207 to 10209.
- **A dropped line during Doc creation.** The mark is saved before the copy or blank Doc is asked for, and the next try puts a stranded Doc in the trash by its mark (W7 commit f85e31a, tested). One gap remains: if Drive's search has not yet caught up when the next try looks, it forgets the mark and the stranded Doc stays, private, in the folder. W7 found one such Doc by listing.

### The conversions
- **Wrong database.** Both old-system connections are opened read-only (`config/database.php` 65 to 87). A probe insert was refused on both ("attempt to write a readonly database"). `check()` refuses a non-SQLite connection, an unnamed file, or a database without the old tables (`OldSystem.php` 45 to 62, `V2Reports.php` 39 to 54), so `--from` pointing at the app's own database is refused. On a database whose files carry no WordPress or v2 note (the demonstration set), nothing is converted.
- **Untouched sources.** `legacy.sqlite` was last changed 2026-10-02 00:36 and is mode `r--------`. The four rehearsal copies are unchanged since they were made. The five v2 backups used keep their own dates (2015 to 2020). `extract.py` opens them read-only.
- **Skips what is done.** Every second run in today's outputs says "already converted" for what was done (12 letters and 3 reports twice, 12 letters once, 2 v2 reports once) and made nothing for them. A letter made in v4 is never replaced, and one sent from v4 is never re-made.
- **Tracked paths.** Outputs go to `storage/app/private/conversion/` and photos to `storage/app/records/`; `git check-ignore` confirms both. The diff and the 16 commit messages hold no real name, address or Doc ID. `resources/v2/*.html` is v2's standard firm wording.

### The File screen (`resources/views/files/show.blade.php`)
- The date sits large beside the client's name, above the address (16).
- The board shows Letter sent, Invoice sent, Paid and Receipt sent with dates (22), and as ticks on the Dashboard (`_rows`) and "Been here before" (`_other-files`).
- The status, "Closed" and "Booked" are gone; a cancellation is a note with a way back (24 to 35).
- Other people are plain text (207 to 218).
- The Letter panel stands above the Job (220, 299). "Not imported yet" shows where the old system holds the letter (278 to 280), and `FileLetterController` refuses to make a new letter there.
- The invoice description is a 12-line box per job (350 to 352).
- An old invoice goes again without a number, as recorded (409, 413).
- The migration keeps cancellations and receipt dates and was run after a backup.
- Normal use: the 26 browser tests and the feature tests pass. The only dead end found is finding 13.

## The checks

Run in the scratch copy with Herd's PHP 8.5 (`php85` and Herd's `composer`). Outside Herd's isolated site folder, `herd` picks PHP 8.4, and the project requires 8.5.

| Command | Result |
|---|---|
| `composer test` (with the browser suite) | **1,426 passed, 5,853 assertions, 0 failed**, 29 s. The agent-format summary says "warnings: 1" with no detail; a plain Pest run of the same suite shows none (W7 and W8 noted the same warning). |
| `composer lint` (Pint) | **passed** |
| `composer analyse` (Larastan) | **passed, 0 errors** |

The 6 probes (4 files) passed as written to record the behaviour above. They were never part of the app and are deleted.

## Not done

No Google call was made, so the current sharing state of the pictures and the look of the 30 real Docs are unchecked. No Doc, photo or letter text was opened. The app was not served.
