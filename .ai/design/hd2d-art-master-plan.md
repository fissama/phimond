# Phimond — Master plan vẽ lại toàn bộ đồ họa sang HD-2D (cho GPT 6 Astra)

- **Ngày:** 2026-10-15 · **Trạng thái:** bản nháp để chủ dự án duyệt trước khi giao việc
- **Phạm vi:** mọi asset hình ảnh của game, **trừ** atlas 160 species (P10 redraw đã xong 152/152 + 8 proposal)
- **Phân vai:** GPT 6 Astra **chỉ vẽ asset rời** (từng tile, prop, backdrop, mảnh UI, icon, FX) + manifest. **Claude dựng cảnh HD-2D** (scene JSON, ánh sáng, sương, hạt, nước, bố cục HUD) từ các mảnh đó. Astra không sửa runtime, không ghép cảnh.
- **Ưu tiên:** bản đồ và họa tiết nhỏ trước (Đợt 1–4), rồi HUD/menu/icon/FX.

Cách dùng: dán nguyên **Phần A (Master prompt)** vào phiên Astra, rồi dán **một** khối "Đợt N" ở Phần D. Mỗi phiên chỉ làm một đợt.

---

## Phần A — MASTER PROMPT (dán cho Astra)

```text
Bạn là art worker cho dự án Phimond (game nuôi linh thú, dựng lại từ 靈獸世界 Online / PokeZoo,
client web Three.js HD-2D). Repo: /Users/phileanh/rust/phimond. Đọc AGENTS.md trước.
Dùng công cụ tạo ảnh có sẵn của bạn để VẼ. Văn bản mô tả không phải artwork. Nếu không có công cụ
tạo ảnh, dừng và báo; không vẽ hình khối bằng Python, không dùng API trả phí thay thế.

MỤC TIÊU
Vẽ lại toàn bộ asset của đợt được giao sang phong cách HD-2D pixel art, đẹp hơn hẳn bản hiện tại
(bản hiện tại do một model không chuyên vẽ dựng tạm, coi là placeholder, KHÔNG dùng làm style).
Bạn chỉ xuất ASSET RỜI + manifest. Một agent khác (Claude) sẽ ghép chúng thành cảnh 3D HD-2D.
Vì vậy: KHÔNG vẽ cảnh ghép hoàn chỉnh, KHÔNG nướng ánh sáng/sương/bóng đổ vào asset.

NGUỒN ĐƯỢC DÙNG (chỉ những nguồn này)
1. Asset gốc APK/JAR liệt kê trong phần đợt (đường dẫn tuyệt đối hoặc tương đối repo). Đây là
   nguồn NỘI DUNG: hình khối, bố cục, chủng loại vật thể, bảng màu gốc. Mở bằng công cụ xem ảnh
   trước khi vẽ. Đính kèm ảnh thật vào công cụ tạo ảnh; nhắc tên file trong văn bản là chưa đủ.
2. Hai style anchor đã duyệt của linh thú (CHỈ để khớp độ dày outline, cách đổ khối, độ bão hòa):
   apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png
   apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png
3. Các asset đã được chủ dự án duyệt ở đợt trước (Đợt 0 là style anchor môi trường/UI).
Không dùng: asset hiện tại trong apps/game-web/public/ (placeholder), ảnh từ internet, tên riêng
hay chữ lấy từ APK/JAR (tên map/NPC dùng bảng tên Việt đã duyệt, xem
.ai/plan/phases/P12-world/P12-world-names-master.md). Không vẽ chữ vào ảnh trừ khi đợt yêu cầu.

STYLE BIBLE HD-2D (áp dụng mọi asset)
- Pixel art sạch: cụm màu lớn, rõ; outline màu tối theo sắc của vật (không đen tuyền) ở mép ngoài;
  đổ khối 2–4 tông; bão hòa có kiểm soát; ăn khớp với hai anchor linh thú.
- Engine hiển thị bằng NearestFilter: không anti-alias mờ, không gradient mượt kiểu vector, không
  texture nhiễu li ti, không bloom/glow nướng sẵn, không viền trắng quanh vật.
- Nguồn sáng chuẩn: trên-trái-phía trước, ấm (key) + bóng hơi lạnh. Không vẽ bóng đổ xuống đất:
  engine tự vẽ bóng tiếp đất. Không vẽ sương/mờ chiều sâu/DOF: engine tự làm (fog, grade, bloom).
- Góc nhìn: camera phối cảnh fov 30°, nhìn xuống 24°. Prop/nhân vật là billboard đứng: vẽ mặt
  trước, thấy nhẹ mặt trên (~24°). Tile nền vẽ nhìn từ trên xuống hơi chếch, không phối cảnh.
- Mật độ điểm ảnh (ràng buộc cứng để mọi mảnh khớp nhau):
  * Prop, nền, decal, backdrop gần: 128 px cho mỗi 1 đơn vị world (1 ô lưới = 0,52 đơn vị ≈ 66 px).
  * Backdrop xa (far): 64 px/đơn vị.
  * Nhân vật người/NPC: cao ~1,3 đơn vị → thân ~160–170 px trong ô 192×192.
  * UI: vẽ @3x so với canvas thiết kế 960×640 (ví dụ nút 67×62 gốc → 201×186).
  * Icon: master 256×256, phải đọc rõ khi thu về 32×32.
- Bảng màu theo vùng (biome) ghi trong khối đợt; giữ nhất quán giữa các mảnh cùng bộ kit.

ĐỊNH DẠNG ĐẦU RA (ràng buộc cứng)
- PNG RGBA, nền trong suốt thật (không checkerboard nướng sẵn), trừ tile nền và backdrop phủ kín.
- Mỗi asset một file. Nếu công cụ sinh ra sheet nhiều vật, bạn phải cắt thành file rời và giữ sheet
  gốc byte-identical làm raw. Lề alpha ≥ 8 px quanh mỗi prop/icon/mảnh UI.
- Tile nền: liền mạch bốn phía (seamless), kích thước 512×512 (= 4×4 đơn vị), kèm 2–3 biến thể và
  tile chuyển tiếp mép (nền→lối đi, nền→nước) nếu khối đợt yêu cầu.
- Backdrop: dải ngang lặp liền mạch trái-phải (đuôi khớp đầu), cao theo khối đợt, mép dưới trong
  suốt mềm để ghép vào nền.
- Prop: pivot = giữa đáy (chân chạm đất). Cây/bụi/cỏ có thể lay: tách thân và tán nếu khối đợt ghi
  "sway-split"; không để vật thể đè lên viền ảnh.
- Mảnh UI co giãn: 9-slice, ghi rõ 4 lề slice trong manifest; không chữ, không số nướng sẵn.
- Nút nghiêng (viên thuốc nghiêng 37°): vẽ trống, engine đặt chữ xoay theo trục.
- Animation (FX, NPC idle, đuốc, nước…): sheet ngang N khung cùng kích thước, ghi fps gợi ý.
- Thư mục ghi: apps/game-web/art-src/hd2d/<đợt>/<asset_id>/
    raw-01.png (đầu ra công cụ, không sửa), final.png (đã cắt/sửa), prompt.md (prompt + danh sách
    ảnh đính kèm theo thứ tự + sha256), review.md (tự review).
- Manifest đợt: apps/game-web/art-src/hd2d/<đợt>/manifest.json, mỗi asset một bản ghi:
  { "id", "category": "floor|edge|decal|backdrop_far|backdrop_mid|prop|prop_sway|light|fx|npc|
    player|ui_9slice|ui_sprite|icon|font|login",
    "kit", "file", "px": [w,h], "world": [w,h] (đơn vị world, suy từ 128 px/đv),
    "pivot": "bottom_center|center", "tileable": "none|x|xy", "slice": [l,t,r,b] | null,
    "frames": n, "fps": n | null, "sway": bool, "source_refs": ["đường dẫn gốc", ...],
    "replaces": "đường dẫn placeholder hiện tại" | null, "notes" }
  "replaces" giúp Claude biết mảnh nào thay mảnh nào; "world" giúp Claude đặt đúng tỉ lệ.

PHẠM VI GHI VÀ AN TOÀN
- Chỉ ghi trong apps/game-web/art-src/hd2d/<đợt>/. Không sửa public/, scene JSON, mã nguồn,
  catalog, dữ liệu APK/JAR, tài liệu .ai (trừ file báo cáo của đợt nếu được yêu cầu).
- Không commit, không push, không kích hoạt asset vào game. Giữ nguyên thay đổi dở của người khác.
- Tối đa 3 lần sinh ảnh cho một asset; thất bại thì để lại attempt, ghi lý do, sang asset kế.

QUY TRÌNH MỖI ASSET
1. Mở ảnh nguồn trong khối đợt, ghi "thẻ nhận diện" ngắn vào review.md: vật gì, hình khối, màu chủ
   đạo, chi tiết đặc trưng, kích thước world dự kiến.
2. Viết prompt từ template Phần C, đính kèm ảnh nguồn + anchor + asset đã duyệt cùng kit.
3. Sinh ảnh, lưu raw-01.png nguyên vẹn, xem lại ngay.
4. Cắt/căn lề/kiểm tra alpha → final.png. Không vẽ đè thủ công bằng code ngoài cắt, dịch, xóa nền.
5. Kiểm tra cơ học (Phần E) + xem ở 1x và 2x trên nền sáng và tối; với tile: ghép 3×3 kiểm seam.
6. Tự review theo checklist Phần E; ghi pass/sửa lại.

BÁO CÁO CUỐI ĐỢT
Một contact sheet PNG (mọi final.png theo kit, có nhãn id), manifest.json, danh sách asset
thiếu/blocked kèm lý do. Trả về đường dẫn. Chủ dự án duyệt; chỉ sau khi duyệt Claude mới dựng cảnh.
```

