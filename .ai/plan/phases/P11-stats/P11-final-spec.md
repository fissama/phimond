# P11 — Stats system, design baseline v1

Date: 2026-10-12. Scope: **design and authored content only**. No runtime stat
engine, gameplay migration, DB writes or simulation harness is delivered.

This is the current normative P11 specification. Read with
[formulas](P11-formulas.md), [tables](P11-stat-tables.md),
[catalog](P11-species-catalog.md), [verification](P11-verification.md) and
[readiness](P11-readiness.md). The interview is preserved in
[decision history](P11-design-decisions.md); historical OPEN/LOCKED statements
there describe their checkpoint, not the final state.

## Authority and decision changes

**Owner selections:** Q7.6–Q13.10, matching-stat inheritance Q14, and the P10
foundation remain as recorded, except the explicit inheritance amendment below.
Q14.5 was a concern about weak fusion rewards, **not approval of a plateau**.
The owner's subsequent instruction, “Nghiên cứu những gì mình rep và thoàn thiện
cả phase này giúp mình”, delegates completion of the remaining design.

**Delegated v1 decisions (agent-selected, not individually owner-approved):**

| ID | Decision | Reason / affected contract |
|---|---|---|
| F01 | Independent six-stat draws; exact 100-bucket weights; immutable versions | Complete Q7 sampling and replay contract |
| F02 | Preserve strongest per-stat lineage investment; earn new training credit; shifted-square-root conversion | Replace the plateau-producing whole-bonus candidate in Q14.3/Q14.4 |
| F03 | Extend lineage preservation to Normal Star-up; preserve fractional credit | Avoid deleting grind at Star-up or losing repeated small gains |
| F04 | Complete MP, resource initialization and effective-stat interfaces | Resolve P11 part of P10-O03/O04 |
| F05 | Author 152 Species and six-element vocabulary as Phimond content v1 | Resolve P11 part of O05 without claiming recovered original stats |
| F06 | Immutable versioned contracts; explicit downstream gates | Close design while keeping implementation/economy/source gates visible |

F02 explicitly amends **P10-D14**'s prohibition on direct lineage carry and
**P10-D16**'s total-only/no-additive-floor formulation. It also replaces Q14.1's
raw-mean-as-sufficient-input contract and Q14.3's whole-bonus output contract.
The independent matching-stat rule, equal weighting of the parents' newly grown
stats, fixed positive references, diminishing marginal returns, Main floor and
no hard cap remain. Q14.2's fixed-reference policy remains; Q14.4's square-root
shape is used for converting accumulated credit, not resetting total inheritance.
F03 deliberately extends protection beyond the old Reinforcement-only floor.
These are visible product changes under the latest delegation, not discoveries
about the original game. P10's historical decision record is not rewritten.

## F07 — Owner-approved Bird SPD priority (catalog v1.1)

On2026-10-12 the owner chose Bird leading at the same Star, role, level and
grade, allowing different roles to exceed it. Comparisons also hold class equal
and use the complete ordered Primary/Secondary blend, zero inheritance/gear/
buffs. Catalog authoring sets Bird base/growth SPD to the highest representable
value <=105% of its exact role/Star target; other Races keep neutral rounded
values. Existing ±5% bounds remain. Strictly greater integer base SPD plus
nonlower growth preserves strict grown SPD ordering for every common grade and
legal level. The current validator enforces this for actual pairs and all252
possible template cohorts. Future authoring must preserve the ordering as well
as local bounds. This is embedded Species content, never a runtime Race bonus.

Source descriptions may be adapted: avoid unsupported species-level “highest”
claims in Phimond gameplay descriptions. Preserve verbatim source quotes as
historical evidence. See [Race direction](P11-race-identity-direction.md) for
scope and proposed identities of the other seven Races, which are not numeric
assignments yet. The other catalog-review findings remain open.

## 1. Stat sources and state

Six core stats: `hp`, `atk`, `mag`, `def`, `spd`, `status_resistance`.
MP is separate; there is no seventh growth roll. One shared DEF; no MDEF or
elemental resistance stat. Race has no stat multiplier; no STAB.

Species owns actual integer Lv1 base, per-stat growth baseline with at most
three decimals, fixed Star/class/Element/roles and later P13 native skill pool.
Base/growth catalog values already include Star, role blend and Species choices.
Never multiply those factors again at hatch. Instances own level, Plus,
immutable resolved growth grades and inheritance credit; derive Species identity.

`grown = base + floor(growth × grade_multiplier × (level−1))`.
`permanent = grown + inheritance_bonus`.
Inheritance is fixed when the Egg is made and never grows with the child's level.
Plus changes the legal level cap only: 60/70/80/90/100 + Plus, Plus in 0…99.
Level is integer in 1…cap. Reaching a higher cap alone gives zero stat gain.

