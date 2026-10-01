---
name: Home Directions v4 runbook, accounts and keys
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The ordered checklist of everything only Gordon can do before v4 can go on a server, in three passes: first the accounts, the server and the staging site (the two GitHub repositories, Forge, the DigitalOcean server, Cloudflare storage, the Google Drive backup folder, Brevo, Calendly, the letters folder and template); then staging's first deploy, the Google credential and the app's own Settings; then production, made only after the first ship; for each step, what to create, the settings the plan and spec decided, where each key goes, what to clear from the settings Forge copies in, and the one line to tell Sancho when it is done
sources: ["[doc:plan-v2.md]", "[doc:hosting-options.md]", "[doc:hosting-claims.md]", "[doc:laravel-kit-spec.md]", "[doc:phase0-brief.md]", "[doc:build-handoff.md]", "[doc:requirements.md]", "[doc:current-system.md]", "[doc:survey-hdonline-home-directions.md]", "[doc:laravel-tooling-research.md]", "[doc:build-log-app.md]", "[doc:build-state.md]", "[doc:reviews/paperwork-W1.md]", "[gordon 2026-10-01]", "[gordon 2026-10-02]", "[web: vendor documentation pages read 2026-10-02, cited where used]"]
status: written 2026-10-02 overnight by the paperwork track (stage W1); reviewed the same night (reviews/paperwork-W1.md) and fixed by a third agent, see "W1 fixes" in build-log-paperwork.md; nothing in it has been done; every line marked "Unconfirmed" is to be settled before or during its step
---
# Runbook: accounts and keys (Gordon's side)

**The short version.** Thirteen steps in three passes. Each step ends with a line to say to Sancho. Nothing here needs code. Everything here needs you, because each step has a password, a payment or a key. [doc:plan-v2.md section 8]

**Pass one: the accounts, the server and the staging site.**

| # | Service | What you end up with |
|---|---|---|
| 1 | GitHub | Two empty private repositories in the Copper Leaf organisation |
| 2 | Laravel Forge | An account on the Hobby plan, joined to GitHub |
| 3 | DigitalOcean | One 2 GB server in New York, made through Forge, with daily backups |
| 4 | The staging site | Staging on that server, under its own user, with its settings cleaned |
| 5 | Cloudflare storage | Two backup buckets, and staging's key |
| 6 | Google Drive | A backup folder in the firm's Drive |
| 7 | Brevo | The account confirmed, office@homedirections.net as the sender, the mail test answered |
| 8 | Calendly | The plan's name, and a test account for staging. The firm's own token waits for the cutover day |
| 9 | Google | The letters folder, and the letter template with its images |

**Pass two: staging comes alive.**

| # | Step | What you end up with |
|---|---|---|
| 10 | The first deploy on staging | The app running on staging |
| 11 | The Google credential | Waits on Sancho. It is a step of its own so nothing can pass without it |
| 12 | The app's Settings, on staging | Invoice texts, template link, stamp images, type map, logins |

**Pass three: production. Only after the first ship.**

| # | Step | What you end up with |
|---|---|---|
| 13 | Production | The production site, its keys, its first deploy, its Settings |

Each line's source is in its own section below. The list itself is the one the build left for you. [doc:build-handoff.md section 6]

Why three passes. The app's own Settings exist only once the app is deployed on that site. [doc:plan-v2.md section 5, "Screens", Settings] And production's branch, `main`, moves only at ship. [doc:laravel-kit-spec.md D2] So staging is made first, and production is made when there is a shipped `main` to make it from.

What it costs each month, by the hosting decision: Forge Hobby $12.00, the server $12.00, DigitalOcean's daily backups $3.60, off-site storage about $0. About $27.60. [doc:hosting-options.md Decision]

## Four rules for every step

1. **Keys go into Forge, and nowhere else.** You create each key in its own service. You enter it in Forge, in the site's settings. It is never typed into the app, never put in the code, and never given to the agent. Staging gets test keys. [doc:plan-v2.md section 5, "Keys and passwords"]
2. **The lines you say to Sancho carry names and addresses only.** Never a key, a token or a password. The agent holds no Forge token, no production key and no production database credential. [doc:plan-v2.md section 8] [doc:laravel-kit-spec.md 8.1]
3. **Forge and DigitalOcean are opened in a browser the agent does not drive.** You said you would try. [gordon 2026-10-01: "yeah, I'll try"] GitHub in the driven browser is accepted for this app. [gordon 2026-10-01] [doc:laravel-kit-spec.md D3]
4. **A production key is made on the day it can be entered.** The production site does not exist until step 13. Cloudflare shows a key's secret once, and Calendly's token cannot be seen again. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02] [web:developer.calendly.com/docs/authentication/how-to-authenticate-with-personal-access-tokens.md 2026-10-02] So in pass one you make staging's keys only. No production key waits in a note or a file.

Where a key goes, in Forge's own words: open the site, go to its "Settings" panel, and click the "Environment" item. The environment is the site's own list of settings and keys. Changes there are written to the site's settings file on the server. [web:laravel.com/forge/docs/sites/environment-variables.md 2026-10-02] After a change, Forge offers to do two things for you: rebuild the app's saved copy of its settings, and restart the queue worker. The queue worker is the background process that sends the mail and makes the PDFs. Choose both, so the app picks up the new values. On screen the two read `config:cache` and `queue:restart`. [web:laravel.com/forge/docs/sites/environment-variables.md 2026-10-02]

The names of the settings each key goes under are not in this runbook. The app was still being built when this was written. Sancho gives you the names, never the values, when each connection is ready. [doc:laravel-kit-spec.md section 7, laravel-ship step 4] [doc:build-handoff.md section 2]

---

## 1. GitHub: the two private repositories

**Create two empty private repositories in the `CopperLeafCreative` organisation.** One holds the kit. One holds the app. [doc:laravel-kit-spec.md D4] [doc:build-handoff.md section 6]

Settings decided:
1. Owner: the `CopperLeafCreative` organisation, beside the plugin kit. [gordon 2026-10-01: "Copper Leaf. Free plan"] [doc:laravel-kit-spec.md D4]
2. Visibility: private, both. [doc:laravel-kit-spec.md D4] [doc:build-handoff.md section 6]
3. Plan: stay on Free. No upgrade. [gordon 2026-10-01] [doc:laravel-kit-spec.md D5]
4. Kit repository name: `clc-laravel-dev-kit`. That name is Sancho's suggestion, not your decision. [doc:laravel-kit-spec.md D4]
5. Create each one empty: no README, no licence file, no ignore file. The history already exists on this Mac and is pushed into it. [doc:build-handoff.md section 2: both are local git repositories already]
6. Add no secret to either repository. The automatic checks there hold no secret of any kind. [doc:laravel-kit-spec.md D12, and section 7 laravel-new: "no secret visible to the repository"]

Unconfirmed: the app repository's name. The documents name the local folder `hdonline-v4` and no GitHub name. [doc:build-handoff.md section 2] Sancho's suggestion is the same name. You decide.

