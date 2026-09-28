# P10 authoring catalogs

Canonical IDs for new P10 development. **Not loaded by the current server.**
Names/descriptions are Vietnamese localization values; never use them as keys.

| File | Purpose |
|---|---|
| `id_registry.json` | Frozen bijection from APK IDs to canonical species/item/recipe IDs |
| `species.json` | 152 species identities, Race/Star/class, localized text and source asset links |
| `items.json` | 8 selected P10-related source item references; not the full APK item catalog |
| `special_recipes.json` | 17 exact parent pairs using canonical foreign keys; disabled pending source rules |

## ID policy

- JSON fields/enums: ASCII English `snake_case`.
- Species: `species_0001`…`species_0152`. IDs are opaque, allocated once in the
  frozen registry; suffix is not a gameplay order, race, star or power ranking.
- Items with established meaning use English function IDs, e.g.
  `item_special_fusion_s4`. `item_source_*` records are source references whose
  gameplay adoption is **not approved**. An English ID does not approve an effect.
- Recipes: `recipe_special_0001`…`recipe_special_0017`.
- Do not regenerate IDs from names, sort order or translated text. Append new
  registry entries after review; never recycle deleted IDs.
- Race IDs stay `insect`, `spirit`, `bird`, `demon`, `beast`, `plant`, `undead`,
  `dragon`. Skill/Element IDs are not invented before P13 content is approved.
- New dynamic instance IDs (`pet_id`, `egg_id`, `item_instance_id`, `mail_id`)
  are server-assigned opaque IDs, separate from these catalog IDs. Their storage
  format belongs to the implementation plan.

## Text, source and assets

`display_name.vi` and `description.vi` are NFC-normalized Unicode. Descriptions
are reference flavor text, **not executable stat/skill/element rules**.
Original strings and IDs remain unchanged in `data/pets/roster_apk84.json` and
`.ai/plan/phases/P10-pet-model/evidence/`.

`source.species_id` / `source.item_id` preserve exact APK IDs. APK `IDItem` is
recorded as `source.item_group_id`; it is not a unique item key (e.g. several
items share `VatBau`). Asset folders retain source IDs for provenance. Consumers
must resolve the `assets` object, never construct paths from canonical IDs.

`element_id`, numeric stats and native skills are omitted and listed in
`unresolved_fields`. Missing means unresolved, not neutral/zero/empty gameplay
content. Special recipes have `enabled: false`; quantity `null` means unknown,
not zero/free. Source-only items must not appear in the shop or grant effects.
No formula-item catalog or generic runtime recipes are created by this import.

## Regenerate / verify

```sh
rtk proxy python3 tools/content/p10_catalog.py --write
rtk proxy python3 tools/content/p10_catalog.py
```

The raw APK importer may be rerun first. It does not overwrite this registry.
The normalized catalogs are deterministic derivatives; edit source decisions or
registry intentionally, then regenerate. Check validates coverage, uniqueness,
source hash, exact Race × Star distribution, parents, material references,
asset hashes/paths, and generated-file drift. Uses Python standard library only.

## Compatibility and rollback

Current readers still load `data/pets/species.json`, `data/items/items.json`,
`data/recipes/recipes.json`, and `data/skills/skills.json`.
Those IDs/save records are **unchanged**. Do not infer a 14→152 mapping by name,
art similarity or index. New catalog ID normalization is not a save migration.

Forward path: P11/P13/P16 fill approved content → explicit legacy mapping and
schema-version migration → migration tests on copied saves → runtime switch.
Old/new readers must coexist or deploy behind a version gate; never silently
accept unknown IDs. Rollback for this authoring-only stage is reverting
`data/p10/` and its tooling/docs; no live save rewrite is involved. Once runtime
migration occurs, rollback requires the later migration's backup/reverse plan.
