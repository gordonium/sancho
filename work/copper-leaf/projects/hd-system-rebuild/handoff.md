---
name: Handoff · HD rebuild thread
type: doc
business: copper-leaf
entity: work/copper-leaf/projects/hd-system-rebuild/
lobe: work
description: Handoff from the Sancho-build thread to a dedicated Home Directions thread, 2026-10-01; where the plan stands, what is decided, what to do first
sources: ["[gordon 2026-10-01]", "[doc:docs/plan.md]"]
---
# Handoff: Home Directions v4 thread (2026-10-01, from the Sancho-build thread)

Scope of this thread: `work/copper-leaf/projects/hd-system-rebuild/` and `work/copper-leaf/clients/home-directions/`. The Sancho-build thread keeps `_setup/`, `_queue/`, `_design/`, `skills/`.

Read in this order: `docs/plan.md` (the draft, with picks and 15 numbered questions), `docs/requirements.md` (R1 to R8, cited to the 09-29 transcript), `docs/current-system.md`, then the two surveys only when a detail matters.

Decided: nothing in the plan is approved yet; the picks are Sancho's. Confirmed facts: Peter is WP user 5 and the only inspector; the home-inspection side is retired entirely; the dev clone `hdonline-sancho.sitedistrict.com` is a copy of live; the public site is homedirections.net (read it through Chrome; bot protection blocks fetch). [gordon 2026-09-30]

Not yet done: the data census on the dev clone (the Chrome tab reached the login page only; Gordon must log in in the tab Claude opens). Phase 0 = questions 1 to 3 (stack, Google Workspace, hosting).

Rules that bite here: the Nerd builds, Cowork plans; nothing is written to the plugin repos or the dev site from this thread; no tasks created for Gordon; cite every fact; the plan is approved by Gordon before step 1 becomes a job.

Added 2026-10-01 late, after Gordon asked why the census needed his permission ("Go ahead and census. (And why did you have to ask for my permission on that?)" [gordon 2026-10-01]):
- **Reading the dev clone needs no permission**: its pages through the logged-in Chrome, and its database through read-only `SELECT`s over SSH on host-2 (alias `wizardacademy-dev`; the clone's folder is `hdonline-sancho.sitedistrict.com`). The thread's "nothing is written to the dev site" is about writes. What went wrong: this thread read "the SSH alias is not set up" in an older note [doc:docs/current-system.md], did not look in `~/.ssh/config`, and filed a read as the Nerd's job. Check: before calling anything "blocked on access", list what access exists.
- **v2 (hdonline.homedirections.net) is read, never operated.** No click, no form, no checkbox: a v2 bug deletes a note from every report when it is unchecked in one. [gordon 2026-10-01]
- **Exceptions Gordon has made to "nothing is written to the plugin repos":** the live-site guard fix in `~/Dev/clc-plugins/bin/` ("Go ahead and fix the WP guard hole" [gordon 2026-10-01]). Nothing else.
- Where things stand and what was produced on 2026-10-01: `project.md` notes, and `docs/phase0-brief.md` Decisions.
