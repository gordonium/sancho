---
name: Home Directions v4 review, app stage P2, plan fit
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of letters, invoices and mail (steps D and E) against the plan and the requirements: the naming rule, the stamp, the tagged places under correction, sending and its half states, the Google class read against Google's manual, invoice numbers under a real race and a full month, the invoice PDF read as text, the mail trap attacked in local and staging modes, the history, the builder's 33 decisions, the real test numbers and the rules with no test; 20 numbered findings, each with file and line, the evidence, the fix and a weight
sources: ["[doc:build-handoff.md]", "[doc:plan-v2.md sections 2, 4, 5, 6, 7, 10]", "[doc:requirements.md R2 to R6]", "[doc:phase0-brief.md, Plan questions 4 onward]", "[doc:build-log-app.md, P2 and its 33 decisions]", "[doc:reviews/app-P1-plan-fit.md]", "[code:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 6ab6cf30927695dd822473a6f20216b54a9df4e4, read 2026-10-02]", "[run 2026-10-02 09:05 to 09:40 CEST: herd composer test, lint, analyse in the app folder; 59 reviewer probes on invented data in a scratch copy; 20 rounds of a real two- and three-process race on a scratch database; one run of the letter job through a real database queue]"]
status: written 2026-10-02, finished 09:45 CEST, by a reviewer that did not write the code; 0 blockers, 8 should-fix, 12 minor; no code was changed, nothing was staged or committed, nothing else was written in the Sancho tree; no client data was opened; the scratch copy was removed afterwards
---
# Review: app stage P2 (letters, invoices, mail), plan fit

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write this code and I changed none of it.

**The conclusion first.** Stage P2 does what the plan says, and it is well made. A letter is named by Gordon's rule exactly. The stamp follows the state for every kind of job. A correction changes the tagged places and nothing else, and I could not make it touch Peter's own sentences. The invoice is one editable field with a stored total, and the PDF reads right. Mail goes from the office with a copy to the office. I tried seven ways to get a message to a real-looking client from local and staging modes and none got out. Every action writes the history. Invoice numbers stayed unique in a real race between three processes.

I found no blocker. Eight things should be fixed, and they are all of one kind: the system says something went well when it did not, or lets a wrong thing go to a client without a word. The first two matter most. Twelve are small.

Weights: **blocker** is wrong behaviour a client or Peter would see, or a foundation the next stages cannot stand on; **should-fix**; **minor**.

## The numbers, run by me

In `/Users/gordonium/Dev/clc-laravel/hdonline-v4`, branch `feature/v4-build`, commit `6ab6cf3`, PHP 8.5.10 through Herd. The working tree was clean before and after (`git status` 0 lines both times).

| Command | Result |
|---|---|
| `herd composer test` | passed: 868 tests, 3,054 assertions, 0 failed, 10.4 s |
| `herd composer lint` | passed (Pint, check only) |
| `herd composer analyse` | passed: 0 errors (Larastan level 8) |

These match the build log exactly.

**How the findings were checked.** Where a finding says something happens, I ran it. The probes are six Pest files of invented data, 59 probes in all, run in a scratch copy of the commit (`git archive`, with a copy of `vendor`) under my session's temp folder, on the app's own test setup: in-memory database, no network, Google and Brevo faked. Each finding quotes what its probe printed. For invoice numbers I also ran real processes against a scratch SQLite file, and I ran the letter job once through a real database queue. Nothing was written inside the app folder. The scratch copy is removed.

---

## What holds (run, not read)

