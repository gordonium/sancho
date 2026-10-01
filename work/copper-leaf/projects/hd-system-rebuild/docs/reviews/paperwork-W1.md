---
name: Home Directions v4 review, paperwork stage W1
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Independent review of the four runbooks written for Gordon's side (accounts, backups, cutover, dress rehearsal): 23 numbered findings, each with the file and heading, what is wrong, the evidence, the fix and a weight; then the citations that were opened and checked, and the vendor pages re-read
sources: ["[doc:runbook-accounts.md]", "[doc:runbook-backups.md]", "[doc:runbook-cutover.md]", "[doc:runbook-dress-rehearsal.md]", "[doc:build-log-paperwork.md]", "[doc:build-handoff.md]", "[doc:plan-v2.md]", "[doc:hosting-options.md]", "[doc:laravel-kit-spec.md]", "[doc:phase0-brief.md]", "[doc:requirements.md]", "[doc:hosting-claims.md]", "[doc:laravel-tooling-research.md]", "[doc:current-system.md]", "[doc:plan.md]", "[doc:build-log-app.md]", "[doc:handoff.md, in the project folder]", "[doc:/Users/gordonium/Sync/Sancho/CLAUDE.md]", "[file:/Users/gordonium/Dev/clc-laravel/hdonline-v4/.env.example, setting names only, read 2026-10-02 01:15]", "[web: Forge, Calendly, Cloudflare and DigitalOcean documentation pages re-read 2026-10-02, listed at the foot]"]
status: written 2026-10-02, finished 01:21 CEST, by a reviewer that did not write the runbooks; 2 blockers, 13 should-fix, 8 minor; no runbook was changed; nothing else was written
---
# Review: paperwork stage W1 (the four runbooks)

Reviewer: Claude, model `claude-fable-5-1`. I cannot see my own effort level. I did not write the runbooks and I changed none of them.

**The conclusion first.** The runbooks follow the decisions closely. One server, the backup schedule and retention, the two backup stores, keys entered by Gordon in Forge, the hard cut with v3 kept as the way back, and every letter since 2022-06-21 are all stated as decided. Of 64 citations opened, 61 say what they are cited for. The trouble is in the order of things and in what the rehearsal does not prove. Two findings would have Gordon do something the plan forbids. Thirteen should be fixed before he works from these. Eight are small.

Weights: **blocker** would cause a wrong action; **should-fix**; **minor**.

---

## Blockers

### 1. Production starts acting on real Calendly bookings weeks before the cutover

**Where.** `runbook-accounts.md`, "8. Calendly", items 3 and 4, and its "Tell Sancho" line; "4.3 Before the first deploy", item 6. `runbook-cutover.md`, Part 1, line 7; Part 2, "Step 7. Go live".

**What is wrong.** The accounts runbook has Gordon put the firm's real Calendly token on the production site, and switch the scheduler on, as part of setting up accounts. It says itself that the 15-minute Calendly check hangs on the scheduler. The cutover runbook then requires, before the day is even picked, that production's Connections panel shows Calendly working. But the cutover's own Step 7 says Calendly is switched on at go-live, and marks "how the connection is switched on" as unconfirmed. Nothing in either runbook holds the intake off in between. By the plan, a booking creates a file, a client, a property and a Google Doc. So from the day the token goes in, production would make real records and real Docs in the firm's Drive for real clients, while Peter is still doing those jobs in v3. The import then brings the same jobs in from WordPress a second time.

**Evidence.** Plan: "Calendly is pointed at v4" is part of going live, not before. [doc:plan-v2.md section 6 step 5; section 7 step I] What a booking creates, and that the system asks Calendly every 15 minutes. [doc:plan-v2.md section 5, "Calendly"] The cutover runbook already half sees it: its own note on bookings that are on the calendar before the cut.

**Fix.** Pick one and say it in both runbooks. Either (a) the production token is not entered until cutover Step 7, and Part 1 line 7 says "Brevo, Google and both backup stores working; Calendly waits for the day"; or (b) the app gets a plain switch, "take bookings from Calendly", off by default, which Gordon turns on in Step 7, and the Connections panel can show Calendly reachable while the switch is off. (b) is a requirement for the app track; say so to it. Either way the "Tell Sancho" line of accounts step 8 must not include a live production connection.

**Weight: blocker.**

### 2. The Mac's key goes on the staging site with no condition that the guard is in place first

**Where.** `runbook-accounts.md`, "4.4 Staging only", item 1; and "Not in this runbook", first line.

**What is wrong.** The runbook tells Gordon to add this Mac's key for the staging site's user. It lists "registering the kit's hooks on this Mac" as outside the runbook, with no order between the two. The approved plan sets that order as a gate: the guard's tests pass before any staging key exists. On one server this matters more, not less: the key opens the machine that also holds production, and the only wall is a permission between two users.

