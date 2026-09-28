# P10 — Pet Model Foundation: Design Decisions

**Baseline date:** 2026-09-28

**Status:** Design baseline audited; implementation/source gates tracked in [P10-readiness.md](P10-readiness.md). No gameplay delivery claimed.

**Coding entry point:** [P10-data-contract.md](P10-data-contract.md). Canonical IDs: `data/p10/`; source evidence: `data/pets/roster_apk84.json`.

**Purpose:** Lock the semantics of Pet / Species / Egg / Fusion / Growth / Inheritance / Skills so P11, P13, P16, P19 and P20 can design their detailed formulas and systems without re-interpreting P10 decisions.

> Imported from the user's `P10 Design Decisions.md`, then updated with explicit decisions confirmed on 2026-09-28. Sections marked pending remain discussion proposals. APK observations establish source content; unobserved server rules are not inferred from asset names. Numeric formulas remain owned by their later phase.

Confirmed during repository review: use the original 152-species roster and distribution; MP is a resource owned by P11; growth reroll is allowed after Pet → Egg; use APK-defined Special species/parent pairs/materials; basic attack is available with zero learned skills; Race and Element are independent and Status Resistance is one shared stat. Stat display option A is accepted: `grown_stat + inheritance_bonus`; their sum is the permanent total (D14/D21/D22).

---

## 1. Taxonomy: Race, Element, Species

### P10-D01 — Remove `Family` as a separate gameplay axis
- Remove `Family` when it duplicates Race.
- `Race` = Species taxonomy + eligibility dimension for skills/fusion.
- `Element` = independent combat element.
- Race and Element do not map 1:1.
- Race grants no automatic damage multiplier/stat bonus.
- Elemental interaction is `skill.element` vs `target.element`.
- No same-element/STAB bonus.
- Exact element chart/multipliers belong to P13.

### P10-D02 — Initial 8-Race target
Initial target:
- Insect
- Spirit
- Bird
- Demon
- Beast
- Plant
- Undead
- Dragon

Rules:
- 8 Race is the initial target, not permanent canon.
- Preserve the source Race of each of the approved 152 Species; roster counts need not be equal.
- Do not reclassify a source Species just to balance counts or match its appearance. Any future exception requires a separate content decision.
- Each Species still has exactly one canonical Race in data.
- Beast is narrower than a generic “all animals” bucket.
- P10 does not add reptile/aquatic/amphibian races yet.

### P10-D03 — Race / Element / Star are fixed Species properties
Species owns:
- race
- element
- star
- species_class
- Lv1 base stats
- growth baseline by stat
- role metadata
- Species Native Skill Pool

Rules:
- Pet instances do not independently change Race / Element / Star.
- Do not persist `pet.race` / `pet.element`; derive from Species.
- `pet.star` may remain for compatibility/query/UI, but invariant: `pet.star == species.star`.
- BattleUnit snapshots Element at battle start.

---

## 2. Species Classification and Roster

### P10-D04 — Normal vs Special Species
`species_class = normal | special`

- Special is domain/content classification, not an extra Star.
- No mandatory Special badge/border/tag in normal pet UI.
- Players mainly recognize Special targets through Formula/content.
- Special Formula rarity/source belongs to Items/Economy.
- Special Species may use elevated stat budgets versus normal Species of the same Star.
- Star defines baseline power band; Species defines exact stat budget/allocation.
- Exact budgets belong to P11.

### P10-D05 — Approved APK 8.4 baseline: 152 Species
Canonical authoring catalog: `data/p10/species.json`; immutable source identity/art catalog: `data/pets/roster_apk84.json`. Full list and source notes: [P10-roster.md](P10-roster.md). Preserve exact source IDs separately in the ID registry and source metadata; use canonical IDs for new development. Preserve names, Race, Star, Special classification and assets. Runtime stat/element/skill configuration and migration are later work; the 14-species legacy catalog is not historical source truth.

| Star | Target Species |
|---|---:|
| 1★ | 50 |
| 2★ | 30 |
| 3★ | 24 |
| 4★ | 21 (17 normal + 4 Special) |
| 5★ | 27 (14 normal + 13 Special) |
| **Total** | **152 (135 normal + 17 Special)** |

Approved Race × Star matrix (normal and Special combined):

