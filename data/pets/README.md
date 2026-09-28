# Pet catalogs

For new P10 development, use the normalized authoring catalog in
[`../p10/`](../p10/README.md). This directory retains raw source and legacy runtime content.

- `species.json`: legacy 14-species runtime content. Existing save IDs and numeric
  rules refer to it; it is reconstructed content, not the original species roster.
- `roster_apk84.json`: **approved raw 152-species identity and art baseline** imported
  from the supplied APK 8.4. Preserves original IDs/names/Race/Star, descriptions,
  17 Special recipes and `res://` asset references.
- `races.json`: legacy runtime race rules; the new design separates Race/Element
  and does not automatically use these old bonuses or elemental assignments.

The new roster intentionally does not invent numeric stats, Element assignments,
growth, skill pools, spawn locations or source server validation. Its metadata
lists the unresolved fields. P11/P13/P16 and a save migration must supply those
before replacing `species.json` in the authoritative server.

Full list: `.ai/plan/phases/P10-pet-model/P10-roster.md`.
Importer: `tools/assets/import_p10_roster.py` (offline, exact source hash checked).

After a raw import, regenerate/check normalized data with `python3 tools/content/p10_catalog.py --write` then `python3 tools/content/p10_catalog.py`. The frozen registry is not overwritten by the raw importer.
