---
name: Home Directions v4 how-to for Peter
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: A page and a half for Peter, the engineer, in plain words and with the button names exactly as the screens show them. It covers finding a client or job by name, street or month; opening a job; New File by hand and the "been here before" prompt; the board of four steps and "Before v4"; the letter in Google Docs (write it, publish a numbered revision, send the latest published revision, change it later as Revision 2, the revision list and "Edited since Revision N"); old letters and "Not imported yet"; the invoice; and the change history.
sources: ["[repo:/Users/gordonium/Dev/clc-laravel/hdonline-v4, branch feature/v4-build, commit 738bbd8: resources/views (dashboard, files/show, files/_rows, components/board, mail/letter, pdf/invoice); app/Actions (PublishRevision, SendLetter, MarkInvoicePaid); app/Http/Controllers (FileLetterRevisionController, FileLetterSendController, FileInvoicePaymentController); app/Http/Requests/MarkPaidRequest.php; app/Exceptions/CannotSend.php; app/Mailing/MailTrap.php; app/Models (File, LetterRevision); app/Notifications/LoginsChanged.php]", "[repo: same commit, tests: Feature/Letters/LetterRevisionsTest, Feature/Letters/SendLetterTest, Feature/Invoices/PaymentDateTest, Feature/Files/BoardTest, Browser/LetterTest]", "[doc:howto-peter.md as written from commit 8e278ec, 2026-10-03 12:50]", "[doc:build-log-app.md W10 and W11]", "[doc:reviews/app-W10-W11.md]", "[doc:phase0-brief.md, letter revisions, Gordon 2026-10-03]", "[gordon 2026-10-03]"]
status: written 2026-10-03 about 12:50 CEST from commit 8e278ec; updated about 14:10 CEST by a reviewing agent on Opus 5.5 so that it reflects commit 738bbd8 (publishing and sending letter revisions, the revision list, "Edited since Revision N", "Receipt", "Before v4", the mail-log wording, the login notices), read in the code and the tests and not clicked through. Must be checked against the app before go-live. Real mail through Brevo and Calendly are not set up yet, the live system's own Google connection is not made, and the live web address is not decided.
---
# How-to for Peter

Words in quotes are exactly what the screen shows. If something cannot be done, a red notice at the top of the page says why.

**Not set up yet**
- **Mail and Calendly.** No letter or invoice reaches a client yet: on Gordon's Mac a message "was written to this machine's mail log only" (Messages still says "Sent"), and a letter sent there is still made readable by its link. Until Calendly is connected, open every visit with "New File"; after that, move or cancel visits in Calendly. If the Dashboard says "Bookings from Calendly are switched off", tell Gordon.
- **Google and the address.** Letters are real Google Docs on Gordon's Mac only; the live connection and web address come before go-live. Log in with your "Email" and "Password".
- **Logins.** Everybody is emailed when a login is added, changed or switched off. Not expected? Tell the others at once.

## 1. Find a client or a job
1. On the Dashboard, type in "Search by client, address or month (May 2022)" and press "Search": a surname, part of a street, a month ("May 2024" or "5/2024"), a year, a surname with a month, or an invoice number (HD-2610-482).
2. Newest visits are at the top; more load as you scroll. "Clear" brings back the list. Nothing found? Try fewer words, or "Look among deleted files".

## 2. Open a job
1. Click its row. At the top: the client, the visit date, the property, and the board (part 4).
2. To correct a name, email, phone or address: "Correct the client" or "Correct the property", then "Save the client" or "Save the property". It changes on every file of theirs, and in the letter. Service, date and time, and stamp: the Job box, "Save the job".

## 3. New File by hand, and "been here before"
1. Press "New File", fill in Client (a last name and the email: without it nothing can be sent), Property and Job, then "Open the file". Stamp, invoice wording and price fill themselves in. The client's mailing address is not copied from the property.
2. If the client or the house is already on record, a yellow box asks. Press "Same client: link the two" (or "Same property: link the two"), or "Different: keep separate"; "Been here before" then lists their other files. A name alone never brings the box. "Not the same: undo the link" undoes a wrong link.

## 4. The board of four steps
1. Under the header: "Letter sent", "Invoice sent", "Paid", "Receipt sent", each green with its first date, or "Not yet". They tick themselves.
2. On a job from the old system, a sending with no date here reads "Before v4": the old system kept no record of sending. "Paid" comes from its records. "Before v4" does not prove a letter exists: if the Letter box says "This file has no letter yet.", there is none.
3. Dashboard rows show them as marks: ✓ done, – before v4, ○ not yet.

## 5. Write the letter
1. A new file gets its letter by itself; otherwise press "Create the letter".
2. Click "Open the Doc": the working letter in Google Docs (signed in as homedirectionsinc@gmail.com). The client never sees it.
3. Replace "[Write the letter here.]" with your letter. Leave the date, names, addresses, "Re:" line and stamp to the system; correct those on the file, and if the box says "A correction made here has not reached the Doc yet", press "Bring the Doc up to date".

## 6. Publish, then send
1. Press "Publish new revision". The letter as it stands becomes a locked, view-only copy and a PDF, both with "Revision 1, <date>" under the letter's date. Nothing is sent or shared. "PDF of Revision 1" shows exactly what the client will get.
2. Press "Send Revision 1": the client gets an email naming the revision, a "Read the letter" link to that copy, and its PDF; the office gets a copy. Before anything is published the button reads "Send the letter" and publishes Revision 1 first.
3. It refuses, saying why, if "[Write the letter here.]" is still in the Doc, a {{tag}} shows, the stamp is missing, or there is no email.

## 7. Change a letter after it went
1. Edit the working letter. The box then says "Edited since Revision 1. The client still gets Revision 1 until a new revision is published."
2. Press "Publish new revision" (Revision 2), then "Send Revision 2"; the subject ends "(Revision 2)". Send always sends the latest published revision, never unpublished edits. With no change, publishing is refused.
3. Under "Revisions": each one, who published it and when, its PDF, and each sending, or "Not sent from here. Nobody outside the firm can read it." A sent revision stays readable by its link.
4. Edit only the working letter: never unlock the copies in "Published revisions (frozen copies)".

## 8. Old letters, and "Not imported yet"
1. "Not imported yet": the old system holds this job's letter or report, not brought over yet. Nothing to open or send, and on purpose no new letter. Read it where you read it today.
2. Letters since June 21, 2022 come over at go-live as "Revision 1 · from the old system: the version the client already has". "Send Revision 1" works only while the Doc is as it came; once edited, publish first. If the box says the stamp could not be placed, press "Bring the Doc up to date" before sending.

## 9. The invoice
1. In "What prints on the invoice", write what was done and type the "Price", then "Save the invoice description" (a Send button does not save it). Hourly work: replace "[period]" and enter the total, or it cannot be sent. A paid invoice cannot be changed.
2. "Look at the PDF", then "Send the invoice" (later "Send the invoice again"; once paid, "Send the receipt again"). Payments: "Mark paid and send a receipt", check "Paid on", confirm.

## 10. The change history
1. At the foot, "Change history": who, when, old → new.
2. Not there: the letter's words (in the Doc, File, then Version history) and published revisions (under "Revisions").