| Race | 1★ | 2★ | 3★ | 4★ | 5★ | Total |
|---|---:|---:|---:|---:|---:|---:|
| Insect | 7 | 4 | 3 | 2 | 4 | 20 |
| Spirit | 5 | 2 | 3 | 3 | 4 | 17 |
| Bird | 7 | 4 | 3 | 3 | 4 | 21 |
| Demon | 6 | 4 | 3 | 3 | 2 | 18 |
| Beast | 7 | 4 | 3 | 4 | 4 | 22 |
| Plant | 7 | 4 | 3 | 2 | 4 | 20 |
| Undead | 7 | 4 | 3 | 2 | 4 | 20 |
| Dragon | 4 | 4 | 3 | 2 | 1 | 14 |
| **Total** | **50** | **30** | **24** | **21** | **27** | **152** |

Notes:
- Matrix was decoded from `DataPoke` in the supplied APK 8.4 and approved by the user.
- No added species or equal-count redistribution is part of this baseline.
- Use the original 152 portraits and 760 linked animation clips in `apps/game-client/assets/pets/apk84/`.
- This is the embedded catalog; obtainability on a live original server is not established.

### P10-D06 — Capture Tier
- Only wild 1★ monsters are captureable.
- Successful capture creates an Egg Item, not a Pet directly.
- Not every 1★ Species must be wild-captureable.
- Some 1★ Species may come from quest/event/NPC exchange/reward/limited content.
- Wild 2★–5★ monsters may exist for battle/boss/challenge but are not captureable.

---

## 3. Star, Level and Plus

### P10-D07 — Base Level Caps
| Star | Base Level Cap |
|---|---:|
| 1★ | 60 |
| 2★ | 70 |
| 3★ | 80 |
| 4★ | 90 |
| 5★ | 100 |

`plus = +00..+99`

`effective_level_cap = base_star_cap + plus`

Example: 5★ +99 => Lv199.

Rules:
- Plus only increases level cap.
- Plus never directly adds/multiplies stats.
- Plus must not appear as a direct stat-formula addend/multiplier.
- There is no separate numeric “generation depth” gameplay stat.
- Plus is the approved product axis; exact equivalence to original-game generation semantics is not established by catalog extraction.
- Lineage depth is represented through parent relationships, not a number.
- Current reconstruction `Pet.Generation` and `Refinement` must not be blindly renamed; migration needs a dedicated plan.

### P10-D08 — Star-up and Plus
- Star-up does not require minimum Plus.
- Star-up always resets Plus to `+00`.
- Both material pets must be at least Lv20.
- Training above Lv20 may still improve child inheritance through stronger permanent stats.
- 6★ is not in the current ruleset.
- Architecture should not make future 6★ impossible.

### P10-D09 — Reinforcement and Plus
- Main and donor must be same Star.
- Resulting Plus depends on Plus values of both pets.
- Exact Plus formula belongs to P16.
- Plus calculation and stat inheritance are independent pipelines.
- User correction (2026-09-28): +99 can still be Reinforced when common validation passes. Plus is capped at +99; a +99 main produces +99. Do not reject merely because Plus cannot increase at the cap. The below-cap formula remains with P16.

---

## 4. Special Same-Star Fusion

### P10-D10 — Special 4★ / 5★ Fusion
Special means the APK's `TT4S` / `TT5S`: exactly 4 Special 4★ and 13 Special 5★ Species. Adopt each original target and exact `Chinh` / `Phu` parent pair from the catalog, with same-Star parents. Keep parent slot order until original order interchangeability is verified. Use the original `KetHopTT4S` / `KetHopTT5S` material identities.

Examples:
- exact 4★ X + exact 4★ Y → Special Z 4★
- exact 5★ A + exact 5★ B → Special S 5★

Rules:
- Source-confirmed recipes are in [P10-roster.md](P10-roster.md); no extra Special species are introduced.
- Source catalog does not recover server cost, Plus outcome, success chance, stat budget or inheritance formula. These remain explicitly unresolved; do not invent a numeric "APK rule".
- User decision (2026-09-28): wait for original-game verification of the Special fusion Plus outcome. Neither reset to +00 nor preservation of the main parent's Plus is approved as a fallback. Keep this behavior blocked until evidence is reviewed.
- Same-Star Special recipes are distinct from normal N→N+1 Star-up. Formula ownership and the common fusion flow must support both recipe kinds.
- Special 4★/5★ may be substantially stronger than normal Species at the same Star.
- Special Reinforcement eligibility remains source-unverified (P10-O02); do not enable it merely from this draft. If enabled after verification, Reinforcement preserves the main Species as in D27.
- Keep Special validation separate until verified; common product rules must not be presented as recovered server rules.
- 5★ is current Star ceiling; 6★ is only a future possibility.

