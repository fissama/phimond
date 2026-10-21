# Phimond HD-2D — Prompt vẽ tiếp 75 map còn lại (Đợt 11+, cho Gemini)

- **Ngày:** 2026-10-15 · Soạn bởi Claude sau tái nghiệm thu Đợt 1–10.
- **Cách dùng:** dán **Phần A** (bắt buộc, kèm bài học lỗi) vào phiên Gemini, đính kèm ảnh nguồn của từng map (`MI:`), rồi dán **một** khối kit ở Phần C. Mỗi phiên làm một kit. Nộp theo Phần D.
- **Phân vai:** Gemini vẽ ASSET RỜI + manifest. Claude dựng cảnh HD-2D (scene JSON, ánh sáng, sương, nước, hạt). Gemini KHÔNG ghép cảnh, KHÔNG sửa code.
- **Phạm vi:** 75 map thuộc 17 kit, 92 − 17 map đã có art. 17 map cũ (Triệu Linh Điện, thành, rừng, biển, tàu) KHÔNG vẽ lại ở đây.

---

## Phần A — Prompt chính (dán cho Gemini)

```text
Bạn là art worker cho Phimond (game nuôi linh thú, client web Three.js HD-2D phong cách Octopath Traveler).
Hãy VẼ bằng công cụ tạo ảnh của bạn. Mô tả bằng chữ không phải artwork. Không vẽ bằng code/hình khối vector.
Bạn chỉ xuất ASSET RỜI. Không ghép cảnh hoàn chỉnh. Không nướng ánh sáng, sương, bóng đổ, glow vào asset.

THAM CHIẾU PHONG CÁCH (đính kèm)
- Các asset ĐÃ ĐẠT cùng dự án (mở trước khi vẽ để khớp outline, đổ khối, độ bão hòa):
  apps/game-web/art-src/hd2d/batch-01-octopath/{grass-floor-01,bush-01,forest-portal-active}/final.png
  apps/game-web/art-src/hd2d/batch-02-octopath/{city-paving-01,barrel,city-teleport-active}/final.png
  apps/game-web/art-src/hd2d/batch-03-octopath/deep-sea-floor-tile/final.png
- Ảnh gốc của map (MI:) để lấy BỐ CỤC + CHỦNG LOẠI VẬT THỂ + bảng màu gốc, không chép nguyên.
  MI = /Users/phileanh/Downloads/Phimond-P12-Review/map-images/<map_id>.png

QUY CÁCH CỨNG (đã bị phát hiện vi phạm ở vòng trước; vi phạm = trả lại)
1. PNG RGBA. Alpha NHỊ PHÂN: mỗi pixel alpha = 0 hoặc 255. TUYỆT ĐỐI không có pixel bán trong suốt (không anti-alias, không lông mờ, không bóng mềm).
2. Tối đa 48 màu (đếm cả màu outline) cho mỗi file. Ép bằng lượng tử hóa bảng màu SAU KHI vẽ, rồi tự đo lại.
3. Không viền hồng/magenta (nếu dùng nền chroma key, phải despill; đo số pixel hồng còn sót = 0).
4. Lề alpha trong suốt ≥ 8 px quanh mọi prop (trừ tile/nền liền mạch). Không pixel lạc rời (vụn < 12 px tách khỏi khối chính).
5. Mật độ: prop/tile/backdrop gần 128 px = 1 đơn vị world (1 ô lưới = 0,52 đơn vị ≈ 66 px). Backdrop xa: 64 px/đơn vị. Nhân vật người cao ~168 px trong ô 192×192 => cây nhỏ nhất cũng phải cao hơn nhân vật.
6. TILE liền mạch: tile 512×512 phải lặp 3×3 không thấy đường nối (đo sai khác mép trái-phải và trên-dưới = 0 pixel khác biệt có ý nghĩa). BACKDROP xa nằm ngang phải lặp được theo trục X (mép trái = mép phải). Sau khi vẽ, ghép thử 3×3 / 3×1 và đính kèm ảnh repeat-3x3.png.
7. Prop đứng: pivot = giữa-đáy ảnh, đáy vật chạm đúng đáy vùng không-alpha. Cây/lá/cờ: tách tán (canopy) và thân (trunk) thành 2 file để engine làm sway (_canopy, _trunk).
8. Vật có trạng thái/động: dormant/active; lửa, đèn, tinh thể phát sáng, nước bọt: dải 4 khung ngang (ví dụ 4×64 px), cùng kích thước từng khung, cùng pivot.
9. KHÔNG vẽ chữ trong ảnh. KHÔNG dùng tên/logo/chữ của APK/JAR. Cờ, biểu tượng, hoa văn tự thiết kế.
10. Không dùng asset hiện tại trong apps/game-web/public/ (placeholder).

PHONG CÁCH
- Pixel art sạch cụm màu lớn; outline sẫm theo sắc vật (không đen tuyền); đổ khối 2–4 tông.
- Nguồn sáng chuẩn: trên-trái-phía trước, ấm; bóng hơi lạnh. Không vẽ bóng đổ xuống đất.
- Góc nhìn: tile nhìn từ trên hơi chếch, không phối cảnh; prop là billboard đứng, thấy mặt trước + hơi mặt trên (~24°).
- Cùng bảng màu và cùng độ dày outline giữa các mảnh trong một kit.

TỰ KIỂM TRA TRƯỚC KHI NỘP (bắt buộc, dán kết quả vào qa.json mỗi asset)
size đúng manifest · mode RGBA · số pixel alpha ∉ {0,255} = 0 · số màu ≤ 48 · lề ≥ 8 px · số cụm vụn lạc = 0 ·
số pixel hồng = 0 · seam X/Y (tile/backdrop) · số khung = khai báo. Nếu có chỉ số không đạt: sửa, KHÔNG ghi "đã sửa" khi chưa đo.
```

