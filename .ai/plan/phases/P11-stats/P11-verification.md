# P11 — Verification evidence, 2026-10-12

Scope: authored design and arithmetic. Runtime checks below exercise the existing
legacy game only; they cannot certify an unimplemented P11 stat engine.
[Historical checks](P11-verification-interview-history.md) retain prior checkpoints.

## Executed design checks

- Catalog builder `--check`: **PASS**,152 frozen species,304 independently
  validated base/growth layers, source hashes/IDs/identities unchanged, exact
  deterministic reproduction, all precision/budget/modifier/role guards.
- One-off exact-rational calculation: **PASS**,4,256 catalog growth states
  (152×4 level positions×7 grades; duplicate levels counted as positions), each
  with six stats. Lv1 invariant, monotonic grade, milli-integer formula equals
  rational cumulative floor. This is not a runtime/simulation harness.
- Probability totals/means: **PASS**,100%,1.0108 main/1.00324 aux.
- Exact inheritance view: **PASS**,5 exact .001 boundaries plus4 just below.
- Long run: closed-form Q=nE at9 checkpoints through10,000; analytical proof
  of unbounded accumulation and diminishing marginal gains. This is mathematical
  evidence, not10,000 gameplay sessions or an economy simulation.
- Independent inheritance review found three issues: mixed-version Q comparison,
  hatch-time sampling wording, and unconditional Lv21 improvement claim. All
  corrected in final spec; negative-grade outcomes remain disclosed.

Static results: [design arithmetic](evidence/design-arithmetic-20261012.json),
[catalog validation](evidence/catalog-validation.json).

## Concrete reward example

`species_0001` Nhện Vong Linh, both parents Normal1 Lv60 allB, no inheritance,
no gear: ATK=45+floor(.9×59)=98. Training factor1. New ATK credit14.7,
bonus13.007. Child at the same Lv60 and B has111.007 ATK: +13.27%.
The child actually hatches Lv1: ATK45+13.007=58.007 until retrained.
A Lv20 donor produces zero fresh training credit but preserves old lineage.

Fixed G=R=50, full training, main coefficient.15:

| Fusion count | Bonus | Gain from last fusion | G+bonus |
|---:|---:|---:|---:|
| 1 | 7.008 | 7.008 | 57.008 |
| 5 | 29.056 | 4.895 | 79.056 |
| 10 | 50.000 | 3.824 | 100.000 |
| 25 | 95.773 | 2.595 | 145.773 |
| 100 | 228.388 | 1.351 | 278.388 |

Numbers are .001 derived values; exact Q persists. Fixed G/training makes this
an analytical fixture, not a prediction of changing-Star/Plus progression.

## Important non-guarantee

A tested unfavorable fixture uses `species_0001`, Lv60, Perfect parent growth,
old ATK credit equivalent to10 full-training generations, then a D child:
same-level ATK186.977→181.624 (−5.353) despite a larger inherited bonus.
This is the preserved fresh-growth-reroll rule, not hidden by the new inheritance
model. The preview must show it. A guarantee that every fusion raises every total
would require a separate change to that owner-approved RNG policy.

## Contract acceptance matrix

| Cases | Design result | Runtime proof owner |
|---|---|---|
| Lv1/growth/grade/Star comparisons | Formula and catalog arithmetic checked | Later stat engine |
| Full/Single reroll and sixPerfect | Exact odds/state contract; no shared budget | P16 RNG/persistence |
| Parent inputs/floor/slots/+99/Star-up | Explicit amended Q model, one carry, no gear | P16 transaction/property tests |
| Split/retry/reversion | No extra earnedQ; immutable snapshots | P16 duplication tests |
| Resources/hatch/levelup | MP and current-resource policies specified | P13/P16/P02 |
| SR/SPD/effects | Exact response/order/channel boundaries specified | P13/P02/P14 |
| Source/152 identity | APK/roster/video research + frozen identity checks | No numeric source-fidelity claim |
| Fun/economy/PvP | Not established by arithmetic | P15/P19/P07 playtests |

## Operational delivery checks

Server build PASS; go test -race PASS (4 tested packages); tools/check.sh PASS
(including Go checks,5 client script checks,7 load-unit tests,3 planner tests and
typecheck). Separate min_smoke PASS and contact_check PASS. Legacy layout_audit
FAIL: LoginScreen rectangle expectations and missing BattleScene Window;2/4
layouts fail. This existing issue is already recorded in ACTIVE.md, but the
AGENTS smoke gate remains blocked. These checks do not exercise P11 runtime.
See the dated handoff for final actual results and existing-workspace limitations.