What you should know before you do it: on the Free plan nothing at GitHub can refuse a bad push to `main`. You accepted that for this app. [gordon 2026-10-01] [doc:plan-v2.md section 8]

No key is created in this step. Pushing is done by the agent with the keys already on this Mac. [doc:laravel-kit-spec.md 8.1]

**Tell Sancho:** "The two repositories exist. Kit: CopperLeafCreative/(name). App: CopperLeafCreative/(name). Push the kit. For the app, push the working branch and `staging`. Do not push `main`."

What happens next: the agent pushes the kit. For the app it pushes the branch the work is on, and the `staging` branch the staging site needs in step 4. No push happens before you say this line. [doc:build-handoff.md section 3: "No pushes"]

`main` is not pushed here. `main` is production's branch. It moves only at ship, by the kit's one ship script, to a commit that was gated, reviewed and run on staging. [doc:laravel-kit-spec.md D2, and section 5 item 3] The overnight build has never run on a staging server. [doc:build-handoff.md section 3: "Local only. No server exists."] So none of it goes up as `main` yet.

- Unconfirmed, and yours to decide: what the first `main` is. Two ways fit the spec.
  - (a) No `main` on GitHub until the first ship. The production site is then made after that ship, in step 13. This runbook is written this way, because it needs no exception to the rule.
  - (b) One bare first commit with nothing of the app in it, pushed once, as a named exception on your recorded say. The production site could then be made beside staging in step 4.
  - Until you choose, (a) stands.

---

## 2. Laravel Forge: the account

**Create a Forge account on the Hobby plan and join it to GitHub. Create no API token.**

1. Sign up at Forge. Choose the **Hobby** plan, $12 a month. It allows one server of our own, which is all this needs. [doc:hosting-options.md Decision] [doc:hosting-claims.md: Forge plans]
   - Unconfirmed: whether you already have a Forge account. Nothing on disk says. [doc:hosting-options.md "Before committing" 1] If you do, use it and say so.
2. Join GitHub. In the organisation's settings, on the "Source control" page, click "Add provider" and choose GitHub. [web:laravel.com/forge/docs/source-control.md 2026-10-02]
3. Limit what Forge can see. On that connection's menu, "Manage GitHub access" opens GitHub so you can choose which repositories the Forge application can reach. Choose the app's repository only. [web:laravel.com/forge/docs/source-control.md 2026-10-02] [doc:hosting-options.md production boundary 2]
   - Forge's own warning: a connection made this way otherwise reaches every repository your account can reach. [web:laravel.com/forge/docs/source-control.md 2026-10-02]
   - If the app's repository does not show up later, Forge's page says the Forge application may not be approved for the organisation that owns it. Use "Reconnect" and grant the organisation. [web:laravel.com/forge/docs/sites/repository-access.md 2026-10-02]
4. **Do not create an API token.** Forge tokens belong to your whole account, with no documented limit to one server. The agent must hold none. [doc:hosting-options.md production boundary 1] [doc:laravel-kit-spec.md 8.1]
5. **Do not add this Mac's key at organisation level or account level.** Forge copies every organisation key onto every server it creates, and does not take them off again. [web:laravel.com/forge/docs/ssh.md 2026-10-02] [doc:hosting-options.md production boundary 4] The Mac's key goes on in step 4, for the staging site's user only.

Things to look at while you are in there, because the documents could not settle them:
- Unconfirmed: whether the Hobby plan includes the health check after a deploy, and heartbeats for scheduled jobs. The pricing page and the docs disagree. Look in the dashboard. [doc:hosting-options.md "What we still own", Monitoring] [doc:laravel-kit-spec.md section 15]

**Tell Sancho:** "Forge is set up on Hobby. GitHub is joined and limited to the app's repository. No API token exists. Health checks on Hobby: yes or no. Heartbeats on Hobby: yes or no."

---

## 3. DigitalOcean: the server

**Create a DigitalOcean account you own, join it to Forge, and let Forge build one server: 2 GB, New York, daily backups on.**

1. Create the DigitalOcean account. It is yours, so the server can leave Forge one day and keep running. [doc:hosting-options.md Decision, and "The pick, in full" reason 4]
   - Unconfirmed: whether you already have a DigitalOcean account. Nothing on disk says. [doc:hosting-options.md "Before committing" 1]
2. Join it to Forge. In Forge: the organisation's settings, the "Server providers" page, "Add provider", DigitalOcean, then "Login with DigitalOcean". Forge gets its own permission from DigitalOcean; no key is copied by hand. [web:laravel.com/forge/docs/server-providers.md 2026-10-02]
3. In Forge, click "New server". Give it a name, choose DigitalOcean, then set the type, the region and the size. [web:laravel.com/forge/docs/servers/the-basics.md 2026-10-02]

| Setting | Value | Source |
|---|---|---|
| Type | App Server | [web:laravel.com/forge/docs/servers/types.md 2026-10-02: the type Forge recommends for one app on one server] |
| Region | New York | [doc:hosting-options.md Decision] |
| Size | 2 GB memory, 1 processor, 50 GB disk, $12 a month | [doc:hosting-options.md Decision] [doc:hosting-claims.md: DigitalOcean Basic droplets] |
| Operating system | Ubuntu 26.04 | [doc:hosting-claims.md: Forge offers 26.04 on every provider] [doc:hosting-options.md "What we still own"] |
| PHP | 8.5 | [doc:plan-v2.md section 2] [doc:laravel-kit-spec.md D9] |
| Database | none: the app uses SQLite, a file | [doc:plan-v2.md section 2] |
| "Add server's SSH key to source control providers" | **unticked** | [web:laravel.com/forge/docs/ssh.md 2026-10-02] [doc:hosting-options.md production boundary 2] |

   - Unconfirmed: check on the vendor's page when you do this step: how the form lets you choose no database. Forge's page says an App Server installs MySQL, Postgres or MariaDB only "if selected". [web:laravel.com/forge/docs/servers/types.md 2026-10-02]
   - Unconfirmed: which of the three New York datacenters. DigitalOcean has NYC1, NYC2 and NYC3. [doc:hosting-claims.md] The documents do not choose. Any of them meets the decision.
   - Why the unticked box matters: if it stays ticked, the server gets a key that can reach every repository your GitHub account can. [web:laravel.com/forge/docs/ssh.md 2026-10-02]
4. Turn on DigitalOcean's **daily** backups for the server. They cost 30 percent of the server's price, $3.60 a month. [doc:hosting-options.md Decision] [web:docs.digitalocean.com/products/backups/details/pricing/ 2026-10-02]
   - Unconfirmed: check on the vendor's page when you do this step: whether Forge's form offers the backups, or you switch them on in DigitalOcean's own panel afterwards. DigitalOcean's page says backups can be enabled on an existing server. [web:docs.digitalocean.com/products/backups/details/features/ 2026-10-02]
   - These backups sit in the same datacenter as the server. They are the fast way back, not the off-site copy. [doc:hosting-options.md Decision] [web:docs.digitalocean.com/products/backups/details/features/ 2026-10-02]
