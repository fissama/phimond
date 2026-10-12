# Historical interview checkpoints — superseded

Current authority: [P11-final-spec.md](P11-final-spec.md). OPEN/LOCKED/status
statements below apply only to the recorded checkpoint. Numerical examples
are not the final catalog unless independently reproduced in current evidence.

# P11 — Verification criteria and evidence

Status: **design synchronization only**, 2026-10-12.
No numerical balance tests, simulation harness, runtime stat engine or
migration were executed. The following cases are required criteria, not PASS
claims. Approved coefficients/tables are needed before numerical evaluation.

## Required design / future numerical cases

| Case | Given / action | Required result |
|---|---|---|
| V01 Lv1 invariant | Same Species, different stored growth profiles | Same grown Lv1 base; inheritance may differ separately |
| V02 deterministic growth | Same Species/profile/level, repeated/direct/incremental calculation | Same cumulative-floor result; retain fractions; no level RNG |
| V03 multiplicative identity | Low/high Species baseline with same multiplier | Relative deviation preserves Species baseline; no universal flat bonus |
| V04 Full reroll | Egg with profile + inheritance + parent snapshots | Six growth rolls redrawn; inheritance/identity/snapshots unchanged |
| V05 Single reroll | Egg, selected stat | Only selected roll redrawn; may improve/equal/worsen; no hidden keep-best |
| V06 six Perfect | Six positive-probability top bands, repeated legal rerolls | All six Perfect reachable; no shared budget/forced loss |
| V07 fixed grades | Same grade/stat family across individuals; Perfect | Same approved multiplier; no within-grade RNG; SPD/SR spread separately checked |
| V08 display | Grown 186, inherited12, equipment25 | Attributes186 +12, permanent198, overview223, parent input198 |
| V09 parent totals | Same bonus but different grown totals / level | Function uses both current permanent totals; no equipment/temp modifiers |
| V10 floor | Main bonus12, weak donor; repeat at +00/+99 | Reinforcement bonus ≥12 for that stat, not ≥Plus; no automatic +1 |
| V11 slots/Star-up | Swap main/donor; Star-up resets Plus | Approved weights/main floor observed; no automatic Star-up floor |
| V12 long-run | 50 generations and stronger analytic/extended checks, equal parents, weak/strong donors, retraining | Quantify marginal gains/pacing; no hard cap or finite-ceiling claim from 50 samples |
| V13 caps | Stars1–5 and Plus0/99 | Caps60/70/80/90/100 +Plus; Plus has no direct stat term |
| V14 Star/class comparisons | Approved common level/quality/bonus conditions plus own caps | Compare both base/growth layers; Special hierarchy evaluated in defined state |
| V15 role identity | Primary/secondary blend then maximal modifier | Approved signature constraints/tolerance survive, no budget inflation |
| V16 MP re-hatch | Pet with old current/maxMP, return to Egg and hatch | CurrentMP = recalculated Lv1 maxMP; no old value/percentage |
| V17 HP/status | First/re-hatch and restoration | Expected currentHP/status/cooldown follows future approved O03 policy |
| V18 shared SR | Control/poison/burn/stat reduction plus direct damage/duration | Only application chance changes; approved bounds/rounding/order |
| V19 roster | Frozen152 canonical IDs | All required assignments approved; no silent identity edits/source guesses |
| V20 persistence boundary | Hatch/reroll/restore at supported later lifecycle | Stored profiles and immutable parent snapshots preserved; no migration without explicit plan |

Training above Lv20, PvP turn order, reroll effort/reward and status immunity
must be reviewed with their downstream owners. Budget equality alone cannot
certify combat viability or original-game fidelity.

## Evidence inspected in this review

- Owner's pasted P11 state imported without assigning missing numbers.
- P10 D01/D07/D08/D11–D16/D20–D22 and open-register ownership cross-checked.
- Local APK8.4 XAPK hash matches P10 extraction;
  IL2CPP metadata version31 and stat/growth/resource identifiers corroborated.
- Existing extracted 152-row schema inspected; 55 blank descriptions counted.
- Local video overview contact sheet inspected. Detailed 01:50–02:12 pet-table
  observations inherited from the 2026-09-23 audit, not a fresh exact-frame scrub.
- Internet developer listing and historical first-person guide reread. See
  [reference comparison](P11-reference-comparison.md) for claims and limits.

## Executed document checks —2026-10-12

