---
name: Home Directions v4 review, app stage P2, safety lens
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of letters, invoices and mail (stage P2, steps D and E) asking one question, is it safe to put on a server and safe with people's data: 12 numbered findings, each with the file and line, what is wrong, the request or test that was actually run and its result, the fix and a weight; then what was checked and holds, whether the P1 fixes still hold, the new dependencies, and the real numbers from the checks
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 6ab6cf3]", "[doc:build-handoff.md]", "[doc:build-state.md]", "[doc:plan-v2.md sections 5, 8, 9, 10]", "[doc:laravel-kit-spec.md section 8]", "[doc:build-log-app.md, P1 fixes and P2]", "[doc:reviews/app-P1-safety.md]", "[run: herd composer test, lint, analyse, audit, 2026-10-02 09:26 CEST]", "[run: 56 scratch probe tests in 8 files, 3 runs of a scratch copy served as production on 127.0.0.1 (about 60 requests), 24 artisan commands on a scratch database, one run of the whole suite under a hostile shell, 2026-10-02 09:27 to 09:37 CEST; the scratch copy was kept outside the repository and removed]"]
status: written 2026-10-02 09:45 CEST by a reviewer that did not write the code; 1 blocker, 3 should-fix, 8 minor; no code was changed, nothing was staged or committed, no scratch file is left; no password, key or client detail appears in this file
---
# Review: app stage P2 (letters, invoices, mail), safety lens

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write the code and I changed none of it. The repository was at `6ab6cf3` on `feature/v4-build` with a clean working tree before and after.

**The conclusion first.** The stage is well built and most of what I attacked held: the PDFs cannot be fetched without a login, the reports door is shut without its token, no key reached a log or a screen, the PDF maker fetches nothing, and every new route asks for a login, the form token and the gate. One thing is a real hole. The switch that makes mail live reads the words "off" and "no" as "on". On a production-mode site with that line written the natural way, a message went to the client's address instead of the trap. That is the blocker, and it is a one-line fix. Three more things should be fixed before a server exists: staging starts life in production mode, so one line stands between it and real clients; a new server says "sent" when nothing left; and markdown typed into a name becomes a link in the client's mail. Eight are small.

Weights: **blocker** is a real hole (a way to leak or lose data, or to mail a real client by mistake); **should-fix**; **minor**.

How the evidence was made. The app was copied (`git archive` of `6ab6cf3`, plus `vendor`) into a scratch folder under the session's temp directory. The bad cases were run there as tests with the app's own test runner, against in-memory databases, with Brevo and Google faked. Where the question was what a real server does, that copy was served three times on `127.0.0.1` in production mode from a scratch database and asked with `curl`; the mailer was the log mailer every time, so nothing could leave this Mac. The login in those runs was a throwaway user with a random password made inside the script and deleted with it. Nothing was sent to Brevo or Google. The client data folder and Downloads were not opened. The scratch folder is removed.

---

## Blocker

### 1. The live-mail switch reads "off", "no" and any other word as "on"

**Where.** `config/hd.php` line 105: `'live' => (bool) env('HD_MAIL_LIVE', false)`. Used by `app/Mailing/MailTrap.php` lines 32 to 35.

**What is wrong.** The framework turns the words `true`, `false`, `null` and an empty value into real values. Every other word arrives as text, and `(bool)` of any text except `"0"` is true. So `HD_MAIL_LIVE=off` means live. The trap, its listener and the last lock in the Brevo transport all ask this one value, so all three open together. The dangerous places are exactly the ones the switch exists for: production between the import and the cutover, and a staging site left in production mode (finding 2).

**Evidence.**
- The app's own `config/hd.php` read with each value in the environment: `false`, `FALSE`, `False`, `0`, `(false)`, `null` and empty give false. `off`, `OFF`, `no`, `No`, `disabled`, `not-yet` give **true** (as do `true`, `1`, `yes`, `on`).
- The scratch copy served as production with `HD_MAIL_LIVE=off`, a trap address set, and the log mailer. The app reported `isLive=true`. Logged in, "Send the invoice" pressed through the real form: the screen said "Invoice sent to" the client's address; the message log had two rows, to the client and to the office, neither marked as trapped; the message written by the mailer was addressed `To:` the client with no "[Test, meant for" in its subject.
- The same run with `HD_MAIL_LIVE=false`: `isLive=false`, the message went to the trap address, the subject began "[Test, meant for", both rows were marked trapped.
- In a test posing as production with Brevo faked and the configuration read with `off`: Brevo was handed the client's address as `to` and the office as `bcc`.