---

## 5. Core Stats and Growth

### P10-D11 — Six Core Stats
MP is a separate resource. P11 owns maximum MP and its growth/recovery rules, coordinating skill consumption with P13. It is not silently removed or counted as a seventh core stat by this list.

Core stats:
- HP
- ATK — physical offense
- MAG — magic offense; may scale healing/shields when skill rules choose
- DEF — shared defense for physical and magic
- SPD — determines turn order only at P10 foundation
- Status Resistance — affects probability of receiving a status

Not core stats:
- MDEF
- Accuracy
- Evasion
- Crit Rate
- Crit Damage

Accuracy/Evasion/Crit may exist later through Skill/Equipment/Effect systems.

### P10-D12 — Lv1 Base Stats and Species Growth
- `species.base_stats` are actual Lv1 stats.
- Each Species has its own growth baseline by core stat.
- Archetype may exist only as a content/balance helper.
- Level growth is deterministic.
- No per-level RNG.

### P10-D13 — Individual Growth Profile
This supersedes random start-stat variance.

Rules:
- Start stats are not randomly rolled.
- Each individual has an independent growth deviation/profile for every core stat.
- Profile is rolled when the Egg is created:
  - successful capture
  - Star-up
  - Reinforcement
- Fusion child rolls a completely new individual growth profile.
- Parent growth rolls are not copied.
- Hatch never automatically rerolls it. A Pet returned to Egg may use a reroll item again (D20/D31).
- Exact distribution and effect on final stats are deferred to P11/P16.
- Requirement: differences must remain meaningful without creating excessive gaps, especially near Lv199.

---

## 6. Stat Inheritance

### P10-D14 — Inheritance Input
**Accepted terminology:** `grown_stat` is Species Lv1 base plus growth earned at the current level under the individual's growth profile, excluding inheritance and equipment. `inheritance_bonus` is the fixed inherited contribution. `permanent_total = grown_stat + inheritance_bonus` includes inheritance exactly once.

Both Star-up and Reinforcement use current total permanent stats of both parents as inheritance inputs.

Correct concept:
`child.inheritance_bonus = f(main.permanent_total, secondary.permanent_total)`

Do not directly sum/copy parent inheritance fields.

Included:
- permanent core stats
- prior inheritance already embodied in parent permanent stats
- Status Resistance

Excluded:
- equipment
- temporary buffs/debuffs
- combat-only modifiers

### P10-D15 — Inheritance Is Fixed
Once Egg is created:
- inheritance contribution is fixed.
- inheritance does not scale with level.

UI example:
- Lv1: `HP 128 +12`
- Lv20: `HP 186 +12`
- Lv50: `HP 274 +12`

### P10-D16 — Inheritance Uses Diminishing Returns, No Hard Cap
User selected B (2026-09-28): inherited bonuses can continue increasing, with
diminishing marginal gains and no hard inheritance cap. Reinforcement remains
available at +99 while output Plus stays +99. This replaces the proposed hard
inheritance cap; it is a product decision, not verified original-game behavior.

P11/P16 define the formula, inputs, coefficients, precision and rounding. P15
must simulate long sequences, equivalent parent quality, donor/slot changes and
Star-up to verify diminishing gains and pacing. Smaller gains do not by
themselves prove a finite bound on total power. Do not silently reintroduce a
hard cap or a minimum +1 gain, or claim every combination improves every stat.
User selected A for weak donors (2026-09-28): in Reinforcement, each child's
inherited stat bonus must be at least the main parent's existing bonus for that
same stat: `child.inheritance_bonus[s] >= main.inheritance_bonus[s]`. Any extra
gain follows diminishing returns; there is no automatic minimum +1 gain.
This floor preserves inherited bonuses, not the main parent's high-level total,
growth profile or level. The child still hatches at Lv1. Count the main parent's
old inheritance once in the total-based calculation; enforcing a floor must not
append it again. The floor applies to Reinforcement, including at +99; it is not
automatically extended to Star-up or source-unverified Special fusion.
Exact formulas and rounding remain with P11/P16. Original-game behavior for
this floor has not been verified.