5. Leave the server's clock on UTC, Forge's default, unless you decide otherwise. [web:laravel.com/forge/docs/servers/the-basics.md 2026-10-02] No backup hour is chosen yet. When it is, `runbook-backups.md` states it once, with the clock it is measured on.
6. Unconfirmed: check on the vendor's page when you do this step: whether Forge shows you a server password at the end of the build. If it shows one, it goes in your password manager and nowhere else.

What the agent can never do here: create the server, see its passwords, or open DigitalOcean's panel. [doc:laravel-kit-spec.md section 13]

**Tell Sancho:** "The server exists. Its name is (name). Its public address is (IP address). Daily backups are on. The source-control box was unticked."

---

## 4. The sites: staging now, production in step 13

**Two sites on that one server, each under its own user. Production deploys only when you press Deploy. Staging deploys when the agent pushes.** [doc:hosting-options.md Decision] [doc:laravel-kit-spec.md D2]

Make the **staging** site now, after step 1's push, so the `staging` branch exists. Make the **production** site in step 13, when `main` exists. This section serves both: 4.1 to 4.3 are done for each site, 4.4 for staging, 4.5 for production.

A site must be made from its repository. Forge's page: a site made without one cannot be given one later, and has to be made again. [web:laravel.com/forge/docs/sites/the-basics.md 2026-10-02]

### 4.1 The addresses

Unconfirmed: the two web addresses. The first draft of the plan named `app.homedirections.net` for production; the approved plan names none, and neither names staging. [doc:plan.md section 9] [doc:phase0-brief.md Q3: that name does not exist in DNS yet] Sancho's suggestion, not a decision: `app.homedirections.net` and `app-staging.homedirections.net`. You decide.

For each address:
1. In Cloudflare, where the domain's DNS lives, add a record pointing the name at the server's public address, with Cloudflare's proxy switched off for that record. [doc:phase0-brief.md Q3: DNS is at Cloudflare] [doc:hosting-options.md: "The pick starts with the hostname unproxied"] Nothing must sit in front of the Calendly and mail notices. [doc:hosting-options.md "The pick, in full" reason 2]
2. Do not use the free `on-forge.com` address Forge gives each site. It runs through Cloudflare's proxy. [web:laravel.com/forge/docs/sites/the-basics.md 2026-10-02]

The name is joined to the site, and its certificate taken, in 4.3, once the site exists.

### 4.2 Creating a site

**First, one question to Sancho, before you make either site: "Is the example settings file on this branch free of seed passwords?"**

Why. When a site is made, Forge copies the app's example settings file onto the server as that site's environment. [web:laravel.com/forge/docs/sites/environment-variables.md 2026-10-02] The overnight build put the three local logins' passwords in that example file. [doc:build-handoff.md section 2 item 7] [doc:build-log-app.md, stage P1 plan, item 4] Taking them out has been handed to the app track's review. [doc:build-state.md, log of hand-offs] **No seed login password may reach a server.** If Sancho's answer is not a plain yes, do not make the site.

Then choose the app's repository and the branch, and open "Advanced settings". [web:laravel.com/forge/docs/sites/the-basics.md 2026-10-02]

| Setting | Production | Staging | Source |
|---|---|---|---|
| Repository | the app's | the app's | [doc:laravel-kit-spec.md section 7, laravel-new] |
| Branch | `main` | `staging` | [doc:laravel-kit-spec.md D2, and section 7 laravel-new] |
| Website isolation (its own user) | on | on | [doc:hosting-options.md Decision] [web:laravel.com/forge/docs/sites/the-basics.md 2026-10-02] |
| Push to deploy | **off**, and it stays off | **off** while you make the site; switched on as the last line of 4.4 | [doc:laravel-kit-spec.md section 7 laravel-new] [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02: it is on by default for new sites, and can be switched on later on the "Deployments" tab of the site's settings] |
| Zero-downtime deployments | on | on | [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02: on by default, and it can only be chosen when the site is created] |
| PHP version | 8.5 | 8.5 | [doc:laravel-kit-spec.md D9] |
| Deploy key | its own, read only | its own, read only | [doc:laravel-kit-spec.md section 7 laravel-new] |

Notes on that table:
1. **Push to deploy is the switch that matters most.** With it on, a push to the site's branch deploys. If it is left on for production, a push ships. The plan rests on it being off. [doc:laravel-kit-spec.md section 1 item 2, and 8.1] Check it twice.
2. Why staging starts with it off too: from the moment it is on, every push to `staging` deploys. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] The first deploy must not run before the shared database path and the cleaned environment of 4.3 are in place. [doc:laravel-kit-spec.md section 7 laravel-new, and section 16]
3. Zero-downtime deployments, in plain terms: each deploy goes into a fresh folder and is switched in only when every step has finished. If a step fails, the site keeps running the release before. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]
4. The deploy key is a key that lets this one site fetch this one repository. Forge can make it while you create the site. You then add it to the app repository's "Deploy Keys" on GitHub, without write access. [web:laravel.com/forge/docs/sites/the-basics.md 2026-10-02] [web:laravel.com/forge/docs/ssh.md 2026-10-02] [doc:laravel-kit-spec.md section 7 laravel-new: "read-only"]
5. The site's own user: Forge's main login, `forge`, can read every site's files, whatever the isolation. [web:laravel.com/forge/docs/sites/user-isolation.md 2026-10-02] So `forge` is yours alone. The agent never gets it.
6. Unconfirmed: check on the vendor's page when you do this step: the box that has Forge install the app's PHP packages when the site is made. Forge's page says this is done right after the site is created. [web:laravel.com/forge/docs/sites/the-basics.md 2026-10-02] Sancho's suggestion: untick it. The repository's own deploy script does that work at the first deploy, after 4.3.

**Once the site is made, do 4.3 in the same sitting. Do not open the site's address and do not press Deploy until 4.3 is finished.** Forge's free `on-forge.com` address is live as soon as a site exists. [web:laravel.com/forge/docs/sites/the-basics.md 2026-10-02]
- Unconfirmed: check on the vendor's page when you do this step: what a new site shows at that address before its first deploy.

### 4.3 Straight after creating a site, before its first deploy

