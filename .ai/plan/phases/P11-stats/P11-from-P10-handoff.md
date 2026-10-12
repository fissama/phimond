# Final P11 handoff amendment

P11 design completion is defined by [final spec](P11-final-spec.md). F02/F03
explicitly amend P10-D14/D16 and Q14.1/3/4: carry strongest lineage Q once,
earn from mean grown stats/training, preserve on Normal Star-up. Main floor,
diminishing gains, no hardcap, fixed Egg inheritance, source-gated Special and
no genetic gear remain. Old pending statements below are historical inputs.
P11 portions of O03/O04/O05 are now designed; cross-phase implementation and
O08 migration remain gated. See [readiness](P11-readiness.md).

# P11 — Concrete inputs from P10

Corrected 2026-10-12 against P10 D01–D46 and the owner's current P11 state.
The earlier scaffold contained suggestions inconsistent with P10; they are
superseded here, not reopened product decisions.

## Locked contracts

| Concept | Accepted form | Authority |
|---|---|---|
| Core stats | `hp`, `atk`, `mag`, `def`, `spd`, `status_resistance`; MP separate | D11 |
| Lv1 | Species base stats are actual fixed Lv1 stats; no start RNG or Race factor | D01/D12/D13 |
| Growth | Each Species owns six baselines; Egg creation rolls a fresh individual profile; deterministic leveling; hatch does not reroll | D12/D13 |
| Display | `grown_stat + inheritance_bonus`; 186 +12 means permanent total 198 | D14/D21/D22 |
| Parent inputs | Both current permanent totals; prior inheritance included exactly once; no equipment/temporary modifiers | D14 |
| Inheritance shape | Diminishing marginal gains, no hard cap or automatic minimum +1 | D16 |
| Reinforcement floor | Each child inherited bonus ≥ main's prior bonus of that stat, including at +99 | D16/D27 |
| Star-up | Resets Plus to +00; no automatic reinforcement floor extension | D08/D16 |
| Level cap | 1★60 / 2★70 / 3★80 / 4★90 / 5★100, plus `plus` | D07 |
| Plus | +00…+99; level cap only; no direct stat multiplier/addend | D07/D09 |
| Re-hatch MP | Recalculate Lv1 max MP; set current MP to that new max; no carry-over | ACTIVE.md / O03 |
| Reroll | Egg-only Full or Single-Stat; may improve/equal/worsen; only growth changes | D20/D31 |
| Status Resistance | Application chance for control, poison/burn, stat reductions; no damage/duration effect | D43 |
| Identity | 152 frozen IDs, eight source Races; Special is a class, not 6★ | D02–D05/D10 |

A +99 parent need not have inheritance bonus 99. The floor compares actual
`inheritance_bonus[s]` values, never Plus ratings or high-level permanent totals.

## Operations

`star_up`, `reinforcement`, `special_fusion`, `pet_reversion`, `hatch`,
`split`, `growth_reroll`, `mail_claim` remain canonical names.

Capture, Star-up and Reinforcement create an Egg with a resolved growth profile;
fusion rolls a new profile rather than copying parent rolls. Hatch uses the
stored profile. Pet → Egg preserves it unless an explicit reroll occurs.
Inheritance is fixed at Egg creation and unaffected by growth reroll.
Split restores immutable parent intrinsic snapshots; child progress and reroll
results do not rewrite those snapshots. P16 owns persistence/atomicity.

## What P11 still designs

- O03 with P13/P16: HP initialization/re-hatch, first-hatch MP formula and
  resource growth; re-hatch MP semantics already locked.
- O04 with P16/P15: deterministic growth curve, precision/rounding, inheritance
  formula/coefficients/parent weighting, numeric reinforcement floor behavior.
  Mixed-Plus output calculation is P16; Plus is not a direct stat input.
- O05 with P13: role vocabulary/blend/templates, species base/growth assignments,
  Element placement; P13 owns chart/native skills and per-skill eligibility.
- O08 contribution: compatibility requirements for later explicit migration,
  not a guessed mapping or runtime switch in this design phase.

The owner accepted Q1–Q7.5 and subsequently locked Q7.6 to A (fixed multiplier per grade); read
[P11-design-decisions.md](P11-design-decisions.md). Budget tolerances, grade
probabilities/ranges and inheritance/resource/status constants are unapproved.

## Design pitfalls corrected from the old scaffold

- No per-level RNG; grade/value sampling belongs to Egg creation or reroll.
- No `base_stats.hp × race_factor × star_factor` at hatch: actual Species Lv1
  values already contain the approved content budget. Do not scale twice.
- No Race × Star universal growth rate; baselines are per Species/stat.
- No `floor(parent.bonus × k^n)` treated as accepted inheritance: D14 inputs are
  both permanent totals and no numeric generation-depth stat is approved.
- Diminishing returns describes inheritance, not an already-selected growth curve.
- Star-up is a stat-inheritance consumer; P11 owns its math with P16 even though
  P16 owns the operation/validation. It does not automatically preserve the
  reinforcement floor when Plus resets.
- No “closest-looking species” legacy mapping and no simulation harness now.

## Future proof / delivery

See [P11-verification.md](P11-verification.md). A finite sample must not claim a
finite inheritance ceiling; no hard cap is approved. Test weak/strong donors,
main/donor swaps, actual per-stat floor values, +99, Star-up, repeated training
and hatch/reroll invariants after numerical formulas are approved.

Future runtime/content work must be additive, preserve frozen identities, use
copied-save/version/rollback gates, follow sprint specifications, and complete
the project's delivery/manual-validation ritual. This handoff grants no runtime
implementation permission and closes none of O03/O04/O05/O08.