---

## Phần B — Kho nguồn gốc (để Astra tìm file nhanh)

| Nguồn | Đường dẫn | Có gì |
|---|---|---|
| Ảnh ghép tĩnh 92 map (APK 3.2) | `/Users/phileanh/Downloads/Phimond-P12-Review/map-images/<map_id>.png` + `map-images.json` (scene gốc, số sprite) | Tham chiếu bố cục và vật thể từng map |
| Sprite cắt rời của 5 map đang chạy | `tools/build-web-assets/source/sprites/{level3_QTTP, level3_NongTrai, level3_DauTruong, level4_rungsau, level5_BaiBien}/` + `meta.json` | Từng mảnh nền/prop gốc |
| Dump Unity APK 3.2 / 8.4 | `apps/game-client/assets/extracted/sbw_v32/{Texture2D,Sprite}/`, `.../sbw_v84/` | Toàn bộ texture/sprite gốc (tìm theo tên) |
| APK đã phân loại | `apps/game-client/assets/extracted/extended/{ui,buttons,chat,icons,hud,rooms,misc,fonts}/` | UI 94, nút 9, chat 4, icon 309, HUD/rank 67, màn tải/đăng nhập 28, linh tinh ~1500 |
| HUD gốc đã chọn lọc | `apps/game-client/assets/reference/hud/` + `hud.json`; `reference/ui/` (UI.png, right_btn0–2, tableitem) | 44 sprite HUD và vị trí |
| Bố cục HUD gốc (960×640) | `apps/game-client/scripts/classic_hud.gd`, `.ai/plan/phases/P12-world/P12-stage3-hud-analysis.md`, `docs/research/HUD_REFERENCE.md` | Tọa độ từng phần tử |
| Người chơi / NPC gốc | `apps/game-client/assets/reference/actors/{Boy,Girl}/`, `reference/npcs/`, `.ai/plan/phases/P12-world/stage4/P12-S4-npc-roster.json` (49 NPC, trường `apk_sprite`) | Sprite và vai trò NPC |
| JAR Pokezoo 1.00 (xem được) | `/Users/phileanh/Downloads/Pokezoo-100-extracted/viewable/` (`index.html`) | `assets/sprites/` 58 gói 965 frame, `assets/original-png/` (intro1–3, logo, matingbg…), `assets/map-tiles/`, `animations/` (addcast, addhit, magcast, maghit, phycast, phyhit, levelup, mating, loadingAni…), `maps/area{5,6,19,33,34}/` |
| JAR — danh sách màn UI | `/Users/phileanh/Downloads/Pokezoo-100-extracted/viewable/ui-text/ui_*.txt` | 68 layout màn hình (tên + text dò được) |
| Asset placeholder hiện tại (sẽ bị thay) | `apps/game-web/public/scenes/tex/`, `public/scenes/*.json`, `public/assets/{ui,actors,login}/` | Chỉ để biết vai trò và kích thước, không dùng làm style |
| Trình xem cảnh | `apps/game-web/scene.html` (`src/dev/sceneview.ts`) | Claude dùng để xem cảnh đã ghép |

