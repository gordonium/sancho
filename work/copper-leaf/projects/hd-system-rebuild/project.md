---
name: Home Directions system rebuild
type: project
lobe: work
area: copper-leaf
status: active
recurring:
goal:
wrike_project:
next_action: {text: "Stack decided (Laravel). Sancho: hosting options with a pick (docs/hosting-options.md), the Laravel kit spec with the updates schedule (docs/laravel-kit-spec.md), then question 2 (Workspace) with Gordon; census on the dev clone still needs Gordon's login in the Chrome tab", set: 2026-10-01}
waiting: []
job:
description: Replace Home Directions' WordPress report/letter system (Phase 1 plan and build), then assimilate the legacy systems and data (Phase 2)
sources: ["[gordon 2026-09-30]", "[rec_8d15ed467e 2026-09-29]"]
---
# Home Directions system rebuild
Phase 1: plan thoroughly, then build the new system. Phase 2: assimilate all legacy systems and data into it, as discussed in the 2026-09-29 meeting. [gordon 2026-09-30] "We need a thorough plan before we build. I expect it will require quite a bit of conversation." [gordon 2026-09-30]
## Notes
- 2026-10-01 · overnight: both repos surveyed end to end (docs/survey-*.md), homedirections.net read, transcript reduced to requirements.md (R1 to R8, cited by timestamp), plan.md drafted (stack pick Laravel, data model, Docs and email mechanics, build order with gates, Phase 2 migration, 15 numbered questions). Dev clone data not yet read: the Chrome tab landed on the login page. [sancho 2026-10-01]
- 2026-10-01 · evening, HD thread: docs/phase0-brief.md written for questions 1 to 3. New facts: mail for homedirections.net is already hosted by Google (MX, SPF, DKIM) and Brevo is already authenticated on the domain [dns 2026-10-01]; SiteDistrict is WordPress-only by its own site [web:sitedistrict.com 2026-10-01]; Laravel 13 is current, not 12 [web:laravel-news.com]. Five corrections to plan.md recorded in the brief. Census still waiting on Gordon's login in the Chrome tab. [sancho 2026-10-01]
- 2026-10-01 · evening, decisions: **stack is Laravel** [gordon 2026-10-01]; the database must also house all legacy data back to the early 1990s (R7.8) [gordon 2026-10-01]; a Laravel skill harness is to be built alongside the WordPress kit and the two compared perpetually [gordon 2026-10-01]; an updates schedule for this and all future Laravel projects [gordon 2026-10-01]; hosting open, Cloudflare edge asked about [gordon 2026-10-01]. Full quotes in docs/phase0-brief.md, Decisions.
