# Historical interview checkpoints — superseded

Current authority: [P11-final-spec.md](P11-final-spec.md). OPEN/LOCKED/status
statements below apply only to the recorded checkpoint. Numerical examples
are not the final catalog unless independently reproduced in current evidence.

# P11 — Formula contracts

Status: **PARTIALLY APPROVED DESIGN; SPECIES CONTENT/INHERITANCE/COMBAT ORDER OPEN**, 2026-10-12.
Authority: [owner decisions](P11-design-decisions.md) and P10 D07/D12–D16/D20.
Growth identities/grade tables and cumulative floor are owner-approved.
Inheritance and resource/status response functions remain unresolved; no
runtime implementation is authorized.

## Accepted identities

For each core stat `s`:

```text
individual_growth[s] = species_growth_baseline[s] × growth_multiplier[s]
permanent_total[s] = grown_stat[s] + inheritance_bonus[s]
grown_stat[s, Lv1] = species.base_stats[s]
effective_level_cap = base_star_cap + plus
```

`grown_stat` excludes inheritance/equipment. Growth multiplier affects earned
growth, not Lv1 base. There is no direct Plus or Race multiplier/addend.
Hatch and every level calculation use the individual's stored profile without
new RNG. Growth does not make the fixed inheritance bonus scale with level.

## Linear level accumulation + cumulative floor — LOCKED Q8/Q8.1

```text
accumulated_growth[s, level] = baseline[s] × stored_multiplier[s] × (level−1)
grown_stat[s, level] = species.base_stats[s] + floor(accumulated_growth[s, level])
```

Owner approved linear curve and cumulative floor2026-10-12. Floor once on the
exact accumulated growth. Do not round individual level gains or grow from a
previously rounded current stat; fractional contributions are retained through
exact recomputation. Direct/incremental leveling, level jumps and save/load
must agree. Lv1 growth is zero; inheritance is fixed and added once afterward.

Worked example: hypothetical baseline2.40, gradeA multiplier1.03.
Lv20:2.40×1.03×19=46.968, floor46. Lv21:2.40×1.03×20=49.44, floor49.
Per-level floor would incorrectly give38 atLv20. No baseline2.40 is assigned
to any Species. Cumulative round-half-up was not chosen.

Baseline precision is at most three decimal places (Q8.2). Represent the
baseline and multiplier as exact integer milli values:

```text
b = baseline × 1000
m = multiplier × 1000
earned_growth(L) = floor(b × m × (L−1) / 1000000)
```

Compute the complete numerator before the division/floor. Reject or explicitly
reapprove baseline values exceeding three decimals; no silent rounding. Prove
safe arithmetic bounds after actual Species baselines are approved. Integer
width/storage and catalog/profile versioning remain implementation questions.
This does not set inheritance, MP or status application rounding.

Example only: baseline2.405, A1.03, Lv20 → numerator47065850 → earned47.
No Species baseline is assigned by this example.

## Growth sampling — PARTIAL

Each core stat has its own weighted grade-bucket roll. After choosing a bucket,
resolve its multiplier from the fixed grade/stat-family table (Q7.6 = A). All six stats share
grade probabilities; SPD/SR may use narrower numeric bands. There is no shared
quality/zero-sum budget. All six Perfect must be reachable. Grade names, complete fixed multipliers and probabilities are approved in
Q7.7–Q7.11; same tables across creation/reroll routes in Q7.12. See stat tables.

Perfect is the top grade/band concept, resolved to its fixed representative
multiplier; no second within-band RNG or exact-maximum chase. Endpoint multipliers are approved: Perfect1.10 for HP/ATK/MAG/DEF,1.03 for
SPD/SR. There are no sampled within-grade thresholds; all grade multipliers are
approved. Numerical probability representation/joint sampling remain open.
The joint sampling/correlation policy is not numerically specified; never add
an anti-perfect constraint. Full reroll redraws six rolls; Single-Stat redraws
only the selected roll. No economy, pity or keep-best behavior is approved.

## Main Species authoring budgets — LOCKED Q9/Q9.1

