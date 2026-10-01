---
name: Home Directions v4 runbook, backups
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: How v4's backups are set up and checked: the nightly encrypted archive to Cloudflare storage and to the firm's Google Drive, the backup before a deploy that changes the database, DigitalOcean's daily backup of the machine, the morning check, the retention (14 daily, 8 weekly, 12 monthly, yearly) and the restore test in its two kinds (staging's own archive before go-live, production's archive every quarter); who does each part, the two fixed rules about the archive passwords, what is still unconfirmed
sources: ["[doc:plan-v2.md section 9]", "[doc:hosting-options.md Decision]", "[doc:laravel-kit-spec.md 8.2, 9.2, 13, 15]", "[doc:laravel-tooling-research.md]", "[doc:hosting-claims.md]", "[doc:runbook-accounts.md]", "[doc:runbook-dress-rehearsal.md]", "[doc:reviews/paperwork-W1.md]", "[gordon 2026-10-01]", "[web: vendor documentation pages read 2026-10-02, cited where used]"]
status: written 2026-10-02 overnight by the paperwork track (stage W1); reviewed the same night (reviews/paperwork-W1.md) and fixed by a third agent, see "W1 fixes" in build-log-paperwork.md; nothing in it is set up; the backup code was not built when this was written, so every step that depends on it is marked
---
# Runbook: backups

**The short version.** Five things run by themselves. One thing you start. Automatic backups stored somewhere else were your condition for one server. [gordon 2026-10-01] [doc:hosting-options.md Decision]

| # | What | When | Where it goes | How you know it worked |
|---|---|---|---|---|
| 1 | The database and the stored PDFs, in one encrypted archive | every night | Cloudflare storage **and** a folder in the firm's Google Drive | a new file in each place every morning; the Connections panel |
| 2 | The same archive | before every deploy that changes the database | the same two places | the deploy stops if it fails |
| 3 | The whole machine | daily, by DigitalOcean | DigitalOcean, same datacenter | DigitalOcean's panel |
| 4 | A check that last night's archive arrived | every morning | an alert to you when it did not | silence means it arrived |
| 5 | Old archives thinned out | with the nightly run | both places | 14 daily, 8 weekly, 12 monthly, then one a year |
| 6 | A restore test on staging, counts compared | every quarter, and once before go-live | staging | the result is written down |

[doc:plan-v2.md section 9] [doc:hosting-options.md Decision, "The backup schedule"]

Rows 1 to 5 run unattended. Row 6 is yours to start. [doc:laravel-kit-spec.md 8.2 and section 13]

**What is not in the archive.** The letters themselves are Google Docs and are not in it. Each sent letter's PDF is. [doc:plan-v2.md section 9] A copy of the letters folder outside Google is a separate question the plan has not answered. [doc:hosting-options.md Decision]

---

## 1. The nightly archive, to two places

**What it is.** One encrypted file holding a consistent copy of the database and the stored PDFs. [doc:hosting-options.md Decision] [doc:plan-v2.md section 9]

**Where it goes.** Two places, both every night. Cloudflare storage is a third company, apart from DigitalOcean and Google. The Drive folder is the copy you and Peter can see without any tool. [doc:hosting-options.md Decision] [gordon 2026-10-01: "could we do both?? I love redundancy"]

**The tool.** The research found one that does this: it makes one archive of chosen folders and the database, handles SQLite, writes to several storage places at once, can encrypt the archive with a password, thins out old archives, and can watch its own health and send notices. It has no restore command of its own. [doc:laravel-tooling-research.md, spatie/laravel-backup] The tool and how it behaves on failure are confirmed when it is built. [doc:hosting-options.md Decision] [doc:laravel-kit-spec.md section 15]

### Setting it up

