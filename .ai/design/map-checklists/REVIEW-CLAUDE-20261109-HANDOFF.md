# Nghiệm thu art Phimond — Claude, 2026-11-09 (bàn giao từ Codex)

Phạm vi: nghiệm thu + lập kế hoạch. Không commit/push, không sửa runtime/gate/waiver, không sinh artwork, không chạy lại generator checklist. Dữ liệu chi tiết: [ASSET-VERDICTS](ASSET-VERDICTS-20261109.csv), [MAP-COVERAGE](MAP-COVERAGE-20261109.csv), [ROADMAP](ROADMAP-ART-92MAPS-20261109.md), [TASKS](ROADMAP-ART-TASKS-20261109.csv). Script sinh dữ liệu: `review-20261109-tools/`.

## 1. Kết luận ngắn

- **Chưa thể nói "100% art plan".** 0/92 map đạt "asset-ready" (còn VẼ_LẠI/THIẾU/SỬA/CHƯA_XEM) và 0/92 có scene proof map-scale từ asset thật.
- 23 map / 8 kit (tower → minigame) chưa có artwork. Đối chiếu ảnh gốc cho thấy brief plan của **6/8 kit sai chủ đề** (tower, maze, battlefield, arena2, maya, dungeon) ⇒ phải viết lại brief theo ảnh gốc trước khi vẽ; battlefield+arena2 (3 map) dùng cùng một ảnh, guild+minigame dùng chung tường/sàn/trời.
- Batch-11 (9 kit): 510/600 primary được DUYỆT ở mức V1 (chưa 4×), 82 VẼ_LẠI, 8 SỬA đóng gói. Lỗi tập trung ở sàn (khe lưới/chu kỳ), edge (seam/cadence), backdrop nightmare, decal nightmare, prop tomb phẳng.
- Batch vẽ đầu giao Codex: **M1-a World Tree (5 asset) + M1-b Garden (5 asset)**; song song M0 sửa metadata (không cần vẽ). Prompt copy-paste trong ROADMAP §4.

## 2. Số liệu theo mẫu số rõ ràng (đếm dòng ASSET-VERDICTS; `counted_unique=yes`)

| Nhóm (mẫu số) | Số dòng | DUYỆT | SỬA_ĐÓNG_GÓI_METADATA | VẼ_LẠI | THIẾU_CHƯA_CÓ | TÁI_DÙNG_HỢP_LỆ | CHƯA_XEM |
|---|---:|---:|---:|---:|---:|---:|---:|
| A. batch-11 primary (9 kit đã vẽ) | 600 | 510 | 8 | 82 | 0 | 0 | 0 |
| B. garden-a | 30 | 25 | 0 | 5 | 0 | 0 | 0 |
| C. P01 redo A–D (thay predecessor) | 39 | 14 | 23 | 2 | 0 | 0 | 0 |
| D. batch-12-city | 41 | 16 | 17 | 8 | 0 | 0 | 0 |
| E. baseline batch-00..09 — scope map (kế thừa/không xem lại) | 309 | 0 | 0 | 0 | 0 | 230 | 79 |
| F. supplemental batch-10/13/p01-release/octopath-s01 | 197 | 0 | 0 | 0 | 0 | 68 | 129 |
| G. THIẾU: slot kit chưa vẽ (8 kit/23 map) | 407 | 0 | 0 | 0 | 407 | 0 | 0 |
| H. THIẾU: slot landmark của kit đã có (desert/forest/ship) + world_tree-edge-03 | 10 | 0 | 0 | 0 | 10 | 0 | 0 |

Không cộng vào mẫu số (trùng/lịch sử/ngoài phạm vi 92 map):

