---
name: Home Directions v4 runbook, cutover from v3
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The one hard cut from v3 to v4, step by step, from plan-v2.md section 6: what must be true before the day, the import of the whole history from WordPress, the conversion of every letter since the last inspection into Google Docs, the old links, the freeze of v3, going live, the first jobs, and the way back (v3 frozen, not removed); who does each step and what is still unconfirmed
sources: ["[doc:plan-v2.md sections 6, 7, 8, 10]", "[doc:build-handoff.md section 3]", "[doc:laravel-kit-spec.md 7, 8, 13, 15]", "[doc:phase0-brief.md]", "[doc:requirements.md]", "[doc:census-2026-10-01.md]", "[doc:current-system.md]", "[doc:handoff.md, in the project folder]", "[doc:runbook-accounts.md]", "[doc:runbook-backups.md]", "[doc:runbook-dress-rehearsal.md]", "[doc:reviews/paperwork-W1.md]", "[gordon 2026-10-01]", "[gordon 2026-10-02]", "[web: vendor documentation pages read 2026-10-02, cited where used]"]
status: written 2026-10-02 overnight by the paperwork track (stage W1); reviewed the same night (reviews/paperwork-W1.md) and fixed by a third agent, see "W1 fixes" in build-log-paperwork.md; the import and the letter conversion were still being built when this was written, so the commands that run them are not named here
---
# Runbook: the cutover from v3

**The short version.** One cut, in production, on one day. No trial week for Peter and Maria Pia. "They will not use it for a week on staging. We're going to dive into the deep end with this launch. One hard cut over in production." [gordon 2026-10-02]

Seven steps on the day: freeze v3, take the copy of live, import the history, convert the letters, check them, point the old links, go live. [doc:plan-v2.md section 6]

**The way back.** v3 is frozen, not removed. For the first weeks, a job can still be done in v3 on a day v4 fails. [doc:plan-v2.md section 6, step 5] Nothing in this runbook deletes or changes a v3 record.

**Who does what.** You do everything that touches production, a password or the live WordPress site. The agent prepares, hands you exact text, and checks what it is able to see. It holds no production key and cannot run anything on production. [doc:plan-v2.md section 8] [doc:laravel-kit-spec.md 8.1 and section 13]

What Gordon set: the history comes in from WordPress, the letters come across in full, Peter works in one place from day one. [gordon 2026-10-01] [doc:plan-v2.md section 6]

---

## Part 1. Before the day: all of this must be true

Do not pick the day until every line is yes.

| # | Must be true | Gate | Source |
|---|---|---|---|
| 1 | The accounts are done, all thirteen steps | `runbook-accounts.md`, each "Tell Sancho" line said, the Google credential (step 11) and production (step 13) among them | [doc:plan-v2.md section 7, step B] |
| 2 | Backups are running to both places, and a restore has worked | `runbook-backups.md`, section 6.1: staging's own archive, restored in rehearsal Path 18 | [doc:plan-v2.md section 7, step B, and section 9] |
| 3 | The dress rehearsal passed on staging | `runbook-dress-rehearsal.md`, every line | [doc:plan-v2.md section 7, step G] |
| 4 | The import was rehearsed on staging and its counts reconcile | step H | [doc:plan-v2.md section 6 step 1, and section 7 step H] |
| 5 | The letter conversion was rehearsed on staging and you approved twenty letters, spread across the years | step H | [doc:plan-v2.md section 6 step 2] |
| 6 | Production is deployed, with the version that passed all of the above | you pressed Deploy; the agent confirmed the commit | [doc:laravel-kit-spec.md section 7, laravel-ship] |
| 7 | On production, the Connections panel shows Brevo, Google and both backup stores working. Calendly shows **not** connected: production holds no Calendly token, and its Dashboard shows no file made from a booking. Calendly waits for the day | Settings; and in Forge, production's Environment has no Calendly token in it | [doc:plan-v2.md section 5, Settings] [doc:plan-v2.md section 6 step 5] |
| 8 | On production, Settings is filled in: the three invoice texts, the template link, the two stamp images, the from address. The Calendly type map too, if the app lets it be set with no token in; if not, it is set in Step 7 | Settings | [doc:plan-v2.md section 5, Settings] |
| 9 | The three logins exist on production: Peter, Maria Pia, you | Settings, users | [doc:plan-v2.md section 4, users] |
| 10 | The mail test is answered: a message to office@homedirections.net reaches the Gmail box Peter and Maria Pia use | `runbook-accounts.md` step 7 | [doc:plan-v2.md section 11 item 4] |
| 11 | The redirect work on v3 is planned and approved as its own WordPress job | Part 2, step 6 | [doc:plan-v2.md section 6 step 3] |
| 12 | The one-page how-tos for Peter and Maria Pia are written, and each of them has read theirs. With no trial period, they are the only training | you asked each of them | [doc:build-handoff.md section 2 item 6] [doc:plan-v2.md section 10, the hard-cutover risk] |

