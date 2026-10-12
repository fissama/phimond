# P11 — Owner-confirmed design decisions

Status: **HISTORICAL OWNER INTERVIEW**, imported 2026-10-12.

Current authority: [P11-final-spec.md](P11-final-spec.md). The owner subsequently
delegated completion of P11. F01–F06 record agent-selected completion decisions;
F02/F03 explicitly supersede the total-candidate inheritance contract Q14.1/3/4
and scope-amend P10-D14/D16. Q14.5 did not approve a plateau. The old checkpoints
and individual owner answers below are retained for audit, not current OPEN gates.

Authority: the owner supplied the following current design state in this chat.
Its LOCKED decisions supersede contradictory P11 scaffold suggestions; P10
remains authoritative elsewhere. Illustrative numbers are not approved tuning.
The rejected overall-quality/zero-sum model must not return through templates.
Q7.6 was subsequently locked to A by the owner on 2026-10-12; see §15.
Recommendations in the review are not decisions. This document does not authorize runtime implementation.

---

# P11 Stats — Current Design State

## 0. Scope

P11 hiện tại là **design/spec phase**, chưa phải implementation phase.

Do not:
- implement runtime stat engine,
- modify gameplay code,
- add Go/GDScript formulas,
- build simulation harness,
- migrate saves/database,
- silently invent missing numeric values.

P11 should define formulas, budgets, tables, species/stat assignment rules, growth rules, inheritance rules, rounding rules, and verification criteria first.

P10 canonical decisions remain authoritative where P11 has not explicitly overridden them.

---

# 1. P10 constraints P11 must preserve

## Core stats

```text
hp
atk
mag
def
spd
status_resistance
```

`mp` is a separate resource and is not one of the six core growth-profile stats.

## Permanent stat display

```text
permanent_total[s]
=
grown_stat[s]
+
inheritance_bonus[s]
```

UI concept:

```text
186 +12
```

where:
- `186` = grown stat
- `+12` = inheritance bonus

## Species Lv1 stats

`species.base_stats` are the actual Lv1 stats.

Lv1 base stats are **fixed by Species**.

There is no random Lv1 start-stat variance.

## Species growth

Each Species owns a growth baseline for every core stat.

Level growth is deterministic once the individual's growth profile is fixed.

There is **no per-level RNG**.

## Individual growth profile

Each Egg/Pet has an individual growth profile for each of the six core stats.

Conceptually:

```text
growth_profile = {
    hp,
    atk,
    mag,
    def,
    spd,
    status_resistance
}
```

These values represent growth deviation/potential, **not current stat values**.

## Growth reroll from P10

P10 already locks two capabilities:

### Full Growth Reroll

Reroll growth rolls for all six core stats.

### Single-Stat Growth Reroll

Reroll one selected core stat's growth roll.

Rules:
- Egg-only.
- New result may be better, equal, or worse.
- A hatched Pet's growth profile is locked.
- Pet → Egg enables reroll again.
- Conversion/hatch does not automatically reroll.
- Growth reroll does not change Species base stats.
- Growth reroll does not change inheritance.
- Parent restoration snapshots are unaffected.

Therefore it is valid for a sufficiently invested player to eventually obtain **Perfect growth in all six stats**.

The economic control for this is intended to come later from item rarity/source/cost, not from forcing growth stats to share a zero-sum budget.

---

# 2. Q1 — Star power philosophy — LOCKED

## Q1 decision

Higher Star means a progressively stronger power band, but lower Stars should remain usable for a meaningful portion of the game.

Low-Star Pets are not intended to equal the final ceiling of 4★–5★.

## Star gap shape

The gap between Star tiers should increase slightly toward higher Stars instead of being exactly flat.

Conceptually:

```text
1★ → 2★   smaller gap
2★ → 3★   moderate
3★ → 4★   larger
4★ → 5★   largest / near-largest
```

Exact percentages are NOT locked.

## Where Star power comes from

Higher Star receives moderate increases to both:

```text
Lv1 base-stat budget
+
growth budget
```

Star advantage must not come only from one of these layers.

Level caps remain:

```text
1★ = 60
2★ = 70
3★ = 80
4★ = 90
5★ = 100
```

## Low-Star endgame philosophy

Low-Star Pets may remain usable into early/niche endgame.

They should not generally match the final raw-stat ceiling of top 4★/5★ Pets.

## SPD and Status Resistance

Star scaling for:

```text
SPD
Status Resistance
```

must be weaker/narrower than scaling for:

```text
HP
ATK
MAG
DEF
```

Reason: avoid excessive turn-economy and resistance scaling.

Exact numeric scaling is NOT locked.

---

# 3. Q2 — Normal Species budget philosophy — LOCKED

Decision: **A+**

Within the same Star, Normal Species should target approximately the same normalized raw-stat budget.

Not exact equality, but only a small allowed variance.

Concept:

```text
same Star Normal Species
≈ same total stat budget
```

Species identity should primarily come from:

```text
allocation
role
growth profile
element
skill synergy
```

and not because one Species simply has a dramatically larger total raw-stat budget.

Avoid intentional "trash Species" that sit 15–20% below their same-Star peers in raw budget.

Small variance is allowed for identity.

Normal main-budget tolerance was subsequently locked to **±3% around target** in Q9.2; auxiliary ranges remain open; Special main tolerance is subsequently locked
to±2% in Q11.4.

---

# 4. Q3 — Special Species power band — LOCKED

Decision: **E3 — Half-step Star**

Current Special progression concept:

```text
2 Normal 4★ → Special 4★
2 Normal 5★ → Special 5★
```

The Special Pet remains the same Star.

It does NOT become an extra Star tier.

## Power hierarchy target

Conceptually:

```text
Normal 4★
<
Special 4★
<
Normal 5★
<
Special 5★
```

A Special is an **elite version within its Star band**.

Special 4★ should be tuned roughly between Normal 4★ and Normal 5★.

Special 5★ has no 6★ reference tier, so its premium should be extrapolated using the same design philosophy.

## Where Special power comes from

The Special premium should be split across:

```text
base-stat budget
+
growth budget
```

Do not apply an additional full-premium multiplier to the finished stats
after authoring the base/growth premium. Arithmetic clarification from this
review: base and accumulated growth are additive. Applying the same factor r
to both components yields r×(base+growth), not r². Different base/growth factors
would instead produce a level-dependent effective premium. Exact allocation
remains an owner decision; floors and actual assignments still need checks.

Target effective premium is not numerically locked yet.

Special should remain "moderately superior", not automatically invalidate every Normal Species in all contexts.

## Still open inside Q3

Not locked:
- exact Special premium %
- exact interpolation formula between Normal Star bands
- whether every Special uses exactly the same premium
- allowed Special-to-Special budget variance

---

# 5. Q4 — Role and stat generation — LOCKED

Decision: **C — Role template + Species modifier**

Role is not merely metadata.

Stat generation should conceptually follow:

```text
Star power budget
→ role template
→ Species modifier
→ final Species base/growth profile
```

The role template gives consistency.

Species modifier gives individuality.

Species modifiers must not be allowed to completely destroy primary-role identity.

Exact role templates remain open; relative modifier method/bounds were subsequently locked in Q10.1/Q10.2.

---

# 6. Q5 — Secondary role — LOCKED

Decision: **B — fixed Primary/Secondary blend**

Secondary role contributes directly to stat-template generation.

Concept:

```text
final role template
=
Primary role weight
+
Secondary role weight
```

Working illustration used during discussion:

```text
75% Primary
25% Secondary
```

**75/25 was subsequently locked in Q10**, including100% Primary when no Secondary exists.

Important invariant:

> Primary role must remain visually/statistically recognizable after blending.

Example:

```text
Primary: Tank
Secondary: Magic Attacker
```

may gain meaningful MAG, but should still retain the HP/DEF signature of a Tank.

Do not use a unique arbitrary blend ratio per Species.

---

# 7. Q6 — When growth randomness happens — LOCKED

Decision: **B**

Growth profile is resolved when the Egg/individual is created/fixed.

Once fixed, level progression is deterministic.

Do NOT roll new growth RNG on every level-up.

Concept:

```text
Egg created
→ growth profile fixed

level up
→ deterministic stat progression using that profile
```

This matches P10's:

```text
Level growth is deterministic.
No per-level RNG.
```

---

# 8. Previous Q7/Q8 "overall quality budget" idea — REJECTED / SUPERSEDED

Do NOT implement or document these earlier brainstorm ideas as accepted rules:

```text
overall growth quality shared across all six stats
zero-sum growth budget
distribution budget shared between stats
cannot Perfect all six stats
one stat gaining growth forces another stat to lose growth
```

These were exploratory suggestions and were later rejected after re-checking P10.

Current intended model:

```text
each core stat has its own growth roll
```

and Full/Single-Stat Reroll operate on those individual rolls.

A player can eventually achieve Perfect on all six growth stats.

---

# 9. Q7 — Growth deviation model — PARTIALLY LOCKED

## Q7 main model — LOCKED

Internal growth rolls use a **weighted/bell-like bucket distribution**, while UI exposes readable grades.

This is the chosen **BC hybrid**.

Concept:

```text
internal weighted roll
→ grade bucket
→ internal growth value
```

UI does not need to expose raw formula complexity.

---

# 10. Q7.1 — Perfect definition — LOCKED

Decision: **B**

`Perfect` is a **top band**, not one exact numerical maximum.

For example only:

```text
109.5%–110.0% = Perfect
```

The later Q7.6/Q7.8–Q7.10 decisions use one fixed Perfect representative per stat family; the example interval is not a sampled runtime band.

Implication:

Perfect does not require hitting exactly one floating-point value.

---

# 11. Q7.2 — Grade generation — LOCKED

Decision: **C — weighted discrete bucket**

The system first rolls a weighted grade bucket.

Conceptual grades discussed:

```text
D
C
B
A
S
SS
Perfect
```

Grade names/count were subsequently locked in Q7.7; this bucket model is accepted.

Concept:

```text
Step 1:
roll weighted grade bucket

Step 2:
resolve numeric growth multiplier/value associated with that bucket
```

Illustrative probabilities such as:

```text
Perfect 0.5%
SS      3.5%
S       10%
...
```

were examples only.

Exact percentages were subsequently locked in Q7.11.

---

# 12. Q7.3 — Distribution bias — LOCKED

Decision: **B — slightly biased toward usable outcomes**

The distribution should not create huge numbers of unusably bad Pets.

Philosophy:

```text
most natural Eggs = usable
good growth = desirable
excellent growth = uncommon
Perfect = very rare
terrible growth = also relatively rare
```

Growth reroll should primarily be:

> long-term optimization

rather than:

> mandatory repair of a bad Pet.

Grade probabilities were subsequently locked in Q7.11.

---

# 13. Q7.4 — SPD / Status Resistance growth range — LOCKED

Decision: **B**

All six stats use the same grade rarity/probability framework.

However:

```text
HP / ATK / MAG / DEF
```

may have wider numerical growth-deviation bands than:

```text
SPD
Status Resistance
```

Example only:

```text
ATK Perfect → larger % deviation
SPD Perfect → smaller % deviation
```

but both can have the same probability of rolling `Perfect`.

This preserves readable rarity while preventing SPD/SR from becoming disproportionately powerful.

Fixed multiplier tables were subsequently locked in Q7.8–Q7.10.

---

# 14. Q7.5 — Growth deviation formula — LOCKED

Decision: **A — multiplicative**

Individual growth deviation is relative to the Species growth baseline.

Conceptual formula:

