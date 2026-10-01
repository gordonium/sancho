---
name: Home Directions v4 runbook, dress rehearsal
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The dress rehearsal that stands in for a trial period before the hard cutover: every path through v4 run end to end on staging by Gordon and the agent, as a script with the expected result of each step, with test bookings and messages that go only to Gordon; the set-up (the mail trap proven first), eighteen paths (the last three: a job from the old system, the three safety nets seen working, the restore test), the clean-up that removes the real history, and the pass rule
sources: ["[doc:plan-v2.md sections 2, 4, 5, 6, 7, 10]", "[doc:requirements.md]", "[doc:phase0-brief.md, Plan questions 4 onward]", "[doc:laravel-kit-spec.md sections 4, 7, 8, 12, 13]", "[doc:build-handoff.md]", "[doc:runbook-accounts.md]", "[doc:runbook-backups.md]", "[doc:runbook-cutover.md]", "[doc:reviews/paperwork-W1.md]", "[gordon 2026-10-01]", "[gordon 2026-10-02]", "[web:rfc-editor.org/rfc/rfc2606.txt 2026-10-02]", "[web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]"]
status: written 2026-10-02 overnight by the paperwork track (stage W1), before the screens existed; reviewed the same night (reviews/paperwork-W1.md) and fixed by a third agent, see "W1 fixes" in build-log-paperwork.md; button and field names are the plan's words and are corrected against the real screens at stage W2
---
# Runbook: the dress rehearsal

**The short version.** Nobody but you and the agent uses v4 before the cut. So every path is run once, end to end, on staging, and each step has a result it must show. Test bookings. Messages that go only to you. [gordon 2026-10-02] [doc:plan-v2.md section 6 step 5, and section 7 step G]

**The pass rule.** Every line passes, or the cutover does not happen. A line that fails is fixed, and its whole path is run again. [doc:plan-v2.md section 7, step G: "every path end to end"]

**Who does what.** "G" is you. "A" is the agent. You do everything with a login, a click in Calendly or Google, or a judgement about how something looks. The agent prepares the test data, reads staging's log after each step, and writes down each result. [doc:laravel-kit-spec.md section 13]

Unconfirmed: the button and field names below. They are the plan's words. The screens did not exist when this was written. The script is corrected against the real screens before you run it.

---

## Set-up: all true before step 1

| # | Who | Must be true | Source |
|---|---|---|---|
| S1 | A | Staging runs the version under test. The commit staging reports equals the commit pushed, nothing is pending in the database's migrations, and the health address answers. | [doc:laravel-kit-spec.md section 7, laravel-edit step 7] |
| S2 | A | Staging's log is proven alive, then read. An empty log proves nothing until then. | [doc:laravel-kit-spec.md section 4, log probe] |
| S3 | G | Staging's Settings, Connections panel: Calendly, Brevo, Google and both backup stores show as working. Press each test button once. | [doc:plan-v2.md section 5, Settings] |
| S4 | G | Staging uses the test Calendly account and the test Google account. Neither owns anything real when the rehearsal starts. From Path 16 until the clean-up, the test Google account holds real letters; see the clean-up. | [doc:laravel-kit-spec.md 8.2] |
| S5 | G and A | The mail trap is proven, with an address that is not yours. Do this once S6 and S7 are true. Make a file by hand for a client named `CLAUDE TEMP TEST Trap`, with the email `trap-check@rehearsal.invalid`. Send its invoice. It must arrive in your own inbox and nowhere else. The agent reads staging's log and confirms the typed address was replaced and nothing was sent to it. If either fails, stop: no path is run until the trap works. | [doc:plan-v2.md section 10: "Staging mail goes to a trap"] [doc:laravel-kit-spec.md 8.2] [doc:runbook-accounts.md 4.4] |
| S6 | G | Three logins exist on staging: one as Peter (owner), one as Maria Pia (treasurer), one as you (admin). | [doc:plan-v2.md section 4, users] |
| S7 | G | Staging's Settings is filled in: the three invoice texts, the template link, the two stamp images, the from address, the Calendly type map. | [doc:plan-v2.md section 5, Settings] |
| S8 | G | If the agent is to look at staging's screens through the browser, you have said so, and it is recorded with the date. Without that, the agent reads the log and you read the screens aloud. | [doc:laravel-kit-spec.md section 13, and section 4, browser tests] |

