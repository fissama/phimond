# P10 — Pet model foundation

Status: **design baseline audited + LOCKED; closure confirmed** (2026-09-30).

**Read [P10-closure.md](P10-closure.md) first** for the canonical exit-gate view (what is locked, what is deferred with owners, what's out of scope).

## Read in this order

1. [Closure report](P10-closure.md): audit verdict + open register + downstream hand-off.
2. [Readiness review](P10-readiness.md): eight named source/dependency gates with explicit owners.
3. [Design decisions](P10-design-decisions.md): accepted behavior, stable D01–D46 references.
4. [Data contract](P10-data-contract.md): fields, lifecycle, operation names and 23 future acceptance scenarios.
5. [Canonical catalog](../../../../data/p10/README.md): frozen IDs, normalized data and compatibility path.
6. [Species roster](P10-roster.md): 152 Vietnamese names/descriptions, source/canonical IDs and assets.

## Evidence and history

- [Discussion review](P10-review.md): rationale, source comparisons and accepted choices.
- [Verification](P10-verification.md): executed checks and limits.
- `evidence/`: unchanged raw metadata/roster/selected-item observations.
- `data/pets/roster_apk84.json`: raw source identity/art export; not runtime-ready.
- `apps/game-client/assets/pets/apk84/`: 152 portraits, 760 clips; paths retain source provenance.

Canonical authoring data: `data/p10/{species,items,special_recipes}.json`.
The existing server still loads legacy catalogs. No stats/Elements/skills,
original-server Special rules or save migration are inferred by normalization.

## Out of P10 scope (separate work)

- **P10 pixel-sprite redraw** (art quality) — see [P10-redraw-plan.md](P10-redraw-plan.md). Owner-approved 2026-09-30, separate peer ownership, not part of design phase delivery.
- **Gameplay code** (numeric formulas, runtime mechanics, save migration) — owned by P11/P13/P16/P19/P20 per master plan.
