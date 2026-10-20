# P13 — APK/JAR source audit

Date: 2026-10-13. Read-only static inspection; original clients/servers not executed.

## Observed

- Both Unity APK catalogs contain **60 unique skill records**; SkillAssetData consumes exactly **9,024/9,024 bytes**.
- Same 60 IDs in APK3.2 and8.4; **13 records differ** in serialized requirements. Names, classification and descriptions agree in this comparison.
- Schema from APK8.4 metadata v31: SkillModelData = ID, NameSkill, TypeChoose, TypesSkill, HeSkill, TypeCombat, TypeLoai, BuffType, YeuCaus, GioiThieu. YeuCau = levelHoc, Mana, Gia, Dame.
- TypeChoose distinguishes Poke/Enemy; TypeCombat All/One; TypeLoai None/Physic/Magic/PhanKich. HeSkill mixes six elemental labels and named status categories, so it is not evidence for the new independent Race/Element chart.
- Source descriptions include sleep waking with double damage, petrification blocking attacks and granting immunity, lethal doom after four turns, passive20% regeneration/rebirth/MP regeneration, and an explicitly non-inheritable ancient holy dragon skill. These are observed client descriptions, not verified server behavior.
- JAR manifest declares MIDlet-Version1.00, CLDC1.1/MIDP2.0. Original archive bytes confirm Race-signature text in l.class, full-slot/forget text in decompressed ui_learnskill.ui, and the AoE trainer help in ui_newplayerhelp.ui.

## Provenance

| Source | SHA-256 |
|---|---|
| APK3.2 | `4585589356c3aaebdf99589f0194d72e74c471cc71425d3b54f7e119437f72ac` |
| APK8.4 | `b8e02a75e49d5d02703a0b05ec52b450cdfaf69d544f04df2f4a2a465199a18e` |
| JAR1.00 | `5b39bc4f6a3490f7fb4d32db55e6f92cf66399cabd6727675386cf6d51e3f7ce` |

Sources: `/Users/phileanh/Downloads/Spirit Beast World 3.2.apk`, `/Users/phileanh/Downloads/Spirit Beast World 8.4 (1).xapk`, `/Users/phileanh/Downloads/Pokezoo 100.jar`. The XAPK primary archive is `com.HCGame.SpiritBeastWorld.apk`.

APK8.4 DataSkill: `sharedassets0.assets`, path_id744. APK3.2 uses its own class-located object recorded in evidence; path IDs are version-specific. Metadata names and serialized layout are reconciled with the existing P10 extraction method.

## Version conflicts — raw requirement values

| ID | Different fields | APK3.2 → APK8.4 |
|---|---|
| ThieuDotPhapLuc | Dame | Dame: 60 → 85 |
| UyRongPhaHoi | Dame | Dame: 200 → 185 |
| CanQuetSieuCap | Dame | Dame: 140 → 123 |
| QuangMinhSieuCap | Dame | Dame: 200 → 130 |
| DaiDiaSieuCap | Dame | Dame: 200 → 130 |
| HanBangSieuCap | Dame | Dame: 200 → 130 |
| HoaThieuSieuCap | Dame | Dame: 200 → 130 |
| ThanPhongSieuCap | Dame | Dame: 200 → 130 |
| HacAmSieuCap | Dame | Dame: 200 → 130 |
| NuHon | levelHoc | levelHoc: 140 → 150 |
| LuoiHai | levelHoc | levelHoc: 140 → 150 |
| PhucSinh | levelHoc, Mana | levelHoc: 140 → 150; Mana: 13579 → 1123 |
| TriLieuNhomSieuCap | Mana, Gia | Mana: 1357 → 789; Gia: 10 → 20 |

## JAR signatures and evidence limits

| Race text | Special / racial signature |
|---|---|
| Bất tử | Hỗn loạn / Trùng sinh |
| Chim | Ngủ say / Cấp tốc |
| Dã thú | Trói buộc / Thú tính |
| Linh thể | Vận xui / Suy tưởng |
| Sâu | Hóa thạch / Giáp xác |
| Thực vật | Mù mắt / Tái sinh |
| Ác ma | Trầm lặng / Ma tính |

Direct UTF-8 byte probes corroborate local extraction snippets. JAR decompile is a convenience only; CFR summary reports incompletely structured an/aw/bm methods. No original server implementation or full species→skill eligibility table was recovered. JAR seven descriptive profiles do not invalidate the frozen8-Race roster or P11 authoring.

## Unknown / explicitly not inferred

- `Mana` values such as1029/10129/7890 and `Dame` values are preserved as raw integers. Their encoding, units, applied rank/range and server formulas are unverified; do not claim these as current MP costs.
- Learn acquisition per Species, combat speed/timing, real status chance/stack/duration, original chart, skill prices and server exclusivity enforcement are not established by this static catalog alone.
- No evidence here proves all source skills/pets can actually be acquired, or that original passive/resource rules fit Phimond P11.

## Candidate resolution

Phimond keeps identifiable names and function themes, keeps four APK AoE tiers as separate fixed-rank skills in v3 (the v1/v2 rank fold was superseded after owner feedback), and authors explicit costs/power/eligibility. No passive MP/HP auto-regeneration; no source instant-death/immunity or double-damage sleep copied into v1. Seven dedicated cleanse names are retained. Four source-adapted skills and seven authored Special signatures are non-inheritable. No roster changes: exactly152 P10/P11 IDs. Source catalogs remain unchanged.

## Reproduce

```sh
rtk proxy tools/.cache/asset-venv/bin/python tools/content/p13_source_audit.py
```

Outputs: `evidence/apk32-skills.json`, `evidence/apk84-skills.json`, `evidence/source-audit.json`. `evidence/apk84-skill-schema.json` preserves metadata schema inspected before full catalog decoding. These are small static evidence, not server emulation or gameplay certification.