Notes:
- About line 7. This is the opposite of the first draft of this runbook, which asked for Calendly to be working on production before the day. A booking creates a file, a client, a property and a Google Doc. [doc:plan-v2.md section 5] With the firm's token on production early, production would make real records for jobs Peter is still doing in v3, and the import would bring them in again. So the token goes in at Step 7 and not before. `runbook-accounts.md` step 8.
- About line 5, which letters. The plan still says "the last twelve months" in four places: its description, section 1, the table in section 2, and the opening of section 6. Its section 6 step 2 records your later decision: every letter since the last inspection on 2022-06-21. "Good, let's do all the letters". [gordon 2026-10-02] [doc:plan-v2.md section 6 step 2] This runbook follows the decision. The four older lines are listed for you in the build log.
- About line 5, how many. The plan's section 6 sets the gate at twenty letters opened by you. Its risk list still says "Peter's ten-letter gate", which is an older line. [doc:plan-v2.md section 6 step 2, and section 10] This runbook follows section 6 and the gate table: twenty, by you.
- About lines 4 and 5. The rehearsal on staging uses a copy of the old data. Production data reaches staging only when you copy it, for a named job. [doc:laravel-kit-spec.md 8.2]
- Unconfirmed: how Peter's and Maria Pia's passwords are first set on production. The documents say three logins and not how they are handed over. Sancho says once the login screens are final.
- Unconfirmed: the cutover date. Nothing on disk sets one.

---

## Part 2. The day

Order matters. Each step has one owner and one check. Do not start a step until the one before it has passed.

### Step 1. Freeze v3

**Who: Gordon.** Tell Peter and Maria Pia: from now, no new appointments in v3. [doc:plan-v2.md section 6 step 4]

1. v3 stays up. It is read-only in practice. It keeps serving the documents of older jobs, whose links work exactly as now until Phase 2 replaces them. [doc:plan-v2.md section 6 step 4]
2. Nothing is switched off, removed or edited on v3 in this step.

- Unconfirmed: the order. The plan lists the freeze as its step 4, after the import. [doc:plan-v2.md section 6] The import reads the live site once, at cutover. Anything entered in v3 after that reading would be missing from v4. So Sancho's reading is that the freeze comes first, as written here. You say if that is wrong.
- Unconfirmed: whether "read-only in practice" is only a word to Peter and Maria Pia, or also a switch on the site. The plan says "in practice". [doc:plan-v2.md section 6 step 4]

**Check:** both of them have said yes.

### Step 2. Take the copy of live that the import reads

**Who: Gordon.** The import runs "once against live at cutover". [doc:plan-v2.md section 6 step 1]

1. Take a fresh backup of the live WordPress site, after the freeze. You did the same with the dev clone for the rehearsal. [doc:build-handoff.md section 3, "Real data"]
2. That backup is also the proof of how v3 stood on the day. Keep it.

- Unconfirmed: how the old data reaches the production server for the import. The importer reads the old tables through a named database connection. [doc:build-handoff.md section 2 item 5] For the rehearsal that was a file made from the backup on this Mac. The loader used that night was the planning thread's own tool; the build was told to write the app its own if the cutover needs one. [doc:build-handoff.md section 3, "Real data"] Copying production data anywhere is yours, per job. [doc:laravel-kit-spec.md section 13] The exact steps are written after the rehearsal on staging (step H), which has to solve the same thing.
- Unconfirmed: how the letters' photographs reach the production server. The old site will not hand a photo to anyone who is not logged in, so Google cannot fetch them from it. The app must hold the photo files itself and hand them to Google by an address Google can reach for a short time. That design could not be proven on the night it was written. [doc:build-handoff.md section 3, "Photos"]