| Nhóm (mẫu số) | Số dòng | DUYỆT | SỬA_ĐÓNG_GÓI_METADATA | VẼ_LẠI | THIẾU_CHƯA_CÓ | TÁI_DÙNG_HỢP_LỆ | CHƯA_XEM |
|---|---:|---:|---:|---:|---:|---:|---:|
| batch-11 auxiliary (frame/sway phụ, không cộng) | 26 | 0 | 0 | 0 | 0 | 0 | 26 |
| P01 predecessor (đã có redo thay, không cộng) | 18 | 0 | 0 | 0 | 0 | 0 | 18 |
| baseline 00..09 UI/actor/NPC (phụ lục, ngoài 92 map) | 452 | 0 | 0 | 0 | 0 | 358 | 94 |
| Dòng checklist cũ/alias/landmark tái dùng/placeholder #2 (không cộng) | 98 | 0 | 0 | 0 | 0 | 5 | 93 |

Ghi chú mẫu số: inventory có 1.712 bản ghi, nhưng batch-11 gồm **600 primary + 26 auxiliary** (prompt gọi 626 "primary"); không cộng baseline/predecessor/redo/aux thành asset duy nhất. CSV có 2227 dòng = 1.712 inventory + 515 dòng checklist (slot THIẾU, alias, landmark, legacy).

Tổng theo verdict (mọi dòng unique): {'CHƯA_XEM': 302, 'TÁI_DÙNG_HỢP_LỆ': 656, 'DUYỆT': 565, 'VẼ_LẠI': 97, 'SỬA_ĐÓNG_GÓI_METADATA': 48, 'THIẾU_CHƯA_CÓ': 417}.

Chi tiết batch-11 theo kit:

| Kit | primary | DUYỆT | SỬA | VẼ_LẠI | THIẾU slot | landmark/tái dùng CHƯA_XEM |
|---|---:|---:|---:|---:|---:|---:|
| world_tree | 51 | 47 | 0 | 4 | 1 | 0 |
| crossroads | 62 | 46 | 4 | 12 | 0 | 1 |
| nightmare | 67 | 47 | 0 | 20 | 0 | 5 |
| tomb | 76 | 59 | 0 | 17 | 0 | 0 |
| windrock | 82 | 70 | 0 | 12 | 0 | 0 |
| desert | 98 | 93 | 0 | 5 | 6 | 6 |
| ghost_castle | 50 | 44 | 0 | 6 | 0 | 3 |
| astral | 59 | 56 | 0 | 3 | 0 | 0 |
| ancient | 55 | 48 | 4 | 3 | 0 | 3 |

## 3. Mức bằng chứng — đã xem và chưa xem

- **V1 = montage** (game-scale lưới, sàn 2×2, edge/backdrop 3×1, backdrop 2×1) của toàn bộ 600 primary batch-11, 30 Garden, 39 P01 redo, contact sheet batch-12, so sánh 3×1 thật cho edge-03 studies, 23 ảnh gốc của kit chưa vẽ. **Không làm 4× caro/tối từng asset**; do đó DUYỆT nghĩa là "đạt V1 + số đo cơ học + không thấy lỗi", điều kiện đóng ghi trong cột `close_criteria` (cần 4× + scene proof).
- **Số đo:** metrics tự đo (màu, alpha bán trong suốt, lề alpha, wrap x/y, độ phủ) cho 750 file; ngưỡng quyết định: <28 màu = phẳng (VẼ_LẠI), lề<8 (SỬA), alpha bán trong suốt (SỬA), sàn wrap>2.0 (VẼ_LẠI).
- **Chưa xem (CHƯA_XEM):** 302 dòng unique — baseline/supplemental chưa có approval hợp lệ, 26 aux, batch-13, octopath-s01, p01-release chưa duyệt, landmark tái dùng chưa đối chiếu ảnh gốc, slot landmark #2 "nếu có".
- **TÁI_DÙNG_HỢP_LỆ cho baseline** = manifest approved và sha khớp file; **không xem lại hình**. 250 dòng như vậy vẫn fail gate `--all` hiện hành (chủ yếu UI batch 06–09); xem cột `gate_all_errors` trong ASSET-VERDICTS.
- **Lệnh gate:** `python3 tools/hd2d_audit/art_gate.py` (batch-11, 9 kit): 626 asset, 0 lỗi, 0 cảnh báo ([log](review-20261109-tools/gate-batch11-20261109.txt)). `python3 tools/hd2d_audit/art_gate.py --all`: 33 thư mục (gồm batch-14..18 ngoài inventory), 1.434 asset, **367 lỗi** ([log](review-20261109-tools/gate-all-20261109.txt)): 295 audit, 21 sheet, 16 size, còn lại bbox-edge; phân bố: batch-09 124, batch-07 90, batch-08 40, batch-12 27, batch-06 22, batch-02 19, batch-13 12. Gate không kiểm sha, không bao Garden/P01; `gate_waivers.json` rỗng — không sửa.

