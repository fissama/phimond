# P10 — Pet model foundation

Status: **design baseline audited; full gameplay not delivered** (2026-09-28).

## Read in this order

1. [Readiness review](P10-readiness.md): verdict, fixed inconsistencies, eight named source/dependency gates.
2. [Design decisions](P10-design-decisions.md): accepted behavior, stable D01–D46 references.
3. [Data contract](P10-data-contract.md): fields, lifecycle, operation names and 23 future acceptance scenarios.
4. [Canonical catalog](../../../../data/p10/README.md): frozen IDs, normalized data and compatibility path.
5. [Species roster](P10-roster.md): 152 Vietnamese names/descriptions, source/canonical IDs and assets.

## Evidence and history

- [Discussion review](P10-review.md): rationale, source comparisons and accepted choices.
- [Verification](P10-verification.md): executed checks and limits.
- `evidence/`: unchanged raw metadata/roster/selected-item observations.
- `data/pets/roster_apk84.json`: raw source identity/art export; not runtime-ready.
- `apps/game-client/assets/pets/apk84/`: 152 portraits, 760 clips; paths retain source provenance.

Canonical authoring data: `data/p10/{species,items,special_recipes}.json`.
The existing server still loads legacy catalogs. No stats/Elements/skills,
original-server Special rules or save migration are inferred by normalization.
