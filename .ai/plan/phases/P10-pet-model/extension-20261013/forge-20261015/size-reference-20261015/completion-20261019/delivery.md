# P10 extension — Five atlas size delivery, 2026-10-19

Status: **size/clarity adjustment implemented and verified; owner review pending**. Full final-art acceptance and runtime activation are not granted.

## Implemented

- Matched visible opaque body height against selected Linh Tiên Hoa Hương (species_0144, 164px).
- Regenerated/edited source art and packed full-source rectangles at one uniform nearest-neighbor scale; no source alpha threshold/erasure.
- Fixed major cross-frame fragments, restored Tinh Vân tail star and Ma Chủ spearhead, repaired Long Thần lower seal, corrected Ma Chủ basic attack order.
- Each species remains one 1124×1405 RGBA PNG, 4×5 cells, 20 distinct poses; alpha stays in cell-local [22,259).
- Idle/movement loop; attack/skill/hurt play once and hold final.
- Added equal-scale interactive96/192/281px comparison with immutable0144 and prior candidates.

## Final candidates

| Species | Attempt | Before | After |
|---|---:|---:|---:|
| Hươu Rêu Nguyệt | 18 | 147px | 166px |
| Tinh Vân Long | 19 | 114px | 160px |
| Ma Nhãn Hư Không | 18 | 141px | 161px |
| Long Thần Song Ấn | 20 | 145px | 169px |
| Ma Chủ Song Cực | 22 | 114px | 167px |

Opaque height measures alpha≥128 in first idle pose; it is a measurement only, not an alpha edit. Narrow deer/humanoid naturally differ in width from a flower fairy. Same complete281pxcell rendered for every species.

## Checks

- 33 asset unit tests passed.
- All5 mechanical checks passed; all20 source rectangles cover the complete raw canvas exactly once.
- All5 source/packed body/weapon/FX and96/192 readability inspected by independent reviewer; exact-hash reconciliation records the results.
- Selected152 atlas hashes and three approved extension atlas hashes unchanged.
- Roster check PASS160 authored records /152frozen /8authored IDs /no runtime activation.
- Live8125 API hashes match all5 candidates; health reports160. Comparison8126 returns200.

## Owner review notes

- Tinh Vân retains a tiny FX speck; pixel finish/glow and four-frame motion remain owner judgments.
- Ma Nhãn tentacles overlap across poses; skill pupil/maw shape needs owner design review.
- Long Thần new wings and clear claw→two-tail-seal ignition sequence still need owner review.
- Ma Chủ gait remains subtle; skill pulse could be distinguished further from spear shape.
- These are not certifications of final player-facing art. The requested size pass is complete; no user approval is invented.

## Manual review

[Compare size and animation](http://127.0.0.1:8126/) · [Save owner feedback](http://127.0.0.1:8125/#species_0159).

Server processes: `review-processes.json`; logs `/tmp/p10-extension-review.log` and `/tmp/p10-size-review.log`. These are art-review servers; game server/DB untouched under the approved art scope.

Evidence: [verification](verification.json), [hash/size data](comparison.json), [review reconciliation](review-reconciliation.json), [live API verification](live-review-verification.json).

## Scope / handoff

No other roster sprites resized. Await owner size review of these5 before reviewing remaining atlas sizes. Historical raw/candidates retained. No push/merge/deploy or runtime asset selection.