```text
individual_growth[s]
=
species_growth_baseline[s]
× growth_multiplier[s]
```

Example:

```text
species ATK growth baseline = 2.40
individual multiplier       = 1.075

actual ATK growth
= 2.40 × 1.075
= 2.58
```

Do NOT use a universal flat additive growth bonus.

Reason:
- preserves Species identity,
- scales naturally across Stars,
- scales naturally across Normal/Special,
- avoids disproportionately boosting Species with low baselines.

---

# 15. Q7.6 — Internal value inside a grade — LOCKED

Owner chose **A — one fixed multiplier per grade** on 2026-10-12.

For a given stat family and grade, every individual receives the same approved
multiplier. There is no continuous/granular/tiny-variance secondary roll.
Different families may use different multiplier tables: HP/ATK/MAG/DEF may have
wider deviations than SPD/Status Resistance, as already locked in Q7.4.

Perfect remains the highest grade/top-band concept from Q7.1, resolved by the
fixed representative multiplier assigned to that grade. It is not a hunt for
an additional exact RNG maximum within Perfect. Any numeric top-band boundaries
and the fixed representative value are still unapproved; do not imply that a
range of individual multipliers is sampled. Grade names/odds and all multiplier
values remain open.

Example `S = 1.06` is illustrative only, not an approved constant.
Options B (within-band granular RNG) and C (tiny variance) were not selected.

---

# 15a. Q7.7 — Grade names/count — LOCKED

Owner confirmed seven grades on 2026-10-12:
`D / C / B / A / S / SS / Perfect`, ordered low to high.
This supersedes the earlier tentative-name wording in Q7.2.
See Q7.10/Q7.11 for subsequently approved multipliers and probabilities.

# 15b. Q7.8 — HP/ATK/MAG/DEF endpoints — LOCKED

Owner confirmed on 2026-10-12:
- D multiplier = **0.90** of Species growth baseline.
- Perfect multiplier = **1.10** of Species growth baseline.

These apply to growth only, not Lv1 or fixed inheritance. Intermediate values
were subsequently approved in Q7.10. Perfect/D earned-growth ratio =1.10/0.90=11/9,
about22.22% higher; total-stat difference depends on base and inheritance.
These are approved Phimond tuning choices, not recovered original-game numbers.

# 15c. Q7.9 — SPD/Status Resistance endpoints — LOCKED

Owner confirmed on 2026-10-12, for both SPD and Status Resistance:
- D multiplier = **0.97** of Species growth baseline.
- Perfect multiplier = **1.03** of Species growth baseline.

Perfect/D earned-growth ratio =103/97, about6.19% higher. This does not mean
6.19% extra actions or percentage-point status protection. SPD determines turn
order under P10; SR's application-chance formula remains open.

---

# 15d. Q7.10 — Complete fixed multiplier table — LOCKED

Owner approved on 2026-10-12:

| Grade | HP/ATK/MAG/DEF | SPD/Status Resistance |
|---|---:|---:|
| D | 0.90 | 0.970 |
| C | 0.95 | 0.985 |
| B | 1.00 | 1.000 |
| A | 1.03 | 1.009 |
| S | 1.06 | 1.018 |
| SS | 1.08 | 1.024 |
| Perfect | 1.10 | 1.030 |

B equals the Species baseline. There is no within-grade random value.
These are growth-only multipliers, not base/total/inheritance/Star multipliers.

# 15e. Q7.11 — Grade probabilities — LOCKED

Owner approved on 2026-10-12, per core stat:

| Grade | Probability |
|---|---:|
| D | 3% |
| C | 12% |
| B | 40% |
| A | 28% |
| S | 12% |
| SS | 4% |
| Perfect | 1% |

Sum100%; B-or-better85%. Mean multiplier1.0108 for HP/ATK/MAG/DEF,
1.00324 for SPD/SR. Perfect first-hit expectation under independent repeated
rolls is100 attempts/stat, not a guarantee, pity counter or item cost.
The alternative Perfect0.5%/SS4.5% was not selected.

# 15f. Q7.12 — Shared distribution across creation/reroll — LOCKED

Owner approved on 2026-10-12: the same grade odds and stat-family multiplier
tables apply to capture, Star-up, Reinforcement, Full Growth Reroll and
Single-Stat Growth Reroll. Full redraws all six without a stat lock; Single
redraws only the chosen stat. No acquisition-specific boosted odds approved.
Special creation remains source-gated separately; shared growth tables do not
activate its operation. Reroll costs/rarity/sources belong to later phases.

---

# 15g. Q8 — Level growth curve — LOCKED

Owner approved **linear accumulation** on 2026-10-12:

```text
accumulated_growth[s, level]
= species_growth_baseline[s] × stored_growth_multiplier[s] × (level−1)
```

Lv1 growth is zero; no per-level RNG. Grown stat equals fixed Species Lv1
base plus the accumulated growth floored once (Q8.1). Baseline precision is at most three decimals (Q8.2). Inheritance stays fixed and is added once afterward.

---

# 15h. Q8.1 — Accumulated-growth rounding — LOCKED

Owner selected **floor once on accumulated growth** on 2026-10-12:

```text
grown_stat[s, level]
= species.base_stats[s]
  + floor(species_growth_baseline[s] × stored_growth_multiplier[s] × (level−1))
```

No per-level truncation. Fractional contributions remain available through
exact recalculation from baseline/profile/level; do not feed a previously
rounded grown stat back into the growth formula. Direct level calculation,
sequential leveling, level jumps and save/load must produce the same result.
Lv1 accumulated growth is zero. Add the fixed inheritance bonus once afterward.
This does not choose inheritance rounding, MP growth or SR application rounding.
Baseline precision is at most three decimals (Q8.2); use exact arithmetic, not a
floating-point approximation followed by a floor near an integer boundary.

Illustrative baseline2.40, gradeA multiplier1.03:
Lv20 growth floor46.968=46; Lv21 growth floor49.44=49. Baseline2.40 is a
worked example only, not assigned to any Species. Round-half-up was not chosen.

---

# 15i. Q8.2 — Exact baseline precision — LOCKED

Owner selected **at most three decimal places** for Species growth baselines
on 2026-10-12. The approved fixed multipliers also fit three decimal places.

Exact mathematical representation:

```text
baseline_milli[s] = species_growth_baseline[s] × 1000
multiplier_milli[s] = approved_grade_multiplier[s] × 1000
accumulated_growth_numerator[s, L]
= baseline_milli[s] × multiplier_milli[s] × (L−1)
earned_growth[s, L]
= floor(accumulated_growth_numerator[s, L] / 1000000)
grown_stat[s, L] = species.base_stats[s] + earned_growth[s, L]
```

Both milli values are exact integers; do not first round/truncate their product
or individual level increments. Baselines authored with fewer decimal places
are valid; values exceeding three places require correction/reapproval rather
than silent rounding. Actual per-Species values/ranges are still open. Safe
arithmetic bounds must be proved against those values before implementation;
this specification does not choose storage schema or a runtime integer width.
The formula is recomputed from baseline/profile/level; no fractional-progress
save field is required by the arithmetic contract itself. Catalog/profile
versioning remains a separate unresolved persistence contract.

Example only: baseline2.405, gradeA1.03, Lv20 gives milli2405 and1030;
numerator47065850, earned_growth47. No Species receives baseline2.405 here.

---

# 15j. Q9 — Budget structure — LOCKED

Owner selected on2026-10-12:
- Main budget for HP/ATK/MAG/DEF.
- Separate narrower budget for SPD/Status Resistance.

Apply this structure to both Species Lv1 and growth-baseline budgets. Role and
Species modifiers allocate within the respective groups; there is no unrestricted
transfer from main stats into SPD/SR or vice versa. Exact normalization weights,
Star targets, auxiliary-budget definition/bounds and tolerances are still open.
Do not read “narrower budget” as an approved raw-unit comparison: HP and SR have
different units. Normal same-Star approximate normalized parity (Q2) still holds;
each group needs explicit comparable-state checks. Numeric weighting within
SPD/SR is not selected by this structure decision.

This is a Phimond authoring/balance structure, not a recovered original-game
budget rule. Original-source descriptions and runtime combat remain distinct.

---

# 15k. Q9.1 — Main-budget normalization — LOCKED

Owner selected **10 HP = one main-budget point** on2026-10-12.
ATK/MAG/DEF each contribute one main-budget point per stat point.

```text
main_base_budget(species)
= species.base_stats.hp / 10
  + species.base_stats.atk + species.base_stats.mag + species.base_stats.def

main_growth_budget(species)
= species.growth_baseline.hp / 10
  + species.growth_baseline.atk
  + species.growth_baseline.mag
  + species.growth_baseline.def
```

Apply the same weights to Lv1 and Species growth-baseline budgets. Do not
floor intermediate normalized contributions. Individual grade multipliers and
inheritance/equipment do not enter the Species authoring-baseline budgets.
This conversion defines authoring units; it does not assert equal combat value
of10 HP and1 ATK/MAG/DEF or recover a source-game formula. SPD/SR remain in a
separate budget with still-open normalization/bounds (Q9).
Star/class targets remain unapproved. Normal main tolerance is subsequently
locked to±3% in Q9.2; auxiliary and Special tolerances remain open.

Illustrative only: HP200,ATK50,MAG10,DEF20 → main_base_budget100;
HP400,ATK10,MAG10,DEF40 → main_base_budget100. These demonstrate different
allocations at equal authoring budget, not approved role templates/Species
assignments or a claim of balanced Tank/Attacker combat power.

---

# 15l. Q9.2 — Normal same-Star main-budget tolerance — LOCKED

Owner selected **±3% around target** on2026-10-12. Evaluate separately:

```text
0.97 × normal_main_base_target[star]
<= main_base_budget[species]
<= 1.03 × normal_main_base_target[star]

0.97 × normal_main_growth_target[star]
<= main_growth_budget[species]
<= 1.03 × normal_main_growth_target[star]
```

Endpoints are inclusive. The Lv1 and growth-baseline checks each must pass;
over-budget base cannot be offset with under-budget growth. Use actual authored
Species values and the Q9.1 exact HP/10 normalization. Do not apply individual
growth grade, level-grown totals, inheritance or equipment to these checks.
This tolerance is for **Normal main budgets only**; SPD/SR bounds and Special
tolerance remain open. Target values for each Star are still unapproved.
No hidden rounding exception may enlarge the ±3% allowance; adjust assignments
or explicitly reopen the decision if actual authoring constraints cannot fit.

Illustrative target100 permits97 through103. Maximum upper/lower budget ratio
is103/97,about1.061856 (6.19%); this does not establish combat power parity.
These are Phimond content rules, not recovered original-game numerical rules.
The ±5% and exact-equality options were not selected.

---

# 15m. Q9.3 — Separate SPD and SR targets/ranges — LOCKED

Owner selected on2026-10-12: **SPD and Status Resistance each have their own
target/range by Star/role; points cannot be exchanged between them**.
Apply separate content targets/bounds to Species Lv1 and growth baselines.
Do not define a shared weighted SPD+SR pool or infer an SPD↔SR conversion rate.
The main HP/ATK/MAG/DEF budget remains separate (Q9/Q9.1/Q9.2).

Exact targets/range widths, role templates and weaker Star scaling are still
open. Individual growth grades multiply the approved Species baselines; the
content range is not an extra per-Pet clamp or inheritance cap. Raw SR units
are not probability percentage points. Separate auxiliary checks and main±3%
checks do not yet prove six-stat/combat parity across roles; final balance
verification must make the intended comparison conditions explicit.

