# Nghiệm thu đồ họa HD-2D (batch-00 → batch-10) — 2026-10-15

Người nghiệm thu: Claude (kỹ thuật + xem ảnh). **Không thay thế duyệt của chủ dự án:** cả 660 asset đều `approved:false`.
Nguồn kiểm tra: `apps/game-web/art-src/hd2d/` (manifest từng đợt, `final.png`, contact sheet). Chưa nạp vào engine/scene, chưa dựng thử map.

## 1. Kết luận

| Mục | Kết quả |
|---|---|
| Số asset giao | 660 (batch-00: 28 mẫu style; batch-01→10: 632) |
| File thiếu / sai kích thước so với manifest | 0 / 0 |
| Alpha lề ≥ 8 px, seam tile (xy/x), mật độ 128 px/đơn vị (far 64) | Đạt, ngoại trừ các mục ở §3 |
| Animation (51 sheet): khung khác nhau, đúng số khung | Đạt (hall-candle và battle_target chuyển động rất nhẹ) |
| Chất lượng mỹ thuật môi trường (rừng, thành, biển, tàu) | **Tốt, đúng hướng Octopath:** pixel sạch, outline theo màu vật, đổ khối 3–4 tông, ánh sáng thống nhất |
| Nhân vật người (NPC, người chơi) | **Chưa đạt phạm vi:** chỉ có ảnh tĩnh, chưa có animation; thiếu 58/107 NPC |
| Menu/Panel (batch-08) | **Cần làm lại một phần:** các khung dùng chung một mẫu phẳng |
| Branding/đăng nhập (batch-10) | **Cần sửa:** viền hồng khử nền, kích thước dưới yêu cầu, nền đăng nhập không tách lớp |
| Map đã đủ bộ asset để dựng | 17/92 (rừng 2, thành 9, biển 5, tàu 1), còn vài mảnh nhỏ ở §4 |
| Map chưa có asset | 75/92 (§6) |

Phán quyết theo đợt: **Nhận** = dùng được để dựng; **Nhận + sửa** = dùng được, có lỗi nhỏ cần xử lý; **Làm lại** = chưa dùng.

| Đợt | Nội dung | Số asset | Phán quyết |
|---|---|---|---|
| 00 | Mẫu style A/B | 28 | Lưu trữ (đã được các đợt Octopath thay thế, không đưa vào game) |
| 01 | Rừng Lục Bảo | 61 | **Nhận** |
| 02 | Thành, cung, sảnh, nông trại, đấu trường | 96 | **Nhận** (thiếu vài mảnh, §4) |
| 03 | Bãi biển | 38 | **Nhận** (thiếu vài mảnh, §4) |
| 04 | Tàu cướp biển + ký hiệu dùng chung | 21 | **Nhận** |
| 05 | NPC + người chơi + chân dung | 62 | **Nhận + bổ sung lớn** (§5) |
| 06 | HUD thế giới | 66 | **Nhận + sửa nhẹ** |
| 07 | HUD trận + FX + trạng thái | 71 | **Nhận + sửa nhẹ** |
| 08 | Menu và màn hình | 83 | **Làm lại phần khung** |
| 09 | Icon | 122 | **Nhận + sửa** |
| 10 | Đăng nhập, tải, logo | 12 | **Sửa** (7/12 lỗi viền; vài mục dưới yêu cầu) |

## 2. Việc đạt, tóm tắt

- **Rừng:** 3 tile cỏ, 2 đất, 2 chuyển tiếp, 11 decal, cỏ/hoa/dương xỉ, 3 cây lớn tách thân–tán (sway-split), cây nhỏ, bụi, đá, nấm, gốc, thân gỗ, rễ, cổng (thường/sáng), biển chỉ đường trống, tổ quái, nền xa/giữa/tiền cảnh, nắng xuyên tán, đom đóm, lá, bào tử. Đủ cho cả Bìa Rừng và Rừng Sâu ở mức cơ bản.
- **Thành:** 4 mặt tiền, mái, 3 mái bạt, 3 sạp chợ, đài phun nước + nước chuyển động, trụ dịch chuyển (tắt/sáng + vòng 6 khung), đèn, ghế, thùng, chậu hoa, giếng, xe đẩy, tượng, bậc thềm, lan can, cờ; cung: cổng, tường, tháp, lính gác, ngai, đèn chùm, rèm, thảm; sảnh: sàn gỗ/đá, tường, kệ, quầy, bảng nhiệm vụ, 3 bệ triệu hồi (tắt/sáng), ổ thú ×3, cửa ra (đóng/mở), đuốc, nến; nông trại: ruộng, rào, rơm, kho, chuồng, cối xay + cánh quay, bù nhìn, cây ăn quả; đấu trường: sàn, khán đài, cờ, giá vũ khí, bảng xếp hạng, đuốc.
- **Biển:** 4 tile cát, bọt sóng, cọ ×3 (tách thân–tán), đá bờ ×3, 4 vỏ sò, 2 sao biển, gỗ trôi, cầu tàu, thuyền ×2, giàn lưới, chòi, hải đăng, rương (đóng/mở), san hô ×3, tảo, bong bóng, nền biển xa, vách đá.
- **Tàu:** boong, mạn tàu, cột buồm, buồm, cờ, đại bác, bánh lái, thùng rượu, dây thừng, đèn bão, trụ dịch chuyển; ký hiệu dùng chung (vòng mục tiêu, vòng chạm, `!`, `?`, `…`, tổ quái, 4 mũi tên lối ra).
- **Trận đấu:** 27 sheet FX 6 khung (vật lý, phép, hồi, buff, kỹ năng lớn, lên cấp, ấn bắt, KO, khiên, chạy; 7 nguyên tố × cast/hit), 7 overlay trạng thái, số sát thương 0–9/+/−/MISS/chí mạng, nameplate, HP phe ta/địch, banner Thắng/Thua/Lượt/Bắt/Lên cấp, 6 icon hành động, vòng sàn/giới hạn.
- **Icon:** 5 vật phẩm runtime, 29 kỹ năng runtime, 8 chủng tộc, 7 nguyên tố, 7 trạng thái, 31 huy hiệu hạng, 9 chỉ số, tiền tệ, loại nhiệm vụ, vai trò NPC, sao.
- **HUD thế giới:** D-pad 4 hướng, tab chat (thế giới, khu vực, đội, hội, riêng, hệ thống), nút Chọn/Trở về/Đồng ý/Hủy (thường/nhấn/khóa), khung chân dung/thanh, HP/MP/XP, tiền tệ, bảng tên map, thông báo/gợi ý/toast.