Tên hiển thị map/NPC: `.ai/plan/phases/P12-world/P12-world-names-master.md` và `P12-naming-proposal-jrpg.md`. Không vẽ tên gốc APK/JAR.

---

## Phần C — Template prompt cho công cụ tạo ảnh (tiếng Anh)

**C1. Tile nền / chuyển tiếp**
```text
Use case: game texture. Seamless 512x512 pixel-art ground tile for an HD-2D RPG (Octopath-like
pixel textures under 3D lighting). Biome: [KIT]. Surface: [grass with clover / packed dirt path /
cobblestone plaza / wet sand ...]. Content and palette follow the attached original tiles
(images 1..n): keep their materials and colors, redraw at higher fidelity. Style: crisp color
clusters, 2–4 tone shading, controlled saturation, matching the attached pet style sheets in
outline weight and saturation only. Viewed from above at a slight angle, no perspective.
Tiles seamlessly on all four edges. Even lighting: no baked shadows, no vignette, no fog.
No props, no text, no border, no checkerboard.
```
Biến thể chuyển tiếp: thêm "Edge tile: left half [A], right half [B], organic irregular boundary, tiles seamlessly top-bottom."

**C2. Bộ prop rời (sheet rồi cắt)**
```text
Use case: game sprites. A sprite sheet of [N] separate pixel-art props for biome [KIT] of an
HD-2D RPG, each isolated with wide transparent spacing, no overlaps: [list: oak tree large (≈3.2
world units tall → ~410 px), bush round, mushroom cluster, ...]. Identity from attached originals
(images 1..n): same object types, silhouettes and palette, redrawn cleaner and richer. Front view
seen from ~24° above, standing upright, flat ground contact at the bottom. Light from top-left,
warm key, cool shade. Dark hue-tinted outline, 2–4 tone shading, matching the attached pet style
sheets. Genuine transparent background. No cast shadow on the ground, no glow, no text, no
scenery behind the objects.
```

**C3. Backdrop**
```text
Use case: parallax backdrop strip. Horizontally seamless pixel-art strip [W]x[H] for biome [KIT]:
[distant forest wall / city skyline with towers / sea horizon with cliffs]. Left edge must
continue the right edge exactly. Bottom [k] px fades to transparent. Content from attached
originals. [far: simpler shapes, lower contrast, cooler]. No fog baked in, no sky gradient
(engine draws sky), no text.
```

**C4. UI 9-slice / sprite**
```text
Use case: game UI element. Pixel-art [panel / button / slot / tab / bar frame] for a fantasy
pet-raising RPG HUD, redrawn from the attached original APK element (image 1): keep its shape,
ornament motifs and color scheme, increase fidelity for a modern high-DPI screen (@3x). [For
9-slice: ornaments only in the corners and edges, center area flat and stretchable.] Provide
states side by side: normal, pressed, disabled [, selected]. No text, no numbers, transparent
background outside the element.
```