**Check:** the backup file exists and is dated after the freeze.

### Step 3. Import the history

**Who: Gordon starts it on production. The agent has prepared it and reads the result with you.**

What comes in: clients, properties, job records and who was copied, for the whole history. [doc:plan-v2.md section 6 step 1] [gordon 2026-10-01: "whole history"]

1. The count to expect, as the census found it: 10,212 jobs. 9,442 came from v2 and are read from v2's own tables inside the WordPress database, cross-checked against the WordPress records. 770 were made in v3 and are read from WordPress. [doc:plan-v2.md section 6 step 1] Live gains two to three jobs a week, so it will hold more by the day. [doc:plan-v2.md section 4] The numbers that count are the ones read from the live copy that day.
2. Test records are left out on purpose: every record whose client name, property address or title contains the whole word "test", and every record dated more than two years after the day of the import (the clone's three markers are dated 2034, 2099 and 8888). Their invoices and letters are left out with them. Each one is counted and listed by its WordPress ID with the reason. None is dropped silently. A real job still to come on the day of the import is not a test record: it comes in like every other job, and the import lists these by WordPress ID under "jobs still to come, brought in". Keep that list for the Calendly step. [gordon 2026-10-02] [doc:build-handoff.md section 3, "Test records are skipped"] [doc:reviews/app-W10-W11.md finding 2] [doc:build-log-app.md W12]
3. Every imported row is recorded as from WordPress and not verified. [doc:plan-v2.md section 6 step 1, and section 4]
4. Duplicates are suggested, never merged silently. [doc:plan-v2.md section 4]
5. The import is safe to run twice, logs what it changed, and has a dry run. [doc:laravel-kit-spec.md section 4, data and migrations] Run the dry run first.

- Unconfirmed: how the import is started on production. Forge's Commands panel runs a command as the site's user, takes no typed input, and stops any command at five minutes. [web:laravel.com/forge/docs/sites/commands.md 2026-10-02] An import of this size may not fit in that. Whether it is started from that panel as a background job or from a button in the app is settled when it is built. The command's name is not in this runbook for the same reason.

**Check: the counts reconcile.** Jobs by year and by type, before and after, must match. The census tables are the pattern. [doc:plan-v2.md section 6 step 1] Imported plus skipped equals what was read. If they do not match, stop. Nothing has been lost: v3 is untouched.

**Check: nothing went out.** Production holds the firm's live Brevo key while these records are made. [doc:plan-v2.md section 10, "A message goes to a real client"] Before going on, both must be true:
1. The app's own record of messages on production shows none since the day began.
2. Brevo's own list of sent messages shows none from the app today.

- Unconfirmed: how you read the app's count of messages on production. The message log sits on each file's page; no screen gives a total. [doc:plan-v2.md section 5, "Screens"] A count on a screen, or one command from Forge, is owed by the app track.
- Unconfirmed: check on the vendor's page when you do this step: where Brevo lists the messages an account has sent.

### Step 4. Convert the letters

**Who: Gordon starts it on production. The agent has prepared it.**

What comes across: every letter since the last home inspection, which was on 2022-06-21. [gordon 2026-10-02: "Good, let's do all the letters"] [doc:plan-v2.md section 6 step 2] On the clone that was 438 published letters. [doc:build-handoff.md section 3] The number on the day is read from the live copy.

For each one:
1. The letter's text and images go into a copy of the new template, as a Google Doc in the firm's letters folder. [doc:plan-v2.md section 6 step 2]
2. The Doc is named by the rule: `Home-Directions-letter_YYYYMMDD_property-address_client-name`. [doc:plan-v2.md section 5, "Letters"]
3. It is filed with its job. [doc:plan-v2.md section 6 step 2]
4. Its invoice comes across with its text, its total and its paid state. [doc:plan-v2.md section 6 step 2]
5. A PDF is made of it as it stood. That PDF is the letter as the client last saw it, and it is what the old link will lead to. [doc:plan-v2.md section 6 step 3]

- Unconfirmed, and yours to decide: the old invoice links. The plan says each migrated letter **and invoice** had a public address on v3, and sends those addresses to "the PDF made at migration, which is the letter as the client last saw it". [doc:plan-v2.md section 6 step 3] That names one PDF, the letter's. It does not say what an old invoice link should show. Two ways:
  - (a) An invoice PDF is also made at migration, and the old invoice link leads to it.
  - (b) Old invoice links are left alone. They keep showing the v3 invoice page, as now.
  - Until you choose, this runbook takes (b), the one that changes less on the live site. Either way, an old invoice link is never pointed at a letter.

What the real letters taught, and what to expect:
- Empty tables are dropped. Letters whose tables hold text are listed by ID for a person to look at. There were three on the clone. [doc:build-handoff.md section 3]
- A client with no street address gets an address block of the name alone. [doc:build-handoff.md section 3]
- Photographs: on the clone, 298 of the 304 letters with photos had every photo; a few photos point at another site or are missing. Those letters are listed, not hidden. [doc:build-handoff.md section 3, "Photos"]
- The original of every letter stays on v3, untouched. [doc:plan-v2.md section 10]

- Unconfirmed: how long the conversion takes and how it is started. It is the same question as step 3, and it talks to Google for each letter.

**Check:** the count of Docs made equals the count of letters read, less the ones listed as failed, each with its reason.

**Check: nothing went out, and nothing was opened to the public.** Sending a letter is what sets its Doc to "anyone with the link can view" and mails the client. [doc:plan-v2.md section 5, "Sending a letter"] The conversion must do neither. Before going on, all three must be true:
1. The app's own record of messages on production still shows none since the day began.
2. Brevo's own list of sent messages still shows none from the app today.
3. The count of converted Docs shared by link is zero.

- Unconfirmed: how the third count is read. The conversion's own report should give it. That is owed by the app track.

### Step 5. The gate: you open the letters

**Who: Gordon.** Open letters spread across the years, in Google Docs, and say they are right. [doc:plan-v2.md section 6 step 2] They are Google Docs, so this needs no login to the new system. [doc:plan-v2.md section 6 step 2]

1. Look at: the letterhead and signature, the address block, the date, the body's paragraphs, the photographs and their captions, the Doc's name.
2. Look at every letter on the "tables with text" list and every letter on the "photos missing" list.
3. Open two of the invoices that came across. Text, total and paid state are as v3 shows them.

- Unconfirmed: how many to open on the day itself. The plan sets twenty for the rehearsal gate. [doc:plan-v2.md section 7, step H] Sancho's suggestion is twenty again, because these are the real Docs.

**Check:** you say "the letters are right". If not, stop. The Docs can be thrown away and made again; the originals are on v3.

### Step 6. Point the old links

**Who: Gordon takes the list out of production. The agent prepares the WordPress job from it. Gordon approves the job and ships it.**

Each migrated letter and invoice had a public address on v3. [doc:plan-v2.md section 6 step 3] [doc:requirements.md, "Facts that constrain the design"] Those addresses are sent to the PDF made in step 4. [doc:plan-v2.md section 6 step 3]

1. v4 produces the list, on production: each old address and what it should lead to now. [doc:plan-v2.md section 4, old_links] The new addresses exist only on production, after step 4, and the agent holds nothing that reaches production. [doc:plan-v2.md section 8] So you take the list out, by a button in the app or one command from Forge, and hand it to the WordPress job.
   - The list holds web addresses only: no name typed beside them, no email, no letter text.
   - Unconfirmed: the way to take the list out is not built. It is owed by the app track.
   - Unconfirmed: whether the old addresses themselves spell out a client's name or a property's address. If they do, the list is client data: it stays out of the Sancho tree, out of both repositories and out of the chat.
2. While v3 is up, the redirect lives on v3. Its Redirection plugin is already installed. [doc:plan-v2.md section 6 step 3] [doc:census-2026-10-01.md]
3. This is a change on the live WordPress site. It is done through the WordPress kit, with your say, as its own job. [doc:plan-v2.md section 6 step 3]
4. Only what was migrated is redirected: the letters, and the invoices only if you chose (a) in step 4. Every older document keeps its v3 address and keeps working as now. [doc:plan-v2.md section 6 step 4]

- Unconfirmed: the web address each PDF is served from, and that a client can open it without a login. The plan says the old address leads to the PDF and not where the PDF lives. [doc:plan-v2.md section 6 step 3]
- Unconfirmed: how the redirects are loaded into v3, one by one or as one file. It is decided in the WordPress job's own plan.

**Check:** you open five old links from five different years in a browser that is not logged in to anything. Each shows the PDF of that letter. One older link, from before 2022-06-21, still shows the v3 page. One old invoice link from a migrated job shows what you chose in step 4: under (b), the v3 invoice page as before. It never shows a letter. [doc:plan-v2.md section 6 steps 3 and 4]

### Step 7. Go live

**Who: Gordon.** Calendly is pointed at v4, and Peter's next job is done in it. [doc:plan-v2.md section 6 step 5]

1. Make the firm's Calendly token now, in the firm's own Calendly account. `runbook-accounts.md` step 8, item 4, shows how. Enter it in Forge on the **production** site's Environment. This is the first moment production holds one. [doc:plan-v2.md section 6 step 5]
2. Open production's Settings. Set the type map if it could not be set before. Press the Calendly test button on the Connections panel. [doc:plan-v2.md section 5, "Screens", Settings]
3. From then, a booking creates the file, the client and the property; a cancellation marks the file cancelled; a reschedule moves the date. [doc:plan-v2.md section 5, "Calendly"]
4. The 15-minute check is running too, as the safety net. [doc:plan-v2.md section 5, "Calendly"]
5. Give Peter and Maria Pia their logins and the address. Their one-page how-tos are already in their hands: Part 1, line 12.
6. Sancho's suggestion, not in the plan: take a backup now, and see it arrive in both places. From tonight the nightly archive holds the whole history anyway. [doc:plan-v2.md section 9]

- Unconfirmed: how Calendly's instant notices are switched on once the token is in: a button on the Connections panel, or a step in a deploy. It waits on how the app sets them up. `runbook-accounts.md` step 8.
- Unconfirmed: what the app does with a booking that arrives after the token goes in and before the type map is set. Sancho says from the built app. If it matters, you stop production's scheduler in Forge for those minutes.
- Unconfirmed: whether anything else listens to the firm's Calendly account today. v3 takes its appointments from a form filled in by hand, not from Calendly. [doc:current-system.md, "How a job flows" item 1] So by the documents there is nothing to disconnect. Look at the Calendly account's connections to be sure.
- Bookings already on Calendly's calendar for dates after the cut. The jobs typed into v3 for those dates came in with the import (item 2 of the import step: it brings in the jobs still to come and lists them). After "Switch bookings on", the first 15-minute check opens no file for a booking that was in Calendly before: it lists each one under Connections, with the file it likely is. For each, press "This is that file" (or "Open a file for it" where v3 held none, or "Leave it"). Connections also lists the imported jobs still to come that have no booking tied to them yet: when every booking is settled, what is left on that list should be only jobs that were never booked through Calendly. Proven on invented data; unconfirmed against the real Calendly account. [doc:build-log-app.md W10 item 3 and W12 item 2]

**Check:** the Connections panel shows Calendly working. Peter's next booking appears as a file within fifteen minutes. [doc:plan-v2.md section 5]

**Gate for the whole cutover:** Peter's first real job in production goes through, and v3 stays frozen and intact as the way back. [doc:plan-v2.md section 7, step I]

---

## Part 3. The first four weeks

1. After each of the first jobs, the log and the error reports are read. [doc:plan-v2.md section 7, step J]
2. Every message in the log is what Peter meant to send. [doc:plan-v2.md section 7, step J]
3. Peter says it is easier than before. [doc:plan-v2.md section 7, step J] [doc:requirements.md R2.2]
4. After each deploy, the agent checks the two addresses that need no login and confirms the commit. You look at the pages, from a short list the agent prepares. [doc:laravel-kit-spec.md D14, and section 7 laravel-ship step 5]

- Unconfirmed: how the agent reads production's log. The plan says the agent reads the log and the error reports after each early job. [doc:plan-v2.md section 7, step J] The spec says the agent holds nothing that reaches production. [doc:laravel-kit-spec.md 8.1] Both cannot be true as written. Either you read the message log on the file's page and tell Sancho, or the app sends its error reports somewhere the agent may read. This needs your decision before the day.

---

## Part 4. The way back

**v3 is frozen, not removed. That is the whole of the safety net, and it is enough.** [doc:plan-v2.md section 6 step 5, and section 10]

### If v4 fails on a working day

| Step | Who | What |
|---|---|---|
| 1 | Gordon | Tell Peter: do this job in v3, as before. [doc:plan-v2.md section 6 step 5] |
| 2 | Gordon | Tell Sancho what failed. The agent finds the cause from what it can see. |
| 3 | Nobody | Calendly bookings need no action. When v4 is back, the 15-minute check picks up anything it missed, and each booking is acted on once. [doc:plan-v2.md section 5, "Calendly"] |
| 4 | Gordon | If a bad deploy caused it: go back a release in Forge. Forge keeps the last four. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] |
| 5 | Gordon | If the data is damaged: restore last night's archive, by the written procedure. `runbook-backups.md` section 6. |
| 6 | Gordon | If v4 will be down for more than a day: switch the redirects off in v3's Redirection plugin. The old links then show the v3 pages again. It is a change on the live site: yours, through the WordPress kit. [doc:plan-v2.md section 6 step 3, and section 10] |