## 3. Lỗi cần sửa trong asset đã giao

| # | Lỗi | Asset | Cách sửa |
|---|---|---|---|
| D1 | **Viền hồng/magenta (dư khử nền) quanh mép** (19–92% pixel mép) | batch-10: `loading-bar-fill`, `map-card-frame`, `app-icon`, `loading-ornament-corners`, `logo-badge`, `logo-horizontal`, `loading-bar-frame` | Vẽ/xử lý lại nền trong suốt; kiểm bằng ảnh phóng 4× trên nền tối |
| D2 | Dưới yêu cầu kích thước | `app-icon` 384² (cần 1024²), `logo-horizontal` 512×128 | Xuất lại ở độ phân giải master |
| D3 | `login-panorama` là một ảnh phẳng, chưa tách lớp parallax (yêu cầu 3–4 lớp) | batch-10 | Vẽ lại tách: trời/núi xa, thành giữa, rừng gần, tiền cảnh |
| D4 | Khác phong cách pixel kit: ảnh tranh minh họa nhiều màu (56k–220k màu), không phải pixel art | `login-panorama`, `intro-01/02/03`, `loading-bg` | Chủ dự án quyết: giữ dạng tranh hay vẽ lại pixel 48 màu như phần còn lại |
| D5 | Mảnh vụn lạc quanh icon | `rank42`, `rank43`, `rank44`, `rank45`, `rank51`; xem lại `egg-earth-shell`, `portrait-forest_guide`, `npc-sq_arena` | Làm sạch rìa |
| D6 | Phong cách icon không đồng bộ: chưa lượng tử hóa, bán trong suốt 20–30% ở mép, hàng nghìn màu (kit môi trường ≤48 màu, alpha nhị phân) | toàn bộ batch-09 (122) và batch-07 (71) | Chủ dự án quyết: chấp nhận cho UI hay ép về palette pixel; nếu ép, làm bằng mã rồi duyệt lại bằng mắt |
| D7 | Bóng loáng/gloss hơn hướng Octopath khắt khe (chính batch ghi cảnh báo) | một số nút/ô ở batch-06 và batch-08 | Giảm gloss ở vòng vẽ lại UI |
| D8 | 18 khung "panel" của batch-08 là cùng một ảnh (`panel-large`, `pet-management-panel`, `appraisal-panel`, `inventory-panel`, …) | batch-08 | Xem §7 |
| D9 | 5 NPC dùng chung ảnh cho nhiều vai (vd `bia_shop`, `mk_general`, `pet_shop`, `fish_shop`, `ship_shop` cùng một người; `bia_free`, `trainer_elin`, `arena_master`, `beach_guide`, `ship_healer` cùng một người) | batch-05 | Xem §5 |

**Lưu ý tỉ lệ (không phải lỗi, xử lý lúc dựng cảnh hoặc vẽ bản nhỏ):** người chơi cao ≈1,31 đơn vị. Cao hơn hoặc ngang người: `barrel` 1,26, `rum-barrel` 1,16, `wooden-crate` 1,14, `treasure-chest-closed` 1,28, `cannon` 1,30, `bench` 1,14, 3 chậu hoa 1,2–1,4, `farm-basket` 1,14, `rope-coil` 0,69, vỏ sò 0,55–0,69 (decal quá to). Claude có thể thu nhỏ trong scene (mất tròn pixel); nếu muốn giữ đúng 128 px/đơn vị thì cần vẽ bản nhỏ (~60–70%).

## 4. Còn thiếu để dựng đủ 17 map đã có kit

**Rừng Sâu Lục Bảo** (đang dùng chung kit Bìa Rừng):
- Bản tối/rậm hơn: tile đất rêu, cây cổ thụ khổng lồ, tường rễ, bụi rậm đậm, đèn nấm/đá phát sáng, cổng vào sâu.

**Thành (nhiều map):**
- Nền xa (`backdrop_far`): đường chân trời thành phố/tòa tháp (chưa có cho thành, nông trại, đấu trường, sảnh).
- `streetlamp-lit` hoặc lớp phát sáng cho đèn (hiện chỉ có `unlit`).
- Vương Cung (nội thất): sàn đá cẩm thạch + thảm đỏ dạng tile; cột trong sảnh; cửa vào ngai.
- Vạn Sự Hội Sảnh: sân khấu/bàn phát thưởng, bảng sự kiện, gian trưng bày.
- Hoàng Môn: tường thành dài lặp được, cầu/cổng nâng, trụ cờ.
- Thương Phố: nền chợ (sàn lát, vỉa hè), thêm sạp (cá, đồ gốm, dược thảo), đèn lồng treo, thùng hàng xếp chồng.
- Sảnh Triệu Linh: tường sau bệ đá có hoa văn, ô cửa sổ sáng, tấm thảm lối vào.
- Phòng thú cưng: sàn tổ chăm sóc, bát ăn, đồ chơi, giường, cỏ khô.
- Quảng Trường Thạch Trụ: đủ nhưng nên có thêm 1–2 trụ trang trí (không phải điểm dịch chuyển).
- Nông trại: nền xa (đồi, rừng), nước/ao nhỏ, cầu gỗ, luống rau (cà rốt, bắp cải).
- Đấu trường: tường rào sân, cổng ra, cột đèn, bậc khán đài hai bên.

**Biển:**
- **Vực Hải Lam (deep sea):** chưa có tile đáy biển riêng (cát xanh, đá, san hô nền), cột sáng nước, cá/sinh vật nền, tảo dày, đá ngầm, xương tàu đắm.
- **Đảo Phú Quý:** chưa có bộ "giàu có": đống vàng/rương đầy, tượng vàng, cờ, trụ cổng, lối đi lát đá.
- **Bờ Đông Ngọc Bích / Bờ Tây Hoàng Sa:** đủ kit chung; nên có biến thể màu cát/đá riêng (xanh ngọc, vàng cát) và thêm cây bụi ven biển, đụn cát, vũng thủy triều.
- Tàu cá còn thiếu buồm/mái, thùng cá, mái chèo; cầu tàu thiếu đèn.

