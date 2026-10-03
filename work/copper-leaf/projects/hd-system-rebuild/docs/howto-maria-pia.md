---
name: Home Directions v4 how-to for Maria Pia
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: One page for Maria Pia, the Treasurer, in plain words and with the button names exactly as the screens show them. It covers finding the job; opening and editing the letter in Google Docs; sending the invoice again; marking an invoice paid, which sends the receipt; taking back a payment recorded by mistake; and what the board's ticks mean.
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 8e278ec: resources/views (dashboard, files/show, files/_rows, components/board, auth/login); app/Search/FileSearch.php; app/Actions (SendLetter, SendInvoice, MarkInvoicePaid, TakeBackPayment); app/Http/Controllers/FileInvoicePaymentController.php; app/Exceptions/CannotSend.php; app/Models/File.php (the board); app/Models/Invoice.php; app/Mailing/MailTrap.php]", "[repo: same commit, tests/Browser: LoginTest, DashboardTest, LetterTest, InvoiceTest, ChangedScreensTest]", "[run: the app's local .env read for MAIL_MAILER and HD_MAIL_TRAP only, 2026-10-03 12:45: the log mailer, no trap address]", "[doc:plan-v2.md section 5]", "[doc:phase0-brief.md, Gordon's entries of 2026-10-03, and Q11]", "[doc:build-log-app.md W2, W5, W9]", "[doc:build-state.md, 10:00 and 12:05 Oct 3: the letters folder shared with homedirectionsinc@gmail.com as Editor]", "[doc:reviews/app-W3-walkthrough.md finding 9]", "[doc:reviews/app-W5-W8.md finding 12]", "[gordon 2026-10-03]"]
status: written 2026-10-03 about 12:55 CEST by a documents-only agent on Opus 5.5 from the screens of commit 8e278ec, read in the code and the browser tests and not clicked through. Must be checked against the app before go-live, because the screens are still changing (three later commits about Calendly bookings and the letter trash were not read). Real mail through Brevo is not set up yet, the live system's own Google connection is not made, and the live web address is not decided.
---
# How-to for Maria Pia

Words in quotes are exactly what the screen shows. If something cannot be done, a red notice at the top of the page says why.

**Not set up yet**
- **Mail (Brevo).** No invoice, receipt or letter reaches a client yet. On Gordon's Mac a Send button still says "... sent to" the client, and Messages says "Sent", but the message only goes into a log file. "Delivered" and "Opened" show in Messages once Brevo is connected.
- **Google and the address.** Letters are real Google Docs on Gordon's Mac only. The live system's Google connection and web address come before go-live. Log in with your "Email" and "Password", then "Log in".

## 1. Find the job
1. On the Dashboard, type in "Search by client, address or month (May 2022)" and press "Search": a surname, part of a street, a month ("May 2024"), or the invoice number on a check (HD-2610-482).
2. Click the job's row. "Clear" brings back the whole list.
3. A row showing "✓ Invoice" and "○ Paid" is an invoice that went and is not paid yet.

## 2. Open and edit the letter in Google Docs
1. In the Letter box, click "Open the Doc". It opens in Google Docs.
2. Be signed in to Google as homedirectionsinc@gmail.com; if Google asks you to request access, switch to it. The letters are also in Google Drive, under "Shared with me", in "Home Directions letters".
3. Edit as in any Google Doc; it saves as you type.
4. Correct names and addresses on the file, not in the Doc: "Correct the client", then "Save the client" (or the same for the property). If the Letter box then says "A correction made here has not reached the Doc yet", press "Bring the Doc up to date".
5. Once a letter has been sent, the client's link shows your edits at once. To send a new PDF too, press "Send the letter again".
6. Earlier versions: in the Doc, File, then Version history.

## 3. Send the invoice again
1. Look at Messages first: what went, when and to whom, with "The PDF as sent". If one says "Not confirmed", it may have gone: ask Gordon before sending again.
2. In the Invoice box press "Send the invoice again" ("Send the invoice" means it has never gone). It goes as it reads now, to the address under the button. On an old job ("From the earlier system") it goes as recorded, without a number.
3. No email on file? Add it with "Correct the client" and "Save the client", then send.
4. Once paid, the button is "Send the paid copy again": the receipt, not the invoice.

## 4. Mark paid and send the receipt
1. In the Invoice box, click "Mark paid and send a paid copy".
2. The question names the client and the amount. If both are right, press "Yes, ... has paid ...".
3. The payment is recorded under your name with today's date (there is no field for the day the check came), and the paid copy, which is the receipt, goes to the client at once. "Paid" and "Receipt sent" tick.
4. No email on file: the payment is still recorded, and a red notice says no copy went. Add the email, then press "Send the paid copy again".
5. If an amber line says the price or wording changed since the invoice went, and the client should see it, press "Send the invoice again" first.

## 5. Take a payment back
1. For a payment recorded on the wrong job or by mistake: click "This was a mistake", then press "Take the payment back".
2. The invoice is unpaid again; "Paid" and "Receipt sent" go back to "Not yet". Nothing is sent to the client. A paid copy that already went stays in Messages; telling the client is your call.
3. "Change history", at the foot, keeps who recorded the payment and who took it back.

## 6. What the board's ticks mean
1. Under the client's name: "Letter sent", "Invoice sent", "Paid", "Receipt sent". Green with a date: done. "Not yet": not done.
2. They tick themselves, never by hand, and keep the date of the first time.
3. On the Dashboard they are small marks: ✓ done, ○ not yet. Point at one to see its date.
4. Old jobs: only "Paid" comes from the old records; "Not yet" on the others means the old system kept no record of sending, not that nothing went. A letter brought over shows "Letter sent" with the old system's date.
