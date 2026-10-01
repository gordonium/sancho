---
name: Copper Leaf plugin registry
type: doc
business: copper-leaf
lobe: work
status: active
description: Every Copper Leaf plugin and theme cloned in the kit: folder, version, newest release, client, status
sources: ["[doc:~/Dev/clc-plugins/]", "[doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md]"]
---
# Copper Leaf plugin registry

Built 2026-10-02 (batch B4) from the six repos cloned in `~/Dev/clc-plugins/`. Copper Leaf has about fifty private plugins and themes; this table covers only the ones cloned so far [doc:~/Dev/clc-plugins/docs/HANDOFF-plugin-dev-workflows.md:13]. Version is the file header; newest release is the top `release-notes.txt` entry; in every row the newest git tag matches the header [doc:~/Dev/clc-plugins/<folder>/.git (git tag, read 2026-10-02)]. Tooling: see `kit.md`.

| Folder | Name | Version | Newest release | Site or client | Status | Entry |
|---|---|---|---|---|---|---|
| `copper-leaf-filmadelphia-festival-calendar` | Copper Leaf Creative: Filmadelphia Festival Calendar | 1.0.0 | 2026-09-21 | Philadelphia Film Society, filmadelphia.org | active | `plugins/copper-leaf-filmadelphia-festival-calendar.md` |
| `copper-leaf-wa-learndash-customizations` | Copper Leaf: Wizard Academy LearnDash Customizations | 1.9.0 | 2026-09-21 | Wizard Academy (Ad Writers' Guild) | active | `plugins/copper-leaf-wa-learndash-customizations.md` |
| `copper-leaf-wizard-academy-deux` | Copper Leaf Creative: Wizard Academy (Deux) | 3.4.11 | 2026-09-21 | Wizard Academy | active | `plugins/copper-leaf-wizard-academy-deux.md` |
| `phillyfilm` (theme) | Philly Film | 2.0.0 | 2026-09-22 | Philadelphia Film Society, filmadelphia.org | active | `plugins/phillyfilm.md` |
| `hdonline` | Copper Leaf: HDOnline | 1.7.5 | 2026-03-24 | Home Directions, Inc. (through the extension below) | active | `plugins/hdonline.md` |
| `hdonline-home-directions` | Copper Leaf: HDOnline for Home Directions | 1.11.7 | 2026-08-20 | Home Directions, Inc. | active | `plugins/hdonline-home-directions.md` |

Sources per row, in order:
- [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/copper-leaf-filmadelphia-festival-calendar.php:4-6] [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/release-notes.txt:4-5] [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:8]
- [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/copper-leaf-wa-learndash-customizations.php:4-6] [doc:~/Dev/clc-plugins/copper-leaf-wa-learndash-customizations/release-notes.txt:2]
- [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/copper-leaf-wizard-academy-deux.php:4-6] [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/release-notes.txt:2]
- [doc:~/Dev/clc-plugins/phillyfilm/style.css:2-6] [doc:~/Dev/clc-plugins/phillyfilm/release-notes.txt:4] [doc:~/Dev/clc-plugins/phillyfilm/CLAUDE.md:1]
- [doc:~/Dev/clc-plugins/hdonline/copper-leaf-hdonline.php:4-6] [doc:~/Dev/clc-plugins/hdonline/release-notes.txt:2] [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:5]
- [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:4-6] [doc:~/Dev/clc-plugins/hdonline-home-directions/release-notes.txt:2]

Notes:
- "Status: active" means the repo is cloned and has a release in 2026; no plugin is marked retired in its own files [inferred from the release dates above].
- Pairs that ship together: Wizard Academy (Deux) defines the lesson fields the LearnDash Customizations plugin prints [doc:~/Dev/clc-plugins/copper-leaf-wizard-academy-deux/CLAUDE.md:8]; HDOnline for Home Directions extends HDOnline [doc:~/Dev/clc-plugins/hdonline-home-directions/copper-leaf-hdonline-home-directions.php:5]; the festival calendar runs inside the Philly Film theme [doc:~/Dev/clc-plugins/copper-leaf-filmadelphia-festival-calendar/CLAUDE.md:14-16].
- Default branch differs: `main` for the festival calendar, hdonline and hdonline-home-directions; `master` for the other three [doc:~/Dev/clc-plugins/<folder>/.git (git rev-parse, read 2026-10-02)].
- Only three repos carry a CLAUDE.md (festival calendar, Wizard Academy (Deux), phillyfilm) [doc:~/Dev/clc-plugins/<folder>/CLAUDE.md].