| Step | Who | What |
|---|---|---|
| 1 | Gordon | The Cloudflare bucket and its key: staging's in step 5 of `runbook-accounts.md`, production's in its step 13. |
| 2 | Gordon | The backup folder in the firm's Drive. `runbook-accounts.md` step 6. |
| 3 | Gordon | The archive's password, one for each site and never the same one, entered in Forge. A second copy of production's is kept away from the server. `runbook-accounts.md` step 5, item 8. |
| 4 | The agent | The backup settings in the app's code: what goes in the archive, the two places, the nightly time, the retention. Through plan, review and ship like any other change. [doc:plan-v2.md section 7] |
| 5 | Gordon | The scheduler switched on for the site in Forge. `runbook-accounts.md` step 4.3, item 7. |
| 6 | Gordon | Press Deploy. [doc:plan-v2.md section 8] |
| 7 | Gordon and the agent | The first-night check, below. |

- Unconfirmed: the hour the archive runs, and the clock it is measured on. The documents say "every night" and no time. [doc:plan-v2.md section 9] The tool's own example is a clean-up at 01:00 and a run at 01:30. [doc:laravel-tooling-research.md] Forge servers keep UTC unless changed. [web:laravel.com/forge/docs/servers/the-basics.md 2026-10-02] The app has a time-zone setting of its own. [doc:reviews/paperwork-W1.md finding 22] So "every night" and "every morning" could mean the server's clock or the app's. When the hour is chosen it is written here once, with its clock.
- Unconfirmed: how the server writes to the Drive folder. It waits on the Google credential. `runbook-accounts.md` steps 6 and 11.
- Unconfirmed: whether the tool needs a small extra program on the server to copy a SQLite database. The page read did not say. [doc:laravel-tooling-research.md, open items]
- Unconfirmed: how big one archive is. Cloudflare's storage is free to 10 GB a month; each 10 GB beyond that is about $0.15 a month. [doc:hosting-claims.md: R2 pricing, and Cloudflare open questions]

### Checking it, the first night and any day after

1. **In the app.** Settings, the Connections panel. The two backup stores each show whether they are working and when they last succeeded. Each has a button to test it. [doc:plan-v2.md section 5, "Screens", Settings]
2. **In Drive.** Open the backup folder. There is a new file dated today. [doc:hosting-options.md Decision: the Drive copy is the one seen without any tool]
3. **In Cloudflare.** Open the bucket. There is a new file dated today.
4. **On staging, the agent can look for itself.** It reads staging's log over its own key and confirms the run. It cannot look at production; it holds nothing that reaches it. [doc:laravel-kit-spec.md 8.1, and section 7 laravel-ship]

An archive that has never been restored proves nothing. Section 6 is the real check. [doc:laravel-tooling-research.md, spatie/laravel-backup: "a backup never restored is unproven"]

---

## 2. Before a deploy that changes the database

**The production deploy takes the backup as its first step and stops if the backup fails.** [doc:laravel-kit-spec.md section 7, laravel-ship, last paragraph] [doc:hosting-options.md Decision]

1. It is part of the deploy script in the app's repository. Nothing to set up by hand. [doc:laravel-kit-spec.md section 4: the deploy steps are one script in the repo]
2. The agent cannot run it and does not try. It runs when you press Deploy. [doc:laravel-kit-spec.md section 7, laravel-ship]
3. How you know: the deploy's own output in Forge shows the backup step first. A failed backup means a failed deploy, the old release stays live, and Forge emails you. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]
4. These archives are kept with the dailies. [doc:hosting-options.md Decision]

- Unconfirmed: what the backup command reports when it fails. The deploy script may only rely on it once that has been seen. [doc:laravel-kit-spec.md section 15] It is seen on staging in the dress rehearsal: `runbook-dress-rehearsal.md` Path 17, line 17.2.
- Two documents differ on what this backup holds. The plan and the hosting decision say the same archive as the nightly one: the database and the stored PDFs. [doc:plan-v2.md section 9] [doc:hosting-options.md Decision, the schedule table, second row] The kit spec says the deploy script takes "the database backup" first. [doc:laravel-kit-spec.md section 7, laravel-ship, last paragraph] This runbook follows the plan. The stored PDFs do not change in a deploy, so the database alone may be enough here, with the full archive every night. That choice is put to the app track and listed for you in the build log.
- Known limit: a Forge deploy fails by itself at ten minutes. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] [doc:hosting-claims.md: Forge deployments] The same deploy also builds the app's assets on the server. [doc:laravel-kit-spec.md D15] A full archive of every stored PDF, sent to two places inside that limit, gets harder each year.