**Evidence.** "the guard's tests pass before any staging key exists". [doc:plan-v2.md section 7, step A] "Both guards ... Before any staging key exists." [doc:laravel-kit-spec.md section 14, step 3] The hooks are not registered tonight, by rule. [doc:build-handoff.md section 3, "Do not register hooks", and section 6] What one machine costs in protection. [doc:hosting-options.md Decision, last paragraph]

**Fix.** Add one line at the head of 4.4 item 1: "Not before the kit's shell guard and browser guard are registered on this Mac and their tests pass. Sancho tells you when." Add the same as a line in the step's "Tell Sancho" text, so the key and the guard are confirmed together.

**Weight: blocker.**

---

## Should-fix

### 3. Forge fills each site's settings from the app's example file, which holds three passwords the agent made

**Where.** `runbook-accounts.md`, "4.3 Before the first deploy", item 4 ("The environment").

**What is wrong.** The step says Sancho gives the names and Gordon enters the values. It does not say that Forge has already filled the site's Environment before he opens it. Forge copies the repository's example settings file into the new site when the site is created. The app's example file is written for this Mac: it carries the three local login passwords the build generated, and its own comment says a server never gets them. On Forge, a server does. It also carries this Mac's local settings for the app's mode and its error display. Left as copied, production would start in local mode with full error pages (the kit's rule is debug off in production), with the kit's protection against destructive commands switched off (it is on everywhere except local and testing), and holding three passwords the agent knows.

**Evidence.** Forge's page on environment variables, in a tip under its introduction: an example file found in the project is copied at site creation, with some database settings replaced. [web:laravel.com/forge/docs/sites/environment-variables.md, re-read 2026-10-02; the runbook cites this same page] The passwords live in the example file by instruction. [doc:build-handoff.md section 2 item 7] [doc:build-log-app.md, stage P1 plan, item 4] The example file's setting names, and its comment. [file:hdonline-v4/.env.example, names only] "debug off in production"; the destructive-command switch. [doc:laravel-kit-spec.md section 4]

**Fix.** In 4.3 item 4, add: "Forge has already filled this box from the app's example file. Before the first deploy, on both sites: remove the three seed-password lines; set the app's mode to production (staging: staging) and error display off; make sure the app key was made on this server. Sancho gives the exact names." Tell the app track that its comment is wrong on Forge, and that the seed passwords would be safer in a file Forge does not copy.

**Weight: should-fix.** Whether Forge also rewrites the mode line was not confirmed; the passwords landing on the server is certain.

### 4. The mail trap is never set by a step and never proven; real client addresses then arrive on staging

**Where.** `runbook-accounts.md`, "4.4 Staging only", item 3. `runbook-dress-rehearsal.md`, Set-up line S5, "The test people and places", and "Path 16". `runbook-backups.md`, section 6.

**What is wrong.** The decision is that staging mail goes to a trap. In the accounts runbook that is a sentence, not a step: it names no setting and no one who sets it. In the rehearsal, S5 says "send one and see where it lands", but every address used in the rehearsal is Gordon's own, so a message reaching Gordon proves nothing about the trap. Then Path 16 and the restore test put real client records, with real email addresses, on staging, and have Gordon open real jobs there with the queue worker running. One press of Send on such a file would test the trap for the first time on a real client.

**Evidence.** "Staging mail goes to a trap; staging uses test accounts." [doc:plan-v2.md section 10] "Mail on staging goes to a trap, never to clients." [doc:laravel-kit-spec.md 8.2] The clone itself uses a reroute plugin for exactly this reason. [doc:census-2026-10-01.md, plugin list]

**Fix.** Make it a step with an owner: the setting that sends every staging message to one address, entered by Gordon on the staging site, name supplied by Sancho. In the rehearsal, change S5 to: make a test file whose client address is **not** Gordon's (an invented address at a domain that cannot receive mail), send its invoice, and expect it in Gordon's inbox and nowhere else; the agent confirms from staging's log that the typed address was replaced. Run that line again as the first line of Path 16, before any real record is opened.

**Weight: should-fix.**

### 5. A second Brevo key on the firm's account, placed on staging, is a real sending key the agent can read

**Where.** `runbook-accounts.md`, "7. Brevo", item 6.

**What is wrong.** The item leaves open "whether that is a second key on the same Brevo account". It does not say what that would mean. Staging's settings are readable from this Mac: that is what the staging key is for. A key on the firm's own Brevo account can send as office@homedirections.net to anyone. So that choice would put a production-capable key where the agent holds it.

**Evidence.** "The agent holds no ... production key". [doc:plan-v2.md section 8] "Staging gets test ones." [doc:plan-v2.md section 5, "Keys and passwords"] The runbook's own rule: "No production key is ever entered on staging." [doc:runbook-accounts.md 4.4 item 4]

