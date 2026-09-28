# P10 review — evidence and remaining decisions

Status: reviewed discussion record; active gates are in [P10-readiness.md](P10-readiness.md). Accepted points below are user decisions from 2026-09-28;
proposals are not implementation approval.

## Confirmed

| Point | Source observation | Product decision |
|---|---|---|
| Roster | DataPoke has 152 unique IDs, 135 normal and 17 Special, uneven Race × Star counts | Preserve all 152 identities, source distribution and assets. No target of 180 and no equal-count rebalance. |
| MP | Poke/PokeInfo have currentMP/maxMP and a spirit/mana stat family; UI has MP | MP is a resource with rules owned by P11. Do not invent its formula now. |
| Growth reroll | Item descriptions support whole-profile and per-attribute reroll, but do not establish Egg-only gating | Reroll while Egg, including after Pet → Egg. Conversion/hatch does not itself reroll; inheritance and parent snapshots remain fixed. |
| Special | 4 TT4S + 13 TT5S records, exact Chinh/Phu parents at the same Star; separate KetHopTT4S/KetHopTT5S materials | Preserve the original Special targets, parent pairs and material identities. Unrecovered server rules stay unresolved. |
| Zero learned skills | APK has separate Attack/Magic actor clips; skill slot behavior is not proved by those clips | Basic attack button is always usable without learned skills and consumes no learned-skill slot. New Pet with 0 learned skills cannot use skill actions. |
| Race/Element/status | APK species catalog has Race/Star; combat metadata contains multiple elemental/status resistance fields | Race and Element independent; one Status Resistance, no per-status map or separate elemental resistance stat. This is a deliberate design change, synchronized to master. |

## Accepted: stat terms and inheritance (D14/D21/D22)

### What the original evidence establishes

IL2CPP metadata for PokeInfo contains separate field families `CSLuc/CSMana/...`,
`PTLuc/PTMana/...`, `KTLuc/KTMana/...`, `BDLuc/BDMana/...`. InfoPokePanel contains
`CoSo`, `PhuTro`, `KeThua`, `BanDau`, HP/MP/EXP controls. This supports separate
stat contributions in the client model. It does **not** recover the server's
inheritance coefficients, caps, rounding or the precise meaning of every number
rendered next to `+` in historical footage.

The original client uses strength/stamina/agility/intellect/spirit/defense and
derived HP/MP/combat values. The proposed six core stats are a product redesign;
copying an original field name is not enough to determine its new formula.

### Accepted contract — user selected option A

For each stat:

- **Grown component B:** Species Lv1 base plus growth earned at current level;
  growth uses this individual's profile. Does not include inheritance/equipment.
- **Inherited bonus H:** fixed when the Egg is created, independent of current level.
- **Permanent total T = B + H:** the input used when this Pet becomes a parent.
- **Equipped total O = T + equipment:** the Overview value before temporary battle effects.
- **Battle value:** derived from O under active effects; not an inheritance input.

Illustrative HP values, not approved growth coefficients:

| Situation | Grown B | Inherited H | Permanent T | Equipment | Overview O |
|---|---:|---:|---:|---:|---:|
| Lv1 | 128 | 12 | 140 | 0 | 140 |
| Lv20 | 186 | 12 | 198 | 0 | 198 |
| Lv20 wearing equipment | 186 | 12 | 198 | 25 | 223 |

At fusion, this parent contributes **198**, not 186, 210 or 223, under D14's
proposed total-permanent-stat rule. The other parent's permanent total is a
separate input. P11/P16 calculate a new child's inherited bonus from the two
totals; they do not append the parents' old H values again. Training matters
because B increases. Parent growth rolls are not copied into the child profile.

After Pet → Egg → reroll → hatch: level returns to 1, H stays 12, the new growth
profile affects future B. Species Lv1 base is fixed under D12/D13, so growth reroll
does not create a fresh random Lv1 base stat. Reaching the old level again may
produce a different B. A separate permanent-consumable-stat system is not defined.