## Phần B — Quy ước đặt tên & nộp bài

- Thư mục: `apps/game-web/art-src/hd2d/batch-11-<kit>/<id>/final.png` (+ `prompt.md`, `qa.json`, `repeat-3x3.png` nếu tile).
- `id`: kebab-case, tiền tố theo kit (`desert-sand-tile-01`, `desert-cactus-02`, `tomb-gravestone-03`).
- `manifest.json` mỗi kit, mỗi asset: `id, category(tile|prop|decal|backdrop|fx|marker), kit, file, px[w,h], world[w,h], pivot, tileable(none|x|xy), frames, fps, sway(none|canopy|trunk), source_refs[], replaces`.
- Mỗi kit phải có thêm `palette.json` (≤ 48 màu chính của kit) và `contact-sheet.png` có nhãn id.
- Ảnh phải thật sự là artwork vẽ mới, không copy/scale ảnh gốc APK.
- **NPC không vẽ ở đợt này.** Roster 107 NPC giữ id gốc ở `.ai/plan/phases/P12-world/stage4/P12-S4-npc-roster.json`; 54 NPC của các map dưới đây chưa có art đúng id, xem Phần E.

## Phần C — 17 kit và 75 map


### kit_desert — Hoang mạc (level6) — 6 map

**Phong cách/bảng màu:** Cát vàng ấm, đá sa thạch đỏ cam, trời xanh gắt. Bảng màu: cát #D9B26B/#B88A44, đá #A5522B, bóng lạnh tím nhạt.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile cát gợn sóng (2 biến thể), cát nứt khô, đá sa thạch phẳng, nền phế tích lát đá; prop: xương quái khổng lồ, xương rồng ×3, đá tảng ×3, cột phế tích gãy ×3, tường phế tích, lều du mục ×2, cổng phong ấn đá, bia chữ cổ (không chữ), giếng, đống cát, cây gai khô; backdrop xa: cồn cát + phế tích thành xa.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `desert_shicheng_ruins` | Sa Thạch Cổ Thành | 3 | không | 0 | desert_aven, desert_brisa, desert_calder, desert_dalia |  |
| `desert_entrance` | Cửa Ngõ Hoàng Mạc | 2 | có | 12 | desert_edda |  |
| `desert_sealed_land` | Phong Ấn Cổ Địa | 1 | có | 12 | — |  |
| `desert_hulu_tribe` | Bộ Lạc Hồ Lô | 3 | có | 10 | desert_fenwick |  |
| `desert_barren_sands` | Hoang Sa Vô Tận | 1 | có | 12 | desert_galen |  |
| `desert_disaster_sands` | Tai Ương Sa Mạc | 1 | có | 10 | — |  |

### kit_windrock — Núi Phong Thạch (level7) — 6 map