**C5. Icon sheet**
```text
Use case: icon set. [N] pixel-art icons on a grid, each 256x256 with 16 px transparent margin,
same lighting (top-left), same outline weight, readable at 32x32: [list]. Base each icon on the
attached original icon when given (images 1..n). Distinct silhouettes, no text.
```

**C6. FX / animation**
```text
Use case: VFX sprite sheet. [effect name] for an HD-2D RPG battle, [N] frames in one horizontal
row, each [S]x[S], transparent background, centered on a fixed pivot. Timing reference: attached
original animation frames. Pixel-art with hard color steps (the engine adds bloom), additive-
friendly colors on a transparent background, no black background.
```

**C7. NPC / người chơi**
```text
Use case: character sprite. Pixel-art NPC "[tên Việt + vai trò]" for an HD-2D RPG, one row of
[4] idle frames (subtle breathing), each 192x192, body ~165 px tall, bottom-center pivot, facing
three-quarter toward the viewer. Outfit/role from attached original sprite (image 1) and the role
note: [ghi chú từ npc roster]. Match outline and shading of the attached pet style sheets.
Transparent background, no ground shadow, no text.
```

---

## Phần D — Danh mục asset A–Z và các đợt

Ký hiệu cột Nguồn: `MI:` = `/Users/phileanh/Downloads/Phimond-P12-Review/map-images/`, `SP:` = `tools/build-web-assets/source/sprites/`, `JV:` = `/Users/phileanh/Downloads/Pokezoo-100-extracted/viewable/`, `EX:` = `apps/game-client/assets/extracted/extended/`, `RF:` = `apps/game-client/assets/reference/`, `PH:` = `apps/game-web/public/` (placeholder hiện tại).

### Đợt 0 — Style anchor (bắt buộc duyệt trước mọi đợt)
Mục tiêu: chốt "giọng" HD-2D cho môi trường và UI. Ba mảnh, mỗi mảnh 2–3 phương án:
1. Tile cỏ rừng 512² + 1 cây lớn + 1 bụi + 4 cụm cỏ/hoa (kit Rừng Lục Bảo). Nguồn: `SP:level4_rungsau/`, `MI:emerald_forest_main_woods.png`.
2. Tile đá lát quảng trường + 1 đèn đường + 1 thùng gỗ (kit Thành). Nguồn: `SP:level3_QTTP/`, `MI:city_square.png`, `JV:maps/area33/`.
3. Panel menu 9-slice + nút Chọn nghiêng (3 trạng thái). Nguồn: `RF:hud/panel_menu.png`, `RF:hud/button_confirm.png`, `RF:ui/UI.png`.
Đầu ra thêm: `style-guide.png` (bảng màu từng kit + mẫu outline/shading). Chủ dự án chọn phương án → thành anchor cho các đợt sau.

### Đợt 1 — Kit Rừng Lục Bảo + 2 map (ưu tiên cao nhất)
| Map ID | Tên | Nguồn |
|---|---|---|
| `emerald_forest_main_woods` | Bìa Rừng Lục Bảo | `MI:emerald_forest_main_woods.png`, `SP:level4_rungsau/` (đang dùng cho cảnh `PH:scenes/forest.json`) |
| `emerald_forest_deep_woods` | Rừng Sâu Lục Bảo | `MI:emerald_forest_deep_woods.png`, APK `level4` |

Danh sách mảnh (kit `forest`):
- Nền: cỏ ×3 biến thể, đất mòn ×2, chuyển tiếp cỏ→lối đi, cỏ→rễ cây/mép rừng.
- Decal (flats): sỏi ×3, lá rụng ×3, mảng rêu ×2, vệt bùn, vòng nấm.
- Cụm cỏ/hoa nhỏ (sway): cỏ ×4, hoa ×4 màu (đỏ, vàng, tím, trắng), dương xỉ ×2, cỏ lau.
- Prop: cây lớn ×3 dạng (sway-split), cây nhỏ ×2, bụi ×3, gốc cây, khúc gỗ đổ, đá ×3 cỡ, nấm to ×2, bụi hoa, cột đá rêu, cổng gỗ thô (lối ra), biển chỉ đường (trống chữ), rễ cây lộ.
- Backdrop: tường rừng xa (far, 64 px/đv), tán rừng giữa (mid), dải bụi tiền cảnh mép trước (front).
- Ánh sáng/hạt (sprite nhỏ để Claude dùng): tia nắng xuyên tán (sprite dải), đom đóm 4 khung, lá bay 4 khung, bào tử phát sáng.
- Điểm tương tác: cổng/lối chuyển map (2 trạng thái: thường, đang sáng), tổ quái (đất xới, có cỏ) đánh dấu nơi quái tuần tra.

