# P10 extension — identity / registry report

Date: 2026-10-13. Status: **160 effective authoring records; new art awaiting owner review; runtime inactive**.

## Stable allocations

Before registration, IDs `species_0153`–`species_0160` were absent from the registry and owner selection manifest. Allocation uses a separate `authored_species` namespace; the existing APK `species` mapping remains exactly unchanged.

| P13 proposal | Stable ID | Name | Class | Role / secondary | Element |
|---|---|---|---|---|---|
| P13-NEW-01 | species_0153 | Hươu Rêu Nguyệt | Normal 5★ | magic_dps | earth |
| P13-NEW-02 | species_0154 | Thiết Giáp Long | Normal 5★ | physical_dps | earth |
| P13-NEW-03 | species_0155 | Tinh Vân Long | Normal 5★ | magic_dps | light |
| P13-NEW-04 | species_0156 | Đao Ma Huyết Giáp | Normal 5★ | physical_dps | fire |
| P13-NEW-05 | species_0157 | Ma Nhãn Hư Không | Normal 5★ | magic_dps | dark |
| P13-NEW-06 | species_0158 | Hộ Vệ Thạch Linh | Normal 5★ | physical_dps | earth |
| P13-SPECIAL-01 | species_0159 | Long Thần Song Ấn | Special 5★ | hybrid / support | light |
| P13-SPECIAL-02 | species_0160 | Ma Chủ Song Cực | Special 5★ | hybrid / disruptor | dark |

## Catalog layering and provenance

- `data/p10/species.json`: frozen historical 152-source snapshot; no edits. SHA256 `9b7bda2ae9bcd7b38c89c5873b2c8115779e3cb4c654cfa0b3c88ab854ce8000`.
- `data/p10/species_authored.json`: eight Phimond-authored records with proposal provenance, no fabricated APK/JAR enum/path/hash.
- `data/p10/species_effective.json`: 160 authoring records composed from the unchanged 152 records plus eight additions.
- Full eight P13 v7 role/stat/growth/MP candidate records retained under `design_candidate.record`; only IDs/registration status remapped. This is explicitly **pending P13 acceptance, not P11 promotion**. No numeric data promoted to runtime.
- `mapping.json` and `../P13-skills/P13-to-P10-eight-species-mapping.json` (relative to the P10 phase root) deliver proposal → stable mappings. P13 owners should remap pool/signature/recipe references in their candidate layer separately.
- The 17 source recipes remain disabled. This extension does not replace those evidence records with the 28 P13 candidate recipes and does not enable fusion.

## Preservation and verification

`preservation-before.json` snapshots **919 file hashes**, including frozen catalogs, APK source roster/assets, the owner selection manifest, and all 152 selected atlas files. It also snapshots all original registry fields. `p10_extension.py` verifies this evidence on every generation/check.

Commands run:

```sh
rtk proxy python3 tools/content/p10_extension.py --write
rtk proxy python3 tools/content/p10_extension.py
rtk proxy python3 tools/content/p10_catalog.py
rtk proxy python3 -m unittest discover -s tools/content -p 'test_p10_extension.py' -v
rtk proxy python3 -m unittest discover -s tools/content -p 'test_p10_catalog.py' -v
rtk proxy git diff --check
```

Results: extension check PASS; original 152 catalog check PASS; **19 tests passed** (10 extension + 9 baseline); whitespace check PASS.

Focused corruption checks reject stable ID collisions, conflicting authored allocations, duplicate original IDs, false APK provenance, and wrong Star. Tests also confirm unchanged original records, exact numeric candidate preservation, six Normal/two Special 5★, and art/runtime gates staying false.

## Pending gates

Art manifests/hashes and mechanical/visual animation review are delivered by the art/review workstream. Each authored record references the art manifest and stable species ID; it does not pin an attempt filename. Resolve the current candidate from the manifest's stable-ID-keyed records so later repairs do not leave stale catalog paths. These references do not assert that art has passed or been selected. No new art selection or runtime activation is authorized by this registration report. Existing baseline design closure is preserved; this extension does not close P13/P11 or certify runtime balance.