---

## 3. DigitalOcean's daily backup of the machine

**Switched on once, in step 3 of `runbook-accounts.md`. It costs $3.60 a month.** [doc:hosting-options.md Decision]

1. What it is: DigitalOcean's own copy of the whole server, taken daily. [doc:plan-v2.md section 9]
2. What it is not: the off-site copy. It is kept in the same datacenter as the server. It is the fast way back after a bad day. [doc:hosting-options.md Decision] [web:docs.digitalocean.com/products/backups/details/features/ 2026-10-02]
3. When it runs: inside a four-hour window each day, which you can choose when you switch backups on. [web:docs.digitalocean.com/products/backups/details/features/ 2026-10-02]
4. How you check it: in DigitalOcean's own panel, on the server's page, there is a new backup each day.
5. Restoring from it is done in DigitalOcean's panel and is yours alone. [doc:laravel-kit-spec.md section 13]

- Unconfirmed: check on the vendor's page when you do this step: how many daily backups DigitalOcean keeps, and where its panel lists them. Its features and pricing pages did not say when read. [doc:hosting-options.md Decision: "length not confirmed at their page"] [web:docs.digitalocean.com/products/backups/details/features/ 2026-10-02]

---

## 4. The morning check

**Every morning something confirms that last night's archive arrived. You hear about it only when it did not.** [doc:plan-v2.md section 9] [doc:hosting-options.md Decision]

What the documents settle: that the check exists, that it runs every morning, and that the alert goes to you.

What they do not settle:
- Unconfirmed: what does the checking. The backup tool can watch its own archives and send a notice. [doc:laravel-tooling-research.md, spatie/laravel-backup] But a check that runs on the server says nothing on the morning the server itself is down.
- Unconfirmed: whether Forge's heartbeats are on your plan. A heartbeat is a check from outside: the nightly job reports in when it finishes, and Forge tells you if it has not heard within the minutes you set. In Forge it is the "Monitor with heartbeats" switch on a scheduled job, with a "Notify me after" value. [web:laravel.com/forge/docs/resources/scheduler.md 2026-10-02] [doc:hosting-options.md "What we still own", Monitoring]
- Unconfirmed: how the alert reaches you: email, or a push to your phone. The first draft of the plan used a push notice through Sancho; the approved plan says only "an alert to Gordon". [doc:plan.md section 9] [doc:plan-v2.md section 9]

Until those three are settled, the daily check is by eye: the Connections panel, or today's file in the Drive folder (section 1). Sancho's own rule is that nothing falls behind silently, so this is settled before go-live, not after. [doc:CLAUDE.md must-never 10]

Silence is the pass signal here, so a broken alert looks the same as a good night. The alert is therefore seen working once, on staging, before go-live: one night's archive is made to fail, and the alert must reach you the next morning. `runbook-dress-rehearsal.md` Path 17, line 17.3. [doc:laravel-kit-spec.md section 4: "Prove the log works before trusting its silence"]

---

## 5. Retention: what is kept

**14 daily, 8 weekly, 12 monthly, then one a year, kept.** [doc:plan-v2.md section 9] [doc:hosting-options.md Decision]

In plain terms: every night's archive for two weeks; then one a week back to eight weeks; then one a month back to a year; then one for each year.