Before numeric role targets, reuse P10-D39's initial vocabulary:
`physical_dps`, `magic_dps`, `tank`, `support`, `disruptor`, `hybrid`.
No new role or gameplay eligibility restriction is introduced. Owner's Q4/Q5
explicitly extend D39's metadata-only wording to role-driven stat authoring;
D39's prohibition on hard gameplay restrictions still holds. P11's authoring
helpers are not per-Pet class restrictions or automatic skill grants.
Primary/secondary blend was subsequently locked to75/25 in Q10; role template
numbers remain open; modifier bounds were subsequently approved in Q10.2.

---

# 15n. Q10 — Primary/secondary role blend — LOCKED

Owner approved **75% Primary /25% Secondary** on2026-10-12.
The ratio is shared by all Species with two roles. A Species with only Primary
uses100% of that role's template; do not leave25% of its budget unused.

```text
blended_template = 0.75 × primary_template + 0.25 × secondary_template
single_role_template = primary_template
```

Apply to Lv1/growth stat-authoring templates and SPD/SR target values, before
the Species modifier. Exact template numbers, auxiliary range widths,
Species modifier bounds were subsequently locked in Q10.2; final quantization remains open. Do not assume
75/25 alone proves primary-role identity; validate the approved role signature
after blending and modifiers. There are no per-Species alternative blend ratios.
This authoring rule is not an additional runtime multiplier on actual Species
Lv1/growth values, and does not alter individual growth sampling or inheritance.

Illustrative main-budget allocations only, ordered HP/10,ATK,MAG,DEF:
Tank[40,10,10,40], MagicDPS[20,10,50,20] →75/25 blend[35,10,20,35].
Each totals100. These are not approved role-template values or assignments.
The80/20 and70/30 alternatives were not selected.

---

# 15o. Q10.1 — Relative per-stat Species modifier — LOCKED

Owner selected on2026-10-12: **bound each stat's relative percentage deviation
from its blended role template**. Do not use percentage-point transfers of main
budget allocation as the selected modifier method. Q10.2 subsequently locks
main±10% and SPD/SR±5%, for both Lv1 and growth baselines.

Concept for each authored layer/stat:

```text
species_value[s] = blended_template_value[s] × (1 + species_modifier[s])
```

This is content authoring, not Pet-instance RNG or an additional hatch/level
multiplier. The final assigned Species values must simultaneously satisfy the
relative-deviation limits, Normal main-budget tolerance (where applicable),
separate SPD/SR ranges, baseline precision and primary-role signature. Any
balancing/quantization step must be rechecked against those same final-value
constraints; an in-range initial multiplier alone does not prove validity.
Budget±3% does not authorize±3% beyond a per-stat bound, or vice versa.

A multiplicative modifier cannot create a positive value from a zero template.
If a future template has zero where a Species needs a nonzero value, resolve
that content/template case explicitly; do not silently insert an additive floor.
Numeric template values/zero policy and assignment quantization remain
unapproved. Modifier limits were subsequently approved in Q10.2; independent
Lv1/growth modifier choices were subsequently approved in Q10.6. Choosing the
relative-deviation method alone did not decide that coupling.

Illustrative only: a10% increase takes MAG10 to11; shifting budget share10%
to15% is a50% relative increase and is not equivalent. No10% bound is approved
by this example. Independent per-Pet growth and six-Perfect reachability stay
unchanged.

---

# 15p. Q10.2 — Numeric Species modifier bounds — LOCKED

Owner approved on2026-10-12, for both Lv1 and growth-baseline authoring:

| Stats | Maximum relative deviation | Inclusive final-value interval |
|---|---:|---|
| HP/ATK/MAG/DEF | ±10% | [0.90×blended value,1.10×blended value] |
| SPD/Status Resistance | ±5% | [0.95×blended target,1.05×blended target] |

Measure from the exact75/25 blended template (or100% Primary without
Secondary). Enforce on final assigned Species values after balancing and
quantization. All other constraints must also pass: Normal main±3% separately
for base/growth, distinct SPD/SR role ranges, precision and primary signature.
The limits are maxima, not permission to raise every stat or exceed budgets.
An auxiliary range may further narrow the allowed interval; neither constraint
supersedes the other. If no valid representable assignment exists, report the
content conflict rather than silently relaxing a bound or clipping values.

This caps a Species authoring deviation only, not accumulated Pet stats or
inheritance. It does not change individual growth tables, Star scaling or
create a new RNG roll. Lv1/growth modifier independence is subsequently locked in Q10.6; final quantization is
still open; the same bound values do not force identical modifiers in both layers.
Example only: blendedATK50 permits45…55; SPD20 permits19…21. Template values
are illustrative and not assigned to any role/Species. The±15% main and
all-six±10% alternatives were not selected.

---

# 15q. Q10.3 — Physical/Magic DPS and Tank primary signatures — LOCKED

Owner approved on2026-10-12. Check each of actual Species Lv1 and growth
baseline separately, after blend/modifiers/final quantization. Let B be that
layer's exact main budget, defined by Q9.1:

| Primary | Required constraints (inclusive) |
|---|---|
| physical_dps | ATK≥0.35×B and ATK≥1.25×MAG |
| magic_dps | MAG≥0.35×B and MAG≥1.25×ATK |
| tank | HP/10+DEF≥0.60×B |

Use the matching layer's stat values (base or growth), without individual grade
multipliers, equipment, inheritance or temporary effects. Constraints apply to
Species authoring, not arbitrary owned-Pet permanent totals; do not reject or
clip inherited stats to force a Pet back into its Species primary signature.
These are approved Phimond design thresholds, not recovered source rules or a
proof of combat viability. Hybrid signature subsequently locked in Q10.4f below. Support/Disruptor
functional guards are subsequently locked in Q10.4a–d below; no universal
bulk/SPD minima are added.
Final template values and their compatibility with all constraints remain open.

Example only: ATK40,MAG10,B100 passes physical_dps; ATK34.9 atB100 fails even
if the ATK/MAG ratio passes. Tank HP350,DEF35 atB100 reaches70% and passes.
No example values are assigned to any Species or role template.

---

# 15r. Q10.4a — Support functional scope — LOCKED

Owner approved on2026-10-12: Support covers ally-facing recovery, protection,
buffs and harmful-status cleansing. This is a broad functional umbrella; a
Species does not have to provide all four functions. Exact effects, skill pool
contents, eligibility and scaling remain P13 dependencies. This decision does
not grant skills automatically or approve a numeric kit-count requirement.

Role identity and statistical signature are separate authoring questions.
Support does not yet require HP/10+DEF≥50%, a MAG minimum or a speed threshold.
Those values were proposals, not approvals. Primary/Secondary assignment
criteria subsequently locked in Q10.5 below; Q10.4d resolves Support stat guards without a
universal bulk/SPD minimum.

Q10.4 was explicitly deferred for further Support/Disruptor discussion. Its
Hybrid20%/20%/combined50%, Support bulk50%, and Disruptor neutral-speed minimum
were all unapproved at this checkpoint. Subsequently Q10.4d rejects Support/
Disruptor minima and Q10.4f approves Hybrid thresholds. Q10.4a approves only
Support's functional scope. The next topic at that checkpoint was:
Q10.4b Disruptor functional scope (subsequently approved below), then revisit statistical signatures.

Original-game comparison: APK descriptions for TomHumRangCua combine physical
attack growth with ally cleansing/HP help; QuaiVatRuongBau combines physical
attack/defense with healing. These are qualitative examples of mixed functions,
not recovered Primary classifications or numeric Support constraints. See
[P11-reference-comparison](P11-reference-comparison.md).

---

# 15s. Q10.4b — Disruptor functional scope — LOCKED

Owner approved on2026-10-12: Disruptor includes control and debuffs that hinder
opponent actions or reduce combat effectiveness. It is not limited to action
control. This defines a functional umbrella, not a required skill list, count,
status probability or numeric stat signature. P13 owns concrete skill effects,
eligibility and interactions; no automatic skill grants follow from the role.

Pure poison/burn damage classification was pending here; Q10.4c below subsequently excludes damage-only effects from establishing Disruptor. The previously
approved broad harmful-status scope of Status Resistance does not itself decide
which status effects establish Disruptor identity. SPD≥neutral target, Support
bulk50% were subsequently rejected in Q10.4d; Hybrid numeric signatures
proposed in Q10.4 were subsequently approved in Q10.4f.
Primary/Secondary criteria subsequently locked in Q10.5 below.

APK HaiLongBaDau's description mentions varied control alongside strong
Intelligence growth and weak defense. This is qualitative source context, not
proof of its Primary role, speed or exact control rules. The functional scope
above is owner-approved Phimond design, not a recovered original-game taxonomy.

---

# 15t. Q10.4c — Pure poison/burn does not establish Disruptor — LOCKED

Owner approved on2026-10-12: poison/burn that only deals damage over time is a
damage function, insufficient by itself to establish Disruptor identity. An
additional control or impairment beyond HP loss is needed for that function
to count as Disruptor. For a mixed effect, the impairment component qualifies;
the damage component alone does not. Exact effects remain P13-owned.

This role convention does not change Status Resistance: harmful poison/burn
application remains in its approved scope. It does not assign any Species a
role or settle Physical/Magic/Hybrid attribution for damage-over-time skills.
Primary/Secondary criteria subsequently locked in Q10.5 below. Support/Disruptor stat
guards were pending here; Q10.4d below subsequently rejects universal
bulk/speed minima while retaining template and existing authoring constraints.

This is owner-approved Phimond terminology, not recovered original-game rules.
Q10.4's numeric proposals were pending here; Q10.4d/f subsequently resolve
them (Support/Disruptor minima rejected, Hybrid thresholds approved).

---

# 15u. Q10.4d — Support/Disruptor authoring guards — LOCKED

Owner approved on2026-10-12: do not add a universal minimum bulk share for
Support or a universal minimum SPD for Disruptor. The earlier Support
HP/10+DEF≥50% and Disruptor SPD≥neutral-target proposals are not adopted.

Both roles still use the approved authoring pipeline: role templates, Primary/
Secondary blend, Star budgets, Species modifier bounds and separate SPD/SR
ranges. This decision does not remove those constraints, make their values
arbitrary or approve actual template/range numbers. Document the intended
functional identity and check it against P13 skill content. Q10.4a–c define
those functions; roles do not automatically grant skills or restrict loadouts.
One ancillary function alone is not automatic proof of Primary identity;
Primary/Secondary criteria subsequently locked in Q10.5 below.

The decision permits varied Support/Disruptor stat shapes without a single
extra bulk/speed threshold across the entire role. Combat viability still
requires the actual P13 content. No original-game numeric rule is asserted.
Hybrid definition was pending here; Q10.4e below subsequently locks dual
physical/magic damage. Numeric Hybrid guards subsequently locked in Q10.4f below.

---

# 15v. Q10.4e — Hybrid means physical + magic damage — LOCKED

Owner approved on2026-10-12: `hybrid` means a dual-damage identity that emphasizes
both physical and magic damage. Other functional combinations are expressed
through Primary/Secondary roles, not a catch-all Hybrid category. This does
not force equal ATK/MAG, approve damage formulas or grant physical/magic skills.
Concrete skill content and scaling remain P13 dependencies.

