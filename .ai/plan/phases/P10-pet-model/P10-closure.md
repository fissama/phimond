# P10 — Design closure report

**Status:** Design baseline **AUDITED + LOCKED** (2026-09-28 final audit; 2026-09-30 closure review).
**Verdict:** P10 design is complete A→Z. Gameplay implementation is **out of P10 scope** per master plan; it belongs to P11 (stats), P13 (skills), P16 (fusion persistence), P19/P20 (items/formulas).

This document is the canonical entry point for downstream phases. It cross-references the already-existing artifacts; it does not duplicate them.

## 1. What "P10 design complete" means

P10 covers the **conceptual model and content vocabulary** of Pet / Species / Egg / Fusion / Growth / Inheritance / Skills, plus the 152-species baseline roster and canonical authoring catalog. Numeric formulas, runtime code, save migration, and Special server rules are explicitly NOT P10's job.

P10 is closed at design level when:
- Taxonomy, vocabulary, and contract vocabulary are all locked.
- 152 species identity/art package is audited.
- Open items have **explicit owners and gates**, not loose notes.
- Reviewers (master, user, code) have signed off on the audit.
- Acceptance scenarios for later phases are written so P11/P13/P16 can target them.

All of the above are true.

## 2. P10 deliverables (committed and stable)

| Artifact | Path | Status | Owner of change |
|---|---|---|---|
| 152-species roster | `P10-roster.md` (242 lines) | ✅ Locked 2026-09-28 | P10 |
| 46 design decisions D01–D46 | `P10-design-decisions.md` (844 lines) | ✅ Locked 2026-09-28 | P10 |
| Data contract + 23 acceptance scenarios | `P10-data-contract.md` (139 lines) | ✅ Locked 2026-09-28 | P10 |
| Review rationale + source comparison | `P10-review.md` (200 lines) | ✅ Locked | P10 |
| Open register (8 gates) | `P10-readiness.md` | ✅ Locked 2026-09-28 | P10 + downstream owners |
| Verification (catalog tests, asset checks, build) | `P10-verification.md` | ✅ All checks PASS 2026-09-28 | P10 |
| Canonical authoring IDs | `data/p10/id_registry.json`, `data/p10/species.json`, `data/p10/items.json`, `data/p10/special_recipes.json` | ✅ Frozen | P10 |
| Catalog tooling + 9 unit tests | `tools/content/p10_catalog.py` + `test_p10_catalog.py` | ✅ PASS | P10 |
| Asset validation tool | `tools/assets/check_p10_assets.gd` | ✅ PASS | P10 |
| Raw source extraction | `data/pets/roster_apk84.json` + `apps/game-client/assets/pets/apk84/` (152 portraits, 760 clips, 1,241 frames) | ✅ Imported with provenance | P10 |
| Project glossary entries for Pet/Species/etc. | `.ai/GLOSSARY.md` | ✅ Locked | P10 |
| Active-development summary | `.ai/ACTIVE.md` | ✅ Updated | P10 |

## 3. P10 vocabulary locked (downstream contract)

