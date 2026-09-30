# P11 — Stats system: design scaffold

Status: **NOT STARTED**. P11 owner to fill in.

## What P11 owns (per master plan)

> P11 — Stat system: growth formulas, Star power bands, species stat budgets, special species elevated budgets, growth-deviation distribution and effect on final stats, inheritance coefficients, diminishing-return inheritance formula and rounding without a hard cap (D16), Status Resistance chance formula.

In short: P11 fills in the **numeric content** that P10 left as vocabulary only.

## Required reading order (before designing)

1. **`.ai/plan/phases/P10-pet-model/P10-closure.md`** — the canonical P10 design exit doc.
2. **`.ai/plan/phases/P10-pet-model/P10-design-decisions.md`** — every D-number is a vocabulary constraint.
3. **`.ai/plan/phases/P10-pet-model/P10-data-contract.md`** — 23 acceptance scenarios + canonical field names.
4. **`.ai/plan/phases/P10-pet-model/P10-readiness.md`** — O03 (P11-owned), O04 (P11-owned), O05 (P11+P13-owned).
5. **`data/p10/species.json`** + **`data/p10/id_registry.json`** — frozen IDs to design against.
6. **`.ai/GLOSSARY.md`** — project-specific terms (Pet / Species / Grown stat / Inheritance bonus / Permanent total / +99 / etc.).
7. **`.ai/plan/PHIMOND_MASTER_SPEC_PLAN.md` §5** — for master ordering (P11 depends on P10; P13/P19/P02/P14 depend on P11).
8. **`P11-from-P10-handoff.md`** (this folder) — concrete inputs extracted from P10.

## P11 deliverables (when complete)

- `P11-design-decisions.md` — numeric content decisions, with explicit user sign-off.
- `P11-formulas.md` — growth curve, inheritance math, +99 reinforcement floor, Status Resistance chance.
- `P11-stat-tables.md` — per (race × star × role) baseline budgets and growth-deviation ranges.
- `P11-species-assignment.md` — per-species element + role + base_stats + growth_baseline (resolves O05 with P13).
- `P11-readiness.md` — open gates passed downstream (P13 needs element chart, P16 needs Plus formula).
- `P11-verification.md` — numerical sanity tests: long-sequence growth, weak/strong donors, +99 floor edge cases.
- Update `data/p10/species.json` with `element_id`, `base_stats`, `growth_baseline`, `role_ids` per species.

## Open gates P11 must close

| ID | What | Notes |
|---|---|---|
| **O03** (P11/P13/P16) | First-hatch HP/MP init; re-hatch semantics | Re-hatch full recalc MP locked in P10; rest is P11 |
| **O04** (P11/P16/P15) | Numeric growth curves, inheritance gains, precision/rounding, +99 floor, mixed-Plus pairs | No hard cap, diminishing gain, reinforcement floor all locked |
| **O05** (P11/P13) | Element / role / growth configuration for 152 species | P11 owns stat/role side; P13 owns Element chart |
| **O08** (P11/P13/P16) | Legacy 14→152 species migration plan | Migration is additive; no name/appearance matching |

## Out of P11 scope (handed off)

- Element chart (multipliers, advantage matrix) → **P13**.
- Skill formulas / hit chance / crit / status duration / skill eligibility / native pool contents → **P13**.
- Special fusion Plus / costs / success rate → **P16**.
- Detailed transaction validation, parent snapshot implementation → **P16**.
- Formula rarity/drop/source/trade/binding → **P19/P20**.
- Mailbox behavior for equipment overflow → **P19**.

## Don't do

- Don't introduce new canonical species IDs; reuse frozen ones in `data/p10/`.
- Don't migrate legacy 14→152 silently; require copied-save tests + version gates + rollback.
- Don't infer stats from source descriptions (APK prose) — those are not approved mechanics.
- Don't auto-rename `Refinement` to `Plus` or `Family` to `Race` in legacy catalog.
- Don't change P10 vocabulary (D-numbers) without reopening P10 explicitly.

## Begin

Owner of this phase creates `P11-implementation-plan.md` (beads) like P00-continuation-beads and `P11-S01-spec.md` from the project sprint template before writing design decisions.