**Tàu cướp biển:**
- Lan can/mạn thấp (`gunwale`), thùng hàng, neo, cửa cabin, cầu thang, buồng lái, dây thừng treo, đèn thêm, vòng sáng trụ dịch chuyển.

**Dùng chung:**
- Lối chuyển map: đã có mũi tên; thiếu bản "thường/sáng" cho cổng thành, cổng biển, cổng tàu.
- Mũi tên điều hướng bổ sung, bảng chỉ đường (trống chữ) cho thành/biển.

Ghi chú: nước (sóng, bọt, độ sâu), bầu trời, sương, bóng tiếp đất do engine làm, không cần vẽ.

## 5. Nhân vật người

| Hạng mục | Hiện có | Cần |
|---|---|---|
| Người chơi nam/nữ | 1 ảnh tĩnh mỗi giới (192²) | **Chạy ×(4 hướng hoặc 3/4 + lật), idle, tương tác**; gốc có Idle/Run (`reference/actors/Boy`, `Girl`) |
| NPC | 49/107 trong roster hiện hành (29 hình khác nhau), tất cả 1 khung | **58 NPC chưa vẽ** (windrock 8, tomb 8, desert 7, nightmare 7, crossroads 5, ancient 5, astral 4, city 3, tower 3, immortal 3, ghost 2, world 2, middle 1); idle 4 khung cho mọi NPC; tách khác nhau những NPC dùng chung ảnh |
| Chân dung hội thoại | 11/21 NPC `main` | **10 chân dung còn thiếu**; xác định lại 17 cũ trong kế hoạch vs 21 hiện tại |
| Kẻ địch/quái | Dùng atlas P10 (đã xong) | Không cần |

Ghi chú: roster NPC đã mở rộng lên 107 (58 map) sau khi batch-05 chạy; batch-05 vẽ theo roster 49 cũ. 4 NPC thuộc map đã có kit (3 thành + 1 tàu) nên ưu tiên đầu.

## 6. 75 map chưa có asset

Tên theo `P12-world-names-master.md`; "(chưa đặt tên)" là map nguồn chưa chốt tên. Cột NPC là số map trong roster hiện hành có NPC.

| Vùng (APK) | Số map | Danh sách | Kit mới cần vẽ |
|---|---|---|---|
| Hoàng mạc (level6) | 6 | Sa Thạch Cổ Thành, Cửa Ngõ Hoàng Mạc, Phong Ấn Cổ Địa, Bộ Lạc Hồ Lô, Hoang Sa Vô Tận, Tai Ương Sa Mạc | cát, đá sa thạch, xương rồng, lều bộ lạc, phế tích, đụn cát, bão cát (FX), phong ấn |
| Núi Phong Thạch (level7) | 6 | Trại Phong Thạch, Cầu Thiên Thạch, Hẻm Gió Gào, Dãy Phong Lĩnh, Sơn Đạo Phong Vân, Đỉnh Thiên Phong | đá núi, vách, cầu đá, tuyết/gió, trại, cây thông |
| Đảo ác mộng (level8) | 6 | Trại Tàn Sinh, Đông Đảo Huyền Thuật, Phế Tích Cổ Thành, Cổng Tai Kiếp, Oán Linh Hải Đạo, Tuyệt Vọng Hải Địa | đá đen, cây héo, ma khí, phế tích, cổng tai kiếp |
| Lăng mộ (level9) | 9 | Doanh trại lăng mộ, Oán Linh Cổ Đạo, Tuyệt Vọng Chi Địa, Tàn tích chết, Sâu trong tàn tích, Lăng mộ các vị thần, Nghĩa trang linh hồn, 2 map chưa đặt tên | bia mộ, quan tài, đèn ma, tường lăng, xương, sương |
| Ngã tư (level10) | 6 | 6 map chưa đặt tên | cần chốt chủ đề trước khi vẽ |
| Tinh giới (level12) | 7 | Khe nứt không thời gian + 6 chưa đặt tên | nền vũ trụ, đảo trôi, tinh thể, khe nứt |
| Cổ tích (level13) | 6 | 6 chưa đặt tên | cổ tích: cột, tượng, rêu, phế tích |
| Lâu đài ma (level14) | 3 | Cổng lâu đài ma, Rừng sâu Bích Ba, Mật thất thành cổ | tường lâu đài, đèn ma, cây ma, nội thất |
| Cây thế giới (level15) | 3 | Cổng cây thế giới, Rừng sâu Bích Ba, Mật thất cây thế giới | rễ khổng lồ, thân cây, ánh sáng thần |
| Tháp (level16) | 3 | Tháp Chim, Rừng sâu Bích Ba, Bí cảnh Tháp Chim | tầng tháp, cửa, lông vũ, cầu thang |
| Mê thành (level17) | 3 | Trường Sinh Mê Thành, Tầng, Bí cảnh Mê Thành | tường mê cung, cổng, sàn |
| Bang hội (level18) | 6 | Pháo đài, Kho bạc, Nhà kho, Doanh trại, Cửa hàng, Chuồng thú | nội thất/ngoại thất bang hội |
| Chiến trường bang (level19) | 1 | Chiến trường bang hội | sân chiến trận, cờ, công sự |
| Cổ Điện Tế Lễ (level20) | 1 | Cổ Điện Tế Lễ · Tầng I | điện đá tế lễ, bậc thang, bàn thờ |
| Hầm ngục (level21) | 1 | Ngục ngầm — tầng 1 | tường ngục, bậc, đuốc, xích |
| Đấu trường hỗn chiến/tổ đội (level22–23) | 2 | Chiến Trường Hỗn Loạn, Chiến trường tổ đội | sàn đấu, cột, khán đài (có thể dùng lại kit đấu trường) |
| Sói–Cừu (level24) | 6 | Sảnh Đối Quyết, Dương Xá, Dương Lan, Khu vực giữa, Lang Huyệt, Lang Sào | nhà cừu/sói, chuồng, sân, cỏ |
| **Tổng** | **75** | | |

Ưu tiên theo roster NPC (vùng đã có kế hoạch gameplay trước): Hoàng mạc → Núi Phong Thạch → Đảo ác mộng → Lăng mộ → Ngã tư/Tinh giới/Cổ tích → các vùng còn lại. Bang hội, Sói–Cừu, đấu trường đội: sau khi mở chức năng.

## 7. UI/HUD/Menu còn thiếu hoặc cần làm lại