**Phong cách/bảng màu:** Đá xám lam, cỏ núi khô, tuyết lốm đốm trên cao, gió mạnh (cờ/cỏ nghiêng). Bảng màu đá #7B8794/#566070, cỏ khô #8A8F4E, tuyết #E8EEF4.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile đá núi nứt, đất sỏi, cỏ núi, tuyết mỏng, lát đường núi; prop: cầu treo gỗ (đoạn lặp + cọc + đoạn đứt), cột đá gió bào ×3, vách đá nhô ×3, thông núi ×3 (sway-split), lều trại, đống lửa trại (4 khung), rào gỗ, biển chỉ đường (không chữ); backdrop xa: dãy núi tuyết 2 tầng, hẻm núi.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `windrock_mountain_camp` | Trại Phong Thạch | 3 | không | 0 | wind_hesper, wind_iris, wind_jorin, wind_kestra |  |
| `windrock_mountain_stone_bridge` | Cầu Thiên Thạch | 2 | có | 12 | wind_loren |  |
| `windrock_mountain_howling_canyon` | Hẻm Gió Gào | 1 | có | 12 | — |  |
| `windrock_mountain_mountain_range` | Dãy Phong Lĩnh | 2 | có | 12 | wind_mirel |  |
| `windrock_mountain_mountain_path` | Sơn Đạo Phong Vân | 2 | có | 12 | wind_nolan |  |
| `windrock_mountain_summit` | Đỉnh Thiên Phong | 1 | có | 10 | wind_orla |  |

### kit_nightmare — Đảo Ác Mộng (level8) — 6 map

**Phong cách/bảng màu:** Đất tím sẫm nứt phát quang, cây hắc ám, tinh thể bóng tối. Bảng màu: #3A2B52/#5B3F7A, vết nứt phát sáng #B26BFF, rêu độc #4E7A4A.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile đất tím nứt, đá đen, nền phế tích; prop: rễ hắc ám ×3, cây khô xoắn ×3 (sway-split), tinh thể bóng tối ×3, cổng ma pháp đen (dormant/active), xương/di vật, tàn tích tường, trại tàn sinh (lều rách, đống lửa 4 khung), đèn ma trơi (4 khung); backdrop xa: đảo đen giữa biển tím, trăng.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `nightmare_island_survivor_camp` | Trại Tàn Sinh | 4 | có | 5 | night_pavel, night_quinn, night_rhea |  |
| `nightmare_island_east_magic_island` | Đông Đảo Huyền Thuật | 2 | có | 12 | night_soren |  |
| `nightmare_island_ruins` | Phế Tích Cổ Thành | 1 | có | 10 | night_talia |  |
| `nightmare_island_disaster_gate` | Cổng Tai Kiếp | 1 | có | 10 | — |  |
| `nightmare_island_resentment_path` | Oán Linh Hải Đạo | 2 | có | 12 | night_ulric |  |
| `nightmare_island_despair_land` | Tuyệt Vọng Hải Địa | 1 | có | 12 | night_vesna |  |

### kit_tomb — Lăng Mộ (level9) — 9 map

**Phong cách/bảng màu:** Gạch mộ rêu phong, đá xám xanh, ánh đèn ma xanh lục. Hai khu ngoài (Cồn Úa Vàng, Bãi Gai Khô) là sa mạc vàng cây gai khô.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile gạch mộ, đá lát rêu, đất nghĩa địa, cát vàng khô (2 khu ngoài); prop: bia mộ ×4, quách đá ×2, cổng vòm mộ, tượng thần vỡ ×2, đèn lồng ma trơi (4 khung) ×2, hố mộ, tường tàn tích ×3, cột gãy ×3, bó xương, cây gai khô ×3; backdrop xa: tường thành mộ, đồi nghĩa trang.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `tomb_region_camp` | Trạm Canh Lăng | 3 | không | 0 | tomb_wren, tomb_xan, tomb_yara, tomb_zora | hub của vùng Lăng Mộ |
| `tomb_region_resentment_path` | Oán Linh Cổ Đạo | 2 | có | 15 | tomb_alder |  |
| `tomb_region_despair_path` | Tuyệt Vọng Chi Địa | 2 | có | 15 | — |  |
| `tomb_region_dead_ruins` | Tàn Tích Tịch Diệt | 2 | có | 0 | — |  |
| `tomb_region_deep_ruins` | Thâm Cung Tịch Diệt | 1 | có | 0 | — | cụt, nối từ Tàn Tích Tịch Diệt |
| `tomb_region_gods_tomb` | Thần Lăng Vĩnh Miên | 1 | có | 0 | tomb_bram |  |
| `tomb_region_soul_cemetery` | Bãi Vãng Sinh | 4 | có | 6 | tomb_cora, tomb_dov | hub: nối Thần Lăng + 2 khu chưa tên |
| `tomb_region_unnamed_area_01` | Cồn Úa Vàng | 1 | có | 0 | — | cụt; sa mạc vàng, cây gai khô |
| `tomb_region_unnamed_area_02` | Bãi Gai Khô | 1 | có | 0 | — | cụt; cùng nền với 01 |

