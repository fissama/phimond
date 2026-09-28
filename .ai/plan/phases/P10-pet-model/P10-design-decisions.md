# P10 — Pet Model Foundation: Design Decisions

**Baseline date:** 2026-09-28

**Status:** Repository review in progress; P10 is not closed.

**Purpose:** Lock the semantics of Pet / Species / Egg / Fusion / Growth / Inheritance / Skills so P11, P13, P16, P19 and P20 can design their detailed formulas and systems without re-interpreting P10 decisions.

> Imported from the user's `P10 Design Decisions.md`, then updated with explicit decisions confirmed on 2026-09-28. Sections marked pending remain discussion proposals. APK observations establish source content; unobserved server rules are not inferred from asset names. Numeric formulas remain owned by their later phase.

Confirmed during repository review: use the original 152-species roster and distribution; MP is a resource owned by P11; growth reroll is allowed after Pet → Egg; use APK-defined Special species/parent pairs/materials; basic attack is available with zero learned skills; Race and Element are independent and Status Resistance is one shared stat. Stat terminology/display (D14/D21/D22) is pending detailed review.

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
Canonical identity/art catalog: `data/pets/roster_apk84.json`. Full list and source notes: [P10-roster.md](P10-roster.md). Preserve source IDs, names, Race, Star, Special classification and assets. Runtime stat/element/skill configuration and migration are later work; the 14-species legacy catalog is not historical source truth.

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
- Original-game generation semantics correspond to this Plus system.
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
- +99 cannot be Reinforced further.

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
- Same-Star Special recipes are distinct from normal N→N+1 Star-up. Formula ownership and the common fusion flow must support both recipe kinds.
- Special 4★/5★ may be substantially stronger than normal Species at the same Star.
- Special Species can be Reinforced normally.
- Reinforcement preserves Special Species identity.
- Special Formula constraints are additive to common validation.
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
**Terminology review pending:** "current total permanent stats" includes the parent's fixed inheritance exactly once. D21/D22 wording must distinguish the grown component from the total before approval; see [P10-review.md](P10-review.md).

Both Star-up and Reinforcement use current total permanent stats of both parents as inheritance inputs.

Correct concept:
`child.inheritance = f(parentA.current_permanent_stats, parentB.current_permanent_stats)`

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

### P10-D16 — Inheritance Needs Cap / Diminishing Return
P11/P16 must design cap/soft-cap/diminishing return to:
- prevent infinite multi-generation power inflation.
- avoid investment becoming worthless too early.
- keep late investment meaningful near the cap.
- keep pets inside intended power budgets.

Exact formula is not part of P10.

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
**Pending clarification:** the expression below must be read as the component before inheritance plus the fixed inheritance bonus, not a total that already includes the bonus. Exact player-facing labels are still being debated.

Do not show raw growth-deviation percentages.

Display:
`current permanent stat + fixed inheritance contribution`

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

### P10-D22 — Overview Tab
**Pending clarification:** `permanent_stat` in this section means the complete permanent total including inheritance exactly once; it must not be confused with the first number shown in D21.

Overview shows final current stats with equipment applied.

Concept:
`overview_stat = permanent_stat + equipment_bonus`

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
- Special Formula may add exact parent/species constraints.
- both parents are consumed.
- result is Egg Item.
- result Species/Race/Element/Star come from target Species.
- Plus resets to +00.

---

## 11. Reinforcement Rules

### P10-D27 — Reinforcement
- Main and donor are same Star.
- Donor may be any Species/Race/Element if common validation passes.
- Formula of exact main `species + star` must be unlocked.
- Main identity is preserved: Species/Race/Element/Star.
- Both pets are consumed.
- Result is Egg → hatch Lv1.
- Resulting Plus uses both parents' Plus values under P16 formula.
- New inheritance uses both parents' current permanent stats.
- +99 cannot Reinforce.

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

Snapshot must allow exact restore of both parents to their state immediately before fusion.

### P10-D30 — Split Fusion Egg
Split Item:
- works only while object is Egg.
- deletes/consumes child Egg.
- restores exact Parent A and Parent B.
- does not refund Gold.
- does not refund Ascension/Reinforcement Stone or material costs.
- child growth rerolls do not mutate parent restoration snapshots.

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

Do not reroll growth or inheritance.
This describes conversion itself. Once converted, the player may explicitly consume a growth-reroll item as allowed by D20. Re-hatch preserves current learned skills (unlike a newly created fusion/capture Egg) and does not reroll inheritance.

### P10-D32 — Equipment Handling on Pet → Egg
Before conversion:
- auto-unequip all equipment.
- return equipment to inventory.
- if inventory cannot receive it, fail entire transaction.
- equipment is never stored in Egg payload.

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
- no RNG chooses inherited skills.
- pool is stored permanently on Egg/Pet.
- pool may contain more than 6.
- first hatch of a newly created fusion/capture Egg starts with 0/6 current skills; basic attack remains available.
- re-hatch after Pet → Egg preserves its current skills under D31.

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
- exact Native Skill Pool size remains open.

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
- inheritance cap/soft-cap/diminishing return
- Status Resistance chance formula

### P13
- element chart/multipliers
- skill formulas
- hit chance rules
- Crit rules
- status duration/stack/refresh
- skill eligibility
- Species Native Skill Pool size
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

Current confirmed endgame direction instead includes:
- Special same-star 4★ fusion
- Special same-star 5★ fusion
- 5★ remains current Star ceiling

If build-change is desired later, reopen it as a separate decision.

---

## 19. Next P10 Review Topics

Before marking P10 design-ready, useful remaining review topics:

1. Species Native Skill Pool size
   - hard cap
   - recommended range
   - fully content-driven

2. Fusion validation edge cases
   - pet currently in battle
   - quest-bound pet
   - invalid transaction state
   - inventory/storage capacity during restore

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
├─ race
├─ element
├─ star
├─ species_class
├─ base_stats_at_lv1
├─ growth_baseline_by_stat
├─ primary_role
├─ secondary_role?
└─ native_skill_pool
```

Conceptual Pet:

```text
Pet
├─ species_id
├─ level
├─ xp
├─ plus
├─ gender
├─ individual_growth_profile
├─ fixed_inheritance_by_stat
├─ current_skills[0..6]
├─ inherited_skill_pool[]
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
├─ individual_growth_profile
├─ fixed_inheritance_by_stat
├─ inherited_skill_pool[]
├─ preserved_current_skills[]   // relevant for Pet → Egg
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
- Egg is the configuration/review stage before permanent hatch.
- Skill inheritance is player-controlled through parent current-skill choices, not RNG.
- Fusion should create long-term build depth without requiring full genealogy complexity.
- UI should remain compact/readable instead of becoming spreadsheet-like.