Hybrid's numeric signature was proposed here and subsequently approved in
Q10.4f below. Historical proposal:
for Primary Hybrid, require ATK≥0.20×B, MAG≥0.20×B and ATK+MAG≥0.50×B, separately
on final authored Species Lv1 and growth baseline. B is the matching layer's
HP/10+ATK+MAG+DEF budget. Exclude individual grades, inheritance, equipment and
temporary effects. Q10.4f below approves these thresholds as Phimond design, not recovered source
rules. They do not add an ATK/MAG ratio requirement or imply equal allocations.

Examples only at B100: ATK25/MAG25 would pass all three proposed checks;
ATK40/MAG10 would fail MAG; ATK20/MAG20 would fail the combined minimum.
Numeric signature checks need not uniquely identify a role; they validate an
explicit content assignment rather than automatically classify a Species.
No role template values or Species assignments are approved by these examples.

---

# 15w. Q10.4f — Primary Hybrid numeric signature — LOCKED

Owner approved on2026-10-12. For each final Species authored layer (Lv1 and
six-stat growth baseline), let B be that layer's exact main budget:

```text
B = HP/10 + ATK + MAG + DEF
hybrid: ATK >= 0.20×B AND MAG >= 0.20×B AND ATK+MAG >= 0.50×B
```

All three checks must pass, with inclusive boundaries, separately for base and
growth. Exclude individual growth multipliers, inheritance, equipment and
temporary effects. This is a Primary Hybrid authoring guard, not a cap on Pet
permanent totals, a Secondary-role threshold or an automatic role classifier.
No ATK/MAG ratio, equal-allocation requirement, concrete template values or
Species assignments are approved here. P13 still owns skills and scaling.

These are owner-approved Phimond thresholds, not recovered original-game math
or proof of combat viability. Q10.4's original Hybrid proposal is now adopted;
its Support bulk50% and Disruptor neutral-SPD minima were rejected in Q10.4d.
Primary/Secondary criteria are subsequently locked in Q10.5 below, coordinated
with P13 functional identity rather than fixed skill-count percentages.

---

# 15x. Q10.5 — Functional Primary/Secondary assignment — LOCKED

Owner approved on2026-10-12: assign roles using the Species' intended function,
supported jointly by authored stats and its planned Native Skill Pool. Primary
is the dominant functional identity. Optional Secondary is a supporting function
with a clear, practically usable contribution; one minor incidental effect does
not automatically qualify. No fixed skill-count or skill-percentage quota is
required. P10 permits content-driven Native Skill Pool sizes across Species.

P11 records the intended role rationale and stat checks. P13 cross-checks that
rationale against concrete native skill content/eligibility/scaling. Until that
content exists, describe the rationale as planned, not combat-validated. Roles
remain Species metadata and do not change with a Pet's current six-skill loadout
or inherited/NPC-learned skills. No skills are automatically granted and no hard
loadout restriction follows from role assignment.

This decision does not assign roles to the152 IDs or approve their stat/skill
content. Source descriptions are qualitative identity inputs, not recovered
Primary/Secondary labels. Ambiguous assignments still need documented rationale
and owner review, not a skill-count heuristic or a fabricated source label.
Lv1/growth Species modifier independence is subsequently locked in Q10.6 below.

---

# 15y. Q10.6 — Independent Lv1/growth Species modifiers — LOCKED

Owner approved on2026-10-12: each stat's Species modifier may be selected
separately for the Lv1 base layer and growth-baseline layer. There is no
requirement to use the same relative percentage in both layers. These are
fixed authored content choices, not individual RNG or per-level changes.

For each layer independently, final assignments must satisfy the existing
relative bounds (main four±10%, SPD/SR±5%), budget constraints, separate SPD/SR
ranges, Primary statistical signatures and functional-role rationale. One layer
cannot compensate for a violation in the other. Q10's Primary/Secondary blend
remains75/25 (or100% Primary without Secondary); this decision does not change
roles or blend weights between layers.

Illustration only: ATK+5% versus its Lv1 blended template and+8% versus its
growth blended template is permitted in principle, provided all other checks
pass in both layers. This does not approve those values for a Species or allow
unbalanced independent increases across the main budget. Actual template/
Species values, final quantization and Special tolerance remain open.

This is owner-approved Phimond authoring policy, not a recovered source formula.
Q11 below subsequently locks comparable states before numeric Star budgets.

---

# 15z. Q11 — Comparable states for Star/Special budget review — LOCKED

Owner approved on2026-10-12. Use the same Primary/Secondary roles and blend in
each comparison; inheritance=0, no equipment or temporary buffs. Use all six
grade B as the reference profile and all six Perfect as an additional check.
Compare like profiles with like profiles, not B against Perfect across bands.

Review authored Lv1 and growth budgets, plus grown stats at these level states:

| State | Level rule | Purpose |
|---|---|---|
| Lv1 | Common level1 | Initial base-stat differences |
| Common Lv60 | Level60 for all Stars/classes | Base + growth difference at equal level |
| Own base cap | 60/70/80/90/100 by Star | Combined budgets and base-cap advantage |
| Own +99 cap | 159/169/179/189/199 by Star | Combined budgets and Plus-cap advantage |

Special uses its own Star's level caps; no extra Star tier is created. Main
budget, SPD and SR are checked separately. Use the approved growth calculation
and per-stat cumulative floor when actual authored values are available. Do
not floor normalized HP contributions or replace an actual table check with
an unrounded aggregate approximation.

These are review conditions, not new growth odds or a guarantee that every
stat/combat matchup follows a universal ordering. Budget targets, Special
premium/tolerance, role templates and152 assignments remain open. Later combat
validation needs P13 content; this zero-inheritance comparison does not replace
inheritance design/long-run checks. No original-game numeric rule is asserted.
Next Q11.1: relative Normal Star main-budget targets before absolute anchors.

---

# 15aa. Q11.1a — Special4 intrinsic premium direction — LOCKED RANGE

Owner selected on2026-10-12: aim for Special4 main-budget intrinsic premium
around8–10% over Normal4 at equal role/blend/grade/level, with inheritance=0.
Revisit the unapproved Normal4→Normal5 spacing to make room, retaining the
approved half-step philosophy and Special4 below Normal5 in comparable states.

This approves a target range/direction, not a precise8%,9% or10% coefficient.
It does not approve the earlier Normal factor table, arithmetic interpolation,
Special base/growth allocation, tolerance, SPD/SR or any P13 skill mechanic.
Special4 retains4★ caps90/189. Own-cap comparisons remain required under Q11,
separate from the same-level premium goal. The~6% illustrative direction was
not selected. This is Phimond tuning, not recovered original-game math.

Normal factors are subsequently approved in Q11.1b below, widening the final
step. This range decision alone did not approve those factors.

---

# 15ab. Q11.1b — Normal Star main-budget factors — LOCKED

Owner approved on2026-10-12, explicitly choosing the wider final4★→5★ step.
Use these factors for each of Normal Lv1 main-budget target and Normal growth
main-budget target, with separate absolute1★ anchors:

| Star | Factor |
|---|---:|
| 1★ | 1.00 |
| 2★ | 1.10 |
| 3★ | 1.22 |
| 4★ | 1.36 |
| 5★ | 1.60 |

```text
normal_base_target[S] = base_target_1 × factor[S]
normal_growth_target[S] = growth_target_1 × factor[S]
```

Normal±3% tolerance still applies independently to final authored budgets in
both layers. These are content target factors, not another multiplier on final
Species stats at hatch or on inherited bonuses. SPD/SR are excluded. Both1★
absolute anchors, concrete role templates/Species values and quantization
remain open.

Additive gaps relative to1★ are0.10/0.12/0.14/0.24;4★→5★ increases target
by17.64706%. This approved choice refines Q1's slightly-increasing-gap wording
with an explicitly more pronounced final step. The earlier5★=1.52 proposal
was not approved and is superseded;1★→5★ target increase is now60%.

Special4 midpoint1.48 is subsequently approved separately for both layers in
Q11.2 below.
Special4 premium direction8–10% is locked by Q11.1a and resolved by Q11.2;
tolerance remains open; Special5 is subsequently approved in Q11.3 below. Q11 actual rounded/common-level/
own-cap checks are still required once absolute content exists. These are
Phimond design factors, not recovered original-game data or combat proof.
Q11.2 below subsequently approves Special4 interpolation/allocation.

---

# 15ac. Q11.2 — Special4 arithmetic midpoint per layer — LOCKED

Owner approved on2026-10-12. Special4's main-budget target is the arithmetic
midpoint of Normal4 and Normal5, applied separately to Lv1 and growth:

```text
special4_base_target = (normal4_base_target + normal5_base_target) / 2
special4_growth_target = (normal4_growth_target + normal5_growth_target) / 2
```

With Q11.1b factors, each equals1.48× its corresponding absolute1★ anchor.
Target premium over Normal4 is37/34−1≈8.82353%; Normal5 target is40/37−1≈8.10811%
above Special4. Absolute anchors remain separate and open. This applies to
main-budget targets only, not SPD/SR, inherited bonuses or a second multiplier
on finished stats. Same-layer targets are interpolated, not actual parent stats.

Special4 retains4★ level caps90/189 and P10 identity/recipe rules. Concrete
Species stats, Special tolerance, rounding/quantization and P13 skills remain
open. Equal premium factor on additive base/growth does not square that factor;
actual per-stat floors/content deviations still require Q11 validation. These
are approved Phimond tuning choices, not recovered original-game numbers.

Special5 extrapolation is subsequently approved in Q11.3 below without
adding a Normal6★ catalog tier.

---

# 15ad. Q11.3 — Special5 additive half-step per layer — LOCKED

Owner approved on2026-10-12. Extrapolate Special5 by adding half the final
Normal4→Normal5 target gap, separately for Lv1 and growth:

```text
special5_base_target = normal5_base_target + (normal5_base_target - normal4_base_target) / 2
special5_growth_target = normal5_growth_target + (normal5_growth_target - normal4_growth_target) / 2
```

Each equals1.72× its matching absolute1★ anchor; premium over Normal5 target
is7.5%. The approved factor sequence Normal4/Special4/Normal5/Special5 is
1.36/1.48/1.60/1.72, with equal absolute half-steps0.12. Special5 retains5★
caps100/199. No6★ catalog tier, extra hatch multiplier or inheritance factor
is introduced. The equal-relative-premium alternative148/85 was not selected.

Apply these factors to main-budget targets only. Absolute1★ anchors, actual
Species values, quantization, Special tolerance and SPD/SR remain open. Target
premiums do not force every individual Species pair's budget ratio to equal the
target ratio; authored tolerance and later per-stat floors need Q11 checks.
No universal ordering of arbitrary inherited Pets or combat matchups is claimed.
These are owner-approved Phimond values, not source-recovered data.
Special main-budget tolerance is subsequently locked to±2% in Q11.4 below.

---

# 15ae. Q11.4 — Special main-budget tolerance — LOCKED

Owner approved on2026-10-12: Special4 and Special5 final authored main budgets
must lie within±2% of their matching targets, inclusively. Check actual Lv1 and
growth-baseline budgets independently, before individual grades, inheritance,
equipment or temporary effects:

```text
0.98 × special_target[layer] <= HP/10 + ATK + MAG + DEF <= 1.02 × special_target[layer]
```

Normal tolerance remains±3%. Per-stat Species modifier bounds, Primary
signatures and separate SPD/SR ranges must still pass simultaneously. Do not
silently clip/relax constraints, compensate between layers or apply these
bounds to grown/inherited Pet totals. Special±3% was not selected.