1. **Share the database's path.** Add a shared path from `database.sqlite` to `database/database.sqlite`. A shared path is a file or folder that stays the same across releases. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] It must exist before the first deploy. Without it, the deploy quietly makes a new empty database with each release. [doc:laravel-kit-spec.md section 7 laravel-new, and section 16]
2. **Share the stored files.** Add `storage` as a shared path. The PDFs the app keeps must survive each release. [doc:plan-v2.md section 5: the system keeps each PDF as sent] Forge shares only the environment file by itself; storage folders are yours to add. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]
3. **Join the address and take the certificate.** Add the name from 4.1 to the site as a custom domain, which means your own web address in place of Forge's free one. Take the free Let's Encrypt certificate. Forge recommends its DNS check: Forge shows you one more record to add in Cloudflare, and that proves the name is yours. That record must stay for as long as the certificate is wanted. Certificates renew by themselves while the Forge subscription is active. [web:laravel.com/forge/docs/sites/domains.md 2026-10-02]
4. **Paste the deploy script.** Each site runs the one script kept in the app's repository, and nothing else, so staging tests the same deploy production gets. [doc:laravel-kit-spec.md section 4] Sancho gives you the few lines to paste into the site's deploy script box. Forge's three special lines that create, switch to and restart a release must stay in it. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]
5. **Clean the environment.** Forge has already filled it. It copied the app's example settings file when the site was made, and changed only some database lines. [web:laravel.com/forge/docs/sites/environment-variables.md 2026-10-02] That example file was written for this Mac, not for a server. [doc:reviews/paperwork-W1.md finding 3] Open the site's "Settings", then "Environment", and go through it with Sancho's list. For each line Sancho gives the name and says clear, replace or leave. Never a value. [doc:laravel-kit-spec.md section 7, laravel-ship step 4]
   - a. **Clear any seed login password.** There should be none, by the question in 4.2. Look anyway. If you find one, delete the line and tell Sancho it was there. Those passwords are then spent, and new local ones are made.
   - b. **Replace the app's mode.** Production on the production site. Staging on the staging site. The example says local. The app reads its mode from this one line. [web:laravel.com/docs/13.x/configuration 2026-10-02] The kit's block on destructive commands is on in every mode except local and testing. [doc:laravel-kit-spec.md section 4] Left at local, that block is off.
   - c. **Replace the error display: off.** Laravel's own page: in production it should always be off, or an error page can show settings to whoever is looking. [web:laravel.com/docs/13.x/configuration 2026-10-02] [doc:laravel-kit-spec.md section 4: "debug off in production"] Off on staging too is Sancho's reading, because staging holds real client data during the rehearsal. [doc:laravel-kit-spec.md section 6 item 5]
   - d. **Replace the app key with one made for this site.** Each site has its own. No environment file is ever copied from one site to the other. [doc:laravel-kit-spec.md 8.2, and section 6 item 10]
     - Unconfirmed: check on the vendor's page when you do this step: whether Forge makes the app key for you, or you start it from the site's Commands panel. Sancho gives the exact line.
   - e. **Replace the site's own address**, and any other line that names this Mac.
   - f. **Leave the stand-in lines for mail, Calendly, Google and the backups until their own steps.** The build ran those against stand-ins. [doc:build-handoff.md section 2 item 3] Sancho's list marks each one and the step that replaces it.
   - Unconfirmed: whether Forge also rewrites the mode line when it copies the file. The review could not confirm it. [doc:reviews/paperwork-W1.md finding 3] Read the line yourself.
   - Later on: ask before editing the environment, and keep the old text. [doc:laravel-kit-spec.md section 6 item 5]
6. **Create the queue worker.** It is the background process that sends the mail and makes the PDFs. Create one from the site's "New Worker" form. Forge keeps it running and restarts it after a crash or a reboot. [web:laravel.com/forge/docs/sites/queues.md 2026-10-02]
7. **Switch on the scheduler.** Forge's Laravel scheduler runs the app's schedule every minute. [web:laravel.com/forge/docs/resources/scheduler.md 2026-10-02] [doc:hosting-claims.md: Forge queue and scheduler] The nightly backup, the morning check and the 15-minute Calendly check all hang on it. [doc:plan-v2.md sections 5 and 9] On production that Calendly check has nothing to ask with until the cutover day, because production holds no Calendly token before then (step 8).
   - Unconfirmed: that the app's 15-minute check does nothing, and raises no alarm, while no token is set. Sancho confirms it from the app's tests before production's scheduler goes on.
8. **Switch on the health check**, if step 2 found it on your plan: the site's "Settings", "Deployments", the "Health check" toggle. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] Point it at the app's `/up` address. [doc:laravel-kit-spec.md D13]

### 4.4 Staging only

Rules for staging. They ask nothing of you now; they bind every later step.
- **Mail on staging never reaches a client.** [doc:laravel-kit-spec.md 8.2] [doc:plan-v2.md section 10]
- **Test accounts only.** Staging's Google and Calendly are separate test accounts that own nothing real. [doc:laravel-kit-spec.md 8.2] [doc:plan-v2.md section 5]
- **No production key is ever entered on staging.** That includes production's archive password (step 5). [doc:laravel-kit-spec.md 8.2] [doc:plan-v2.md section 5, "Keys and passwords"]

Steps, in this order:
1. **Put a login in front of staging.** [doc:laravel-kit-spec.md section 7 laravel-new] Forge can put a password on a whole site or on one path: the site's "Network" tab, "Add security rule". Forge does not keep that password. [web:laravel.com/forge/docs/sites/network.md 2026-10-02] Sancho names the paths to protect.
2. **Set the mail trap.** On the staging site's Environment, enter the setting that sends every message staging makes to one address, yours, whatever address is on the file. Sancho gives the setting's name. [doc:plan-v2.md section 10: "Staging mail goes to a trap"] [doc:laravel-kit-spec.md 8.2]
   - Unconfirmed: that the built app has this setting. If it has not, it is owed by the app track, and staging holds no real client address until it exists.
   - The trap is proven before anything else in the rehearsal, with an address that is not yours. `runbook-dress-rehearsal.md`, set-up line S5.
3. **Add this Mac's key, for the staging site's user only. Not before the guards are in place.**
   - a. First, the condition. The kit's shell guard and browser guard are registered on this Mac, and their tests pass. The plan makes this a gate: "the guard's tests pass before any staging key exists". [doc:plan-v2.md section 7, step A] [doc:laravel-kit-spec.md section 14, step 3] Registering them is yours, from the kit installer's printed instructions. [doc:build-handoff.md section 3, "Do not register hooks", and section 6] Sancho then shows you the guards' tests passing and its start-of-job check passing. [doc:laravel-kit-spec.md section 5 item 7] Sancho tells you when. Until then, add no key.
   - b. Why it matters more on one server: this key opens the machine that also holds production. The only wall is a permission between two users. [doc:hosting-options.md Decision, last paragraph]
   - c. Then the key. On the server: "Settings", the "SSH" tab, "Add key". Because the sites are isolated, Forge lets you choose which user gets the key. Choose the staging site's user. Not `forge`. Not production's user. [web:laravel.com/forge/docs/ssh.md 2026-10-02] [doc:hosting-options.md Decision]
   - d. Ask Sancho for the public key to paste. A public key is safe to show.
4. **Switch push to deploy on, last.** The staging site's "Settings", "Deployments", the "Push to deploy" toggle. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] From now a push to `staging` deploys. [doc:laravel-kit-spec.md section 7 laravel-new]

### 4.5 Production only (done in step 13)

Rules for production:
- **No key from this Mac.** Not for `forge`, not for production's user. [doc:hosting-options.md production boundary]
- **Deploy is your press.** The agent hands you the full commit ID, the long code that names one exact version of the app. The commit Forge shows must be that one. Pressing Deploy is the moment it goes to production. [doc:laravel-kit-spec.md section 7, laravel-ship step 4]
- **Push to deploy stays off.** [doc:laravel-kit-spec.md section 1 item 2, and 8.1]
- Forge emails you when a deploy fails. That is on by default. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]