Why S5 uses a strange address. Every other address in this rehearsal is one of your own, so a message reaching you would prove nothing about the trap. An address ending in `.invalid` can never receive mail: that ending is reserved for names that are sure to be invalid. [web:rfc-editor.org/rfc/rfc2606.txt 2026-10-02] If the trap were broken, the message would go nowhere, not to a stranger.

Unconfirmed: what the copy to office@homedirections.net does on staging. In production every message is copied to that mailbox. [doc:plan-v2.md section 5, "Mail"] In the rehearsal nothing may go to anyone but you. Whether staging switches the copy off or sends it to you too is settled when the mail connection is built. Line S5 is where you find out.

**The test people and places.** Invented, every one. Every record made by hand carries the words `CLAUDE TEMP TEST` in the client's name. [doc:laravel-kit-spec.md section 4, hand-test rules] No real client's name, address or email is typed anywhere in this rehearsal. [doc:build-handoff.md section 3]

| Label | Client name | Property | Why |
|---|---|---|---|
| T1 | CLAUDE TEMP TEST Alder | 12 Rehearsal Lane, Ridgefield, CT | Connecticut stamp |
| T2 | CLAUDE TEMP TEST Birch | 34 Rehearsal Lane, Katonah, NY | New York stamp |
| T3 | CLAUDE TEMP TEST Cedar | 56 Rehearsal Lane, Lenox, MA | no stamp |
| T4 | CLAUDE TEMP TEST Dogwood | 78 Rehearsal Lane, Ridgefield, CT | the truly new client of line 3.5 |

Every email address used is one of your own, except the trap address of line S5. Clients are matched on email first, so the four test people need four different addresses. [doc:plan-v2.md section 4, Rules] Use your own mailbox with a tag after a plus sign: (you)+t1@(your domain) for T1, then +t2, +t3 and +t4.
- Unconfirmed: check on the vendor's page when you do this step: that your mail service delivers a plus-tagged address to your normal inbox. If it does not, use four different addresses of your own.

---

## Path 1. Logging in

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 1.1 | G | Log in as yourself. | The Dashboard: a New File button, a search box, the most recent files newest first, a way to Settings. | [doc:plan-v2.md section 5, Screens 1] [doc:requirements.md R6.1] |
| 1.2 | G | Log out. Log in with Peter's login. | The same Dashboard. | [doc:plan-v2.md section 4] |
| 1.3 | G | Log out. Log in with Maria Pia's login. | She gets in, and can open a file. | [doc:plan-v2.md section 2, Maria Pia Seirup] |
| 1.4 | G | Give a wrong password several times in a row. | No way in. The login slows down or refuses for a while. | [doc:laravel-kit-spec.md section 4, security: login rate limited] |

Unconfirmed: what each of the three kinds of login may and may not do. The documents say Maria Pia records payments and you are the admin, and no more. [doc:plan-v2.md sections 2 and 4]

## Path 2. A new file by hand

Hourly design work is entered by hand; it does not come through Calendly. [doc:plan-v2.md section 5]

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 2.1 | G | As Peter: New File. Client T1, property T1, service hourly design. Save. | A file opens with its client and its property, the service set to hourly, and a status. | [doc:plan-v2.md sections 4 and 5] [doc:requirements.md R1.3] |
| 2.2 | G | Look at the invoice panel. | An invoice already exists. Its description is the hourly text from Settings. Its number reads like `HD-2610-482`: year, month, three digits. | [doc:plan-v2.md section 5, "Invoices", and section 2] [doc:requirements.md R4.1] |
| 2.3 | G | Look at the letter panel. Open the Doc. | A Google Doc made from the template, with the name, address and date filled in. It is named `Home-Directions-letter_(date)_12-Rehearsal-Lane-Ridgefield_(client name)`. | [doc:plan-v2.md section 5, "Letters"] |
| 2.4 | G | Look at the stamp on the file. | Connecticut, because the property is in Connecticut. | [doc:plan-v2.md section 2, Stamp] |
| 2.5 | G | Go back to the Dashboard. | The new file is at the top, showing its client, address, status and the next thing to do. | [doc:plan-v2.md section 5, Screens 1] |
| 2.6 | A | Read staging's log. | No error. One file, one invoice, one Doc recorded. | [doc:laravel-kit-spec.md section 4] |