- **The naming rule.** `Home-Directions-letter_20261014_12-Shad-Hill-Rd-Ridgefield_Smith` comes out exactly. Punctuation goes, capitals stay, accents are written plainly (`Müller-Straße` gives `Muller-Strasse`, `Иванов` gives `Ivanov`). A couple with one surname gives `Smith`; with two, `Smith-Hale`. No street gives the town alone (`_Ridgefield_Smith`); no address at all gives `address-not-recorded`. The date is the job's, on the firm's clock: 03:59 UTC on the 15th is still the 14th.
- **The stamp.** All 36 combinations of three services, three modes and four states: Connecticut and New York got their stamp, New Jersey and Massachusetts none, virtual visits included. A corrected state moves it; a stamp chosen by hand and a sent letter keep theirs.
- **Corrections touch only the tagged places.** Client "Ada Stone" corrected to "Eda Stein" with this typed in the body: "The Stonework at the cornerstone is sound. Ada Stone asked about the keystone. Adamant: Ada's hearthstone." The block, the greeting and the Doc's name changed; that sentence did not. A client who lives at the property (the same address in two places, and typed a third time by Peter): correcting the property changed only the "Re:" line; correcting the mailing address changed only the block; Peter's sentence stayed. A template with the same tag twice: both filled, both corrected. Emoji and accents in a name: positions still right. Text typed right after a tagged place stays outside it.
- **Sending a letter.** The Doc is shared to read only; the PDF is made as it stands and kept; the revision is noted (3, then 4 on a resend after an edit); two PDFs kept, the first date kept. A correction after sending changed the Doc and left the kept PDF untouched.
- **A failure halfway through a fill** leaves the file knowing what it has and has not done, and the next run finishes it. The stand-in writes a fill in one go and Google takes it as one batch, so a Doc is never half filled. The file screen said "has not reached the Doc yet" in all three cases I forced.
- **Invoice numbers.** `HD-2610-712`; the month turns on the firm's clock (03:30 UTC on 1 November is still `HD-2610`). With 999 taken, the one left was found in half a millisecond. Three real processes opening a file at the same instant with two numbers free, 12 rounds: each time two got the two numbers and the third was told the month was full. Never a duplicate, never a clash.
- **The invoice PDF**, read as text and by eye: letterhead with the firm's address and phone; "Invoice HD-2610-588"; the date; "Bill to" with name and address; "For: Professional Opinion at:" the property, "on October 14, 2026"; the invoice description, line breaks kept; the price; "Amount due $950.00"; how to pay by check and by Zelle. One page. The paid copy says "Paid October 20, 2026. Thank you." and drops how to pay. The description on the file is the only wording that prints.
- **Mark paid** records who and when, sends the paid copy, refuses a second time, and refuses a price change afterwards. With no email on file the payment is still recorded and the screen says the copy did not go.
- **Mail.** Sender `office@homedirections.net`, "Home Directions"; the client as "to"; people marked copied as "cc" on the letter only; the office as a blind copy; no reply-to, so replies go to the office. One line per recipient in the log.
- **The trap.** Local and staging, Brevo as the mailer with a key: through the three buttons, straight at the mailer, a raw message through the named mailer, the same with the listener removed, and the transport by hand with an envelope that differs from the headers. With no trap address: 0 requests to Brevo. With one: every request went to the trap address only, with "[Test, meant for ...]" in the subject. Switching `HD_MAIL_LIVE` on changed nothing outside production. The set-your-password link is trapped on staging too.
- **Reports.** Delivered, opened and bounced each landed on the right recipient's line; an address in capitals still matched; a privacy proxy's "open" was not counted; no token, a wrong token and a token in the address all got 403.
- **History.** One whole job wrote 28 history lines: the four records made, the Doc and its name, each correction with old and new, the invoice's wording and total each time it changed, four "sent" lines with who they went to, the status changes, the payment and who recorded it. Sends and invoices refuse to be deleted.
- **The queue.** Through a real database queue the letter was made by the worker, and a later correction renamed the Doc by the worker. Those history lines carry no user, which is right: the system did it.

---

## Should-fix

### 1. A server whose mailer is still "log" tells Peter the message was sent

**Where.** `.env.example:59` (`MAIL_MAILER=log`); `app/Mailing/MailTrap.php:57` and `:119-124`; `app/Mailing/Outbox.php:62-83`.