- Exact-rational arithmetic: probability sum100%, B-or-better85%, multiplier
  means1.0108/1.00324, strictly ascending tables: **PASS**.
- Local Markdown links: **24 checked,0 missing, PASS**.
- `git diff --check -- .ai/ACTIVE.md .ai/plan/phases/P11-stats`: **PASS**.
- `git fetch origin`: successful; `HEAD...origin/main` ahead/behind **0/0**.
- Workspace remains dirty from pre-existing P10/client work plus this P11 design
  update. No commit/push, source integration, server restart or phase-delivery
  claim in this ongoing discussion. The AGENTS.md delivery/manual-validation
  ritual remains due before delivering a completed task/phase.

These checks validate document/table arithmetic, not numerical balance,
Species viability or original-game stat formulas. No simulation harness built.
Runtime checks would validate legacy gameplay only, not these P11 rules.

## Q8.1 arithmetic check —2026-10-12

Exact-rational worked examples PASS:2.40×1.03×19 floors to46; atLv21
floors to49; sequential differences sum to the same direct result.
Integer-boundary example2.5×1.024×25=64 floors to64 exactly.
These are formula arithmetic checks, not a simulation harness or Species
balance proof. Local links rechecked:24 valid.

## Q8.2 exact arithmetic check —2026-10-12

Milli-product/division agrees with exact rational cumulative floor on100
worked combinations (four illustrative baselines, five approved multipliers,
levels1/20/60/100/199). Baseline2.405,A1.03,Lv20 gives numerator47065850
and earned growth47. PASS;24 local links valid. This is arithmetic verification,
not a simulation harness or assignment of these baselines to Species.

## Q9.1 budget arithmetic check —2026-10-12

Equal-budget illustrative allocations200/50/10/20 and400/10/10/40 both
normalize to100. A fractional growth example2.405/0.500/0.100/0.200
normalizes to1.0405 exactly, without flooring the HP contribution. PASS.
These are arithmetic examples, not Species/role assignments or combat proof.
Local Markdown links rechecked:24 valid.

## Q9.2 tolerance arithmetic check —2026-10-12

Inclusive bounds verified using exact fractions: target100 accepts97/103,
rejects96.9/103.1; illustrative fractional target7.5 accepts7.275/7.725.
Upper/lower ratio103/97 has relative difference6/97,about6.19%. PASS.
No target is assigned to a Species/Star by these examples.24 local links valid.

## Q9.3 document contract check —2026-10-12

Confirmed separate SPD/SR targets/ranges in decisions, formulas and stat tables;
no shared auxiliary pool or implicit conversion. P10-D39 initial role vocabulary
reused with the explicit Q4/Q5 stat-authoring extension; no skill restrictions
or grants introduced.24 local links valid. Q10 blend remains unapproved.
No numerical target assignment or runtime test claimed.

## Q10 blend arithmetic check —2026-10-12

Illustrative main-budget vectors[40,10,10,40] and[20,10,50,20] blend75/25
to[35,10,20,35], sum100. Weights sum1; no extra/unused budget. PASS.
The example0.001/0.002 blends to0.00125, demonstrating that exact intermediate
precision can exceed the three-decimal final baseline constraint; final
assignment quantization remains open. No role template assigned by these
examples.24 local links valid.

## Q10.1 modifier-method arithmetic check —2026-10-12

MAG10→11 is10% relative change; budget share10%→15% is50% relative change.
Illustrative main allocation200/50/10/20 has budget100; changing ATK50→55
alone gives105, outside the approved±3% main tolerance. This demonstrates why
per-stat and budget constraints must both be checked; no numeric modifier cap
is approved by the example. Arithmetic PASS;24 local links valid.

## Q10.2 modifier-bound arithmetic check —2026-10-12

Illustrative templateATK50 accepts45/55 and rejects44.9; templateSPD20 accepts
19/21 and rejects21.001. Inclusive limits PASS. Precision-conflict example:
blended0.00125 with±10% permits[0.001125,0.001375], containing no three-decimal
value; this must be reported/retuned as content, not silently clipped or granted
a precision/bound exception. These are worked examples, not template/Species
assignments.24 local links valid. Primary-role signature thresholds remain
pending Q10.3 and are not tested/claimed as approved here.

## Q10.3 signature arithmetic check —2026-10-12