## Path 3. The duplicate prompts

Duplicates are suggested, never merged silently. [doc:plan-v2.md section 4]

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 3.1 | G | New File. A client with a different spelling of T1's name and the **same email** as T1. | The system says this looks like an existing client and offers one click to link, or to keep apart. | [doc:plan-v2.md section 4: clients match on email first] |
| 3.2 | G | Choose link. | The file is on the existing client. No second client was made. | [doc:plan-v2.md section 4] |
| 3.3 | G | New File. The same client. The property typed as "12 Rehearsal Ln, Ridgefield CT". | The system says this looks like an existing property and offers link or keep apart. | [doc:plan-v2.md section 4: properties match on the place, then on the normalised address] |
| 3.4 | G | Choose link. Open the file. | "Been here before" shows the earlier file, with a link to it. | [doc:plan-v2.md section 5, Screens 2] [doc:requirements.md R2.1] |
| 3.5 | G | New File. A truly new client, T4, with T4's own email, and choose "keep apart" on any prompt. | A second, separate client exists. | [doc:plan-v2.md section 4] |

## Path 4. A booking from Calendly

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 4.1 | G | In the test Calendly account's booking page, book a Professional Opinion as T2, with the New York address, at a date next week. | Within moments a file appears on the Dashboard: client T2, the New York property, service opinion, price $875. | [doc:plan-v2.md section 5, "Calendly"] [doc:phase0-brief.md Q4] |
| 4.2 | G | Look at the stamp. | New York. | [doc:plan-v2.md section 2, Stamp] |
| 4.3 | G | Book a Structural Design as T3, with the Massachusetts address. | A file: service design, price $1,250, stamp none. | [doc:plan-v2.md section 2] [doc:phase0-brief.md Q4 and Q9] |
| 4.4 | G | Book again with T2's email and a new address. | A new file. The system suggests the existing client; it does not merge by itself. | [doc:plan-v2.md section 5, "Calendly", and section 4] |
| 4.5 | G | Wait sixteen minutes. Look at the Dashboard. | Still one file for each booking. The 15-minute check found the same bookings and did nothing twice. | [doc:plan-v2.md section 5: "Each booking is acted on once"] |
| 4.6 | A | Read staging's log. | Each booking recorded once. No error. | [doc:plan-v2.md section 7, step F] |

Unconfirmed: how a booking is marked as a virtual visit or a site visit. The file has both. [doc:plan-v2.md section 4, mode] The documents do not say which Calendly answer decides it. A virtual visit still gets the stamp of the property's state. [gordon 2026-10-01] [doc:phase0-brief.md Q9]

## Path 5. A reschedule

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 5.1 | G | In Calendly, reschedule T2's first booking to another day. | The same file, with the new date. No second file. | [doc:plan-v2.md section 5, "Calendly"] [doc:requirements.md R1.4] |
| 5.2 | G | Open the file's change history. | The date change is listed: old date, new date, when. | [doc:plan-v2.md section 5, Screens 2] |

## Path 6. A cancellation, twice

The file is marked cancelled and kept. An untouched Doc goes to Drive's trash. An edited one stays. [gordon 2026-10-01] [doc:plan-v2.md section 2]

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 6.1 | G | Open T3's Doc and type one line in it. Leave T2's second booking's Doc untouched. | Nothing yet. | |
| 6.2 | G | In Calendly, cancel T2's second booking (the untouched one). | Its file is marked cancelled. It leaves the working list and can still be found by search. | [doc:phase0-brief.md Q5] |
| 6.3 | G | Look in the test Google account's Drive. | That Doc is in the trash. | [doc:plan-v2.md section 2] |
| 6.4 | G | In Calendly, cancel T3's booking (the edited one). | Its file is marked cancelled and kept. | [doc:plan-v2.md section 2] |
| 6.5 | G | Look in Drive. | That Doc is still there, with your line in it. | [doc:plan-v2.md section 2] |
| 6.6 | G | Check your mail. | The system sent nothing about either cancellation. | Sancho's reading: the plan lists three kinds of message (invoice, paid copy, letter) and none for a cancellation. [doc:plan-v2.md section 4, sends] |

