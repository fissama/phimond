# P10 review — evidence and remaining decisions

Status: ongoing debate. Accepted points below are user decisions from 2026-09-28;
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

## Current debate: stat terms and inheritance (D14/D21/D22)

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

### Proposed precise contract — awaiting user decision

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

Display options to decide:

1. Attributes `HP 186 +12` with explicit labels/tooltip **grown + inherited**;
   Overview `HP 223` with equipment. Compact and closest to the supplied spec.
2. Attributes `HP 198` with breakdown `186 grown +12 inherited`; Overview `223`.
   Shows the usable permanent total immediately but uses more UI space.

Recommendation: option 1 if compactness is the priority, with a readily available
total of 198 and clear labels; never call 186 the "permanent total".

## Next debate: Special fusion, source rules vs missing server logic

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

## Remaining sequence

1. Stat definitions and display (current question).
2. Special same-Star contract and Plus; original structure versus server unknowns.
3. MP's design boundary and reroll consequences, without committing P11 formulas.
4. Basic attack versus six skill slots; first hatch versus re-hatch.
5. Race/Element and eligibility; single Status Resistance tradeoffs.
6. Restore capacity/ownership/equipment; conflicts with one-way parent retirement.
7. Endgame +99: reconcile the supplied draft's removal of standalone build-change
   with the master's older requirement. Do not silently resolve that remaining conflict.

Only explicit decisions are incorporated into the active specification. P10 is
not design-ready until these boundaries and the source-unknown policy are reviewed.