## 4. Phát hiện chính

**Artwork**
1. Sàn: crossroads (8/8) và nightmare (8/8) lộ khe chữ thập phẳng khi lát 2×2; desert (5/9), windrock (9/9), tomb (4+1), astral (2), ghost (3), ancient (1), world_tree (1) có nhịp lặp theo lưới / seam.
2. Edge: world_tree 01/02 lộ đường cắt 512; crossroads 3/3; ghost 02 có vạch magenta, 03 vạch tối; ancient 03 đối xứng gương; astral 03 cadence; nightmare 01/03 khe trống; tomb 3 dải là gò rời; windrock 3 dải 63 màu.
3. Backdrop: nightmare far/far-02 phẳng, mid/near phủ ~50%; ghost near dính thân cây ở điểm nối.
4. Decal nightmare trùng họa tiết/sha (02=03; 05=06=08; 01–04 cùng mẫu); 09/10 viền sáng.
5. Tomb: 9 prop <28 màu hoặc halo nướng (stele, keys).
6. World Tree: hoa gate-landmark-01 yếu; edge-03 chưa có (16 attempt bị bác — xem preview 3×1 thật ở `world-tree-repeat-corrections/`).
7. Garden: 25/30 DUYỆT; trả 5 (trunk-seg-01/02, seal-strip, seal-strip-lit, pillar-vein-01).
8. P01 redo: 14 DUYỆT, 2 VẼ_LẠI (màu), 23 SỬA (lề alpha 0 px — kiểm bị cắt cạnh).
9. Batch-12-city: 8 asset vượt gate (density/size/seam), 17 cần pad lề; 16 giữ DUYỆT V1.

**Metadata / provenance**
10. 30 sha lệch (không phải 30 redraw): batch-01 15 (aux 10 + 5 primary), batch-03 4, ancient shadow 3 + crossroads foam 4 (qa.json sha == file ⇒ manifest cũ), 3 predecessor P01 (`farm-tilled-01`, `streetlamp-lit`, `pet-feed-bowl-water`: file == git blob HEAD commit 3f484654 ⇒ manifest cũ, không phải file bị thay), `world_tree_gate-landmark-01` (manifest cũ sau sửa lề; art cũng yếu). Batch-01/03 file không đổi từ commit nhưng sha kỳ vọng chưa bao giờ commit ⇒ không kế thừa approval khi chưa xem lại.
11. Pet bowls P01 predecessor D thiếu `manifest.file` (path suy luận; file thật tồn tại).
12. Raw provenance: 3 raw bị PNG re-encode (pixel giống, byte/hash khác bản ImageGen gốc); các tuyên bố "byte-identical" trước đây sai cho những file đó; bản gốc ở `generated-originals/`.
13. Preview `repeat-3x.png` của edge-03 studies 11, 13–16 chỉ phóng 1 tile ⇒ không dùng làm bằng chứng; dùng `world-tree-repeat-corrections/` (11/13/16 lặp cụm, 14 nhịp khối đều, 15 phẳng).