While v4 is down, the redirected old links are down too. After step 6 of the day, the old address of each migrated letter leads to a PDF that v4 serves. A client who opens such a link on a day v4 is down gets an error, although the original is still on v3. [doc:plan-v2.md section 6 step 3, and section 10] Row 6 is the answer when it lasts.

- Unconfirmed: the exact steps to go back a release in Forge. [doc:laravel-kit-spec.md section 15] They are done once on staging and written down in the dress rehearsal, Path 17, line 17.1. Going back a release does not undo a change to the database. [doc:laravel-kit-spec.md section 4, Rollback]
- Unconfirmed: what becomes of a job done in v3 during a bad day. It is not in v4. Either it is entered into v4 by hand afterwards, or the import is run again for it. The documents do not say. The import is built to be safe to run twice. [doc:laravel-kit-spec.md section 4]
- Known limit: if v4 is down for a whole day, Calendly is reported to switch its notices off. The 15-minute check still works, and a failure lasting a day raises an alert. [doc:plan-v2.md section 10] That alert is seen working once on staging: dress rehearsal Path 17, line 17.5.

### If the cutover itself goes wrong, on the day

1. Stop at the step that failed. Steps 2 to 5 change nothing on v3 and nothing a client sees.
2. Tell Peter and Maria Pia that v3 is open again. That undoes step 1.
3. If step 6 was done, the redirects can be taken off v3 again, as their own WordPress job. The old addresses then show the v3 pages as before, because the originals were never touched. [doc:plan-v2.md section 10]
4. If step 7 was done, take the Calendly token out of production's Environment in Forge again.
   - Unconfirmed: check on the vendor's page when you do this step: how a token is withdrawn in Calendly itself, and whether the notices the app set up stop with it.
5. The Docs made in step 4 can stay or be thrown away. They are copies.

### What the way back does not cover

It ends. v3 is retired in Phase 2, with v2. [doc:plan-v2.md section 3] Until then, nothing may be removed from v3.

---

## What the cutover deliberately does not do

- Verify or repair the history. That is Phase 2. [doc:plan-v2.md section 6]
- Print PDFs of older documents. Phase 2. [doc:plan-v2.md section 6]
- Touch v2. Phase 2. v2 is read, never operated: no click, no form, no checkbox. [doc:plan-v2.md section 6] [doc:handoff.md]
- Carry WordPress's errors out. They come in with the import, marked unverified, and Phase 2 corrects them. You accepted that. [gordon 2026-10-01] [doc:plan-v2.md section 10]

## One thing waiting on you afterwards

The real data staged for the rehearsal, in `~/Dev/hd-v4-import-data/` on this Mac. You say what becomes of it once it has served its purpose. [doc:build-handoff.md section 6]

**Tell Sancho, at the end of the day:** "The cutover is done. Imported: (count). Skipped: (count). Letters converted: (count). Old links checked. Calendly is on. Peter and Maria Pia have their logins."