**Fix.** State the constraint in the item, so the open question is asked the right way: staging's Brevo key must come from an account that cannot send as the firm, or the choice goes to Gordon as an exception he signs. The likely answer is a separate free Brevo account for staging, sending to the trap of finding 4.

**Weight: should-fix.**

### 6. Nothing forbids production's archive password from going onto staging for the restore test

**Where.** `runbook-accounts.md`, "5. Cloudflare storage", items 7 and 8. `runbook-backups.md`, section 6, steps 3 and 4 and the second "Unconfirmed".

**What is wrong.** Item 8 says "choose the archive's password", once. It does not say staging gets a different one. The restore test then needs production's archive opened on staging, and the runbook leaves open "how the archive's password is given to staging". The easy answer, entering it in staging's settings, would hand the agent the key to every production archive.

**Evidence.** The backup's encryption password is one of the keys Gordon enters in Forge, and staging gets test ones. [doc:plan-v2.md section 5, "Keys and passwords"] "It is never given to the agent." [doc:runbook-accounts.md step 5 item 8]

**Fix.** Two fixed rules, while the mechanism stays open: staging has its own archive password, different from production's; and production's password is never entered on the staging site. For the test, Gordon opens the archive himself and hands staging the opened copy.

**Weight: should-fix.**

### 7. The first push puts `main` on GitHub outside the ship script

**Where.** `runbook-accounts.md`, "1. GitHub", "What happens next".

**What is wrong.** It says the agent pushes the app "including the `main` and `staging` branches", and cites kit decision D2. D2 says the opposite: `main` moves only at ship, by one kit script, to a commit that was gated, reviewed and run on staging; the guard refuses any other push that names `main`. The overnight build has never run on a staging server. Production's site is then created from `main` in step 4, and Forge installs the branch's code on the server when a site is created.

**Evidence.** [doc:laravel-kit-spec.md D2; section 5 item 3; 8.1, the row "`main` moved only by the ship script"] Forge installs the repository at site creation. [web:laravel.com/forge/docs/sites/the-basics.md, re-read 2026-10-02]

**Fix.** Say what the first `main` is and who allows it: either a bare first commit pushed once with Gordon's recorded say as a named exception, with the app itself reaching `main` only through the first ship; or the production site is created after the first ship. The line Gordon says in step 1 should name what he is approving.

**Weight: should-fix.**

### 8. The restore test: which archive, and what it does to staging in the middle of the rehearsal

**Where.** `runbook-dress-rehearsal.md`, "Path 15" and "Path 16". `runbook-backups.md`, section 6.

**What is wrong.** Three things do not fit together.
1. Path 15 makes an archive of **staging**, then says "run the restore test from `runbook-backups.md` section 6". Section 6 is written for **production's** archive copied to staging. The two runbooks mean different archives.
2. Section 6 ends by deleting the restored data from staging. Path 16 comes after it and needs staging full of the rehearsed import. Run in the written order, Path 15 empties what Path 16 needs.
3. "Once before go-live" comes before production holds anything but three logins and Settings. Section 6 says the counts must equal "production as of last night". Before the cut that compares almost nothing.

**Evidence.** "a restore onto staging, counts compared", every quarter and once before go-live. [doc:plan-v2.md section 9] The gate "a restore that works". [doc:plan-v2.md section 7, step B] The drill runs with staging's worker and scheduler stopped, and the data is deleted afterwards. [doc:laravel-kit-spec.md 8.2]

**Fix.** Say which archive the before-go-live test uses. The useful one is staging's own archive taken after the import rehearsal, since it is the size of the real thing; production's first real restore test is then the first quarterly one. Move Path 15 to the end, after Path 16, and say what state staging is left in.

**Weight: should-fix.**

### 9. The rehearsal's clean-up leaves the real history and some 438 real letters behind

**Where.** `runbook-dress-rehearsal.md`, "Clean-up", lines C2 and C3; the note under Path 16; Set-up line S4.

**What is wrong.** The clean-up removes the invented test records and "the test Docs". Path 16 has by then loaded the firm's whole client history onto staging and converted the real letters into Google Docs in the test Google account, with their photographs held by the app. The note under Path 16 says that data "is deleted afterwards", but no clean-up line does it, names who does it, or checks it. S4 says the test Google account "owns nothing real", which stops being true at step H.

**Evidence.** Production data on staging is deleted afterwards. [doc:laravel-kit-spec.md 8.2] No file holding real rows, and nothing made from them, stays where it should not. [doc:build-handoff.md section 3, "Real data"] The letter count on the clone. [doc:build-handoff.md section 3]