### Đợt 2 — Kit Thành (9 map trong thành)
| Map ID | Tên | Nguồn |
|---|---|---|
| `city_square` | Quảng Trường Thạch Trụ | `MI:city_square.png`, `SP:level3_QTTP/`, `JV:maps/area33/` (thay `PH:scenes/severa.json`) |
| `city_market` | Thương Phố | `MI:city_market.png`, `JV:maps/area19/` |
| `city_palace_gate` | Hoàng Môn | `MI:city_palace_gate.png`, `JV:maps/area34/` |
| `city_royal_palace` | Vương Cung | `MI:city_royal_palace.png` |
| `city_activity_hall` | Vạn Sự Hội Sảnh | `MI:city_activity_hall.png` |
| `city_pet_room` | Phòng thú cưng | `MI:city_pet_room.png` |
| `city_farm` | Điền Trang Lục Dã | `MI:city_farm.png`, `SP:level3_NongTrai/`, `JV:maps/area5/` (thay `PH:scenes/ranch.json`) |
| `city_deathmatch_arena` | Huyết Chiến Đài | `MI:city_deathmatch_arena.png`, `SP:level3_DauTruong/` (thay `PH:scenes/arena.json`) |
| `summoning_hall_main_hall` | Triệu Linh Điện | `MI:summoning_hall_main_hall.png`, `JV:maps/area6/` |

Danh sách mảnh:
- Kit `city` ngoài trời: đá lát ×3, đá lát hoa văn tròn (tâm quảng trường), lối gạch, mép bồn cỏ; tường nhà mặt tiền ×4 kiểu (backdrop mid, ghép được), mái ngói, cửa hàng có mái bạt ×3 màu, quầy hàng chợ ×3 (rau, vải, vũ khí), đài phun nước (thân + sprite nước 4 khung), **trụ teleport Thạch Trụ** (tắt/sáng + vòng ma pháp 6 khung), đèn đường, cờ/băng rôn ×2 (sway), ghế dài, thùng, thùng gỗ, chậu hoa ×3, xe đẩy, giếng, tượng đá, bậc thềm, lan can, cây cảnh đô thị ×2.
- Kit `palace`: cổng hoàng cung lớn (backdrop mid), tường thành có tháp, lính gác tượng, thảm đỏ (decal dài lặp), cột đá chạm, ngai, đèn treo, rèm.
- Kit `hall` (nội thất: Vạn Sự Hội Sảnh, Phòng thú cưng, Triệu Linh Điện): sàn gỗ/đá nội thất ×2, tường trong (backdrop) ×2, kệ, bàn quầy, bảng nhiệm vụ, chuồng/ổ linh thú ×3, **3 bệ đá triệu hồi** (tắt/sáng), vòng phù văn sàn, nến/đuốc tường (4 khung), cửa ra (2 trạng thái).
- Kit `farm`: ruộng luống ×2, rào gỗ (đoạn lặp + cột), kho cỏ, đống rơm ×2, chuồng, cối xay gió (cánh quay 4 khung), máng ăn, giỏ, cây ăn quả, bù nhìn, lối đất, hoa đồng ×3.
- Kit `arena`: sàn đấu trường (tile), vạch/hoa văn tâm đấu trường (decal), khán đài (backdrop mid), cờ phe ×2, đuốc (4 khung), cột đá, giá vũ khí, bảng xếp hạng (trống chữ).

### Đợt 3 — Kit Bãi biển (5 map)
| Map ID | Tên | Nguồn |
|---|---|---|
| `treasure_beach_fishermen_beach` | Bến Ngư Châu | `MI:treasure_beach_fishermen_beach.png`, `SP:level5_BaiBien/` (thay `PH:scenes/beach.json`) |
| `treasure_beach_east_beach` | Bờ Đông Ngọc Bích | `MI:treasure_beach_east_beach.png` |
| `treasure_beach_west_beach` | Bờ Tây Hoàng Sa | `MI:treasure_beach_west_beach.png` |
| `treasure_beach_deep_sea` | Vực Hải Lam | `MI:treasure_beach_deep_sea.png` |
| `treasure_beach_prosperity_island` | Đảo Phú Quý | `MI:treasure_beach_prosperity_island.png` |

Mảnh (kit `beach`): cát khô ×2, cát ướt, chuyển tiếp cát→nước (Claude dùng shader nước, Astra vẽ viền bọt sóng 4 khung), cỏ biển; dừa ×3 (sway-split), đá bờ ×3, vỏ sò ×4, sao biển ×2, gỗ trôi dạt, cầu tàu gỗ (đoạn lặp + cọc), thuyền chài ×2, lưới phơi, nhà chòi ngư dân (backdrop mid), hải đăng, rương kho báu (đóng/mở), san hô ×3 (Vực Hải Lam), tảo bẹ (sway), bong bóng 4 khung; backdrop: biển xa + đảo, vách đá.

### Đợt 4 — Tàu cướp biển + vật thể tương tác dùng chung
- `middle_corridor_main_hall` Hải Tặc Hào: `MI:middle_corridor_main_hall.png`, APK `level11`. Kit `ship`: sàn boong (tile), mạn tàu (backdrop), cột buồm + buồm (sway), dây thừng, thùng rượu, đại bác, bánh lái, cờ hải tặc, đèn bão (4 khung), trụ teleport Lv40+.
- Dùng chung mọi map: vòng chọn mục tiêu, vòng đích khi chạm màn hình, dấu hội thoại NPC (`!` nhiệm vụ mới, `?` trả nhiệm vụ, `…` nói chuyện), mũi tên lối ra (4 hướng, 4 khung nhấp nháy), dấu tổ quái, rương báu, bóng tiếp đất mẫu (chỉ để tham chiếu, engine tự vẽ). Nguồn: `JV:assets/sprites/{arrow,door,doornew,light,shadow,taskicon}/`, `EX:misc/`.