1. It is set in the app's code, once, by the agent. Nothing for you to do. The tool has a setting for each of those tiers and a clean-up command that runs with the nightly job. [web:spatie.be/docs/laravel-backup/v10/cleaning-up-old-backups/overview 2026-10-02]
2. The tool never deletes the newest archive, whatever the settings. [web:spatie.be/docs/laravel-backup/v10/cleaning-up-old-backups/overview 2026-10-02]
3. One default must be changed when it is built: the tool starts deleting the oldest archives once they pass 5,000 MB in total. Left alone, that could cut the yearly copies short. [web:spatie.be/docs/laravel-backup/v10/cleaning-up-old-backups/overview 2026-10-02]
4. Archives taken before a deploy are kept with the dailies. [doc:hosting-options.md Decision]

How you check it: after a month, the Drive folder holds about fourteen recent files and a few older weekly ones, not thirty. After a year, look again.

- Unconfirmed: for how many years the yearly copies are kept. The decision says "then one a year, kept", which reads as for good. [doc:hosting-options.md Decision]
- Both places follow the same schedule. The plan gives the two places and the one retention in the same passage. [doc:plan-v2.md section 9, first bullet]

---

## 6. The restore test

**Every quarter, and once before go-live, an archive is loaded onto staging and its counts are compared. You start it.** [doc:plan-v2.md section 9] [doc:hosting-options.md Decision] [doc:laravel-kit-spec.md 9.2, the quarterly row]

It is also a gate: the host does not count as done until a restore has worked. [doc:plan-v2.md section 7, step B]

There are two kinds of this test. Before go-live, production holds almost nothing to compare. After go-live it holds everything.

**Two rules about the archive passwords hold for both kinds.**
1. Staging has its own archive password, different from production's. Staging gets test keys. [doc:plan-v2.md section 5, "Keys and passwords"]
2. Production's archive password is never entered on the staging site, and never given to the agent. [doc:plan-v2.md section 8] Staging's settings can be read from this Mac, so a password entered there is one the agent holds, and it would open every production archive. When production's archive is tested, you open it yourself and hand staging the opened copy.

### 6.1 The first test, before go-live: staging's own archive

Which archive is Sancho's reading, for you to overrule. The documents say "once before go-live" and "last night's archive", and do not say whose. [doc:plan-v2.md section 9] [doc:hosting-options.md Decision, the schedule table] Before the cut, production holds three logins and its Settings; restoring that proves little. Staging, after the import rehearsal, holds the whole history. An archive of that is the size of the real thing. So the first test restores **staging's own archive, onto staging**. Production's first real restore test is then the first quarterly one, 6.2.

It is the last path of the dress rehearsal: `runbook-dress-rehearsal.md` Path 18. In short:

| Step | Who | What |
|---|---|---|
| 1 | Gordon | Say "start the restore test". The restore drill is yours to start. [doc:laravel-kit-spec.md 8.2 and section 13] |
| 2 | The agent | Write down staging's counts: clients, properties, files, invoices, messages sent, stored PDFs. Counts only. [doc:plan-v2.md section 9: "counts compared"; the list of what to count is Sancho's reading of the tables in section 4] |
| 3 | Gordon and the agent | Take an archive of staging now. See it arrive in staging's bucket and in the test Google account's backup folder. |
| 4 | Gordon | In Forge, stop staging's queue worker and scheduler. The test runs with both stopped, so restored data can send nothing and book nothing. [doc:laravel-kit-spec.md 8.2] |
| 5 | Gordon and the agent | Empty staging, then load the archive back, from the written procedure. |
| 6 | The agent | Compare the counts with step 2. They must be equal. |
| 7 | The agent | Write the result and the procedure down, with the date. [doc:hosting-options.md Decision] |
| 8 | Gordon and the agent | Go on to the rehearsal's clean-up, which removes the real history from staging and the archives made of it. Then start the worker and the scheduler again. [doc:laravel-kit-spec.md 8.2] |

This test uses staging's own archive password, which staging already holds. Production's password is not involved.

The first test writes the procedure. Restoring is your action, from a short written procedure that the first restore test produces. [doc:hosting-options.md Decision] So the first one is done slowly and written up as it goes.

