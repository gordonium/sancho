---
name: Home Directions v4 build, questions for Gordon
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Every question the build's agents left for Gordon, in their own words, by stage, with what each stage reported as not done; compiled by script from the agents' reports so none is lost
sources: ["[doc:build-state.md]", "[doc:build-log-kit.md]", "[doc:build-log-app.md]", "[doc:build-log-paperwork.md]"]
status: compiled 2026-10-02 15:40 from workflow 1 (run wf_49719010-123); the agents' wording, not yet sorted by Sancho; the earlier fifteen questions (runbooks and P1) are in build-state.md
---
# Questions for Gordon from the build

These are the agents' own words. Where an agent gave a pick, it is theirs, not Sancho's. The detail behind each is in the stage's section of the build log.


## Kit: guard fixes (K1 fixes)

1. Finding 19: add the GitHub pages that commit to main, cut a release or make a repository, and GitHub's API paths, to the guard's refused list? The exact lines are in the log. Pick: yes.
2. Herd ships a `forge` program on this Mac, and it is on the PATH of the shell Claude's tools use. Leave the file (the guard refuses it once registered, and it holds no token) or delete it? Pick: leave it, and never run `forge login` here.
3. Register the three hooks for the whole Mac, or in each project's own settings? For the whole Mac a broken guard stops every session, Sancho's unattended ones included. Pick: the whole Mac, as designed.
4. Forge's documentation and price pages live on the panel's own host, which the guard refuses whole, so the monthly re-read of source pages cannot fetch them. Allow those paths or keep the host shut? Pick: keep it shut until the updates stage needs them.
5. GitHub over port 443 uses another name (ssh.github.com) that is not on the 'left to another guard' list. Add it? Pick: only if the usual port is ever blocked.
6. Can a session that does not run on this Mac (a cloud session, a remote agent) push main? It passes none of these hooks. This needs an answer before the first ship.
7. Before the hooks are registered, Sancho's side must be told, so a refused pipeline run is noticed and not silent (must-never 10). That step belongs to the thread that owns _setup/.