### Đợt 5 — Nhân vật người (không gồm linh thú)
- Người chơi nam/nữ: atlas idle 4 + chạy 6–8 khung, 4 hướng (hoặc 3/4 trái + lật), 192×192. Nguồn: `RF:actors/Boy/`, `RF:actors/Girl/`, `JV:assets/sprites/{male,female}/`, `JV:animations/{male,female}/`. Thay `PH:assets/actors/player.webp`.
- 49 NPC theo `stage4/P12-S4-npc-roster.json` (tên Việt, vai trò, `apk_sprite`), idle 4 khung. Nguồn: `RF:npcs/`, `JV:assets/sprites/npc/`, `JV:animations/npc/`. Gom theo nhóm nghề để tái dùng thân: lính/thị vệ, thương nhân, y sư, sư phụ kỹ năng, ngư dân, thủy thủ, quan chức, người hướng dẫn. Thay `PH:assets/actors/npc_*.webp`.
- Chân dung NPC cho hộp thoại (bán thân 256×256) cho 17 NPC chính (tier `main`).

### Đợt 6 — HUD thế giới
Nguồn chính: `RF:hud/` + `hud.json`, bố cục `classic_hud.gd`. Thay `PH:assets/ui/`.
- Góc trái trên: khung chân dung (`frame_portrait`), khung thanh (`frame_bars`), thanh HP / MP / XP (nền + phần đầy + vạch sáng), huy hiệu cấp, 2 nút tròn Linh thú / Nhiệm vụ (`button_pet`, `button_quest`, `button_round`, `button_round_red`).
- Góc phải trên: bảng tên map (9-slice), icon vàng, icon pha lê, nút Menu (`button_menu`), các nút bên (`button_side`, `EX:buttons/right_btn*`).
- Dải dưới: D-pad (đế, 4 mũi tên thường/nhấn, nút tâm) (`dpad`, `panel_controls`), khung chat (`frame_chat`, `EX:chat/chatbg`), 6 tab chat (thường/đang chọn) (`tab_menu`), nút Chọn và Trở về nghiêng (thường/nhấn/khóa) (`button_confirm`, `button_back`, `button_accept`, `button_cancel`), nút chat (`icon_chat`, `EX:chat/chat`).
- Thông báo: dải thông báo (`EX:rooms/*notification_747x76*`), dải gợi ý, thanh XP dài (`EX:rooms/*prog_xp*`), toast nhỏ.
- Góc trang trí (`ornament_corner`), nền mờ lớp dưới HUD.

### Đợt 7 — HUD trận đấu và FX
- Thanh hành động trận (`battle_actions`): 6 icon Tự động, Đánh, Kỹ năng, Vật phẩm, Thủ, Chạy (`icon_auto`, `icon_attack`, `icon_magic`, `icon_inventory`, `icon_run` + icon Thủ mới), viền nút thường/nhấn/khóa.
- Nhãn đơn vị trên đầu: khung tên, thanh HP nhỏ phe ta/địch, dấu mục tiêu ▼ (4 khung).
- Banner: Thắng / Thua (`battle_win`, `battle_loss`), "Lượt N", "Bắt thành công", "Lên cấp" (`JV:assets/sprites/{levelup,levelupStr,battleText}/`), số sát thương/hồi máu/chí mạng/né (font số bitmap 0–9, +, −, MISS) (`JV:assets/sprites/{battleNum,numbig,numsmall,imgFont}/`).
- FX (sheet ngang, 6–10 khung): chém vật lý (cast + hit) (`JV:animations/{phycast,phyhit}/`), phép (cast + hit) (`JV:animations/{magcast,maghit,magic}/`), hồi máu/buff (`JV:animations/{addcast,addhit}/`), kỹ năng lớn (`JV:animations/lskill/`), lên cấp (`JV:animations/levelup/`), ném ấn bắt (`capture_seal`), KO tan biến, khiên Thủ, chạy trốn (bụi).
- FX theo nguyên tố: mỗi nguyên tố trong `data/pets/races.json` một bộ cast/hit (đất, nước, gió, lửa, … đủ theo file).
- 7 hiệu ứng trạng thái (`data/skills/statuses.json`: petrify, doom, sleep, silence, bind, blind, confusion): icon 256² + lớp phủ lặp trên sprite (4 khung).
- Nền trận: dùng lại cảnh map hiện tại; vẽ thêm vòng sàn trận (decal) và "vạch giới hạn" mờ.