---

## 7. Egg Lifecycle and Storage

### P10-D17 — Egg Is an Item
All acquisition routes create Egg before owned Pet:
- wild capture → Egg
- Star-up → Egg
- Reinforcement → Egg

Pet instance is created at hatch.

### P10-D18 — Hatch Rules
- Formula is not required.
- Active team max = 3 pets.
- Hatch requires a free active-team slot.
- If team is 3/3, hatch fails without consuming Egg.
- Successful hatch creates a Lv1 Pet directly into active team.
- Farm storage is not an automatic hatch destination.

### P10-D19 — Farm Storage
- Base farm pet storage = 30 pets.
- Future items may expand storage.
- Exact expansion amount/max/source/price belongs to Items/Economy.
- Pet Keeper manages active ↔ storage.
- Fusion NPC may select eligible pets from active team or storage.

### P10-D20 — Egg Growth Reroll
Two future item capabilities:
1. Full Growth Reroll — rerolls all core-stat growth rolls; no stat lock.
2. Single-Stat Growth Reroll — rerolls one chosen core stat.

Rules:
- New result may be better, equal or worse.
- Reroll only works while object is Egg.
- While the object is a hatched Pet, its growth profile is locked.
- Pet → Egg re-enables the same Egg-only reroll items. Conversion and hatch do not automatically reroll.
- Reroll changes the growth profile only; fixed inheritance and immutable parent restoration snapshots remain unchanged.
- Item rarity/source/cost belongs to Items/Economy.

---

## 8. Stat UI

### P10-D21 — Base / Attributes Tab
**Accepted option A:** show the grown component followed by the fixed inherited bonus. Label/explain the components as **Bản thân + Kế thừa**; the first number is not the permanent total.

Do not show raw growth-deviation percentages.

Display:
`grown_stat + inheritance_bonus`

Example:
- `HP 128 +12`
- `ATK 74 +8`
- `MAG 62 +6`
- `DEF 61 +5`
- `SPD 52 +3`

Rules:
- first value increases with level/growth.
- inheritance number remains fixed.
- equipment is not included here.
- `HP 186 +12` means permanent HP 198. Do not display `198 +12`, which would count inheritance twice.

### P10-D22 — Overview Tab
Use the permanent total from D14, including inheritance exactly once, then apply equipment.

Overview shows final current stats with equipment applied.

Concept:
`overview_stat = permanent_total + equipment_bonus`

Example: Attributes `HP 186 +12`; equipment adds 25; Overview shows 223. The parent's inheritance input is 198. Temporary combat modifiers do not enter either the permanent total or inheritance input. Numeric growth/inheritance coefficients remain P11/P16 decisions.

---

## 9. Formula and Farm NPCs

### P10-D23 — Formula Knowledge
Formula:
- Item containing target Species image/identity.
- tied to exact `species + star`.
- use once → unlock permanent account-owned knowledge.
- one account = one character, but semantics are account-level.
- duplicates may still drop.
- future sell/trade/market may be designed later.
- reusing an already-known Formula should reject without consuming it.
- Formula is not consumed per fusion.
- Hatch does not require Formula.

Unlock semantics:
- 1★ Formula → Reinforcement for that exact target.
- Normal 2★–5★ Formula → unlock normal N→N+1 Star-up into target + Reinforcement of exact target.
- Special Formula → the APK's exact same-Star parent recipe for that Special target; no generic N→N+1 shortcut into it. Reinforcement eligibility for Special follows the separately reviewed common rule, not an inferred source server behavior.

### P10-D24 — Three Farm NPCs
1. Fusion NPC
   - Star-up
   - Special same-Star recipes from the APK catalog
   - Reinforcement
   - sells fusion stones/materials for Gold
   - target selection from unlocked Formula list

2. Incubator NPC
   - hatches Eggs

3. Pet Keeper
   - active/storage management

### P10-D25 — Fusion Stones
Two families:
- Ascension Stone → Star-up
- Reinforcement Stone → Reinforcement