Exact boundary checks PASS: physicalATK35/MAG28 at budget100 satisfies both
35% share and1.25 ratio;ATK34.9 fails the share andMAG28.001 fails the ratio.
Symmetric magic cases verified. TankHP300/DEF30 at budget100 satisfies60%;
HP299/DEF30 at the same budget reaches59.9% and fails. Examples are not actual
Species/template assignments and do not verify combat balance.24 local links
valid. Hybrid/Support/Disruptor guards were pending at that checkpoint;
Q10.4a–f subsequently resolve them (see decisions and checks below).

## Q10.4f Hybrid signature arithmetic check —2026-10-12

Eight exact-rational worked cases at actual B100 PASS: ATK/MAG25/25,20/30
and30/20 accepted;19.999/30.001 and30.001/19.999 rejected by single-stat minima;
20/29.999 rejected by combined49.999%;40/10 and20/20 rejected. Every example
uses HP200 with DEF chosen to keep actual B100. Checks cover inclusive minima
and just-below boundaries; they are not Species/template assignments or combat
balance tests. Q10.4d's absence of universal Support bulk/Disruptor SPD minima
does not waive other template, budget, modifier or SPD/SR range constraints.

## Q11.1b proposed-factor arithmetic —2026-10-12

Exact-rational illustrative calculation: Normal4=1.36, proposed Normal5=1.60;
midpoint=1.48. Normal4→5 target increase17.64706%; midpoint premium over
Normal4=8.82353%; Normal5 premium over midpoint=8.10811%. With hypothetical
Special±3%, target-budget intervals remain separated:1.4008<1.4356 and
1.5244<1.552. These are proposal arithmetic checks, not approved factors,
Special tolerance, Species assignments or combat evidence. Actual floor and
own-cap effects require approved absolute content; no harness was added.

## Special additive-premium clarification —2026-10-12

Twelve exact-rational illustrative cases (base/growth anchors100/2 or70/3,
Lv1/60/90, multiplier1 or1.10) verify that applying r=1.48/1.36 to both additive
components scales their unrounded sum by r, not r². Arithmetic PASS; this is
not approval of Special midpoint/layer allocation, target anchors or a runtime
simulation. Actual per-stat floors and Species budgets still require checks.

## Q11.2 approved-midpoint arithmetic —2026-10-12

Exact midpoint(1.36+1.60)/2=1.48 verified. For illustrative anchors100,2,7.5,
midpoint of separately scaled Normal targets equals1.48×matching anchor.
Arithmetic PASS; no absolute anchor/Species values approved by these examples.
Special tolerance and actual rounded/Q11 own-cap comparisons remain open.

## Q11.3 / Q11.4 arithmetic —2026-10-12

Approved Special5 factor:1.60+(1.60−1.36)/2=1.72, premium7.5%; equal0.12
steps across Normal4/Special4/Normal5/Special5 verified. Proposed Special±2%
with approved Normal±3% yields main-budget intervals1.3192–1.4008,
1.4504–1.5096,1.552–1.648,1.6856–1.7544. All three strict interval-separation
checks PASS using exact rationals. Special tolerance is NOT approved by this
check;±3% would also separate target bands. Actual floor/content/combat
validation remains open. These checks are worked arithmetic, not a harness.

## Q11.4 approved-boundary arithmetic —2026-10-12

For illustrative targets1.48,1.72,100,7.5, exact98%/102% boundaries accepted;
values0.000001 below/above rejected. Sixteen exact-rational boundary checks
PASS. Approved main authoring intervals remain separated as previously shown.
Examples approve no actual target anchors/Species content; final precision/
per-stat floors and combat validity still require later checks.

## Q11.5 derived-target arithmetic —2026-10-12

Approved100-point Lv1 anchor times approved factors gives exact targets
100/110/122/136/148/160/172. Seven factor calculations PASS; illustrative
HP200/ATK45/MAG10/DEF25 budget100 also verified. No role/Species assignment
or combat proof follows; growth anchor remains open.

## Q11.6 approved-growth target arithmetic —2026-10-12

Seven exact factor calculations PASS:2.000×approved factors yields
2.000/2.200/2.440/2.720/2.960/3.200/3.440. Tolerance checks apply to authored
HP_growth/10+ATK_growth+MAG_growth+DEF_growth, not final grown Pet totals.
Previously worked actual-floor example atLv60 gives216.6 versus unrounded218;
it remains illustrative, not approved Species/role content. Actual assignments
and Q11 per-stat rounded comparisons remain open.

## Q11.8 proposed-share arithmetic —2026-10-12