### kit_crossroads — Ngã Tư / Địa Đạo (Giao Điểm) (level10) — 6 map

**Phong cách/bảng màu:** Hang địa đạo xanh lam đêm, rêu biếc, thủy quang, san hô tím. Một chuỗi phòng cùng nền, đổi sắc nhẹ theo phòng.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile đá hang ẩm, đường mòn đá cuội, rêu biếc, mặt nước nông (viền bọt 4 khung), đáy hang; prop: măng đá ×4, thạch nhũ treo ×3, san hô tím ×3, nấm phát quang ×3, ván cầu đá, cột đá chống hầm, đèn hang, cổng hầm; backdrop xa: vách hang sâu, ánh sáng cửa hang.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `crossroads_unnamed_area_01` | Cổng Địa Đạo Lam Dạ | 3 | không | 0 | cross_elric, cross_fara | nối Quảng trường; hub 02 + 05 |
| `crossroads_unnamed_area_02` | Hành Lang Rêu Biếc | 2 | có | 12 | — | chuỗi 01→02→03→04→06 |
| `crossroads_unnamed_area_03` | Đoạn Thủy Quang | 2 | có | 12 | cross_gwen |  |
| `crossroads_unnamed_area_04` | Ngã Ba Đêm Xanh | 2 | có | 10 | cross_hale |  |
| `crossroads_unnamed_area_05` | Hốc San Hô Tím | 1 | có | 10 | cross_ines | cụt, nhánh từ 01 |
| `crossroads_unnamed_area_06` | Đáy Địa Đạo | 1 | có | 10 | — | cuối chuỗi |

### kit_astral — Tinh Giới (Khe nứt thời không) (level12) — 7 map

**Phong cách/bảng màu:** Cảnh ma mị: rừng mây tím, hoàng hôn, hồ vân ảnh, cổ thụ; Khe nứt thời không phát sáng. Bảng màu: tím #5B4A9B, hồng hoàng hôn #E08AA0, vàng #F2C879.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile mặt đất tím/hoàng hôn, đường mây lát đá, cỏ tím; prop: cây tím ×3 (sway-split), cổ thụ rỗng (Hốc Cổ Thụ), tinh thể pha lê ×3, đá lơ lửng ×3, hoa phát sáng, vòng xoáy khe nứt (4 khung), bờ hồ (viền), cầu mây; backdrop xa: dải ngân hà, mây tím, núi trôi.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `astral_realm_unnamed_area_01` | Tử Vân Lâm | 4 | không | 0 | astral_joss, astral_kira | hub: 02, 04, 05 + Khe nứt |
| `astral_realm_spacetime_rift` | Thời Không Liệt Khích | 2 | không | 0 | — | nối Hải Tặc Hào |
| `astral_realm_unnamed_area_02` | Lối Mây Tím | 2 | có | 10 | astral_lars | →03 |
| `astral_realm_unnamed_area_03` | Bờ Hồ Vân Ảnh | 1 | có | 10 | — | cụt |
| `astral_realm_unnamed_area_04` | Hốc Cổ Thụ | 1 | có | 12 | — | cụt |
| `astral_realm_unnamed_area_05` | Rừng Hoàng Hôn | 2 | có | 10 | astral_mara | →06 |
| `astral_realm_unnamed_area_06` | Tận Cùng Thời Không | 1 | có | 12 | — | cụt |

### kit_ancient — Cổ Tích (Tiền Sảnh Ngọc Lục) (level13) — 6 map