**The fix.** Live only when the value is the real `true`: `'live' => env('HD_MAIL_LIVE') === true` (the framework gives a real `true` only for the word `true`). A test that reads the configuration file with a table of words (`off`, `no`, `0`, `disabled`, `yes`, `1`, `on`, `true`) and expects live for `true` alone. Say in `.env.example` that only the word `true` switches it on.

---

## Should-fix

### 2. A staging site starts life in production mode, so one line is all that keeps it from mailing real clients

**Where.** `.env.example` line 17 (`APP_ENV=production`), lines 66 to 71; `app/Mailing/MailTrap.php` lines 32 to 35.

**What is wrong.** "Live" is two things together: the production environment and the switch. That is sound for a site whose environment line says `staging`. But Forge copies `.env.example` into every new site, staging included, and after the P1 fix that file says `production`. Nothing in the app can tell the two sites apart, so on staging the first lock is already open and the switch (finding 1) is the only one left. Stage P4 puts the real history, with its client addresses, on staging for the rehearsal. The plan's rule is that staging mail never reaches a client. [doc:plan-v2.md section 10; doc:laravel-kit-spec.md 8.2]

**Evidence.** `.env.example` as committed: `APP_ENV=production`, `HD_MAIL_LIVE=false`, no trap. The runbooks do not yet tell Gordon to change the environment line on staging: a search of the four `runbook-*.md` files for `APP_ENV` finds nothing. The builder's own tests, which I reran, show the consequence both ways: posing as `staging` with the switch on, nothing goes to a client; posing as `production` with the switch on, the client is mailed. An environment file copied from production to staging, which the kit forbids by instruction only, would therefore mail real clients from staging.

**The fix.** Tie "live" to the site's own name as well, so a copied or mistaken line is not enough: for example a setting that names the one host allowed to send (`HD_MAIL_LIVE_HOST`), compared with the host in `APP_URL`, with a test. And in the paperwork (W2): staging's list of settings begins with `APP_ENV=staging`.

### 3. A server on the log mailer says "sent" when nothing left, and writes the whole message and its PDF into the log

**Where.** `.env.example` line 59 and `config/mail.php` line 19 (`MAIL_MAILER=log` is what a new server starts with); `app/Mailing/MailTrap.php` lines 52 to 60 and 119 to 124 (the log and array mailers are let through anywhere); `app/Mailing/Outbox.php` lines 62 to 83.

**What is wrong.** The log mailer is treated as harmless everywhere, which is right on a developer's machine. On a server it means: until `MAIL_MAILER=brevo` is entered, every Send looks like it worked. The invoice is marked issued, the history gains a "sent" line, the message log shows the client's address and "Sent", and the client received nothing. The full message, the client's address and the PDF attached are written into `storage/logs/laravel.log`. P1 already made `hd:user` refuse the log and array mailers on a server; client mail was not given the same refusal.

**Evidence.**
- The scratch copy served exactly as `.env.example` leaves a new site (production, log mailer, switch false, no trap). "Send the invoice" pressed: the screen said "Invoice sent to" the client's address; the message log had rows to the client and the office with a sent time and no trap mark; the invoice had an issue date; the history had a `sent` line. The log file was 80,597 bytes and held the message addressed to the client with the PDF attached.
- A test posing as production, live, with the log mailer: the same "sent" record, nothing handed to Brevo, 52,507 bytes written by the mailer, with the client's address and a PDF part in them.

**The fix.** Outside a developer's machine (the one rule P1 wrote, `DeveloperMachine`), refuse the log and array mailers for client mail with a message that says what to set, as `hd:user` already does; with a test. If a server must be able to run without Brevo for a day, record such a message as "written to the log, not sent", never as sent, and leave the invoice not issued.

### 4. Markdown typed into a name or an address becomes a link or a remote image in the client's mail

**Where.** `resources/views/mail/invoice.blade.php` lines 3 and 8; `resources/views/mail/letter.blade.php` lines 3 and 5. The values come from `Client::salutation()` and `Property::oneLine()`.

