---
name: Home Directions v4 requirements
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: What Gordon and Peter asked for on 2026-09-29, one requirement per line with the transcript timestamp; Sancho's inferences marked as such; the source of truth for the plan
sources: ["[rec_8d15ed467e 2026-09-29]", "[gordon 2026-09-30]", "[web:https://www.homedirections.net 2026-10-01]"]
---
# Home Directions v4: requirements

Every line cites the transcript (`[hh:mm:ss]`, speaker as confirmed: 01 = Gordon, 02 = Peter) or Gordon directly. Lines marked **inferred** are Sancho's reading, not something either of them said; treat them as questions. The transcript has diarization fragments on SPEAKER_00 (mostly Peter's dictation pauses and the lunch order); nothing from 00 is used as a requirement.

## Business context (why the system is smaller than the old one)

- Peter has limited the practice to structural troubleshooting and design since 2022; the home-inspection side is being retired entirely. [gordon 2026-09-30] [web:homedirections.net "2022-present"]
- Three services, and therefore three kinds of file: **Professional Opinion, $875** (up to 1 h visit or virtual, documentation letter); **Structural Design, $1,250** (visit, load calculations, stamped documentation letter); **Design work for architects, builders, homeowners, $475/h** (beam and structural design from plans, usually remote, booked by phone, not Calendly). [web:homedirections.net] [00:00:28 Peter: "one for the 875, one for the 1250, and one for the engineering jobs"]
- Clients book the first two online through Calendly; Peter sets up the hourly design jobs himself, "in my spare time," not on a calendar basis. [00:00:43 Peter]
- Service area: 35 minute radius of Ridgefield, CT; licensed CT (#13055) and NY (#89793). [web:homedirections.net] [doc:hdonline-home-directions/single-hdo_reports.php:156]
- Two people touch the documents: Peter and "Mom" (Gordon's mother; unconfirmed whether she is Maria Pia Seirup, Treasurer, named on the invoice template). [09:30 Gordon: "Mom can edit it"] [doc:hdonline-home-directions/single-hdo_invoices.php:173]

## R1. Intake from Calendly

- R1.1 The system listens to Calendly; when a client books online, it creates the appointment record from the booking: client name, property address, email, appointment type, price. [04:53 Gordon]
- R1.2 If a client cancels through Calendly, the appointment and its Google Doc shell are removed automatically. [14:42 Gordon]
- R1.3 Peter can also create an appointment by hand (design clients; "for some other esoteric reasons someone didn't book the Calendly"), choosing the type. [12:37 Gordon]
- R1.4 **inferred:** reschedules in Calendly should move the appointment date rather than create a second one. Not discussed.
- R1.5 **inferred:** the Calendly booking form must ask for the property address (a required question), or R1.1 cannot be met. Not discussed; the current Calendly questions are unknown.

## R2. The file (appointment record)

- R2.1 Backed by a proper relational database: a clients table, unique and deduplicated; a properties table, unique and deduplicated; so Peter can look up a property and see whether he has been there and for which clients, or a client and where he has worked for them. [05:00 Gordon]
- R2.2 The file shows all client data and lets Peter edit it in place (misspelled email, last name). "Yes, that does happen." [06:30 Gordon, 06:51 Peter]
- R2.3 Editing a fact once fixes it everywhere: in the system, in the letter's content, and in the letter's file name. The old system scattered data so a correction "only corrects it for the printout"; Peter has lived with wrong street names ("Shady Lane" that is really Shad Hill Road) rather than ask. [15:25 Peter, 16:44 Gordon, 17:00 Peter]
- R2.4 Appointment type is a three-way choice: **virtual**, **site visit**, **design**. [12:37 Gordon]
- R2.5 A big paragraph text field for the narrative description of what was actually done; it feeds the invoice. Price is editable per file. [06:30 Gordon]
- R2.6 Peter can delete an appointment from the system (double confirmation), whether or not it came through Calendly. [14:42 Gordon]
- R2.7 Streamline the property facts: septic, sewer, square footage and "comments" were inspection-era fields Peter leaves blank now; "As provided at time of booking" existed only because inspection clients misreported house size. [18:57 to 19:50 Peter]

## R3. The letter (the product)

- R3.1 The letter is a Google Doc, created from a template that carries the letterhead and the standard layout for the client's address block. [07:30 Gordon]
- R3.2 File name: `YYYY-MM-DD_<client last name>_<property address>`, plus something that says Home Directions so the client recognises it (the client sees the file, not just the report, from now on). [07:50 Gordon, 17:19 to 18:07]
- R3.3 The doc is linked from the file; Peter (and Mom) edit it in Google Docs, as long as they like, in multiple tabs; nothing about that is dangerous any more. [09:30 Gordon]
- R3.4 Peter drafts by voice or text into email and pastes into the doc. [09:30 Gordon]
- R3.5 When sent, the client gets read-only access (anyone with the link can view). If Peter edits after sending, the client's link shows the newest version; Peter accepted that ("You like the fact that the link updates. Let's just leave that as is"). A "revised on" box like building drawings was floated and parked as too complicated. [10:02 to 10:59]
- R3.6 It must still look like it came from an engineer: letterhead, signature, stamp, licence numbers; the read-only view should look like a document, not an editor. Gordon will send himself one to check. [18:29 to 18:57]
- R3.7 Stamped documentation letters are the deliverable for the $875 and $1,250 services; "stamped" can be dropped from an invoice line for a virtual visit. [12:31 Peter] **inferred:** the letter template therefore needs stamp variants (CT, NY, none), as the old system had.

## R4. Invoices

- R4.1 Generated automatically when the file is created, as a PDF from a template. [06:30 Gordon]
- R4.2 Three standard invoice descriptions, one per service, as **templates Peter edits in a Settings page**, so they are "not hidden in code somewhere forever"; a change applies to new invoices only; each invoice starts from the template and can be edited freely. [04:12 to 04:53, 30:04 Peter]
- R4.3 The three texts as Peter dictated them [11:33 to 12:31, 24:35 to 27:00, 27:42 to 30:31]; mishearings possible, Peter expects to edit these in Settings:
  - **$875 Professional Opinion:** "Structural consultation including site visit, diagnosis, prescription, calculations as necessary, and preparation of stamped documentation letter." Variants: "virtual site visit"; drop "stamped".
  - **$1,250 Structural Design:** "Structural consultation including site visit, calculation of loads, evaluation of different beam and load path configurations, calculations of chosen beam, column and footing configuration, and preparation of stamped documentation letter."
  - **Design clients (hourly):** "Time spent on the project at the above address during [period], including evaluation of architectural drawings and photographs; phone, email and text conversations with client; calculation of structural loads involved; mathematical evaluation of various structural configurations; final calculation of chosen joists, rafters, beams, columns and foundations; and preparation of stamped documentation letter."
- R4.4 The file page can send the invoice, mark it paid, and resend it. Marking paid automatically sends the client a paid copy ("just good transactional business and housekeeping"). [08:30 Gordon, Peter: yes]
- R4.5 **inferred:** an invoice needs a stored total and line items, not arithmetic in a template; the old invoices re-render at today's prices. [doc:survey-hdonline-home-directions.md §6]

## R5. Sending and email

- R5.1 "Send / deliver letter" sends from the system, from a properly authenticated real email address, not PHP mail, for deliverability. [09:00 Gordon]
- R5.2 The system keeps email logs: invoice sent at, letter sent at; return receipts or delivery confirmation if achievable. [09:20 Gordon]
- R5.3 Sending delivers whatever the latest version of the doc is. [09:45 Gordon]

## R6. Dashboard

- R6.1 On login: a **New Appointment** button, the most recent appointments in an infinite-scroll list, and a link to Settings. [12:50 Gordon]
- R6.2 Search across everything, by client name, property address, or a time window ("show me what I did in May of 22"). Peter: unlikely but possible, "I just did it recently." [23:05 to 23:50]

## R7. Migration and retirement (Phase 2)

- R7.1 About a year of recent letters lifted out of WordPress into Google Docs so they can be edited if needed; then the old system is retired "once and be done, with a good date." [20:00 Gordon]
- R7.2 Old inspection reports are never edited again; their links must keep working. Generate each report, print to PDF, store the PDF, redirect the old link to it. Today each view regenerates the report. [20:30 Gordon]
- R7.3 All the way back: the 1997-era Word files (Peter: "started in 83, on the computer in 86; lost about 88 to 91; not 94 to 96") read and spooled to PDF into one knowledge base. [21:00 to 21:36]
- R7.4 Reassemble the database that "got blown apart" from backups to shrink the roughly two percent data loss, before printing the old PDFs. [21:50 Gordon]
- R7.5 Retire the current system and "the Grayson system that's still online" (a predecessor, unconfirmed what it is). [21:36 Gordon]
- R7.6 End state: an appointment record for every historical job (who, when, where) with its PDF attached, searchable (R6.2); all old systems permanently retired. [23:05 Gordon]
- R7.8 The new system's database houses **all the legacy data going back to the early 1990s**, not only a file row with a PDF attached; "so we may need more tables." [gordon 2026-10-01] This strengthens R7.6. Which legacy fields become columns and which stay inside the archived PDF is not yet stated; the census decides what exists to carry.
- R7.7 Peter's real need from history: "somebody calls me about a crack in a foundation and if I've been there, 35 years ago, 22 years ago; sometimes I wrote on the wall; if I have it in a report, those are really interesting to have." [22:31 Peter]

## R8. Out of scope, parked, or separate

- Website changes: homedirections.net still has leftover inspection content; Peter wants a few changes; "some other time," together. [13:41 to 14:29]
- "Revised on" revision box in the letter (R3.5): parked.
- Tech stack: "to be determined, might still be WordPress, thinking not; doesn't much matter to you." Gordon to decide with the AI. [05:00 Gordon] **Decided 2026-10-01: Laravel.** [gordon 2026-10-01] [doc:phase0-brief.md Decisions]
- Peter's ask about communication: email Gordon rather than text (texts are ephemeral; phone calls bad; email "dodgy" but best). [27:00 to 27:42]

## Facts that constrain the design (from the code, cited in the surveys)

- Reports and invoices are public by URL since 2026-02 (page passwords removed at Peter's request after years of trouble). [doc:survey-hdonline.md §4]
- The current PDF is the browser's print dialog after five retired PDF mechanisms. [doc:survey-hdonline-home-directions.md §9]
- The current email is a Gravity Forms notification; nothing logs delivery. [doc:survey-hdonline.md §6.4]
- Corrections do not propagate today because report and invoice titles/slugs are derived and rewritten on save while the doc content is a frozen Gutenberg blob. [doc:survey-hdonline.md §9 item 23, 43]
- The inspector is hard-coded to WordPress user 5, who is Peter; he is the only inspector. [gordon 2026-09-30] [doc:survey-hdonline-home-directions.md §3]
