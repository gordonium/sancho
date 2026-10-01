---
name: WordPress kit live-site guard check
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: The exact command texts handed to the Copper Leaf plugin kit's live-site guard on 2026-10-01 and what it answered; eight shapes it allows that it should refuse; evidence for laravel-kit-spec.md section 11 item P-1; nothing in the kit was changed and no server was contacted
sources: ["[sancho test 2026-10-01 late: /usr/bin/python3 ~/Dev/clc-plugins/bin/sitedistrict-live-site-guard.py, one hook-shaped JSON input per case on stdin]", "[doc:~/Dev/clc-plugins/bin/sitedistrict-live-site-guard.py at kit HEAD d15e66f, file sha256 beginning 7c96cd93a251f53a]", "[doc:wp-kit-map.md, mechanisms weaknesses]", "[sancho subagent review 2026-10-01, workflow wf_4aaefbba-f62]"]
status: evidence, then the fix: Gordon said "Go ahead and fix the WP guard hole" [gordon 2026-10-01] and seven of the eight were closed the same evening (section "The fix, as applied"); not committed; an independent review of the fix was started and its outcome is appended when it returns
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
