# P11 — Concrete inputs from P10

This document is the **handoff package** P11 owner needs before writing any design decision. P11 inherits only what P10 locked; everything else is P11's content.

## Locked vocabulary P11 must respect

| Concept | Locked form | Source |
|---|---|---|
| Stats | `hp`, `atk`, `mag`, `def`, `spd`, `status_resistance`; `mp` separate | D11 |
| Stat display | `grown_stat + inheritance_bonus` (e.g. `186 +12`); permanent total 198 | D14 / ACTIVE.md |
| Inheritance shape | Diminishing returns, no hard cap | D16 |
| Reinforcement +99 floor | Each inherited stat bonus ≥ main parent's prior bonus, including at +99 | D27 / ACTIVE.md |
| Re-hatch MP | Full recalc, set current MP to new max; no carry-over | ACTIVE.md |
| Level cap | 1★60 / 2★70 / 3★80 / 4★90 / 5★100 | D07 |
| Re-hatch skills | Lv1 with preserved learned skills (option A); use conditions still apply | ACTIVE.md |
| Status Resistance scope | One shared stat; affects application chance only (control, poison/burn, stat reductions); not duration, not direct damage | D43 / ACTIVE.md |
| Races | 8 (Insect, Spirit, Bird, Demon, Beast, Plant, Undead, Dragon) | D02 |
| Species roster | 152 IDs frozen in `data/p10/species.json` | D05 |

## Operation names (don't invent new ones)

```
star_up            reinforcement       special_fusion     pet_reversion
hatch              split               growth_reroll      mail_claim
```

## Operation semantics P11 needs

| Op | P10 contract | P11 owns |
|---|---|---|
| `star_up` | Star-up NPC consumes Pet + materials, produces higher-Star Egg; Lv1 hatch | none — P11 doesn't need to design this |
| `reinforcement` | Consumes both parents, produces Egg; Lv1 hatch; +99 inheritance floor | yes — P11 designs inheritance math |
| `hatch` | Lv1, growth profile resolved | yes — P11 designs HP/MP init + per-stat growth realization |
| `growth_reroll` | Allowed after `pet_reversion`; per-egg | yes — P11 designs deviation distribution |
| `split` | Egg → two parents, exact snapshot restore | no (P16 owns) |
| `pet_reversion` | Pet → Egg; preserves Plus; consumes Pet | yes (partial) — P11 designs HP/MP carry-over |
| `special_fusion` | DISABLED until O01 closed | no |
| `mail_claim` | Overflow to mailbox | no (P19) |

## Open gates P11 must close

### O03 — First-hatch HP/MP init + re-hatch semantics
**P10 locked:** Re-hatch full recalc MP at Lv1, set current MP to new max.
**P11 must design:**
- First-hatch HP formula (probably `species.base_stats.hp × race_factor × star_factor`).
- First-hatch MP formula (similar).
- Growth profile realization: at each level-up, draw individual growth deviation; sum into `grown_stat`.
- Effect of `growth_reroll` on existing growth profile.
- Per-stat growth rates (`hp`, `atk`, …) — by race × star, not per species.

### O04 — Numeric growth curves, inheritance formulas, +99 floor
**P10 locked:** Diminishing returns, no hard cap; +99 reinforcement has main-parent floor.
**P11 must design:**
- Concrete diminishing-returns curve (e.g. `floor(parent.bonus × k^n)` where `k` is a fixed rate).
- Per-stat coefficients (6 stats × some scaling).
- Rounding policy (integer vs float; truncation; floor/ceil/round-half-up).
- Reinforcement +99 inheritance: floor = main parent's prior bonus per stat.
- Mixed-Plus pairs (e.g. main parent +30, secondary +50): how inheritance combines.
- Status Resistance chance formula.

### O05 — Per-species Element + role + growth_baseline + base_stats + native skill pool count
**P10 locked:** Per-Species counts may differ; P11 designs content by role/identity; six current-skill slots unchanged.
**P11 must design:**
- `role_ids` per species (primary + optional secondary).
- `base_stats` per species at Lv1 (6 stats).
- `growth_baseline` per species per stat.
- `element_id` per species — **P11 owns placement decision, P13 owns the chart** (P11 says "species X is element Y"; P13 says "Y > Z does 2x, Z > Y does 0.5x").
- Update `data/p10/species.json` with these fields for all 152 species.

