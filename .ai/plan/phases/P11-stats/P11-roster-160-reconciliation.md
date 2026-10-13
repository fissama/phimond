# P11 — Roster 160 and top-tier reconciliation, 2026-10-13

Current effective numeric design: [catalog160](P11-species-catalog-160.md). This reconciles the owner-requested extension and P13 v7 role directions. It does not activate runtime or approve the full P13 phase.

## Current counts / identity

141 Normal + 19 Special; 17 Normal4, 20 Normal5, 4 Special4 and 15 Special5. The 152 APK IDs/names/Race/Star/class/Element/source descriptions are unchanged; eight additions use P10 authored allocations species_0153–species_0160. Source registry hashes now bind the original namespace independently of appended authored IDs. Full registry and proposal mapping provenance are pinned in the amendment manifest.

No existing Race ID change was found in the current P10/P13 input. Race stat directions remain the approved P11 directions; role changes regenerate main/SPD/SR/MP targets before the same Species modifiers. Changing Race IDs later requires explicit identity reconciliation.

## Fourteen role changes

| ID / Name | Previous roles | Current roles |
|---|---|---|
| species_0020 — Thủ Lĩnh Hắc Ám | tank / physical_dps | physical_dps / tank |
| species_0035 — Trưởng Lão Người Cây | tank / support | magic_dps / support |
| species_0037 — Độc Đằng Nữ | disruptor / magic_dps | magic_dps / disruptor |
| species_0038 — Tinh Linh Bách Hoa | support / tank | physical_dps / support |
| species_0051 — Long Vương Hắc Ám | hybrid | physical_dps / disruptor |
| species_0069 — Trụy Thiên Sứ | support / magic_dps | hybrid / support |
| species_0084 — Tinh Tinh Rock | tank / disruptor | tank / physical_dps |
| species_0103 — Chim Đại Phì | disruptor / magic_dps | magic_dps / disruptor |
| species_0124 — Trùng Bất Tử Địa Huyệt | tank | physical_dps / tank |
| species_0126 — Trùng Mẫu Mào Vàng | support / disruptor | magic_dps / support |
| species_0141 — Totem Thượng Cổ | support / magic_dps | magic_dps / support |
| species_0145 — Cây Cự Linh | tank / support | tank / physical_dps |
| species_0148 — Ngựa Bùn Cỏ | physical_dps / support | magic_dps / support |
| species_0150 — Đảo Thiên Đường | tank / support | physical_dps / tank |

## Eight authored additions

| P13 alias | P10 stable ID | Name | Race / Class | Roles |
|---|---|---|---|---|
| P13-NEW-01 | species_0153 | Hươu Rêu Nguyệt | beast / normal5 | magic_dps |
| P13-NEW-02 | species_0154 | Thiết Giáp Long | dragon / normal5 | physical_dps |
| P13-NEW-03 | species_0155 | Tinh Vân Long | dragon / normal5 | magic_dps |
| P13-NEW-04 | species_0156 | Đao Ma Huyết Giáp | demon / normal5 | physical_dps |
| P13-NEW-05 | species_0157 | Ma Nhãn Hư Không | demon / normal5 | magic_dps |
| P13-NEW-06 | species_0158 | Hộ Vệ Thạch Linh | spirit / normal5 | physical_dps |
| P13-SPECIAL-01 | species_0159 | Long Thần Song Ấn | dragon / special5 | hybrid / support |
| P13-SPECIAL-02 | species_0160 | Ma Chủ Song Cực | demon / special5 | hybrid / disruptor |

## Development and numeric contract

- Every Race has primary Physical and primary Magic Normal at 4/5★. Tank/Support/Disruptor secondary channels and Special do not count toward this coverage. Hybrid is its own channel, not counted as both specialists.
- Preserve Normal Hybrid5 Thánh Rồng Thái Cổ, Nhân Sư and Trụy Thiên Sứ. Their direction reaches two Special Hybrid5: Long Thần Song Ấn and Ma Chủ Song Cực. Hybrid keeps ATK/MAG split, not two turns or ATK+MAG in one hit.
- Special4 remains Thanh Long Hybrid, Bạch Hổ Physical, Chu Tước Magic/Support, Huyền Vũ Tank/Support. Special5 role amendments are shown above; other Species retain prior role.
- Main targets remain Normal4=136/2.720, Special4=148/2.960, Normal5=160/3.200, Special5=172/3.440. Same tolerances, 75/25 blend, per-stat bands, integer base/milli growth and cumulative floor. No further premium or Race multiplier is added.
- Parent/recipe directions inform kits and roster coverage. They never average parent stats into Species base/growth or bypass P11 inherited-credit rules. Recipe eligibility/operations/Plus stay P16/P20; candidate28 is separate from source17.
- Existing Bird priority remains relative to ordered role blend. Example Chim Đại Phì now Magic/Disruptor, not Disruptor/Magic; its template SPD changes with that role order. It still leads non-Birds in the new matching cohort.
- Same-grade/level/class role comparisons are required. Level/grade/inheritance/equipment can reverse individual matchups. Static authoring cannot establish measured combat or acquisition balance.

## Verification and source boundaries

320 layers valid; all six Elements remain represented by Normal5. Bird proof covers 67 actual pairs plus 252 template cohorts. Exact numeric projection (six stats, roles, identity, MP) matches pinned P13 v7 after stable remapping.146 vectors,25 Species in shared-vector groups; P13 owns kit differentiation. All160 records have authored descriptions, original97 quotes remain verbatim. New eight descriptions are Phimond authoring, not recovered source.

Old P11 JSON/Markdown and arithmetic reports remain 152 snapshots. Existing P13 generator still reproduces unchanged v7. Current README/spec/tables direct consumers to catalog160. The mapping/art/recipe/pool references need delivery through their respective owners; no art or P13 runtime is enabled here.