**Phong cách/bảng màu:** Điện đá ngọc lục bích, tượng cổ, tinh thạch; chuỗi phòng trong nhà (có tường).

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sàn đá ngọc lục, sàn hoa văn, thảm đá; prop (tường/cột): tường phòng trong module, cột chạm ×3, tượng thần ×3 (một vỡ), bệ tế lễ, tinh thạch xanh ×3 (phát sáng, 4 khung), đèn đá, cổng đá, bậc thang; backdrop xa: sảnh điện sâu.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `ancient_ruins_unnamed_area_01` | Tiền Sảnh Ngọc Lục | 4 | không | 0 | ancient_neth, ancient_olin | nối Hải Tặc Hào; hub 02, 03, 04 |
| `ancient_ruins_unnamed_area_02` | Phòng Tượng Cổ | 1 | có | 0 | ancient_perrin | cụt |
| `ancient_ruins_unnamed_area_03` | Phòng Tinh Thạch | 1 | có | 0 | — | cụt |
| `ancient_ruins_unnamed_area_04` | Hành Lang Thạch Vệ | 2 | có | 0 | ancient_rue | →05 |
| `ancient_ruins_unnamed_area_05` | Thâm Sảnh Ngọc Lục | 2 | có | 0 | ancient_sable | →06 |
| `ancient_ruins_unnamed_area_06` | Tận Điện Cổ Tích | 1 | có | 0 | — | cụt |

### kit_ghost_castle — Lâu Đài Ma (level14) — 3 map

**Phong cách/bảng màu:** Đá cẩm thạch đen nứt, rèm nhung rách, nến bạc, rừng U Lâm xanh bích.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sàn cẩm thạch đen, thảm rách, cỏ khô nghĩa địa; prop: cổng lâu đài sắt, tường lâu đài, tháp canh nhỏ, rèm rách ×2, chân nến bạc (lửa 4 khung), tranh chân dung (không mặt nhận diện), tủ sách mục, cây khô ×3, đèn ma; backdrop xa: lâu đài trên đồi + trăng.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `ghost_castle_gate` | Cổng U Lâu | 2 | không | 0 | ghost_tove, ghost_una |  |
| `ghost_castle_deep_woods` | U Linh Cổ Thành | 2 | có | 25 | — | tên nguồn trùng với 2 map khác |
| `ghost_castle_ancient_city_secret_chamber` | Mật Thất Cổ Thành | 1 | có | 20 | — |  |

### kit_world_tree — Cây Thế Giới (level15) — 3 map

**Phong cách/bảng màu:** Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile vỏ cây/cành lát, rêu, lá rụng; prop: rễ khổng lồ ×3, lá khổng lồ ×3 (sway), nấm khổng lồ, quả thần phát sáng (4 khung), cổng tán cây, bậc thang cành, dây leo, đom đóm (4 khung); backdrop xa: thân cây vươn tới trời, tán lá.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `world_tree_gate` | Thế Thụ Môn | 2 | không | 0 | tree_vik, tree_willa |  |
| `world_tree_deep_woods` | Thế Thụ Thâm Lâm | 2 | có | 17 | — | tên nguồn trùng |
| `world_tree_secret_chamber` | Mật Thất Thế Thụ | 1 | có | 17 | — |  |

### kit_tower — Điểu Tháp (level16) — 3 map

**Phong cách/bảng màu:** Tháp đá cao nhìn trên mây, đá lục giác phù văn, lan can kim loại; rừng Vân Tiêu Thiên Tầng xanh lam.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sàn đá lục giác phù văn, đá lát tháp, cỏ tầng thượng; prop: lan can kim loại (đoạn lặp), cột tháp ×3, cửa chuyển tầng (dormant/active), tượng chim đá ×2, lông vũ khổng lồ, đèn tháp, bậc thang xoắn; backdrop xa: biển mây từ trên cao.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `tower_region_main_tower` | Điểu Tháp | 2 | không | 0 | tower_yves, tower_zane | 'Tháp Chim' là đề xuất sửa chính tả trong NAMING-REVIEW |
| `tower_region_deep_woods` | Vân Tiêu Thiên Tầng | 2 | có | 17 | tower_aria | tên nguồn trùng |
| `tower_region_secret_floor` | Điểu Tháp Mật Tầng | 1 | có | 17 | — |  |

### kit_maze — Mê Thành Bất Tử (level17) — 3 map