### Đợt 8 — Menu và các màn hình
Nguồn chung: `RF:hud/{panel_menu,panel_ornate,row_menu,row_selected,selection,slot,slot_light,tab_menu,frame_small}.png`, `RF:ui/{UI,tableitem,tableitem1}.png`, `EX:ui/`, danh sách màn `JV:ui-text/ui_*.txt`.
- Bộ khung chung: panel lớn 9-slice, panel nhỏ, thanh tiêu đề, nút đóng ×, tab (thường/chọn), dòng danh sách (thường/chọn/khóa), ô vật phẩm (thường/chọn/khóa/hiếm theo sao), thanh cuộn, ô tích, công tắc, ô nhập chữ, nút chữ nhật chính/phụ (9-slice, 3 trạng thái), hộp xác nhận, tooltip, khung số lượng.
- Menu chính 3×2: icon Linh thú, Túi đồ, Nhiệm vụ, Hội, Cửa hàng, Cài đặt (`button_pet`, `button_inventory`, `button_quest`, `button_guild`, `button_shop`, `button_settings`) + Kết nối lại, Đăng xuất.
- Màn riêng (theo JAR `ui_*`): Linh thú (`pet`, `viewpet`, `fieldpetmenu`) — khung thẻ pet, khung sao, khung chỉ số; Giám định (`petauspicate`); Ban phúc (`petbless`); Ấp trứng (`pethatch`, nguồn trứng `JV:assets/sprites/egg/`); Lai tạo (`petmate`, nền `JV:assets/original-png/matingbg.png`, `JV:animations/mating/`, khung nguyên liệu `JV:assets/sprites/petSynMater/`); Cường hóa +N/10; Phả hệ (nút nối cây phả hệ); Học kỹ năng (`learnskill`); Túi đồ (`bag`); Cửa hàng NPC (`npcshop`, `npcsell`, `store`); Nhiệm vụ (`tasklist`, icon `JV:assets/sprites/taskicon/`); Bảng xếp hạng (`ranklist`, huy hiệu ở Đợt 9); Nông trại; Đấu trường; Cài đặt (`setting`); Hội thoại NPC (`touchnpc_all`) — khung hội thoại + khung chân dung.
- Để sau (chưa có chức năng): Hội (`guild*`), Bạn bè (`friendlist`), Thư (`mail`), Đấu giá (`auctionhouse`, `stoneaution`), Ngân hàng (`bank`), Cẩm nang quái (`monstermanual`), Nạp (`charge`, `tokenstore`) — chỉ vẽ khi chủ dự án mở chức năng.

### Đợt 9 — Icon
Master 256², sheet theo nhóm. Nguồn chính `EX:icons/` (309 icon gốc), `JV:assets/sprites/{petIcons,defaultIcon,shortcut,newshortcut,menu}/`.
- Vật phẩm runtime: `data/items/items.json` (capture_seal, potion, ether, synthesis_soul, blessing_leaf…) + bản authoring `data/p10/items.json`.
- Kỹ năng: 29 skill runtime (`data/skills/skills.json`) trước; 97 skill P13 sau khi P13 promote.
- Chủng tộc: 8 race (`data/pets/races.json`); nguyên tố theo cùng file.
- Trạng thái: 7 (xem Đợt 7).
- Chỉ số: HP, MP, Công, Thủ, Phép, Tốc độ, Kháng, Cấp, Kinh nghiệm.
- Sao 1★–5★ (thường/nhạt), dấu hiếm (`EX:rooms/*star_outlined*`).
- Huy hiệu xếp hạng: 26 cái `rank01–55` + `rank6` (`EX:hud/*rank*`).
- Tiền tệ: vàng, pha lê; loại nhiệm vụ: chính, phụ, hằng ngày; vai trò NPC: cửa hàng, hồi phục, nhiệm vụ, hội, kỹ năng, lai tạo, đấu trường, dịch chuyển.
- Chân dung linh thú KHÔNG vẽ: cắt từ atlas P10 (Claude làm bằng code).

### Đợt 10 — Đăng nhập, tải, thương hiệu
- Logo **Phimond** (thương hiệu riêng, không dùng tên/logo PokeZoo, 靈獸世界 hay Spirit Beast World): chữ pixel + biểu tượng linh thú, bản ngang và bản vuông, icon app 1024².
- Nền đăng nhập: toàn cảnh HD-2D (rừng + thành phía xa), chia 3–4 lớp parallax tách rời. Nguồn ý tưởng: `EX:rooms/*2020_06_14_231047*`, `EX:rooms/*ld_900x680*`.
- 3 tranh giới thiệu thay `intro1–3` (`JV:assets/original-png/intro{1,2,3}.png`, `PH:assets/login/`).
- Màn tải: nền + khung thanh + phần đầy (`EX:rooms/*loadingbg*`, `*loadingbar*`, `JV:assets/sprites/{loading,newloading,loadingGround,loadingAniRes}/`, `JV:animations/loadingAni/`), sprite linh thú chạy làm biểu tượng chờ (lấy từ atlas P10, không vẽ).
- Thẻ map cho màn chuyển cảnh/bản đồ thế giới: 1 hình thu nhỏ mỗi map (sau khi map đã dựng; Claude chụp từ cảnh, Astra chỉ vẽ khung).

### Đợt 11+ — 75 map còn lại (chỉ khi P12 cho phép từng vùng)
Mỗi vùng = 1 kit mới + tile/backdrop/prop riêng; nguồn `MI:<map_id>.png`, APK `levelN`.

