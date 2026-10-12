# Historical interview checkpoints — superseded

Current authority: [P11-final-spec.md](P11-final-spec.md). OPEN/LOCKED/status
statements below apply only to the recorded checkpoint. Numerical examples
are not the final catalog unless independently reproduced in current evidence.

# P11 — Stat table design requirements

Status: **PARTIAL NUMERIC APPROVAL**, 2026-10-12. Growth multipliers/odds are approved; Species/Star budgets remain open.
Source: [owner decisions](P11-design-decisions.md), Q1–Q7.5.

## Accepted level caps

| Star | Base cap | Cap at +99 |
|---|---:|---:|
| 1★ | 60 | 159 |
| 2★ | 70 | 169 |
| 3★ | 80 | 179 |
| 4★ | 90 | 189 |
| 5★ | 100 | 199 |

Plus increases the cap only. Species Star/class budgets determine Lv1 and
growth separately; never apply Star multipliers again when hatching.

## Accepted growth grade table

| Grade | HP/ATK/MAG/DEF | SPD/Status Resistance | Probability per stat |
|---|---:|---:|---:|
| D | 0.90 | 0.970 | 3% |
| C | 0.95 | 0.985 | 12% |
| B | 1.00 | 1.000 | 40% |
| A | 1.03 | 1.009 | 28% |
| S | 1.06 | 1.018 | 12% |
| SS | 1.08 | 1.024 | 4% |
| Perfect | 1.10 | 1.030 | 1% |

Owner approvals Q7.6–Q7.12,2026-10-12. One fixed multiplier per grade/stat family,
no within-grade RNG. Same table for capture/Star-up/Reinforcement and both
reroll types. Full redraws six; Single redraws selected stat. No source boost.
Multipliers affect growth only, not Lv1 or inheritance; they do not set Star
scaling. B=baseline; probabilities total100%, B-or-better85%.

Worked arithmetic: mean multiplier1.0108(main group)/1.00324(SPD/SR);
Perfect/D growth ratios11/9 and103/97. Under independent repeated draws,
Perfect first-hit expectation100/stat. These do not specify item effort/cost,
whole-pet power, status probability or turn frequency. Joint sampling and
integer probability representation/versioning still need a precise contract.

## Accepted budget structure — Q9