Special same-Star fusion uses the source's separate `KetHopTT4S` / `KetHopTT5S` material variants. It must not silently charge a normal Star-up stone. Exact costs/counts remain unresolved.

Convention:
`Stone Star = resulting Pet Star`

Examples:
- 2★ + 2★ → target 3★ → Ascension Stone 3★
- Main 3★ + donor 3★ → Reinforced 3★ → Reinforcement Stone 3★

Exact quantities/catalog/costs belong to P16/P19.

---

## 10. Star-up Rules

### P10-D26 — Normal Star-up
Requirements:
- two material pets have same Star N.
- both are at least Lv20.
- same Species is not required.
- same Race is not required.
- player selects target from unlocked Formula list.
- normal progression target Star = N+1.
- at least one ingredient pet must have same Race as target Species.
- Special targets are excluded from normal Star-up; use their separate exact same-Star recipes under D10.
- both parents are consumed.
- result is Egg Item.
- result Species/Race/Element/Star come from target Species.
- Plus resets to +00.

---

## 11. Reinforcement Rules

### P10-D27 — Reinforcement
- Main and donor are same Star and both at least Lv20 under the common product fusion gate.
- Special Species eligibility is separately gated by D10/P10-O02.
- Donor may be any Species/Race/Element if common validation passes.
- Formula of exact main `species + star` must be unlocked.
- Main Species properties are preserved: Species/Race/Element/Star. This does not promise the same owned pet instance ID after fusion; two parents are consumed and a child is created.
- Both pets are consumed.
- Result is Egg → hatch Lv1.
- Resulting Plus uses both parents' Plus values under P16 formula.
- New inheritance uses both parents' current permanent stats.
- +99 can Reinforce; the result stays +99. The same two-parent consumption, costs, Egg → Lv1 hatch and inheritance pipeline apply. Plus caps level capacity; inheritance uses diminishing returns without a hard cap under D16. P11/P16 own the formula. Repeated reinforcement is not a promise that every stat increases.

---

## 12. Lineage, Restoration and Pet ↔ Egg

### P10-D28 — Direct Lineage Only
- Store direct two-parent lineage.
- No numeric generation depth.
- No P10 requirement for full ancestry-tree traversal.

### P10-D29 — Fusion Restoration Snapshot
Fusion Egg preserves:
- direct parent references
- immutable pre-fusion restoration snapshot for Parent A
- immutable pre-fusion restoration snapshot for Parent B

Snapshot must allow exact restore of both parents' intrinsic state immediately before fusion. Equipment ownership is handled separately under D32; restoration does not recreate or re-equip items returned to inventory/mail. Historical owner metadata is not authority to return pets to an old owner: restoration ownership follows D30.

### P10-D30 — Split Fusion Egg
Split Item:
- works only while object is Egg.
- User selected A (2026-09-28): a fusion child that has already hatched may return to Egg under D31 and then be split. Having hatched before does not remove restoration eligibility; valid direct-parent snapshots are still required.
- deletes/consumes child Egg.
- restores exact Parent A and Parent B.
- Restore the parents' pre-fusion state, not progress earned by the child. Child levels, learned skills and rerolled growth do not transfer back to the restored parents. Reroll costs are not refunded.
- Retired parents cannot be used while consumed. A successful split restores those same parents and consumes the child atomically; it must not create additional copies. Restored parents are usable once delivered to pet storage; parents awaiting mailbox claim remain unavailable. This is the explicit exception to the old one-way retirement rule.
- does not refund Gold.
- does not refund Ascension/Reinforcement Stone or material costs.
- child growth rerolls do not mutate parent restoration snapshots.
- User selected A (2026-09-28): the restoration right follows the child Pet/Egg through any valid ownership transfer. Splitting grants both restored parents to the child's current owner, not the original fusion owner. Preserve parent identities and intrinsic snapshots; historical owner fields must not overwrite the current recipient.
- Transfer eligibility must respect both parents' binding restrictions; fusion, re-hatch and splitting must not bypass a parent's non-transferability. P08/P19/P16 define the detailed binding/transfer contract before trading is implemented. This decision does not make every child tradable or return previously removed equipment to the buyer.
- User selected A (2026-09-28): if pet storage lacks space on split, deliver parents that fit to storage and hold the remaining restored parents in the current owner's mailbox. Storage capacity alone does not reject splitting. Mail preserves restored identity, level, Plus, growth, skills and other intrinsic snapshot state; claiming does not create an Egg or reset level.
- A parent awaiting claim cannot be used or traded. Claim requires available pet storage and transfers that same pet exactly once; it must not create a second copy. Split consumption and durable delivery to storage/mail commit consistently. P19/P16 define mailbox retention, capacity, claim UI and deterministic delivery order; no numeric limits or expiry policy are approved here.

