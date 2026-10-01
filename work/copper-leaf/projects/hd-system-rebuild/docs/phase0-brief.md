---
name: Home Directions v4 Phase 0 brief
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Questions 1 to 3 of the plan (stack, Google Workspace, hosting) with the evidence gathered 2026-10-01, Sancho's pick for each, what would flip the pick, corrections to the draft plan, and the census status
sources: ["[doc:plan.md]", "[doc:requirements.md]", "[doc:current-system.md]", "[doc:survey-hdonline.md]", "[doc:~/Dev/clc-plugins/CLAUDE.md]", "[dns:homedirections.net 2026-10-01]", "[web:sitedistrict.com 2026-10-01]", "[web:laravel.com 2026-10-01]", "[web:knowledge.workspace.google.com 2026-10-01]"]
status: Q1 (stack) and Q2 (Workspace) decided by Gordon 2026-10-01; Q3 (hosting) open; the Q1 to Q3 sections below are as first written, with dated supersede notes where later work changed them
---
# Phase 0 brief: questions 1 to 3

Written 2026-10-01 19:30 CEST by the HD thread. The picks are Sancho's. Gordon decides; decisions get recorded at the bottom when they land.

## Q1. Stack: Laravel, or WordPress for the kit's sake?

**Pick: Laravel (plan option B), with three costs the draft undersold stated out loud.**

Why:
- Nothing from the old plugins carries forward. Notes library, compile, sections, data sheets, brokers and attorneys, LOCAL mode, Gravity Forms intake and ACF are all dropped. [doc:plan.md §1] [doc:current-system.md] Staying on WordPress therefore preserves no code, only the login screen and the habit.
- What v4 actually is: two deduplicated tables with an audit trail, plus integrations (Calendly webhook, Google Docs and Drive, a mail provider with delivery events, queued jobs, PDF). [doc:requirements.md R1, R2.1, R2.3, R3, R5] WordPress helps with none of those; a framework with migrations, foreign keys, queues and mail built in does.
- Tests must be automatic (must-never 9). [doc:CLAUDE.md] Laravel's fakes for mail, queue and outbound HTTP let the Google, Calendly and mail paths be tested without the network; the WordPress test harness makes that awkward. [doc:plan.md §2]
- Inbound webhooks on SiteDistrict sit behind bot protection that "can return 429 to automated HTTP requests". [doc:~/Dev/clc-plugins/CLAUDE.md §10] Whether Calendly's calls would be blocked is unconfirmed, but it is a risk only the WordPress option carries.
- The old system exposed every post type, contacts included, as public and on the REST API. [doc:survey-hdonline.md §348, line 101] A small app with no plugin ecosystem has a smaller surface. (Corrected 2026-10-01 late: that sentence overstated its source. By the code, every post type is registered public and on the REST API, so contact titles, which are client names, may be readable without login; field values are not exposed, and front-end pages other than reports and invoices require login. Unconfirmed on the live site. [doc:survey-hdonline.md line 101; §9 Security item 5, line 348])
- Gordon's own lean on 09-29: "might still be WordPress and thinking not". [rec_8d15ed467e 2026-09-29 00:04:53]

The costs:
1. **The kit does not transfer.** plugin-edit, plugin-review, plugin-ship, the SiteDistrict live-site guard and the staging conventions are WordPress-only. [doc:~/Dev/clc-plugins/CLAUDE.md §9 to §11] v4 needs its own CLAUDE.md, its own deploy and its own review chain. The plan says so in one clause; it is real setup work in step 1.
2. **An upgrade clock.** Each Laravel major gets bug fixes for 18 months and security fixes for two years; Laravel 13 (released 2026-03-17, PHP 8.3 minimum) has security fixes until 2028-03-17. [web:laravel.com/docs/13.x/releases via search 2026-10-01] [web:laravel-news.com/laravel-releases] A WordPress plugin with its own tables has no such clock. v4 therefore carries a standing upgrade job roughly every two years, forever. (**Superseded 2026-10-01 late: the real cadence is one Laravel upgrade per app every year**, because a major cannot be skipped inside the two-year security window. [doc:laravel-kit-spec.md §9.1] Gordon accepted this cost on the two-year figure; he has been told.)
3. **Leah and Astra cannot maintain it.** The plan's own table says "Gordon with Claude Code; not Leah". [doc:plan.md §2]