Capture creates zero inheritance. Capture, Normal Star-up and Reinforcement
create a new six-grade profile; hatch reads it. Pet reversion, hatch, leveling,
login and battle do not draw grades. Egg-only Full Reroll replaces all six;
Single Reroll replaces only the selected stat. Worse/equal/better are legal;
no keep-best, pity or cross-stat budget. Reroll never changes lineage, Species,
parent snapshots or lineage-credit precision.

F01: six independent draws from unbiased integer 0…99, with cumulative intervals
D [0,3), C [3,15), B [15,55), A [55,83), S [83,95), SS [95,99), Perfect [99,100).
The shared table applies to every approved creation/reroll route. All-Perfect
on one full independent draw has probability 10^-12; single-stat targeting has
mean 100 draws per first Perfect, not a guarantee. Persist resolved grades and
table/catalog version; never regenerate old profiles from a new balance table.

## 2. Species authoring and comparison

Use the approved numbers in [tables](P11-stat-tables.md). Main budget is
HP/10 + ATK + MAG + DEF, checked separately for base and growth. Normal tolerance
±3%, Special ±2%; per-stat deviations from the exact role template are main±10%,
SPD/SR±5%, inclusive. SPD and SR have independent targets; no budget exchange.
Primary/Secondary weights 75/25; single Primary 100%. Base and growth modifiers
are independent; no compensation across layers. Exact target intermediates
precede final integer/milli authoring and validation.

Physical: ATK≥35% of actual main budget and ATK≥1.25 MAG. Magic mirrors this.
Tank: HP/10+DEF≥60%. Hybrid: ATK≥20%, MAG≥20%, combined≥50%.
Support: ally heal/protect/buff/cleanse. Disruptor: control/debuff that impairs
actions/effectiveness; pure HP damage over time alone does not qualify.
Support/Disruptor have no additional universal bulk/SPD minimum. Role rationale
is functional, not a skill-count quota; P13 must supply the intended function.
Roles are not recalculated from currently learned skills, and grant no free skill.

Compare all B and all Perfect, inheritance=0, no gear/buffs, same role/blend:
Lv1, common Lv60, own base cap and own +99 cap. Special4 targets sit between
Normal4/5; Special5 targets exceed Normal5. This is a main-budget statement at
comparable states, not every stat or every owned matchup. Aux bands overlap.
Unlimited inheritance means a sufficiently invested low-Star pet can exceed a
less-invested high-Star pet; there is no absolute finite low-Star power ceiling.
Higher Star retains its grown-stat budget advantage at equal conditions.

## 3. Inheritance: preserve investment, reward training

Apply only to **Normal** Star-up and Reinforcement when P10/P16 operation gates
pass (both Lv≥20, valid recipe/Star/Plus/materials). Special operation rules remain
disabled until P10-O01/O02 source gates and P16 are resolved. Stats assigned to
Special Species do not authorize acquiring/fusing/reinforcing them.

For each stat independently, read both parents' intrinsic snapshot:
grown `Gm,Gd`, lineage credit `Qm,Qd`, current level `Lm,Ld`, and Star base caps
`Cm,Cd`. Equipment, battle buffs and current HP/MP are excluded. Permanent totals
can be recorded for explanation, but are no longer sufficient as the sole inputs.

```
R = {hp:500, atk:50, mag:50, def:50, spd:100, status_resistance:50}
a = {hp:.15, atk:.15, mag:.15, def:.15, spd:.04, status_resistance:.04}
training = max(0, min((Lm−20)/(Cm−20), (Ld−20)/(Cd−20)))
G = (Gm + Gd) / 2
new_credit = a × G × training
Qchild = max(Qm, Qd) + new_credit
raw_bonus(Q) = R × (sqrt(1 + 2Q/R) − 1)
inheritance_bonus = floor(1000 × raw_bonus(Qchild)) / 1000
```

`Q` is earned lineage credit in stat units, a hidden intrinsic accumulator, not
another stat addend. It corresponds to `Q = B + B²/(2R)` for exact raw bonus B.
Only the derived bonus enters permanent totals. Carry one larger Q per stat;
do not sum parent Q, append Main bonus after conversion, or earn new credit from
either parent's old bonus. A high-investment donor transfers its stronger
lineage without duplicating both lineages. Swapping parent slots leaves this
numeric result unchanged; operation identity/recipe/Plus can still differ.