**What is wrong.** Both messages are markdown mails. Blade escapes HTML in the names and the address, and the result is then read as markdown, which Blade does not escape. So `[words](address)` in a first name is sent as a working link, and `![](address)` in a street is sent as an image fetched from that address, in a message from the firm's own mailbox, signed by the engineer. Today only the three users can type a name. From stage P3 the name and address come from Calendly's public booking form, and P4 brings in ten thousand old records whose punctuation was never checked.

**Evidence.** Through the real New File form (accepted, no validation error): first name `[Your invoice is overdue: pay here](https://evil.example/pay)`, street ending `![](https://evil.example/pixel.gif)`, town `Ridgefield <b>bold</b>`. Then "Send the invoice". The HTML of the message contained one link to `https://evil.example/pay` with the text "Your invoice is overdue: pay here" and one image from `https://evil.example/pixel.gif`. The raw `<b>` did not survive (HTML is escaped; only markdown gets through). The `To:` name carried the bracketed text as well.

**The fix.** Escape markdown in every value that comes from a record before it goes into these two views (one helper, used in both, with a test that sends the strings above and finds no link and no image from them); or write the two messages as plain Blade views instead of markdown. Before P3 opens the door to Calendly.

---

## Minor

### 5. A message is sent first and written down second, and a timeout is recorded as "not sent"

**Where.** `app/Mailing/Outbox.php` lines 62 to 83; `app/Mailing/BrevoTransport.php` lines 60 to 69.

**What is wrong.** The message is handed to Brevo, and only then are the message-log rows, the history line and the invoice's issue date written. If that write fails, the client has the message and the system has no trace of it. And when Brevo does not answer within 30 seconds, the log says "Not sent" as a fact, though Brevo may have taken it; the natural next act is to press Send again, and the client gets two.

**Evidence.** Posing as production, live, Brevo faked: with the write of the message-log row made to fail ("database is locked") the request answered 500, Brevo had been handed 1 message, the message log had 0 rows and the invoice was not marked issued. With Brevo's answer replaced by a 30-second timeout: both rows read "Not sent" with the timeout as the reason. Whether Brevo would really have delivered in that case is not demonstrated; no account exists.

**The fix.** Write the rows before the send, marked as being sent, and complete or fail them afterwards. For a timeout, say "may have been sent; check Brevo before sending again".

### 6. A template copy whose answer is lost is made again: two Docs for one file

**Where.** `app/Letters/GoogleLetterDocs.php` lines 47 to 55; `app/Actions/PrepareLetter.php` lines 59 to 65; `app/Jobs/KeepLetterCurrent.php` lines 30 and 41 to 44 (five tries).

**What is wrong.** The Doc's identifier is kept only when Google's answer arrives. If Google makes the copy and the answer is lost, the next try copies the template again. The first Doc stays in the letters folder, named with the client's surname and address, belonging to no file. The lock added in the restart stops two people making two Docs; it does not cover this.

**Evidence.** With Google faked so that the first copy request times out and the second answers: first try "Google could not be reached to copy the template", second try done; 2 copy requests were sent. That a real Google would have completed the first copy is by construction, not demonstrated.

**The fix.** Mark each copy with the file's number (Drive's own `appProperties`) and look for a Doc so marked before copying again. Or accept it and have the Connections panel list Docs in the folder that no file points at.

### 7. The last lock looks at the envelope; Brevo is handed the headers

**Where.** `app/Mailing/BrevoTransport.php` line 50 (the guard reads the envelope's recipients) and lines 92 to 96 (the request to Brevo is built from the message's To, Cc and Bcc).

**What is wrong.** For a mail service reached by its web interface, the addresses in the request decide who gets the message, not the envelope. The two agree today because the framework never passes its own envelope. The third lock is described as holding "in case anything ever reaches it another way", and that way it does not hold.

**Evidence.** Posing as staging with a trap address: a message addressed to a client, sent straight through the transport with an envelope naming only the trap address, was accepted, and Brevo (faked) was handed the client's address as `to`.

**The fix.** Run the guard on the addresses the request is built from.

### 8. A long name makes a letter impossible to send

**Where.** `app/Actions/SendLetter.php` lines 52 and 53; `app/Letters/LetterName.php` lines 27 to 35; the lengths allowed in `app/Validation/ClientFields.php` and `PropertyFields.php`.