What would flip the pick to WordPress (option A, custom tables, no ACF, no Gravity Forms): Gordon wanting Leah to be able to maintain it, or refusing a second host. If neither is true, Laravel.

Amendments to the draft's concrete line, whichever way this goes: **Laravel 13, not 12** (12 was current when the draft's knowledge was; 13 is current now). [web:laravel-news.com/laravel-13-released] PHP 8.4. (Superseded: PHP 8.5; 8.4 leaves active support on 2026-12-31. [doc:laravel-kit-spec.md D9]) SQLite stands if Q3 lands on a server with a disk; see Q3.

## Q2. Google Workspace on homedirections.net: yes or no?

**The DNS says it is already there. Pick: yes, use it; do not buy anything until the edition is known.**

Evidence, read from public DNS on 2026-10-01 19:15 CEST:
- MX for homedirections.net is Google's five `aspmx.l.google.com` hosts. [dns:homedirections.net MX]
- SPF is `v=spf1 include:_spf.google.com ~all`. [dns:homedirections.net TXT]
- A Google DKIM key is published at `google._domainkey`. [dns:google._domainkey.homedirections.net TXT] (Not a wildcard: a random name returns nothing.)
- Two `google-site-verification` records. [dns:homedirections.net TXT]

So mail for the domain is hosted by Google, which means a Workspace account (or a legacy free G Suite account) exists. What DNS cannot say, and Gordon or the Admin console can: **which edition**, **who the super admin is**, and **which mailboxes exist** (is there a `peter@homedirections.net` that Peter actually reads?). Unconfirmed, all three. The invoices name a consumer address, `homedirectionsinc@gmail.com`, for Zelle [doc:current-system.md, How a job flows, item 8; the literal address is at hdonline-home-directions/single-hdo_invoices.php:173], so there are at least two Google identities in play and the plan must name the one that owns the letters.

On the shared drive: Google's own edition comparison lists shared drives in all three Business editions, Starter included [web:knowledge.workspace.google.com/admin/getting-started/editions/compare-business-editions, read 2026-10-01]; two reseller pages say Starter has none [web:googleworkspaceresellers.com, web:fes.cloud]. Google's page is the better source; the Admin console is the proof. A legacy free edition would not have them (unconfirmed).

Pick in full: service account with domain-wide delegation acting as Peter's Workspace user, letters in a shared drive if the edition has one, otherwise in a folder in Peter's My Drive shared with Mom. For a one-person firm the shared drive is a nicety, not a reason to upgrade. The plan's fallback (OAuth as Peter, `drive.file` scope) stays as the fallback. [doc:plan.md §4]