**Fix.** Add clean-up lines, each with an owner and a check: the imported history removed from staging's database; the converted letters removed from the test account's Drive, its trash included; the photograph files and the old-data copy removed from the staging server; the agent confirms counts of zero. Amend S4 to say the test account holds real letters between step H and the clean-up. Deleting is Gordon's to do or to approve by name.

**Weight: should-fix.**

### 10. Path 16 would pass a system that moved only twelve months of letters

**Where.** `runbook-dress-rehearsal.md`, "Path 16", lines 16.1 to 16.3.

**What is wrong.** The decision is every letter since the last inspection on 2022-06-21. The path checks one job "from before 2022" (no Doc expected) and one "from the last year" (Doc expected). Nothing checks 2022, 2023 or 2024, which is exactly the part the decision added. Line 16.3 cites the quote that belonged to the twelve-month version. The approved plan itself still says "the last twelve months" in four places (its description, section 1, the section 2 table, and the opening of section 6), so the wrong reading is easy to build.

**Evidence.** "Decided: all of them. 'Good, let's do all the letters'". [doc:plan-v2.md section 6 step 2] [doc:phase0-brief.md, 2026-10-02 entries] The stale lines. [doc:plan-v2.md lines 7, 17, 37, 107]

**Fix.** Add two lines: a job from the second half of 2022 has a Google Doc that opens and can be edited; a consultation from before 2022-06-21 has none and its old link still shows the v3 page. Cite the 2026-10-02 decision on 16.3. Tell the orchestrating thread about the four stale plan lines; the paperwork log lists two plan contradictions and not this one.

**Weight: should-fix.**

### 11. Cutover step 6: the agent is to prepare a list that only production holds, and invoice links are not covered

**Where.** `runbook-cutover.md`, "Step 6. Point the old links", the "Who" line, item 1 and the check; "Step 4", item 5.

**What is wrong.** Two things.
1. "The agent prepares the list." The list pairs each old address with the new PDF's address, and the new addresses exist only on production after step 4. The agent cannot read production. The step does not say how the list leaves production or what is in it.
2. The plan sends the old address of each migrated letter **and invoice** to a PDF. Step 4 makes a PDF of the letter only, and the check opens letter links only. What an old invoice link shows after the cut is not stated.

**Evidence.** "Each migrated letter and invoice had a public address on v3. Those addresses are sent to the PDF made at migration". [doc:plan-v2.md section 6 step 3] The agent holds nothing that reaches production. [doc:plan-v2.md section 8]

**Fix.** Say that Gordon exports the list from production (a button or one command, to be built) and hands it to the WordPress job, and that it holds addresses only. Add the invoice: either an invoice PDF is made at migration and the old invoice link goes to it, or old invoice links are left on v3; one or the other, written down, with one invoice link in the check.

**Weight: should-fix.**

### 12. No check that production sent nothing during the import and the conversion

**Where.** `runbook-cutover.md`, "Step 3" and "Step 4", the two "Check" lines.

**What is wrong.** Production holds the live Brevo key when some 10,000 files and 438 letters with their invoices are created on it. The checks count rows and Docs. Neither looks at whether a message went out, or whether any converted Doc was opened to "anyone with the link".

**Evidence.** Sending is what sets a Doc to public view and mails the client. [doc:plan-v2.md section 5, "Sending a letter"] The risk named in the plan. [doc:plan-v2.md section 10, "A message goes to a real client"]

**Fix.** Add to each check: the app's message log on production shows no message since the day began; Brevo's own sent list shows none; and for step 4, a count of converted Docs shared by link is zero. Add the same three lines to the rehearsal of step H on staging.

**Weight: should-fix.**

### 13. The rehearsal never practises the three things the way back leans on

**Where.** `runbook-dress-rehearsal.md`, the list of paths. `runbook-cutover.md`, Part 4. `runbook-backups.md`, sections 2 and 4.

**What is wrong.** Three safety mechanisms are relied on and never seen working before the cut.
1. Going back a release in Forge. The cutover's way back uses it; both runbooks mark its steps unconfirmed.
2. A failed backup stopping a deploy. The backups runbook says the deploy script may rely on it only "once that has been seen". No step sees it.
3. An alert actually reaching Gordon: the morning check when an archive is missing, and the one-day Calendly alert. Silence is the pass signal for both, so a broken alert looks the same as a good night.

**Evidence.** "Rollback ... exact steps on Forge unconfirmed". [doc:laravel-kit-spec.md section 4 and section 15] "Prove the log works before trusting its silence". [doc:laravel-kit-spec.md section 4] Never let the pipeline fall behind silently. [doc:/Users/gordonium/Sync/Sancho/CLAUDE.md must-never 10]