Separate main HP/ATK/MAG/DEF budget and narrower SPD/SR budget, for both Lv1
and growth baselines. Allocate within each group, without unrestricted transfer
between groups. Q2 approximate same-Star Normal normalized parity still applies.
HP/10 normalization is approved in Q9.1. SPD/SR target values/bounds,
Normal main tolerance is±3% (Q9.2); auxiliary ranges and absolute Star target
absolute numbers remain open; relative Normal factors are locked in Q11.1b. “Narrower” does not compare raw unlike stat units.
Approved Q9.1 main budget: `HP/10 + ATK + MAG + DEF`. Use the same weights
for actual Lv1 base stats and Species growth baselines, with exact fractional
normalized contributions. Individual profiles/inheritance/equipment do not enter
these authoring budgets. Normal main budget: each of Lv1 and growth-baseline budgets must lie within
[0.97×target,1.03×target], inclusively, per Star. Neither layer compensates for
the other. Auxiliary range widths remain open; Special main tolerance±2% is
approved in Q11.4. Q9.3 uses separate
SPD/SR targets/ranges by Star/role; no shared pool or conversion. Q10 shared75/25 blend approved; single-role Species use100% Primary. Apply
to Lv1/growth templates and SPD/SR targets before Species modifiers. Template
values and final quantization remain open. Q10.1/Q10.2 choose relative per-stat
deviation: main stats±10%, SPD/SR±5%, for both Lv1/growth, inclusive. Validate bounds on final assignments, including after quantization
or balancing. Q10.3 signatures approved separately on base/growth final assignments:
physical_dps ATK≥35% main budget and≥1.25×MAG; magic_dps symmetric;
tank HP/10+DEF≥60% main budget. No clipping/rejection of inherited Pet stats.
Q10.4e defines Hybrid as dual physical/magic damage; Q10.4f locks its numeric guard: ATK≥20%×B, MAG≥20%×B, ATK+MAG≥50%×B. Support/Disruptor guards follow Q10.4a–d. Q10.4a locks
Support scope: ally recovery/protection/buffs/cleansing; no numeric threshold
is implied. Q10.4b locks Disruptor as control/debuffs that hinder actions or
reduce opponent effectiveness; no SPD threshold is implied. Q10.4c: pure
poison/burn damage alone does not establish Disruptor; SR scope is unchanged.
Q10.4d adds no universal Support bulk/Disruptor SPD minima; template, budget,
modifier and separate SPD/SR range checks remain required, with functional
rationale checked against P13 content. Hybrid checks apply separately to authored base/growth, not Pet totals or
Secondary role. No ATK/MAG ratio or actual template numbers are assigned.
Q10.5 assigns Primary by dominant function and optional Secondary by clear,
usable supporting function, using stats plus planned Native Skill Pool; no
skill-count/% quota. P11 records rationale, P13 cross-checks concrete content.
Role does not change with a Pet loadout. Q10.6 permits separate fixed Species
modifier percentages for Lv1/growth, with all constraints checked separately
and no cross-layer compensation. Q11 comparison states locked below. Q11.1a Special4 premium direction8–10% and Q11.1b Normal factors locked; Q11.2 Special4 midpoint1.48 per layer locked; Q11.3 Special5 factor1.72 per layer locked; Q11.4 Special main tolerance±2% locked; Q11.5 Lv1 anchor100 locked; Q11.6 growth anchor2.000 locked; Q11.7 shared main shares locked; Q11.8 concrete role main shares locked; Q11.9 integer base grid locked; Q12 SR rating unit locked; Q12.1 diminishing benefit locked; Q12.2 proportional chance reduction locked; Q12.3 sub100% asymptotic benefit ceiling locked; Q12.4 effect ceiling80% locked; Q12.5 rational curve locked; Q12.6 shared constant H locked; Q12.7 H100 locked; Q12.8 reference SR50 locked; Q12.9 neutral20/0.510 locked; Q12.10 Normal SR factors locked; Q12.11 Special SR factors locked; Q12.12 SR role factors locked; Q12.13 SR range±5% locked; Q12.14 response-input floor0 locked; Q12.15 one application roll locked; Q13 deterministic SPD comparison locked; Q13.1 fixed battle-start tie priority locked; Q13.2 preserved established order locked; Q13.3 reference SPD100 locked; Q13.4 neutral40/1.020 locked; Q13.5 Normal SPD factors locked; Q13.6 Special SPD factors locked; Q13.7 SPD role factors locked; Q13.8 SPD ranges±5% locked; Q13.9 comparator input floor0 locked; Q13.10 no comparator rounding locked; Q14 matching-stat inheritance locked; Q14.1 parent mean50/50 locked; Q14.2 fixed per-stat R locked; Q14.3 same R output units locked; Q14.4 square-root family locked; next Q14.5 repeated-fusion plateau.
This is an authoring metric, not a proof of combat equivalence.

## Q11.1 original proposal — NOT APPROVED; superseded by Q11.1b

Relative Normal main-budget target factors, proposed for both Lv1 and growth:

| Star | Factor relative to its layer's1★ target |
|---|---:|
| 1★ | 1.00 |
| 2★ | 1.10 |
| 3★ | 1.22 |
| 4★ | 1.36 |
| 5★ | 1.52 |

Proposed `base_target[S]=base_target[1]×factor[S]` and
`growth_target[S]=growth_target[1]×factor[S]`. The two absolute1★ anchors are
separate and remain open. Additive gaps relative to1★ rise0.10/0.12/0.14/0.16.
This proposal affects authored target budgets only, not a second multiplication
of final Species stats at hatch. Normal±3% checks still apply if adopted.
SPD/SR and Special factors are not included. Actual rounded tables and own-cap
advantages must be checked using Q11; these factors alone prove no combat
balance. This is proposed Phimond tuning, not recovered original-game data.

## Q11.1 discussion — Special4 difference, still UNAPPROVED

The owner asks how Special4 differs from Normal4/Normal5; this is not approval
of the Normal factor proposal. With illustrative Normal4=1.36 and Normal5=1.52,
an arithmetic midpoint would be Special4=1.44: target premium5.88235% over
Normal4 and target shortfall5.26316% versus Normal5. Arithmetic midpoint and
all these factors remain unapproved. This is a budget-target illustration,
not per-stat equality, effective combat power or original-game recovery.

Special4 retains4★ caps90/+99→189; Normal5 has100/+99→199. Species/recipe
identity follows P10; concrete skill distinctions depend on P13. Inheritance
is a separate layer and is zero in Q11 comparisons. No innate immunity,
extra skill slots, automatic skills or hidden Star tier is introduced here.

If Special4 hypothetically also used±3% tolerance, its minimum would be1.3968
versus Normal4 maximum1.4008, so these illustrative bands overlap. Special
tolerance is not yet approved. Strict nonoverlap versus Normal4 at this midpoint
would require Special4 lower tolerance strictly below2.72222%; comparison
against Normal5 and actual authored/floored tables must also be checked. This
is a conditional authoring finding, not an approved tolerance or a claim that
all roles/owned Pets must have universally ordered combat power.