Selected option **A**: Attributes `HP 186 +12` with explicit labels/tooltip
**Bản thân + Kế thừa**; permanent total is 198 and Overview shows 223 with equipment.
The first number must never be called the permanent total. Option B (showing
198 first with a separate breakdown) was not selected. Numeric growth/inheritance
formulas remain with P11/P16.

## Special fusion: Plus outcome awaits original-game verification

User chose to wait for original-game verification (2026-09-28). No custom
reset/preserve fallback is approved. Do not implement this outcome until source
evidence is reviewed; other P10 design discussion can continue.

A targeted check of the extracted metadata string literals found Special material
labels and IDs, but no statement establishing the Plus outcome. This limited
check does not establish that the behavior cannot be recovered from executable
code or observed in the original game. Material label text alone also does not
prove the server's validated quantity or cost.

Confirmed source structure is in P10-roster.md and the data catalog. All 17 exact
parent pairs resolve; each main parent has the target Race and both parents are
normal at the target Star. Do not allow arbitrary race-compatible parents to
produce a Special target just because normal Star-up permits generic parents.

These questions are not answered by the recovered table:

- Is Chinh/Phu order interchangeable in the original server?
- Does Special fusion reset Plus, preserve a parent's Plus, or calculate it?
- Exact level gates, material count, Gold cost and success chance.
- Exact stat-budget advantage and stat/skill inheritance behavior.
- Whether every existing Special can be Reinforced under all normal rules.

The product common rule Lv20 and generic new inheritance design should not be
presented as recovered APK behavior. Discuss unknown rules explicitly before P16.

## Accepted: MP on re-hatch

User decision (2026-09-28): after Pet → Egg → hatch, recalculate maximum MP
from the new Lv1 state under P11 rules and set current MP to this new maximum.
Do not carry over the old high-level current/max MP or its percentage. This is
a product decision; the original game's corresponding behavior is unverified.
The numerical formula and growth/inheritance contributions remain owned by P11.

Illustration only: old 30/200 MP, new Lv1 maximum 40 → 40/40 MP.

## Accepted: learned skills after re-hatch

User selected A (2026-09-28): level requirements apply when learning a skill,
not when using a preserved learned skill after re-hatch at Lv1. MP and other
P13 use conditions still apply. A newly created fusion/capture Egg still starts
with 0 current skills; this decision does not automatically teach inherited-pool
skills. Original-game behavior for this case remains unverified.

P13 should account for early access to preserved skills when balancing fixed
damage and strong effects; this note does not approve new balancing formulas.

## Accepted: inherited-skill eligibility

User selected A (2026-09-28): eligibility follows each skill's restrictions,
including allowed Races where applicable. Different skill/child Elements alone
do not exclude inheritance. This does not mean every skill is inheritable by
every Species. Eligible skills enter the inherited learnable pool, not current
skills. Learning-level requirements apply when learning, not when constructing
the newborn's inherited pool. P13 defines specific restrictions with P16.
This is a product decision; original-game eligibility has not been verified.

## Accepted: shared Status Resistance scope

User selected A (2026-09-28): the shared stat affects application probability
for all harmful statuses, including control, poison/burn, and stat reductions.
It does not reduce duration, direct hit damage, or the tick damage of a status
that was successfully applied. A hit can deal direct damage even when its
accompanying status is resisted. Formula, caps and boss rules remain with P11/P13.
This is a product decision; APK metadata has separate resistance fields and
does not establish this shared-stat behavior.

## Accepted: restoration after the child has hatched

User selected A (2026-09-28): a fusion child may hatch, progress, return to Egg,
and then split back into its exact two pre-fusion parents. Consume the child;
do not transfer its progress back to the parents or refund fusion/reroll costs.
Valid direct-parent snapshots remain required. Consumed parents stay unusable
until the split restores them; restoration must not duplicate pets. This is the
explicit exception to the master's previous one-way retirement rule.

Original APK item descriptions support splitting into the original two parents,
but do not establish the hatch/re-hatch eligibility conditions. The accepted
behavior is therefore a product decision. Equipment is resolved below; pet
capacity and ownership are resolved below.