Steps:
1. **Never copy the deploy hook.** Every site has a web address that deploys it for whoever holds it. Forge shows it under "Settings", "Deployments", "Deploy hook". [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02] Never copy production's anywhere: not a note, not a chat, not a file. [doc:hosting-options.md production boundary 5]
2. **Read the key list once everything is in place.** On the server: "Settings", the "SSH" tab. [web:laravel.com/forge/docs/ssh.md 2026-10-02] Tell Sancho which keys are there and which user each belongs to. The agent records them, and its start-of-job check then proves that no key on this Mac opens `forge` or production's user. [doc:laravel-kit-spec.md section 5 item 7, section 7 laravel-new, and section 12]
   - Unconfirmed: check on the vendor's page when you do this step: whether that screen shows each key's fingerprint or only its name. A fingerprint is a short code that identifies a key without revealing it. The spec asks for fingerprints. They are not secrets.

### 4.6 The check the agent runs

From the staging site's user, production's folder cannot be read. The agent runs this test and shows you the result. [doc:hosting-options.md Decision, last paragraph] [doc:laravel-kit-spec.md, the note under the title] It needs production's folder to exist, so it is run in step 13, as soon as the production site is made and before any production key is entered.

**Tell Sancho, for staging:** "The staging site exists at (address), branch staging, user (name). You said the example file held no seed password, and I found none. Mode is staging, error display is off, the app key is its own. The database path and storage are shared. The login is in front. The mail trap points at (my address). The guards were registered and passing before the Mac's key went on, and the key is on the staging user only. Push to deploy went on last."

### Sancho settles these (nothing for you to do)

- Which credential a zero-downtime site really uses to fetch the code. One Forge page says such a site fetches with the GitHub connection's own token and no key. The same page says that once a site has a deploy key, Forge deploys with that. [web:laravel.com/forge/docs/sites/repository-access.md 2026-10-02] The kit spec lists it as something to confirm on a real site. [doc:laravel-kit-spec.md section 15] It is one more reason step 2's limit to the one repository matters.
- How the repository's deploy script and Forge's three special lines fit together. Confirmed on the first staging deploy. [doc:laravel-kit-spec.md section 15]
- The queue worker's exact settings. Sancho gives them from the built app.
- Whether a new key is made on this Mac for staging, or one already here is used. The kit decides at its first job.
- How staging's login and the incoming notices from Calendly and Brevo live together. A password on the whole site would turn those notices away. [web:laravel.com/forge/docs/sites/network.md 2026-10-02]
- Whether production's deploy hook still works with push to deploy off. The spec assumes it does. [doc:laravel-kit-spec.md section 15]

---

## 5. Cloudflare storage: the off-site backups

**Create two private buckets, one for production's backups and one for staging's. Each gets a key that opens that bucket and nothing else. Make staging's key now. Make production's in step 13.** [doc:hosting-options.md Decision, "Where 'somewhere else' is"] [doc:plan-v2.md section 9]

1. Sign in to the Cloudflare account that already holds the domain's DNS. [doc:hosting-options.md Decision]
2. Add R2, Cloudflare's storage, to the account. Cloudflare's page calls this completing a checkout to add an R2 subscription. [web:developers.cloudflare.com/r2/get-started/ 2026-10-02] Storage is free up to 10 GB a month; this app's archives are far below that. [doc:hosting-claims.md: R2 pricing] [doc:hosting-options.md Decision: "about $0 at this size"]
   - Unconfirmed: check on the vendor's page when you do this step: whether the checkout asks for a payment card even for the free amount. [doc:hosting-claims.md, Cloudflare open questions]
3. Create the two buckets.
   - Unconfirmed: the buckets' names and location. The documents set neither. Sancho's suggestion for names: `hd-v4-backups` and `hd-v4-backups-staging`.
4. Create **staging's** key. In the dashboard: R2 object storage, then "Manage" beside API Tokens. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02]
   - Permission: **Object Read & Write**. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02]
   - Limit it to the one bucket, staging's. That choice is offered for this permission. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02] [doc:hosting-options.md Decision: the credential "can reach that one bucket and nothing else"]
   - Unconfirmed: the kit spec asks for a backup key that "can write to one folder and read nothing". [doc:laravel-kit-spec.md 8.2] Cloudflare's four permissions do not include write-only, and removing old archives needs more than writing. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02] So the key as described here is one bucket, read and write. Sancho raises the difference with you; it is not settled.
   - Unconfirmed: check on the vendor's page when you do this step: "Create Account API token" or "Create User API token". Both are offered. An account token belongs to the account; a user token belongs to you. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02]
5. Cloudflare then shows an Access Key ID and a Secret Access Key. The secret is shown once. [web:developers.cloudflare.com/r2/api/tokens/ 2026-10-02]
6. Enter five things in Forge, on the **staging** site's Environment: the Access Key ID; the Secret Access Key; the bucket's name; the endpoint, which is the web address programs use to reach the storage, `https://(your account ID).r2.cloudflarestorage.com`; and the region, which for Cloudflare is the word `auto`. [doc:hosting-claims.md: R2 implements the S3 interface at that address with region 'auto']
7. **Production's key: in step 13.** Items 4 to 6 again, for production's bucket, entered on the production site. Staging gets test keys, never production's. [doc:plan-v2.md section 5]
8. **Choose two archive passwords, one for each site.** The nightly archive is encrypted, and its password is one of the keys you enter in Forge. [doc:plan-v2.md section 5, "Keys and passwords"] The tool the research found takes it under the name `BACKUP_ARCHIVE_PASSWORD`; the tool and the name are confirmed when it is built. [doc:laravel-tooling-research.md, spatie/laravel-backup] [doc:hosting-options.md Decision] Enter staging's now, on the staging site. Enter production's in step 13, on the production site.
   - **Staging's password is different from production's.** Staging gets test keys. [doc:plan-v2.md section 5, "Keys and passwords"]
   - **Production's password is never entered on the staging site, and never given to the agent.** Staging's settings can be read from this Mac, so a password entered there is one the agent holds. [doc:plan-v2.md section 8] For the restore test, see `runbook-backups.md` section 6.
   - Unconfirmed: where the second copy of production's password lives. It must exist somewhere other than the server, or losing the server makes every archive unreadable. The documents do not say where. Sancho's suggestion: your own password manager.

**Tell Sancho:** "Cloudflare storage is set up. Production bucket: (name), no key yet. Staging bucket: (name), with its own key, limited to its bucket, entered in Forge on staging. Staging's archive password is set, and it is not the one production will get."

---

## 6. Google Drive: the second backup place

**Create one folder in the firm's Google Drive for the backup archives. It is not the letters folder.** [doc:plan-v2.md section 9] [gordon 2026-10-01: "could we do both?? I love redundancy"]