**Cần làm lại (D8):** bộ khung menu. Hiện 18 panel là cùng một ảnh (nền xanh đậm phẳng, chỉ 4 góc vàng, không có tiêu đề, đường phân cách, hoa văn cạnh), nên mọi màn hình trông giống nhau và không đạt độ phong phú của HUD batch-06. Cần phân cấp:
- Cửa sổ chính (viền dày, ngọc ở góc, thanh tiêu đề riêng);
- Panel con (viền mỏng);
- Panel danh sách (viền + đường chia);
- Hộp xác nhận/thoại;
- Tooltip, khung chân dung, khung cột chỉ số;
- Mỗi khung có thể co giãn (9-slice) và không nướng chữ.

**Thiếu:**
- Icon nút menu "Hội" (có linh thú/túi đồ/nhiệm vụ/cửa hàng/cài đặt/kết nối lại/đăng xuất, thiếu Hội);
- Nút thu/phóng/bảng đồ thế giới (nếu mở);
- Con trỏ chọn, hiệu ứng lướt chuột trên hàng;
- Biểu tượng gắn thẻ (mới/đã đọc), dấu chấm đỏ thông báo;
- Chân dung linh thú KHÔNG cần (cắt từ atlas).
- Màn chờ: spinner đã có trong `loading-ornament-corners` nhưng nên có sheet quay riêng.
- Màn chọn nhân vật/tạo nhân vật (chưa có asset): khung, bệ, nút giới tính.

**Hoãn (chưa có chức năng):** Hội, bạn bè, thư, đấu giá, ngân hàng, cẩm nang quái, nạp; icon 97 kỹ năng P13 (chờ P13 được chốt).

## 8. Thứ tự đề xuất

1. **Sửa D1–D3, D5** (nhanh, 7 asset batch-10 + vài rank): bắt buộc trước khi đưa vào game.
2. **Người chơi + NPC có animation** (§5): chặn việc dựng thế giới có người đi lại.
3. **Bổ sung kit 17 map** (§4): ưu tiên Vực Hải Lam, Đảo Phú Quý, nền xa thành/nông trại/đấu trường, Rừng Sâu, nội thất Vương Cung.
4. **Khung menu** (§7) và icon Hội.
5. **Vùng ngoài**: Hoàng mạc → Núi Phong Thạch → Đảo ác mộng → Lăng mộ → … (§6).
6. Quyết D4/D6 (phong cách tranh/icon) cùng chủ dự án trước khi vẽ thêm.

## 9. Giới hạn nghiệm thu này

- Đã chạy kiểm tra cơ học trên 660/660 asset (kích thước, alpha, lề, seam, mật độ, số màu, mảnh lạc, viền hồng, trùng ảnh) và xem contact sheet của mọi đợt cùng một số ảnh phóng to; **chưa** mở từng ảnh `final.png` một.
- Chưa nạp vào engine nên chưa kiểm: ghép lớp trong cảnh, thứ tự lớp trước/sau, bóng, sway-split ghép thân–tán, độ mờ khi thu nhỏ, hiệu năng bộ nhớ (≈660 texture).
- "Thiếu" ở §4 là đánh giá của Claude dựa trên ảnh ghép APK và bố cục map hiện có; có thể đổi sau khi dựng thử cảnh thật.

---

## Tái nghiệm thu (22:40) — sau báo cáo "hoàn thiện tất cả" của GPT/Gemini

Audit lại 741 asset (`~/hd2d_audit/audit.py`). Kết quả so với báo cáo:

| Khẳng định trong báo cáo | Kết quả đo | Đạt? |
|---|---|---|
| Batch-07 (FX/HUD chiến đấu) đã lượng tử hóa ≤48 màu | 71 asset không đổi, tới ~19.992 màu | KHÔNG |
| Batch-09 icon ≤48 màu, sạch AA | ≤48 màu đạt, nhưng 122/122 icon còn 20–56% pixel bán trong suốt | MỘT PHẦN |
| Batch-08 18 panel → 6 khung 9-slice | Đã có khung khác nhau, nhưng 6.5k–20k màu | MỘT PHẦN |
| Batch-10 hết viền hồng, app-icon 1024² | 7 asset đạt kiểm tra; app-icon 1024² đạt | ĐẠT |
| Login 4 lớp parallax | Có 4 lớp 1280×720 nhưng là tranh painterly (90k–149k màu, 9–22% bán trong suốt), không phải pixel art | MỘT PHẦN |
| 58 NPC mới đủ 107 roster | Chỉ 49/107 id khớp `P12-S4-npc-roster.json`; 58 NPC mới đặt id/tên khác (`desert_01`, `tree_01`…) so với roster (`desert_aven`, `sq_exchange`, `maze_*`…) | KHÔNG khớp |
| Mảnh còn thiếu của 17 map | `deep-sea-floor-tile` sạch. `deep-woods-giant-tree` (23.720 màu), `royal-throne`, `palace-marble-pillar`, `royal-carpet-runner` (margin 0), `city-skyline-far`, `prosperity-treasure-chest` chưa lượng tử hóa; `arena-stands-far` (SEAM_X 72.7) và `farm-hills-far` (SEAM_X 56.2) không seamless | MỘT PHẦN |
| 75 map còn lại "đã báo cáo kit" | Chỉ là tài liệu danh mục `hd2d-remedy-and-expansion-plan.md`; chưa có file art nào | KHÔNG phải art |

Kết luận: 17 map kit của P12 dựng được ở mức thử; chưa phải "xong hết". 75 map chưa có art.

## Tái nghiệm thu 2 (23:40) — Batch-11: TỪ CHỐI 304/304. Chi tiết: hd2d-batch-11-rejection-and-redo-prompt.md

## Thí điểm batch-11-tomb (23:55): CHƯA ĐẠT, 3/10 đạt. Chi tiết: hd2d-batch-11-tomb-pilot-review.md

## Thí điểm tomb lần 2 (00:20): 5 đạt, 2 có điều kiện, 3 chưa đạt; đã dựng thử tomb_hd2d. Xem hd2d-batch-11-tomb-pilot-review.md

