---
name: WordPress kit live-site guard check
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The exact command texts handed to the Copper Leaf plugin kit's live-site guard on 2026-10-01 and what it answered; eight shapes it allows that it should refuse; evidence for laravel-kit-spec.md section 11 item P-1; nothing in the kit was changed and no server was contacted
sources: ["[sancho test 2026-10-01 late: /usr/bin/python3 ~/Dev/clc-plugins/bin/sitedistrict-live-site-guard.py, one hook-shaped JSON input per case on stdin]", "[doc:~/Dev/clc-plugins/bin/sitedistrict-live-site-guard.py at kit HEAD d15e66f, file sha256 beginning 7c96cd93a251f53a]", "[doc:wp-kit-map.md, mechanisms weaknesses]", "[sancho subagent review 2026-10-01, workflow wf_4aaefbba-f62]"]
status: evidence, then the fix: Gordon said "Go ahead and fix the WP guard hole" [gordon 2026-10-01] and seven of the eight were closed the same evening (section "The fix, as applied"); not committed; an independent three-reader review of the fix then found more holes, older ones included, and a second round closed those too (last section)
---
# Live-site guard check (2026-10-01)

## What was done
The guard is the hook that stops a shell command reaching a live client site on SiteDistrict. [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md §6.1] Each case below was handed to the guard script the way the hook hands it a command: as JSON on standard input, read from a file. The script only reads text and answers; **no command was run and no server was contacted.** Host and folder names are made up, except that `host-2.sitedistrict.com` is the real naming pattern the guard recognises. This is a manual check, not an automatic test; the cases belong in the guard's own test file when it is fixed.

## Results

| Case | The remote command, as written | Should be | Guard said |
|---|---|---|---|
| C1 control | `cd ~/sites/example-dev.sitedistrict.com/www && ls -la` | allow | allow |
| C2 control | `cd ~/sites/liveclient.com/www && ls -la` | block | block |
| C3 control | `cd ~/sites/example-dev.sitedistrict.com/www ; rm -rf public_html` | block | block |
| H1 | `cd ~/sites/example-dev.sitedistrict.com/www && ls ; rm -rf public_html` | block | **allow** |
| H2 | `cd ~/sites/example-dev.sitedistrict.com/www && ls \|\| rm -rf sites` | block | **allow** |
| H3 | `cd ~/sites/example-dev.sitedistrict.com/www && crontab -r` | block | **allow** |
| H4 | `cd ~/sites/client-sitedistrict.community/www && ls` | block | **allow** |
| H5 | `cd ~/sites/example-dev.sitedistrict.com/www && tar xf a.tar -C/home/coppergordonsd/sites` | block | **allow** |
| H6 | `cd ~/sites/example-dev.sitedistrict.com/www && ls` then a line break, then `rm -rf public_html` | block | **allow** |
| H7 | `cd ~/sites/example-dev.sitedistrict.com/www && ls & rm -rf public_html` | block | **allow** |
| H8 | the C2 command (a live folder), with the program written `/usr/bin/ssh` instead of `ssh` | block | **allow** |

Every case was sent as `ssh coppergordonsd@host-2.sitedistrict.com '<remote command>'`, except H8 which begins `/usr/bin/ssh`.

## What the holes mean

- **H8 is the widest.** Writing the program by its full path takes the command out of the guard's sight altogether: the same command that is blocked as `ssh ...` is allowed as `/usr/bin/ssh ...`, live folder and all. The guard looks for the bare tool words. [bin/sitedistrict-live-site-guard.py:340-349]
- **H1, H2, H6, H7: anything after the first real command is unchecked.** The guard checks that the remote command *starts* with `cd <staging> &&`. [bin/sitedistrict-live-site-guard.py:232] If the staging folder name is mistyped in a way that still contains `sitedistrict.com`, the `cd` fails, the `&&` part is skipped, and whatever follows `;`, `||`, a line break or `&` runs in the home folder, which holds every live site. C3 shows the guard does catch `;` when it comes straight after the `cd`; it does not once a command sits between.
- **H3: the guard limits where, not what.** Staging and live share one login on a host [HANDOFF §4], so an account-wide command (the scheduled-jobs table here) reaches live from a staging folder.
- **H4: staging is recognised by "contains", not "is".** [bin/sitedistrict-live-site-guard.py:210]
- **H5: an absolute path directly after a flag letter is not seen.** [bin/sitedistrict-live-site-guard.py:260]