1. Sign in to the firm's Workspace. The super admin is office@homedirections.net. [gordon 2026-10-01]
2. Create a folder for the backup archives, apart from the letters folder in step 9. Each archive holds the whole database and the stored PDFs, encrypted. [doc:plan-v2.md section 9] Share the folder with nobody who does not need it.
   - Unconfirmed: the folder's name and which Workspace user owns it. The documents do not say.
3. Staging writes its test archives to a folder in the separate test Google account, never to the firm's Drive. [doc:laravel-kit-spec.md 8.2]

Why both places: Cloudflare is a third company, apart from DigitalOcean and Google. The Drive folder is the one you and Peter can see without any tool. A lock-out at Google would take the letters and this copy together, which is why it is the second place and not the only one. [doc:hosting-options.md Decision]

**Tell Sancho:** "The backup folder exists in the firm's Drive. Its name is (name). Its owner is (account). Its link is (link)."

What happens next: how the server writes into that folder waits on the Google credential, step 11. The exact kind of credential is settled at the start of the build, and the build had no Google account to work with when this was written. [doc:plan-v2.md section 5, "Google access"] [doc:build-handoff.md section 2 item 3]

---

## 7. Brevo: the account, the sender, the mail test

**Confirm the Brevo account is the firm's, make sure office@homedirections.net is a sender, and answer the mail test. Production's key is made in step 13.**

What is already true: Brevo is authenticated on homedirections.net in DNS. No new account and no DNS change is needed for production. [doc:phase0-brief.md Q2 and Q8] [doc:plan-v2.md section 2]

1. Sign in to Brevo. Confirm it is the account in use. You were "90% sure". [gordon 2026-10-01] [doc:plan-v2.md section 11 item 5]
2. Look at what else sends through it. The website's mail is the likely answer; it is not confirmed. [doc:phase0-brief.md Q2, the Brevo finding, and Q8]
3. Make sure office@homedirections.net is set up as a sender. All mail goes out as that address, replies go there, and a copy lands in that mailbox. [doc:phase0-brief.md Q8] [doc:plan-v2.md section 5, "Mail"]
   - Unconfirmed: check on the vendor's page when you do this step: where senders are listed in Brevo and what it asks to confirm one.
4. Do the mail test, still open: does a message sent to office@homedirections.net reach `homedirectionsinc@gmail.com`, the one Gmail box Peter and Maria Pia use? [doc:plan-v2.md section 11 item 4] [gordon 2026-10-01: "send an email, ask him to confirm receipt"] Gmail stopped fetching other accounts in January 2026, so it is worth the five minutes. [doc:plan-v2.md section 11 item 4] The message is yours to send; Sancho sends nothing.
5. **Production's key: in step 13.** Create a key for the app, and enter it in Forge on the production site's Environment.
   - Unconfirmed: check on the vendor's page when you do this step: where keys are made in Brevo, and whether the key is shown only once. Brevo's help page for keys could not be read tonight.
   - Unconfirmed: which kind of key the app needs. Sancho says when the mail connection is built against the real service; tonight it was built against a stand-in. [doc:build-handoff.md section 2 item 3]
6. **Staging's key must come from an account that cannot send as the firm.**
   - Why. Staging's settings can be read from this Mac; that is what the staging key is for. A key on the firm's own Brevo account can send as office@homedirections.net to anyone. The agent holds no production key. [doc:plan-v2.md section 8] Staging gets test ones. [doc:plan-v2.md section 5, "Keys and passwords"] No production key is ever entered on staging. [doc:laravel-kit-spec.md 8.2]
   - So a second key on the firm's account does not go on staging, unless you sign that as an exception, by name and date.
   - Sancho's suggestion: a separate free Brevo account for staging, with all its mail going to the trap of 4.4.
   - Unconfirmed: check on the vendor's page when you do this step: whether a free Brevo account can do this, what address it sends from without touching the firm's DNS, and whether it gives delivered and opened reports. The rehearsal needs real delivery to your own address, with those reports. [doc:plan-v2.md section 7, step E]
   - This is your choice to make. It is listed for you in the build log.

**Tell Sancho:** "Brevo is confirmed as ours. Office@ is a sender. Other things sending through the account: (list, or none). The mail test: arrived, or did not arrive. Staging's mail uses (which account), and its key is in Forge on staging."

### Sancho settles these (nothing for you to do)

- Delivered and opened reports. The system records each message's delivered and opened reports against it. [doc:plan-v2.md section 5, "Mail"] Brevo sends those as notices to an address on the app; its event names include `delivered`, `opened` and `unique_opened`. [web:developers.brevo.com/docs/transactional-webhooks 2026-10-02] Who sets that notice up, you in Brevo's panel or the app through Brevo's interface, is not settled. Brevo's page shows it can be created through the interface. [web:developers.brevo.com/docs/how-to-use-webhooks 2026-10-02] How the app proves a notice really came from Brevo is not settled either. Both are settled when the connection is built. [doc:phase0-brief.md Q8: "To confirm when the connection is built"] If it turns out to need you, Sancho brings the steps.

---

## 8. Calendly: the plan, and a test account for staging

**Check the plan's name, and set up a separate test Calendly account for staging. Do not create the firm's own token yet. It is made and entered on the cutover day, and not before.**

What is already true: the account is on a paid plan; there are two appointment types; the booking form already requires the property address; the booking page is calendly.com/homedirections. [gordon 2026-10-01] [doc:phase0-brief.md Q4]

Why the firm's token waits. A booking creates a file, a client, a property and a Google Doc, and the system also asks Calendly every 15 minutes for anything it missed. [doc:plan-v2.md section 5, "Letters" and "Calendly"] Pointing Calendly at v4 is part of going live, not of setting up. [doc:plan-v2.md section 6 step 5, and section 7 step I] With the firm's token on production before the cut, production would make real files and real Docs for jobs Peter is still doing in v3. The import would then bring the same jobs in a second time. So production holds no Calendly token until `runbook-cutover.md` Step 7.

1. Sign in to Calendly. Check the plan's name. Calendly's page lists the plans that can send instant notices: Professional, Standard, Standard Plus, Teams, Teams Plus and Enterprise. [web:calendly.com/help/webhooks-overview 2026-10-02] The tier was never stated; this closes that open item. [doc:plan-v2.md section 11 item 7]
2. **Create no token in the firm's account now.** If one already exists for another purpose, leave it where it is and enter it nowhere.
3. Set up staging's test account. Calendly has no practice mode, so staging uses a separate test Calendly account that owns nothing real. [doc:laravel-kit-spec.md 8.2] Give it the same two appointment types and the same required address question, so the rehearsal bookings look like real ones.
   - Unconfirmed: whether the test account must be on a paid plan. By Calendly's page a free account cannot send instant notices. [web:calendly.com/help/webhooks-overview 2026-10-02] Without them, staging can test the 15-minute check but not the instant path. You decide whether to pay for a month.
   - Unconfirmed: the exact wording of the address question on the real booking form. The test account's form should match it. Sancho cannot see the real form without you.
