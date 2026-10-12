# Final review disposition

The findings below are historical review checkpoints. Current resolution:
[final spec](P11-final-spec.md), [verification](P11-verification.md),
[inheritance audit](P11-inheritance-design-audit.md). R20 plateau is resolved by
explicit F02/F03 accumulated-credit amendments. Numeric/content/resource gaps
are closed in design; downstream runtime/source/economy gates remain explicit.

# P11 — Plan review and discussion checkpoint

Reviewed 2026-10-12, Codex. Scope: owner's pasted design state, P11 scaffold,
P10 contracts and original-game references. **Design in progress, not closed.**
Q7.6 subsequently approved **A: one fixed multiplier per grade/stat family**.

## Findings and disposition

| ID | Finding / implication | Disposition |
|---|---|---|
| R01 | README said NOT STARTED despite confirmed Q1–Q7.5 | Corrected status/index; imported exact owner baseline and recorded subsequent Q7.6 answer |
| R02 | Handoff instructed per-level RNG, universal Race growth and Race/Star HP factors | Corrected to P10 Species Lv1/baselines, Egg profile, deterministic levels; no double scaling |
| R03 | Handoff encouraged bonus-only depth formula and confused +99 with stat floor | Removed suggested formula; both permanent totals, no numeric generation-depth stat, actual main bonus floor |
| R04 | Handoff suggested closest legacy mapping and building harness now | Corrected: explicit later mapping/version/rollback gate; design-only scope, no harness |
| R05 | README table axis Race×Star×role implied Race power bonus | Corrected Star/class/role/species budgets; taxonomy grants no automatic stats |
| R06 | Handoff treated Star-up as outside stat math and suggested floor carry-over | P11 owns stat inheritance with P16 operation; reinforcement floor not auto-applied to Star-up |
| R07 | Prior overall quality/zero-sum ideas would prevent six Perfect and contradict reroll | Explicit rejected models preserved; each stat has its own roll |
| R08 | Perfect top-band wording vs fixed-per-grade A could imply hidden secondary roll | Q7.6=A recorded; top grade resolves to one fixed representative. Numeric band/threshold terminology still needs table approval; no within-grade RNG |
| R09 | Raw stat sum lacks common units; same budget does not imply equal combat power | Open normalization/reference-state contract; P13/P02/P15 verify skill/turn/status value later |
| R10 | Special hierarchy/low-Star ceiling could be read as universal despite uncapped inheritance | Q11 locks zero-inheritance, same-role/blend/profile comparisons at Lv1/Lv60/own caps. Numeric hierarchy still needs actual budgets; arbitrary player totals cannot obey universal ordering |
| R11 | Higher-Star base/growth premium plus higher cap can amplify Star gaps | Q11 locks common Lv60 and own base/+99 caps, all B with Perfect check. Target ratios/anchors now locked Q11.1b–Q11.6; actual role/Species tables and rounded comparisons still pending |
| R12 | Species modifiers/secondary blend could destroy primary role or inflate budget | Need signature bounds, blend ratio, modifier limits/renormalization;75/25 locked in Q10; modifier limits locked in Q10.2; template/signature constraints remain open |
| R13 | Diminishing inheritance, reinforcement floor and unlimited retraining cannot prove finite ceiling from50 generations | Require precise diminishing-gain definition and long-run reasoning; zero gain allowed, no hard cap/minimum+1 invented |
| R14 | Stat-training input wording not fully specified | Level-grown current totals included by D08/D14; coordinate distinct P15 permanent-training layer before formula approval |
| R15 | Original Spirit/MP and multiple status concepts differ from P10 core stats | Document adaptation; do not equate source Spirit with shared SR or infer MP loss |
| R16 | APK descriptions cannot fill all152 assignments;55 empty | Keep stat/role assignment unapproved and trace each design decision; no silent source-prose parsing |
| R17 | Split main/aux budgets do not yet provide a combined six-stat parity metric | Q9.2 checks only Normal main parity. Auxiliary definition/role bounds remain open; do not claim Q2 fully verified or all roles combat-equivalent from the main±3% check |
| R18 | P10-D39 says roles are metadata/content aid only, while accepted P11 Q4/Q5 drive stat templates | Explicit scoped extension by owner Q4/Q5, documented in Q9.3: reuse initial six-role vocabulary; no hard gameplay restriction or skill grant. 75/25 blend locked in Q10; template values remain open |
| R19 | Exact75/25 blends can exceed three-decimal final baseline precision; modifier intervals may contain no valid grid value | Keep intermediates exact. Example0.00125±10% cannot fit a three-decimal value. Final quantization/templates must be approved and preserve all budget/role/bound constraints; no silent clipping/relaxation |