**Fix.** Add a Path 17 on staging: deploy, go back a release, write the steps down; break the backup store's setting once and press Deploy, expect the deploy to stop and the old release to stay; skip one nightly archive and expect the alert on Gordon's phone or in his mail the next morning. Each closes an "unconfirmed" in two runbooks.

**Weight: should-fix.**

### 14. Several "Tell Sancho" lines cannot be said when their step is done, and no step says when the first deploy happens

**Where.** `runbook-accounts.md`, step 8 item 5 and its "Tell Sancho"; step 9.2 item 8 and step 9's "Tell Sancho"; step 6; step 9.3; "When all nine are done". `runbook-cutover.md`, Part 1, line 1.

**What is wrong.** The accounts runbook says it is everything "before v4 can go on a server", and that each step ends with a line to say. But the type map, the template link and the stamp images are set in the app's own Settings, which exist only after the app is deployed on that site. Steps 6 and 9 cannot be finished at all, because the Google credential is "do not create one yet". And nowhere in the nine steps does Gordon press Deploy for the first time, on either site. The cutover's first gate is "each 'Tell Sancho' line said", which as written can be met with no Google credential and cannot be met for step 8 until production is deployed.

**Evidence.** Settings holds the type map, the template link and the stamp images. [doc:plan-v2.md section 5, "Screens", Settings] The credential is settled at the start of the build. [doc:plan-v2.md section 5, "Google access"]

**Fix.** Split the runbook in two passes and say so at the top: pass one, accounts and keys (steps 1 to 7, 8 items 1 to 4, 9.1, 9.2 items 1 to 7); then a named step "the first deploy" for staging and for production; then pass two, "in the app's Settings" (type map, template link, stamp images, users), which is what cutover Part 1 line 8 already asks for. Give the Google credential its own numbered place-holder step so the gate cannot pass without it.

**Weight: should-fix.**

### 15. Inside step 4, two things come before what they need

**Where.** `runbook-accounts.md`, "4.1 The addresses", item 3; "4.2 Creating each site", the "Push to deploy" row; "4.3".

**What is wrong.**
1. 4.1 item 3 adds the address to the site and takes the certificate. The site is not created until 4.2.
2. Staging is created with push to deploy on. From that moment any push to `staging` deploys. 4.3's shared database path "must exist before the first deploy", and so must the environment of finding 3. Nothing tells the agent to hold its pushes, or Gordon to switch push to deploy on last.

**Evidence.** The shared path must exist before the first deploy, or each release gets a new empty database. [doc:laravel-kit-spec.md section 7 laravel-new; section 16] Push to deploy is on by default and is a toggle on the site's Deployments settings afterwards. [web:laravel.com/forge/docs/sites/deployments.md, re-read 2026-10-02]

**Fix.** Move 4.1 item 3 to after 4.2. Create staging with push to deploy **off**, finish 4.3 and 4.4, then switch it on as the last line of 4.4, and say so in the "Tell Sancho" line.

**Weight: should-fix.**

---

## Minor

### 16. When v4 is down, the redirected old links are down too

**Where.** `runbook-cutover.md`, Part 4, "If v4 fails on a working day".

**What is wrong.** After step 6 the old addresses of the migrated letters lead to PDFs served by v4. On a day v4 fails, a client opening an old link from 2022 onward gets an error, although the original is still on v3. The table does not mention it.

**Evidence.** The redirect lives on v3 and points at v4's PDF; the original stays on v3. [doc:plan-v2.md section 6 step 3; section 10]

**Fix.** One more row: "If v4 will be down for more than a day: switch the redirects off in v3's Redirection plugin (a change on the live site, Gordon's, through the WordPress kit); the old links show the v3 pages again."

**Weight: minor.**

### 17. Writing Gordon cannot follow by ear

**Where.** `runbook-accounts.md`: the paragraph "Where a key goes"; 4.1 item 3; the 4.2 table and note 2; 4.3 items 2, 5; 4.4 items 3, 4; 4.5 items 1, 3, 5; step 5 item 6; step 7 items 6, 7.

**What is wrong.**
1. **Steps that are not steps.** 4.3 item 2 ("The stored files") states a fact; the action ("add `storage`") is inside an "Unconfirmed" bullet. 4.4 items 3 and 4, and 4.5 items 1 and 3, are rules with no action. Step 7 items 6 and 7 are open questions numbered as steps. A listener cannot tell which numbers he must do something for.
2. **Words used with no meaning given:** queue worker (4.3 item 5: what it is for is never said), zero-downtime deployments, commit ID, fingerprint, endpoint and "region auto" (step 5 item 6), custom domain, DNS check, and two commands spelled out in code in the opening section.
3. **One passage needs re-reading:** the "Unconfirmed" under 4.2 note 2 (two Forge pages that disagree about which credential fetches the code). It asks nothing of Gordon and sits in the middle of his steps.