## Path 7. The 15-minute check by itself

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 7.1 | A and G | Arrange for one booking's instant notice not to arrive, then book as T1. | No file at first. | [doc:plan-v2.md section 5, "Calendly"] |
| 7.2 | G | Wait sixteen minutes. | The file is there, complete, once. | [doc:plan-v2.md section 5] [gordon 2026-10-01: "every 15 minutes would be fine"] |

Unconfirmed: how the instant notice is held back for step 7.1. If the test Calendly account is on a free plan it sends no instant notices at all, and then every booking in paths 4 to 6 arrives this way and the instant path is not rehearsed. `runbook-accounts.md` step 8.

## Path 8. The letter, and fixing a name once

A corrected name changes in the system, in the Doc and in its name. [doc:plan-v2.md section 7, step D]

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 8.1 | G | Open T1's Doc. In the body, type a sentence that uses the client's last name. | Saved by Google. | [doc:plan-v2.md section 10] |
| 8.2 | G | On T1's file, correct the client's last name, in place. | The file shows the new name. | [doc:requirements.md R2.2] |
| 8.3 | G | Open the Doc again. | The address block and the greeting show the new name. The Doc's own name has the new name. | [doc:plan-v2.md section 5, "Letters"] [doc:requirements.md R2.3] |
| 8.4 | G | Read the sentence you typed in 8.1. | Unchanged. Only the tagged places were replaced. | [doc:plan-v2.md section 10] |
| 8.5 | G | On the file, correct the street name of the property. | The file, the Doc's address block and the Doc's name all show the new street. | [doc:requirements.md R2.3] |
| 8.6 | G | Open another file for the same client. | The new name is there too. Fixed once, right everywhere. | [doc:plan-v2.md section 1] |
| 8.7 | G | On the file, override the stamp: set it to none. | The file shows none. | [doc:plan-v2.md section 2: Peter can override] |
| 8.8 | G | Look at the Doc as a letter. | Letterhead, date, address block, greeting, "Sincerely,", signature, "Peter Seirup, P.E.", both licence lines. It looks like it came from an engineer. | [doc:phase0-brief.md, "The letter template"] [doc:requirements.md R3.6] |

## Path 9. The invoice: send, pay, resend

One whole job, with the client's messages going to your own address. [doc:plan-v2.md section 7, step E]

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 9.1 | G | On T1's file, edit the invoice description and change the price. | Both save. The invoice preview shows the new wording and the new total. | [doc:plan-v2.md section 5, Screens 2] [doc:requirements.md R2.5] |
| 9.2 | G | Preview the invoice. | A PDF. The number, the description, the total. | [doc:plan-v2.md section 5, "Invoices"] |
| 9.3 | G | Send the invoice. | An email reaches your address, from office@homedirections.net, with the invoice as a PDF. | [doc:plan-v2.md section 5, "Mail"] |
| 9.4 | G | Look at the file's message log. | One line: invoice, to whom, when sent. | [doc:plan-v2.md section 4, sends] [doc:requirements.md R5.2] |
| 9.5 | G | Open the email. Wait a few minutes. Look at the log again. | The line now shows delivered, and opened. | [doc:plan-v2.md section 5, "Mail"] |
| 9.6 | G | Log in as Maria Pia. Open the file. Mark the invoice paid. | The invoice shows paid, by her, with the time. | [doc:plan-v2.md section 5, "Invoices", and section 2] |
| 9.7 | G | Check your mail. | A paid copy of the invoice has arrived. | [doc:requirements.md R4.4] |
| 9.8 | G | Press resend. | The invoice arrives again. The log has a new line. | [doc:plan-v2.md section 5, "Invoices"] |
| 9.9 | G | Open the PDF you received in 9.3 beside the invoice now. | The first PDF still shows the wording and total it was sent with. | [doc:plan-v2.md section 4, invoices: "as it stood when issued", "the PDF as sent"] |
| 9.10 | A | Read staging's log. | Three messages for this file: the invoice, the paid copy, the resend. All to your address. None to any other. | [doc:laravel-kit-spec.md 8.2] |