## Accepted: equipment return with mailbox overflow

User selected automatic unequip and explicitly requested mailbox overflow
(2026-09-28). Fusion returns both parents' equipment to inventory, with items
that do not fit sent to the player's mailbox. Apply the same rule to Pet → Egg,
replacing the previous inventory-full rejection. Splitting restores parents
unequipped and never recreates equipment from snapshots. P19 owns the system
mailbox contract (delivery, claims, capacity, retention) with P14/P16 integration;
no detailed mail policy or player-to-player mail is approved by this decision.
Durable equipment delivery must be consistent with the operation and exactly
once. This is a product decision, not verified original-game behavior.

## Accepted: restoration ownership after a valid transfer

User selected A (2026-09-28): restoration rights travel with the child Pet/Egg.
Its current owner receives both restored parents on split, not the original
fusion owner. Parent identities and intrinsic snapshots remain intact; old owner
metadata cannot override the new recipient. Previously returned equipment is
not part of the transfer/restoration. Binding restrictions from both parents
must not be bypassed through fusion or splitting; detailed rules belong to
P08/P19/P16. This does not approve trading every pet or implementing trading now.
The original game's transfer/restoration behavior remains unverified.

## Accepted: restored-pet mailbox overflow

User selected A (2026-09-28): split succeeds when pet storage is full; parents
that fit go to storage and the rest await claim in the current owner's mailbox.
Preserve each restored parent's identity and intrinsic state, including level,
Plus, growth and skills. Mail claim does not convert it into an Egg or reset it
to Lv1. Unclaimed pets cannot be used or traded. Claim requires free pet storage
and delivers the same pet exactly once. Child consumption and durable delivery
must be consistent. P19/P16 define retention, capacity, claim UI and delivery
order; no mailbox expiry or numeric limit is decided here. Original-game
behavior is unverified.

## Remaining sequence

1. Stat definitions and display: resolved, option A.
2. Special same-Star contract and Plus: wait for original-game verification; no fallback approved.
3. MP's design boundary and re-hatch initialization: resolved; numeric formulas remain with P11.
4. Basic attack versus six skill slots; first hatch versus re-hatch: resolved, including level-as-learning-gate option A.
5. Race/Element and inherited-skill eligibility: resolved, option A. Shared Status Resistance covers all harmful statuses: resolved, option A.
6. Restore after hatch/re-hatch: resolved, option A; retirement exception synchronized. Equipment return: inventory then mailbox overflow, resolved. Restoration ownership: current owner, resolved option A. Restored-pet overflow: mailbox pending claim, resolved option A; detailed contracts deferred to P19/P16.
7. Endgame +99: resolved by user correction, 2026-09-28. Remove standalone build-change; allow Reinforcement at +99 with output +99, normal costs/parent consumption/Egg → Lv1 flow. This replaces the old cap-based rejection. User selected B for inheritance: diminishing marginal gains, no hard inheritance cap. Formula/rounding remain with P11/P16, long-run simulation with P15. Do not promise every donor improves every stat or that diminishing gains prove bounded total power. Special fusion Plus remains a separate source-verification question.
8. Species Native Skill Pool size policy: resolved, option A (2026-09-28). Counts may differ per Species; P13 defines concrete contents/counts by role and identity. Balance includes quality/synergy, not only count. Six current-skill slots remain unchanged, and the pool is not automatically learned. Original APK pools for all 152 Species remain unverified.
9. Reinforcement with a weak donor: resolved, option A (2026-09-28). For each stat, child inheritance bonus is at least the main parent's existing bonus, including at +99. Extra gains diminish; no automatic minimum +1. Preserve the bonus floor without adding old inheritance twice. This does not preserve high-level total stats, growth or level; child still hatches at Lv1. The floor is not automatically a Star-up or Special fusion rule. Formula/rounding remain with P11/P16; original-game behavior is unverified.

Only explicit decisions are incorporated into the active specification. The full
audit and named implementation gates are now in P10-readiness.md; this file
preserves rationale and does not constitute a gameplay-delivery claim.