**Evidence.** Plain language, jargon defined, conclusion first. [doc:laravel-kit-spec.md section 3] Gordon dictates and listens. [doc:/Users/gordonium/Sync/Sancho/CLAUDE.md, "Who you are"]

**Fix.** In each numbered list keep only lines that begin with a verb Gordon does. Move rules to a short "Rules for this site" list above the steps, and open questions that need nothing from him to a list at the foot of each section headed "Sancho settles these". Give each of the listed words one plain clause the first time it appears (for example: "the queue worker, the background process that sends the mail and makes the PDFs").

**Weight: minor.**

### 18. Two citations whose source does not say it

**Where.** `runbook-dress-rehearsal.md`, line 6.6. `runbook-accounts.md`, step 8, the type-map table, third row.

**What is wrong.**
1. Line 6.6 (the system sends nothing when a client cancels in Calendly) cites phase0 Q6. Q6 is about deleting a file in v4 and letting Calendly send its own notice. The cancellation decision is Q5, and Q5 says nothing about mail. The expectation is sensible; the source for it is the absence of any cancellation message in the plan.
2. The $475 hourly rate cites plan-v2 section 5, which gives no price. The price is in requirements, business context, which the row also cites.

**Evidence.** [doc:phase0-brief.md, "Plan questions 4 onward", Q5 and Q6] [doc:plan-v2.md section 5] [doc:requirements.md, "Business context"]

**Fix.** On 6.6 cite the plan's list of message kinds (invoice, paid copy, letter) and mark the line "Sancho's reading". On the table row keep the requirements citation for the price and plan-v2 only for "entered by hand".

**Weight: minor.**

### 19. Three "Unconfirmed" markers that a document already settles

**Where and evidence.**
1. `runbook-backups.md`, section 5: "whether both places follow the same schedule". The plan gives one retention in the same sentence as the two places. [doc:plan-v2.md section 9, first bullet] Settled: the same on both.
2. `runbook-accounts.md`, 4.3 item 2: "whether Forge shares the `storage` folder by itself". The Forge page the runbook cites says the settings file is the only path shared by default, and lists storage folders as something to add. [web:laravel.com/forge/docs/sites/deployments.md, re-read 2026-10-02] Settled: add it. It should be a plain step.
3. `runbook-dress-rehearsal.md`, Clean-up: "how a test record is removed from staging". Half settled: no tinker and no one-off scripts on staging; every data change is a committed, reviewed migration or command. [doc:laravel-kit-spec.md section 6, item 5] So it is a committed clean-up command or a rebuilt staging database, never a hand edit.

**Fix.** Replace each marker with the settled statement and its source.

**Weight: minor.**

### 20. Three gaps no runbook covers

**Where.** `runbook-cutover.md`, Part 1 table; `runbook-accounts.md`, step 9.2 items 3 and 8; no runbook, for the third.

**What is wrong.**
1. The how-tos for Peter and Maria Pia are not a line in "all of this must be true before the day". With no trial period they are the only training, and they are in tonight's scope. [doc:build-handoff.md section 2 item 6] [doc:plan-v2.md section 10, the hard-cutover risk]
2. The runbook asks for four image files (letterhead, signature, two stamps) and says where none of them is. The documents do: the letterhead file in the Home Directions plugin, the signature in the site's uploads, and the two stamp files by name. [doc:current-system.md, "How a job flows", items 5 and 7] [doc:survey-hdonline-home-directions.md, the stamp passage near line 228]
3. The plan's monthly upkeep "from a checklist" (system updates, PHP patch releases, a reboot) has no checklist. The first one falls due a month after the server is made, which is probably before the cut. [doc:plan-v2.md section 9] [doc:laravel-kit-spec.md 9.2, the monthly row]

**Fix.** Add the how-tos as Part 1 line 12. Name the four files and where each is. Note the monthly checklist as owed, in stage W2 or by the kit track.

**Weight: minor.**

### 21. The backup before a deploy: two sources differ, and Forge's ten-minute limit is not mentioned

**Where.** `runbook-backups.md`, the top table row 2, and section 2.

**What is wrong.** The runbook says the whole archive (database and stored PDFs) goes to both places before a deploy. The kit spec says the deploy script takes "the database backup" first. The hosting decision says "the same archive". The runbook follows one source without noting the other. A Forge deploy fails by itself at ten minutes, and the same deploy also builds the app's assets on the server; a full archive of every stored PDF to two stores inside that limit gets harder each year.

**Evidence.** [doc:laravel-kit-spec.md section 7, laravel-ship, last paragraph; D15] [doc:hosting-options.md Decision, the schedule table, second row] Deploys are limited to ten minutes. [doc:hosting-claims.md, Forge deployments] [doc:hosting-options.md, "The pick, in full"]