| Vùng | File APK | Map ID |
|---|---|---|
| Hoàng mạc | level6 | `desert_entrance`, `desert_shicheng_ruins`, `desert_sealed_land`, `desert_hulu_tribe`, `desert_barren_sands`, `desert_disaster_sands` |
| Núi Phong Thạch | level7 | `windrock_mountain_camp`, `_stone_bridge`, `_howling_canyon`, `_mountain_range`, `_mountain_path`, `_summit` |
| Đảo ác mộng | level8 | `nightmare_island_survivor_camp`, `_east_magic_island`, `_ruins`, `_disaster_gate`, `_resentment_path`, `_despair_land` |
| Lăng mộ | level9 | `tomb_region_camp`, `_resentment_path`, `_despair_path`, `_dead_ruins`, `_deep_ruins`, `_gods_tomb`, `_soul_cemetery`, `_unnamed_area_01`, `_unnamed_area_02` |
| Ngã tư | level10 | `crossroads_unnamed_area_01…06` |
| Tinh giới | level12 | `astral_realm_spacetime_rift`, `astral_realm_unnamed_area_01…06` |
| Cổ tích | level13 | `ancient_ruins_unnamed_area_01…06` |
| Lâu đài ma | level14 | `ghost_castle_gate`, `_deep_woods`, `_ancient_city_secret_chamber` |
| Cây thế giới | level15 | `world_tree_gate`, `_deep_woods`, `_secret_chamber` |
| Tháp | level16 | `tower_region_main_tower`, `_deep_woods`, `_secret_floor` |
| Mê thành | level17 | `immortal_maze_main_maze`, `_floor`, `_secret_floor` |
| Bang hội | level18 | `guild_fortress`, `_treasury`, `_warehouse`, `_barracks`, `_shop`, `_pet_stable` |
| Chiến trường bang | level19 | `guild_battlefield_main_field` |
| Cổ điện tế lễ | level20 | `maya_floor_01` |
| Hầm ngục | level21 | `dungeon_floor_01` |
| Đấu trường hỗn chiến / đội | level22–23 | `chaos_arena_main_field`, `team_arena_main_field` |
| Sói–Cừu | level24 | `wolf_sheep_waiting_hall`, `_sheep_house`, `_sheep_pen`, `_middle_field`, `_wolf_pen`, `_wolf_house` |

Tên hiển thị: theo `P12-world-names-master.md` (mục A, B, C).

### Không thuộc phạm vi
- Atlas 160 species, chân dung linh thú (cắt từ atlas).
- Bầu trời, sương, bóng tiếp đất, tia sáng thể tích, mặt nước động, hạt bay: engine/Claude làm; Astra chỉ vẽ sprite nhỏ mà khối đợt ghi rõ.
- Phông chữ (dùng Baloo 2 / Be Vietnam Pro), emoji (dùng của hệ thống).
- Mọi chữ hay số trên UI (engine render).

---

## Phần E — Kiểm tra và tiêu chí đạt

Cơ học (Astra tự chạy bằng Python/Pillow, chỉ đọc):
- Kích thước đúng manifest; RGBA; alpha thật (có pixel alpha=0 ở lề với prop/icon/UI).
- Lề trong suốt ≥ 8 px; không pixel nào chạm mép ảnh.
- Tile: ghép 3×3 không lộ đường nối (so sánh cột/hàng mép, chênh lệch trung bình < 6/255).
- Backdrop: cột đầu khớp cột cuối.
- Mật độ: `px / world` ≈ 128 (prop/nền) hoặc 64 (far), sai lệch ≤ 10%.
- Số màu: mỗi prop ≤ 48 màu sau khi gom (giữ chất pixel), không pixel bán trong suốt rải rác giữa thân (trừ FX).
- Không có chữ (kiểm bằng mắt).

Mỹ thuật (tự review + reviewer độc lập + chủ dự án):
- Đúng loại vật thể và tinh thần nguồn gốc; đẹp và rõ hơn rõ rệt so với placeholder.
- Cùng outline, hướng sáng, độ bão hòa với anchor và với các mảnh cùng kit.
- Đọc được ở kích thước thật trên màn hình điện thoại (xem ở 1x).
- Không lẫn phong cách (vector, anime mượt, ảnh thật, 3D render).
- Nút nghiêng: trục dài đúng 37°, vùng chữ trống.

Bàn giao cho Claude: sau khi chủ dự án duyệt một đợt, Claude đọc `manifest.json`, chuyển PNG sang webp cho `public/`, dựng lại scene JSON (floor/flats/back/props/lights/particles/water/grade), cập nhật `hud.json`/CSS, rồi kiểm tra bằng `scene.html` và ảnh chụp trên khung iPhone. Astra không làm bước này.

---

## Phần F — Thứ tự và ước lượng

| Đợt | Nội dung | Số asset ước tính |
|---|---|---|
| 0 | Style anchor môi trường + UI | ~10 (×2–3 phương án) |
| 1 | Rừng Lục Bảo (2 map) | ~60 |
| 2 | Thành (9 map: city, palace, hall, farm, arena) | ~150 |
| 3 | Bãi biển (5 map) | ~50 |
| 4 | Tàu cướp biển + vật thể tương tác | ~35 |
| 5 | Người chơi + 49 NPC | ~70 sheet |
| 6 | HUD thế giới | ~45 |
| 7 | HUD trận + FX + trạng thái | ~60 |
| 8 | Menu + màn hình | ~70 |
| 9 | Icon | ~120 |
| 10 | Đăng nhập, tải, logo | ~15 |
| 11+ | 75 map còn lại theo vùng | ~40–80 mỗi vùng |

Đợt 1–4 phủ đủ 17 map trong phạm vi P12 Stage 4 (gồm 5 cảnh đang chạy) — làm xong là game nhìn khác hẳn ngay.