## Tái nghiệm thu map Rừng (2026-10-16 00:40)
Audit batch-01: 61/62 sạch. 5 điểm đã nêu: (1) nền xa liên tục ĐẠT (3 lớp wall-far / canopy-mid / hedge-front phủ kín); (2) canopy-mid đã khai báo tileable x, lặp được, ĐẠT; (3) wall-far hết vết nối nhìn thấy (edge diff 0), ĐẠT; (4) 3 backdrop semi-alpha = 0, ĐẠT; (5) ranh giới edge/dirt CHƯA ĐẠT hẳn: `dirt-floor-02` lệch 12,7 so với đáy `edge-grass-dirt` (`dirt-floor-01` chỉ 3,5); mép cỏ của edge tile lệch 10,5 so với `grass-floor-01` → còn vạch ngang ở chỗ đổi nền.
Vấn đề mới: `forest-hedge-front` chạm hàng alpha đầu tiên nên mép trên bị cắt phẳng (vạch ngang trên màn hình); `deep-woods-giant-tree` vẫn 23.720 màu (chưa lượng tử hóa); `edge-grass-dirt` có hướng đất ở phía xa, cỏ ở phía gần khi dựng trong engine.

## Tái nghiệm thu map Rừng lần 2 & Thí điểm Lăng Mộ lần 3 (2026-10-16 09:10)

- **Map Rừng (`forest_hd2d`): ĐẠT TOÀN DIỆN**
  - `forest-hedge-front`: Mép trên đã chừa 35 px alpha (≥ 8 px), tạo hình tán bụi lồi lõm tự nhiên (triệt tiêu hoàn toàn vạch ngang phẳng tại y ≈ 95); mép đáy neo vững chắc (alpha = 255); seam X = 0; 41 màu.
  - `edge-grass-dirt`: Mép cỏ (hàng 0, phía gần z = 3.2) đồng bộ hoàn toàn với `grass-floor-01` (chênh lệch biên = 0); mép đất (hàng 511, phía xa z = -0.8) đồng bộ hoàn toàn với `dirt-floor-01` (chênh lệch biên = 0); seam X = 0; 48 màu.
  - `dirt-floor-02`: Đã cân bằng màu và đồng bộ mép với `dirt-floor-01` và `edge-grass-dirt` (chênh lệch biên = 0); seam X = 0, seam Y = 0; luma diff mép–tâm = 0.39 (≤ 3.0); 32 màu. `build_hd2d_forest_test.py` xen kẽ cả 2 sàn đất tự nhiên không lộ vết nối.
  - `deep-woods-giant-tree`: Đã lượng tử hóa về 40 màu (≤ 48 màu), alpha nhị phân (0 pixel bán trong suốt).
  - Lỗi 404 trình duyệt: Đã tra rõ nguồn (do trình duyệt tự động gửi request `/favicon.ico` khi mở `scene.html`, nay đã có file và link `/favicon.svg` + `/favicon.ico` trả về 200 OK; toàn bộ 52 texture cảnh đều tồn tại và tải thành công 200 OK, 0 lỗi console).

- **Thí điểm Lăng Mộ lần 3 (`batch-11-tomb` & `tomb_hd2d`): ĐẠT**
  - `tomb-brick-floor`: Họa tiết gạch lát cổ từ bản vẽ gốc, loại bỏ ô vuông lớn và chữ thập đậm; seam X = 0, seam Y = 0; chênh độ sáng mép–tâm 0.74 (≤ 3.0); 34 màu.
  - `tomb-graveyard-dirt`: Triệt tiêu dither ô cờ 1×1 (hết nhiễu moiré); seam X = 0, seam Y = 0; chênh độ sáng mép–tâm 0.41 (≤ 3.0); 32 màu.
  - `tomb-tile-edge-decal`: Decal chuyển tiếp ranh giới đá vỡ lồi lõm hữu cơ giữa đất và gạch lát; seam X = 0; 36 màu.
  - `tomb-necropolis-wall-far`: Tường thành đá u linh có lỗ châu mai và trụ tường (buttresses), tháp canh nhọn xa, trăng rằm huyền bí qua sương, cây khô khẳng khiu, bia mộ nhấp nhô; seam X = 0; 38 màu; nhị phân alpha.
  - `tomb_hd2d`: Đã dựng hoàn chỉnh trong engine (10 texture, 27 prop, 26 flat, 4 backdrop, 0 lỗi 404, 0 lỗi console).


## Tái nghiệm thu lần 3 (2026-10-16 09:50): map Rừng + pilot Lăng Mộ
Audit: batch-01 62/62 sạch; batch-11-tomb 11 asset, 1 cờ `DENSITY 64` của backdrop xa (đúng quy cách 64 px/đv, lỗi nằm ở audit.py, không phải asset).
Rừng: ĐẠT, trừ 1 lỗi: `forest-canopy-mid` mép trên cắt phẳng (hàng 300→301 nhảy từ 0% lên 90% alpha) nên vẫn có vạch ngang ở y≈95 trên màn hình (trước đó mình quy nhầm cho hedge-front; hedge-front đã sửa đúng). `dirt-floor-02` seam Y max 12,2 (không phải 0). Edge↔dirt/cỏ nay lệch 0,0.
Lăng Mộ pilot: ĐẠT CÓ ĐIỀU KIỆN. Tile gạch/đất seam max 2,4–3,3, backdrop đúng chủ đề (tường, tháp, trăng, cây khô), dựng cảnh ghép tốt. Tồn đọng: `tomb-tile-edge-decal` seam X max 16,5; gạch mép tối hơn tâm 8; cổng dịch chuyển vẫn cầu thang chéo; dải nền phía sau chân tường tối phẳng (do sương, chỉnh ở cảnh).

## Đính chính + tái nghiệm thu (2026-10-16 10:50)
ĐÍNH CHÍNH của Claude: cột `seam_x/seam_y` trong audit cũ là [chênh trung bình mép bọc, chênh trung bình lân cận], KHÔNG phải chênh tối đa. Các nhận định trước đây "dirt-floor-02 seam Y 12,2", "tomb-tile-edge-decal seam X 16,5", "hedge-front 17,6", "brick 3,3" là đọc sai; chênh bọc tối đa thực đo của những tile này đều = 0 (edge decal chỉ khai báo lặp X; trục Y không cần). `audit.py` đã sửa: thêm `seam_x_max/seam_y_max`, và nền xa 64 px/đv không còn bị cờ.
Chỉ số thật (max): batch-01 và batch-11-tomb 0 lỗi; riêng `grass-floor-01/02/03` và `edge-grass-roots` có chênh bọc tối đa 26 (trung bình thấp, chưa thấy vết trong cảnh).
`forest-canopy-mid`: ĐẠT, hàng đầu có nội dung 277, bước nhảy hàng lớn nhất 2,5% (không còn cắt phẳng), 42 màu.
Quyết định: mở kit Hoang Mạc và Núi Phong Thạch. Prompt: hd2d-batch-11-next-kits-prompt.md.