The training factor is **not capped at 1**. Both parents at their unmodified
Star cap give 1; actual levels above it earn more. Plus itself is not an input.
A Lv20 parent yields zero new credit, even alongside a highly trained parent;
existing lineage survives. This intentionally distinguishes eligibility from
rewarding training, and must be stated in the fusion preview. Both parents above Lv20 can earn positive credit; the derived .001 bonus may
remain unchanged until accumulated credit crosses its next display boundary. A high-Star parent is normalized by
its own base cap; no division by mutable Plus-expanded cap penalizes old training.

Store Q as a reduced exact nonnegative rational numerator/denominator, serialized
as decimal integer strings. This is design data, not a save migration. Do not
round each credit award to .001. Compute the derived .001 bonus via an exact
integer inequality (see formulas); thus accumulated sub-.001 awards eventually
become visible and no numeric rounding creates a permanent plateau. UI may show
integer summaries with precise detail and pending-credit progress. No forced +1.

At fixed grown stats/training, each repetition adds fixed E>0 to Q. After n:
`Qn=Q0+nE`; B grows without bound, while dB/dQ=1/sqrt(1+2Q/R) decreases.
If E=0, repeating fusion preserves lineage and adds nothing. Merging two equally
advanced parents does not double accumulated credit. New eggs cannot be cloned;
P16 must consume both parents atomically and prevent split/claim retry duplication.

**Magnitude example, not an XP/time claim:** with G=R, training=1 and no old
lineage, main-stat raw bonus/R after 1/5/10/25/100 fusions is approximately
0.140/0.581/1.000/1.915/4.568. At the tenth fusion the gain is about 0.076R,
roughly 4% of the preceding G+B total. Aux coefficients are smaller. The exact
catalog examples and long-run math are in verification. P15/P19 must check
real training time/cost; these numbers do not certify a fun economy.

## 4. Fusion presentation and reward acceptance

The child hatches at Lv1 using fresh grades already rolled at fusion Egg creation. It has zero current
learned skills, with eligible inherited skills in its pool (P13/P16). These P10
rules remain. A lower grade can offset some bonus at the same trained level;
fusion is not guaranteed to improve every final combat stat.

Before consumption, show deterministic inherited bonus/credit gain, current
parent totals, child Lv1 grown+bonus, cap change, and a **same-level projection**
at min(Main current level, child cap). If grades are not rolled until commit,
show D…Perfect range and B reference, never a fabricated exact outcome. After
creation show the actual projection with resolved grades and clear losses as
well as gains. Explain zero new training credit when either parent is Lv20.
Do not compare a trained parent's total to a Lv1 child as the sole reward display.

Main budget gain, SPD order changes and SR chance reduction are separate;
do not call a 10% SR-rating gain 10% status immunity. Show both numeric bonus
and capability growth (cap, learnable pool) without promising new learned skills.
P03 owns presentation implementation; P15/P19 own time-to-retrain/cost testing.
If benchmark rewards fail pacing targets, tune declared a coefficients through
a new version; never silently increase fresh growth grades or hide a downgrade.

## 5. MP and current resources — F04

MP has no random grade, inheritance, Race or equipment contribution in v1.
It is a resource, not evidence that Support/Disruptor automatically knows skills.

```
mp_role_factor = physical1.00, magic1.30, tank1.00,
                 hybrid1.15, support1.30, disruptor1.15
mp_star_factor = Normal [1,1.10,1.22,1.36,1.60], Special4 1.48, Special5 1.72
mp_base = round_half_up(50 × mp_star_factor × blended_mp_role_factor)
mp_growth = round_half_up_to_milli(.5 × mp_star_factor × blended_mp_role_factor)
maxMP(L) = mp_base + floor(mp_growth × (L−1))
```

Use 75/25 blend or single Primary. MP source values are derived from the pinned
Species version; no arbitrary per-Species MP modifier in v1. MAG is not an
extra MP multiplier. P13 starts skill-cost design against these maxMP anchors;
changing costs cannot mutate this curve without a versioned design change.

First hatch and re-hatch: full new Lv1 maxHP/maxMP, no battle statuses, no active
battle cooldowns. Reversion/fusion/hatch is prohibited during battle; costs and
availability belong to P16/P19. Full restoration is intentional; economy must
not assume reversion is free healing. Per-account item/service cooldowns and
timestamps survive lifecycle operations; no cooldown bypass by replacing a pet.

No passive world/battle HP or MP regeneration and no automatic end-battle refill
in v1. Server-authorized recovery service can restore both to max, clear battle
statuses and revive to full; access/cost belongs to P12/P19. Items restore only
declared amounts, capped at current max. Basic attack costs zero MP (P13).
Battle-local status/cooldown state ends with battle; P13 may later define an
explicit persistent status class, never infer it from SR. Fainted currentHP=0;
recovery/revival behavior at defeat is P02/P12, not automatic P11 teleport/heal.