| Concept | Locked form | Source D# |
|---|---|---|
| Race taxonomy | 8 races (Insect, Spirit, Bird, Demon, Beast, Plant, Undead, Dragon); Race ≠ Element; Race grants no stat bonus | D01–D03 |
| Species classification | normal vs Special; Special is content/domain, not extra Star | D04 |
| Species roster | 152 (135 normal + 17 Special); race × star distribution adopted | D05 |
| Capture tier | 1★ wild capture creates Egg | D06 |
| Base level caps | 1★60 / 2★70 / 3★80 / 4★90 / 5★100 | D07 |
| Star-up / Plus | Star-up = next-Star; Plus = +00..+99 reinforcement ceiling | D08 |
| Reinforcement | Allowed at +99 with output +99; consumes both parents, hatches Lv1 | D09, D27 |
| Special fusion | Same-Star only; 4★ and 5★ only; **DISABLED until O01 verified** | D10 |
| Core stats | hp, atk, mag, def, spd, status_resistance; mp separate | D11 |
| Lv1 base stats + species growth | Species owns base + growth baseline | D12, D13 |
| Inheritance input | `inheritance_bonus` only (permanent total = grown_stat + inheritance_bonus) | D14 |
| Inheritance is fixed | Set at Egg creation; leveling/reroll do not change it | D15 |
| Inheritance diminishing | Diminishing returns, no hard cap; +99 reinforcement inherits main parent floor | D16 |
| Egg is an item | Egg = item with bound Species + growth + inherited pool | D17 |
| Hatch rules | Lv1, growth profile resolved | D18 |
| Farm storage | Capacity policies fixed; P19/P16 own runtime | D19 |
| Growth reroll | Allowed after Pet → Egg; per egg | D20 |
| Stat UI | Base/Attributes + Overview tabs; display `186 +12` style | D21, D22 |
| Formula knowledge | Account-owned set of species IDs; blueprint unlocks target knowledge (P20 detail) | D23 |
| Three Farm NPCs | trainer / ranch_keeper / arena_master roles | D24 |
| Fusion stones | Material-item based, no separate currency | D25 |
| Normal Star-up | Single-step at Star-up NPC | D26 |
| Reinforcement | Consume both parents; produce Egg; Lv1 hatch | D27 |
| Direct lineage only | Parent snapshot references exact originals | D28 |
| Fusion restoration snapshot | Intrinsic boundary explicit; current owner/equipment separate | D29 |
| Split fusion egg | Egg → two parents; consume Egg | D30 |
| Pet → Egg | Reversible; preserves Plus; consumes Pet | D31 |
| Equipment on fusion/Pet→Egg | Auto-unequip; overflow to mailbox | D32 |
| Split after previous hatch | Each split creates fresh pair, no history cross-link | D33 |
| Gender | Metadata only; no gameplay impact | D34 |
| Max 6 current skills | Permanent current slots; basic attack separate | D35 |
| Inherited skill pool | Per-Species pool from parents | D36 |
| Only current skills propagate | Inherited pool seeded from current; not full pool | D37 |
| Skill NPC pool | NPC offers per-Species available pool | D38 |
| Role metadata | Primary + optional secondary role per Species | D39 |
| Combat-stat boundaries | MAG/DEF/SPD/SR/ELE/ACC/CRIT rules per D40–D46 | D40–D46 |

## 4. Open register O01–O08 (each has explicit owner)

These are **NOT pending P10 design**. They are explicitly handed off:

| ID | Unresolved content | Owner | Phase that resolves | P10 obligation |
|---|---|---|---|---|
| **O01** | Special fusion Plus, costs, success rate | Original-game research → P16 | P16 | None; 17 recipes disabled in catalog until O01 closes |
| **O02** | Whether Special species can Reinforce | Original-game research → P16/P20 | P16/P20 | None |
| **O03** | First-hatch HP/MP init, re-hatch semantics | P11/P13/P16 | P11 first | Re-hatch full recalc MP locked; rest to P11 |
| **O04** | Numeric growth curves, inheritance formulas, +99 floor | P11/P16/P15 | P11 first | Diminishing-returns shape locked; concrete formula to P11 |
| **O05** | Element / role / growth config for 152 species | P11/P13 | P11 first | Per-Species element/role NOT invented by P10 |
| **O06** | Egg/Pet instance-ID persistence | P16 implementation plan | P16 | None |
| **O07** | Mail retention/capacity | P19/P08/P16 | P19 first | Overflow-to-mailbox contract locked |
| **O08** | Legacy 14→152 species migration | P11/P13/P16 implementation plan | P11/P13/P16 | Migration is additive; no implicit auto-rename |

P10 does not invent content to close these gates. P11/P13/P16 owners will accept or defer them.

## 5. Out of P10 scope (separate ongoing work)

### 5.1 P10 pixel-sprite redraw contract
- Plan: `.ai/plan/phases/P10-pet-model/P10-redraw-plan.md` (owner-approved 2026-09-30)
- Status: in progress under separate peer ownership (Lead / Tooling-client Peer / Art Peer / Reviewer).
- Owner: explicit roles assigned in the plan; this is **not** part of P10 design phase delivery.
- P10 design is not blocked by redraw work.

### 5.2 Legacy runtime catalog
- Legacy `data/pets/species.json` (14 species) still loaded by the server.
- P10 wrote `data/p10/` (152 species) for new content.
- Migration `14→152` is **O08**, owned by P11/P13/P16 implementation plans.
- Server still builds, runs, and serves gameplay with legacy catalog; P10 catalog is dormant.

