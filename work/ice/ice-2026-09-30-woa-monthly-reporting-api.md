---
name: Monthly reporting data for WoA clients, gathered by API
id: ice-2026-09-30-woa-monthly-reporting-api
title: Monthly reporting data for WoA clients, gathered by API
type: idea
lobe: work
area: wizard-of-ads
project:
description: Monthly reporting data for WoA clients, gathered by API
captured: 2026-09-30
source: "[gordon 2026-09-30]"
status: captured
next_review: 2026-11-02
log:
  - 2026-09-30 captured from _design/seeds/work-ice.md
---
# Monthly reporting data for WoA clients, gathered by API
- **Area:** wizard-of-ads. Per client.
- **What:** pull Google Search Console, GA4, Google Business Profile, Local Services Ads, and Google Ads data monthly into a per-client report; **fetch the LSA Phone Responsiveness score via API**, which alone replaces a $160/month tool.
- **Review questions:** which client folders need which sources (a `reporting:` block in `entity.md`); OAuth for five Google APIs on the Mac (one Google Cloud project, one consent, tokens in the encrypted secrets file); output template per client; the Phone Responsiveness fetch is the obvious first MVP because the ROI is immediate and it's one API. Runs as a scheduled command on the Mac; the report draft is a skill.