## Current verdict

Accepted qualitative design is coherent with P10 after scaffold corrections.
Numerical budget, curve, inheritance, MP/HP/status contracts and152 Species
assignments remain unresolved; P11 is not ready for runtime implementation.

The fixed-per-grade choice makes equal Species/grade deterministic and removes
optimization inside Perfect. Tradeoff: fewer individual differences and sharper
grade boundaries, so fixed multiplier gaps matter. Seven existing candidate
grades give more progression steps; fewer grades simplify reading. Owner subsequently retained seven labels (Q7.7), HP/ATK/MAG/DEF endpoints
0.90/1.10 (Q7.8), SPD/SR0.97/1.03 (Q7.9). Q7.10 approved complete multipliers, Q7.11 odds with Perfect1%, Q7.12 shared
creation/reroll tables. All these are design tuning, not original recovered math.

## Next discussion

Q7.6 closed to A. Q10.4a–d lock Support/Disruptor functional guards without universal bulk/SPD
minima. Q10.4e locks Hybrid to dual physical/magic damage. Q10.4f locks its20%/20%/combined50% guard. Q10.5 functional role criteria locked without skill quotas. Q10.6 permits independent Lv1/growth Species modifier percentages, retaining
all per-layer checks. Pending owner choice:
**Q14.5 repeated-fusion plateau requirement**. Rating points, diminishing benefit,
proportional chance reduction and a sub100% asymptotic benefit ceiling are
locked; Q12.4 sets the effect ceiling80%. Q12.5 rational function locked; Q12.6 shared constant H locked; Q12.7 locks H100. Q12.8 neutral Normal1 Lv60 B SR50 locked; Q12.9 base20/growth0.510 locked; Q12.10 Normal SR Star factors locked; Q12.11 Special SR factors locked; Q12.12 SR role factors locked; Q12.13 SR ranges±5% inclusive locked; Q12.14 response-input floor0 locked; Q12.15 one application roll locked; actual content/effective-SR derivation and P13 interfaces remain open. Q11.9 integer Species base values locked;
growth baselines≤3 decimals. Q11.8 six-role main shares locked. Q11.7 shared main shares locked; Species
modifiers remain independent. Q11 comparison states locked;
Q11.1a selects Special4 premium direction8–10%; Q11.1b approves Normal
factors1/1.10/1.22/1.36/1.60; Q11.2 approves Special4 midpoint1.48 separately
for Lv1/growth; Q11.3 approves Special5 factor1.72 per layer. Absolute1★
Q11.4 approves Special main tolerance±2%, Q11.5 Lv1 anchor100 and Q11.6
growth anchor2.000, with derived targets. Actual role/Species tables and
rounded/Q11 validation remain open.
Do not select proposed numbers, claim phase closure, start a simulation harness
or advance to runtime work while design remains incomplete.

Evidence: [P11-reference-comparison.md](P11-reference-comparison.md).
Requirements/evidence status: [P11-verification.md](P11-verification.md).

## R20 — Unbounded input response versus repeated-fusion bound

Q14.4 sqrt response is unbounded as input increases, but a bounded grown-stat
term and fixed finite R/k produce a finite invariant bonus bound before rounding.
Reinforcement retaining Main bonus does not bypass it. This is not an explicit
configured hard cap, yet can lead to a natural plateau; owner intent pending
Q14.5. Do not promise unlimited accumulated bonus or certify a global ceiling
while training/rounding/operation coefficients remain open. See verification.