### 5.3 Gameplay code (NOT P10's job)
Per master plan: "Master plan chỉ ghi phạm vi/flow/decision/gate; chưa tạo implementation plan, công thức số hoặc code trong lượt này."

- Numeric formulas → P11
- Element chart → P13
- Skill mechanics → P13
- Plus formula → P16
- Save migration → P11/P13/P16

## 6. Verification chain (already run)

| Check | Result |
|---|---|
| `python3 tools/content/p10_catalog.py` | PASS (152 species, 8 selected items, 17 disabled recipes; complete unique IDs, references, matrix, asset hashes/paths) |
| `python3 -m unittest discover -s tools/content -p 'test_p10_catalog.py' -v` | PASS (9 tests; corruption cases: duplicate IDs, JSON keys, missing mapping, localized ID, wrong Star/parent, missing asset, wrong source hash) |
| `tools/assets/check_p10_assets.gd` | PASS (152 portraits/resources, 760 clips, 1,241 timed frames) |
| `sh tools/check.sh` | Exit 0 (Go race/vet cached, 5 client checks, 7 harness tests, 3 web tests, TypeScript) |
| `go build -o /tmp/phimond-server ./cmd/server` | Exit 0 |
| Local Markdown link check (P10 docs) | PASS (324 relative links resolve) |
| `git diff --check` | PASS |
| Visual spot check (6 species, alias + race-surprising cases) | Reviewed |

## 7. Ready-to-hand-off package for downstream phases

For P11 specifically, the inputs are:

| Input P11 needs | Source | Locked? |
|---|---|---|
| Species glossary (152 IDs) | `data/p10/species.json` + `id_registry.json` | ✅ |
| 8-race taxonomy + Star distribution | `P10-design-decisions.md` D02/D05 | ✅ |
| Stat keys (hp/atk/mag/def/spd/status_resistance) | `P10-design-decisions.md` D11 | ✅ |
| MP as separate resource | `P10-design-decisions.md` D11 | ✅ |
| Growth option A (`grown_stat + inheritance_bonus`) | `P10-design-decisions.md` D14 | ✅ |
| Inheritance diminishing (no hard cap) | D16 | ✅ |
| Reinforcement +99 inheritance floor (main parent prior bonus) | D27 / Accepted Option A | ✅ |
| Operation names (`star_up`, `reinforcement`, `special_fusion`, `pet_reversion`, `hatch`, `split`, `growth_reroll`, `mail_claim`) | `P10-data-contract.md` | ✅ |
| Re-hatch MP full recalc | ACTIVE.md | ✅ |
| Open gate O03 (P11-owned) | `P10-readiness.md` | ✅ |
| Open gate O04 (P11-owned) | `P10-readiness.md` | ✅ |
| Open gate O05 (P11/P13-owned, NOT YET CONFIG) | `P10-readiness.md` | ⚠️ P11 must add per-Species config; P10 didn't invent |

For P13, P16, P19/P20 — same pattern. All have explicit owner tag.

## 8. Exit gate for P10 design phase

P10 design is **closed at design level** when:

- ✅ Taxonomy / classification / Star / Plus / Egg / fusion / growth / inheritance / skill / role / combat-stat-boundary vocabulary all locked (D01–D46).
- ✅ 152-species baseline adopted with provenance.
- ✅ 8 open gates documented with explicit owners.
- ✅ Catalog tooling + asset validation + canonical checks all PASS.
- ✅ Glossary + ACTIVE.md + design-decisions cross-reference each other.
- ✅ Review (master + code) signed off.

This document is the audit closure. P11/P13/P16 can begin their work.

## 9. P11 entry point

P11 owner should:

1. Read `.ai/plan/phases/P11-stats/README.md` (scaffold).
2. Read `.ai/plan/phases/P11-stats/P11-from-P10-handoff.md` (concrete inputs from P10).
3. Decide per-Species growth curves / inheritance coefficients / first-hatch HP/MP init — these are P11's content, not P10's.
4. Use canonical IDs from `data/p10/species.json`; do not introduce new IDs.
5. Resolve O03 and O04 explicitly with user; mark O05 ownership split with P13.

P10 does not constrain P11's numerical choices; it only sets vocabulary and inheritance shape.

---

*Closure review: 2026-09-30. P10 design locked. Out-of-scope ongoing work (redraw, legacy runtime, gameplay code) tagged and tracked separately.*