```text
main_base_budget = base_hp / 10 + base_atk + base_mag + base_def
main_growth_budget = growth_hp / 10 + growth_atk + growth_mag + growth_def
```

Exact normalization; do not floor contributions. Evaluate Species base and
baseline budgets separately, without individual grades, inheritance/equipment.
SPD and SR each have their own target/range by Star/role (Q9.3). No shared
auxiliary pool or SPD↔SR conversion. Exact targets/range widths are OPEN.
Normal main tolerance is±3% of the target for each Star/layer (Q9.2), inclusive.
Base/growth checks must both pass without cross-layer compensation. Actual
absolute targets and SPD/SR range widths remain open; Special main tolerance
±2% is approved in Q11.4. Equal authoring budget does not
prove combat equivalence or original-game parity.

## Role blend — LOCKED Q10

```text
role_template = 0.75 × primary_template + 0.25 × secondary_template
```

If there is no Secondary, use100% Primary. Apply this common ratio to Lv1 and
growth-authoring templates and SPD/SR targets, before Species modifiers. Exact
auxiliary target values and actual assignments remain OPEN; authoring grids
are locked in Q11.9/Q8.2; Q10.2 fixes modifier
limits at main±10%, SPD/SR±5%.
Preserve exact blend arithmetic until the final authored Species assignment;
that final assignment must satisfy approved precision/budget/role constraints.
Actual Species stats/baselines already embody the blend; never multiply them
by75/25 again during hatch/leveling. Individual RNG and inheritance are separate.

## Species modifier method/limits — LOCKED Q10.1/Q10.2

```text
assigned_species_value[s] = blended_template_value[s] × (1 + modifier[s])
```

Measure each stat's relative deviation from the exact blended template, rather
than shifting percentage points of budget share. Final assigned values must lie in[0.90×template,1.10×template] for
HP/ATK/MAG/DEF, and[0.95×target,1.05×target] for SPD/SR, inclusively.
Apply to both Lv1 and growth-baseline authoring.
Validate the final assignment after any balancing/quantization against all
per-stat bounds, main budget, SPD/SR ranges, precision and primary signature.
This is a fixed Species authoring rule, not another runtime growth multiplier.
If constraints have no representable intersection, report the content conflict;
do not silently relax limits or clip. These are authoring bounds, not per-Pet
stat/inheritance caps. Q10.6 permits independent fixed per-stat modifier
percentages for Lv1 and growth; no cross-layer compensation for failed checks.
Zero template values cannot become nonzero via multiplication; resolve such
content cases explicitly without an invented additive minimum.

## Primary signature checks — LOCKED Q10.3/Q10.4f

For each final Species authored layer (Lv1, growth baseline), let B be its
actual main budget:

```text
physical_dps: ATK >= 0.35×B AND ATK >= 1.25×MAG
magic_dps: MAG >= 0.35×B AND MAG >= 1.25×ATK
tank: HP/10 + DEF >= 0.60×B
hybrid: ATK >= 0.20×B AND MAG >= 0.20×B AND ATK+MAG >= 0.50×B
```

All boundaries inclusive, checked separately for both layers. Do not apply to
Pet totals after individual growth/inheritance/equipment. These are authoring
guards, not gameplay class restrictions. Q10.4e defines Hybrid as dual physical/
magic damage; Q10.4f locks the numeric guard above without an ATK/MAG ratio. Q10.4d
adds no universal Support bulk or Disruptor SPD minimum; existing template,
budget, modifier and SPD/SR range checks still apply. Support/Disruptor
functional rationale must be checked against P13 content (Q10.4a–d); no
outgoing-status power is inferred from shared incoming SR.

## Role assignment — functional criteria LOCKED Q10.5

Primary reflects dominant function; optional Secondary reflects a clear, usable
supporting function. Use authored stats plus planned Native Skill Pool without
a fixed skill-count/% quota. P11 records rationale; P13 checks concrete content.
This is Species metadata, not a formula recomputed from current Pet skills.
Actual templates/assignments remain open; independent Lv1/growth modifiers
are approved in Q10.6 with every constraint checked on each layer.