## Path 10. Sending the letter

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 10.1 | G | On T1's file, send the letter. | An email reaches your address with a link to the letter and a PDF of it. | [doc:plan-v2.md section 5, "Sending a letter"] [doc:phase0-brief.md Q7] |
| 10.2 | G | Open the link in a browser that is not signed in to Google. | The letter, read-only. It looks like a document, not an editor. | [doc:requirements.md R3.5 and R3.6] |
| 10.3 | G | Open the PDF. | The letter as it stood when sent. | [doc:plan-v2.md section 5] |
| 10.4 | G | Look at the message log. | A line for the letter, and the system holds the PDF that was sent. | [doc:plan-v2.md section 4, sends] |
| 10.5 | G | In the Doc, add a sentence. Open the link again. | The link shows the new sentence. | [doc:requirements.md R3.5] |
| 10.6 | G | Open the PDF kept on the file. | It does not have the new sentence. It is the record of what was sent. | [doc:plan-v2.md section 5, "Sending a letter"] |

## Path 11. Search and the list

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 11.1 | G | Search for "Alder". | T1's files. | [doc:plan-v2.md section 5, Screens 1] |
| 11.2 | G | Search for "Rehearsal Lane". | All the test properties' files. | [doc:requirements.md R6.2] |
| 11.3 | G | Search by the month the test bookings fall in. They were booked for next week, which may be next month. | The files dated in that month, the cancelled ones included. | [doc:requirements.md R6.2] [doc:phase0-brief.md Q5: cancelled files stay findable] |
| 11.4 | G | On the Dashboard, scroll down. | The list keeps loading older files as you go. | [doc:plan-v2.md section 5, Screens 1] [doc:requirements.md R6.1] |

Line 11.4 needs more files than one screen holds. Run it after the import rehearsal has filled staging. [doc:plan-v2.md section 7, step H]

## Path 12. The change history

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 12.1 | G | Open T1's file. Look at the foot of it. | The change history is there, folded shut. | [gordon 2026-10-02] [doc:plan-v2.md section 5, Screens 2] |
| 12.2 | G | Open it. | Every change from paths 8 and 9: the name, the street, the stamp, the price, the description, invoice sent, marked paid, letter sent. Each with who, when, the old value and the new one. | [doc:plan-v2.md section 5, Screens 2] |
| 12.3 | G | Look for the sentence you typed into the Doc. | Not there. Edits to the letter's text are Google's to remember, not the system's. | [doc:plan-v2.md section 5, Screens 2] |

## Path 13. Delete and restore

Deleting hides a file and keeps it recoverable. Nothing is destroyed. [gordon 2026-10-01] [doc:plan-v2.md section 2]

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 13.1 | G | Delete the file from step 3.5, which was entered by hand. | The system asks twice before it does it. | [doc:requirements.md R2.6] |
| 13.2 | G | Look at the Dashboard and search for it. | Gone from the working list. | [doc:plan-v2.md section 2] |
| 13.3 | G | Restore it. | It is back, whole. The change history shows the delete and the restore. | [doc:plan-v2.md section 5, Screens 2] |
| 13.4 | G | Book a new Calendly appointment as T2 for next week. When its file appears, delete that file. | The dialog offers "also cancel it in Calendly", already ticked. | [doc:phase0-brief.md Q6] |
| 13.5 | G | Confirm, leaving it ticked. | The file is hidden. In Calendly the booking is cancelled, and Calendly sends its own notice. The system sends nothing itself. | [doc:phase0-brief.md Q6] |
| 13.6 | G | Delete T1's file from path 2, which was entered by hand. | No Calendly offer. Only our record is hidden. | [doc:phase0-brief.md Q6] |
| 13.7 | G | Restore T1's file. | Back, with its invoice, its letter and its log. | [doc:plan-v2.md section 2] |

Unconfirmed: where a hidden file is found in order to restore it. The plan says recoverable and not on which screen.