A second finding that belongs to question 8, not this one: **Brevo is already authenticated on the domain** (two `brevo-code` TXT records, a `brevo1._domainkey` CNAME, and DMARC `p=none` reporting to `rua@dmarc.brevo.com`). [dns:homedirections.net TXT, _dmarc, brevo1._domainkey] What sends through Brevo today is unconfirmed (the website's mail is the likely answer). The plan picks Postmark without knowing a transactional sender was already set up; revisit at question 8.

## Q3. Hosting

**Pick: Laravel Forge (Hobby) managing one small VPS; SiteDistrict stays WordPress-only. Only relevant if Q1 is Laravel.** (Superseded 2026-10-01 late by `hosting-options.md`: two servers, staging and production apart, in an account Gordon owns.)

Evidence:
- SiteDistrict describes itself as WordPress hosting only: "Our platform is for building & hosting WordPress sites for real people." No mention of other PHP apps. [web:sitedistrict.com 2026-10-01] The plan's question "does SiteDistrict run a non-WordPress PHP app" is, by their own page, no; unconfirmed with their support.
- The public site, `reports.homedirections.net` and the dev clone all resolve to the same address, 99.83.157.227 (Amazon). [dns 2026-10-01] The three hosts checked are all on SiteDistrict. (Corrected: the draft said "the whole current estate"; v2 is live at hdonline.homedirections.net and where it is hosted is not known.) `app.homedirections.net` does not exist yet. [dns 2026-10-01] DNS is at Cloudflare. [dns:homedirections.net NS]
- Forge Hobby is $12 a month and manages servers billed separately by the provider. [web:laravel.com/forge/pricing via search 2026-10-01] A small VPS price is not verified here; unconfirmed.
- Laravel Cloud Starter is $5 a month plus usage, with the scheduler and managed queues included and scale-to-zero; it has no persistent disk, so SQLite is out there and the database becomes managed MySQL or Postgres. [web:laravel.com/cloud/pricing via search 2026-10-01]

Why Forge and a VPS: the plan's data story is one SQLite file copied nightly to Drive, portable without the app [doc:plan.md §2, §11 bus factor]; that needs a disk. Forge gives deploy on push, the queue worker, the scheduler, certificates and security patching without hand-built server work, at a fixed cost. No bot-protection layer in front of the Calendly and mail webhooks.

What would flip it to Laravel Cloud: Gordon preferring never to own a server. The price is SQLite (managed database instead, nightly dump to Drive instead of a file copy).

Not decided here: which VPS provider and region, and whether Gordon already has a Forge account or a server (unknown; no source on disk).

## Corrections to the draft plan (recorded, not overwritten)

1. Plan §2 "Laravel 12, PHP 8.3": Laravel 13 has been current since 2026-03-17. [web:laravel-news.com/laravel-13-released]
2. Plan §12 question 2 asks whether to add Workspace: mail for the domain is already on Google. [dns 2026-10-01] The real questions are edition, admin, and which user owns the letters.
3. Plan §12 question 3 asks whether SiteDistrict runs a non-WordPress app: its own site says WordPress only. [web:sitedistrict.com 2026-10-01]
4. Plan §6 picks Postmark without the fact that Brevo is already set up on the domain. [dns 2026-10-01]
5. The inline question numbers in plan §4, §7, §8 and §11 do not match the list in §12 (Workspace is called "question 4" inline and is 2 in the list; Calendly plan "5" is 4; booking-form address "6" is inside 4; Calendly cancel via API "7" is 6; link or PDF "8" is 7). The §12 list is the authority; the inline numbers get fixed when the plan is next revised.

## Census status

(Superseded 2026-10-01 late: the census ran; see `census-2026-10-01.md` and `census-part2-2026-10-01.md`.) The Chrome tab is on the dev clone's login page (`hdonline-sancho.sitedistrict.com/wp-login.php`), waiting for Gordon to log in. [chrome 2026-10-01 19:20 CEST] Sancho does not type credentials. Once in, the census is read-only: admin list screens and REST `GET`s for counts by post type, appointment type and year, compiled reports versus consult letters, invoices and paid flags, contacts by type, properties, notes, and which fields are actually filled (plan §10.1). Nothing is saved, edited or clicked that changes state.

## Decisions

Gordon, 2026-10-01 evening, in the HD thread, answering the Q1 walk-through (pick plus three costs):

- **Q1 decided: Laravel.** "i still agree with your decision." [gordon 2026-10-01]
- **New requirement, stated with the decision:** "The new system's db also needs to house all the legacy data going back to the early '90s so we may need more tables". [gordon 2026-10-01] Recorded as R7.8 in `requirements.md`; the data model in plan §3 grows in Phase 2 and must be shaped for it in Phase 1.
- **Cost 1 (the kit does not transfer): build one.** "let's start building a similar skill harness for Laravel and perpetually compare the two to cross-apply improvements and lessons." [gordon 2026-10-01] Spec: `laravel-kit-spec.md` (this folder, until it has a home of its own).
- **Cost 2 (the upgrade clock): accepted.** "No problem on 2, we just need to build an updates schedule for this and all future Laravel projects, I expect there will be more." [gordon 2026-10-01] The schedule is part of the kit spec, not of this one app.
- **Cost 3 (Leah and Astra cannot maintain it): accepted.** "No problem on 3." [gordon 2026-10-01]
- **Q3 hosting: open, with a question.** "Where should we host it? Can we do it on Cloudflare Edge? Otherwise, we need a task to shop hosting options." [gordon 2026-10-01] Sancho shops it now (`hosting-options.md`); no task is created for Gordon (must-never 2).
- **Q2 Workspace: not yet walked.** Sancho reads Gordon's "2" and "3" as the numbered costs under Q1, not as plan questions 2 and 3, because the replies match the costs line for line. Said to Gordon in the reply; if that reading is wrong, this entry is superseded. (Superseded the same evening by the next entry: Q2 walked and answered.)
- **Q2 decided: build on the existing Workspace.** "Yes, we have Google Workspace Business Starter. office@homedirections.net is the Super Admin." [gordon 2026-10-01] Edition: Business Starter. Super admin: office@homedirections.net. Still open: which mailbox Peter works in and which Workspace user owns the letters (asked, not yet answered); whether Business Starter has shared drives is settled by looking in that account's Drive, not by the web pages that disagree.
- **Census: unblocked.** "Chrome tab is logged in." [gordon 2026-10-01] Part 1 done the same evening: `census-2026-10-01.md`. Part 2 needs database access: `census-part2-queries.md`.
- **Q3 hosting: researched, pick made, not yet decided by Gordon.** Cloudflare's edge cannot host it (no PHP on Workers; no persistent disk on Containers). Sancho's pick is Laravel Forge with a production server in an account Gordon owns, about $34 a month. `hosting-options.md`, with the per-claim record in `hosting-claims.md`. The Q3 section above said "Forge and one small VPS"; the pick is now two servers (staging and production apart), and PHP 8.5 not 8.4. Superseded by `hosting-options.md`.
- **Gordon, 2026-10-01 late, second round** [gordon 2026-10-01]:
  - **Cost is not the constraint; simplicity is.** "Do we really need Laravel Forge, or can we just 'dev in place' at a staging address directly in Digital Ocean? The cost isn't an issue, just looking for simplicity over complexity." Hosting stays open; answered in `hosting-options.md`, section "Forge, or a bare server".
  - **The legacy lineage, in his words:** the WordPress system is "v3". "v2 which Grayson built" is live at `hdonline.homedirections.net/hdonline/` (he gave the address with its access parameter). "v1 which we call 'legacy' which I think is no longer live anywhere, but we might be able to re-assemble from backups." "Before that, there was an MS Access database for 'the booking system' and a pile of Word files." And: "the bulk of the legacy data is in WP, but there is even more legacy data - fragmented and fractured - that needs to be audited and merged in." This answers plan question 14 (Grayson is a person, the builder of v2).
  - **The data loss, in his words:** "Circa 2015, as a young programmer, Grayson wrote the worlds worst bug - a 'delete note-number-x' with NEITHER a reportID or a LIMIT 1, so each time a note got unchecked in any report, it got deleted from EVERY report. Then one day I asked leah to go check and uncheck all notes to test something else and we blew away nearly anything. ... After my efforts, I think we sustained an ~3% total data loss, but I'm hoping we can actually audit ALL the backups ... reduce that loss after all these years." So the loss is note selections inside v2 reports, around 2015. It is **not** the 2008 gap the census found; that gap is a separate, unexplained thing. `census-2026-10-01.md` finding 3 is superseded accordingly.
  - **SSH:** "You have SSH access to host-2 on SD, right? That's where you'll find the staging clone to dig deeper." "Go ahead and census. (And why did you have to ask for my permission on that?)" Census part 2 is run from this thread, read-only.
  - **The WordPress guard:** "Go ahead and fix the WP guard hole." This is Gordon's say for a change in `~/Dev/clc-plugins/bin/`, which the handoff reserves to him and which this thread's opening brief had put off limits.
  - **Mail:** "Peter uses homedirections@gmail.com most often, but I think that box checks office@homedirections.net, so sending from there should work the way we want. Let's send some test emails to confirm." So the sending address is office@homedirections.net (not peter@, as the plan drafted). Unconfirmed by Gordon's own "I think": that the Gmail box collects office@. Also open: the invoices name `homedirectionsinc@gmail.com` for Zelle [doc:current-system.md, How a job flows, item 8], which is not the address Gordon typed; whether these are two boxes or a slip is not known. A reason to test rather than assume: Gmail stopped fetching mail from other accounts by POP ("Check mail from other accounts") in January 2026. [web:theregister.com/2026/01/05/gmail_dropping_pop3/; web:techrepublic.com/article/news-gmail-ends-gmailify-pop3/; secondary sources] If the Gmail box collected office@ that way, it no longer does; if office@ forwards to it, it still does. Sancho has no mail tool and holds no mail credentials, so the test messages are Gordon's or Peter's to send; the three checks are in the reply of 2026-10-01 late and belong in plan question 8.
- **Gordon, 2026-10-01 night, third round** [gordon 2026-10-01]:
  - **The v2 tables in WordPress are not to be trusted as complete.** "even those tables in WP are suspect. Good data, but probably incomplete and maybe a little messy. We should dig all the way back into original MS Access database backups if we can." So the source of truth for the old jobs is the oldest surviving source, not the newest copy; `REPORTS` and `CONTACTS` in the clone are one witness among several. Recorded as R7.11.
  - **Forge: liked.** "Forge sounds awesome, thanks for explaining." Taken as yes to Forge; how many servers is still open (he asked why two).
- **Gordon, 2026-10-01 night, fourth round** [gordon 2026-10-01]:
  - **Q3 hosting decided: Forge, one machine.** "one machine is fine under one condition: we need a good schedule of automatic backups that get stored somewhere else. Otherwise, the risks are ok. This is a very infrequently used system by one person, my dad, so little downtimes are likely never going to be noticed, let alone a big problem." And: "For more robust client systems in the future, we'll probably expand to two." The backup schedule is in `hosting-options.md`.
  - **Phase order, restated as a correction to this thread:** "Do you remember me saying the legacy data part of the project is Phase 2? We should be focusing on building the new system and cutting over from v3. Then we can backfill the historic data and files". Sancho had drifted into Phase 2 work (the legacy inventory and audit proposal). Phase 1 is the build and the cutover from v3; the handoff now carries the rule.
  - **Legacy scope for Phase 2, when it comes:** "No need to go into the older MSACCESS backups, the most recent will do - that's not the era in which the problems happened. v1 is probably fine, but let's go through 'em anyway. v2 is what needs to go under a microscope to stitch back together everything we can. Let's do that later on a dedicated thread with maximum resources. You'll have to audit the Word Files as we attach them to client records and generate PDFs from them."
  - **The 2008 gap:** "2008 is probably when v1 launched, replacing the Access DB." Gordon's recollection, marked probable by him.
  - **mdbtools:** "Go for install." Installed (see `legacy-sources.md` for what it could and could not open).
- **Gordon, 2026-10-01 night, fifth round** [gordon 2026-10-01]:
  - **Kit decision D1: the Readability Rule is WordPress-only.** "Great question - those rules should apply to WP only. Let's go whole-hog elegant inside Laravel, as I never intend to read the code. That's all you, boo."
  - **Before any real code is written, Gordon is warned.** "please warn me before you start writing any real code, so I can increase your Effort Level to Ultracode first, AND we'll want to proactively compact or just start a new 'actually write it' thread separate from this planning thread."
  - **Laravel Herd:** "Go for install" (kit decision D17).
- **Laravel kit: spec drafted** (`laravel-kit-spec.md`), with the WordPress kit mapped item by item (`wp-kit-map.md`) and the tooling and calendar research (`laravel-tooling-research.md`). Twelve decisions in it are Gordon's.