**Fix.** Note the difference and put it to the app track: database only before a deploy (the PDFs do not change in a deploy), full archive nightly. Mention the ten-minute limit beside it.

**Weight: minor.**

### 22. "The backup times are stated against UTC", but no time is stated

**Where.** `runbook-accounts.md`, step 3 item 5. `runbook-backups.md`, section 1, first "Unconfirmed".

**What is wrong.** The accounts runbook says the backup times in the backups runbook are stated against the server's clock. The backups runbook states no time; the hour is unconfirmed. The app also has its own time-zone setting, so "every night" and "every morning" could mean the server's clock or the firm's.

**Evidence.** [doc:runbook-backups.md section 1] The setting name. [file:hdonline-v4/.env.example, names only]

**Fix.** Drop the sentence from step 3, or state the hour in both runbooks once it is chosen, with the clock it is measured on (the firm is in Connecticut; Gordon is travelling).

**Weight: minor.**

### 23. Small practical slips in the rehearsal script

**Where.** `runbook-dress-rehearsal.md`, "The test people and places"; lines 9.10 and 11.3.

**What is wrong.**
1. Clients are matched on email first, and the script needs T1, T2, T3 and the "truly new client" of line 3.5 to be four different people. It says only "every email address used is one of your own". Gordon needs four distinct addresses and the script does not give them.
2. Line 9.10 expects "three messages out". By then S5 has sent one, and paths 4 to 6 have produced Calendly's own notices to the same inbox.
3. Line 11.3 searches "this month" for bookings made "next week". Run in the last week of a month, it fails for no fault of the app.

**Evidence.** Clients match on email first. [doc:plan-v2.md section 4, Rules]

**Fix.** Give four labelled addresses in the test table (the same mailbox with a different tag after a plus sign, if his mail allows it). Change 9.10 to "three messages for this file". Change 11.3 to search the month the test bookings fall in.

**Weight: minor.**

---

## Citations opened and checked

Sixty-four citations to documents on disk were opened at the cited section. Sixty-one say what the runbook says they say. Two do not; they are finding 18. One supports the opposite of its sentence (accounts step 1, "What happens next", citing D2); that is finding 7.