## Path 14. Settings and the connections

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 14.1 | G | In Settings, change one word in the Professional Opinion invoice text. | Saved. | [doc:requirements.md R4.2] |
| 14.2 | G | Open T2's existing file. | Its invoice description is unchanged. | [doc:requirements.md R4.2: a change applies to new invoices only] |
| 14.3 | G | Make a new Professional Opinion file by hand. | Its invoice description has the new word. | [doc:requirements.md R4.2] |
| 14.4 | G | Look at the letter template setting. | A link to the template Doc. No editor for the letter's look. | [doc:plan-v2.md section 5, Screens 3] |
| 14.5 | G | Look at the Connections panel. Press each test button. | Calendly, Brevo, Google and the two backup stores: each working, each with the time it last succeeded. | [doc:plan-v2.md section 5, Screens 3] |
| 14.6 | G | Look for any place in Settings to type a key or a password for a service. | There is none. Keys live in Forge. | [doc:plan-v2.md section 5, "Keys and passwords"] |

## Path 15. The backup

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 15.1 | G and A | Let the nightly archive run on staging, or start one. | A new encrypted archive in staging's bucket and in the test Google account's backup folder. | [doc:plan-v2.md section 9] |

The restore test is Path 18, at the very end. It empties staging, so it cannot come before Path 16.

## Path 16. A job that came from the old system

Run after the import and the letter conversion have been rehearsed on staging. [doc:plan-v2.md section 7, step H] From here on, staging holds real client records with real email addresses. So the trap is proven again first, and nothing real is opened until it is.

What came across: the whole history as job records, and every letter since the last inspection on 2022-06-21 as a Google Doc. [gordon 2026-10-02: "Good, let's do all the letters"] [doc:plan-v2.md section 6 steps 1 and 2]

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 16.1 | G and A | Before any real record is opened: run line S5 again. Send the trap file's invoice once more. | It arrives in your inbox and nowhere else. The agent confirms from the log that the `.invalid` address was replaced. | [doc:plan-v2.md section 10] [doc:laravel-kit-spec.md 8.2] |
| 16.2 | A | Read staging's record of messages since the import began. | No message was made by the import or by the conversion. | [doc:plan-v2.md section 10, "A message goes to a real client"] |
| 16.3 | G | Look at the sent list of the mail account staging uses. | Nothing was sent during the import or the conversion. | [doc:plan-v2.md section 10] |
| 16.4 | A | Count the converted Docs that are shared by link. | Zero. Only sending a letter opens a Doc to "anyone with the link". | [doc:plan-v2.md section 5, "Sending a letter"] |
| 16.5 | G | Search for a consultation from before 2022-06-21. Open it. | The job record: who, when, where. It is marked as from WordPress and not verified. It has no Google Doc. | [doc:plan-v2.md section 4, sources, and section 6 steps 1 and 2] |
| 16.6 | G | Search for a job from the second half of 2022. Open it. | The same record, and a letter panel with a Google Doc. | [doc:plan-v2.md section 6 step 2] |
| 16.7 | G | Open that Doc. Type a word. | It opens in the new template and can be edited, like a new letter. | [gordon 2026-10-02: "Good, let's do all the letters"] [doc:plan-v2.md section 6 step 2] |
| 16.8 | G | Search for a job from 2023 or 2024. Open it and its Doc. | A Google Doc that opens and can be edited. | [doc:plan-v2.md section 6 step 2] |
| 16.9 | G | Search for a job from the last year. Open it and its Doc. | A Google Doc that opens and can be edited. | [doc:plan-v2.md section 6 step 2] |
| 16.10 | G | Look at that job's invoice. | Its text, its total and its paid state came across. | [doc:plan-v2.md section 6 step 2] |
| 16.11 | G | Open a property that has had more than one job. | "Been here before" lists the earlier jobs. | [doc:requirements.md R2.1] |
| 16.12 | A | Report the import's counts. | Counts and field names only. Never a name, an address, an email or a letter's text. | [doc:build-handoff.md section 3, "Counts and field names only"] |

Why lines 16.6 to 16.9 look at four different years. The first plan moved only the last twelve months of letters. The decision since is every letter back to 2022-06-21. [doc:plan-v2.md section 6 step 2] A check of one recent job would pass a system that moved only twelve months.

The old link of the job in line 16.5 is not checked here. No redirect exists during the rehearsal. It is checked on the day: `runbook-cutover.md` Step 6.