### P10-D31 — Pet → Egg
Future item may convert Pet back to Egg.

Preserve:
- Species
- Star
- Plus
- individual growth profile
- inheritance
- gender
- direct parent/restoration metadata
- all current permanent learned skills
- inherited skill pool

When hatched again:
- level = 1
- xp = 0
- Recalculate maximum MP from the new Lv1 state using P11 rules, including any approved growth reroll and preserved inheritance as those rules specify.
- Set current MP to that newly calculated maximum. Do not carry over the former high-level current/max MP or preserve its percentage. This is the user's design decision (2026-09-28), not verified original-game behavior.

Do not reroll growth or inheritance.
This describes conversion itself. Once converted, the player may explicitly consume a growth-reroll item as allowed by D20. Re-hatch preserves current learned skills (unlike a newly created fusion/capture Egg) and does not reroll inheritance.

### P10-D32 — Equipment Handling on Fusion and Pet → Egg
User selected automatic unequip with mailbox overflow (2026-09-28).
For both fusion parents, or the pet being converted to Egg:
- auto-unequip all equipment.
- return equipment to inventory.
- send equipment that does not fit to the player's mailbox; inventory capacity alone does not reject the operation.
- equipment is never stored in Egg payload.
- splitting restores parents unequipped; snapshots must not recreate items already returned to inventory or mail.
- P19 (Items) owns system mailbox delivery/claim semantics, capacity and retention rules, coordinated with P14/P16. These details are not approved here.
- conversion/fusion and durable inventory/mail delivery must commit consistently and exactly once, including on retry; a failed delivery must not lose or duplicate equipment.

### P10-D33 — Split After Previous Hatch
If fusion result already hatched:
`Pet → Pet-to-Egg item → Egg → Split item → exact restore parents`

Fusion-origin restoration metadata must survive:
`Egg → Pet → Egg`

Implementation must prevent duplicate ownership/restore exploits.

---

## 13. Gender

### P10-D34 — Metadata Only
Gender:
- cosmetic/identity metadata.
- no global male+female fusion requirement.
- does not affect Star-up/Reinforcement eligibility.
- does not affect inheritance or Plus.
- future special Formula may use gender only if explicitly designed later.

---

## 14. Skills

### P10-D35 — Max 6 Current Skills
Basic attack is a separate gameplay action available through the attack button even with zero learned skills. It does not occupy one of the six learned-skill slots. A newly hatched Pet with no learned skills cannot use skill actions yet, but can attack normally.

Supersedes previous “10 learned skills” direction.

A Pet has at most:
`6 current skills`

These 6 are:
- current permanent learned set
- active battle set

No separate 10-skill reserve list.

### P10-D36 — Inherited Skill Pool
At fusion:
- only parents' current skills are candidates.
- max 6 + 6.
- combine → deduplicate → eligibility filter → child Inherited Skill Pool.
- User selected A (2026-09-28): inheritance eligibility is defined per skill. A skill may allow multiple Races or restrict specific Races; a mismatch between skill Element and child Element does not by itself exclude the skill. This does not approve universal inheritance of every skill. P13 defines individual restrictions in coordination with P16.
- Eligible inherited skills enter the learnable pool, not the current learned set. Learning-level gates are checked when learning; a child's initial low level must not by itself discard a skill from its inherited pool.
- no RNG chooses inherited skills.
- pool is stored permanently on Egg/Pet.
- pool may contain more than 6.
- first hatch of a newly created fusion/capture Egg starts with 0/6 current skills; basic attack remains available.
- re-hatch after Pet → Egg preserves its current skills under D31.
- User selected A (2026-09-28): a skill's level requirement gates learning, not use of an already learned skill. After re-hatch at Lv1, preserved current skills are immediately usable subject to MP and other P13 use conditions; do not level-lock them again. This is a product decision, not verified original-game behavior. Newly created fusion/capture Eggs still hatch with 0 current skills.