**Mâu thuẫn tài liệu**
14. Brief plan vs ảnh gốc (6/8 kit chưa vẽ) — chi tiết ROADMAP §5.
15. README/kit md: Tomb ❌ (Gemini) dù 76 candidate tồn tại; windrock 42 dòng "Gemini cũ bị trả" là lịch sử; nightmare ⬜ prop-10/13/14, marker-arrival, backdrop-far-01 thực ra có asset dưới ID khác (portal, camp-tent+campfire, wisp-lantern, marker-arrival-frame, backdrop-far); quota "thiếu N" trong bảng "Trạng thái asset hiện có" (forest 5/8 floor…, ship 1/8…, beach edge 0/3) chưa chứng minh là bắt buộc cho map; desert edge 0/3 trong README nhưng có 3 dải `desert-edge-sand-*` 512×128.
16. Garden: log Codex cũ ≠ review Claude hiện hành (25/30). Dùng review Claude.
17. Gate batch-11 "0 lỗi" ≠ đạt hình: nhiều lỗi sàn/edge/backdrop ở §4 lọt gate; ngược lại README ghi windrock edge "qua gate" nhưng 63 màu > Master.
18. Landmark tái dùng: spot-check `ancient_ruins_unnamed_area_04` cho thấy ref ≠ mô tả tái dùng ⇒ mọi landmark tái dùng ancient/astral/crossroads/tomb ghi CHƯA_XEM tới khi đối chiếu từng ảnh gốc.

## 5. Ba mục yếu nhất theo kit

| Kit | 3 mục yếu nhất |
|---|---|
| world_tree | `world_tree-edge-03` (THIẾU, 16 attempts bị bác); `world_tree-edge-01/02` (lộ đường cắt 512); `world_tree_gate-landmark-01` (hoa: art yếu + manifest sha cũ) |
| crossroads | bộ 8 sàn `crossroads-floor-*` (khe chữ thập navy 16 px); `crossroads-edge-01` (lệch bờ tại mốc 512); `crossroads_unnamed_area_02-landmark-01` (thùng cam lạc tông) |
| nightmare | bộ 8 sàn (khe chữ thập, floor-01 gần phẳng); `nightmare-backdrop-far-02`/`far` (21–24 màu phẳng); `nightmare-decal-09/10` (viền trắng-lavender) + decal trùng sha 03/06/08 |
| tomb | `tomb-glyph-stele` + `tomb-ancient-keys` (halo nướng, không đọc ra vật); 3 edge (gò tam giác rời); `tomb-dead-thorn-bush` (19 màu) / `tomb-hanging-censer` (20 màu) |
| windrock | 3 edge (63 màu, wx 2.3–2.8); 9 sàn (nhịp lặp theo lưới); `windrock-edge-01` là mục sửa đầu tiên |
| desert | `desert-sandstone-floor`, `desert-sand-cracked-01/02` (nhịp lặp theo lưới), `desert-sunken-brick-floor` (như decal trên nền phẳng); 6 landmark #1 THIẾU |
| ghost_castle | `ghost_castle-floor-extra-05` (lưới bát giác lộ); `ghost_castle-edge-02` (vạch magenta 1 px); `ghost_castle-backdrop-near` (2 thân cây dính ở điểm nối) |
| astral | `astral-floor-extra-03` (lộ vạch lưới); `astral-floor-extra-05` (hạt phẳng nhiễu); `astral-edge-03` (lặp cụm đều) |
| ancient | `ancient-floor-extra-02` (bát giác khổng lồ seam rõ); `ancient-edge-03` (đối xứng gương); `ancient-marker-arrival` (lề 2 px) + 3 shadow manifest sha cũ |
| forest | landmark #1 của 2 map THIẾU (chưa chọn vật nhận diện); bảng quota floor 5/8, edge 2/3, prop 35/36 của README chưa được chứng minh là cần; chưa có scene proof |
| city | 8 asset batch-12 vượt gate (DENSITY/size/seam: `city-sacks`, `animal-cat`, `animal-pigeon-*`, `city-lion-fountain`, `palace-flagpole`, `city-roofline-mid`); 23 asset P01 redo lề 0 px; ~19 asset CHƯA_XEM ở city_square |
| beach | quota floor 6/8, edge 0/3, prop 28/36 theo README (chưa chứng minh bắt buộc); batch-03 sha lệch 4 + treasure-chest vượt cỡ (gate size); chưa có landmark/scene proof |
| ship | landmark #1 THIẾU; quota floor 1/8, edge 0/3, prop 5/36 theo README (chưa chứng minh bắt buộc); batch-04 `rum-barrel`, `teleport-pillar-high` vượt/thiếu cỡ (gate size) |
| tower | Brief plan (tháp đá/lan can kim loại) mâu thuẫn ảnh gốc (rừng xanh, cầu ván gỗ, tổ chim) ⇒ cần BRIEF-tower trước; 3 landmark #1; tầng Mật cầu ván gỗ |
| maze | Brief plan (dây leo rêu) mâu thuẫn ảnh gốc (xương/móng nhọn, cổng sọ phát sáng, sàn hồng-nâu) ⇒ BRIEF-maze; cổng sọ phát sáng; chuỗi gai/móng trên sàn |
| guild | 6 công trình riêng (lâu đài, kho bạc, nhà khung gỗ, doanh trại, cabin, chuồng) chưa có; tường thành + sàn nứt dùng chung với minigame; cờ bang tự thiết kế |
| battlefield | Brief plan (đất cháy/chiến xa) mâu thuẫn ảnh gốc (quảng trường trắng cột tím); đài phun nước; tượng thú đồng trên bệ — dùng chung với arena2 |
| maya | Brief plan (kim tự tháp/rừng) mâu thuẫn ảnh gốc (điện thờ lục thẫm); cột phù điêu xoắn; ngai đá chạm |
| dungeon | Brief plan (ngục sắt/xích) mâu thuẫn ảnh gốc (tường gạch be + đầu hươu cam, sàn vảy vàng-xanh); chỉ 1 map |
| arena2 | Cùng ảnh quảng trường với battlefield (chaos/team); plan "cát/khán đài" không khớp; chỉ vẽ phần khác biệt sau battlefield |
| minigame | Tường/sàn/trời dùng chung với guild; 4/6 map là sân trống; sheep_house/wolf_house nhà mái nâu + bạt xanh |