4. Create the **test account's** token. In Calendly: the Integrations page, the "API & Webhooks" tile, then "Get a token now" (or "Generate new token"), "Create Token", "Copy token". It cannot be seen again afterwards. [web:developer.calendly.com/docs/authentication/how-to-authenticate-with-personal-access-tokens.md 2026-10-02] The firm's token is made the same way, on the day.
5. Enter the test account's token in Forge on the **staging** site's Environment.

The type map is set in the app's Settings, in step 12 for staging. This is the map: [doc:plan-v2.md section 5, "Screens", Settings]

| Calendly appointment type | Service in v4 | Price | Source |
|---|---|---|---|
| Professional Opinion | opinion | $875 | [doc:phase0-brief.md Q4] [doc:requirements.md, business context] |
| Structural Design | design | $1,250 | [doc:phase0-brief.md Q4] [doc:requirements.md, business context] |
| (none) | hourly design work, entered by hand | $475 an hour | entered by hand: [doc:plan-v2.md section 5]; the price: [doc:requirements.md, business context] |

**Tell Sancho:** "Calendly is on the (plan name) plan. No token of the firm's account is entered anywhere. The test account is (account), on the (plan name) plan, and its token is in Forge on staging."

### Sancho settles these (nothing for you to do)

- The instant notices. Calendly's help page sends you to its developer interface to set these up; it describes no screen for it. [web:calendly.com/help/webhooks-overview 2026-10-02] So the app does it, with the token. How the app switches the notices on (a button on the Connections panel, or a step in the deploy), and how it proves a notice came from Calendly, is settled when the connection is built against the real service. On production it happens on the cutover day, with the token.
- Known risk: Calendly is reported to stop sending after a day of failures. The source is secondary. The 15-minute check and a one-day alert cover it. [doc:plan-v2.md section 10] [doc:hosting-options.md "Also learned"]
- A possible later change, not in the plan: a plain switch in the app, "take bookings from Calendly", off until the day. With it, the firm's token could go in early and be tested while the switch stays off. It is put to the app track. Until it exists and you have approved it, the rule above stands: no token on production before the cut. [doc:reviews/paperwork-W1.md finding 1]

---

## 9. Google: the letters folder and the letter template

**Two things now: a folder for the letters, and a finished template in it. The credential is step 11.**

### 9.1 The letters folder

1. Signed in to the firm's Workspace, look in Drive for shared drives. Whether Business Starter has them is settled by looking, not by the web pages that disagree. [doc:phase0-brief.md Decisions, Q2]
2. Create the letters folder. The letters live in the firm's Workspace, in one folder. [doc:plan-v2.md section 5, "Google access"]
   - Unconfirmed: which Workspace user owns the folder. [doc:plan-v2.md section 11 item 6]
   - Unconfirmed: shared drive or plain folder. For a one-person firm the shared drive is a nicety. [doc:phase0-brief.md Q2]
3. Share it with the Google account Peter and Maria Pia actually use. That is probably `homedirectionsinc@gmail.com` for both; it is confirmed when you share the folder and they open it. [gordon 2026-10-01] [doc:plan-v2.md section 5 and section 11 item 6]
4. Unconfirmed: whether the Workspace lets a Doc in that folder be set to "anyone with the link can view". Sending a letter does exactly that. [doc:plan-v2.md section 5, "Sending a letter"] Check the sharing rules in the Admin console before the rehearsal.

### 9.2 The letter template

1. Start from the draft: "Home Directions letter template - DRAFT 2026-10-01". It sits in your own Drive, not the firm's. It has the places to fill in and the wording. It does not have the images. [doc:phase0-brief.md, "The letter template"]
2. Make the real template in the firm's Drive, in or beside the letters folder. [doc:phase0-brief.md, "The letter template"]
3. Put in the two images the draft could not carry: the letterhead at the top, and Peter's signature above his name. [doc:phase0-brief.md, "The letter template"] [doc:build-handoff.md section 6] v3 prints both today. Where each file is:
   - The letterhead: `letterhead-2025.gif`, in the `images` folder of the Home Directions plugin. [doc:current-system.md, "How a job flows" item 5] [doc:survey-hdonline-home-directions.md, image inventory]
   - The signature: `peter-signature-pe.jpg`, in the old site's uploads, under 2020/11. It is not in the plugin. [doc:current-system.md, "How a job flows" item 7] [doc:survey-hdonline-home-directions.md, "Signature and stamp"]
   - The plugin's clone is on this Mac, under `~/Dev/clc-plugins/`. [doc:build-handoff.md section 1] The signature comes from the old site's media library.
4. What the finished template carries, top to bottom: the letterhead, the date, the client and the property, "Dear ...", the body, "Sincerely,", the signature image, "Peter Seirup, P.E.", "CT License #13055", "NY License #89793", and the stamp when the property's state calls for one. [doc:phase0-brief.md, "The letter template"] [doc:plan-v2.md section 2, Stamp]
5. Leave the places to fill in exactly as they are. The app finds them by their tags, and that is how a corrected name is replaced only where it belongs. [doc:plan-v2.md section 5, "Letters"]
   - Unconfirmed: whether the built app's tags match the draft's. Sancho compares them when the letters stage is built and gives you any change.
6. One template serves all three services to begin with. [doc:plan-v2.md section 5, "Keys and passwords", last sentence]
7. The address block must still look right when a client has a name and no street address. [doc:build-handoff.md section 3, "What the planning thread learned from the real letters"]
8. Have the two stamp images ready for step 12. Both are in the same `images` folder of the Home Directions plugin: Connecticut is `peter-seirup-engineering-stamp_WEB_20231106.png`, New York is `peter-seirup-engineering-stamp_NY_WEB_20240306.png`. [doc:survey-hdonline-home-directions.md, "Signature and stamp" and image inventory]
9. The look and wording are edited in Google Docs from then on, not in the app. Peter keeps the template. [doc:plan-v2.md section 5]

**Tell Sancho:** "The letters folder exists, owned by (account), shared with (account). The template is finished with both images; its link is (link). I have the two stamp images. The test Google account is (account)."

---

## 10. The first deploy on staging

**Staging runs the app for the first time. Do this once step 4 is finished for staging.** Steps 5 to 9 can come before it or after it: the app only reports whether each connection works. [doc:plan-v2.md section 5, "Keys and passwords"]

1. Say to Sancho: "Staging is ready for its first deploy."
2. The agent pushes `staging`. Push to deploy is on, so Forge deploys it. [doc:laravel-kit-spec.md D2] [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]
3. The agent confirms three things and shows you: the commit staging reports is the one it pushed; nothing is pending in the database's migrations; the health address answers. [doc:laravel-kit-spec.md section 7, laravel-edit step 7]
4. The agent deploys a second time and confirms the database is the same one, not a new empty one. That proves the shared path of 4.3. [doc:laravel-kit-spec.md section 7 laravel-new, and section 16]
5. The agent proves staging's log is alive, then reads it. [doc:laravel-kit-spec.md section 4, log probe]
6. Open staging's address. Expect the login in front of it, then the app's own login page.