Using the approved factors, authoring intervals relative to each layer's1★
anchor are Normal4[1.3192,1.4008], Special4[1.4504,1.5096],
Normal5[1.552,1.648], Special5[1.6856,1.7544]. All three adjacent bands have
positive separation at the main-budget authoring level. This is not universal
ordering of individual stats/owned Pets/combat outcomes. Target premium8.82%/
7.5% is not required for every actual Species pair. Q11 actual rounded checks
remain necessary once absolute content is approved.

These are owner-approved Phimond tolerances, not recovered source rules.
Absolute anchors, actual assignments, final quantization and SPD/SR remain
open. The absolute Normal1★ Lv1 anchor is subsequently locked to100 in Q11.5 below.

---

# 15af. Q11.5 — Absolute Lv1 main-budget anchor — LOCKED

Owner approved on2026-10-12: Normal1★ Lv1 main-budget target is100 points,
using HP/10+ATK+MAG+DEF. Combined with Q11.1b/Q11.2/Q11.3 factors:

| Band | Lv1 main target |
|---|---:|
| Normal1 | 100 |
| Normal2 | 110 |
| Normal3 | 122 |
| Normal4 | 136 |
| Special4 | 148 |
| Normal5 | 160 |
| Special5 | 172 |

Normal±3% and Special±2% apply around these targets independently from per-stat
modifier/role/range constraints. This approves actual target magnitudes, not
role allocation or any of the152 Species assignments. The50-point alternative
was not selected. Lv1 stats remain fixed Species content, not individual RNG.

The separate Normal1★ growth anchor is subsequently approved as2.000 in
Q11.6 below. These numbers
do not set SPD/SR/MP or combat damage/healing coefficients. Absolute scale is
owner-approved Phimond tuning, not recovered original-game stats. Q11 actual
per-stat/floor checks require approved role/Species content.
Growth anchor is subsequently approved in Q11.6 below.

---

# 15ag. Q11.6 — Absolute growth main-budget anchor — LOCKED

Owner approved on2026-10-12: Normal1★ growth-baseline main-budget target is
2.000 normalized points per level at grade B, defined by
HP_growth/10+ATK_growth+MAG_growth+DEF_growth. The3.000 alternative was not
selected. Apply approved factors and matching class tolerance:

| Band | Lv1 main target | Growth main target | Main tolerance per layer |
|---|---:|---:|---:|
| Normal1 | 100 | 2.000 | ±3% |
| Normal2 | 110 | 2.200 | ±3% |
| Normal3 | 122 | 2.440 | ±3% |
| Normal4 | 136 | 2.720 | ±3% |
| Special4 | 148 | 2.960 | ±2% |
| Normal5 | 160 | 3.200 | ±3% |
| Special5 | 172 | 3.440 | ±2% |

These are authored main-budget targets before individual grade multipliers,
inheritance/equipment/temporary effects; not a2-point increase to every stat
or a guarantee of exactly2 normalized points on each discrete level-up. Actual
six per-stat baselines/grade multipliers/cumulative floors determine Pet stats.
SPD/SR and MP remain separate and unapproved numerically.

Both absolute main anchors are now locked. Role template shares, actual152
Species assignments, quantization and P13 combat content remain open. This is
Phimond tuning, not recovered source growth. Q11 actual table checks remain
required; unrounded aggregate examples alone do not prove combat validity.
Role main shares are subsequently approved as shared across Lv1/growth in
Q11.7 below, before separately authored Species modifiers.

---

# 15ah. Q11.7 — Shared role main shares across Lv1/growth — LOCKED

Owner approved on2026-10-12: each role uses the same template percentage
allocation across HP/10, ATK, MAG and DEF for Lv1 and growth. Apply each layer's
own approved main-budget target to those shares. Secondary blend remains75/25,
or100% Primary if absent. Species modifiers still differ by layer under Q10.6.

For a main-budget target B and role shares summing1, construct the exact raw
template HP=10×B×share_HP, ATK=B×share_ATK, MAG=B×share_MAG, DEF=B×share_DEF.
Perform role blending and final content checks as approved. Actual shares are
not selected by this decision. Final quantization/assigned values must preserve
all constraints; shared shares do not bypass rounding/representability issues.

This applies only to the main four stats. It does not couple SPD/SR templates,
growth baselines, individual grades or actual Species modifiers between layers.
The separate-Lv1/growth-share alternative was not selected. No owned-Pet stat
ratios or current skill restrictions follow. This is Phimond authoring policy,
not a recovered source allocation table.
Concrete main shares are subsequently approved in Q11.8 below.

---

# 15ai. Q11.8 — Six-role main-budget shares — LOCKED

Owner approved on2026-10-12. Shares below sum100% per row and apply to each
role's Lv1/growth templates under Q11.7, before75/25 blending and independently
authored Species modifiers:

| Role | HP/10 | ATK | MAG | DEF |
|---|---:|---:|---:|---:|
| physical_dps | 25% | 45% | 10% | 20% |
| magic_dps | 25% | 10% | 45% | 20% |
| tank | 40% | 15% | 10% | 35% |
| hybrid | 25% | 30% | 30% | 15% |
| support | 25% | 25% | 25% | 25% |
| disruptor | 25% | 25% | 25% | 25% |

HP column is normalized budget contribution; raw HP template is10×that
contribution. For Normal1★ single-role Physical, the exact unmodified template
would be Lv1HP250/ATK45/MAG10/DEF20 and growthHP5/ATK0.900/MAG0.200/DEF0.400.
This derived template is not an approved assignment to any Species. Final
content still requires grid/precision and simultaneous constraint checks.

Support/Disruptor deliberately have neutral main shares; functional identity
must be cross-checked with P13. No MAG-based healing/status scaling, new bulk/
SPD minimum or automatic skill is inferred. SPD/SR targets remain separate.
Templates/modifier bounds still limit possible stat shapes; they do not allow
arbitrary redistribution of main budget. Roles are not automatic classifiers
of current Pet totals/loadouts.

Six single-role vectors and30 distinct75/25 blends satisfy budget and applicable
Primary signatures before modifier/quantization (worked arithmetic in
verification). Final modifiers may violate a signature even while budget/bounds
pass; recheck and rework content rather than relax the approved constraints.
These are owner-approved Phimond allocations, not recovered source values or
proof of combat validity. Actual152 assignments remain open.
Q11.9 below subsequently locks integer final Species base values; growth
precision remains at most three decimals under Q8.2.

---

# 15aj. Q11.9 — Integer Species Lv1 base values — LOCKED

Owner approved on2026-10-12: each of the six final Species base stat values at
Lv1 is an integer. Growth baselines remain at most three decimals (Q8.2).
Role/blend/budget intermediate values are computed exactly; the base grid does
not authorize prematurely rounding intermediate templates or widening bounds.

Author final values on the permitted grid and check all applicable modifier,
budget, Primary signature and auxiliary-range constraints simultaneously. If no
valid representable content exists, revise the proposed content/template and
review the change; do not silently clip, insert a floor or relax a constraint.
This decision does not specify an automatic round-nearest/tie-breaking seed
algorithm, nor authorize such an algorithm to produce invalid final content.

Example only: Normal3 Physical/Magic75/25 main template is
HP305/ATK44.225/MAG22.875/DEF24.4. CandidateHP305/ATK44/MAG23/DEF24 is integer,
within per-stat±10%, main budget121.5 within target122±3%, and passes Physical
ATK≥35% and ATK≥1.25×MAG. No candidate is assigned to a Species by this example.

This applies to Species base values, not inheritance bonus/output rounding,
SR chance arithmetic, equipment/effect rounding or arbitrary Pet totals.
The fractional-Lv1 alternative was not selected. Source evidence does not
establish this exact grid; it is owner-approved Phimond design.
Next Q12: Status Resistance units before choosing auxiliary target values.

---

# 15ak. Q12 — Status Resistance rating unit — LOCKED

Owner approved on2026-10-12: Status Resistance uses rating points, not a
stored direct resistance percentage. SR100 means100 rating points; it does
not by itself mean100% resistance, a100 percentage-point subtraction or
immunity. The six-stat base/growth/grade/inheritance pipeline retains this unit.
Species base SR is integer under Q11.9; its growth baseline retains at most
three decimals under Q8.2. Inheritance rounding is still open.

This unit decision does not approve a response curve, coefficient, Star/role
target, probability floor/ceiling, immunity rule, effective-SR stacking order
or P13 base-chance integration. Shared SR still affects harmful-status
application chance only, including control, poison/burn and stat reductions;
it does not alter duration/direct damage or imply outgoing status power.

The direct-percent alternative was not selected. This is owner-approved
Phimond design; existing APK/video/internet evidence does not establish this
rating unit or its numerical mapping as an original-game formula.
Next Q12.1: response shape, before selecting coefficients and auxiliary targets.

---

# 15al. Q12.1 — Diminishing SR resistance benefit — LOCKED

Owner approved on2026-10-12: at the same initial status application chance,
additional SR provides decreasing marginal resistance benefit as SR rises.
This selects the response shape, not a specific function or numerical curve.
The linear equal-benefit-per-point alternative was not selected.

No rational/exponential function, coefficient, skill-chance integration,
probability bounds, immunity behavior or effective-SR stacking order is
approved by this choice. Do not infer a stored SR cap from diminishing combat
benefit; inheritance remains governed by its separate contract. SR still uses
rating points and affects harmful-status application chance only.

This is Phimond design, not a recovered APK/video/internet equation.
Next Q12.2: proportional reduction versus percentage-point subtraction from
skill chance; coefficients and auxiliary targets remain open.

---

# 15am. Q12.2 — Proportional SR chance reduction — LOCKED

Owner approved on2026-10-12:

```text
chance_after_sr = chance_before_sr × (1 − resistance_effect)
```

Resistance effect is dimensionless; the SR rating-to-effect function is still
open and must respect Q12.1 diminishing marginal benefit. The input is the
status application chance presented to the SR stage. Its derivation from P13
skill data and ordering with other effects remain open. This expression does
not specify a second independent resistance roll or a complete combat pipeline.

Illustration only: resistance effect0.25 maps chance0.80→0.60 and0.20→0.15.
No SR rating is assigned effect0.25 by this example. Percentage-point
subtraction was not selected. Curve family/coefficient, probability bounds,
immunity, rounding/RNG precision and effective-SR stacking remain unapproved.
Shared SR scope remains application chance only, not duration/direct damage.

This is owner-approved Phimond design, not a recovered original-game formula.
Next Q12.3: immunity/limit behavior from SR alone, before exact curve tuning.

---

# 15an. Q12.3 — SR benefit approaches a ceiling below immunity — LOCKED

Owner approved on2026-10-12: as SR increases, resistance effect approaches a
ceiling strictly below100%. For a positive input application chance, the SR
stage retains a positive fraction of that chance, including in the limiting
case. The ceiling's numerical value and exact response function remain open.
This is a relative chance remainder, not an absolute percentage-point floor.
A zero input chance is not raised by this rule.

Do not infer a hard cap on stored SR or inheritance. This selects an
asymptotic benefit ceiling, not an early hard clamp at an arbitrary rating.
The alternatives of approaching100% or reaching100% at finite SR were not
selected. Independent skill/item immunity, other effect ordering, probability
precision and the exact P13 input-chance contract remain separate decisions.

This is Phimond design, not recovered original-game behavior.
Next Q12.4: numerical resistance-effect ceiling, before curve family/coefficient.

---

# 15ao. Q12.4 — SR resistance-effect ceiling80% — LOCKED

Owner approved on2026-10-12: the asymptotic resistance-effect ceiling is0.80.
At the SR stage, the limiting remaining chance is0.20×chance_before_sr.
This is not an absolute20% status chance floor. A50% input chance approaches
10%, a20% input approaches4%, and zero input remains zero.

