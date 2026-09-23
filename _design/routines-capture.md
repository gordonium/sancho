# Foundational routines: capture from Gordon's head

Started 2026-09-21. These are Gordon's own ideas for routines that do not depend on anything in v2 or v3. Captured as dictated, lightly cleaned. This is an ICE capture queue: nothing here is approved for build until Phase 2 designs it and Phase 3/4 sequences it under the three-in-development limit.

Format per routine: what it's for, when it fires, inputs, outputs, what "done and habitual" looks like.

---

## 1. Food (highest priority)

**Why it matters, in Gordon's words.** Leaving the house, the kitchen, and the people he cooked for is really hard. "My little Italian soul just wants to cook for people to show them my love, and I don't have anyone to cook for or host anymore, and I'm not very good at feeding myself." He was crying while dictating this. This routine is about care, not logistics. Sancho should treat it that way: warm, not clinical, and never make him feel managed.

**The problem.** Feeding himself, alone, in an RV, while working. Three parts:

1. **Breakfast.** Six years of half a bagel with cream cheese every morning. No bagels, no toaster now. The habit is gone and nothing replaced it.
2. **Midday.** He tends to skip lunch and then crash. What worked for a couple of months: a batch of tuna salad (read from "to the salad"; confirm) kept in the fridge, eaten with Ritz crackers. He burnt out on it. Needs: **low-ingredient, very easy, shelf-stable or fridge-stable** things he can eat without stopping work, so calories get in.
3. **Dinner.** He's talked himself into being excited about his new small air fryer. Wants a "Julie and Julia" style cook-through of an air-fryer-cooking-for-one book, but hasn't found one he likes. Alternative: he and Sancho work through ingredients, meal plans, shopping, cooking, and eating for one together, over time. He has never cooked for one before.

**What has worked (the pattern to build on).** A **Sunday session picking four meals for the week**, then each day picking whichever of the four feels best, knowing the choice was already made. The value is in having pre-decided, not in a rigid schedule.

**Constraints.** RV: small kitchen, limited storage, small fridge, air fryer as the main appliance, stores change with location. Living alone. ADD: the midday crash is partly an attention problem, so the food has to be reachable without a decision.

**Routine shape (first sketch, for Phase 2 to design properly).**
- *Weekly (Sunday):* inputs are what's on hand, the week's calendar, current location/stores, what he's tired of. Outputs: four dinners, a breakfast default, a midday default, one shopping list. Written to disk.
- *Daily (morning routine, personal lobe):* one line: today's four options, and a nudge for the midday thing. No planning; just recognition.
- *Ongoing:* a cooking-for-one journal. What he made, whether it worked, what he'd change. Feeds next Sunday. Over time this *is* the cookbook he couldn't find.

**Done and habitual looks like:** he eats breakfast and something midday most days without thinking about it, and Sunday planning takes fifteen minutes because Sancho brings the options and the journal.

**Open (to ask later, not now):** what he actually likes to eat; dietary constraints if any; how far he wants Sancho to go on the emotional side (some people want a cooking companion, some want a list).

(Tuna salad confirmed.)

---

## 2. Nomad daily check (RV adventure startup)

**Big picture.** Gordon lives in his RV full-time. Years ago he found a map on Imgur: a 9,000-mile, 12-month road trip through North America that chases an average of 70°F. He is not doing that exact trip; he's taking the concept and overlaying it with **where his favorite and most important people are**, so he keeps his social exposure during a solo adventure. That social contact is very important to his mental well-being. This routine is as much about people as weather.

**What he wants every morning.** He says "good morning, Sancho" and gets:
1. **Weather** for the next couple of days where he is.
2. **How far and in what direction to drive** to stay in his ideal temperature range.
3. **Cross-reference against his people-and-places list** (people he wants to see, places he wants to visit), so the direction of travel is chosen with visits in mind, not just temperature.
4. A verdict: **drive today, drive in the next couple of days, or stay**, to keep the adventure going and comfortable.

**Temperature range (confirmed):** overnight low no warmer than ~60°F, daytime high no hotter than ~85°F. Routing chases cooler, not warmer.

**Components he can't remember yet.** He said there are a couple more. Leave a slot; ask again another day.

**Inputs (first sketch).** Current location (how does Sancho know? phone location, a manual "I'm in X," or the RV's own GPS); weather forecast source (needs an API or web lookup); the people-and-places list (lives in the personal lobe, references `people/` in the spine, with locations and "want to see by" dates); the calendar (commitments that fix location on given days); Gordon's driving tolerance per day (max hours/miles).

**Outputs.** One short morning brief: where you are, the next 2–3 days' highs and lows, the nearest direction/distance that gets back into range, who's within reach along that direction, and the verdict. Written to disk as a dated log entry so the trip has a record.

**Done and habitual looks like:** he says good morning, reads five lines, and knows whether today is a driving day. He never has to open a weather app or think about the map.

**Notes for Phase 2.**
- Wake phrase (decided 2026-09-22): "Hey Sancho" opens the personal lobe by default; "Hey Sancho, let's work" opens the work lobe. Any Sancho greeting counts. See decisions.md.
- This is the personal morning routine's core, or a skill it calls. It shouldn't be a separate ritual on top of a ritual (Q2 failure).
- Weather and geocoding need a script with a real data source, not an MD instruction. Which source, and whether it works from a Cowork session, is a Phase 2 question.
- The people-and-places list is a first concrete consumer of the spine's `people/` design (decision #8): people need a `location` field and a "last seen / want to see" field.

---