### P10-D37 — Only Current Skills Propagate
When a Pet later becomes parent:
- only its current 6 skills propagate.
- full historical Inherited Skill Pool does not automatically propagate.

### P10-D38 — Skill NPC Available Pool
`Skill NPC available pool = Species Native Skill Pool + Inherited Skill Pool + Other Eligible Skills defined by P13`

Rules:
- Species Native Skill Pool preserves Species identity.
- Inherited Skill Pool preserves lineage options.
- Other Eligible Skills may cover Race/quest/item/trainer/event rules.
- At 6/6, learning a new skill requires replacing/forgetting one current skill.
- NPC-learned skill becomes a permanent current skill.
- if still in current 6 at future fusion, it can pass to next generation.
- User selected A (2026-09-28): Native Skill Pool size is content-driven per Species and may differ between Species. P13 defines the concrete skills/counts by role and identity; there is no mandatory equal-size pool across Species. This does not alter the six current-skill limit or automatically teach pool skills. Balance must consider skill quality/synergy, not count alone. Original APK pools for all 152 Species have not yet been verified.

---

## 15. Role Metadata

### P10-D39 — Primary and Optional Secondary Role
Species has:
- `primary_role`
- optional `secondary_role`

Initial vocabulary:
- physical_dps
- magic_dps
- tank
- support
- disruptor
- hybrid

Role is metadata/UI/content aid only:
- filter/sort
- roster balance
- encyclopedia
- team suggestions

Role is not a hard gameplay restriction.

---

## 16. Combat-Stat Boundaries

### P10-D40 — MAG
MAG may scale:
- magic damage
- healing
- shields

when the skill formula chooses.

Percentage/rule-based buffs/debuffs do not automatically need MAG scaling.

### P10-D41 — One Shared DEF
Use one DEF for both physical and magic damage.

No MDEF at P10.

### P10-D42 — SPD Only Controls Turn Order
At P10:
`SPD → determines turn order`

Extra turns/action gauges/tick frequency belong to P13 if ever added.

### P10-D43 — Status Resistance
Use one shared Status Resistance stat.
- affects chance to receive status.
- User selected A (2026-09-28): covers all harmful statuses, including crowd control (stun/sleep/freeze), damage-over-time statuses (poison/burn), and stat reductions (ATK/DEF/SPD). This is a product decision, not a recovered original-game rule.
- Resistance applies to status application, not the direct-damage component of a hit. Resisting poison on a damaging hit does not negate that hit's direct damage. It does not reduce an applied status's tick damage.
- does not reduce status duration.
- no per-status resistance map.
- exact formula/cap/boss rules belong to P11/P13.

### P10-D44 — No Separate Elemental Resistance Stat
Elemental interaction is only through `skill.element vs target.element` chart.
Existing reconstruction elemental `resistances` are legacy fields to rework.

### P10-D45 — No Accuracy/Evasion Core Stats
Hit/miss rules belong to Skill mechanics.

### P10-D46 — Crit Is Not a Core Stat
Crit may later come from:
- Skill
- Equipment
- Buff/Debuff

through P13/P18.

---

## 17. Deferred Ownership

### P11
- exact stat formulas
- Star power bands
- Species stat budgets
- Special Species elevated budgets
- growth-deviation distribution
- growth-deviation effect on final stats
- inheritance coefficients
- diminishing-return inheritance formula and rounding, without a hard cap (D16)
- Status Resistance chance formula

### P13
- element chart/multipliers
- skill formulas
- hit chance rules
- Crit rules
- status duration/stack/refresh
- skill eligibility
- concrete Species Native Skill Pool contents/counts under the accepted per-Species policy
- Other Eligible Skills
- learn/forget UX details

### P16
- exact Plus formula
- fusion costs/material quantities
- detailed transaction validation
- parent snapshot implementation
- restore exploit prevention
- fusion edge cases

### P19/P20
- Formula rarity/drop/source/trade/binding
- Growth Reroll item rarity/source/cost
- storage expansion items
- fusion stone economy
- system mailbox for returned equipment/restored pets (P19 with P16), claim/retention/capacity and binding rules