A subagent reader also reported, and Sancho did not test: the guard allows the command when it cannot read its input; a crash or a timeout would also let the command through; the 37 tests pass only because this Mac's SSH config defines two real aliases; the self-test hook does not fire when the guard is changed from the shell. [doc:wp-kit-map.md, mechanisms weaknesses]

## The smallest fix (a proposal)
1. Recognise `ssh`, `scp`, `rsync` and `sftp` with or without a path in front.
2. After the leading `cd <staging> &&`, refuse `;`, `||`, a single `&` and any line break. (The connection check the edit skill uses names no folder and is judged by a different rule, so it is not affected.)
3. Match the staging folder against an explicit list, not a substring.
4. Catch an absolute path glued to a flag.
5. Add the eight cases above to the guard's test file, with a fixture SSH config so the tests do not depend on this Mac.
The verb problem (H3) has no small fix inside a path checker; it is an argument for the allowlist design in the Laravel kit spec, section 8.3.

## The fix, as applied (2026-10-01 late)

Gordon: "Go ahead and fix the WP guard hole." [gordon 2026-10-01] Changed in `~/Dev/clc-plugins`, in the working tree, **not committed**:

- `bin/sitedistrict-live-site-guard.py`
  - Rule A: the program is recognised by its bare name or as the last part of a path, so `/usr/bin/ssh` counts (H8).
  - New Rule N: after the opening `cd <staging> &&`, a `;`, a `||`, a single `&` or a line break is refused, anywhere in the rest of the command, quote marks or not (H1, H2, H6, H7). Output redirection of the form `2>&1` is not counted as a single `&`.
  - Rule D and the staging path pattern: a staging folder name must **end** with `.sitedistrict.com` (H4). Checked against host-2, where all six staging folders do.
  - Rule I: an absolute path glued onto an option is caught (H5).
  - The header documents the changes, and the "honest limit" now names what is still open: account-wide verbs (H3), a script on this Mac that itself runs ssh, and that the guard does not understand quoting.
- `bin/sitedistrict-live-site-guard-tests.py`: twenty new cases, written with the server named in full so they do not depend on this Mac's SSH config; one existing case changed (`php -r "...;"` became `php -v`, because a `;` inside quotes is now refused on purpose). 57 cases, all pass.
- `CLAUDE.md` section 10 and `skills/plugin-edit/SKILL.md` Step 2: the lines that tell an agent how to write a remote command now say the same as the guard.

Re-run of the table above against the fixed guard: C1 allow, C2 block, C3 block, H1 block, H2 block, **H3 allow (still open, by design)**, H4 block, H5 block, H6 block, H7 block, H8 block.

What the fix costs in ordinary use: an ssh command to a staging site must be one line on its own, chained with `&&` only. A multi-line shell call with an ssh line in it, or a trailing `; echo done`, is now refused, with a message saying what to do instead.

Not changed, and still as the reader reported them: the guard allows a command when it cannot read its input, and a crash or timeout lets a command through; the self-test hook fires only on Write and Edit. These are design choices recorded in the guard itself or in the hook, and are items for the shared guard core in `laravel-kit-spec.md` section 8.3.

## The independent review of the fix, and the second round (2026-10-01 night)

Three readers who had not written the fix: one hunting ways past the guard, one hunting ordinary documented work the fix now refuses, one reviewing the code. Between them they ran 496 command texts through the guard (as text; no server contacted). [sancho subagent review 2026-10-01, workflow wf_e0959670-dcd] Verdicts: "not ready", "sound with fixes", "sound with fixes". 32 findings: 5 blockers, 9 major, 18 minor.