Q11.1a subsequently selects the8–10% intrinsic Special4 premium direction and
review of Normal4→5 spacing. The~6% direction was not selected. Preserve
the approved half-step philosophy; exact interpolation/allocation remains open.

## Q11.1a direction / Q11.1b Normal factors — LOCKED

Owner approves Special4's same-state intrinsic main-budget premium direction
around8–10%, with Normal4→5 spacing reviewed first. Exact coefficients,
interpolation and Special layer allocation/tolerance remain open.

Approved Normal target factors for both base and growth, each relative
to its own separate1★ absolute anchor:

| Star | Approved factor |
|---|---:|
| 1★ | 1.00 |
| 2★ | 1.10 |
| 3★ | 1.22 |
| 4★ | 1.36 |
| 5★ | 1.60 |

Owner approves the earlier1★–4★ proposal and widens only the last step.
Additive gaps become0.10/0.12/0.14/0.24; the last step is more pronounced than
before (relative Normal4→5 increase17.64706%). Owner explicitly selects this
tradeoff, refining the earlier slightly-increasing-gap philosophy. No extra
Star factor is applied at hatch; Normal±3% tolerance remains unchanged.

Q11.2 subsequently approves midpoint Special4=1.48,8.82353% above Normal4;
Normal5 is8.10811% above Special4 at target-budget level. Both target layers
use their own midpoint; absolute anchors remain separate. Even if Special hypothetically had±3%, these
illustrative target-budget bands would be separate: Normal4 max1.4008 <
Special4 min1.4356, and Special4 max1.5244 < Normal5 min1.552. This is not an
approval of Special tolerance or universal per-stat/combat ordering.

Absolute anchors, actual rounded assignments, own-cap effects and SPD/SR still
need review. Special5 factor1.72 is subsequently approved in Q11.3. Normal factors above are approved Phimond
tuning; Special illustrations remain proposals, not original-game recovery.

## Q11.2 Special4 midpoint — LOCKED

Arithmetic midpoint separately for both target layers:

```text
special4_base_target = (normal4_base_target + normal5_base_target) / 2
special4_growth_target = (normal4_growth_target + normal5_growth_target) / 2
```

With Q11.1b factors this gives1.48× each corresponding1★ anchor, a target
premium37/34−1≈8.82353% over Normal4. Absolute anchors remain separate. This
decision does not determine Special tolerance, SPD/SR or concrete stats;
Special5 is subsequently approved in Q11.3.
Equal factor r on additive base/growth yields r×(base+growth), not r²; do not
multiply the resulting final stats by the premium again. Actual per-stat floors
and content deviations still require Q11 checks. Different premium allocation
across these two layers was not selected.

## Q11.3 Special5 additive half-step — LOCKED

Owner approves reusing half the final Normal4→5 target difference in each layer:

```text
special5_target = normal5_target + (normal5_target - normal4_target) / 2
# independently for base and growth targets
```

This gives1.72× the matching1★ anchor: target premium7.5% over Normal5.
Normal4/Special4/Normal5/Special5 factors become1.36/1.48/1.60/1.72, separated
by equal absolute half-steps0.12. Special5 retains5★ caps100/199. No6★ catalog
tier is created; no SPD/SR or inheritance factor is decided here.

Unselected alternative: mirror Special4's relative premium exactly, using
`normal5_target × (1.48/1.36)`, factor148/85≈1.74117647 and premium≈8.82353%.
Keep that rational factor exact if selected; the displayed decimal is not a
silent authoring-precision decision. Both formulas apply independently to both
target layers with separate anchors. Special tolerance, actual assignments and
quantization remain open. The additive-half-step choice is approved Phimond
design; the relative-premium alternative is not selected. Neither is source math.

## Q11.4 Special main tolerance — LOCKED

Owner approves±2% of each Special4/Special5 main-budget target, independently for
final authored Lv1 and growth baseline. Normal tolerance stays±3%. Per-stat
modifier bounds, role signatures and SPD/SR ranges remain separate constraints.
Approved authoring-factor intervals, each relative to its own layer's1★ anchor:

| Band | Tolerance used here | Interval |
|---|---:|---:|
| Normal4 | Approved±3% | 1.3192–1.4008 |
| Special4 | Approved±2% | 1.4504–1.5096 |
| Normal5 | Approved±3% | 1.5520–1.6480 |
| Special5 | Approved±2% | 1.6856–1.7544 |

Exact rational interval checks show three positive separations. These are
main-budget authoring intervals, not individual stat ranges or combat guarantees.
Target premium Special4≈8.82% / Special5=7.5% describes target ratios, not an
identical ratio for every Species pair. Floors require actual-content checks.
Using±3% also keeps these target bands separated;±2% is a tighter-content
choice, not an arithmetic necessity. Special±3% was not selected.

