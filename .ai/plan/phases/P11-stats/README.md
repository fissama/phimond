# P11 — Stats design baseline v1

Date: 2026-10-13. **P11 design updated: effective catalog v3 / 160 validated. Prior v2 closure retained as history.**
No runtime stat engine, migration, gameplay simulation harness or Special
operation activation. The owner's last instruction delegates completion; see
F01–F06 for agent-selected decisions versus individually approved answers.

Read in order:
1. [Final specification](P11-final-spec.md): current authority and explicit
   inheritance amendments to Q14.1/3/4 and P10-D14/D16.
2. [Formulas](P11-formulas.md) and [numeric tables](P11-stat-tables.md).
3. [Current 160-Species catalog](P11-species-catalog-160.md), [JSON](P11-species-catalog-160.json) and [role/development reconciliation](P11-roster-160-reconciliation.md). The old 152 catalog is the frozen v2 input.
4. [Verification](P11-verification.md), [readiness](P11-readiness.md),
   [source audit](P11-fusion-source-audit-20261012.md),
   [inheritance review](P11-inheritance-design-audit.md).

The original [owner interview](P11-design-decisions.md) and files named
`*-interview-history.md` are checkpoint history, not current OPEN questions.
[P10 handoff](P11-from-P10-handoff.md) records the inherited contracts and the
scoped final amendments. P10 frozen IDs/recipes/art remain unchanged.

The key final change: accumulate exact training credit, preserve the stronger
lineage per stat once, then derive a diminishing-return bonus. This replaces
the whole-bonus square-root reset that naturally plateaued. Normal Star-up also
preserves lineage. Special fusion remains source-gated. The child still resets
to Lv1 and receives the fresh profile rolled at Egg creation; lower grades can
still offset some inherited gain at the same level, disclosed in preview.

P13 owns skill/Element combat content, P16 transactions/Plus/recipes, P15/P19
real training-time and economy calibration. Formula completion does not certify
runtime correctness or measured player satisfaction. Legacy14 runtime remains
active until a separately authorized versioned implementation/migration.

## Catalog balance review — 2026-10-12

[Review of all152 assignments](P11-catalog-review-20261012.md) confirms numeric
constraints but does **not** approve final species identity/combat balance.
V1 has79 distinct base/growth vectors;104 species share a vector; several source
stat signatures are absent, and Normal5 Wind coverage is empty. Authoring v2 is
recommended within existing bands, with P13 kit/value proof before activation.
No numeric assignments changed in this review. Static design completeness is
not balance approval; see the review for six prioritized findings and evidence.

## Bird priority update — catalog v1.1

[Owner-approved Race direction](P11-race-identity-direction.md): Bird has
strictly higher grown SPD at the same Star/class, role blend, level and grade,
without inheritance/gear/buffs. All21 Bird records now embody this preference
within existing ±5% bounds; proof covers actual pairs and252 template cohorts.
Previous review measurements refer to catalog v1; the seven other Race profiles were subsequently approved and authored in v2;
Element coverage and P13 kit findings are tracked separately below.

## Race/catalog v2 revision

The owner approved the remaining seven Race directions. Catalog v2 authors
all152 Species with budget-conserving Race emphases, explicit Species accents
and adapted gameplay descriptions without absolute superlatives; source quotes
remain archived unchanged.304 numeric layers pass all existing guards, including
Bird priority.137 distinct vectors;27 Species still share stats and require
P13 kit differentiation. The owner approved species_0107 as Wind; Normal5 covers all six Elements; runtime/combat certification remains downstream.

[Design closure report](P11-closure.md) records scope and downstream gates.

## Current extension — 2026-10-13

F10/F11 reconcile P10 authored IDs and P13 v7 directions: 160 stable design IDs,
14 revised role blends, 320 valid stat layers, explicit MP on all records.
No change to growth grades, Star/Special budgets, inheritance or Race formulas.
Use build_effective_catalog.py for the current full catalog; build_species_catalog.py
continues validating the frozen source152 snapshot. Art/runtime and P13 acceptance
remain separate. See reconciliation for registration/delivery dependencies.