**What is wrong.** The example file every server starts from sets the mailer that writes a message into the log and sends nothing. The trap leaves that mailer alone on purpose, for local work. Nothing stops it on a server. So a production site where that one line was not changed says "Invoice sent", marks the invoice issued and the letter sent, and nothing leaves the machine. The builder closed this same hole for letters (production refuses the stand-in, `AppServiceProvider.php:56-60`) and for the login link (`UserCommand.php:51`), but not for client mail.

**Evidence.** Probe M3, production with the live switch on and the mailer `log`: the screen said `"Invoice sent to real.client@example-client.test."`; the message log said `outcome=Sent`; `invoice issued: true`; `anything left this machine: 0`. The same on staging and on production not yet live.

**The fix.** Anywhere that is not a developer's machine, refuse to send a client message through a mailer that sends nothing, with the same plain notice as the trap's. One test per environment. The Connections panel in P3 should show it too.

### 2. A tagged place that is not in the Doc is recorded as written, and a letter can go out with `{{...}}` showing

**Where.** `app/Letters/Places/TaggedPlaces.php:70-72` and `:194` (lower-case names only); `app/Letters/LetterDocs.php:36` (`fill` says nothing back); `app/Actions/PrepareLetter.php:72-75`; `app/Actions/SendLetter.php:48-55`.

**What is wrong.** When a tag is missing from the Doc, the fill writes nothing there, and the file then records every value as written. Nothing tells anyone. Three cases, all run:
- **A template with a tag spelled wrong.** Peter edits the template himself in Google Docs. One slip there and every later letter carries a raw tag.
- **A place Peter typed over.** His own text stays, which is fair, but the system says the Doc is up to date when a later correction has not reached it.
- **A migrated letter** (stage P4). Unless the conversion makes each Doc with the same tagged places, a correction renames the Doc and changes nothing in it.

**Evidence.** Probe T4, a template with `{{Client_Name}}`, `{{client_adress}}` and `{{property address}}`: the file screen showed no warning; "Send the letter" answered `Letter sent to ada.stone@example.test.`; the Doc as sent read `{{Client_Name}}` / `{{client_adress}}` / `Re: Professional Opinion at {{property address}}`. Probe T5: the greeting retyped as "Dear Mrs. Stnoe,", then the client corrected: the Doc still said "Dear Mrs. Stnoe,", the file recorded `Dear Edna,` as written, and the screen did not say the Doc was behind. Probe P2 (a Doc with no places, as a conversion might make): name corrected from Cleint to Client; the Doc was renamed, its text still said "Dear Old Cleint,", and the file recorded all seven places as written.

**The fix.** Have `fill` say which tags it found. Record only those as written. Show on the file which places the Doc does not have ("this Doc has no place for the client's name; correct it by hand"). Refuse to send a letter that still holds `{{`, and say which tag. Tests for all three cases.

### 3. The stamp picture travels in the same batch as the names; if Google cannot fetch it, nothing is filled

**Where.** `app/Letters/GoogleLetterDocs.php:61-70` (one `batchUpdate`) and `:299`.

**What is wrong.** Google applies a batch whole or not at all (its manual says so). The stamp is put in by giving Google an address on this site to fetch. If that fetch fails (the site is behind a gate, the address is not public, the signature fails behind a proxy, the image is too large), the names, the address and the date are not filled either, and the letter cannot be sent. The screen only says a correction has not reached the Doc.

**Evidence.** Probe G1, Google faked to answer what its manual gives for an image it cannot retrieve: one batch of 22 requests went, the picture among the text edits; `letter_filled: null`; the job would retry (five tries, then stop); "Send the letter" answered `The message was not sent: Google could not fill in the letter (400): ... There was a problem retrieving the image`. **Not demonstrated** against real Google: that Google refuses the whole batch. What the app does with that refusal is demonstrated.

**The fix.** Fill the text first and the picture in a second batch. If the picture fails, keep the text, and say on the file that the stamp could not be placed and why.

### 4. An hourly job's invoice goes out for one hour's rate, with "[period]" in it