## Q11.5 Lv1 main-budget targets — LOCKED

Owner approves Normal1★ main-budget Lv1 target100 points, giving:

| Band | Approved Lv1 main-budget target |
|---|---:|
| Normal1 | 100 |
| Normal2 | 110 |
| Normal3 | 122 |
| Normal4 | 136 |
| Special4 | 148 |
| Normal5 | 160 |
| Special5 | 172 |

Illustration only: HP200/ATK45/MAG10/DEF25 gives HP/10+ATK+MAG+DEF=100.
This is not a Species/template assignment. Growth anchor, auxiliary stats/MP,
actual Species values and combat formulas remain separate. The inspected
APK/video evidence does not establish an original-game Lv1 anchor;100 is a
owner-approved Phimond scale, not source recovery.

## Q11.6 growth main-budget targets — LOCKED

Owner approves Normal1★ growth-baseline main-budget target2.000 normalized
points per level before individual multiplier/floor. Derived targets:

| Band | Approved growth main-budget target |
|---|---:|
| Normal1 | 2.000 |
| Normal2 | 2.200 |
| Normal3 | 2.440 |
| Normal4 | 2.720 |
| Special4 | 2.960 |
| Normal5 | 3.200 |
| Special5 | 3.440 |

These are sums HP_growth/10+ATK_growth+MAG_growth+DEF_growth, not a universal
increase of2 to each stat or a second grade modifier. Tolerances and all other
authoring constraints still apply separately. SPD/SR/MP remain excluded.

Target-level arithmetic for Normal1 all B, base budget100, inheritance0:
unrounded main total atLv60 would be218 and atLv159 would be416. Alternative
growth anchor3.000 yields277/574 at those levels. These unrounded aggregates
illustrate growth pace, not final Pet stats after per-stat floors.

Illustrative actual-floor example atLv60: baseHP200/ATK45/MAG10/DEF25;
growthHP4/ATK0.9/MAG0.2/DEF0.5 has main baseline2.000. All B gives actual
HP436/ATK98/MAG21/DEF54, normalized main216.6 rather than unrounded218.
No role template or Species is assigned by this example. The approved2.000
anchor is Phimond tuning, not source recovery; combat proof remains pending.
The3.000 alternative was not selected.

## Q11.7 shared role main shares — LOCKED STRUCTURE

Each role uses one percentage vector HP/10–ATK–MAG–DEF for both Lv1 and growth,
scaled by each matching target. Raw HP template=10×target×HP share; other raw
stats=target×share. Apply75/25 role blend (single-role100% Primary). Q10.6
Species modifier choices remain independent across layers. Concrete percentages are approved in Q11.8; final quantization requires
approval. Auxiliary SPD/SR remain separate.

## Q11.8 main-role share table — LOCKED

| Role | HP/10 share | ATK share | MAG share | DEF share |
|---|---:|---:|---:|---:|
| physical_dps | 25% | 45% | 10% | 20% |
| magic_dps | 25% | 10% | 45% | 20% |
| tank | 40% | 15% | 10% | 35% |
| hybrid | 25% | 30% | 30% | 15% |
| support | 25% | 25% | 25% | 25% |
| disruptor | 25% | 25% | 25% | 25% |

All six sum100%. Exact checks for six single-role vectors and30 distinct
75/25 blends preserve main budget and applicable Primary signature before
Species modifiers/quantization. Owner approves the percentage rows, not actual Species assignments or
all allowed modifier combinations as valid. Final signatures must be checked.

Support/Disruptor deliberately use neutral main shares to avoid assuming MAG
scales all support/debuff effects or imposing high universal bulk. Their
functional identity still needs P13 content; SPD/SR templates remain open.
Equal main vectors do not imply identical skills/auxiliary stats or role
interchangeability. The shared template and tight modifier bounds still limit
possible stat shapes; no arbitrary full redistribution is allowed.

Illustrative valid-bound/budget counterexample: Physical-primary/Magic-secondary
growth template at B2 is HP5/ATK0.725/MAG0.375/DEF0.4. FinalHP5.5/ATK0.653/
MAG0.375/DEF0.422 stays within each±10% bound and budget2, but ATK share32.65%
fails35%. That final assignment must be rejected/reworked, not its constraint
relaxed. Both values have at most three decimals. No example is assigned to a
Species; the invalid final example must be reworked. Percentage rows are
owner-approved Phimond allocations, not source recovery or combat proof.

## Species numerical grid — LOCKED Q11.9/Q8.2

