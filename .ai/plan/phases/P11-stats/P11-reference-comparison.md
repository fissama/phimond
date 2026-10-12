# Current source comparison

Fresh APK/video/internet check: [fusion audit](P11-fusion-source-audit-20261012.md).
All P11 numeric tables/catalog/credit formulas are Phimond authored. Historical
recommendations below do not override [final spec](P11-final-spec.md).

# P11 — Original-game comparison

Reviewed 2026-10-12. Keep **observed source**, **owner-approved Phimond design**,
**inference/proposal**, and **unknown** separate. Older Java video, Android8.4
and revived iOS versions are related sources, not one proven identical ruleset.
No live original-server test or exact server formula recovery occurred here.

## Evidence and confidence

| Source | Inspected evidence | What it establishes / limitations |
|---|---|---|
| Local APK8.4 | `/Users/phileanh/Downloads/Spirit Beast World 8.4 (1).xapk`, SHA256 `b8e02a75e49d5d02703a0b05ec52b450cdfaf69d544f04df2f4a2a465199a18e`; primary APK `com.HCGame.SpiritBeastWorld.apk`; raw IL2CPP metadata version31 | Hash matches P10 extraction; names `TCSucManh`, `TCChiuDung`, `TCNhanhNhen`, `TCTriTue`, `TCTinhThan`, `TCPhongNgu`, `CTSucManh`, `KTLuc`, `CurrentMP`, `HonLoan` present. Identifiers corroborate distinct growth/stat/resource concepts, not their calculations |
| P10 extracted catalog | `../P10-pet-model/evidence/apk84-roster-extraction.json`, DataPoke `sharedassets0.assets:739`, 152 rows, 24,412 bytes and decoded field_schema | `PokeModelData` has identity/portrait/parent/Race/Star/description fields, no numeric base/growth table in this recovered schema. Does not prove no numeric data exists elsewhere in APK/server. 55 descriptions are blank |
| P10 extracted items | `../P10-pet-model/evidence/apk84-selected-items.json`, `sharedassets0.assets:738` | Full refresh and individual Strength/Spirit refresh descriptions support item capability categories; no probability, Egg eligibility, grade band or core-stat mapping recovered |
| Supplied video | [Pokezoo — Huyền thoại một thời](https://www.youtube.com/watch?v=FXJtLBPoGgo), linked by existing audit; local `tools/.cache/reference/video/overview.jpg` viewed in this review | Contact sheet confirms pet-tab visual family. Detailed 01:50–02:12 observations, including growth table at02:00–02:02, are inherited from `docs/research/VIDEO_UI_AUDIT_2026-09-23.md`, not freshly transcribed numeric frames. No grade RNG or formula inferred |
| Developer iOS listing | [Spirit Beast World](https://apps.apple.com/vn/app/spirit-beast-world/id6446976981), read2026-10-12 | Developer describes Strength/Agility/Endurance/Intelligence/Spirit/Defense/Crit, Spirit affecting MP, eight Races and fusion fromLv20. This supports resource/attribute distinction and progression concepts; it is version-specific prose, not Android8.4 numeric evidence |
| Historical first-person guide | [2010-08-05 breeding guide](https://m.ali213.net/gonglue/100805/10818.html), read2026-10-12, player-authored account | Describes appraisal near a1000 reference, role-oriented parent selection, Speed-heavy builds, growth allocations and repeated low-Star breeding. Useful direct testimony, not developer-confirmed formulas; its level/gender/skill rules cannot override approved P10 |

## Comparison outcome

| Topic | Source evidence | Current Phimond contract |
|---|---|---|
| Growth individuality | APK has per-attribute aptitude fields; historical player guide describes appraisal | Six core-stat rolls; fixed grade multiplier (Q7.6=A), weighted odds. Fixed multipliers/odds Q7.10–Q7.11 are owner-approved Phimond tuning, not recovered values |
| MP | APK Spirit aptitude/CurrentMP identifiers; developer links Spirit to MP | MP separate from six core stats. No implicit Spirit→Status Resistance mapping; MP baseline/growth still open |
| Resistance | APK metadata includes separate harmful-status identifiers; earlier audit/guide suggests multiple resistance concepts | One shared Status Resistance, application chance only: intentional P10 design, not asserted original equivalence |
| Lv1/growth | Catalog descriptions mention Species strengths, but recovered schema has no numeric stat rows | Species-fixed Lv1, deterministic levels, no per-level RNG: owner-approved contract; exact curve unverified |
| Reroll | APK prose supports all/individual aptitude refresh | Egg-only Full/Single reroll and six Perfect reachability are owner-approved; Q7.11 Perfect1% is Phimond tuning; no original probabilities/pity/keep-best recovered |
| Star/Special | Catalog proves five Stars and TT4S/TT5S classes/parent identities | Moderate increasing Star bands and Special half-step are design choices, not recovered premium percentages |
| Normal parity/roles | Source descriptions distinguish attack/magic/defense identities; historical guide has differing totals | Same-Star approximate normalized budget + role blend: approved design philosophy, not source arithmetic parity |
| Inheritance/+99 | Metadata/prose/guide support inherited attributes and repeated breeding | Current-total inputs, no hard cap, diminishing gains and per-stat reinforcement floor are P10 design. Exact source math not verified |

## Role discussion evidence — Q10.4a–f / Q10.5

APK catalog descriptions (`../P10-pet-model/evidence/apk84-roster-extraction.json`)
provide these qualitative examples, freshly reread2026-10-12:

- `TomHumRangCua`: physical attack growth with ally curse cleansing/HP help.
- `QuaiVatRuongBau`: physical attack/defense growth with healing.
- `HaiLongBaDau`: strong Intelligence growth, weak defense and varied control.

These support considering mixed functional identities. They do not establish
Primary/Secondary assignments, Support bulk percentages, speed requirements,
skill eligibility or exact effect formulas. Q10.4a's broad Support definition
and Q10.4b's control/debuff Disruptor definition are owner-approved Phimond
design; Q10.4c excludes pure poison/burn damage from establishing Disruptor
while keeping harmful-status application within SR scope. Q10.4 numeric
Hybrid thresholds are subsequently approved in Q10.4f as Phimond design. Q10.4d rejects the universal Support bulk
and Disruptor SPD minima while retaining template and existing authoring checks
plus functional rationale checked with P13. No recovered source taxonomy or
numeric role threshold is asserted. Q10.4e defines Hybrid as dual physical/
magic damage in Phimond; the source descriptions above do not establish that
role taxonomy or the owner-approved Q10.4f thresholds (20%/20%/combined50%).
Q10.5 functional Primary/Secondary assignment without skill quotas is also a
Phimond authoring decision. P11 documents rationale and P13 checks concrete
Native Skill Pool content; source descriptions alone do not validate the final
assignment or a current Pet loadout.

## Research still required

A numeric frame cannot prove a growth curve without controlled samples for the
same Species/level/profile/inheritance. To recover Q7 grade behavior from the
original, obtain identifiable same-grade/appraisal examples and level deltas,
with version and equipment/bonus states. To infer a distribution, use enough
natural/reroll samples and label uncertainty; asset names and anecdotes are
insufficient. Source-verification for Special operations remains P10 O01/O02.

Current evidence does not choose multiplier values, probability weights,
normalization, role blend or inheritance coefficients for the owner.

## Lv1/growth modifier coupling — Q10.6

Owner approves independently authored modifier percentages for each stat in
Lv1 and growth, preserving all checks in both layers. This is a Phimond design
choice; the inspected original-game descriptions, APK schema and video contact
sheet do not establish numeric modifier coupling or a common percentage rule.

## Star/Special comparison states — Q11

Owner approves equal-role/blend, all-B reference plus all-Perfect check with
zero inheritance/equipment/buffs at Lv1/Lv60/own base/+99 caps; main/SPD/SR
checked separately. This is a Phimond review protocol, not a recovered source
stat table or proof of original Star/Special scaling. Numeric targets remain open.

## Special4 premium direction — Q11.1a

Owner selects a same-state intrinsic main-budget premium direction around8–10%
above Normal4, revisiting unapproved Normal4→5 spacing while retaining half-step
positioning. Neither this range nor the proposed revised Normal factors is
source-recovered. Exact Special interpolation, layer allocation, tolerance,
SPD/SR and P13 skill distinctions remain open.

## Normal Star factors — Q11.1b

Owner approves Normal main-budget target factors1/1.10/1.22/1.36/1.60 for
Lv1/growth with separate1★ anchors, deliberately widening the last step.
These are Phimond tuning rather than recovered source values. Special4
midpoint1.48 is subsequently approved per layer in Q11.2; Special5 and
Special tolerance remain open.

## Special4 midpoint — Q11.2

Owner approves arithmetic midpoint of Normal4/Normal5 main-budget targets,
separately for Lv1/growth:1.48× each matching1★ anchor. Target premium over
Normal4≈8.82353% is Phimond tuning, not source recovery. Special4 keeps4★
caps90/189. Special5/tolerance/SPD-SR and concrete skills remain open.

## Special5 additive half-step — Q11.3

Owner approves Normal5 plus half the Normal4→5 gap separately for main-budget
Lv1/growth targets:1.72× each matching1★ anchor, premium7.5% over Normal5.
Caps remain100/199. This is Phimond design, not source recovery. Special
tolerance and SPD/SR remain open; no6★ catalog tier is introduced.

## Special main-budget tolerance — Q11.4

Owner approves±2% independently around Special4/Special5 Lv1/growth targets;
Normal remains±3%. These are Phimond authoring tolerances, not recovered
original-game variance. Absolute anchors, concrete assignments and auxiliary
ranges remain open; no Pet inheritance/grade clamp is implied.

## Absolute Lv1 scale — Q11.5

Owner approves Normal1★ Lv1 main-budget target100 and derived Normal
100/110/122/136/160, Special148/172. This is Phimond tuning; inspected source
evidence does not establish this scale. Growth anchor, auxiliary stats/MP,
actual Species assignments and combat formulas remain open.

## Absolute growth scale — Q11.6

Owner approves Normal1★ main growth-baseline target2.000 normalized points
per level at grade B, yielding Normal2.000/2.200/2.440/2.720/3.200 and
Special2.960/3.440. This is Phimond tuning, not recovered source growth.
Actual Species baselines, auxiliary/resource stats and combat formulas remain
open. Do not interpret this aggregate authoring metric as each stat's gain.

## Role template share coupling — Q11.7

Owner approves shared main-budget percentage allocation across Lv1/growth per
role, before independently selected Species modifiers. Concrete shares remain
open. This is Phimond authoring policy; source prose does not establish either
this coupling or the proposed Q11.8 neutral Support/Disruptor allocations.

## Six-role main shares — Q11.8

Owner approves Physical25/45/10/20, Magic25/10/45/20, Tank40/15/10/35,
Hybrid25/30/30/15, Support/Disruptor25/25/25/25, ordered HP/10–ATK–MAG–DEF.
These are Phimond allocations, not APK/video numeric recovery. Neutral
Support/Disruptor vectors do not recover original role taxonomy or assume
MAG-based effect scaling; P13 function and auxiliary targets remain dependencies.

## Species base numerical grid — Q11.9

Owner approves integer final six-stat Species base values; growth baselines
retain≤3 decimals. This is Phimond authoring policy, not a proven original-game
precision rule. Intermediate templates remain exact and final content must
satisfy all bounds/budgets/signatures; inheritance/output rounding stays open.

## Status Resistance unit — Q12

Owner approves rating points, with numerical response still open. Existing
APK identifiers, video observations and source prose do not establish this
shared SR rating unit or conversion formula. Do not equate original Spirit
with Phimond SR or interpret SR100 as100% resistance.

## Status Resistance diminishing benefit — Q12.1

Owner approves decreasing marginal resistance benefit at the same initial
status chance. This is Phimond tuning; existing source evidence does not prove
this shape or a specific numerical equation. Chance integration remains open.

## Proportional status-chance reduction — Q12.2

Owner approves chance_before_sr × (1 − resistance_effect). This is Phimond
design; source evidence does not establish this equation or a rating-to-effect
coefficient. Skill chance input/ordering and immunity remain unresolved.

## SR benefit limit — Q12.3

Owner approves an asymptotic resistance-effect ceiling below100%, retaining a
fraction of positive input chance. This is Phimond design, not an original-game
immunity rule recovered from APK/video/internet. The ceiling value is open.

## SR80% benefit ceiling — Q12.4

Owner approves an80% asymptotic resistance-effect ceiling. The remaining
limiting fraction is20% of input chance, not an absolute20% status chance.
This constant is Phimond design; existing source evidence does not prove it.
Exact curve and rating scale remain unresolved.

## Rational SR response — Q12.5

Owner approves0.80×SR/(SR+H), for nonnegative SR and positive H. This is
Phimond design, not source-recovered math. H value/context policy remains open;
worked ratios prove arithmetic properties, not original parity or combat balance.

## Shared constant H — Q12.6

Owner approves a shared H independent of level/Star/role. This is Phimond
policy; source evidence does not establish this scaling choice. H value and
actual ratings remain open. Equal rescaling of H and SR preserves effects,
so H alone does not certify balance.

## Shared H100 scale — Q12.7

Owner approves H100; SR100 gives40% resistance effect. This is a Phimond
unit-scale choice, not a recovered original coefficient or a Species target.
Actual base/growth/Star/role SR strengths remain unapproved.

## Neutral SR50 reference — Q12.8

Owner approves a neutral Normal1★ Lv60 B template anchor SR50 without
inheritance/equipment/buffs. This is Phimond tuning, not an original-game
stat recovered from APK/video/internet, and does not assign Species or roles.
Base/growth allocation and role/Star target values remain open.

## Neutral SR base20/growth0.510 — Q12.9

Owner approves the Normal1 neutral SR split20/0.510. Lv60 B SR50 and Lv159 B
SR100 are computed from approved cumulative floor, not observed source values.
Role/Species assignments, Normal Star and Special SR scaling remain open.

## Normal SR Star scaling — Q12.10

Owner approves1/1.03/1.06/1.09/1.12 for SR base/growth targets relative to
Normal1★. These are Phimond authoring factors, not recovered source stats.
Exact intermediate targets do not override final numerical grids; Special
SR targets and role/range/content decisions remain separate.

## Special SR half-step — Q12.11

Owner approves Special4/5 SR factors1.105/1.135, independently of main-budget
premium. This is Phimond target design, not source-recovered Special stats.
It does not certify final SR ordering or activate source-gated operations.

## SR role factors — Q12.12

Owner approves Tank/Support1.10 and all other roles1.00 on both SR target
layers before75/25 blend. This is Phimond authoring policy, not recovered
role classification or numerical source bonuses. No Species/skill is assigned.

## SR content range±5% — Q12.13

Owner approves inclusive±5% around exact blended SR targets independently for
base/growth, Normal/Special. This is Phimond content tolerance, not a source
rule or an inherited/effective-stat cap. It matches SR Species modifier bounds.

## Effective-SR input floor — Q12.14

Owner approves max(0,effective SR) at the response stage. Negative effective
SR gives no resistance benefit or vulnerability amplification. This is Phimond
design; source evidence does not establish the corresponding original behavior.

## Single application-stage roll — Q12.15

Owner approves one final-chance roll per eligible single-status attempt. This
is Phimond design, not a recovered original RNG sequence. Hit/eligibility/
multi-status/UI behavior remains a separate interface. SPD turn-order-only
scope comes from P10-D42; source evidence does not establish its exact sort.

## Deterministic SPD comparison — Q13

Owner approves higher effective SPD going first when comparing by SPD, without
RNG for unequal values. This is Phimond design within P10-D42, not an exact sort
recovered from source. Equal-value tie-breaking and scheduler timing remain open.

## Fixed random equal-SPD priority — Q13.1

Owner approves random tie priority drawn once at battle start and retained
within the battle, used only for equal effective SPD. This is Phimond policy;
source evidence does not recover the original tie-breaking sequence.

## SPD changes and established order — Q13.2

Owner approves retaining an established action list on SPD changes, applying
new SPD at the next ordering point. This is Phimond policy, not source-recovered
timing; list formation and eligibility remain P02/P13 dependencies.

## Neutral SPD100 reference — Q13.3

Owner approves a Normal1★ Lv60 B neutral template SPD100, before modifiers
and without inheritance/gear/buffs. This is Phimond authoring scale, not
original-game numeric recovery. It does not introduce action-frequency scaling.

## Neutral SPD40/1.020 — Q13.4

Owner approves Normal1 neutral SPD base40/growth1.020. Computed B values at
Lv1/60/159 are40/100/201; these are Phimond design arithmetic, not numeric
source observations. Star/role/Special targets and combat integration remain open.

## Normal SPD Star factors — Q13.5

Owner approves1/1.02/1.04/1.06/1.08 on SPD base/growth targets relative to1★.
These are Phimond authoring factors, not numeric APK/video recovery. Special
SPD targets remain separate from the approved main/SR factors.

## Special SPD half-step — Q13.6

Owner approves Special4/5 SPD factors1.07/1.09, separate from main/SR factors.
This is Phimond target tuning, not source numeric recovery. It does not prove
final SPD order or activate source-gated Special operations.

## SPD role factors — Q13.7

Owner approves Physical/Magic/Hybrid1.00, Tank0.90, Support1.05, Disruptor1.10
on both target layers before75/25 blend. These are Phimond authoring factors,
not recovered original role assignments or universal role speed thresholds.

## SPD content range±5% — Q13.8

Owner approves inclusive±5% around exact blended SPD target for each Species
base/growth layer, Normal/Special. This is Phimond content tolerance, not source
recovery, owned-stat capping or guaranteed speed order.

## SPD comparator floor0 — Q13.9

Owner approves max(0,effective SPD) for comparison, with negatives tying at0
without automatic action loss. This is Phimond policy, not recovered original
negative-stat behavior. Effective-SPD derivation/precision remains open.

## Fractional SPD comparison — Q13.10

Owner approves retaining fractional comparator inputs without another rounding
step, so50.9 precedes50.2. This is Phimond comparison policy, not a recovered
original-game numerical representation. Upstream effect/rounding rules stay open.

## Independent matching-stat inheritance — Q14

Owner approves each inherited stat using only matching parent permanent totals.
This is Phimond structure, not an exact numeric formula recovered from source.
Parent combination/normalization and diminishing-return coefficients remain open.

## Equal arithmetic parent-input mean — Q14.1

Owner approves50/50 matching-stat arithmetic mean as raw inheritance input.
This is Phimond design, not recovered original parent coefficients. It does
not by itself set the child's bonus or erase operation-specific asymmetry.

## Fixed per-stat inheritance references — Q14.2

Owner approves normalized input=parent mean/R[s], with fixed positive per-stat
references shared across Species/Star/role. This is Phimond design, not recovered
source normalization. Reference values and output-unit conversion remain open.

## Same-reference inheritance output units — Q14.3

Owner approves converting normalized function output to candidate bonus with
the same fixed R[s], not child Species base. This is Phimond unit policy, not
recovered source coefficients. Function/R values/rounding remain open.

## Square-root inheritance — Q14.4

Owner approves square-root response family; this is Phimond design, not a
source formula. Conditional repeated-fusion bounds are mathematical consequences
of the proposed structure, not observations of original-game long-run behavior.