**Phong cách/bảng màu:** Tường mê cung dây leo rậm, cổng đá chuyển dịch, bẫy chông sàn; xanh rêu + đá xám.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sàn đá mê cung, cỏ, sàn bẫy; prop: tường mê cung (module lặp + góc + đầu cụt), dây leo, cổng đá chuyển dịch (dormant/active), bẫy chông (thu/ra 4 khung), cột đá ×2, đèn đá, bụi rậm ×3; backdrop xa: mê cung vô tận.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `immortal_maze_main_maze` | Trường Sinh Mê Thành | 2 | không | 0 | maze_bex, maze_cleo | giữ nguyên, đã hợp style |
| `immortal_maze_floor` | Bất Tử Mê Tầng | 2 | có | 30 | maze_dune | tên nguồn quá chung |
| `immortal_maze_secret_floor` | Bất Tử Mật Tầng | 1 | có | 30 | — |  |

### kit_guild — Bang Hội (6 phòng) (level18) — 6 map

**Phong cách/bảng màu:** Đá granit kiên cố, cờ quân kỳ bang hội xanh/vàng (cờ tự thiết kế, không dùng logo gốc); trong nhà gỗ + đá ấm.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sàn đá granit, sàn gỗ, thảm bang, sân huấn luyện; prop: tường thành lũy (module), cổng thành, tháp canh, cờ ×2 màu, kho báu (rương đầy, vàng chất đống), kệ kho, thùng/bao tải ×4, giường doanh trại, giá vũ khí, quầy hàng, chuồng linh thú ×2 + rơm; backdrop xa: tường thành.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `guild_fortress` | Thành Lũy Bang Hội | 6 | không | 0 | — | hub dịch vụ bang |
| `guild_treasury` | Ngân Khố Bang | 1 | không | 0 | — |  |
| `guild_warehouse` | Kho Vật Tư Bang | 1 | không | 0 | — |  |
| `guild_barracks` | Doanh Trại Bang | 1 | không | 0 | — |  |
| `guild_shop` | Quầy Hàng Bang | 1 | không | 0 | — |  |
| `guild_pet_stable` | Chuồng Linh Thú | 1 | không | 0 | — |  |

### kit_battlefield — Chiến Địa Kết Minh (level19) — 1 map

**Phong cách/bảng màu:** Đất cháy xém, vũ khí cắm đất, chiến xa hỏng, tháp canh gỗ; khói lửa.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile đất cháy, đất nứt, cỏ cháy; prop: vũ khí cắm ×4, chiến xa hỏng, tháp canh gỗ, rào chắn, cờ rách ×2 màu, hố bom, đống lửa (4 khung), xương/giáp vỡ; backdrop xa: chân trời khói lửa.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `guild_battlefield_main_field` | Chiến Địa Kết Minh | 1 | không | 0 | — |  |

### kit_maya — Điện Thờ Maya · Tầng I (level20) — 1 map

**Phong cách/bảng màu:** Kim tự tháp đá xanh xám, hoa văn thần mặt trời (tự thiết kế), rừng nhiệt đới nguyên sinh.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sàn đá chạm, bậc thang kim tự tháp, rêu; prop: đài hiến tế, cột chạm ×3, tượng mặt trời, đầu rắn đá, đuốc (4 khung), dây leo nhiệt đới, cây nhiệt đới ×3; backdrop xa: rừng nguyên sinh + kim tự tháp.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `maya_floor_01` | Cổ Điện Tế Lễ · Tầng I | 1 | có | 0 | — | nhãn game: 'Điện thờ Maya' (Lv25–30) |

### kit_dungeon — Địa Lao · Tầng I (level21) — 1 map

**Phong cách/bảng màu:** Tường đá ẩm rêu xanh, ngục sắt, xích treo, vũng nước.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sàn đá ẩm, rãnh nước, rơm ngục; prop: cửa ngục sắt (đóng/mở), xích treo tường ×3, vũng nước (viền), đuốc tường (4 khung), xương, thùng/giá tra tấn (không máu), cầu thang; backdrop xa: hành lang ngục sâu.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `dungeon_floor_01` | Địa Lao · Tầng I | 1 | có | 0 | — |  |

### kit_arena2 — Đấu Trường Hỗn Mang / Tổ Đội (level22-23) — 2 map

**Phong cách/bảng màu:** Dùng lại kit Huyết Chiến Đài (batch-02) cho cột/cờ/giá vũ khí; thêm nền cát/đất đấu trường và khán đài khác màu cho mỗi đấu trường (hỗn mang: đỏ cam; tổ đội: xanh lam).

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile sân đấu (2 biến thể mỗi đấu trường), vòng ranh giới đội, khán đài module; prop: cột cờ đội đỏ/xanh, cổng vào, bục điểm hồi sinh, giá vũ khí (tái dùng), bảng điểm (không chữ); backdrop xa: khán đài ngoài trời.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `chaos_arena_main_field` | Đấu Trường Hỗn Mang | 1 | không | 0 | — |  |
| `team_arena_main_field` | Đấu Trường Tổ Đội | 1 | không | 0 | — |  |