Six proposed single-role vectors and30 distinct75/25 blends: all36 exact
checks PASS for sum100 and applicable Primary signatures before modifiers.
Proposed rows are not owner-approved. A worked growth counterexample within
per-stat±10% and main budget2 violates Physical35% share, demonstrating why
final signatures remain mandatory after modifiers; it is not an assigned
Species or a failing runtime test. Quantization/content/combat checks remain open.

## Q11.8 approval checkpoint —2026-10-12

Owner approves the exact six share vectors already checked in36 single/blended
cases above. Arithmetic evidence is unchanged; no new runtime/Species test
is claimed. Final modifier signature checks remain required, including the
previously demonstrated invalid-modifier example. Final Lv1 numerical grid
and actual152 assignments remain open.

## Q11.9 integer-base example —2026-10-12

Exact Normal3 Physical/Magic75/25 template305/44.225/22.875/24.4 versus integer
candidate305/44/23/24 verified: all fields integer, all four within±10%,
main121.5 within122±3%, ATK≥35%×121.5 and ATK≥1.25×MAG. Arithmetic PASS; this
is an illustrative valid candidate, not an assigned Species or automatic
rounding algorithm. Other content and auxiliary targets remain unapproved.

## Q12.5 rational SR response arithmetic

Using x=SR/H≥0, effect=(4/5)×x/(x+1). Exact fractions verify x=0/1/2/4
yield0/2⁄5/8⁄15/16⁄25. Its derivative is(4/5)/(x+1)²>0 and second
derivative−(8/5)/(x+1)³<0; effect approaches4/5 while input chance retains
a limiting fraction1/5. These properties hold for H>0; H policy/value remain
unapproved. No runtime or combat balance validation is claimed.

## Q12.9 neutral SR split arithmetic

Exact milli baseline510, B1000: Lv60 earned=floor(510×1000×59/1000000)=30;
Lv159 earned=floor(510×1000×158/1000000)=80. Base20 yields50/100 respectively.
The Q12.8 SR50 effect is4/15, and input chance1/2 becomes11/30. At SR100 the
effect is2/5. This is design arithmetic; role/Star targets and combat balance
remain unresolved, with no runtime tests claimed.

## Q12.12 SR grid feasibility under existing modifier bounds

Exact rational checks cover7 Normal/Special factors ×(6 single-role templates
+30 distinct75/25 role blends)=252 combinations. Each exact SR base target has
an integer candidate within its existing±5% modifier interval; each SR growth
target has a milli-grid candidate within that interval. This verifies SR-only
grid feasibility, not full Species assignments, combat parity, or approval of
the separate range width still pending Q12.13. No runtime harness was added.

## Q13.4 SPD anchor arithmetic

Exact milli baseline1020 and B1000 yield earned growth60 atLv60
(floor(1020×1000×59/1000000)) and161 atLv159
(floor(1020×1000×158/1000000)); base40 gives100/201.
No role/Star target, runtime implementation or combat certification follows.

## Q13.7 SPD grid feasibility

Exact rational checks cover7 approved Normal/Special factors ×(6 single-role
templates+30 distinct75/25 role blends)=252 combinations. All have integer
base and milli growth candidates within existing±5% modifier bounds. A
proposed±3% interval also has representable candidates for each; this is not
approval of that range. No actual Species assignment or full combat check is
claimed. SPD range choice remains pending Q13.8.

## Q14.4 conditional natural-bound proof — owner intent pending Q14.5

Before rounding, fix a stat with R>0,k>0 and grown parent totals≤G. Assume
existing parent inheritance bonuses≤L. Then mean permanent input≤G+L and
candidate≤k×sqrt(R×(G+L)). Let A=k²R and
L*=(A+sqrt(A²+4AG))/2. It satisfies L*²=A(G+L*), so any
L≥max(L*,initial bonus bound) is preserved by both the candidate and the
Reinforcement Main floor. This applies to arbitrary pairs within those bounds,
not just a single self-repeat sequence. It is a finite invariant bound under
these assumptions despite the absence of an explicit configured cap.

Illustrative numbers only, not approved coefficients/references: G100,R100,
k0.2 and initial bonus0 yield repeated equal-parent unrounded bonus
0→20→21.908902→22.082473→22.098188, with bound≈22.099751. Checked the
fixed-point equality numerically. Rounding/training/operation policies remain
open and may change actual behavior; no runtime simulation or global ceiling
certification is claimed. Resolve whether a natural plateau is desired before
selecting R/k. The shape approval itself is recorded without treating the
long-run gameplay consequence as already approved.