Final Species base stats are integers; each growth baseline has at most three
decimals. Intermediate templates/blends stay exact. Author valid final values
and check all constraints simultaneously; no silent clipping or bound waiver.
This does not choose an automatic rounding seed algorithm or inheritance/effect
rounding. Actual assignments remain open.

## Tables requiring owner approval

| Table | Required parameters | Accepted constraints |
|---|---|---|
| Normal Star budgets | Main targets and role shares locked for Lv1/growth; actual assignments open; integer base/≤3-decimal growth grids locked | Both layers scale; final4★→5★ step explicitly widened |
| Normal main tolerance | Approved ±3% per Star/layer; absolute targets locked Q11.5/Q11.6 | Separate checks for Lv1 and growth baseline; no cross-layer compensation |
| Stat normalization | HP/10 + ATK + MAG + DEF locked; SPD/SR separate ranges by Star/role; widths open | Raw unlike units cannot be summed without an approved definition |
| SPD/SR scaling | SR and SPD factors/role targets/ranges locked through Q13.8; actual content open | Narrower/weaker than HP/ATK/MAG/DEF |
| Special budgets | Special4 factor1.48 and Special5 factor1.72 per layer plus±2% tolerance locked; Lv1 targets148/172 and growth targets2.960/3.440 locked; assignments/quantization open | Normal4 < Special4 < Normal5 < Special5 in defined comparable state |
| Roles | Initial six-role vocabulary reused;75/25 blend locked; modifier limits main±10%/SPD-SR±5% locked; main shares locked Q11.8 and numerical grids Q11.9/Q8.2; auxiliary targets/actual assignments open | Primary + optional secondary; global fixed blend; primary recognizable |
| Growth sampling details | Joint sampling, probability precision/versioning, grade presentation | Approved seven-grade table above; no hidden within-grade RNG |
| Grade value resolution | Fixed grade/stat-family lookup; numeric precision | Q7.6 = A; baseline/multiplier precision at most three decimals (Q8.2) |
| Inheritance | Parent weighting, coefficients/response scales | Diminishing gain, no hard cap, main floor for Reinforcement |
| Resources/status | MP/HP initialization open; SR curve/H100/80% ceiling locked, effective-SR/chance input/order/precision open | Separate MP; shared SR application-only |

±5% budget tolerance, Perfect0.5% and109.5–110% interval in the
original owner state remain unapproved illustrations. Explicitly approved
growth numbers above supersede the earlier “all values open” checkpoint. Q11.2/Q11.3 explicitly approve arithmetic midpoint/additive extrapolation
for main targets; SPD/SR do not inherit those formulas automatically. Special5 does not require creating a 6★ catalog row.

## Comparable-state definition — LOCKED Q11

Same Primary/Secondary roles and blend; inheritance=0, no equipment or temporary
buffs. All six grade B is the reference; all six Perfect is an additional check.
Compare matching profiles across bands. Review Lv1/growth budgets and grown
stats at Lv1, common Lv60, each Star's own base cap and own +99 cap. Special
uses its Star's caps. Check main budget, SPD and SR separately. Once actual
values exist, compute per-stat growth/floor as approved, not just an unrounded
aggregate. No numeric Star/Special target is approved by these conditions.

Higher cap adds further Star advantage beyond base/growth budgets. Infinite
uncapped inheritance makes universal cross-Star superiority claims invalid;
compare specified equivalent investment rather than arbitrary player pets.
Same normalized raw budget is not proof of combat parity: roles, turn order,
skills, healing and statuses need P13/P02/P15 review.

Specify numeric primary-role constraints and modifier renormalization so a
secondary blend or species modifier cannot accidentally create extra budget or
remove Tank HP/DEF identity. Define treatment of a Species without a secondary.
Do not assign arbitrary per-Species blend ratios.

## Current SR contract — owner-approved through Q12.15

- Response input S=max(0,effective SR); effect=0.80×S/(S+100).
- Application chance=input chance×(1−effect); one application roll per eligible
  single-status attempt. SR only affects application, not duration/direct damage.
- Neutral Normal1 base20/growth0.510; at B Lv1/60/159 SR20/50/100 before modifiers.
- Normal Star factors1/1.03/1.06/1.09/1.12; Special4/5 factors1.105/1.135.
- Tank/Support role factors1.10; others1.00; blend75/25, single-role100% Primary.
- Final Species base integer/growth≤3 decimals, each within±5% inclusive of
  exact blended target, before grades/inheritance/gear/buffs.

Actual Species content, effective-SR derivation/order, P13 input chance/hit/
eligibility/immunity/multi-status contracts and numerical precision remain
open. SPD remains separate. The following Q12 sections are chronological
checkpoints; later approvals supersede earlier statements of open decisions.

## Status Resistance unit — LOCKED Q12