## Kit Hoang Mạc (batch-11-desert) — nghiệm thu 16/10 13:40
- Audit: 18 asset, 0 issue; tile seam max 0, 34–36 màu, backdrop 1024×384 wrap 0, portal dormant/active cùng mask. Xem mắt: art ĐẠT (chất lượng bằng kit rừng).
- Kết luận: **ĐẠT CÓ ĐIỀU KIỆN — cho phép mở Núi Phong Thạch song song.**
- Sửa nhỏ (không chặn kit sau): (1) scene desert_hd2d bị cháy sáng/vàng chói (ambient 2.2 + fog [0.82,0.65,0.42] quá mạnh, mất chi tiết cát/backdrop) → hạ ambient ~1.4–1.6, fog nhạt hơn/ít đục; (2) backdrop lát nối có vạch đứng + bậc sáng/tối tại điểm nối trong engine (x≈65 và ≈915 ở 1280px) — kiểm tra khoảng đặt layer (bước = đúng chiều rộng thế giới của ảnh, không chồng/hở) và cùng fog cho mọi mảnh; (3) pixel lạc: cactus-01 (18px), ruins-wall (2,2,1px), nomad-tent (11px) → xoá; (4) prop quá lớn so với player (cactus ~2.5 đơn vị, portal 487×404) → giảm w/h trong scene hoặc xuất lại nhỏ hơn; (5) dải cát-02/sandstone xen kẽ nhìn như sọc ngang, cần decal chuyển tiếp mềm hơn.

## Hoang Mạc tái kiểm + Núi Phong Thạch (batch-11-windrock) — 16/10 14:10
- Hoang Mạc: pixel lạc đã hết (1 thành phần/asset), grade dịu, prop đúng tỉ lệ → ĐẠT. Còn: vạch nối backdrop ở x≈65/1280 vẫn thấy; sàn là các mảng chữ nhật cạnh cứng.
- Windrock audit: 19 asset, tile seam 0, backdrop wrap 0, 0 semi-alpha; art đẹp. Lưu ý: portal dormant/active chạm mép phải (margin 0, bbox x 10..369/370); pine-trunk có 3 thành phần (nét rời trên ngọn); DENSITY cảnh báo arch-gate/pillar/trunk (156/149/144, nên ~128); campfire/spawn 512 (strip, bỏ qua). Scene: cùng vạch backdrop x≈65 & ≈915, đường đen mảnh ở biên z giữa 2 mảng sàn, sàn ghép mảng cứng.
- Kết luận: ĐẠT CÓ ĐIỀU KIỆN → cho mở kit Đảo Ác Mộng.

## Hoang Mạc 85 asset — từ chối (16/10 17:30)
Audit: 85 asset, 46 cảnh báo. Lỗi: tile sand-floor-03 và sand-cracked-01 có số "1","2" dính vào ảnh; 8 decal mép (edge-sand-*) là ô vuông đục, margin 0; decal bones/pottery/sunken-bricks/pebbles/boulder-02/pottery-urn có vạch cam lạ ở trên; boulder-03 gần như trống (chỉ mảng xanh); camp-charcoal-stove trùng hash với nomad-tent-large (cùng file); nomad-stake-banner thực chất là bao tải; dunes-mid/ruins-near là dải cát phẳng, không có phế tích; horizon-gradient và 6 shadow chỉ 1 màu, gần như vô hình; density 140–250 (chuẩn 128) ở ~40 prop; cactus nhỏ/tall/palm-trunk quá đen lệch palette; ruins-wall-arch/stone-stairs cam phẳng. Scene: backdrop vẫn có vạch dọc ở x≈790 (0.5) và x≈475 (0.15), dải ngang nhòe ở chân trời, prop xếp hàng ngang, hố vực chỉ là 1 đốm, sàn đơn điệu một tile.

## Hoang Mạc vòng 3 — ĐẠT CÓ ĐIỀU KIỆN (17/10 03:20)
Audit 85 asset: 0 cảnh báo, 0 hash trùng, seam tile 0 (đo lại thật). Scene: backdrop nhiều lớp liền mạch, sàn 1 tile chủ đạo, hết đai chân trời, hết hộp nhân sư — đạt về tổng thể. Còn sửa: sand-dune-medium viền vàng-xanh neon + 459 thành phần (dither rời); sand-mound/dune còn mảng chữ nhật sáng hơn ở mép; decal gạch dưới cột và dải gạch/sỏi ở camera 0.15 vẫn hình chữ nhật cạnh cứng; 8 edge-sand-* thành tam giác/lục giác/dải thẳng, chưa dùng được; boulder-03 vỡ (chỉ còn mảng tối ở góc), stone-stairs/ruins-wall-arch vàng chói lệch gam; shadow-* thành nửa vòm; sàn 1 tile lớn đơn điệu (gợn sóng to, tiền cảnh trống); small-cactus-01, charcoal-stove, tent-large còn pixel rời.

## Hoang Mạc Round 6 (Chốt chuẩn mốc — 17/10 10:45)
- **ĐẠT (Benchmark chính thức cho toàn bộ 17 kit HD-2D).** Khép vòng sửa cho Hoang Mạc (`batch-11-desert`, 85 asset).
- **Kết quả nghiệm thu thực tế qua scene 3 camera & audit:**
  - `sand-dune-medium`: Hết hai cạnh dọc cắt vuông tại x≈305 và x≈545. Cồn cát vuốt mềm tự nhiên hai đầu, có vân sóng cát, hòa hợp với sàn.
  - `desert-sphinx-ruin`: Xóa bỏ hoàn toàn hộp đế chữ nhật bên phải và vết cắt thẳng; thân và đuôi tượng vuốt tự nhiên.
  - `desert-decal-ancient-rune-faded` & đĩa portal: Đã bo tròn thành đĩa đá cổ hoàn chỉnh, loại bỏ hoàn toàn viền vuông.
  - Gạch dưới cột phế tích (`sandstone-rubble`, `sunken-bricks`): Loại bỏ góc cắt vuông cạnh cứng, hòa vào nền cát tự nhiên.
  - Backdrop nhiều lớp, bậc thang sa thạch, vòm tường, boulder ổn định, không có vạch nối.
  - **Audit 85 asset**: 0 hash trùng, seam tile = 0. Có 6 cảnh báo `SEMI_ALPHA` ở 6 `desert-shadow-*` (41–60% pixel bán trong suốt) — **ĐƯỢC CHẤP NHẬN CHÍNH THỨC** theo cơ chế bóng đổ procedural gradient mềm (thay thế dither Bayer 1-bit bị vỡ hạt). Cảnh báo SEMI_ALPHA chỉ được phép áp dụng riêng cho nhóm shadow, các asset prop/tile/decal khác vẫn giữ nguyên tắc alpha nhị phân nghiêm ngặt.
