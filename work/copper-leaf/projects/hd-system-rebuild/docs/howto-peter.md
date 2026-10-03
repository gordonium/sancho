---
name: Home Directions v4 how-to for Peter
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: One page for Peter, the engineer, in plain words and with the button names exactly as the screens show them. It covers finding a client or job by name, street or month; opening a job; New File by hand and the "been here before" prompt; the board of four steps; the letter in Google Docs (create it, open it, write it, send it, send it again); the invoice description and price; sending the invoice; "Not imported yet" on an old job; and the change history at the foot.
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 8e278ec: resources/views (dashboard, files/create, files/show, files/_rows, files/_match, files/_answers, files/_client-fields, components/board, settings/edit, auth/login); app/Search/FileSearch.php; app/Actions (OpenFile, PrepareLetter, SendLetter, SendInvoice); app/Exceptions/CannotSend.php; app/Mail/FileMail.php; app/Mailing/MailTrap.php; app/Matching/ClientMatcher.php; app/Letters/StandInLetterDocs.php (the letter's layout)]", "[repo: same commit, tests/Browser: LoginTest, DashboardTest, NewFileTest, FileScreenTest, LetterTest, InvoiceTest, ChangedScreensTest]", "[run: the app's local .env read for MAIL_MAILER and HD_MAIL_TRAP only, 2026-10-03 12:45: the log mailer, no trap address]", "[doc:plan-v2.md section 5]", "[doc:phase0-brief.md, Gordon's entries of 2026-10-03]", "[doc:build-log-app.md W2, W5, W9]", "[doc:build-state.md, 10:00 and 12:05 Oct 3]", "[doc:reviews/app-W3-walkthrough.md finding 9]", "[doc:reviews/app-W5-W8.md finding 12]", "[gordon 2026-10-03]"]
status: written 2026-10-03 about 12:50 CEST by a documents-only agent on Opus 5.5 from the screens of commit 8e278ec, read in the code and the browser tests and not clicked through. Must be checked against the app before go-live, because the screens are still changing (three later commits about Calendly bookings and the letter trash were not read). Real mail through Brevo and Calendly are not set up yet, the live system's own Google connection is not made, and the live web address is not decided.
---
# How-to for Peter

Words in quotes are exactly what the screen shows. If something cannot be done, a red notice at the top of the page says why.

**Not set up yet**
- **Mail (Brevo).** No letter or invoice reaches a client yet. On Gordon's Mac a Send button still says "... sent to" the client, and Messages says "Sent", but the message only goes into a log file.
- **Calendly.** Until it is connected, open every visit with "New File". After that, bookings open their own files; move or cancel those visits in Calendly, not here.
- **Google and the address.** Letters are real Google Docs on Gordon's Mac only. The live system's Google connection and web address come before go-live. Log in with your "Email" and "Password", then "Log in".

## 1. Find a client or a job
1. On the Dashboard, type in "Search by client, address or month (May 2022)" and press "Search": a surname, part of a street, a month ("May 2024" or "5/2024"), a year by itself ("2019"), a surname with a month, or an invoice number (HD-2610-482).
2. The newest visits are at the top; more load as you scroll. "Clear" brings back the whole list. Nothing found? Try fewer words, or "Look among deleted files".

## 2. Open a job
1. Click its row. At the top: the client, the visit date, the property, and the board (part 4).
2. To correct a name, email, phone or address, click "Correct the client" or "Correct the property", then "Save the client" or "Save the property"; it changes on every file of theirs, and in the letter. The service, date and time, and stamp are in the Job box: "Save the job".

## 3. New File by hand, and "been here before"
1. Press "New File". Fill in Client (a last name, and the email: without it nothing can be sent), Property (street, city, state) and Job ("Service", "How", "Date and time"), then press "Open the file". The stamp, invoice wording and price fill themselves in.
2. The client's mailing address is not copied from the property. If they live there, type it in both.
3. If the client or the house is already on record, a yellow box says "This client may already be on file" or "This property may already be on file". Press "Same client: link the two" (or "Same property: link the two"), or "Different: keep separate". "Been here before" then lists their other files.
4. A name alone never brings the yellow box: an email, a phone number or a mailing address must match too. "Not the same: undo the link" undoes a wrong link.

## 4. The board of four steps
1. Under the header: "Letter sent", "Invoice sent", "Paid", "Receipt sent", each green with the date of the first time, or "Not yet". They tick themselves; nobody ticks them by hand.
2. Dashboard rows show the same four as small marks: ✓ done, ○ not yet.
3. On an old job only "Paid" comes from the old records; "Not yet" on the others means the old system kept no record of sending.

## 5. The letter
1. A new file gets its letter by itself. If the Letter box says "This file has no letter yet.", press "Create the letter".
2. Click "Open the Doc". It opens in Google Docs; be signed in to Google as homedirectionsinc@gmail.com.
3. Replace "[Write the letter here.]" with your letter; it saves as you type. Leave the date (the visit's date), names, addresses, "Re:" line and stamp to the system, and correct those on the file. If the box then says "A correction made here has not reached the Doc yet", press "Bring the Doc up to date".
4. Press "Send the letter". The client gets a "Read the letter" link and a PDF; the office gets a copy. A missing email or stamp, or anything left in double braces like {{client_name}}, stops it. Nothing checks that "[Write the letter here.]" is gone.
5. After a change, press "Send the letter again": the same link, a new PDF. The link always shows the Doc as it is now.

## 6. The invoice description and price
1. In "What prints on the invoice", write what was done; it starts from the service's standard wording (Settings, "Invoice texts"). Type the "Price" in dollars.
2. Press "Save the invoice description". A Send button does not save what you typed.
3. Hourly design work: replace "[period]" with the dates and enter the total, or the invoice cannot be sent or marked paid.
4. A paid invoice's wording and price cannot be changed.

## 7. Send the invoice
1. In the Invoice box, click "Look at the PDF" to check it.
2. Press "Send the invoice". It goes to the address under the button. Later, "Send the invoice again" sends it as it then reads.

## 8. "Not imported yet" on an old job
1. In the Letter box it means the old system holds this job's letter or report, not yet brought over: nothing to open or send, and on purpose no new letter can be made there. Read it where you read it today.
2. Letters since June 21, 2022 are to come over at go-live; older ones later.

## 9. The change history
1. At the foot of the file, click "Change history".
2. Newest first: who, when, and each change as old → new: corrections, price, wording, payments, messages, links, delete and restore.
3. The letter's own words are not there. In the Doc, use File, then Version history.