### O08 — Legacy 14→152 migration plan (P11 contributes with P13/P16)
**P11 must design:**
- For each of the 14 legacy species, explicit canonical mapping → closest 152 entry.
- Per-stat scaling factor (legacy stats → canonical base_stats).
- Pet save format version bump.
- Migration requires copied-save tests, backups, version gates, rollback plan.

## Numerical sanity tests P11 should plan

Per `P10-readiness.md > Verification for this review` and `P10-closure.md §6`:

- Long-sequence growth: 50 generations of cross-family fusion; verify no runaway stats.
- Weak-donor / strong-donor edge cases: `atk 10` vs `atk 200` parent → child inherits within bounds.
- +99 floor edge: main parent +99, secondary +00; child inheritance must be ≥ +99 per stat.
- Mixed-Plus: cross-check both parents' Plus ratings.
- Star-up interaction: does +99 pet survive Star-up (1★→2★) without losing inheritance floor?
- Reinforcement cooldown / cost bounds (if cost system touches P11).

## Numerical ownership matrix (P11 vs others)

| Numerical aspect | Owner | Notes |
|---|---|---|
| Growth curve shape | P11 | diminishing returns locked |
| Per-stat coefficients | P11 | — |
| Inheritance formula | P11 | — |
| Reinforcement +99 floor | P11 | main parent bonus per stat |
| Status Resistance chance | P11 | application only, not duration |
| Per-species element placement | P11 (with P13) | P13 owns chart |
| Per-species role / base_stats / growth_baseline | P11 | — |
| Element chart multipliers | P13 | — |
| Skill damage formulas | P13 | — |
| Hit chance / crit | P13 | — |
| Plus formula | P16 | reinforcement specifics |
| Fusion cost / material quantity | P16 | — |
| Capture success rate | P19 | — |
| Formula rarity / drop | P19/P20 | — |
| Re-hatch MP semantics | P11 | locked in P10 |
| Lv1 base stats per species | P11 | — |
| Growth profile distribution | P11 | — |

## Catalog format P11 should produce

Update `data/p10/species.json` per species with:

```jsonc
{
  "id": "species_xxxx",
  "display_name": "...",
  "description": "...",
  "race_id": "beast",
  "star": 3,
  "species_class": "normal",
  "assets": { ... },
  "source": { ... },
  // NEW (P11):
  "element_id": "fire",
  "role_ids": ["physical_attacker"],
  "base_stats": {
    "hp": 60, "atk": 22, "mag": 12, "def": 18, "spd": 14, "status_resistance": 8
  },
  "growth_baseline": {
    "hp": 6, "atk": 2.2, "mag": 1.2, "def": 1.8, "spd": 1.4, "status_resistance": 0.8
  },
  // P13 owns:
  "native_skill_ids": []
}
```

Do NOT modify any field already present in `data/p10/species.json` without explicit user approval. New fields are additive.

## What NOT to do

- Don't change P10 design decisions (D01–D46) — reopen them explicitly if you must.
- Don't use legacy `species.json` for new content.
- Don't introduce new IDs.
- Don't merge APK prose into mechanics.
- Don't commit numeric formulas without a sanity-test log.

## Begin checklist (P11 owner)

- [ ] Read P10-closure.md and P10-design-decisions.md end-to-end.
- [ ] Decide numerical ownership split with P13 (who places elements, who defines chart).
- [ ] Write `P11-S01-spec.md` (scope + acceptance criteria) following project sprint template.
- [ ] Write `P11-design-decisions.md` with concrete formulas, formulas table, sanity-test expectations.
- [ ] Build a small simulation harness (separate from load harness) for sanity tests before committing.
- [ ] Update `data/p10/species.json` additively per accepted content.
- [ ] Hand off to P13 with explicit list of "P11 placed X as element Y; P13 defines Y vs Z".
- [ ] Hand off to P16 with explicit list of "+99 reinforcement floor = main parent prior bonus per stat; P16 implements".
- [ ] Update `.ai/ACTIVE.md > P11 closed` when done.
- [ ] Run `sh tools/check.sh` before commit.