**The blockers were holes that the first round had not closed. Four of the five are older than today's change.** Each is something an agent could write by mistake:
- **A connection check with a second line.** `echo ok`, a line break, then any command made of plain words: allowed, and it runs in the home folder, beside every live site. The rule for commands that name no folder split on `;` and `&&` but not on line breaks, and the `echo` pattern swallowed the next line as echo's own words.
- **`find / -name wp-config.php`, `du -sh /*`, `ls //home/...`.** The absolute-path rule needed a letter after the slash, so the root folder itself, and any path starting `//` or `/` then a digit, dot or star, was not seen.
- **`rm -rf $PLUGIN_DIR/*`.** Shell variables do not survive from one call to the next, so the variable is empty and the server receives `rm -rf /*`.
- **`wp --ssh=<server>:~/sites/<live site> ...`.** WP-CLI's own way of running over ssh; the word "ssh" glued to dashes was not seen.

**Second round, applied the same night** (same files, still not committed):
- Connection checks must be one line (Rule M).
- The root folder, and `/` followed by anything but a letter, are refused (Rule I). The glued-option check now also covers digits in the option and `//`.
- A variable followed by `/`, and `$OLDPWD`, are refused (Rule H).
- `wp --ssh=` aimed at a SiteDistrict server is refused outright, with the message saying how to write it as an ordinary ssh command.
- The server and the program are recognised in capital letters, and a server name with a trailing dot is still that server.
- Rule N's message now says plainly that it covers everything after the server name, the closing quote included, and that rewriting the command as the message describes is the expected fix. (The first-round message told the agent how to rewrite and, in the same breath, not to rephrase.)
- The regular expressions added today are explained piece by piece, as the kit's Readability Rule asks.
- Tests: 86 cases, all pass. The 49 added today name the server in full and pass with an empty home folder; the 37 older ones still depend on two nicknames in this Mac's SSH config, and the test file now says so.
- `skills/plugin-edit/SKILL.md` Step 2 lists each newly refused shape with its rewrite; the handoff's section 6.1 carries a dated note.

**Check that nothing got looser:** all 496 reviewer cases were run against the guard as it was this morning (from git) and as it is now. None that was blocked is now allowed. 164 that were allowed are now blocked: the holes, and the false alarms below.

**What the fix costs.** The regression reader found 44 ordinary command shapes that the first round newly refuses, all with a rewrite that passes. The common ones: anything after the closing quote of an ssh command other than `&&`, a pipe or a redirection (`; echo done`, `|| true`, a loop around ssh); a `;` or `&` inside a quoted URL, SQL statement, PHP snippet or browser user-agent string; `|| echo ...` after a `grep` that may find nothing. Two per-project files document workflows that now need rewording and were **not** edited, because they are plugin repos: `phillyfilm/CLAUDE.md` (server-local `curl` with a Chrome user-agent, which contains `;`) and `copper-leaf-filmadelphia-festival-calendar/CLAUDE.md` (lint over stdin in a loop). The rewrites are in plugin-edit Step 2.

**Still open, and now written in the guard's own "honest limit":**
- an account-wide command after a valid `cd` (H3 above);
- a script file, on staging or on this Mac, that itself does the damage;
- anything that travels over ssh without being one of the four programs: `git push` to a server path, sshfs, autossh, a WP-CLI `@alias`;
- a server named by its number address;
- deliberate disguise: a backslash inside the program name, a variable holding it, a quote trick after a staging folder name, a decoy first mention of the server.
- Not changed, by design choice recorded in the guard: when it cannot read its input it allows the command; a crash or timeout lets the command through. The reviewers confirmed these behave as before.

**One thing for Gordon to settle in the rules file.** `CLAUDE.md` section 10 says: if the guard blocks you, do not rephrase, stop and tell Gordon. The guard's Rule N message and plugin-edit now say that writing the command the way the message describes is the expected fix. Both are consistent with the file's own "how to write remote commands so the guard accepts them", but the sentence in section 10 reads more strictly than that. It was left as it is.