The benefit approaches this ceiling; no finite-rating hard clamp, cap on
stored SR or inheritance, or independent immunity rule is authorized.
The90% and95% ceiling alternatives were not selected. Exact curve family,
coefficient/rating scale, auxiliary targets, P13 input chance/effect ordering,
and numerical precision remain open. Finite-rating results require the exact
curve, not replacement with the asymptotic limit.

This is Phimond balance design, not an APK/video/internet recovered constant.
Next Q12.5: exact response-function family, with its scale parameter still open.

---

# 15ap. Q12.5 — Rational SR response family — LOCKED

Owner approved on2026-10-12, for nonnegative SR and positive H:

```text
resistance_effect = 0.80 × SR / (SR + H)
chance_after_sr = chance_before_sr × (1 − resistance_effect)
```

SR0 gives zero resistance effect. SR=H gives0.40; SR=2H gives8/15
(approximately0.533333); SR=4H gives0.64. H is the half-ceiling rating.
The response rises with decreasing marginal benefit and approaches0.80,
retaining a limiting fraction0.20 of positive input chance. These are exact
function properties, not content balance certification. The exponential
alternative was not selected.

The value and context-dependence of H remain open. No global/level-scaled
parameter policy is inferred yet. Effective-SR calculation, negative-SR
handling, P13 input chance/effect ordering, numerical precision and independent
immunity remain unresolved. No stored-SR/inheritance cap follows.

This is Phimond design, not a recovered original-game equation.
Next Q12.6: whether H is a shared constant or depends on level, before its value.

---

# 15aq. Q12.6 — Shared constant H — LOCKED

Owner approved on2026-10-12: H is one shared positive constant, independent of
recipient level, Star and role. The level-scaled-H alternative was not selected.
At the SR stage, equal effective SR gives equal resistance effect under this
shared curve; input chance and other effects may still differ.

H's numerical value remains open. No actual SR target/range or Species rating
is approved here. Rescaling both H and SR by the same positive factor leaves
SR/(SR+H) unchanged; the eventual numerical scale and rating content must be
reviewed together. Integer base grids and growth precision still apply.
Effective-SR derivation, negative-SR handling, chance input/order, precision and
independent immunity remain open. This is Phimond policy, not recovered math.
Next Q12.7: numerical rating-scale convention before auxiliary target tuning.

---

# 15ar. Q12.7 — Shared H100 rating scale — LOCKED

Owner approved on2026-10-12: H=100, shared across level/Star/role.

```text
resistance_effect = 0.80 × SR / (SR + 100)   (SR≥0)
chance_after_sr = chance_before_sr × (1 − resistance_effect)
```

SR25/50/100/200 give effects0.16/4⁄15/0.40/8⁄15 respectively. These are
rating-scale examples, not approved Species targets. No base/growth rating,
Star/role range or level-benchmark resistance strength is selected here.
The alternate order of selecting benchmark strength before H was not chosen.

Effective-SR calculation, negative-SR handling, P13 chance input/order,
precision and independent immunity remain open. This is Phimond scale design,
not a recovered original-game constant. Next Q12.8: a neutral reference SR
target at the agreed comparison state, before base/growth allocation and roles.

---

# 15as. Q12.8 — Neutral SR reference50 at Normal1 Lv60 B — LOCKED

Owner approved on2026-10-12: the neutral reference template has SR50 at
Normal1★, Lv60, grade B, inheritance0 and no equipment/buffs, before Species
modifiers. This is an authoring anchor, not an assignment to every Species or
automatic designation of Support/Disruptor as neutral-SR roles.

With shared H100, resistance effect is4⁄15 (approximately26.6667%) and an
input chance1⁄2 yields11⁄30 (approximately36.6667%). The SR25 and75 reference
alternatives were not selected. Base/growth allocation must reproduce this
reference using the cumulative floor contract; their values remain open.
Role/Star auxiliary targets/ranges and actual Species content are not selected.
This is Phimond tuning, not source-recovered stats or combat certification.
Next Q12.9: neutral Normal1 SR base/growth allocation.

---

# 15at. Q12.9 — Neutral Normal1 SR base20/growth0.510 — LOCKED

Owner approved on2026-10-12: neutral Normal1★ template base SR20 and growth
baseline0.510. At grade B, SR=20+floor(0.510×(level−1)); Lv1/Lv60/Lv159
are20/50/100 respectively. This reproduces the Q12.8 reference anchor exactly
under cumulative floor. Values exclude inheritance/equipment/buffs and precede
Species modifiers. At Lv159 B the SR-stage effect is0.40 with H100.

The base10/growth0.680 and base30/growth0.340 alternatives were not selected.
No role/Species assignment, Normal Star scaling, Special SR premium, auxiliary
range width or specific Species modifier is approved by this split. Actual
content must satisfy the independent base/growth precision and modifier rules.
This is Phimond tuning, not source-recovered content or combat certification.
Next Q12.10: Normal SR Star target scaling.

---

# 15au. Q12.10 — Normal SR Star target factors — LOCKED

Owner approved on2026-10-12: Normal1★→5★ SR target factors are
1.00/1.03/1.06/1.09/1.12, applied to both neutral base and growth targets
before role and Species modifiers. Factors are relative to the Normal1 anchor,
not successive compound multipliers. Normal5 targets exceed Normal1 by12%.

| Normal Star | Factor | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 1 | 1.00 | 20 | 0.510 |
| 2 | 1.03 | 20.6 | 0.5253 |
| 3 | 1.06 | 21.2 | 0.5406 |
| 4 | 1.09 | 21.8 | 0.5559 |
| 5 | 1.12 | 22.4 | 0.5712 |

These are exact authoring targets, not final Species values. Intermediate
fractional bases and four-decimal growth targets do not waive Q11.9 integer
base or Q8.2 three-decimal final growth precision. Author final content on its
permitted grid, checking modifier/range constraints against exact targets;
do not silently round the target before those checks. Role targets, auxiliary
ranges and actual content remain open. Neither the20% alternative nor flat
Star scaling was selected. Special SR targets remain separately unresolved.
This is Phimond tuning, not recovered original-game growth.
Next Q12.11: Special SR target policy.

---

# 15av. Q12.11 — Special SR half-step targets — LOCKED

Owner approved on2026-10-12: Special4★ SR factor1.105 is the arithmetic
midpoint of Normal4/5 factors1.09/1.12; Special5★ factor1.135 adds half that
Normal4→5 gap to1.12. Both factors apply to neutral SR base/growth targets
relative to Normal1, before role/Species modifiers.

| Special Star | SR factor | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 4 | 1.105 | 22.1 | 0.56355 |
| 5 | 1.135 | 22.7 | 0.57885 |

Target premiums versus matching Normal are approximately1.37615%/1.33929%.
These are exact intermediate targets, not final Species stats: integer base,
three-decimal growth and all applicable constraints still apply. Do not round
targets before authoring checks. Small target differences plus modifiers,
grids and cumulative floor do not guarantee owned/Species SR ordering.
Main-budget factors/tolerances remain separate and unchanged; no main premium
is reapplied to SR. The same-as-Normal SR alternative was not selected.
Role targets, SR range widths and actual content remain open. This does not
activate source-gated Special operations. It is Phimond tuning, not recovered
original-game stats. Next Q12.12: SR role-target policy.

---

# 15aw. Q12.12 — SR role factors — LOCKED

Owner approved on2026-10-12: Tank/Support SR role factor1.10;
Physical DPS/Magic DPS/Hybrid/Disruptor factor1.00. Apply the same factor to
base/growth targets before the approved75/25 Primary/Secondary blend and
Species modifier. Single-role Species uses100% of its Primary template.

```text
blended_sr_target[layer] = neutral_normal1_sr[layer] × sr_star_factor
                          × (0.75×primary_sr_factor + 0.25×secondary_sr_factor)
```

Without Secondary, replace the parenthesized term by primary_sr_factor.
Neutral anchors20/0.510 and approved Normal/Special SR factors apply.
This authoring expression is not an extra multiplier on already authored
Species stats at runtime. Exact targets are retained through blend; final
Species base is integer and growth≤3 decimals with all constraints rechecked.
No actual Species role/content is assigned here. Disruptor incoming resistance
is distinct from P13 outgoing status effects; no auto-granted skill follows.
The all-role-neutral alternative was not selected. SR range widths remain
open; existing Species modifier bounds±5% remain mandatory. This is Phimond
tuning, not source-recovered role data. Next Q12.13: SR allowed range widths.

---

# 15ax. Q12.13 — SR target ranges±5% inclusive — LOCKED

Owner approved on2026-10-12: final authored Species SR base and growth must
each lie within[0.95×blended_target,1.05×blended_target], inclusively. Use the
same width for Normal and Special. Targets retain exact Star/role/blend
arithmetic. This range coincides with the existing±5% SR Species modifier
bounds; both requirements are satisfied by the same interval check.

Evaluate before individual grade, inheritance, equipment and temporary effects.
Base integer and growth≤3 decimals remain mandatory; base/growth checks are
independent, with no cross-layer compensation. This is not a range for owned
Pet totals and does not clamp inherited/effective SR. The tighter±3% range was
not selected. Actual Species values and effective-SR derivation remain open.
This is Phimond authoring policy, not recovered original-game tolerance.
Next Q12.14: negative effective-SR handling at the response stage.

---

# 15ay. Q12.14 — Floor negative effective SR at response input — LOCKED

Owner approved on2026-10-12:

```text
sr_for_response = max(0, effective_sr_before_response)
resistance_effect = 0.80 × sr_for_response / (sr_for_response + 100)
chance_after_sr = chance_before_sr × (1 − resistance_effect)
```

Negative effective SR produces zero resistance effect and preserves input
chance. This is a local response-input rule, not mutation of stored Species,
grown or inheritance values. Effective-SR derivation and buff/debuff ordering
remain separate unresolved contracts. No upper rating cap is introduced.
The negative-SR vulnerability alternative was not selected; do not add a
chance amplification branch below zero. Independent skill/item immunity and
status eligibility remain separate from this input floor.

This is Phimond design, not recovered original-game behavior.
Next Q12.15: one final application roll versus separate proc/resistance rolls.

---

# 15az. Q12.15 — One final status application roll — LOCKED

Owner approved on2026-10-12: each eligible attempt to apply one harmful
status uses one application roll at chance_after_sr. Do not add a separate
proc roll followed by a resistance roll. Example chance_before_sr0.50 and
SR100 give effect0.40, chance_after_sr0.30 and one roll at0.30.

This does not define hit checks, status eligibility, immunity exceptions,
multiple statuses' attempt/correlation policy, effect ordering, RNG precision
or UI failure labels. Those interfaces remain open with P13/P02; one roll
here does not mean one roll per whole skill/attack or no separate hit check.
The two independent application-stage rolls alternative was not selected.
This is Phimond design, not recovered original-game RNG behavior.
Next Q13: SPD ordering rule within its P10-D42 turn-order-only scope.

---

# 15ba. Q13 — Deterministic SPD comparison — LOCKED

Owner approved on2026-10-12: when order is compared by SPD, higher effective
SPD always precedes lower effective SPD. No RNG perturbs unequal-SPD ordering.
The probabilistic-SPD-order alternative was not selected. Preserve P10-D42:
SPD controls turn order only; no extra turns/action gauge/tick frequency follows.