- **Hai quy tắc nghệ thuật cốt lõi được chốt:**
  1. *Bóng đổ (Shadows)*: Được phép làm procedural gradient alpha mềm (màu nâu hổ phách ấm `#68482A`), cấm dùng Bayer dither 1-bit gây vỡ thành hàng nghìn hạt rời.
  2. *Decal chuyển tiếp*: **CẤM sinh bằng mã hoặc công thức toán học.** Bắt buộc vẽ bằng công cụ tạo ảnh (AI generation) để đảm bảo hình khối tự nhiên, hữu cơ.
- **Tồn đọng nhỏ (không chặn, xử lý kết hợp khi tiện):**
  - Quầng sáng rất nhẹ quanh cồn cát và nhân sư (hơi nhạt hơn sàn); sườn trái cồn cát còn một vệt tối nhỏ.
  - Vệt cát bay góc trái (camera 0.5, x≈290–420, y≈580–610) còn đầu cắt vuông phía dưới.
  - Cồn cát `sand-mound` và boulder nhỏ bóng hơi mờ, có thể tăng độ đậm thêm một chút.
- **Quyết định:** Mở toàn diện cho triển khai **Núi Phong Thạch (`batch-11-windrock`)** mở rộng từ 19 lên $\ge 70$ asset theo tiêu chuẩn Hoang Mạc Round 6. Bắt buộc nộp đủ ảnh render 3 góc camera + ảnh zoom 2× chuyển tiếp sàn mỗi vòng.

## Núi Phong Thạch (batch-11-windrock, 74 asset) — TỪ CHỐI (17/10 13:30)
Kiểm bằng audit + đo tile + dựng cảnh thật (3 camera). Kết luận: chưa đạt, chưa nghiệm thu.
Lỗi chặn:
1. Gemini nói đã xuất 4 ảnh nhưng không có file nào trên đĩa (windrock_cam_*.png, transition_zoom_2x). contact-sheet.png vẫn là sheet cũ 19 asset (chỉ thấy cliff cát vàng, thông cũ…), không phải 74.
2. grass-snow-floor và snow-crust-floor tương quan 1.00 (cùng một ảnh, chỉ đổi màu; "snow crust" thành xanh ô-liu, không phải tuyết). Đây là bản sao đội lốt, không phải asset vẽ mới.
3. Chuẩn hóa luma bằng ép trung bình RGB: rock-floor-01/02 và slate-floor có trung bình RGB y hệt [76,90,102]; 4 tile còn lại cũng gần y hệt nhau. "Chênh luma 1.5/255" đạt bằng cách ép số liệu, mất bản sắc tile (slate = rock).
4. Backdrop cliffs-near có vệt nhòe dọc ở giữa (làm mượt đường nối đã làm bẹt pixel), thấy rõ ở cam 0.5.
5. Cầu treo nhỏ ~130 px, nằm trên mảng tối dạng decal; không bắc qua khe thật, cầu đứt lơ lửng. Khe bị cắt mép ở rìa phải.
6. Mép đất/đường chân trời cắt thẳng ngang, không thấy horizon-gradient.
7. Toàn bộ prop xếp 1 hàng ngang cùng độ sâu (đúng lỗi đã cấm); nửa dưới màn hình trống. Chỉ 36 prop cho map dài ~25 đơn vị.
8. cliff-snow-ledge vẫn là vách cát vàng cỏ khô kiểu sa mạc, mép phải răng cưa cắt dọc, đặt cạnh cổng.
9. Thông vặn: vệt rêu xanh neon trên thân; vài điểm đỏ lẻ gần chân cột (dư magenta); mảnh cột gãy nhỏ lơ lửng (pillar-01).
10. audit: 38/74 cảnh báo DENSITY (chưa giải thích), 6 bóng semi-alpha (được phép).
Ghi chú: chỉ 3/8 tile sàn được dùng trong scene.

## Layout desert_entrance vòng 1 (17/10 14:20) — ĐẠT HƯỚNG, CHƯA NGHIỆM THU (sửa vòng 2)
Đúng: file layout/preview/3 cam/3 zoom có trên đĩa; validate 0 lỗi (xác nhận tự chạy); 4 neo giữ đúng px; Edda có why; bố cục 3 tầng, trạm lều giữa map, bầu không khí ổn, ngân sách trang trí đủ.
Lỗi nhìn thấy (validator không bắt được):
1. Sprite bị cắt thẳng mép phải: tumbleweed-02, small-cactus-02, small-rock-03 (cam 0.15 và 0.85). Nghi lỗi builder tính world/UV sai.
2. Cổng: tây dùng portal-active (đĩa lửa bị liềm đen che), đông dùng portal-dormant (lỗ đen hoàn toàn); hai cổng không cùng trạng thái; cổng đông chồng 3 asset (portal + stairs + arch-gate) tạo mảng chữ nhật nâu nhạt phía trên vòm.
3. Decal chữ nhật cạnh thẳng + chấm dither: desert-edge-sand-sandstone-corner-01 ở (2320,480) cạnh bậc thềm đông. Viền đen quanh vết nứt/pebbles gần cổng đông.
4. Cọ: gốc có mảng đất nâu chữ nhật; sau xương rồng cao + cọ có mảng cồn vàng lơ lửng viền cứng (halo chưa hết).
5. Mảng cam của decal bones/bone-pile lệch màu so với cát, mép cứng.
6. Prop vẫn thành 2 dải ngang (mid y 480–520: 44 vật; front y 700–760: 32 vật), khoảng 540–680 trống.
7. Cụm mỏm đá xoắn + xương rồng lệch của ảnh gốc (trái trên) không thấy trong 3 cam; Gemini nói "giữ đúng" nhưng chưa chứng minh.
Bổ sung 17/10 15:45: lỗi "sprite cắt mép phải" KHÔNG do builder; do chính asset (cột mép ngoài đặc): tumbleweed-01/02, small-rock-02, boulder-03, cactus-dead, decal-cracked-earth-patch, stone-stairs, edge-sand-sandstone-w, corner-01/02. Đã sửa nội dung phản hồi Gemini.