**Where.** `config/hd.php:66-69`; `app/Models/Invoice.php:77-87`; `resources/views/files/show.blade.php:225-229`.

**What is wrong.** For design work the file's price starts at the hourly rate, $475, and the invoice total is that price. There is nowhere to put the hours. The standard text carries the words "[period]" for Peter to replace. Nothing stops the invoice going as it stands. The P1 review said this stage "must say where the hours go" (its decision 16); it does not.

**Evidence.** Probe I3, an hourly file opened and sent with no edit: the PDF read `Time spent on the project at the above address during [period], ...` and `Amount due $475.00`; total stored 47500.

**The fix.** Ask Gordon which he wants: an hours box beside the rate (total worked out once and stored), or a price that starts empty for hourly work. Either way, refuse to send an invoice whose description still holds "[period]". Test both.

### 5. An old invoice that is not yet paid cannot be marked paid or sent here

**Where.** `app/Models/File.php:107-116`; `resources/views/files/show.blade.php:256`; build log, "For the stages that follow", P4 ("by design: it is a record").

**What is wrong.** An imported invoice has no number, and an invoice with no number cannot be sent or marked paid. That is right for the 10,000 old jobs. It is wrong for the jobs in flight on cutover day: visited, invoiced from v3, not yet paid. The plan brings each recent job's invoice across "with its text, total and paid state" and has Peter working "in one place from day one". [doc:plan-v2.md section 6] Maria Pia could not record those payments in v4.

**Evidence.** Probe P1, a job imported through `importFrom` with an unpaid invoice: `invoice number: null`; the screen offered no "Mark paid", no "Send the invoice", no PDF; the payment address answered `This file has no invoice to send.`; `paid_at: null`.

**The fix.** Decide before P4. Either the import gives a number to every invoice that is not paid, or the file screen offers "give this invoice a number" for an old one, after which it behaves like any other. A test with an imported unpaid invoice.

### 6. "Mark paid" is one click, mails the client at once, and cannot be taken back

**Where.** `resources/views/files/show.blade.php:266-270`; `app/Actions/MarkInvoicePaid.php:31-56`; `routes/web.php` (no way back).

**What is wrong.** A click on the wrong file sends that client "Paid, with thanks" for an invoice that is not paid. After that the invoice is settled for good: it cannot be un-paid, its price cannot change, and it can only be resent as paid. The plan's answer to a wrong click elsewhere is "reversible through the history". The builder raised this as a question for Gordon; I weigh it as a should-fix because nothing in the system can repair it.

**Evidence.** Probe I6: a second click answers `This invoice is already marked paid.`; a price change answers `The invoice is paid, so its wording and price are settled.` No route undoes a payment.

**The fix.** A confirmation that names the client and the amount, and "this was a mistake" on a paid invoice: it clears the payment, writes the history, and sends nothing by itself. Test both.

### 7. A Connecticut or New York letter can be sent with no stamp

**Where.** `app/Actions/SendLetter.php:40-58`; `resources/views/files/show.blade.php:288-290`.

**What is wrong.** Until a stamp image is in Settings the stamp's place is empty. The file screen says so in small amber print, but "Send the letter" works. A stamped letter is the product. [R3.7] On the first day, with the images not yet uploaded, letters would go out unstamped.

**Evidence.** Probe L2, a Connecticut file with no image in Settings: `Letter sent to ada.stone@example.test.`; stamp on file `ct`; the Doc has no stamp.

**The fix.** Refuse to send while the file's stamp has no image, and say where to add it. He can still choose "No stamp" on the file to send without one. A test.

### 8. The mail leaves before anything is written down

**Where.** `app/Mailing/Outbox.php:62-83`.

**What is wrong.** The message is handed to the mailer first; the log lines, the history and the "issued" mark are written after. If that write fails (the database is busy, the disk is full), the client has the message and the system has no record of it. Peter sees an error page, presses Send again, and the client gets it twice. The requirement is a log of every message. [R5.2]