**What is wrong.** The kept PDF is named after the letter, and the letter's name is built from the street, the unit, the town and the surnames with no limit. The forms allow 400 characters of address and 200 of surname; a file name may be 255. Past that, Send fails with a server error and nothing says why.

**Evidence.** Through the real New File form, with every field at the length the form allows: accepted; the letter's name was 621 characters; "Send the letter" threw `UnableToWriteFile`. Path characters are not the problem: `../`, quotes, slashes and line breaks are all stripped from the name (checked below).

**The fix.** Cut each part of the name to a sensible length, or name the kept file by the file's number and the time and use the long name only for the attachment.

### 9. One odd report stops a batch, and a batch has no limit

**Where.** `app/Actions/RecordDeliveryReport.php` lines 82 to 89; `app/Http/Controllers/Hooks/BrevoController.php` lines 34 to 41.

**What is wrong.** Only a caller with the token gets this far, so this is about a clumsy or forged report from someone who holds it. A time far out of range is a server error, and the reports after it in the same batch are not recorded. Any time is otherwise believed. A batch is processed whole, one query per report.

**Evidence.** With the right token: `ts_event` of `99999999999999999999`, `1e30`, the largest integer, or a fifteen-digit number each answered 500 (`InvalidFormatException`); in a batch of two, the good report after the bad one was not recorded. A report dated the year 2000 was recorded as opened in 2000, one dated 2100 as delivered in 2100. A batch of 20,000 reports (2.1 MB) ran 20,000 queries and answered 204 in 0.95 seconds on an in-memory database. On the served copy the 500 was the plain error page, with no detail.

**The fix.** Take the report's time only when it lies within a day or so of now, otherwise use now; catch a failure per report; refuse a batch over a few hundred.

### 10. A letter is shared and its PDF kept before the app knows the mail can go

**Where.** `app/Actions/SendLetter.php` lines 49 to 55, then line 60.

**Evidence.** Posing as staging with Brevo as the mailer and no trap address: "Send the letter" was refused with the right message and nothing was handed to Brevo, but the Doc had already been set to "anyone with the link" and one PDF had been kept, with no line in the message log pointing at it.

**The fix.** Ask the trap where each recipient's mail would go (it throws when it cannot) before sharing the Doc and making the PDF.

### 11. Google's access token sits in the database in plain text

**Where.** `app/Letters/GoogleLetterDocs.php` line 166 (`Cache::remember`), with `CACHE_STORE=database` on a server.

**Evidence.** With the database cache: after one call the `cache` table held one row whose value was the access token as plain text, expiring 45 minutes later. The token itself lives about an hour, but the nightly archive copies the database, so each archive carries whichever token was current. The refresh token and the client secret were not in any table (searched: `sends`, `history`, `settings`, `jobs`, `failed_jobs`, `cache`, `files`, `invoices`).

**The fix.** Keep it encrypted (`Crypt::encryptString` around the value), or in a store that is not archived.

### 12. One-line fields accept line breaks

**Where.** `app/Validation/ClientFields.php` lines 22 to 34; `app/Validation/PropertyFields.php` lines 22 to 24 (`string` with a length and nothing else).

**Evidence.** Through the New File form, a first name, last name and street each carrying a line break followed by `Bcc: ...` were accepted and stored with the line break in them. They did no harm in the mail (below), and the email field refused the same trick. But they are written as they are into the Doc's tagged places and shown on every screen.

**The fix.** One rule for single-line fields that refuses control characters, used by both field lists, with a test.

---

## What was checked and holds

