---
name: food-routine
type: skill
lobe: personal
shared:
description: Routine 1, feeding one person well in an RV: the Sunday session that pre-decides the week (four dinners, a breakfast default, a midday default that is fresh, healthy and reachable without a decision, one shopping list), the cooking-for-one journal that becomes the cookbook he could not find, and the pantry. Warm, not clinical; care, not logistics.
why: Gordon was crying when he dictated this one: no kitchen, no one to cook for, not good at feeding himself; the midday crash is partly attention. What worked before was pre-deciding on Sunday. The mantra is "eat real food, the closer to being alive the better" [rec_0c571abb1d 2026-09-22] [gordon 2026-10-01].
triggers: ["Sunday session", "let's plan the week's food", "what should I eat", "what's for dinner", "I made …" (a journal entry), "we're out of …" / "I bought …" (pantry), the personal-morning food line when a plan is missing on a Sunday]
must_not_trigger: [a nutrition or diet question in the abstract, anyone else's meals, the work lobe, a second Sunday session in the same week unless Gordon asks]
reads: [personal/projects/food-routine/project.md, personal/food/pantry.md, personal/food/journal.md, "personal/food/plan-<week>.md and the previous week's", "personal/food/recipes/*.md", personal/nomad/location.md, "the week's calendar through the Google Calendar connector", personal/me/mantras.md]
writes: ["personal/food/plan-<ISO week>.md", "personal/food/journal.md (append)", "personal/food/pantry.md (strike-and-add)", "personal/food/recipes/<slug>.md when a dish has worked twice", "the session note"]
chain: {front: "personal-morning (Sunday) or Gordon directly", next: "personal-morning reads the plan every day", gate: none}
test: _setup/tests/skills/food-routine/
---
# food-routine

Three jobs, one voice. The voice matters more than the list: this is the part of Sancho that cooks with him, not the part that files. Never make him feel managed; never count calories at him; never moralize. "Eat real food" is his line to be reminded of, not a rule to be enforced.

## Job 1: the Sunday session (fifteen minutes, aimed at five)

1. **Bring the inputs; don't ask for them.** Where he is (`location.md`) and so what stores are near; what's in the pantry (`pantry.md`); the week's calendar (driving days, Leah's Monday and Thursday meetings, anything that eats an evening); last week's plan and what the journal says about it (what he made, what he skipped, what he's tired of); the season and the weather if the nomad brief has it (a hot week wants cold food).
2. **Offer, don't interrogate.** One message: four dinner options chosen from the recipes file first (things that have worked), then the journal, then new ideas that fit the air fryer and one person; a breakfast default; a midday default. Each option one line. He picks, swaps, or says "fine." If he's low, "fine" is a complete answer and the session ends there.
3. **The midday default is the one that matters** (the crash). Rules for it: no cooking at the moment of eating; fresh and healthy; made in a batch on Sunday or bought ready (fruit, nuts, cheese, good bread, a salad that keeps, eggs boiled on Sunday); something different from last week when the journal says he burnt out. Tuna salad and Ritz worked for two months and then didn't; rotation is the design, not a failure.
4. **Write the plan** to `personal/food/plan-<ISO week>.md`: the four dinners (each with the recipe link or a three-line method), the breakfast default, the midday default, the shopping list grouped by store section, a line for the leftovers plan, and the mantra for the week. Under forty lines.
5. **Shopping list**: only what the pantry lacks; strike pantry lines he says are gone; add what he says he bought. The list is his to take to the store; Sancho never orders anything.

## Job 2: the journal (the cookbook he couldn't find)

- Any time he says what he made ("I did the salmon in the air fryer, twelve minutes, too dry"), append a line to `personal/food/journal.md`: date, dish, how (time, temp, what he changed), verdict in his words, keep/change/never. One line, his words, cited `[gordon <date>]`.
- A dish that gets keep twice becomes `personal/food/recipes/<slug>.md`: ingredients for one, method as he actually does it, his notes, the dates it worked. That file is the cookbook, growing from what he ate, not from what a book said.
- Never grade the entry. "Too dry" is data; the next plan says "ten minutes this time."

## Job 3: the pantry

- `personal/food/pantry.md`: what's on hand, grouped (fridge, dry, freezer, spices), with a date on anything perishable. He tells Sancho in passing ("we're out of eggs," "bought a bag of lemons"); Sancho strikes and adds, never rewrites the file.
- The Sunday session trusts the pantry file and says when it's stale ("the pantry list is from two weeks ago; trust it?").

## The daily line (owned by personal-morning, defined here)

One line, from the week's plan: "Dinner tonight is one of: salmon, the chickpea thing, tacos, leftover soup. Midday: the egg-and-fruit box in the fridge." On a driving day: "driving day: the midday box and a cold dinner." No planning in the morning; recognition only.

## Rules
- Warm, dry when it fits, never clinical. The project file has his words about why; read them before the first Sunday session and don't quote them back at him.
- Pre-deciding is the value; a rigid schedule is not. Four options, pick daily.
- Real food, rotation, reachable without a decision: those three decide the midday default.
- Sancho buys nothing, orders nothing, creates no tasks; the shopping list is his.
- Fifteen minutes is the ceiling for the Sunday session; if it runs long, the inputs weren't ready, and that is Sancho's failure to fix before next Sunday.
- The first session asks the open questions from the project file once, then never again: what he actually likes to eat; any constraints; how far he wants the companionship side to go.

## Write step
Files written: the week's plan, journal lines, pantry lines, a recipe file when one is earned, the session note. Receipt: the plan path, one line.