## Species authoring grids — LOCKED Q11.9/Q8.2

Final six Species base values are integers. Each growth baseline has at most
three decimals. Keep role/blend/budget intermediate calculations exact; author
final values on their respective grids and recheck every budget, modifier,
Primary signature and auxiliary constraint. No silent clipping/relaxation for
unrepresentable content. Automatic seed rounding/tie-breaking is not selected.
Inheritance and effect/output rounding remain separate design gates.

## Role main-template construction — LOCKED Q11.7/Q11.8

Use each role's same main percentage vector in Lv1/growth, scaled by the
matching budget target B. Concrete percentage vectors (HP/10–ATK–MAG–DEF):
Physical25/45/10/20, Magic25/10/45/20, Tank40/15/10/35, Hybrid25/30/30/15,
Support25/25/25/25, Disruptor25/25/25/25 (Q11.8):

```text
HP_template = 10 × B × share_HP
ATK_template = B × share_ATK
MAG_template = B × share_MAG
DEF_template = B × share_DEF
```

Shares sum1. Blend roles75/25 or use100% Primary, then author Species modifiers
independently per layer. Recheck all constraints on final quantized content.
No SPD/SR coupling or owned-Pet ratio requirement follows.

## Normal main-budget targets — LOCKED Q11.1b

```text
factor[1..5] = [1.00, 1.10, 1.22, 1.36, 1.60]
base_target_1 = 100  # Q11.5
growth_target_1 = 2.000  # Q11.6
normal_base_target[S] = base_target_1 × factor[S]
normal_growth_target[S] = growth_target_1 × factor[S]
```

Lv1 anchor100 and separate growth anchor2.000 are approved in Q11.5/Q11.6.
Check each final Normal authored main budget
within97–103% of its matching target. Do not multiply final stats at hatch by
Star again. These factors do not apply to SPD/SR or inheritance. Special
main tolerance±2% is approved in Q11.4; Special5 additive half-step is approved in Q11.3.

## Special4 main-budget targets — LOCKED Q11.2

```text
special4_base_target = (normal4_base_target + normal5_base_target) / 2
special4_growth_target = (normal4_growth_target + normal5_growth_target) / 2
# each equals 1.48 × its matching absolute1★ anchor
```

Keep the anchors separate: Lv1 anchor100 gives Special4 target148; growth
anchor2.000 gives Special4 growth target2.960. Target premium over Normal4 is37/34−1. No
additional premium multiplier is applied to finished stats. Caps remain90/189.
SPD/SR and actual assignments remain open; Special main tolerance±2% is
approved in Q11.4; Special5 is
approved in Q11.3 below.

## Special5 main-budget targets — LOCKED Q11.3

```text
special5_base_target = normal5_base_target + (normal5_base_target - normal4_base_target) / 2
special5_growth_target = normal5_growth_target + (normal5_growth_target - normal4_growth_target) / 2
# each equals 1.72 × its matching absolute1★ anchor
```

Target premium over Normal5=7.5%; caps100/199. No6★ tier or additional
finished-stat multiplier. Special main tolerance±2% is approved in Q11.4;
Lv1 anchor100 gives Special5 target172; growth anchor2.000 gives target3.440.

## Special main-budget validation — LOCKED Q11.4

For each final authored Special4/Special5 layer (Lv1, growth baseline):

```text
B = HP/10 + ATK + MAG + DEF
0.98 × special_target[layer] <= B <= 1.02 × special_target[layer]
```

Boundaries inclusive. No cross-layer compensation; retain per-stat modifier,
Primary signature and SPD/SR checks. Applies before individual growth profile/
inheritance/equipment, not to owned-Pet totals. Normal remains±3%.

## Star/Special comparison states — LOCKED Q11