## 6. Phụ lục — ngoài 92 map / phụ thuộc riêng

- NPC/portrait/UI/icon/walker: 452 dòng baseline + gói bổ sung; coverage `npc_dependency_separate` liệt kê NPC theo roster, không tính vào % map.
- Gói bổ sung: `batch-10` (28), `batch-13-release` (14, chưa có contact sheet), `p01-release-art-20261023` (110), `octopath-s01-s27-20261029` (45, schema riêng) — CHƯA_XEM/TÁI_DÙNG, chưa xác định liên hệ plan.
- Ngoài inventory 1.712: các thư mục `batch-14..18`, `p01-release-art-20261022` hiện có trong working tree (gate `--all` có quét); chưa đối chiếu — cần bàn giao inventory bổ sung nếu thuộc scope.
- Working tree có nhiều thay đổi chưa commit từ nhiều công việc (`git-art-status.txt`); không revert/dọn.
- Đã cập nhật tay: block trạng thái nghiệm thu đầu `README.md` và các `kit-*.md` (giữ lịch sử, không đổi tick cũ).

## 7. Tiêu chí để được nói "100% art plan"

Mọi nhu cầu asset của 92 map có verdict hợp lệ (DUYỆT/TÁI_DÙNG_HỢP_LỆ) và 0 task REDRAW/NEW/FIX bắt buộc; scene/gameplay integration báo riêng. Hiện: 562 dòng unique cần làm (VẼ_LẠI 97, THIẾU 417, SỬA 48) + 302 CHƯA_XEM cần xem.