## Layout desert_entrance vòng 2 (17/10 15:50) — CHƯA NGHIỆM THU (còn 5 điểm)
Đã sửa: hai cổng cùng dormant (xoáy nâu đồng nhất), bỏ chồng 3 asset ở cổng đông, bỏ decal chữ nhật corner-01, halo sau cọ/xương rồng hết, thêm zoom cụm góc trái, 124 placement (mid 74/front 30/back 20), validator 0 lỗi, 4 neo vẫn đúng px, cả hai cổng dormant.
Còn lỗi:
1. Asset bị cắt mép KHÔNG được sửa (kiểm bbox_edge.py vẫn 18 mục): tumbleweed-01/02, small-rock-02/03 (thấy rõ cạnh cắt dọc ở cả 3 cam), boulder-03, cactus-dead, decal-cracked-earth-patch, ruins-wall/-arch, các edge-sand-sandstone. Gemini chưa vẽ lại.
2. Gốc cọ vẫn có mảng đất nâu chữ nhật cạnh trái thẳng.
3. Mảng cam quanh xương thú lệch màu, mép cứng.
4. Cụm góc trái: thay "mỏm đá xoắn xám" của ảnh gốc bằng vòm đá cam + xương rồng xanh đặt NGAY SAU/TRÊN mái cổng tây nên nhìn như xương rồng mọc trên đỉnh cổng; chân vòm đá bị cắt phẳng ngang. Phải dời ra khỏi chiều đứng của cổng (lệch trái/sau ≥ 250 px) và dùng đá xoắn xám đúng ảnh gốc (hoặc yêu cầu asset mới).
5. Vẫn hai hàng: hàng nhỏ tiền cảnh y~720 (17 vật) cùng độ sâu; khoảng 560–700 còn thưa. Nhẹ.
Nhận xét nhỏ: xoáy cổng là các vòng đồng tâm phẳng, hơi giả (chấp nhận được).

## Cổng art tự động (17/10 16:20)
`tools/check.sh` giờ chạy thêm `tools/check_hd2d_art.sh` -> `tools/hd2d_audit/art_gate.py` (HD2D_ART_GATE=0 để bỏ qua). Quét kit batch-11-*: audit manifest (size/margin/màu/mật độ/seam/alpha), bbox-edge (vật bị cắt thẳng), tile sàn trùng ảnh, contact-sheet cũ hơn manifest, layout map (validator + 3 cam + preview + zoom, mới hơn layout.json). Miễn trừ chỉ do Claude/owner duyệt: tools/hd2d_audit/gate_waivers.json. Gemini phải chạy tới 0 lỗi trước khi báo nghiệm thu; Claude vẫn duyệt bằng mắt.

## Layout desert_entrance vòng 3 (17/10 16:10) — CHƯA NGHIỆM THU (3 lỗi mới + cổng art đỏ)
Đã sửa đúng: 18 asset bị cắt mép (bbox-edge desert = 0 trong repo gate), gốc cọ sạch mảng nâu, hàng ngang tiền cảnh đã so le, validator 0 lỗi (156 placement), 4 neo giữ px, ảnh bằng chứng đủ và mới hơn layout.json.
Lỗi còn/mới:
1. Cụm đá xoắn góc trái: crop trích từ ảnh gốc, sprite xám trắng lệch palette ấm, nằm sau mái cổng tây bị che gần hết, cạnh cắt phẳng; xương rồng xanh lục neon lơ lửng trên trời cạnh đá (cam 0.15). Tệ hơn vòng 2.
2. Mảng cát quanh xương thú giờ xanh chanh neon (cam 0.15/0.50), Gemini báo #D9B26B nhưng ảnh render ngược lại.
3. Decal gió cát (wind-sand) hình xoắn cam có viền nhạt + dither, đầu cụt cứng (cam 0.85, zoom cổng đông): trông dán lên.
4. Vài cạnh thẳng còn sót (đá nhỏ cạnh xương rồng ~x797 cam 0.15; cỏ lăn ~x550) dưới ngưỡng bbox 60%.
5. Cổng art: art_gate.py vẫn 47 lỗi toàn kit (desert: boulder-01 file 152x117 ≠ manifest 356x276 + COLORS 510 + SEMI_ALPHA; monster-bones SEMI_ALPHA; portal COLORS 794; contact-sheet cũ hơn manifest). Gemini báo "check.sh 100% green" nhưng chạy trước khi có cổng art; dùng bbox_edge.py riêng của Gemini (tools/assets) chỉ quét desert/đã bỏ qua nhiều loại.
Nhận xét nhỏ: xoáy cổng vẫn vòng đồng tâm phẳng.

## Layout desert_entrance vòng 4 (19/10 09:00) — ĐẠT CÓ ĐIỀU KIỆN (chuẩn mốc layout đầu tiên)
Tự kiểm: art_gate.py không còn lỗi nào của batch-11-desert (40 lỗi còn lại đều của windrock); validator 0 lỗi (138 placement); 4 neo giữ nguyên px; gate_waivers.json trống, không đụng script. Ảnh: hết xanh neon quanh xương thú (nay mô cát xám nhạt), bỏ cụm đá góc trái, hết decal xoắn cam dán, cạnh cắt rõ rệt đã hết, bố cục 3 tầng.
Điều kiện / tồn đọng nhỏ (không chặn):
- Landmark gốc "mỏm đá xoắn xám + xương rồng nghiêng" đã bị bỏ; ghi asset_requests để vẽ mới đúng palette cho vòng sau (cần giữ bố cục gốc).
- Xoáy cổng vẫn vòng đồng tâm phẳng; vệt cát xoắn còn dither nhẹ; đá nhỏ cạnh xương rồng ở cam 0.15 còn một cạnh thẳng nhẹ.
- Gemini viết "2D gốc không có cổng tây": sai, cổng do owner vẽ ở P12 (px [118,490]).