Hold roles/blend, grade profile and external conditions equal. Use all B as
reference and all Perfect for an additional check; inheritance=0 and no
gear/temporary buffs. Compare Lv1/growth budgets plus grown stats at Lv1,
common Lv60, own base cap and own +99 cap. Main/SPD/SR remain separate.
Special follows its Star's caps. Q11.2 resolves Special4 targets to1.48× each
matching1★ anchor (within Q11.1a's8–10% direction). Absolute anchors/assignments,
Special main tolerance±2% is approved in Q11.4; Special5 factor1.72 in Q11.3. Normal factors are approved in
Q11.1b. No Special factor is applied twice.

## Inheritance — input/floor accepted, function OPEN

```text
main_total[s] = main.grown_stat[s] + main.inheritance_bonus[s]
donor_total[s] = donor.grown_stat[s] + donor.inheritance_bonus[s]
parent_input[s] = (main_total[s] + donor_total[s]) / 2  # Q14.1
normalized_parent_input[s] = parent_input[s] / R[s]  # Q14.2: R[s]>0
candidate_bonus[s] = R[s] × f_s(normalized_parent_input[s]; approved_parameters)
```

Q14 locks independent matching-stat parent inputs: HP from parent HP, ATK
from parent ATK, and likewise MAG/DEF/SPD/SR. No cross-stat pool/redistribution.
Q14.4 locks f_s(x)=k_s×sqrt(x), x≥0,k_s>0, common shape for all six stats.
Equivalently candidate_bonus[s]=k_s×sqrt(R[s]×parent_input[s]).
It uses both current permanent totals, counts old
inheritance once, exclude equipment/temporary battle modifiers, support
approved diminishing returns and have no hard inheritance cap.

For Reinforcement, after the approved rounding/floor order:

```text
child.inheritance_bonus[s] >= main.inheritance_bonus[s]
```

The floor is a lower bound, not a second additive copy of main inheritance.
Zero gain is allowed. At +99 the same floor applies and output Plus stays +99.
Star-up inherits stats too, but this floor is not automatically extended to it.
Special inheritance remains source-gated in P10 O01; do not enable it here.

Q14.1 locks exact arithmetic50/50 mean of matching-stat totals before the
next inheritance steps. No rounding is added at the mean stage. Swapping
parents preserves this input, not necessarily operation-specific final output.
Q14.2 locks positive fixed references R[s] shared across Species/Star/role.
The six R values remain open. Q14.3 locks output conversion using the same
R[s], not child Species base, before final rounding/floor handling. No HP/10 budget
normalization or child-base reference is automatically reused here.
Still open: coefficient grouping/values, reference values, long-run plateau requirement,
training contribution, rounding and operation-specific behavior. P10 D08/D14
already imply stronger permanent stats from leveling may improve inheritance;
P15-specific training layers need explicit inclusion/exclusion. Do not replace
current-total inputs with parent Lv1 stats or raw bonus fields.

## Resources — OPEN except re-hatch MP

MP is separate from core growth-profile stats. Define maxMP source, level curve,
Star/Species/role effects, recovery and first-hatch initialization with P13.
At re-hatch, compute Lv1 maxMP using approved rules and set currentMP equal to
that value. Old MP amount/percentage is not carried over. Maximum HP uses the
HP stat pipeline; current HP at first/re-hatch still needs an initialization
policy. HP/status/cooldown restoration interfaces require P13/P16 coordination.

## Status application — OPEN

SR uses rating points (LOCKED Q12), not direct percent. SR100 does not by
itself mean100% resistance. Species base SR is integer; growth baseline≤3
decimals; inheritance rounding remains open.

Resistance benefit has decreasing marginal gains at the same initial status
chance (LOCKED Q12.1). Q12.5 selects the function below; H remains open.

Proportional integration is LOCKED Q12.2:

```text
chance_after_sr = chance_before_sr × (1 − resistance_effect)
```

`resistance_effect` is dimensionless, derived from SR by the Q12.5 function below.
`chance_before_sr` is the input chance at this stage; its derivation and ordering
with other effects remain open. This identity does not require a second
independent resistance roll. Example effect0.25: chance0.80→0.60,0.20→0.15;
no SR rating-to-effect coefficient is implied.

Q12.3/Q12.4 lock an asymptotic resistance-effect ceiling0.80. Thus the
limiting chance_after_sr is0.20×chance_before_sr. For input50%, the limit is
10%, not20%; input zero remains zero. Q12.7 locks H100; actual SR targets remain OPEN.
Positive input chance retains a positive fraction even at the limit;
this is not an absolute chance floor and does not raise zero input chance.
No stored-SR/inheritance cap or finite-rating hard clamp is inferred. SR alone
does not produce immunity; independent skill/item immunity remains unresolved.

Q12.5 selects the exact response family for SR≥0, H>0:

```text
resistance_effect = 0.80 × SR / (SR + 100)  # Q12.7: H=100
```

H is the half-ceiling rating: SR=H→effect0.40. SR0→0; SR=2H→8/15;
SR=4H→0.64. Q12.6 locks H as one shared positive constant, independent of level/Star/role.
Q12.7 locks its numerical value100. Equal effective SR gives equal effect at this
stage. Rescaling H and SR together preserves the curve, so rating targets and
H value must be assessed together.
Q12.14 uses max(0,effective_sr_before_response) as the response input; negative
effective SR gives zero resistance effect and preserves input chance. This
does not mutate stored stats. Effective-SR derivation/effect order remains open. The
exponential alternative was not selected.

Define the remaining P11 response parameters and P13 skill base-chance interface,
auxiliary SR targets, other probability bounds, independent immunity,
stacking and rounding
order. One shared SR stat applies to control, poison/burn and stat reductions.
No duration/direct-damage modification. No linear `chance − SR`, percent unit,
independent immunity or universal coefficient is assumed. No hard inheritance cap may
be smuggled in through a cap on the stored SR stat; probability bounds are a
separate combat rule that still needs approval.

## Neutral SR authoring anchor — LOCKED Q12.8

Before Species modifiers, neutral Normal1★ Lv60 gradeB SR target=50, with
inheritance0/no equipment/buffs. Its eventual integer base and three-decimal
growth baseline must satisfy base_sr + floor(growth_sr×59)=50.
Q12.9 locks neutral Normal1 base_sr=20 and growth_sr=0.510. At gradeB,
SR=20+floor(0.510×(level−1)): Lv1/60/159→20/50/100. Q12.10 locks Normal SR factors1/1.03/1.06/1.09/1.12 on base/growth targets
relative to1★, before role/Species modifiers. Q12.11 locks Special4/5 SR factors1.105/1.135 relative to1★ on both
base/growth targets. Q12.12 SR role factors are Tank/Support1.10, all other roles1.00, for both
base/growth before75/25 blend. Q12.13 allowed SR ranges are±5% inclusive of the exact blended target,
for each base/growth layer, both Normal and Special; the interval coincides
with existing SR modifier bounds. Actual Species content remains open. Fractional intermediate targets stay exact; final
Species grids remain integer base/three-decimal growth. This does not
assign the neutral anchor to a Species or automatically to any particular role.

SR target authoring, for each base/growth layer:

```text
sr_target = neutral_normal1_sr × sr_star_factor × blended_sr_role_factor
blended_sr_role_factor = 0.75×primary_sr_factor + 0.25×secondary_sr_factor
```

Single-role uses primary_sr_factor alone. Keep exact intermediates and validate
final integer base/three-decimal growth within approved Species modifier bounds.
Actual content already embeds these factors; no extra runtime multiplication.

Q12.13 final SR authoring interval: [0.95×sr_target,1.05×sr_target], inclusive,
separately for integer base and three-decimal growth. Evaluate before grades,
inheritance/gear/buffs; do not clamp owned Pet totals to this content interval.

## SR response input floor — LOCKED Q12.14

```text
sr_for_response = max(0, effective_sr_before_response)
resistance_effect = 0.80 × sr_for_response / (sr_for_response + 100)
chance_after_sr = chance_before_sr × (1 − resistance_effect)
```

No negative-SR vulnerability amplification or upper SR cap follows. This floor
only applies at the response stage; stored stats and the derivation/order of
effective SR remain separate contracts. Q12.15 selects one application roll per eligible single-status attempt at
chance_after_sr; no separate proc/resistance pair. Hit check, eligibility,
multi-status policy, numerical precision and UI feedback remain open.

## SPD ordering comparator — LOCKED Q13

When comparing by SPD, sort higher effective SPD before lower effective SPD.
No RNG perturbs unequal-SPD ordering. Q13.1 equal-SPD tie-break uses random priority drawn once at battle start,
retained for the battle and consulted only on equal SPD. It must form a
consistent order; no independent random pairwise comparison. Q13.2 preserves established lists on SPD changes and uses new SPD at the next
ordering point. When lists are formed, effective-SPD precision/derivation,
eligibility and skill-priority interactions
remain open. Preserve P10-D42 turn-order-only scope: no extra actions/gauge/tick
frequency or complete scheduling architecture is inferred. SPD content targets
remain unapproved.

Q13.1 tie priority never overrides unequal SPD and is not redrawn each order
resolution. Exact generation/persistence/replay and late-entry/replacement
policy remain open implementation/P02/P13 interfaces.

Q13.2: do not reorder an established action list merely because SPD changes;
use updated effective SPD at the next order formation. This does not define
round/tick structure or override dead/ineligible actor handling. P02/P13 owns
list-formation timing, action entitlements, control, replacements and priority.

## Neutral SPD reference — LOCKED Q13.3

Neutral Normal1★ Lv60 B SPD target100 before Species modifier, with
inheritance0/no equipment/buffs. Final template split must reproduce
base_spd + floor(growth_spd×59)=100 using integer base/milli growth. Q13.4 locks base_spd40/growth_spd1.020: B Lv1/60/159→40/100/201.
Q13.5 Normal SPD factors1/1.02/1.04/1.06/1.08 apply to both exact neutral
base/growth targets relative to1★, before role/Species modifiers. Role usage,
Q13.6 locks Special4/5 SPD factors1.07/1.09 on both neutral base/growth
targets relative to1★. Q13.7 SPD role factors Physical/Magic/Hybrid1.00, Tank0.90, Support1.05,
Disruptor1.10 apply to both layers before75/25 blend. Q13.8 SPD ranges±5% inclusive of exact blended targets are locked for both
layers, Normal/Special. Actual content remains open.
This authoring anchor does not define action frequency or extra turns.

SPD target authoring, separately for base/growth:

```text
spd_target = neutral_normal1_spd × spd_star_factor × blended_spd_role_factor
blended_spd_role_factor = 0.75×primary_spd_factor + 0.25×secondary_spd_factor
```

Single-role uses primary_spd_factor alone. Final Species values embody these
factors; do not apply them again at runtime. Keep exact target arithmetic and
check integer base/milli growth against coincident±5% inclusive modifier/range intervals.
This does not add a universal SPD threshold to functional role classification.

Q13.8 SPD range checks apply separately to final Species base/growth before
grades/inheritance/gear/buffs. This content interval does not cap owned or
effective SPD and does not guarantee matchup order.

## SPD comparator input floor — LOCKED Q13.9

spd_for_order=max(0,effective_spd_before_comparison). Compare descending;
equal values use fixed tie priority. Negative values compare at0 and do not
automatically remove an action. No stored-stat mutation or positive SPD cap.
Q13.10 retains fractional comparator inputs without extra floor/rounding.
Upstream precision/effect derivation, inheritance rounding and UI remain open.

Q13.10: retain fractional spd_for_order without added comparator rounding.
50.9 precedes50.2; only equal comparison inputs use fixed tie priority.
Source precision/representation and inheritance/effect rounding remain separate.

## Square-root inheritance long-run qualification — pending Q14.5

The selected function is unbounded in unbounded parent input. With fixed finite
R/k and grown parent stats bounded by G, however, bonus B≤L is invariant for
L=(A+sqrt(A²+4AG))/2, A=k²R, before rounding and with zero initial bonus.
Candidate≤sqrt(A(G+L))=L; retaining Main's bounded bonus as a floor does not
escape this bound. Actual rounding/training/operation parameters remain open.
This is conditional mathematical analysis, not a certified global runtime cap
or owner approval of a desired plateau. Resolve Q14.5 before tuning coefficients.
