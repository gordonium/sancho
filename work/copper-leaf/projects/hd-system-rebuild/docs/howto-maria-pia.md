---
name: Home Directions v4 how-to for Maria Pia
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: A page and a half for Maria Pia, the Treasurer, in plain words and with the button names exactly as the screens show them. It covers finding the job; editing the letter in Google Docs, then publishing a numbered revision and sending the latest published one; the revision list and "Edited since Revision N"; sending the invoice again; marking an invoice paid on the day the payment came, which sends the receipt; taking back a payment recorded by mistake; and what the board's ticks, "Before v4" and "Not imported yet" mean.
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 738bbd8: resources/views (dashboard, files/show, files/_rows, components/board, mail/letter, pdf/invoice); app/Actions (PublishRevision, SendLetter, SendInvoice, MarkInvoicePaid, TakeBackPayment); app/Http/Controllers (FileLetterRevisionController, FileLetterSendController, FileInvoicePaymentController); app/Http/Requests/MarkPaidRequest.php; app/Exceptions/CannotSend.php; app/Mailing/MailTrap.php; app/Models (File, LetterRevision, Invoice); app/Notifications/LoginsChanged.php]", "[repo: same commit, tests: Feature/Letters/LetterRevisionsTest, Feature/Invoices/PaymentDateTest, Feature/Files/BoardTest, Browser/InvoiceTest]", "[doc:howto-maria-pia.md as written from commit 8e278ec, 2026-10-03 12:55]", "[doc:build-log-app.md W10 and W11]", "[doc:reviews/app-W10-W11.md]", "[doc:phase0-brief.md, letter revisions and Q11, Gordon]", "[doc:build-state.md, 10:00 Oct 3: the letters folder shared with homedirectionsinc@gmail.com as Editor]", "[gordon 2026-10-03]"]
status: written 2026-10-03 about 12:55 CEST from commit 8e278ec; updated about 14:10 CEST by a reviewing agent on Opus 5.5 so that it reflects commit 738bbd8 (publishing and sending letter revisions, the revision list, "Edited since Revision N", the "Paid on" day, "Receipt", "Before v4", the mail-log wording, the login notices), read in the code and the tests and not clicked through. Must be checked against the app before go-live. Real mail through Brevo is not set up yet, the live system's own Google connection is not made, and the live web address is not decided.
---
# How-to for Maria Pia

Words in quotes are exactly what the screen shows. If something cannot be done, a red notice at the top of the page says why.

**Not set up yet**
- **Mail (Brevo).** No invoice, receipt or letter reaches a client yet: on Gordon's Mac a message "was written to this machine's mail log only" (Messages still says "Sent"). "Delivered" and "Opened" show in Messages once Brevo is connected.
- **Google and the address.** Letters are real Google Docs on Gordon's Mac only; the live connection and web address come before go-live. Log in with your "Email" and "Password".
- **Logins.** Everybody is emailed when a login is added, changed or switched off ("A change to who can log in"). Not expected? Tell the others at once.

## 1. Find the job
1. On the Dashboard, type in "Search by client, address or month (May 2022)" and press "Search": a surname, part of a street, a month ("May 2024"), or the invoice number on a check (HD-2610-482). Click the job's row; "Clear" brings back the list.
2. Each row has four marks: ✓ done, – before v4, ○ not yet. "✓ Invoice ○ Paid" is an invoice that went from here, unpaid; "– Invoice ○ Paid" is an old invoice the old system has as unpaid.

## 2. Edit the letter, publish it, send it
1. In the Letter box, click "Open the Doc" (Google Docs, signed in as homedirectionsinc@gmail.com; also in Drive, "Shared with me", "Home Directions letters"). This is the working letter: the client never sees it. Edit it as any Google Doc.
2. Correct names and addresses on the file, not in the Doc: "Correct the client", "Save the client". If the box then says "A correction made here has not reached the Doc yet", press "Bring the Doc up to date".
3. Edits do not reach the client by themselves. The box says "Edited since Revision 1. The client still gets Revision 1 until a new revision is published."
4. Press "Publish new revision": the letter as it stands becomes Revision 2, a locked copy and a PDF with "Revision 2, <date>" under the letter's date. Nothing is sent. "PDF of Revision 2" shows exactly what the client will get.
5. Press "Send Revision 2": the client gets an email naming the revision, a link to that copy and its PDF; the subject ends "(Revision 2)". Send always sends the latest published revision; "Send Revision 2 again" sends it again. It refuses if "[Write the letter here.]" is still in the Doc.
6. Under "Revisions": each one, who published it and when, and each sending, or "Not sent from here. Nobody outside the firm can read it." A letter from the old system starts as "Revision 1 · from the old system: the version the client already has"; once edited, publish before sending.
7. Edit only the working letter; never unlock the copies in "Published revisions (frozen copies)". Earlier versions: in the Doc, File, then Version history.

## 3. Send the invoice again
1. Look at Messages first: what went, when and to whom, with "The PDF as sent". "Not confirmed" means it may have gone: ask Gordon before sending again.
2. Press "Send the invoice again" ("Send the invoice" means it never went). It goes as it reads now, to the address under the button; an old one ("From the earlier system") goes as recorded, without a number. No email? "Correct the client", "Save the client", then send.
3. Once paid, the button is "Send the receipt again": the receipt, not the invoice.

## 4. Mark paid and send the receipt
1. In the Invoice box, click "Mark paid and send a receipt". The question names the client and the amount.
2. "Paid on" shows today. If the payment came earlier, change it to that day; a day still to come is refused. The button does not repeat the day, so check it before you press "Yes, ... has paid ...".
3. The payment is recorded under your name with that day, and the receipt goes to the client at once, reading "Paid <day>. Thank you." "Paid" and "Receipt sent" tick.
4. Nothing seemed to happen? Open "Mark paid and send a receipt" again: a refused day is explained in red inside it.
5. No email on file: the payment is still recorded, and a red notice says "The receipt was not sent." Add the email, then "Send the receipt again".
6. An amber line saying the price or wording changed since the invoice went: if the client should see it, press "Send the invoice again" first.

## 5. Take a payment back
1. Wrong job, wrong day or a mistake: click "This was a mistake", then "Take the payment back". The invoice is unpaid again; "Paid" and "Receipt sent" go back to "Not yet". Nothing is sent to the client.
2. A receipt that already went stays in Messages; telling the client is your call. For the right day, mark it paid again (a new receipt goes). "Change history" keeps who did what.

## 6. What the board means
1. Under the client's name: "Letter sent", "Invoice sent", "Paid", "Receipt sent". Green with a date: done, on that first date. "Not yet": not done. Never ticked by hand.
2. On an old job, a sending with no date here reads "Before v4": the old system kept no record, so it may have gone then; that is not proof. "Paid" comes from the old records. A letter brought over shows "Letter sent" with the old system's date.
3. "Not imported yet" in the Letter box: the old system holds the letter, not brought over yet; nothing to open or send here. Brought over, it becomes Revision 1.