SR is measured in rating points, not direct resistance percent. SR100 is100
points, with no implied100% resistance or immunity. Species base SR is integer
and its growth baseline≤3 decimals; inheritance rounding remains open.
Response shape/coefficient, numeric auxiliary targets, chance bounds/immunity
and P13 skill integration remain unapproved.

## Status Resistance response shape — LOCKED Q12.1

At the same initial status chance, resistance benefit increases with SR while
benefit per additional point decreases as SR rises. Exact function, coefficient,
chance integration/bounds/immunity and auxiliary target values remain open.
This selects a curve shape only; it does not cap stored SR or inheritance.

## SR chance integration — LOCKED Q12.2

Chance after SR = chance before SR × (1 − resistance effect). Rating-to-effect
curve/coefficient, chance bounds/immunity, effect ordering and numerical
precision remain open. Example effect25% maps80%→60% and20%→15%; this is not
a rating-to-effect assignment or authorization for a second resistance roll.

## SR benefit limit — LOCKED Q12.3

Resistance effect approaches a ceiling below100%; the numerical ceiling is
OPEN. SR retains a positive fraction of positive input chance even at the
limit, not an absolute percentage-point floor. Zero input chance stays zero.
No cap on stored SR/inheritance follows. Independent immunity and curve tuning
remain open; reaching or approaching100% resistance from SR was not selected.

## SR numerical benefit ceiling — LOCKED Q12.4

Effect approaches0.80; limiting chance is0.20×input chance, not a20% absolute
chance floor. Example input50%→limit10%, input20%→limit4%, zero→zero.
Curve family/scale and actual rating targets remain open; finite-rating results
cannot be calculated by simply substituting this asymptotic limit.

## SR response family — LOCKED Q12.5

Effect =0.80×SR/(SR+H), for SR≥0,H>0. At SR0/H/2H/4H effects are
0/0.40/8⁄15/0.64. H policy/value and auxiliary rating targets remain open.
Negative-SR handling, effective-SR derivation and numerical precision are not
selected by this function-family approval.

## Shared H policy — LOCKED Q12.6

H is a shared positive constant, independent of level/Star/role. Its numerical
value and actual auxiliary targets remain open. Equal effective SR yields
equal effect at the SR stage; input chance/other effects may differ. Scaling
H and all SR by the same factor leaves effects unchanged, subject to authoring
grids/rounding. This policy does not approve a numerical balance target.

## SR rating scale — LOCKED Q12.7

Shared H=100. Effect=0.80×SR/(SR+100) for SR≥0.

| SR (examples, not content targets) | Resistance effect | Remaining input chance fraction |
|---|---:|---:|
| 25 | 16% | 84% |
| 50 | 26.666…% | 73.333…% |
| 100 | 40% | 60% |
| 200 | 53.333…% | 46.666…% |

No Species/role/Star base or growth target is approved by selecting this scale.

## Neutral SR reference anchor — LOCKED Q12.8

Normal1★ Lv60 gradeB, inheritance0/no equipment/buffs, template before Species
modifier: SR50. Effect4⁄15≈26.6667%; input chance50%→11⁄30≈36.6667%.
Base/growth split, role/Star targets/ranges and Species content remain open.
No actual role is automatically assigned this neutral reference.

## Neutral Normal1 SR split — LOCKED Q12.9

Base SR20; growth baseline0.510. At B, grown SR=20+floor(0.510×(L−1)).
Lv1/60/159→20/50/100, before Species modifier and without inheritance/gear/buffs.
Roles/Species using this anchor, Normal Star scaling, Special SR targets and
auxiliary range widths remain open. The10/0.680 and30/0.340 alternatives were
not selected. Lv159 SR100 gives40% SR-stage resistance effect, not immunity.

## Normal SR Star targets — LOCKED Q12.10

| Normal Star | Factor vs1★ | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 1★ | 1.00 | 20 | 0.510 |
| 2★ | 1.03 | 20.6 | 0.5253 |
| 3★ | 1.06 | 21.2 | 0.5406 |
| 4★ | 1.09 | 21.8 | 0.5559 |
| 5★ | 1.12 | 22.4 | 0.5712 |

Same factors for base/growth before role/Species modifiers, relative to1★,
not compounded between Stars. These exact targets precede final authoring
grids: Species base integer, growth≤3 decimals. Check against exact targets;
do not round them early. Role/range/content and Special SR targets remain open.

## Special SR targets — LOCKED Q12.11

| Special | Factor vs neutral Normal1 | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 4★ | 1.105 | 22.1 | 0.56355 |
| 5★ | 1.135 | 22.7 | 0.57885 |