- Unconfirmed: how the agent reads the two counts of lines 16.2 and 16.4. The same two counts are needed on production at the cutover, where you read them. They are owed by the app track. `runbook-cutover.md` Steps 3 and 4.
- Unconfirmed: check on the vendor's page when you do this step: where the mail service lists what an account has sent (line 16.3).

This path shows real client history on staging. Production data reaches staging only when you copy it, for a named job, and it is deleted afterwards. [doc:laravel-kit-spec.md 8.2] The deleting is lines C4 to C7 of the clean-up.

## Path 17. The three safety nets, seen working

The way back at the cutover leans on three things nobody has seen work: going back a release, a failed backup stopping a deploy, and an alert reaching you. For the alerts, silence is the pass signal, so a broken alert looks the same as a good night. [doc:laravel-kit-spec.md section 4: "Prove the log works before trusting its silence"] [doc:CLAUDE.md must-never 10] Each is done once here, on staging. This path does not need the imported history, so it can be run before Path 16. It takes two nights.

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 17.1 | G and A | Going back a release. The agent pushes a small harmless change to staging, so there are two releases. Then you, in Forge, go back to the release before. | Staging reports the earlier commit again. The database is untouched. The agent writes down the exact steps you took. | [doc:laravel-kit-spec.md section 4, Rollback, and section 15] [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02: Forge keeps the last four releases] |
| 17.2 | G and A | A failed backup stops a deploy. In Forge, on staging's Environment, change one line of the backup store's settings so the store cannot be reached. Keep the old text. Then press Deploy on staging. | The deploy stops at the backup step. The old release stays live. Forge emails you. The agent writes down what the backup command reported. | [doc:laravel-kit-spec.md section 7, laravel-ship, last paragraph, and section 15] [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] |
| 17.3 | G | The morning alert. Leave that line broken overnight, so the nightly archive fails. | The next morning the alert reaches you, by the channel that was chosen. No alert means this line fails. | [doc:plan-v2.md section 9: "an alert to Gordon if not"] [doc:runbook-backups.md section 4] |
| 17.4 | G and A | Put the line back as it was. Press Deploy on staging. Let one nightly archive run. | The deploy passes. The archive arrives in both places. No alert the next morning. | [doc:plan-v2.md section 9] |
| 17.5 | G and A | The one-day Calendly alert. Make staging fail Calendly's notices for as long as the alert needs. | The alert reaches you. | [doc:plan-v2.md section 10, "Calendly stops notifying"] |

- Unconfirmed: the exact steps to go back a release in Forge. Line 17.1 is where they are found and written down. That closes the same open line in `runbook-backups.md` and in `runbook-cutover.md` Part 4. [doc:laravel-kit-spec.md section 15]
- Unconfirmed: whether staging's deploy takes the backup on every deploy, or only on one that changes the database. [doc:plan-v2.md section 9] If only then, the deploy of line 17.2 must carry a small database change. Sancho says from the deploy script.
- Unconfirmed: which line to break in 17.2. Sancho names it. Editing a server's environment is asked first, and the old text is kept. [doc:laravel-kit-spec.md section 6 item 5]
- Unconfirmed: what does the morning check and how its alert reaches you. `runbook-backups.md` section 4. Line 17.3 cannot pass until that is settled.
- Unconfirmed: how the Calendly failure of line 17.5 is brought about on staging, and whether it can be done without waiting a whole day. Sancho says once the alert is built.

## Path 18. The restore test, last

This is the restore "once before go-live". [doc:plan-v2.md section 9] It restores staging's own archive, taken while staging holds the rehearsed import, because that archive is the size of the real thing. Why not production's: `runbook-backups.md` section 6.1. It comes last because it empties staging.

| # | Who | Do | Expect | Source |
|---|---|---|---|---|
| 18.1 | G | Say "start the restore test". | It is yours to start. | [doc:laravel-kit-spec.md 8.2 and section 13] |
| 18.2 | A | Write down staging's counts: clients, properties, files, invoices, messages sent, stored PDFs. | Counts only. | [doc:plan-v2.md section 9: "counts compared"] |
| 18.3 | G and A | Take an archive of staging now. | It arrives in staging's bucket and in the test Google account's backup folder. | [doc:plan-v2.md section 9] |
| 18.4 | G | In Forge, stop staging's queue worker and scheduler. | Both stopped, so restored data can send nothing and book nothing. | [doc:laravel-kit-spec.md 8.2] |
| 18.5 | G and A | Empty staging. Then load the archive back, from the written procedure. | Staging holds what the archive held. | [doc:hosting-options.md Decision: the first restore test produces the procedure] |
| 18.6 | A | Compare the counts with line 18.2. | Equal, every one. | [doc:plan-v2.md section 9] |
| 18.7 | A | Write the result and the procedure down, with the date. | Written. | [doc:hosting-options.md Decision] |

