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

## Catalog v1.1 Bird update

Catalog constraints/reproduction PASS for152 records/304 layers. Only21 Bird
SPD base/growth pairs changed numerically.57 actual cross-Race same-cohort pairs
and252 possible template cohorts pass strict integer-base advantage plus
nonlower growth, proving strict ordering at every common grade/level. Earlier
arithmetic/review snapshots are explicitly pinned to v1. New evidence:
[Bird priority](evidence/bird-priority-20261012.json).

## 2026-10-12 follow-up: layout repair and catalog v2

The prior failed layout result is historical. The repaired current layout audit
passes and is included in tools/check_godot.mjs. A temporary incorrect-login
fixture failed with exit1 and no positive marker; it was removed afterward.
Full tools/check.sh passed; fresh go test -race ./... -count=1 and server build
passed. min_smoke completed with its existing overall PASS output.

Catalog v2 --write/--check validates152 frozen identities,304 numeric layers,
owner-approved Race direction checks and Bird priority. Static numeric vectors
increase from94 (v1.1) to137;27 Species remain in shared-vector groups. All152
authored descriptions avoid absolute superlatives;97 original quotes remain
verbatim,55 remain missing. Source/registry hashes and Bird SPD values remain
unchanged. See evidence/race-catalog-review-20261012.json and the current
catalog-validation.json. Older arithmetic/catalog review evidence remains pinned
to its recorded catalog version and does not certify v2 combat balance.

## 2026-10-13 effective roster160 follow-up

Current --check:160 records/320 layers,14 existing role/numeric amendments and
eight authored stable allocations;138 original stat profiles unchanged.
Exact MP/six-stat projection matches pinned P13 v7 after stable remapping.
Normal4/5 primary Physical/Magic coverage passes independently for all8 Races.
Bird proof:67 actual pairs plus252 templates.146 vectors;25 Species in shared
groups. Source152 --check also passes after authored registry append; original
namespace corruption still rejected. P13 v7 generator reproduces unchanged.

Seven focused generation/corruption regressions plus P13 compatibility passed;
see extension-regression-20261013.json. Build, fresh Go race tests, canonical
check (six Godot checks including contact/layout,7 load/3 planner tests, vet
and typecheck) and min_smoke PASS. No P11 runtime or measured balance claim.
Pinned design inputs permit reproduction before shared P10 changes are committed;
if a live authored namespace exists, allocation mismatch is rejected. Offline
static reproduction is not proof of live registry/art/runtime readiness.