| Runbook | Citation checked | Verdict |
|---|---|---|
| accounts | Monthly cost $27.60 [hosting-options Decision] | holds |
| accounts | Hobby allows one server of our own [hosting-claims, Forge plans] | holds |
| accounts | 2 GB, 1 processor, 50 GB, $12 [hosting-claims, DigitalOcean Basic droplets] | holds |
| accounts | Ubuntu 26.04 on every provider [hosting-claims] | holds |
| accounts | NYC1, NYC2, NYC3 [hosting-claims] | holds |
| accounts | Daily backups cost 30 percent [hosting-claims; hosting-options] | holds |
| accounts | Organisation keys copied to every server, not removed [hosting-claims; boundary 4] | holds |
| accounts | "yeah, I'll try" on keeping Forge out of the driven browser [phase0-brief] | holds |
| accounts | Kit repository name is Sancho's suggestion; Free plan; private [kit spec D4, D5] | holds |
| accounts | Names never values [kit spec section 7, laravel-ship step 4] | holds |
| accounts | Shared database path; empty database if missing [kit spec section 7; section 16] | holds |
| accounts | One deploy script in the repo [kit spec section 4] | holds |
| accounts | Own app key; no environment file copied; ask before editing [kit spec 8.2; section 6 items 5, 10] | holds |
| accounts | Scheduler every minute; worker restarted [hosting-claims, Forge queue and scheduler] | holds |
| accounts | Hostname unproxied; DNS at Cloudflare [hosting-options; phase0-brief Q3] | holds |
| accounts | `app.homedirections.net` only in the superseded draft [plan.md section 9] | holds |
| accounts | Storage free to 10 GB; S3 address and region [hosting-claims, R2] | holds |
| accounts | Whether a card is needed is open [hosting-claims, Cloudflare open questions] | holds |
| accounts | Archive password name [laravel-tooling-research, spatie/laravel-backup] | holds |
| accounts | Brevo authenticated in DNS; "90% sure" [phase0-brief Q2, Q8] | holds |
| accounts | Mail test and Gmail's change [plan-v2 section 11 item 4; phase0-brief] | holds |
| accounts | Calendly paid, two types, address required, booking page [phase0-brief Q4] | holds |
| accounts | $875 and $1,250 [phase0-brief Q4; requirements, business context] | holds |
| accounts | $475 an hour [plan-v2 section 5] | **does not say it** (requirements does) |
| accounts | Template draft, its images, the wording and licence lines [phase0-brief, "The letter template"] | holds |
| accounts | Signature image is v3's [current-system, "How a job flows" item 7] | holds |
| accounts | Address block with a name alone [build-handoff section 3] | holds |
| accounts | Backup credential "write to one folder and read nothing" [kit spec 8.2] | holds |
| accounts | Fingerprints recorded; preflight [kit spec section 5 item 7; section 12] | holds |
| accounts | Agent pushes `main` [kit spec D2] | **contradicts** (finding 7) |
| backups | Schedule, retention, both places [plan-v2 section 9; hosting-options Decision] | holds |
| backups | The tool: SQLite, several stores, password, no restore command [laravel-tooling-research line 87] | holds |
| backups | Example times 01:00 and 01:30 [laravel-tooling-research] | holds |
| backups | "a backup never restored is unproven" [laravel-tooling-research] | holds |
| backups | Extra program for SQLite not stated [laravel-tooling-research, open items] | holds |
| backups | $0.15 a month per further 10 GB [hosting-claims] | holds |
| backups | Deploy takes the backup first and stops if it fails [kit spec, laravel-ship] | holds |
| backups | Restore drill is Gordon's to start; worker and scheduler stopped; data deleted [kit spec 8.2; 13] | holds |
| backups | Quarterly row; Sancho creates no task [kit spec 9.2; 9.4] | holds |
| backups | The first draft used a push notice through Sancho [plan.md section 9] | holds |
| backups | Forge keeps the last four releases [hosting-claims; web] | holds |
| cutover | Gordon's "deep end" quote [phase0-brief; plan-v2 section 6 step 5] | holds |
| cutover | 10,212, 9,442 and 770 [plan-v2 section 6 step 1] | holds |
| cutover | Two to three jobs a week [plan-v2 section 4] | holds |
| cutover | Test records skipped, counted, listed by ID [build-handoff section 3] | holds |
| cutover | Safe to run twice, logged, dry run [kit spec section 4] | holds |
| cutover | 438 letters; three tables with text; 298 of 304 [build-handoff section 3] | holds |
| cutover | Redirection plugin installed [census-2026-10-01, plugin list] | holds |
| cutover | Public addresses since 2026-02 [requirements, "Facts that constrain the design"] | holds |
| cutover | v3's appointments come from a hand-filled form [current-system, item 1] | holds |
| cutover | v2 is read, never operated [handoff.md in the project folder] | holds |
| cutover | Twenty letters; the stale "ten-letter" line [plan-v2 sections 6, 7, 10] | holds |
| cutover | Step J against section 8 [plan-v2; kit spec 8.1] | holds; the conflict is real |
| rehearsal | Staging commit, migrations, health address [kit spec, laravel-edit step 7] | holds |
| rehearsal | `CLAUDE TEMP TEST` and removal checked [kit spec section 4] | holds |
| rehearsal | Login rate limited [kit spec section 4, security] | holds |
| rehearsal | Invoice made at file creation [requirements R4.1] | holds |
| rehearsal | Settings change applies to new invoices only [requirements R4.2] | holds |
| rehearsal | Double confirmation on delete [requirements R2.6] | holds |
| rehearsal | Search by client, address, month [requirements R6.2] | holds |
| rehearsal | Cancelled file leaves the list, stays findable; Doc to trash if untouched [phase0-brief Q5] | holds |
| rehearsal | System sends nothing on a client's cancellation [phase0-brief Q6] | **does not say it** (finding 18) |
| rehearsal | "Also cancel it in Calendly", ticked by default [phase0-brief Q6] | holds |
| rehearsal | Change history folded shut [phase0-brief, 2026-10-02] | holds |

**Vendor pages re-read tonight** (public pages, text only, nothing signed in to). Forge's came back whole: `sites/deployments.md`, `sites/commands.md`, `ssh.md`, `sites/the-basics.md`, `sites/environment-variables.md`. Every Forge claim checked against them holds: push to deploy on by default and switched in "Advanced settings"; zero-downtime only at creation; four releases kept; the SQLite shared path as written; the three special lines; the health check and deploy hook where the runbook says; failure emails on by default; the five-minute limit and no typed input on Commands; organisation keys copied and not removed; a key can be given to one isolated site's user; the on-forge.com address runs through Cloudflare. The one thing those pages say that the runbook missed is finding 3. Three more came back as a summary, so they are one reader's reading: Calendly's webhook help page (the six plan names, set-up through the developer interface), Cloudflare's R2 token page (four permissions, bucket limit, the secret shown once), DigitalOcean's backup features page (same datacenter, a four-hour window that can be chosen, no retention count). All three agree with the runbooks.

## What was not checked

The Brevo pages, the spatie retention page, Forge's pages for domains, network, queues, scheduler, server types, user isolation, source control and repository access, and DigitalOcean's pricing page were not re-read. No command was run on any server, and nothing in either code repository was changed. The app's example settings file was read for its setting names only; no value from it is in this review.