What state this leaves staging in: holding the restored real history, with its worker and scheduler stopped. Go straight on to the clean-up. The worker and the scheduler are started again at its end.

Unconfirmed: the restore steps themselves, and how staging is emptied in line 18.5. `runbook-backups.md` section 6.

---

## Clean-up

Two things are removed: the invented test records, and the real history that Path 16 put on staging. Deleting the real history is yours to do, or to approve by name. [doc:laravel-kit-spec.md 8.2 and section 13]

| # | Who | Do | Check | Source |
|---|---|---|---|---|
| C1 | G | In the test Calendly account, cancel any test booking still standing. | None is left on its calendar. | [doc:laravel-kit-spec.md section 4, hand-test rules] |
| C2 | G and A | Remove every `CLAUDE TEMP TEST` record from staging. | The agent searches for the words and finds none. | [doc:laravel-kit-spec.md section 4, hand-test rules] |
| C3 | G | Empty the test Docs out of the test Google account's letters folder. | The folder holds no test Doc. | [doc:laravel-kit-spec.md section 4, hand-test rules] |
| C4 | G approves by name; A does it | Remove the imported history from staging's database. | The agent reports counts of zero: clients, properties, files, invoices, messages, sources. | [doc:laravel-kit-spec.md 8.2: "the data is deleted afterwards"] |
| C5 | G | Remove the converted letters from the test Google account's Drive. Empty its trash too. | You see no letter in the folder and none in the trash. | [doc:laravel-kit-spec.md 8.2] [doc:build-handoff.md section 3, "Real data"] |
| C6 | G approves by name; A does it | Remove from the staging server the letters' photograph files, the copy of the old data, and the stored PDFs made from them. | The agent lists each place and finds it empty. | [doc:laravel-kit-spec.md 8.2] [doc:build-handoff.md section 3, "Photos"] |
| C7 | G | Remove every archive of staging made while it held the real history: from staging's bucket and from the test Google account's backup folder, trash included. | You see none left in either place. | [doc:laravel-kit-spec.md 8.2] |
| C8 | G | In Forge, start staging's queue worker and scheduler again. | Both running. | [doc:laravel-kit-spec.md 8.2] |
| C9 | A | Write down each path's result and each clean-up check, with the date. | Written. | [doc:laravel-kit-spec.md section 12: behaviours verified on staging, with dates] |

How a record is removed from staging. In v4 "delete" only hides. [doc:plan-v2.md section 2] So C2 and C4 are not done with the app's delete. They are not done by hand in the database either: on staging there is no tinker and no one-off script, and every data change is a committed, reviewed migration or command. [doc:laravel-kit-spec.md section 6, item 5] That leaves two ways: a committed clean-up command, or staging's database started again, empty.
- Unconfirmed: which of the two. Neither is built. Sancho's suggestion: start staging's database again, which does C2 and C4 in one act. It is owed by the app track before the rehearsal is run.

The staged copy of the real data on this Mac, in `~/Dev/hd-v4-import-data/`, is not part of this clean-up. You say what becomes of it. [doc:build-handoff.md section 6]

## The result

- All eighteen paths pass, and the clean-up checks pass: gate G is met. [doc:plan-v2.md section 7, step G]
- Any line fails: the agent finds the cause, the fix goes through plan, review and ship, and that path is run again from its first step. [doc:plan-v2.md section 7]
- What this rehearsal cannot show: whether Peter finds it easier than before. Only the first weeks live show that. [doc:plan-v2.md section 7, step J, and section 10]

**Tell Sancho, at the end:** "The dress rehearsal ran on (date). Passed: (paths). Failed: (paths and step numbers)."