**1. Mail leaving by mistake.**
- Posing as staging, local and testing with the switch on: never live (the builder's tests, rerun). On staging with a trap address, extra fields posted with Send (`to`, `cc`, `bcc`, `email`, `trap`, `meant_for`) moved nothing: three messages, each handed to Brevo for the trap address only, with no cc or bcc. Nothing a person can type reaches the trap address, the office copy or the switch: all three are read from the environment only, and a Settings save carrying keys such as `hd[mail][trap]` and `from_address` stored 0 rows.
- A queued message and a message sent through a named mailer were trapped too. On staging with no trap address, the `smtp`, `failover` and `sendmail` mailers were each refused before connecting.
- A letter with a person marked "copied": on staging everything went to the trap address alone.
- Header injection: a line break followed by `Bcc:` in the first name, last name and street produced no extra recipient; the envelope held the client and the office only; the subject and the `To:` name were folded onto one line. The same in the email field was refused by validation.
- Two presses of Send send two messages. That is the Resend button doing its job; the builder has asked Gordon whether Send should ask first.

**2. The receiving end for reports.** Shut with no token on the server whatever is presented (403 four ways, an empty bearer against an empty token included). With a token set: none, a wrong one, a prefix of the right one, the token in the query, in the body, or as basic auth were all 403 and changed nothing. With the right token: 204, no cookie set, `GET` is 405. A report can only touch rows that match both its message name and its address: array values, `%` wildcards and another row's id reached nothing, and the other file's row stayed untouched. Not JSON, a bare number, 600 levels of nesting and an empty body all answered 204 and wrote nothing. A reason carrying a script tag was stored (cut to 300 characters) and came back escaped on the file screen. The limit is 240 a minute per connecting address: the 241st was 429, forged `X-Forwarded-For` and `X-Real-IP` headers did not slip it, and it counts refused tries. The sender is known only by the token; Brevo offers no signature, so the token must be long and random and replaced if it leaks.

**3. Stored PDFs and links.** They are kept under `storage/app/records/` (or `HD_RECORDS_PATH`), which no web address reaches. On the served copy a kept PDF was fetched by a logged-in user (200, `application/pdf`, `no-store`) and by nobody else: as a visitor the route answered 302 to the login, and four guessed addresses for the file itself answered 404. The folders were made `0700` and the file `0600`. A PDF is served only under its own file: another file's message under this file's address was 404, as were a made-up id, a traversal in the id and everything on a hidden file. A row made to point at `../../../.env` answered 500 and served nothing. The stamp address needs this app's signature: unsigned 403, a made-up signature 403, one stamp's signature on the other 403, a later expiry 403, an extra parameter 403, after 31 minutes 403. The stand-in Doc address cannot be walked (five traversal tries, all 404). The framework's own storage address answered 403 without a signature for a kept PDF, a stand-in Doc and the local logins file, for reading and for writing. All of these paths are ignored by git (`git check-ignore` on each).

**4. The Google and Brevo wrappers.** Keys are read from the environment through `config/services.php` and nowhere else. With marker values for the Google client secret, refresh token and access token, the Brevo key and the reports token, and Google and Brevo made to fail seven ways (refused sign-in, unreachable, 500, 401 twice, Brevo 401, Brevo timeout): none of the five appeared in 43,084 bytes of log including stack traces, in anything shown to the person, or in any table except the access token of finding 11. Every call has a deadline (5 seconds to connect, 30 in all, 15 for the sign-in); nothing retries by itself except one repeat after a 401, which is safe. A queued letter job carries the file's number only (699 bytes, no name, address or email). A hostile surname and street (`../../`, quotes, `?alt=media&x=#frag`, a line break, `{{stamp}}`) reached Google as a Doc name of letters, digits and hyphens only, and as text inside a JSON request; no identifier or path was built from them. In Settings, a template link is cut down to the Doc's identifier (letters, digits, `_` and `-`), and `id/../..`, `id?alt=media`, a line break and a path were refused.

**The PDF maker.** Every value in the invoice page is escaped: seven hostile fields each came out as text, with no tag. Handed raw hostile HTML directly, with a listener on `127.0.0.1` to catch any fetch: remote stylesheet, `@import`, `@font-face`, background image, plain and scheme-less images, `file://` and bare paths to the scratch `.env` and `/etc/passwd`, `php://`, `phar://`, object, iframe, embedded PHP, script, and an SVG carrying a remote and a local image. The listener saw 0 requests; the PDF held nothing from either file and no script; the embedded PHP did not run.

**5. Invoice numbers.** No public route takes or shows one. The only addresses a visitor can reach are the login, the password link, `/up`, the reports door (token), the stamp address (signature) and the framework's storage address (signature). The invoice routes go by the file's number and sit behind the login. Numbers are drawn with the system's secure random source from those free in the month, and the table refuses a repeat.

**6. New routes and forms.** All 12 new routes were read from the production route list. Ten sit behind the login; with the gate made to say no, each of the ten answered 403, so the authorisation is really wired on every one. Posing as production with no form token, the five changing routes answered 419 and sent nothing; the same on the served copy. Extra fields sent with the job form (`letter_doc_id`, `letter_name`, `letter_sent_at`, `letter_filled`, `client_id`, `property_id`, `hidden_at`, invoice number, paid date, total, discount, `pdf_path`) were not stored; "sent" and "paid" cannot be set by hand; a payment was recorded for the logged-in person at the present time whatever was posted. Stamp uploads judged by their bytes: PHP named `.png`, HTML named `.gif`, SVG named `.png` and a file named `.php` were refused; 6 MB was refused; an image named `../../stamp.png` was kept under the app's own name for it. Hostile text came back escaped on the file screen, the stand-in Doc page and Settings (0 raw, 17 escaped on the file screen).

**The P1 fixes still hold.**
- `.env.example`: production, debugging off, a placeholder address, secure cookie, log level `info`, no password of any kind (searched).
- The seeder: refused with "never seeded on a server" in production, in staging, in local mode with a real address, and with the placeholder address; 0 users each time.
- Wiping commands: `migrate:fresh`, `migrate:refresh`, `migrate:reset`, `migrate:rollback` and `db:wipe`, each with `--force`, were refused in all four of those states; all 21 tables were still there.
- The tests on their own database: the whole suite run with `DB_DATABASE` pointing at a scratch file, `APP_ENV=production`, `MAIL_MAILER=smtp`, `HD_MAIL_LIVE=true`, a trap address, the Google driver, and made-up Brevo and Google values all set in the shell: 868 passed; the file's marker row and its one user were untouched and no table was added. The run wrote nothing to the log.

---

## New dependencies

`composer.json` gained one line, `dompdf/dompdf ^3.1`. It brings four more. All five are current releases and none is abandoned:

| Package | Version | Released | Needed for |
|---|---|---|---|
| `dompdf/dompdf` | 3.1.6 | 2026-07-20 | the invoice PDF |
| `dompdf/php-font-lib` | 1.0.2 | 2026-01-20 | dompdf's fonts |
| `dompdf/php-svg-lib` | 1.0.2 | 2026-01-02 | dompdf's SVG support (not used by the invoice) |
| `masterminds/html5` | 2.11.0 | 2026-08-18 | dompdf's HTML reader |
| `sabberworm/php-css-parser` | 9.5.0 | 2026-09-20 | the SVG library's styles |

`herd composer audit`: no advisories. `composer outdated --direct`: nothing behind. No npm package was added. Google and Brevo are reached with the framework's own HTTP client, so neither brought a library. dompdf has a history of holes around remote files and SVG; the options that close them are set in `app/Support/Pdf.php` and were tested above. Keep it on the monthly updates list.

---

## The checks, run by me on 2026-10-02 at 09:26 CEST, PHP 8.5.10 through Herd, in the app folder

| Command | Result |
|---|---|
| `herd composer test` | passed: 868 tests, 868 passed, 3,054 assertions, 0 failed, 10.7 seconds |
| `herd composer lint` | passed |
| `herd composer analyse` (Larastan, level 8) | passed: 0 errors |
| `herd composer audit` | no advisories |
| the suite under a hostile shell, in the scratch copy | 868 passed; marker row untouched |

These match the builder's report in `build-log-app.md`.

My own probes: 56 scratch tests in eight files (26 on mail, 10 on the reports door, 9 on routes and forms, 1 on uploads, 4 on Google, 2 on PDFs, 4 others), three served runs with about 20 requests each, and 24 artisan commands against a scratch database.

## For whoever fixes this, and the stages that follow

- Finding 1 before anything else; it is one line and a test.
- Findings 2 and 3 before step B creates a server. Finding 4 before P3 lets Calendly write names.
- Not demonstrated, read in the code only: the trap writes the addresses a message was meant for into the log at `info` level (`app/Mailing/MailTrap.php` line 90). On a staging site holding the real history that puts client addresses in the log file. Worth dropping to the count of addresses.
- Not mine and left alone: the app repository still has a second working tree registered from an earlier agent (`git worktree list` shows one under the session's scratch folder, on a branch `p2-build` at `9706e8d`). It should be removed and the branch looked at before anything is pushed.
- Already raised by the builder and still open for Gordon: the Treasurer's name and the firm's Gmail address are in `config/hd.php`; whether a correction should rewrite letters already sent, which are public to anyone with the link.