### kit_minigame — Sói – Cừu (level24) — 6 map

**Phong cách/bảng màu:** Hai bên: sân cỏ xanh (cừu) và sân đá u ám (sói); bãi giữa cỏ xanh trung tính; sảnh chờ trong nhà.

**Mảnh tối thiểu cần vẽ cho kit (chung cho các map bên dưới):** tile cỏ xanh, cỏ khô vàng, đất đá sói, sàn gỗ nhà; prop: rào gỗ chuồng cừu (đoạn+cọc+cổng), đống cỏ khô ×2, máng cừu, nhà cừu (backdrop mid), hang đá sói, xương, rào đá sói, nhà sói, cờ 2 phe, bục xuất phát, cỏ/hoa ×4; backdrop xa: đồi cỏ.

Mỗi kit thêm: 1 `marker` điểm xuất hiện/dịch chuyển (vòng sáng, 4 khung), 1 cặp `portal dormant/active` đúng tông kit, 1 decal viền lối đi/chuyển tiếp nền (edge) cho mỗi cặp tile nền chính.

| map_id | Tên hiển thị | Số cổng | Vùng quái | Điểm spawn | NPC roster | Ghi chú |
|---|---|---|---|---|---|---|
| `wolf_sheep_waiting_hall` | Sảnh Đối Quyết Lang Dương | 1 | không | 0 | — |  |
| `wolf_sheep_sheep_house` | Dương Xá | 1 | có | 0 | — |  |
| `wolf_sheep_sheep_pen` | Dương Lan | 2 | có | 0 | — |  |
| `wolf_sheep_middle_field` | Bãi Tranh Đoạt | 2 | không | 0 | — |  |
| `wolf_sheep_wolf_pen` | Lang Huyệt | 2 | có | 0 | — |  |
| `wolf_sheep_wolf_house` | Lang Sào | 1 | có | 0 | — |  |

## Phần D — Bàn giao & nghiệm thu

1. Giao theo kit; mỗi kit một thư mục `batch-11-<kit>`. Không gộp 17 kit một lần.
2. Mỗi kit nộp: `final.png` từng mảnh, `manifest.json`, `palette.json`, `contact-sheet.png`, `qa.json` từng mảnh với số đo thật.
3. Claude sẽ chạy lại audit riêng (`audit.py`) và chỉ nhận kit khi 0 lỗi: size, RGBA, bán trong suốt, màu ≤ 48, lề, vụn lạc, hồng, seam, số khung.
4. Thứ tự đề xuất (theo số map và giá trị): Lăng Mộ → Hoang Mạc → Núi Phong Thạch → Đảo Ác Mộng → Giao Điểm → Tinh Giới → Cổ Tích → Bang Hội → Lâu Đài Ma → Cây Thế Giới → Điểu Tháp → Mê Thành → Sói–Cừu → Chiến Địa → Điện Maya → Địa Lao → Đấu trường 2.
5. Mỗi kit nên nộp một **map mẫu đại diện** (ghép thử thành một ảnh phẳng 1 góc để Claude xem bảng màu), nhưng ảnh ghép này chỉ để tham khảo, không dùng làm asset.

## Phần E — Việc kèm theo (tách riêng, không trộn với vẽ map)

- **NPC:** 54 NPC roster thuộc các map trên chưa có ảnh đúng id. Vòng trước Gemini/GPT đặt 58 NPC id khác roster (`desert_01`, `tree_01`...) nên không gắn được. Yêu cầu đợt NPC riêng: dùng ĐÚNG id từ `P12-S4-npc-roster.json` (ví dụ `desert_aven`, `desert_brisa`), cùng chuẩn 192×192, thân 168 px, idle 4 khung.
- **Sửa lỗi cũ chưa đạt (xem `hd2d-art-acceptance-20261015.md`, mục tái nghiệm thu):** batch-07 chưa lượng tử hóa; batch-09 còn bán trong suốt; batch-08 panel nhiều màu; login painterly; 9 mảnh map mới chưa ≤ 48 màu hoặc không seamless. Làm trước hoặc song song, không làm chung phiên với vẽ map.
