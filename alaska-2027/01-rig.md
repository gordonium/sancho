# The Rig — 1990 Toyota Sunrader

## Confirmed specs
| Item | Spec |
|---|---|
| Length | **~21'2" — MEASURE EXACTLY, including bumpers** (see GTSR note) |
| Weight | ~7,500 lbs |
| Drivetrain | RWD, **dually**, **6-lug full-floating rear axle** ✓ |
| Engine (current) | 3VZ-E 3.0L V6, ~150 hp / 180 lb-ft |
| Engine (planned) | **5VZ-FE 3.4L V6 swap, ~190 hp / 220 lb-ft** — complete w/ transmission |
| Exhaust | 3" from headers back (with the swap) |
| Tires | 1 year old |
| Suspension | Rear airbags now. **Full rebuild to exact ride weights before trip.** |
| Restoration | Frame-off, less than 5 years ago. New fuel tank. |

## Systems
| System | Detail |
|---|---|
| Electrical | **600W solar, 240Ah lithium** (~3,000 Wh usable) |
| Fridge | AC/DC compressor — **no propane** |
| Propane | Stove + furnace only → very low consumption, likely 1 refill all trip |
| A/C | Roof unit — shore power only (240Ah won't run it meaningfully) |
| Connectivity | **Starlink + WeBoost** |
| Shade | Dual awnings |
| Fuel | ~17–19 gal. **220 mi max / 160 mi reliable.** New tank, not larger. |
| Cabin air filter | **NONE.** 1990 Toyota truck HVAC has no filter provision. |

## The good news
At ~21' and 7,500 lbs on a 6-lug full-float dually, this is close to the ideal rig
for this route. **Every road on this trip is accessible**: McCarthy Road, Top of the
World Highway, Salmon Glacier road, the Dempster. People in 35-foot Class Cs will be
turning around where this rig walks through. The one-piece fiberglass shell handles
washboard far better than stick-built construction.

The 6-lug full-float axle removes the single biggest Toyota-motorhome failure mode
(snapped 5-lug axle shafts). That was the main worry and it's off the table.

## ⚠ Open items / decisions

### 1. Exact length — Going-to-the-Sun Road
GTSR in Glacier NP prohibits vehicles **over 21 feet** between Avalanche Creek and
Rising Sun. At 21'2" he is over by two inches. Measure to the inch including bumpers
and any hitch-mounted gear. If over: park and take the free NPS shuttle — which works
fine, but it changes how Glacier gets planned.

### 2. Axle ratio vs. bigger tires
If "more aggressive tires" means **taller** tires, that effectively raises the final
drive and eats the 5VZ's power advantage on grades. Confirm the current ratio
(Sunraders commonly 4.10 / 4.30 / 4.56). Recommendation: keep tire diameter close to
stock, or re-gear. Also recalibrate the speedometer if diameter changes.

### 3. Lift — recommend AGAINST
No road on this route needs more clearance. A lift raises the CG on a rig that is
already tall, narrow-tracked up front, and crosswind-sensitive at 7,500 lbs.
**Recommendation: rebuild to correct ride height, skip the lift.**

### 4. Tires — recommend all-terrain, not mud-terrain
~10,000 miles of mostly pavement with maybe 400 miles of gravel. Load Range E
all-terrains in near-stock size. Mud-terrains cost noise, tread life, and 1–2 mpg
for zero benefit on this route.

### 5. Storage expansion — roof box vs. hitch
Roof box concerns: fiberglass shell needs load spread into structure; adds frontal
area (real mpg hit); puts weight at the worst possible height on a top-heavy rig.
**Also: 600W of solar on a 21' roof already occupies most of the available space —
confirm what room is actually left.**

Preferred order:
1. **Hitch-mounted cargo tray/box** — weight low and aft, easy access, no roof
   penetration. Check receiver rating. Watch departure angle on McCarthy Rd washboard.
2. **Low-profile roof basket** for bulky-light only (chairs, firewood, recovery gear)
3. Interior reorganization first — cheapest win

### 6. Cabin air filter / wildfire smoke
No OEM filter, and July–August is peak smoke season in Interior Alaska and BC.
Mitigations, in order of value:
1. **12V HEPA air purifier running off the lithium.** A small unit draws 10–40W —
   trivially sustainable 24/7 on 600W solar. This is the real answer.
2. N95/P100 respirators for outdoors
3. Recirculate mode; fabricate a MERV-13 media panel into the cowl fresh-air intake
4. Re-do cab weatherstripping (37 years old, almost certainly shot)
5. Route around smoke using PurpleAir + AirNow

### 7. OBD generation after the swap
The 1990 chassis is **pre-OBDII**. Whether the swapped rig is OBDII depends on which
harness/ECU generation came with the 5VZ. **Confirm, and carry the matching reader.**

## 5VZ-FE notes
- **Timing belt**, not chain. 90k interval. Generally regarded as non-interference
  (a snap won't bend valves) — verify for the specific application, but either way
  a broken belt strands you.
- **Knock sensors live in the valley under the intake manifold.** They fail, throw a
  code, and retard timing. Replacing one roadside is miserable.
- Other known items: valve cover gaskets, IAC valve, crank/cam position sensors,
  distributor O-ring.

### ★ Do every "intake-off" job during the swap
The intake manifold is already coming off. While it's off, do:
- Both knock sensors
- Valley plate / intake gaskets
- Timing belt + water pump + tensioner + both idler pulleys (as a kit)
- Valve cover gaskets
- Rear main seal, oil pump seal
- Distributor cap, rotor, O-ring
- Plugs and wires
- Thermostat
- New radiator + hoses + fan clutch

Doing these now costs hours. Doing them at Muncho Lake costs the trip.

---

# Session 2 updates (2026-09-24)

## 5VZ-FE provenance ✓
Swapped into the **1988 Toyota Seabreeze** by **ToyOnlySwaps, Eugene OR**, roughly
2024, **with every upgrade the shop offered.** That's excellent provenance. The
engine+transmission+3" exhaust package moves from the Seabreeze into the Sunrader.

Open items in `02-spares-and-prep.md` §D: get the build sheet, establish miles on
the timing belt, confirm who does the Sunrader transplant, and size the cooling
system for 7,500 lbs rather than the Seabreeze's weight.

## Electrical — new Victron system, complex, well executed
### ⚠ On adding a "big ass inverter"
Worth being precise, because the likely motivation is running the roof AC off-grid,
and **a bigger inverter alone will not do that.**

Roof AC math:
- 13,500 BTU roof unit ≈ **1,300–1,500W running**, 2,500–3,000W startup surge
- 240Ah @ 12.8V = 3,072 Wh; ~90% usable = **2,765 Wh**
- At 1,400W + ~10% inverter loss = ~1,550W draw
- **≈ 1.8 hours.** With 600W solar contributing ~400W average midday, **≈ 2.4 hours.**

So a 3000W inverter buys the *ability* to start the AC, not the *endurance* to use it.
Shore power remains the answer for the heat zones.

### What would actually extend off-grid AC, in order of value
1. **Micro-Air EasyStart soft-start on the AC compressor.** Drops the surge from
   ~2,800W to ~1,200W. Without it, a 2000W inverter may not start the unit at all.
   Cheapest meaningful upgrade.
2. **More battery.** 400–600Ah gets you 3–5 hours. The real lever.
3. **A 12V DC air conditioner** (Mabru, Nomadic) draws ~600W instead of ~1,400W —
   roughly halves consumption. Big install, big payoff.

### ⚠ The inverter is not the constraint — the DC side is
A 3000W inverter at 12V pulls **~300A**. That requires 4/0 cable, a properly sized
Class-T fuse, and a busbar that can take it.

**More importantly: check the battery's continuous discharge rating.** 300A on a
240Ah pack is 1.25C. Many drop-in LiFePO4 BMSs limit to 100–200A continuous — which
would cap the inverter regardless of its rating. **Confirm the pack spec before
sizing the inverter.**

### Recommendation
**Victron MultiPlus-II 12/3000**, if the DC side and the BMS support it. Beyond
inverting, its **PowerAssist** feature supplements a weak campground pedestal with
battery power — genuinely useful when running AC off a tired 15A post in Ellensburg
or Cache Creek. Pair it with a soft-start on the AC.

## Starlink ✓
Runs on 12V DC, not permanently mounted — more robust than assumed. Fair correction.
The remaining gap is only that it needs a conscious operator; see the inReach
recommendation in `02-spares-and-prep.md` §E.

## ⚠ Storage decision: no hitch box
Gordon: *"Hitch mounted storage kills on length."* Correct — at 21'2" against the
21'0" Going-to-the-Sun limit, a receiver box makes a marginal situation worse.

And the spares only need **~3.7 cu ft / ~120 lbs — one 27-gal tote plus a toolbox.**
Storage pressure is lower than assumed. If expansion is still wanted, a low-profile
**roof basket** for bulky-light items (chairs, firewood, traction boards) is the
remaining option — contingent on what space the 600W of solar left.

---

# Session 3 — inverter load math (2026-09-24)

Gordon: *"I know I can't run AC on an inverter, but I can run a 1000–1500W space
heater, also my air fryer."*

Bank: 240Ah × 12.8V = 3,072 Wh; ~90% usable = **2,765 Wh.**

| Load | Draw (+10% inverter loss) | Runtime | Verdict |
|---|---|---|---|
| **Air fryer**, 1,500W × 15–20 min | 1,650W | 375–500 Wh = **13–18% of the bank** | ✓✓ **Excellent.** Solar replaces it in about an hour of sun. This is the use case. |
| **Space heater**, 1,500W continuous | 1,650W | **~1.7 hrs** | ⚠ Poor off-grid. Fine on shore power. |
| Both at once | 3,300W | ~50 min | Needs ~300A DC — see BMS note |

### ⚠ Don't heat with the battery
A 20 lb propane tank holds **432,000 BTU.** The full battery bank holds **9,435 BTU.**
Propane carries roughly **46× the heat energy** of the entire lithium bank.

Electric resistance heat is the single worst use of stored electricity. Off-grid,
**use the furnace.** The space heater's real job is **on shore power, to avoid burning
propane** — genuinely useful on the cold Yukon and Alaska nights (August lows in the
40s) and free at a full-hookup site.

### Inverter sizing
`inverter watts ÷ 12V ÷ 0.9 = amps from the battery`

| Inverter | DC draw | Covers |
|---|---|---|
| 2000W | ~185A | Air fryer OR heater, comfortably. Induction cooktop. |
| 3000W | ~280A | Both at once. Roof AC startup (with soft-start). |

⚠ **The BMS is the gate, not the inverter.** 280A on a 240Ah pack is 1.17C. Many
drop-in LiFePO4 BMSs cap at 100–200A continuous. **Get the pack's continuous discharge
spec before buying.** If it's ≥200A, the MultiPlus-II 12/3000 is the call. If it's
capped at 150A, 2000W is the ceiling no matter what you buy — and 4/0 cable plus a
correctly sized Class-T fuse are required either way.

---

# Session 3 — Seabreeze status ✓
**Stripped to the truck frame.** Either a donor or the platform for a ground-up custom
build; leaning donor. That makes the 5VZ pull easy and clean.

While it's apart, harvest and verify:
- [ ] ★ **Fuel tank size** — if it's bigger than the Sunrader's, that solves the single
      biggest planning constraint on this trip for free. See `08-packing-and-purchases.md`.
- [ ] Wiring harness + ECU come with the engine — **this answers the OBD-generation
      question**, so note the part numbers
- [ ] Radiator, fan clutch, accessories, and whether they're sized for 7,500 lbs
- [ ] Driveshaft, mounts, exhaust routing — all Sunrader-specific work regardless

---

# Session 4 corrections (2026-09-24)

## ✓ Fuel tank: 16.5 usable gallons — confirmed empirically (ran it dry)
At 14 mpg that's **231 mi theoretical / ~160 reliable** — matches the original figure.

This puts the tank at the **small end** of the documented Sunrader range (13 / 21 / 23 /
26 gal across model years). **A larger tank remains the single highest-value mod for
this trip** — 26 gal would give ~250 reliable miles, eliminate the Cassiar 140-mi gap,
and retire the jerry cans. Check the stripped Seabreeze's tank first.

## ⚠ RETRACTED: the cabover is NOT free storage
**It's his bed.** He's solo but he sleeps up there. The earlier "solo means the cabover
is free" insight was wrong — disregard it.

Storage remains genuinely tight. Standing conclusions:
- Spares distribute into 6-qt / 12-qt sub-kits, ~3.7 cu ft total (`08`)
- No hitch box (length penalty vs. the 21' Going-to-the-Sun limit)
- A low-profile **roof basket** for bulky-light gear is the remaining option, contingent
  on what the 600W of solar left — **and the backpacking kit is now competing for that
  same space**

## ✓ Cooling: resolved
The 5VZ carries **large cooling upgrades including a brand new aluminum radiator.**
My earlier concern about sizing the cooling system for 7,500 lbs is closed.

## Engine swap: Gordon + Doug, or a different pro shop
Doug has done comparable Toyota swaps in rock crawlers and has been on a King of the
Hammers team. Not ToyOnly — reasonable, since it means driving both trucks to Oregon.

Doug's experience transfers well. The two things rock crawling doesn't rehearse:
1. **Sustained highway load.** A crawler sees short bursts at low speed; this rig will
   hold 7,500 lbs up 20-mile grades for hours. The aluminum radiator covers most of it —
   also verify fan clutch, shroud fit, and trans cooling.
2. **Exhaust heat in a fiberglass-and-wood house.** Routing and heat shielding matter
   far more here than in a tube-frame buggy. Check clearances to the floor, tanks,
   wiring, and propane lines.

### ★ The scheduling point that matters most
**Finish the swap early enough to shake down 1,500–2,000 miles before departure.**
A swap completed two weeks before the Alaska Highway is how good builds strand people —
the failures are always the small stuff (a chafed wire, a loose clamp, a sensor
connector) and they surface in the first thousand miles.

**Target: swap done by ~March 2027, shakedown trips through spring.**
A DIY swap also means you and Doug know the rig intimately, which on a remote trip is
worth more than a shop warranty you can't reach from Watson Lake.

## ✓ Air fryer: Cosori, ~800W (verify the label)
| Load | Draw | Per use | % of bank |
|---|---|---|---|
| 800W air fryer, 20 min | ~880W | ~293 Wh | **~11%** |

Better than modeled. **A 1500–2000W inverter comfortably covers everything actually on
the list** — no need to chase 3000W or audit the BMS. (Cosori's small units run
900–1500W depending on model, so check the plate.)

## ✓ Space heater: dropped
Reasoning worth one line, because the intuition was sensible: solar *is* free, but the
limit is **collection rate, not cost.** 600W of panels on a good day yields ~3–4 kWh
≈ 13,600 BTU. A 20 lb propane tank holds 432,000 BTU. **A full day of perfect sun
collects about 3% of one propane tank's heat.** Heating is simply an enormous demand
and solar is a trickle. Propane for heat, electrons for everything else.

---

# Session 5 — ⚠ THE SWAP IS NOW THE BINDING CONSTRAINT (2026-09-24)

## The problem
- **Swap window STARTS mid-April 2027**
- Departure target **June 7**
- That's **~7 weeks** for a DIY motorhome engine swap *plus* a shakedown

A motorhome swap is harder than the same swap in a pickup: worse access, exhaust
routing through a fiberglass-and-wood house, driveshaft length, and wiring into a
camper. Realistic DIY estimate on evenings and weekends: **3–6 weeks.** That leaves
**1–3 weeks of shakedown**, and shakedown is exactly where a fresh swap earns its
reliability. Swap failures are always small — chafed wire, loose clamp, sensor
connector backing out — and they surface in the first thousand miles.

**Driving to Alaska on an unshaken-down swap is worse than driving there on the
engine that's already running.**

## ★ Set a go/no-go gate: May 20, 2027
If the rig is not **running, driving, and loaded** by May 20, **go on the 3VZ-E.**
Write the date down now, while it's cheap to agree to.

## The four levers

| Lever | Effect | Cost |
|---|---|---|
| **1. Go/no-go gate + smart shakedown** | Keeps June 7 | Requires discipline to actually honor the gate |
| **2. Later departure** | Jun 20 buys two more weeks | ~13 float days. Route still works — Loveland→Tok by Aug 4 needs ~45–50 days, so departure as late as ~Jun 17–20 is viable with less slack. |
| **3. Pro shop (not ToyOnly)** | Faster, more predictable | $$ and you lose the intimate knowledge |
| **4. Go on the 3VZ-E** | Zero integration risk | 150 hp vs 190, ~1 mpg worse, slower on grades. **The 5VZ is an upgrade, not a requirement.** |

## Smart shakedown — quality over mileage
You don't need 2,000 aimless miles. A **hard loaded mountain loop on a hot day**
surfaces cooling and driveline problems faster than 2,000 flat ones:
1. **Day 1:** Fully loaded, Trail Ridge Road / Berthoud Pass / Poudre Canyon.
   ~200 mi, sustained grades, watch temps. Find the problems.
2. **Then:** a 3–4 day, ~1,000 mi trip with real camping.
3. Re-torque everything, re-check every clamp and connector after each.

That fits in two weeks if the swap lands on time.

## ✓ Resolved this session
- **Seabreeze tank is also in the teens** — no free upgrade there. See `08`.
- **Killswitch: bring the Seabreeze's over.** Free, and it's the single best
  anti-drive-away measure.
- **Cab door locks being replaced + upgraded to power locks anyway.**
  ★ **Doors apart = do the cab weatherstripping at the same time.** That's the
  wildfire-smoke and dust-sealing fix from `01-rig.md` §6, essentially free while
  the panels are off. Don't miss the window.
- **Storage bay locks not yet installed → being replaced anyway.** CH751 concern moot.
  When specifying: keyed-alike *to each other* for convenience, but **not CH751**.
  Marine/stainless grade for weather.
- **Starlink unmounted → lives inside when not in use.** ✓

---

# Session 6 (2026-09-24)

## ⚠ Custom driveshafts — transfer value is lower than it looked
The Seabreeze swap used **custom-fabricated driveshafts.** Probability they fit the
Sunrader correctly is low (wheelbase and trans output position likely differ).
So the "complete package" transfer is really: engine, transmission, exhaust (likely
needs rework too), cooling, harness/ECU. **The Sunrader needs its own driveshaft(s).**

Consequences:
- **New item on the swap's critical path.** Custom driveshaft shops quote days to
  ~2 weeks, and you can't order until the engine/trans are mounted.
- **Sequence matters:** suspension rebuild to ride height FIRST → then the swap →
  then measure for driveshaft. Measuring before the suspension is at final height
  gets the pinion angle and length wrong.
- Exhaust likely needs re-routing/re-fitting for the Sunrader frame as well.

## ✓ Real-world data: ATL → Loveland, 95°F+, AC cranked, interstates
- Held **70 mph uphill** in that heat with the AC on — **the 3VZ's cooling is proven.**
- **8 mpg at 70**, roughly 6,600 lbs (mostly unloaded).
- This materially strengthens "the swap is optional."

### ⚠ Fuel economy — my 14 mpg assumption was wrong
Previous budget used 14 mpg. Reality check:
- 8 mpg at 70 (measured)
- 16.5 gal / 160 mi reliable = **~9.7 mpg implied**
- At 55–60 on state highways aero drag drops roughly 30% vs. 70 — expect **~10–12**.

**Plan at 10.5 mpg.** Range figures stand (160 reliable); the fuel *budget* rises — see `05-budget.md` v4.
Loaded for Alaska, expect **~7,300–7,500 lbs** vs. the 6,600 measured. CAT scale before departure.