### Original-game research
- 152-Species roster and Race × Star distribution: decoded and adopted.
- 152 portraits and 760 actor animation clips: extracted with provenance.
- server-only Special fusion rules: still unverified.
- original Formula/source coverage

---

## 18. Migration / Superseded Decisions

### Family
If `Family` duplicates Race, replace conceptually with Race.

### Generation
Numeric lineage generation/depth is removed as gameplay axis.
Plus is the separate +00..+99 progression axis.

### Refinement
Do not automatically rename `Refinement` to Plus.

### Elemental Resistances
Separate elemental resistance stats are removed.

### Status Resistance Map
Per-status maps are replaced by one shared Status Resistance stat.

### Start-Stat Variance
Superseded by individual growth profile.

### Old 10-Skill Design
Superseded by:
- max 6 current permanent active skills
- permanent Inherited Skill Pool

### Old 5★ +99 Build-Change Placeholder
The previous placeholder mechanic “5★ +99 build-change without stat/cap increase” is not a current P10 requirement.

User selected A and corrected the cap rule (2026-09-28): remove the standalone
build-change action, but allow normal Reinforcement at +99 with output +99.
Skill changes and Pet → Egg → growth reroll remain available under common rules.
Pet → Egg preserves Plus. Reinforcement consumes both parents and costs, produces
an Egg, and hatches at Lv1; it does not preserve the main parent's current level.
This supersedes the previous prohibition on Reinforcement at +99 and does not
resolve the separate source-unverified Special fusion Plus outcome.

Current confirmed endgame direction instead includes:
- Special same-star 4★ fusion
- Special same-star 5★ fusion
- 5★ remains current Star ceiling

If build-change is desired later, reopen it as a separate decision.

---

## 19. Remaining implementation gates

The authoritative open register is [P10-readiness.md](P10-readiness.md). Deferred numerical/content work does not reopen accepted decisions. Remaining handoffs:

1. Species Native Skill Pool policy is resolved: content-driven per Species,
   without mandatory equal counts. Concrete skill lists/counts belong to P13.

2. Fusion validation edge cases
   - pet currently in battle
   - quest-bound pet
   - invalid transaction state
   - capacity policies already fixed in D18/D19/D30/D32; P19/P16 implement storage/mail rules

3. Final data-contract boundary between
   - P10 Pet/Species/Egg
   - P11 Stats
   - P13 Skills
   - P16 Fusion
   - P19/P20 Items/Formula

4. Review the decoded 152-Species data/asset package; design later runtime migration after stats/elements/skills are approved.

---

## 20. High-Level Model Summary

Conceptual Species:

```text
Species
├─ id
├─ race_id
├─ element_id
├─ star
├─ species_class
├─ base_stats_at_lv1
├─ growth_baseline_by_stat
├─ primary_role
├─ secondary_role?
└─ native_skill_ids
```

Conceptual Pet:

```text
Pet
├─ species_id
├─ level
├─ xp
├─ plus
├─ gender
├─ growth_profile
├─ inheritance_bonus
├─ current_skill_ids[0..6]
├─ inherited_skill_ids[]
├─ direct_parent_refs
└─ fusion_restoration_metadata?
```

Conceptual Egg:

```text
Egg Item
├─ species_id
├─ star
├─ plus
├─ gender
├─ growth_profile
├─ inheritance_bonus
├─ inherited_skill_ids[]
├─ preserved_current_skill_ids[]   // relevant for Pet → Egg
├─ source_type
├─ direct_parent_refs
└─ immutable_parent_restore_snapshots?  // fusion origin only
```

---

## 21. Core Design Philosophy

- Star gives clear progression structure without fully determining Species strength.
- Species identity matters.
- Special Species may be substantially stronger within the same Star.
- Plus expands level ceiling, not raw stats.
- Training parents matters because current permanent stats affect inheritance.
- Individuality comes from growth potential, not random Lv1 start stats.
- Growth becomes deterministic once the Egg is fixed.
- Egg is the configuration/review stage; hatch is reversible through the approved Pet → Egg item.
- Skill inheritance is player-controlled through parent current-skill choices, not RNG.
- Fusion should create long-term build depth without requiring full genealogy complexity.
- UI should remain compact/readable instead of becoming spreadsheet-like.