Half-step on the SR-specific Normal4→5 gap, applied to both exact base/growth
targets before role/Species modifiers. Final content remains integer base and
growth≤3 decimals; no early target rounding. Main premium/tolerances are
separate. Target order is not guaranteed final SR order; roles/ranges/content
and source-gated Special operations remain unresolved.

## SR role targets — LOCKED Q12.12

| Role | SR factor for base and growth |
|---|---:|
| Physical DPS | 1.00 |
| Magic DPS | 1.00 |
| Tank | 1.10 |
| Hybrid | 1.00 |
| Support | 1.10 |
| Disruptor | 1.00 |

Multiply neutral Normal1 anchors20/0.510 by the approved Star/Special SR factor
and role factor; blend Primary/Secondary75/25 (single-role100% Primary), then
author Species values within modifier/grid constraints. Do not multiply already
authored Species stats again at runtime. Range widths and Species content remain
open; Disruptor SR is incoming resistance, not outgoing status power.

## SR content ranges — LOCKED Q12.13

Final Species SR base/growth must each lie in[0.95×exact blended target,
1.05×exact blended target], inclusive, for Normal/Special. This coincides with
SR modifier bounds; retain exact targets and check integer base/milli growth
independently before grade/inheritance/gear/buffs. No owned-total cap follows.
The±3% alternative was not selected. Actual content and combat pipeline remain
open; SPD authoring targets/ranges are still separate pending decisions.

## Effective-SR input floor — LOCKED Q12.14

Use max(0,effective_sr_before_response) in the H100 response. Negative input
gives zero resistance effect and preserves chance_before_sr. No vulnerability
amplification or stored-stat mutation follows. Effective-SR ordering/derivation,
application roll count and numerical precision remain open.

## Status application roll — LOCKED Q12.15

One roll at chance_after_sr per eligible attempt to apply one status. No extra
proc/resistance pair. Eligibility, hit checks, immunity, multi-status correlation,
RNG precision and UI feedback are separate unresolved interfaces.

## Current SPD contract — owner-approved through Q13.10

- Compare unequal effective SPD descending, without RNG perturbation.
- Equal SPD uses consistent random priority drawn once at battle start, retained
  within battle. SPD changes apply at the next order formation, not by reordering
  an established list. P10-D42 turn-order-only scope remains in effect.
- Neutral Normal1 base40/growth1.020; B Lv1/60/159→40/100/201 before modifiers.
- Normal Star factors1/1.02/1.04/1.06/1.08; Special4/5 factors1.07/1.09.
- Physical/Magic/Hybrid role factors1.00, Tank0.90, Support1.05, Disruptor1.10;
  blend75/25, single-role100% Primary.
- Final integer base/milli growth each within±5% inclusive of exact blended
  target, Normal/Special, before grade/inheritance/gear/buffs.

Q13.9 comparator uses max(0,effective SPD); negative values tie at0 without
automatic action loss. Q13.10 retains fractional inputs without extra rounding. Actual content, effective-SPD derivation/precision and P02/P13
list formation/eligibility/priority/late-entry interfaces remain open. The
following SPD checkpoints are chronological; later approvals supersede earlier
open statements.

## SPD order comparison — LOCKED Q13

Higher effective SPD precedes lower when comparing by SPD; no random perturbation
for unequal values. Q13.1 equal-SPD ties use random priority drawn once at battle start, fixed
throughout the battle. Snapshot timing, effective-SPD precision,
priority/eligibility and actual content targets remain open. This does not
introduce extra actions or a scheduler under P10-D42.

## SPD equal-value ties — LOCKED Q13.1

Draw random tie priority once at battle start, retain within battle and use
only for equal SPD. Unequal-SPD comparison stays deterministic. Consistent
priority order is required; no random per-pair comparisons/redraw per order.
Exact implementation/replay and late-entry/replacement policy remain open.

## SPD change timing — LOCKED Q13.2

Keep established action order when SPD changes; updated SPD is used at the
next order formation. Eligibility/death/control and action entitlement rules
remain separate; this does not freeze other combat state or define rounds.
SPD numerical targets and effective-SPD derivation/precision remain open.

## Neutral SPD reference anchor — LOCKED Q13.3

Normal1★ Lv60 B target SPD100 before Species modifier, inheritance0/no gear/
buffs. This is a turn-order stat scale; base/growth split, role assignment to
the neutral anchor, Star/Special factors and ranges remain open. No extra
actions or guaranteed matchup ordering follows.

## Neutral Normal1 SPD split — LOCKED Q13.4

Base40/growth1.020; B grown SPD=40+floor(1.020×(L−1)).
Lv1/60/159→40/100/201 before Species modifier and without inheritance/gear/buffs.
Role usage, Normal/Special factors, SPD ranges and actual content remain open.
This is independent of SR targets and does not change action frequency.