Reported as not done:
- A git pre-push hook in the project template (the review's second suggestion for finding 3) is not built. It would also stop a push of main from a script, an alias, a tag with a plain name, or a bare `git push` after a `cd` made in an earlier call. It needs changes to K2's template, ship script and project check, which have not had their review yet. It is a request to the stage that reviews and fixes K2 and K3 (kit handoff, section 6).
- Nothing is registered, so every hook fact (what exit code 127 or a timeout does, whether the hook's cwd follows a cd, whether subagents pass the hooks) is read, not tried.
- The WordPress kit was not opened, so whether one of its workflows uses an ssh option now refused for hosts left to another guard (-J, -W, -L, -F, -o HostName=, -o ProxyCommand=) was not checked.
- `artisan env` and `artisan about --json` on staging were left allowed (finding 10 asked to refuse them); neither was tried on a real app.
- For K3: the table 'What each mechanism rests on today' in the kit's CLAUDE.md has rows that say 'not built: build step 6'. They must be changed in the commit that builds the skills and plan-gate hooks; the lint checks a row exists, not that it is still true.
- For K3: any new hook needs its exact command text in bin/check-registration.py, and any new slow test must be named in bin/guard-selftest.py.

## Kit: skills and hooks (K3)

8. Register the three plan-gate hooks only after the overnight build has finished? Once on, any change to a project without a job file is refused, and the build's agents write into hdonline-v4 with no job file. Pick: yes, wait.
9. After registering, try the plan stamp once (installer step 8): approve a one-line plan and see whether the record holds the text. That settles the one row labelled instruction.
10. The plan gate fails open for shell commands and for the kit's own files when it cannot run. Keep that, or fail closed like the guards? Pick: keep.
11. migrate:rollback on staging: always refused, or allowed on your recorded say? Pick: leave refused until a staging server exists and a rollback is first needed.
12. Who runs bin/whats-due.py on a schedule and surfaces its exit code? That wiring is Sancho's side.
13. The WordPress skills still trigger on bare words ('ship it', 'review this'). Tighten them (existing proposal P-9)?
14. Is 'bring the closed job records forward with the next job' acceptable, or should the ship script write the closing lines before it moves main?

Reported as not done:
- The migrate:rollback exception on staging that K1 and K2 handed to K3 (it loosens a just-fixed guard rule and the brief does not ask for it; the job file has the 'Rollback approved: Gordon <date>' line it would read).
- A laravel-new skill (the spec lists it; the brief names five chain skills plus update and parity; bin/laravel-new.py exists from K2).
- No hook registered, no skill or agent linked, nothing pushed: all are printed installer steps.
- No live trial of any hook: whether the stamp hook is handed the plan's text, whether its message is shown, the effort field, and the three-tool agent were read in documentation or the installed program, not tried.
- The first parity review and any proposal for the WordPress kit (build step 9).
- The calendar's source pages were not re-read today; dates are the spec's and the research's from 2026-10-01. Node line and server OS for hdonline-v4 are not recorded.
- The git pre-push hook in the project template (left by the K1 fix for the K2/K3 review stage) is still not built.
- No skill has run a real job (that is the pilot, step 8).

## Kit: fixes after the K2 and K3 reviews

15. The first app's test config: if hdonline-v4/phpunit.xml holds only force="true" on its <env> lines, a database named in the shell is still the one its tests use (proved with real PHP on the template). Should the app track add the <server> lines and try it? I did not open the app.
16. Fit 7: laying the template over the first app needs a stage of its own. Until then do not run laravel-new.py --apply there. Who owns that stage?
17. Add three GitHub pages to the refused list (the page that grants an application access, cloud workspaces, a repository's deployments)? It is a change to your rules file.
18. Narrow the refused GitHub Actions and branch pages to Copper Leaf's own repositories? Today they are refused for every repository.
19. A push from a folder held in a variable (cd "$PLUGIN_DIR" && git push ...) stays refused everywhere on this Mac. The two reviews disagree. If the WordPress ship skill writes its pushes that way, the Laravel guard will refuse them once registered. I may not read that kit. Check before registering, or allow it when the session is not in a kit project?
20. May a Laravel job ever be moved to a cloud session, or have auto-merge switched on? Both tools are refused by name in a kit project today.
21. Does the app show its plan approval dialog in auto mode? The installer's step 8 is the try-out and needs you. Until it is known, no stamp is written in bypass mode, and auto mode still stamps.
22. Do you want a real wall around the plan stamp store (the stamp written by something the session cannot write as)? Today it is a hook plus instruction.
23. Should the kit's self-test run only in sessions that stand in the kit folder? Today it runs after any change in any session, and its message says who it is for.
24. Fit 15: who owns the words "ship it" when both kits are linked: proposal P-9 on the WordPress descriptions, or laravel-ship naming them for projects under ~/Dev/clc-laravel?
25. Fit 21b: the backup before a deploy. The plan says the encrypted archive in two places elsewhere; the template makes a checked copy on the same disk. Which is it?
26. Fit 25: set Laravel Boost up in the template (it rewrites CLAUDE.md), or leave it as a package only?
27. Zero-downtime deployment must be on for both sites, and the deploy box must hold only the host's fetch lines and "bash deploy.sh". Will you confirm both on the first staging site?
28. Is the guard's new strictness acceptable? A note after a command that names ssh, gh or forge is refused (put it on its own line); curl piped into a shell is refused; a call over one megabyte is refused; the ship script watches production for at least ten minutes; the gate will not run until composer install follows a lock change.

Reported as not done:
- Fit 7: the template was not laid over the first app (hdonline-v4). It needs a stage of its own. I did not open the app.
- Fit 15: which skill owns the words "ship it" once both kits are linked. Gordon's decision.
- Fit 25: Laravel Boost is installed by the template and not set up (setting it up rewrites CLAUDE.md). Gordon's decision; the skill no longer promises its search.
- Fit 21b: the backup before a deploy is still a checked copy on the same disk, not the encrypted archive the plan names. Already a question in the paperwork log.
- Fit 26a: "what is due" still reads PHP from composer.json, not from the server. It errs toward a false alarm.
- Nothing was tried against a registered hook: none is registered. Whether the app shows its plan approval dialog in auto mode is still unknown.
- The pre-push hook is in the template only. It is in no real project yet and must be switched on once in each clone (git config core.hooksPath .kit/hooks).
- The lines for Forge's deploy box (.kit/deploy-box.txt) and a two-word FORGE_COMPOSER are unconfirmed until the first real staging deploy.
- 18 attack cases are still allowed: 13 are inside the honest limit, 2 are deliberate disguises, 3 wait for Gordon. 10 are still refused: 8 kept on purpose, 2 wait for Gordon.
- A deliberate forgery of a plan stamp through a program is not stopped. The documents now say "instruction".
- 23 small clc-gate-report-test folders from before the fix of fit 27 are still in the Mac's temporary folder. I could not tell whose they are, so I left them.

## App: letters, invoices, mail (P2)

29. Should a correction change letters already sent? Today a corrected name or mailing address is written into every letter that client has, old jobs included; the PDF kept at sending does not change.
30. Which date belongs at the top of a letter: the job's date (as now) or the day it is sent?
31. Should Send and Mark paid ask 'are you sure?', and should a payment recorded by mistake be undoable? Today each is one click and a payment cannot be taken back.
32. Which Google user does the app sign in as? It must read the template and own the letters.
33. Are the 'how to pay' lines and the letterhead taken from the old system still right? They also put the Treasurer's name and the firm's Gmail address in the repository (P1 question 8).
34. Should anyone but the client and the office get the invoice? Today people 'copied' on a job get the letter only.
35. If a gate is ever put in front of the site, it must let through POST /hooks/brevo and GET /stamps/... (Brevo's reports and Google's fetch of the stamp image).

Reported as not done:
- Nothing was sent to Google or Brevo; the full list of what that leaves unproven is in the log under 'What cannot be proven until the real Google and Brevo accounts exist'.
- No screen was looked at in a browser; I did not log in to a running copy. Panels are tested on their HTML only.
- http://hdonline-v4.test did not answer at all at 09:15; Herd's services need Gordon's restart.
- No confirmation prompt on Send or Mark paid, and no undo for a payment recorded by mistake: not in the documents, asked as a question.
- From address as a Setting, Calendly map, users and Connections panel are P3's.
- The Mac's storage/logs/laravel.log still holds about 11,000 lines of earlier test noise (invented data, no password); left as is, ignored by git.

## App: fixes after the P2 reviews

36. Hourly design work: where do the hours go? An hours box beside the rate (total worked out once and stored), or a price that starts empty? Today the price starts at one hour ($475), the file says so, and the invoice cannot go until '[period]' is replaced.
37. Old invoices not yet paid at cutover: numbered by a person, one at a time from the file screen (as built), or all of them by the import? The old data may show many long-paid invoices as unpaid, which is why the import numbers none.
38. Should the company print under the person's name on the invoice and at the head of the letter? Today it shows only when nobody is named.
39. A Connecticut or New York letter is refused until its stamp is in the Doc. Right? If Peter places the stamp by hand, he must choose 'No stamp' on the file.
40. A letter already sent keeps its stamp image when a new one is uploaded in Settings. Right, or should old letters take the new image at their next correction?
41. When a payment recorded by mistake is taken back, nothing is sent to the client, even if a paid copy went out. Right?
42. HD_MAIL_LIVE_HOST is one more line to enter on production at go-live (the site's own name); it belongs in the cutover runbook. Agreed?
43. The app repository still has a second working tree and a branch p2-build from the first P2 builder (three commits, superseded). Remove both before the first push? Sancho's pick: yes.

Reported as not done:
- Plan-fit 13 (company under the person's name on invoice and letter): not built; Gordon's to say.
- Plan-fit 19, the parts only a real Google can show: the look of a line after a fill (insert first, then delete), the credential's reach, the refresh token's life.
- Plan-fit 11, one part: a name in a script with no Latin spelling still becomes 'client' in the Doc's name.
- Plan-fit 9, one case remains by its nature: if Brevo refuses after the Doc was shared, the Doc stays shared; the message log says 'Not sent' with the reason. Sharing writes no history line.
- Two processes racing for one invoice number are not run in the suite; the mechanism is tested (the number is read inside a transaction).
- The fix for a lost template copy (the mark in Drive's appProperties and the lookup) is written against Google's manual and tested against faked answers only.
- No screen was looked at in a browser; the new notices and confirmations are tested on their HTML.
- The leftover working tree and branch p2-build in the app repository (first P2 builder, three commits, superseded by dadcc67) were left alone: not mine to remove.