**Evidence.** Probe M7, the write made to fail after the send: `mails that left: 1`; `log rows: 0`; `invoice issued: false`.

**The fix.** Write the log lines first, as "being sent", in their own short step; then send; then mark them sent or failed. A line stuck at "being sent" is then the honest record. A test.

---

## Minor

### 9. Loose ends when a send fails halfway

**Where.** `app/Actions/SendLetter.php:50-55`; `app/Actions/SendInvoice.php:37-41`; `app/Actions/MarkInvoicePaid.php:49-53`.

Nothing is half sent, but things are left behind. Probe H4 (the PDF fails after sharing): the Doc stays shared to anyone with the link, nothing was sent, and no history line says it was shared. Probe H5 (the revision fails after the PDF was kept): a PDF sits in the records with no message pointing at it. Probes I6 and I8 (no email on file): an invoice PDF is kept, and the invoice row is brought up to date with three history lines, though nothing went. The records folder is meant to hold "every PDF as sent".

**The fix.** Check the email and build the message before sharing or keeping anything; share last; keep the PDF only once the message has left, or mark it as not sent.

### 10. A very long Doc name cannot be kept as a PDF

**Where.** `app/Letters/LetterName.php:62-71` (no limit); `app/Actions/SendLetter.php:52-53`.

Probe N2b, the longest names the forms allow: a name of 342 characters; sending threw `UnableToWriteFile` (an error page, not a notice), and the Doc was left shared. A file name on the server stops at 255. Real names will not reach this; it is the missing limit that is the finding.

**The fix.** Cut each part of the name to a stated length (for example 60), and name the kept PDF by the file's number and the time.

### 11. Small things in the name and the letter's text

**Where.** `app/Letters/LetterName.php:42-70`; `app/Letters/LetterContent.php:34`.

From probes N1, N3 and P1:
- `12 1/2 Main St` becomes `12-12-Main-St`.
- An underscore is dropped with no hyphen: `Smith_Jones` gives `SmithJones`, `12_Shad Hill Rd` gives `12Shad-Hill-Rd`.
- A name in a script with no Latin spelling (`王`) becomes `client`.
- A file with no service (an old job) gets "Re:  at 5 Old Rd", with two spaces and no service.

**The fix.** Turn `/` and `_` into a hyphen before the rest is dropped; write "Re: 5 Old Rd" when there is no service.

### 12. Changing the service keeps the old price and wording

**Where.** `app/Http/Controllers/FileController.php:84-89`.

Probe L1: a file opened as Professional Opinion, then changed to Structural Design on the Job panel. The invoice read "Structural Design at:" with the opinion's wording and `$875.00`. Nothing on the screen said the price had stayed. The difference is $375.

**The fix.** When the service changes and the price and wording are still the old standard ones, offer the new standard with one click. Never change them silently.

### 13. A company is not named on the invoice or the letter when a person is

**Where.** `resources/views/pdf/invoice.blade.php:47`; `app/Letters/LetterContent.php:31-33`.

Probes I4 and L6: a client "Ada Stone" of "Stone & Hale Architects LLC". The invoice is billed to "Ada Stone"; the letter is addressed to "Ada Stone". The company shows only when nobody is named. Design clients are architects and builders. [doc:requirements.md, business context]

**The fix.** Ask Gordon. If wanted: the company on its own line under the name, in both.

### 14. The paid copy can differ from the invoice the client was sent

**Where.** `app/Actions/MarkInvoicePaid.php:39-44` (decision 3).

Probe I5: invoice sent at $875.00; the price and wording then changed on the file without sending again; "Mark paid" sent a paid copy for $500.00 with the new wording. The history shows it. The decision is sound (one field, as the plan says); the cost is that the client's two papers disagree and nothing says so at the click.

**The fix.** When the file differs from the invoice as last sent, say so beside "Mark paid".

### 15. A full month gives an error page, and the numbers are safe only inside a transaction

**Where.** `app/Invoices/InvoiceNumber.php:37-41`; `app/Actions/DraftInvoice.php:18-24`.

