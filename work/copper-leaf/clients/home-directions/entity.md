---
name: Home Directions, Inc.
type: client
kind: organization
business: copper-leaf
lobe: work
status: active
since:
role: builds and runs their report and letter-writing system
lead:
brands: []
people: [peter-seirup]
description: Peter Seirup's engineering firm (P.E.); the WordPress-powered report/letter system is being replaced (project hd-system-rebuild)
sources: ["[gordon 2026-09-30]", "[rec_8d15ed467e 2026-09-29]"]
---
Home Directions, Inc. is Gordon's father's engineering firm. [gordon 2026-09-30] Gordon builds and runs its report and letter-writing system, currently WordPress-powered (repos `hdonline`, `hdonline-home-directions`), and is replacing it. [gordon 2026-09-30; rec_8d15ed467e 2026-09-29] Home Directions is a Copper Leaf client for this work. [gordon 2026-09-30] Dev clone of the current site for Sancho's use: https://hdonline-sancho.sitedistrict.com/ [gordon 2026-09-30] (SiteDistrict; SSH alias and staging facts to be registered per the kit when the Nerd sets them up).

The dev clone is a copy of live data. [gordon 2026-09-30] Peter is WordPress user 5 and the only inspector. [gordon 2026-09-30] **The home-inspection side of the business is being retired entirely**; the rebuild is for what remains (engineering/consultation work). [gordon 2026-09-30] Public site: https://homedirections.net (bot protection is strict; read it through Chrome, not fetch). [gordon 2026-09-30]

Google: the firm has Google Workspace Business Starter on homedirections.net; the super admin is office@homedirections.net. [gordon 2026-10-01] Public DNS agrees that Google hosts the domain's mail (MX, SPF, a Google DKIM key) and shows Brevo also authenticated as a sender on the domain; DNS is at Cloudflare. [dns:homedirections.net 2026-10-01] Which mailbox Peter works in is not yet stated. (Superseded 2026-10-01 late: "Peter uses homedirections@gmail.com most often, but I think that box checks office@homedirections.net" [gordon 2026-10-01]; that the Gmail box collects office@ is Gordon's belief, to be confirmed by a test message.)

The systems, oldest first [gordon 2026-10-01]: a pile of Word files and an MS Access database ("the booking system"); **v1, "legacy"**, thought to be live nowhere now, perhaps recoverable from backups; **v2, built by Grayson**, still live at hdonline.homedirections.net/hdonline/; **v3**, the current WordPress system (repos `hdonline`, `hdonline-home-directions`). Around 2015 a bug in v2 deleted a note from every report whenever it was unchecked in one; after recovery Gordon puts the loss at about 3 percent and wants the backups audited to shrink it. [gordon 2026-10-01] Because of that bug, nothing is ever clicked in v2: it is read, never operated.
