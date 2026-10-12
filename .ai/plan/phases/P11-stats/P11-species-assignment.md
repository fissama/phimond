# Current assignment authority

Completed catalog: [P11-species-catalog.md](P11-species-catalog.md) and
[JSON](P11-species-catalog.json). All152 assignments are authored under delegated
F05; old OPEN/no-assignment wording below is pre-completion planning history.
Current numeric authority is [P11-final-spec.md](P11-final-spec.md).

# P11 — Species assignment contract

Status: **RULES PARTIAL; 152 NUMERIC ASSIGNMENTS OPEN**, 2026-10-12.

## Frozen inputs

Use `data/p10/species.json` and `data/p10/id_registry.json`: 152 canonical IDs,
135 Normal +17 Special (4 Special4★, 13 Special5★). Preserve original source
Race/Star/class/name/art/parent recipe identities. Race does not automatically
multiply stats. Element is an independent Species field.

Review against `data/pets/roster_apk84.json` and P10 roster descriptions as
qualitative identity evidence. The extraction has **55 descriptions empty out
of 152**. A description is not an approved runtime formula or skill assignment;
missing prose cannot be filled by visual/name matching.

## Accepted assignment pipeline

```text
Star/class power budgets (Normal factors Q11.1b and Special4/5 factors Q11.2/Q11.3 locked; Lv1/growth anchors100/2.000 Q11.5/Q11.6 locked; Normal±3%/Special±2% main tolerance locked)
→ role template (fixed primary/secondary blend where applicable)
→ bounded Species modifier
→ final per-Species Lv1 base_stats + six growth_baseline values
```

Reuse P10-D39 initial role vocabulary: `physical_dps`, `magic_dps`, `tank`,
`support`, `disruptor`, `hybrid`. Q10 fixes75/25 Primary/Secondary, or100% Primary if no Secondary. Apply to
Lv1/growth templates and SPD/SR targets before Species modifiers. Q11.7 uses
shared role main shares across Lv1/growth, scaled by each layer target; raw HP
uses10×normalized HP share. Q11.8 approves the six main percentage vectors
in stat tables. Species modifiers remain independent. Auxiliary target values,
final assignments remain open. Q11.9 locks integer final Species base values;
Q8.2 growth baselines have at most three decimals. Exact intermediates and all
final constraints remain required; no automatic rounding seed is selected. Q10.6 permits
independent fixed per-stat Lv1/growth modifier percentages; all constraints
still apply independently to each final layer, without cross-layer compensation.
Q10.2 limits final deviation to±10% main stats/±5% SPD-SR for both layers.
Q10.1 bounds modifiers by relative per-stat deviation from the blended
template. Validate final assigned values after balancing/quantization,
simultaneously with budget/range/primary-signature constraints. Q10.3 locks
DPS/Tank signatures; check base and growth separately. Q10.4f locks Primary Hybrid: ATK≥20%×B, MAG≥20%×B,
ATK+MAG≥50%×B, inclusive and separate for both authored layers. Q10.4e defines Hybrid specifically as dual physical/magic damage;
other functional combinations use Primary/Secondary. Q10.4a defines Support broadly as ally recovery,
protection, buffs or cleansing, without requiring every function or approving
stat thresholds/kit counts. Q10.4b defines Disruptor as control/debuffs that
hinder actions or reduce opponent effectiveness, with no implied SPD minimum.
Q10.4c excludes damage-only poison/burn from establishing Disruptor; an
additional control/impairment beyond HP loss is needed. SR still covers harmful
poison/burn application. P13 owns the actual skills. Q10.5 assigns Primary by
dominant function and Secondary by clear, usable supporting function, based
on stats and planned Native Skill Pool; no skill-count/% quota. P11 records
rationale and P13 cross-checks concrete content. Roles are Species metadata,
not recalculated from current, inherited or NPC-learned Pet skills. Individual
role assignments remain open until reviewed. Q10.4d adds no universal Support bulk or
Disruptor SPD minimum; retain template/budget/modifier/SPD-SR range checks and
document functional rationale for checking against P13 skill content.
Do not constrain owned-Pet inherited totals. Q4/Q5 explicitly extend D39
metadata-only wording to role-driven stat authoring; roles still impose no hard
gameplay restrictions or automatic skill grants. Primary identity must survive blending/modification.
Species base stats are actual fixed Lv1 values. Each Species owns its baseline;
no Race × Star table replaces these fields. Individual deviation scales that
baseline multiplicatively and never changes Species identity.

## Required future assignment record

For each frozen ID, document primary/optional secondary role, Element placement,
six base stats, six growth baselines, normalized budgets/tolerance, source
identity notes, intentional adaptations, role rationale and owner approval.
Link to approved budget/template/normalization versions. Blank-source cases
must explicitly say unverified source identity details; do not imply recovery.

P11 owns stat/role placement and coordinates Element assignment with P13. P13
owns Element chart, native pool contents/counts and skill eligibility. Viability
can only be finalized with that combat content; a raw-budget check is limited.

No JSON content edits are authorized until numerical assignments are approved.
Future additive fields: `element_id`, `role_ids`, `base_stats`,
`growth_baseline`. Do not alter existing fields or activate incomplete content.
Legacy 14→152 migration is a separate later gate. No “closest” name/appearance
mapping or presumed source stat translation.