Equal-SPD tie-breaking, order-snapshot timing, effective-SPD derivation/precision,
actor eligibility and P13 skill-priority interaction remain open. This choice
is a comparator contract, not a complete battle scheduler or implied fixed
round architecture. It does not approve SPD base/growth targets or Star/role
scaling. This is Phimond design, not recovered original-game sorting evidence.
Next Q13.1: equal-SPD tie-break policy.

---

# 15bb. Q13.1 — Battle-start fixed random tie priority — LOCKED

Owner approved on2026-10-12: draw random tie priority once at battle start and
retain it throughout that battle. Use this priority only when effective SPD
values are equal. Higher SPD still precedes lower regardless of tie priority.
Do not redraw on each comparison/order resolution or use universal slot/ID
precedence across battles. The per-order-redraw and fixed-slot/ID alternatives
were not selected.

Priority must define a consistent order, not independent random pairwise
comparisons that can contradict each other. Exact generation/storage/replay
implementation remains open. Late entrant/replacement actors, SPD snapshot
policy, effective-SPD precision and skill-priority interactions remain separate
unresolved contracts. This does not add actions or alter P10-D42 scope.
This is Phimond design, not recovered original-game tie behavior.
Next Q13.2: effect of SPD changes on an already established action order.

---

# 15bc. Q13.2 — Preserve established order until next ordering point — LOCKED

Owner approved on2026-10-12: SPD changes do not reorder an already established
action list. Use updated effective SPD when forming the next action order;
equal-SPD comparisons still use the fixed battle-start tie priority.
The immediate reordering of pending actors alternative was not selected.

This only controls reordering due to SPD changes. It does not keep a dead or
otherwise ineligible actor actionable, define when lists are formed, freeze
all combat state, choose round/tick architecture, or grant actions. Eligibility,
control effects, replacements/late entry, skill priority and action entitlements
remain P02/P13 interfaces. Effective-SPD derivation/precision also remains open.
Preserve P10-D42 turn-order-only scope. This is Phimond scheduling policy,
not source-recovered original-game timing.
Next Q13.3: neutral SPD authoring reference scale.

---

# 15bd. Q13.3 — Neutral SPD reference100 at Normal1 Lv60 B — LOCKED

Owner approved on2026-10-12: neutral reference SPD target100 at Normal1★,
Lv60, grade B, before Species modifiers, inheritance0/no equipment/buffs.
This is a numerical authoring scale for turn-order comparison, not action
frequency, extra turns or a guarantee of going before another specific pet.
The SPD50 scale alternative was not selected.

Base/growth split must reproduce this anchor using cumulative floor and
approved grids; its values remain open. No role is assigned this neutral
anchor automatically. Star/Special scaling, role targets/ranges and actual
Species content remain open. Integer grid/floor can affect ties, so numerical
scale is not treated as arbitrary after content authoring.
This is Phimond design, not a recovered original-game stat.
Next Q13.4: neutral Normal1 SPD base/growth split.

---

# 15be. Q13.4 — Neutral Normal1 SPD base40/growth1.020 — LOCKED

Owner approved on2026-10-12: neutral Normal1★ SPD template base40 and growth
baseline1.020. At grade B, SPD=40+floor(1.020×(level−1)); Lv1/Lv60/Lv159
are40/100/201. Values precede Species modifiers and exclude inheritance/gear/
buffs. This exactly reproduces the Q13.3 anchor under cumulative floor.

The20/1.360 and60/0.680 alternatives were not selected. This is an independent
SPD authoring decision, not a rule coupling SPD and SR or converting their
budgets. Roles using the neutral anchor, Normal/Special scaling, SPD ranges
and actual Species content remain open. The split does not increase action
frequency or grant extra turns. Final grids/modifier constraints still apply.
This is Phimond tuning, not source-recovered values or combat certification.
Next Q13.5: Normal SPD Star target factors.

---

# 15bf. Q13.5 — Normal SPD Star target factors — LOCKED

Owner approved on2026-10-12: Normal1★→5★ SPD factors
1.00/1.02/1.04/1.06/1.08, applied to both neutral base/growth targets before
role/Species modifiers. Factors are relative to1★, not compounded between
Stars. Normal5 targets exceed Normal1 by8%.

| Normal Star | SPD factor | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 1 | 1.00 | 40 | 1.020 |
| 2 | 1.02 | 40.8 | 1.0404 |
| 3 | 1.04 | 41.6 | 1.0608 |
| 4 | 1.06 | 42.4 | 1.0812 |
| 5 | 1.08 | 43.2 | 1.1016 |

These are exact intermediate authoring targets; final Species base remains
integer and growth≤3 decimals, with modifier/range checks against exact
blended targets. Do not silently round targets before checking content.
The12% and flat-scaling alternatives were not selected. Special SPD factors,
role targets/ranges and actual content remain open. Main/SR factors do not
apply to SPD. This is Phimond tuning, not recovered original-game values.
Next Q13.6: Special SPD target policy.

---

# 15bg. Q13.6 — Special SPD half-step targets — LOCKED

Owner approved on2026-10-12: Special4★ SPD factor1.07 is the midpoint of
Normal4/5 factors1.06/1.08; Special5★ factor1.09 adds half their gap to1.08.
Apply to both neutral base/growth targets relative to Normal1, before role
and Species modifiers. Main/SR factors remain separate.

| Special Star | SPD factor | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 4 | 1.07 | 42.8 | 1.0914 |
| 5 | 1.09 | 43.6 | 1.1118 |

Target premiums versus matching Normal are approximately0.94340%/0.92593%.
These are exact intermediate targets, not final Species values; integer base,
three-decimal growth and applicable modifier/range constraints still apply.
Do not round targets before checking final content. Modifier/grid/floor can
produce equal or inverted final SPD; no universal go-first guarantee follows.
The same-as-Normal alternative was not selected. Role/range/Species content
and source-gated Special operations remain unresolved. This is Phimond tuning,
not recovered original stats. Next Q13.7: SPD role-target table.

---

# 15bh. Q13.7 — SPD role factors — LOCKED

Owner approved on2026-10-12: Physical DPS/Magic DPS/Hybrid SPD factor1.00;
Tank0.90; Support1.05; Disruptor1.10. Apply the same role factor to base/growth
targets before75/25 Primary/Secondary blend and Species modifier. Single-role
uses100% Primary. Neutral Normal1 anchors are40/1.020; approved Normal/Special
SPD factors apply independently of main/SR.

```text
spd_target[layer] = neutral_normal1_spd[layer] × spd_star_factor
                   × (0.75×primary_spd_factor + 0.25×secondary_spd_factor)
```

Without Secondary, use primary_spd_factor alone. Exact intermediates precede
integer base/three-decimal final growth; all applicable constraints still
apply. No multiplier is reapplied to already authored Species stats at runtime.
This is template tendency, not new role-classification thresholds or a
universal Disruptor-before-Support guarantee. Q10.4d's rejection of universal
Disruptor SPD minima is preserved. Actual Species assignments, SPD ranges,
effective-SPD derivation/precision and priority interfaces remain open.
The all-neutral-role alternative was not selected. This is Phimond tuning,
not recovered role data. Next Q13.8: SPD allowed target ranges.

---

# 15bi. Q13.8 — SPD target ranges±5% inclusive — LOCKED

Owner approved on2026-10-12: final authored Species SPD base/growth must each
lie in[0.95×exact blended target,1.05×exact blended target], inclusively.
Normal/Special use the same width. This coincides with existing±5% SPD Species
modifier bounds, so the same interval check satisfies both requirements.

Keep Star/role/blend target arithmetic exact; final base is integer and growth
has at most three decimals. Check layers independently before grades,
inheritance/equipment/buffs; no cross-layer compensation. This is not a cap on
owned or effective SPD, nor a guarantee of final ordering between Species.
The±3% alternative was not selected. Actual content, effective-SPD derivation/
precision and P02/P13 scheduling interfaces remain open. This is Phimond
content policy, not recovered source tolerance.
Next Q13.9: negative effective-SPD handling for ordering.

---

# 15bj. Q13.9 — Floor negative effective SPD at comparison input — LOCKED

Owner approved on2026-10-12:

```text
spd_for_order = max(0, effective_spd_before_comparison)
```

Compare spd_for_order descending; equal values use the fixed battle-start tie
priority. Negative effective values all compare at0: −5 and−20 tie rather
than retaining a negative-order distinction. The signed-comparison alternative
was not selected. This is a local comparator input rule, not mutation of
stored Species/grown/inheritance stats or a cap on positive effective SPD.

Zero/negative input does not itself remove an action; eligibility/control
rules remain P02/P13 interfaces. Effective-SPD calculation/order, fractional
precision/rounding, late-entry and skill priority remain open. Preserve the
established-list policy Q13.2. This is Phimond design, not recovered source
behavior. Next Q13.10: fractional SPD at the comparison stage.

---

# 15bk. Q13.10 — Preserve fractional effective SPD in comparator — LOCKED

Owner approved on2026-10-12: retain the fractional part of effective SPD when
comparing, after max(0,effective SPD). Do not introduce an additional floor or
other rounding at the comparator. Thus50.9 precedes50.2, rather than tying at50.
Use fixed battle-start priority only when the actual comparison inputs are equal.
The floor-before-comparison alternative was not selected.

This does not select upstream effect math/precision, inheritance rounding,
storage representation or UI formatting. Integer Species bases and cumulative
floor on level growth remain unchanged; a fractional effective input may arise
from separately approved sources. No approximate-equality band is authorized
by this choice. Scheduling/eligibility/skill-priority and late-entry interfaces
remain open with P02/P13. This is Phimond design, not recovered source precision.
Next Q14: inheritance structure, preserving the approved total-based inputs,
Reinforcement floor and no-hard-cap/diminishing-gain contracts.

---

# 15bl. Q14 — Independent per-stat inheritance — LOCKED

Owner approved on2026-10-12: compute inheritance independently for each of
the six core stats, using only the matching current permanent totals from
both parents as parent-stat inputs. HP uses parent HP; ATK uses parent ATK;
MAG/DEF/SPD/SR follow the same matching-stat structure. No pooled parent-stat
budget, cross-stat redistribution or HP→ATK conversion is selected.

```text
candidate[s] = F_s(main_total[s], donor_total[s]; approved_parameters)
```

This selects structure, not F_s. Parent weights, coefficients, normalization,
diminishing-gain function, training-layer treatment, rounding and operation-
specific behavior remain open. Both totals include existing inheritance once
and exclude equipment/temp buffs under the accepted input contract. The
Reinforcement per-stat floor remains; do not extend it silently to Star-up or
source-gated Special operations. No hard cap or minimum positive gain follows.
Stat-specific parameters remain possible pending approval. This is Phimond
structure, not a source-recovered numeric inheritance equation.
Next Q14.1: combination of the two matching-stat parent inputs.

---

# 15bm. Q14.1 — Equal arithmetic parent-input weights — LOCKED

Owner approved on2026-10-12, independently for every core stat:

```text
parent_input[s] = (main_total[s] + donor_total[s]) / 2
```

These are current permanent matching-stat totals with old inheritance counted
once, excluding gear/temp effects. Preserve the exact mean at this stage;
this approval does not add rounding before the still-open inheritance math.
Example parent ATK100/200 gives raw input150, not child bonus150.
The70/30 Main/Donor alternative was not selected.

Swapping parents leaves the raw mean unchanged. Final operations can remain
asymmetric: Reinforcement retains its Main per-stat inheritance floor, while
Star-up/Special behavior is separately governed. No final output symmetry,
minimum positive gain or additional copy of Main inheritance is inferred.
Normalization/reference values, coefficients, diminishing function, training
and rounding/floor order remain open. This is Phimond design, not recovered
source weights. Next Q14.2: normalization reference policy.