Probe I2: with all 1,000 numbers of a month taken, New File answered 500 with "a thousand invoices in one month"; nothing was half made (0 client rows added). At three jobs a week this will not happen. Separately: the clean result in the race above rests on New File's transaction taking the write lock first. With the generator called outside a transaction, two processes clashed in 3 rounds of 8 (the table refused the second; never a duplicate).

**The fix.** A plain notice instead of the error page. Say in `DraftInvoice` that it must run inside a transaction, so stage P3's Calendly intake does. A test that it does.

### 16. A replaced stamp image does not reach letters already made

**Where.** `app/Letters/LetterContent.php:47-50` (a picture is remembered by which stamp it is, not which image).

Probe L3: a new Connecticut image uploaded in Settings; a letter made before it did not show as behind, so it keeps the old image.

**The fix.** Remember the image's file name with the stamp, so unsent letters are brought up to date.

### 17. A setting can be destroyed

**Where.** `app/Models/Setting.php:26`.

Probe I10: `Setting::delete()` removed the row; sends and invoices refused. No screen deletes a setting today.

**The fix.** Add the same "never destroyed" guard and a test.

### 18. The example file gives every server `APP_ENV=production`

**Where.** `.env.example:17`, `:66-71`; `README.md`, "On a server".

The trap is two lines: production and the live switch. A staging site made from the example file is already "production", so there the trap rests on one line, and the stand-in for Google is refused. The README says to leave the switch off on staging; it does not say to set the environment to `staging`.

**The fix.** Say it in `.env.example` and the README. For W2: the staging checklist sets `APP_ENV=staging` first.

### 19. The Google class: what I could not run

**Where.** `app/Letters/GoogleLetterDocs.php`.

I read every request against Google's Drive and Docs manuals as I know them. The addresses, the request bodies and the field names are right for copy, read, batch update, rename, share, export and revisions. I found nothing that plainly cannot work. These are **not demonstrated**, and each should be looked at on the first real Doc:
- **Look after a fill.** Each place is filled by deleting the tag and then inserting the value. Google gives inserted text the style of the text before it. A tag at the start of a line, or the address block (inserted right after the name), may take a neighbour's style, and the line after the block may take the name line's spacing. If it shows: insert first, then delete.
- **A named range in two pieces.** Probe G2: when Google reports one range as two pieces, the whole value is written into each. Whether Google ever does that to these ranges I do not know.
- **Tags in a header, a footer or a second tab** are not read. With finding 2 fixed, the app would at least say so.
- **The credential's reach.** Copying a template the app did not make needs the wide Drive permission, which reaches all of that Google user's Drive. The plan says the credential "can reach only what the app needs". [doc:plan-v2.md section 5] That holds only if the app signs in as a Google user whose Drive holds the letters and nothing else. Gordon's question 4 in the build log decides it.
- **The refresh token.** If the Google app is left in "testing" its tokens stop after a week (from memory; unconfirmed, as the builder also says).
- **The export** asks for JSON in its Accept header while fetching a PDF (probe G3). I expect Google to ignore that.

### 20. Important rules with no test

**Where.** `tests/`.