## Normal SPD Star targets — LOCKED Q13.5

| Normal Star | Factor vs1★ | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 1★ | 1.00 | 40 | 1.020 |
| 2★ | 1.02 | 40.8 | 1.0404 |
| 3★ | 1.04 | 41.6 | 1.0608 |
| 4★ | 1.06 | 42.4 | 1.0812 |
| 5★ | 1.08 | 43.2 | 1.1016 |

Same factor on exact base/growth targets before role/Species modifiers,
relative to1★. Final Species grids remain integer base/growth≤3 decimals.
Do not round targets early. Special SPD/role/ranges and actual content remain
open; no SR/main factor is automatically applied here.

## Special SPD targets — LOCKED Q13.6

| Special | Factor vs neutral Normal1 | Neutral base target | Neutral growth target |
|---|---:|---:|---:|
| 4★ | 1.07 | 42.8 | 1.0914 |
| 5★ | 1.09 | 43.6 | 1.1118 |

SPD-specific half-step applied to exact base/growth targets before role and
Species modifiers. Keep integer base/three-decimal final growth and check
against exact targets. No guaranteed final SPD/go-first ordering follows.
Role/ranges/content remain open; main/SR factors are not reapplied here.

## SPD role factors — LOCKED Q13.7

| Role | SPD factor for base and growth |
|---|---:|
| Physical DPS | 1.00 |
| Magic DPS | 1.00 |
| Tank | 0.90 |
| Hybrid | 1.00 |
| Support | 1.05 |
| Disruptor | 1.10 |

Multiply neutral Normal1 anchors40/1.020 by SPD Star factor and role factor;
blend75/25 (single-role100% Primary) before Species modifiers. Exact targets
precede final grids. This is authoring tendency, not a role threshold or
universal speed order. SPD ranges, actual content and effective-stat/priority
interfaces remain open; no factors are reapplied at runtime.

## SPD content ranges — LOCKED Q13.8

Final Species base/growth separately within±5% inclusive of exact blended SPD
target, Normal/Special. This coincides with Species modifier bounds; preserve
integer base/milli growth and exact target arithmetic. Evaluate before grade/
inheritance/gear/buffs. No owned/effective cap or cross-layer compensation.

## SPD comparison input floor — LOCKED Q13.9

Use max(0,effective SPD); positive values stay unchanged, negative values
compare at0 and use equal-value tie priority. No stored-stat mutation, positive
cap or automatic action loss. Fractional precision and effect order remain open.

## Fractional comparator inputs — LOCKED Q13.10

Keep fractional effective SPD after max(0,SPD), without an added floor/rounding
at comparison.50.9 precedes50.2; actual equal inputs use fixed tie priority.
Upstream precision, inheritance rounding, effect math and UI remain separate.

## Inheritance parent-stat structure — LOCKED Q14

Each core stat uses only matching current permanent parent totals. No pooling
or cross-stat redistribution. F_s, parent combination/weights, normalization,
coefficients, diminishing-gain math and rounding remain open. Reinforcement
floor/no-hard-cap contracts remain; no minimum positive gain is inferred.

## Inheritance parent mean — LOCKED Q14.1

Raw matching-stat input=(Main permanent total+Donor permanent total)/2 for all
six stats. Preserve exact mean; no rounding added here. Example100/200→150 is
an input, not the child's bonus. Normalization, diminishing function, coefficients
and final rounding/floor order remain open. Reinforcement floor still applies
to Main; raw symmetry does not impose final operation symmetry.

## Inheritance normalization references — LOCKED Q14.2

Normalized input=parent_input[s]/R[s], with positive fixed per-stat R shared
across Species/Star/role. The six R values, output-unit conversion, diminishing
function, coefficients and rounding remain open. No child-base normalization,
HP/10 budget reuse or cross-stat pooling is approved. R is not a bonus cap.

## Inheritance output units — LOCKED Q14.3

Candidate bonus=R[s]×f_s(parent_input[s]/R[s]); same R as normalization, not
child Species base. Function/coefficients/R values and rounding/floor order
remain open. Accepted Reinforcement floor remains a lower bound, not another
additive copy of Main inheritance. This is not an output cap or minimum gain.

## Inheritance square-root family — LOCKED Q14.4

f_s(x)=k_s×sqrt(x), common shape for all six core stats, with positive k_s
values/grouping still open. Candidate=k_s×sqrt(R[s]×parent_input[s]).
R values, rounding/floor order and training/operation parameters remain open.
Unbounded response in input does not guarantee unbounded repeated-fusion bonus
under bounded grown stats; conditional natural-bound proof is in verification.
Owner long-run plateau requirement is pending Q14.5.