---

# 15bn. Q14.2 — Fixed positive per-stat normalization references — LOCKED

Owner approved on2026-10-12:

```text
normalized_parent_input[s] = parent_input[s] / R[s]
R[s] > 0
```

Each stat has its own fixed reference R, shared across Species/Star/role.
The six reference values are still open. Using child Species Lv1 base as the
reference, or no normalization with raw-stat curves, was not selected.
Changing child Species/Star/role does not by itself change this normalization
reference. No cross-stat pooling/conversion follows; each input stays separate.

This does not choose output-unit conversion, curve family, coefficients,
reference values, training-layer treatment or rounding/floor order. Do not
reuse HP/10 main-budget normalization as an inheritance reference without
approval. A reference is a unit/curve-scale parameter, not an inheritance cap.
Reinforcement floor and operation-specific/source gates remain in effect.
This is Phimond design, not recovered source math.
Next Q14.3: conversion from normalized result to candidate stat-bonus units.

---

# 15bo. Q14.3 — Same-reference inheritance output units — LOCKED

Owner approved on2026-10-12:

```text
candidate_bonus[s] = R[s] × f_s(parent_input[s] / R[s]; approved_parameters)
```

The same positive fixed per-stat R converts dimensionless function output back
to stat-bonus units. Child Species Lv1 base is not the output-unit multiplier.
With equal input/R/function parameters, candidate bonus does not change merely
because child Species/Star/role changes. Final operation behavior may still
be asymmetric through the accepted Reinforcement Main floor and separate gates.

This selects unit conversion only. It does not define f_s, its coefficients,
R values, training contribution, rounding/floor order or approve operation-
specific parameters. Do not add Main inheritance as a second additive copy;
the accepted floor is a lower bound applied under a still-open order contract.
No cap/minimum gain is introduced by R. This is Phimond design, not recovered
source arithmetic. Next Q14.4: diminishing-response function family.

---

# 15bp. Q14.4 — Square-root inheritance response family — LOCKED

Owner approved on2026-10-12, common shape across six core stats:

```text
x = parent_input[s] / R[s]
f_s(x) = k_s × sqrt(x)               (x≥0, k_s>0)
candidate_bonus[s] = k_s × sqrt(R[s] × parent_input[s])
```

The last expression is algebraically equivalent to R[s]×f_s(x). Shape values
at x1/4/16/100 are1/2/4/10 before the coefficient. The log2(1+x) alternative
was not selected. Function output increases with diminishing marginal benefit
for positive input and is unbounded as input grows; no explicit bonus cap is
selected. Coefficient grouping/values, R values, rounding/floor order, training
and operation-specific behavior remain open. No runtime math is authorized.

Important qualification: unbounded response to unbounded input does not imply
unbounded inheritance under repeated fusion with bounded grown parent stats.
The square-root recurrence can have a finite invariant bonus bound even without
an explicit cap; the Reinforcement floor does not automatically remove that
bound. See verification for assumptions/proof. Whether this natural plateau
matches the intended long-run gameplay remains pending owner discussion.
This is Phimond design, not source-recovered inheritance.
Next Q14.5: accept a natural repeated-fusion bound or require unbounded accumulation.

---

# 16. Growth reroll semantics — LOCKED from P10

Do not redesign growth reroll into Quality/Distribution reroll types.

Current baseline already supports:

```text
Full Growth Reroll
Single-Stat Growth Reroll
```

The owner explicitly confirmed:

> Player may eventually Perfect all six growth stats.

Rarity, source, and cost of reroll items belong to later Items/Economy work.

P11 may define what mathematical reroll happens, but should not invent item economy.

---

# 17. Important unresolved P11 topics

The following remain open and must NOT be invented by Codex.

## Growth

Locked: seven names, fixed multiplier table, odds, shared source/reroll table.
Still open: exact joint sampling contract/PRNG precision/versioning, catalog/profile versioning, UI detail beyond readable grades.
No zero-sum constraint or additional within-grade optimization allowed.

## Star budgets

- exact Lv1 budget for each Star
- exact growth budget for each Star
- exact normalized Star-to-Star gaps
- exact SPD/SR Star scaling
- exact SPD/SR auxiliary normalization and bounds (main HP/10 weight locked in Q9.1)

## Normal Species

- auxiliary SPD/SR bounds (Normal main tolerance locked to±3% in Q9.2)
- exact role templates
- final assignment quantization (modifier limits locked in Q10.2; independent Lv1/growth choice locked in Q10.6)
- exact Species stat assignments
- exact Species growth-baseline assignments

## Special Species

- exact half-step interpolation formula
- exact Special base premium
- exact Special growth premium
- actual Special assignments/quantization (main tolerance±2% locked Q11.4)

## Roles

- final role list if not already canonical elsewhere
- role template values and final assignment quantization (75/25 blend locked in Q10)
- minimum constraints preserving primary-role identity
- exact role template values

## Inheritance

Still needs dedicated decisions:
- exact parent inputs
- main-parent vs secondary-parent weighting
- diminishing-return formula
- inheritance coefficients
- rounding
- reinforcement +99 floor behavior numerically
- interaction with parent level/training
- resolve any P10 wording inconsistency around inheritance input vs parent training

Do not silently invent these.

## MP

Still open:
- MP baseline/source
- whether MP grows with level
- Star effect on MP
- Species/role effect on MP
- exact first-hatch MP formula
- exact re-hatch MP formula beyond the already-locked rule that current MP becomes new maximum

## HP initialization / re-hatch

Needs numeric rules.

## Status Resistance

Still needs:
- application-chance formula
- exact scaling
- floor/ceiling
- whether 100% application immunity is possible
- rounding/order of operations

Status Resistance only affects application chance for:
- control,
- poison/burn,
- stat reductions.

It does not modify direct damage or status duration unless a later phase explicitly changes that.

## Species assignments

Still open:
- final stat/growth assignment for all 152 Species
- exact element/role assignment ownership if not already canonical
- verification that all Species remain viable inside intended niches

## Legacy migration

Detailed 14 → 152 Species migration remains later/open.

No silent name/appearance matching.

---

# 18. Other canonical constraints

## Plus

```text
+00 … +99
```

Plus increases level cap only.

Plus must NOT directly add or multiply stats.

## Reinforcement at +99

Allowed.

Output stays `+99` if common validation succeeds.

## Special

Special is a classification, NOT a sixth Star.

## Race

Race gives no automatic stat multiplier/bonus.

## Growth reroll

Changes growth profile only.

It does NOT:
- change Species,
- change Star,
- change Species Lv1 base stats,
- change inheritance bonus,
- change immutable parent restoration snapshots.

---

# 19. Recommended current P11 document outputs

P11 should remain design/document driven.

Suggested outputs:

```text
P11-design-decisions.md
P11-formulas.md
P11-stat-tables.md
P11-species-assignment.md
P11-verification.md
P11-readiness.md
```

Do not implement gameplay code until the design decisions and numeric tables are approved.

---

# 20. Current next interview question

Q7.6–Q7.12 resolved: fixed seven-grade multiplier/probability tables shared
across approved creation/reroll routes. Q8 linear level curve locked. Q8.1 cumulative floor locked. Q8.2 precision locked to three decimals. Q9 split budgets locked. Q9.1 HP/10 weighting locked. Q9.2 Normal main±3% locked. Q9.3 separate SPD/SR ranges locked. Q10 shared75/25 blend locked. Q10.1 relative per-stat modifier locked. Q10.2 main±10%/SPD-SR±5% limits locked. Q10.3 DPS/Tank signatures locked. Q10.4a Support and Q10.4b Disruptor functional scopes locked; Q10.4 proposals resolved by Q10.4d/f (no universal Support/Disruptor minima; Hybrid thresholds approved). Q10.4c excludes pure poison/burn damage from establishing Disruptor. Q10.4d rejects universal Support bulk/Disruptor SPD minima; all existing authoring constraints retained. Q10.4e locks Hybrid as dual physical/magic damage. Q10.4f Hybrid20%/20%/combined50% signature locked. Q10.5 functional Primary/Secondary criteria locked, no skill quota; P11 rationale/P13 cross-check. Q10.6 independent Lv1/growth Species modifiers locked. Q11 comparison states locked (all B + Perfect check; Lv1/Lv60/own base/+99 caps; zero inheritance/equipment/buffs; main/SPD/SR separate). Q11.1a Special4 premium direction8–10% locked; revise Normal4→5 spacing. Q11.1b Normal factors1/1.10/1.22/1.36/1.60 locked, separate base/growth anchors. Q11.2 Special4 midpoint1.48 per layer locked. Q11.3 Special5 factor1.72 per layer locked. Q11.4 Special main tolerance±2% locked. Q11.5 Lv1 main target anchor100 and derived targets locked. Q11.6 growth main anchor2.000 and derived targets locked. Q11.7 shared Lv1/growth role main shares locked; Species modifiers remain independent. Q11.8 six-role main share table locked. Q11.9 integer Species base values locked; growth precision≤3 decimals. Q12 SR rating unit locked. Q12.1 diminishing resistance benefit locked. Q12.2 proportional chance reduction locked. Q12.3 sub100% asymptotic benefit ceiling locked. Q12.4 effect ceiling80% locked. Q12.5 rational response0.80×SR/(SR+H) locked. Q12.6 shared constant H locked. Q12.7 H100 locked. Q12.8 neutral Normal1 Lv60 B SR50 anchor locked. Q12.9 neutral SR20/0.510 locked. Q12.10 Normal SR factors1/1.03/1.06/1.09/1.12 locked. Q12.11 Special SR factors1.105/1.135 locked. Q12.12 SR Tank/Support1.10 and other roles1.00 locked. Q12.13 SR ranges±5% inclusive locked. Q12.14 response input max(0,effective SR) locked. Q12.15 one final application roll locked. Q13 deterministic unequal-SPD comparison locked. Q13.1 fixed battle-start random tie priority locked. Q13.2 established order retained until next ordering point locked. Q13.3 neutral Normal1 Lv60 B SPD100 locked. Q13.4 neutral SPD40/1.020 locked. Q13.5 Normal SPD factors1/1.02/1.04/1.06/1.08 locked. Q13.6 Special SPD factors1.07/1.09 locked. Q13.7 SPD role-factor table locked. Q13.8 SPD ranges±5% inclusive locked. Q13.9 comparator input max(0,effective SPD) locked. Q13.10 no added comparator rounding locked. Q14 independent matching-stat inheritance locked. Q14.1 arithmetic parent mean50/50 locked. Q14.2 fixed positive per-stat R references locked. Q14.3 same R output-unit conversion locked. Q14.4 square-root response locked. Next **Q14.5 — Repeated-fusion plateau requirement**. Star budgets, inheritance,
resources/status and152 assignments still require dedicated decisions.

Q11.1 follow-up: owner asked how Special4 differs from Normal4/Normal5 rather
than approving the Normal target table. The proposed1.36/1.44/1.52 midpoint
comparison is illustrative only; Normal ratios, Special interpolation and
tolerance remain open. Q11.1a subsequently selects an8–10% premium direction
and review of Normal4→5 spacing. Q11.1b subsequently approves the revised
Normal factors, followed by Q11.2 Special4 midpoint approval; Q11.3 Special5 additive half-step approved; Q11.4 Special main tolerance±2% approved; Q11.5 Lv1 anchor100 approved; Q11.6 growth anchor2.000 approved; next Q11.7 role main-share structure.