### 6.2 Every quarter after go-live: production's archive, on staging

| Step | Who | What |
|---|---|---|
| 1 | Gordon | Say "start the restore test". Production data moves only on your word, for a named job. [doc:laravel-kit-spec.md 8.2 and section 13] |
| 2 | Gordon | In Forge, stop staging's queue worker and scheduler. The test runs with both stopped, so restored data can send nothing and book nothing. [doc:laravel-kit-spec.md 8.2] |
| 3 | Gordon | Fetch last night's production archive and open it yourself, with production's password, away from the staging site. Staging holds no production key, so it can neither fetch the archive nor open it. [doc:laravel-kit-spec.md 8.2] |
| 4 | Gordon | Copy the opened contents to staging. |
| 5 | Gordon and the agent | Load them into staging, from the written procedure. |
| 6 | Gordon and the agent | Compare the counts: clients, properties, files, invoices, messages sent, stored PDFs. Staging after the restore must equal production as of last night. [doc:plan-v2.md section 9: "counts compared"; the list of what to count is Sancho's reading of the tables in section 4] |
| 7 | The agent | Write the result down, with the date. [doc:hosting-options.md Decision] |
| 8 | Gordon and the agent | Delete the restored data from staging, and the opened copy wherever it sat. Start the worker and the scheduler again. [doc:laravel-kit-spec.md 8.2] |

### Unconfirmed, for both kinds

- Unconfirmed: the exact restore steps. The backup tool has no restore command; its own documentation points to a separate community package. Which is used is decided when it is built. [doc:laravel-tooling-research.md, spatie/laravel-backup]
- Unconfirmed: how staging is emptied in 6.1 step 5. No hand edits on staging: every data change there is a committed, reviewed command. [doc:laravel-kit-spec.md section 6, item 5]
- Unconfirmed: in 6.2 step 3, where you open production's archive (which machine, which program), and how the opened copy travels to staging in step 4. The rule is fixed. The mechanism is not.
- Unconfirmed: how production's counts are read in 6.2 step 6. The agent cannot look at production. [doc:laravel-kit-spec.md 8.1] Either the app shows the counts to you on a screen, or you run one command from Forge. Neither is built yet.
- Unconfirmed: where the result is written. Sancho's suggestion: a dated line in this project's notes.

**When it is due.** Once before go-live (6.1). Then every quarter (6.2), with the kit's other quarterly work. [doc:laravel-kit-spec.md 9.2] Sancho raises it when it is due and creates no task for you. [doc:laravel-kit-spec.md 9.4]

---

## If it all goes wrong: which copy to reach for

| What happened | Reach for | Who |
|---|---|---|
| A bad deploy, the data is fine | The previous release, in Forge. Forge keeps the last four. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] | Gordon |
| The data is wrong or gone, the server is fine | Last night's archive, by the restore procedure. [doc:hosting-options.md Decision: restoring is Gordon's action] | Gordon |
| The server is broken | DigitalOcean's daily backup of the machine: the fast way back after a bad day. [doc:hosting-options.md Decision] | Gordon |
| The server and the DigitalOcean account are both lost | The archive in Cloudflare storage or in Drive, onto a new server: the off-site copy is what survives losing the provider or the account. [doc:hosting-options.md Decision] | Gordon |
| Google is locked out | The archive in Cloudflare storage. The letters themselves are not in it; the PDFs of sent letters are. [doc:hosting-options.md Decision] | Gordon |

- Unconfirmed: the exact steps to go back a release in Forge. [doc:laravel-kit-spec.md section 15] They are done once on staging and written down in the dress rehearsal: `runbook-dress-rehearsal.md` Path 17, line 17.1. Going back a release does not touch the database. [doc:laravel-kit-spec.md section 4, Rollback]

**Tell Sancho, when the first restore has worked:** "The restore test passed on (date). Counts matched. The procedure is written."