The suite is strong: the trap, the reports, the tagged places and the Google requests are tested rule by rule, both ways. These have nothing guarding them:
- a server with a mailer that sends nothing (finding 1);
- a letter that still holds a tag being sent, a place missing from the Doc (finding 2);
- Google refusing a batch over the picture (finding 3);
- an hourly invoice as it goes out (finding 4);
- an imported unpaid invoice (finding 5);
- a letter sent while its stamp has no image (finding 7);
- the mail leaving and the write failing (finding 8);
- a send that fails after sharing, or after the PDF is kept (finding 9);
- two processes at one invoice number (I ran it by hand; the suite tests the table's refusal only);
- the letter job through a real queue (the suite runs it in line; I ran it by hand);
- the invoice PDF's own text (the suite reads the page it is printed from);
- the naming rule for a town with no street, a first name only, and a very long name;
- no screen has been looked at in a browser, as the builder says.

---

## The builder's decisions (33)

None closes a door that Calendly or search will need. One closes a door the import needs: finding 5. Those that need a word:

| # | Decision | Verdict |
|---|---|---|
| 1 | Status follows the facts | Sound. Run both ways (paid first; letter first). A file can be closed with its invoice never sent; that is a person's choice. |
| 2 | One log line per recipient | Sound; it is how Brevo reports. |
| 3 | Wording and price taken from the file until paid | Sound, and it is the plan's "one field". Cost: finding 14. |
| 4 | The number's month is when the invoice is made | Sound. |
| 7 | Sent while the person waits | Sound for three users. Cost: finding 8. |
| 9 | Copied people get the letter only | Sound as a start; Gordon's to say. |
| 10 | Live means production and the switch | Sound. See finding 18. |
| 11 | Reports let in by a token; proxy opens not counted | Sound and honest. Many clients' mail hides real opens, so "Opened" will often never show. |
| 12 | One Google user with a refresh token | Workable. Which user decides whether the plan's "only what the app needs" holds: finding 19. |
| 14 | The letter's date is the job's | Sound; Gordon's to confirm. A Calendly reschedule will rename the Doc, which is right. |
| 15, 16, 17 | Surname in the name; greeting by first name; block only with a street | Sound. They match Gordon's example and the 320 clients with no street. |
| 18 | A corrected state moves the stamp unless chosen by hand or sent | Sound. |
| 19 | A correction reaches sent letters too | Follows R2.3. Gordon's to confirm. For P4: all migrated letters will be rewritten on a correction, so they must be made with the tagged places (finding 2). |
| 20, 31 | Only changed places rewritten; ranges dropped and named again | Sound. |
| 21 | The letter is made by a queued job | Sound; ran it through a real queue. For P3: a Calendly cancellation needs "put the Doc in the trash" and "was it touched?", and a restore needs it back. The interface has none of the three yet; nothing stops adding them. |
| 22 | The client's link is the "preview" address | Sound; to be looked at once. |
| 23 | The stamp fetched by a signed address | Workable. Finding 3. |
| 24 | Stand-in allowed on staging | Sound. See finding 18. |
| 26 | Every PDF kept by itself, on a disk no address reaches | Sound. For P4: an old link must lead to a PDF, so one new address that serves a kept PDF to a client will be needed. Nothing stops it. |
| 27 | Google refuses a fill on a stale reading | Sound. |
| 28 | Payment recorded even if the copy cannot go | Sound. |
| "by design" | An imported invoice cannot be sent from here | Closes a door for jobs in flight: finding 5. |

The rest (5, 6, 8, 13, 25, 29, 30, 32, 33) are sound and need no comment. Decision 6 (the letterhead and "how to pay" lines taken from the old system) I could not check against the old system; my brief did not open it.

## Against the requirements

| Requirement | Verdict |
|---|---|
| R2.3 fix once, right everywhere | Met for the system, the Doc's tagged places and the Doc's name. Silent where a place is missing: finding 2. |
| R2.5 one description, editable price | Met. |
| R3.1, R3.2 template and name | Met; the name is exact. |
| R3.5 read-only link, latest version | Met on the stand-in; Google's side written, not run. |
| R3.6, R3.7 stamp by state | Met; can be sent without: finding 7. |
| R4.1 invoice made with the file, as a PDF | Met. |
| R4.2, R4.3 three texts in Settings, new invoices only | Met; the three texts match the requirements word for word. |
| R4.4 send, mark paid with a paid copy, resend | Met. No way back from paid: finding 6. |
| R4.5 stored total and lines | Met. Hourly: finding 4. |
| R5.1 a real authenticated address | Met in the request Brevo is sent; Brevo itself not run. |
| R5.2 log of every message, delivery reports | Met, with the gap in finding 8. |
| R5.3 sends the latest version | Met: the Doc is brought into step, then exported. |