If the deploy fails, the old release stays, and here there is none: tell Sancho what Forge's deploy output says. [web:laravel.com/forge/docs/sites/deployments.md 2026-10-02]

**Tell Sancho:** "Staging deployed. I saw its login page at (address)."

---

## 11. The Google credential

**This step cannot be started yet. It is numbered so that nothing later can pass without it.** [doc:reviews/paperwork-W1.md finding 14]

Unconfirmed: the exact kind of Google credential. The plan leaves it to the start of the build, and the overnight build worked against a stand-in. [doc:plan-v2.md section 5, "Google access"] [doc:build-handoff.md section 2 item 3] Do not create one yet. Sancho brings you the steps once it is settled. What is fixed:

1. The credential on production reaches only what the app needs. [doc:plan-v2.md section 5] By Sancho's reading that is the letters folder and the backup folder, and the backup side should be able to do as little as possible. [doc:laravel-kit-spec.md 8.2]
2. No credential that can act as any user in the Workspace. That draft idea is dropped. [doc:plan-v2.md section 5]
3. The production credential exists on the production site only. It is entered in Forge on production, in step 13, and nowhere else. [doc:laravel-kit-spec.md 8.2]
4. Staging uses a separate test Google account that owns nothing real, with its own letters folder, its own backup folder, its own copy of the template and its own credential. [doc:plan-v2.md section 5] [doc:laravel-kit-spec.md 8.2]
   - Unconfirmed: whether that test account is a plain Google account or a second user in the Workspace.

**Tell Sancho, when Sancho's steps are done:** "The test account's credential is in Forge on staging. It reaches the test letters folder and the test backup folder and nothing else."

---

## 12. The app's Settings, on staging

**Fill in Settings on staging, then look at the Connections panel.** These screens exist only once staging is deployed (step 10). [doc:plan-v2.md section 5, "Screens", Settings]

1. Make the three logins: one as Peter (owner), one as Maria Pia (treasurer), one as you (admin). [doc:plan-v2.md section 4, users]
   - Unconfirmed: how the first login is made on a server. The build's own way of making the three local logins refuses to run anywhere but local and testing. [doc:build-log-app.md, stage P1 plan, item 4] Sancho says once the login screens are final.
2. Check the three invoice texts. [doc:plan-v2.md section 5, "Screens", Settings] The texts as Peter dictated them are in the requirements. [doc:requirements.md R4.2 and R4.3]
   - Unconfirmed: whether the app arrives with the three texts filled in, or you paste them.
3. Paste the link to the test account's copy of the letter template. [doc:plan-v2.md section 5, "Screens", Settings]
4. Upload the two stamp images, Connecticut and New York. [doc:plan-v2.md section 5, "Screens", Settings]
5. Check the from address. [doc:plan-v2.md section 5, "Screens", Settings]
6. Set the type map from the table in step 8: which Calendly appointment type is which service. [doc:plan-v2.md section 5, "Screens", Settings]
7. Look at the Connections panel. It shows Calendly, Brevo, Google and the two backup stores: whether each is working and when it last succeeded, with a button to test each. [doc:plan-v2.md section 5, "Screens", Settings] Press each one.

All five working on staging is the start of the dress rehearsal (`runbook-dress-rehearsal.md`).

**Tell Sancho:** "Staging's Settings are filled in. The three logins exist. Connections on staging: (each of the five, working or not)."

---

## 13. Production: the site, its keys, its first deploy, its Settings

**Only after the first ship.** The first ship is the first time the kit's ship script moves `main`, to a commit that was gated, reviewed and run on staging. [doc:laravel-kit-spec.md D2, and section 7 laravel-ship] Sancho tells you when `main` exists. If you chose the bare first commit in step 1, the site (items 1 to 4) can be made earlier; the keys and the deploy still wait for the first ship.

1. Ask Sancho the question of 4.2 again, for `main`: is the example settings file free of seed passwords? No plain yes, no site.
2. Make the production site: 4.1, then 4.2 with the Production column, then 4.3 in the same sitting. Push to deploy off. Check it twice.
3. The agent runs the check of 4.6 at once: from staging's user, production's folder cannot be read. It shows you the result. No production key goes in before that result.
4. Enter production's keys, each made today, each on the **production** site's Environment:
   - Cloudflare: production's bucket key (step 5, items 4 to 6).
   - The archive password: production's own, not staging's (step 5, item 8). Put its second copy away now.
   - Brevo: the firm's key (step 7, item 5).
   - Google: production's credential (step 11).
   - **Not Calendly.** No Calendly token goes on production until `runbook-cutover.md` Step 7.
5. Press Deploy. The agent has handed you the full commit ID. The commit Forge shows must be that one. [doc:laravel-kit-spec.md section 7, laravel-ship step 4] Afterwards the agent reads the two addresses that need no login and confirms the commit. [doc:laravel-kit-spec.md D14, and section 7 laravel-ship step 5]
6. Fill in production's Settings, as in step 12: the three logins, the three invoice texts, the link to the real template, the two stamp images, the from address. [doc:plan-v2.md section 5, "Screens", Settings]
   - Unconfirmed: whether the type map can be set while no Calendly token is in. If it can, set it now. If it cannot, it is set in cutover Step 7, straight after the token.
   - Unconfirmed: how Peter's and Maria Pia's passwords are first set and handed over. `runbook-cutover.md` Part 1.
7. Look at production's Connections panel. Expect Brevo, Google and both backup stores working. Expect Calendly **not** connected. That is right until the day. [doc:plan-v2.md section 6 step 5]
8. Do 4.5: leave the deploy hook alone, and read the key list to Sancho.

**Tell Sancho:** "Production exists at (address), branch main, push to deploy off, user (name). The example file held no seed password. Mode is production, error display is off, the app key is its own. The database path and storage are shared. The read test from staging's user failed to read production, as it should. Production's keys are in: Cloudflare, the archive password, Brevo, Google. No Calendly token. It deployed at commit (first characters). The keys on the server are: (name, user, fingerprint for each)."

---

## When the thirteen are done

1. The backups are set up and checked from `runbook-backups.md`. A restore must work before the host counts as done. [doc:plan-v2.md section 7, step B]
2. What is still left for the cutover day, on purpose: the firm's Calendly token on production. `runbook-cutover.md` Step 7.

## Not in this runbook

- Registering the kit's hooks on this Mac. It waits on you, and it must come before the Mac's key goes on staging (4.4). [doc:build-handoff.md section 6] [doc:plan-v2.md section 7, step A]
- The WordPress guard fix; what becomes of the staged real data in `~/Dev/hd-v4-import-data/`. Those wait on you too, and the build's own summary lists them. [doc:build-handoff.md section 6]
- How-tos for Peter and Maria Pia. They are written after the screens exist. [doc:build-handoff.md section 2 item 6]
- The monthly upkeep checklist: system updates, PHP patch releases and a reboot. The plan calls for one and none is written yet. [doc:plan-v2.md section 9] [doc:laravel-kit-spec.md 9.2, the monthly row] It is owed by stage W2 or by the kit track. The first one falls due a month after the server is made.