Level-up or max-resource change preserves absolute current HP/MP then clamps
down to the new maximum; no free top-up and no revival. Hatch/recovery are the
explicit exceptions. Split restores parent intrinsic snapshots including Q and
old profile/level; initialize out-of-battle resources by clamp of saved absolute
values, clear battle-local state, and retain account cooldowns. Child progress
never enters restored parents. P16 must snapshot current resources at fusion.

## 6. Effective stats and combat boundary — F04

All modifier channels are declared data, never inferred from names. For each
core stat, v1 pipeline is:

```
P = grown + inherited
equipped = (P + sum(gear_flat)) × max(0, 1 + sum(gear_percent))
effective = (equipped + sum(battle_flat)) × max(0, 1 + sum(battle_percent))
```

Percent values within each channel add; channels multiply in this order. No
intermediate rounding. Flat channels use milli-stat integers; percent channels
use basis points (1/10000). Invalid/nonfinite/out-of-range serialized values are
rejected, not coerced. P14/P13 own permissible sources, stacking eligibility,
duration/dispels and budgets. Max HP=floor(max(1,effective_hp)); ATK/MAG/DEF
response inputs=max(0,effective), no extra rounding; final damage/heal rounding,
minimum damage, crit and penetration belong to P13. Equipment/buffs never become
permanent parent input. SR/SPD use their own approved response floors below.

`S=max(0,effective_sr)`; resistance=.80×S/(S+100).
Given P13's validated rational chance p in [0,1], final p=p×(1−resistance).
No absolute chance floor. SR never grants immunity; declared eligibility/immunity
is checked before this attempt. P13 determines whether a hit occurred and which
status attempts exist; one eligible status uses one Bernoulli draw at final p,
not separate proc/resist rolls. Multiple statuses each use the same interface;
shared event correlations must be explicitly specified by P13, not invented here.
Exact rational chance can use unbiased uniform integer [0,denominator) and compare
with numerator; implementation must specify rejection sampling and replay tests.

SPD comparator: descending max(0,effective_spd), retain fractional value. On
equality, use a fixed battle-specific random rank. F04 late entrant policy:
derive a 128-bit rank from server battle RNG stream on its first admission;
persist rank per combatant instance across reconnect/temporary withdrawal.
Collision falls back to stable instance ID, not another draw. New replacement
instance gets a new rank. Seed/state and rank are server-owned replay data.
Do not re-sort an already established action list due solely to SPD changes.
P02/P13 own order-formation timing, priority, eligibility/death/control and action
rights. SPD grants no extra turns, gauge/tick rate or skill priority.

## 7. Wild units, persistence and downstream contracts

Ordinary wild units use the same Species/catalog and grown-stat formula; v1
spawn profile all B, Q=0, declared legal level/Plus. Capture creates a new Egg
profile using the approved odds, Q=0; preview does not promise the wild profile.
Bosses require an explicit encounter modifier layer applied after intrinsic
stats, excluded from capture/inheritance; never edit Species base to boost a boss.
P12/P15 own spawn levels and P02 behavior. No unlisted boss exception.

Version every Species numeric catalog, growth table, inheritance formula and
resource ruleset. Pin versions on created Eggs/instances and immutable parent
snapshots. Normal fusion requires matching inheritance-formula versions and
uses that version for its result; mixed-version fusion is rejected until an
explicit conversion contract exists. Comparing Q from different R/semantics
would be invalid and could reduce a previously preserved bonus. Catalog changes are not retroactive by default; explicit migration
must state affected existing pets, preserve Q/profile/snapshots, dry-run copied
saves, compare before/after and provide rollback. Do not infer 14→152 legacy IDs
from names/portraits. No migration or runtime activation is authorized here.

| Owner | Required consumption / remaining gate |
|---|---|
| P13 | Six-element chart, Native Skill Pools consistent with roles, costs, damage/hit/status order and immunity; no free hatch skills |
| P16 | Atomic consume/create/restore, exact Q/profile versions, Lv20/recipes/Plus, immutable snapshots, Special source gates |
| P15/P19 | XP/retraining time, donor supply, fusion/reversion/reroll costs; real pacing and exploit proof before economy release |
| P14 | Gear channels and budgets compatible with effective pipeline; no genetic gear transfer |
| P02/P07 | Scheduling/replay, effective snapshot moments, PvP limits/matchmaking for unbounded progression |
| P03 | Honest before/after projection, fractions/credit detail and downgrade disclosure |
| Later implementation | Overflow/precision/replay/property tests and copied-save migration; no floating-point boundary guesses |

These are integration dependencies, not unanswered P11 numeric questions.
Design completion does not certify runtime correctness, combat balance, economy
fairness, original-game formula fidelity or readiness to enable Special operations.
