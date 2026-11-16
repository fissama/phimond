# Đơn 15 v2 — Căn Mạch Linh Viên: 30 LINH THẢO (cây có mặt, có tính cách, có chuyển động)

- Ngày: 2026-11-09. Thay thế bản tĩnh (lưu ở `15-garden-crops-anim-prompt-v1-static.md`). Dán master v2 + file này. Một phiên = MỘT cây (một atlas 20 khung).
- **Hướng mới (owner):** cây trồng không phải đồ vật cứng. Mỗi cây là một **Linh Thảo**: sinh vật nhỏ, có mắt, miệng, tính cách, theo motif thú hoặc người, vẫn nhận ra loài dược liệu. Mục tiêu: người chơi muốn nhìn, chạm, thu hoạch vì thấy chúng sống động, như thú nuôi mini.
- Pilot bản tĩnh (Bạc Hà, Mộc Nhĩ) bị trả: xem `garden-b/REVIEW-CLAUDE-20261109.md`. Vẽ lại hai cây này theo v2 làm pilot mới (Đợt 0).
- Cây KHÔNG gắn tầng. "Mở" là cấp nông trại mở khóa. Bảng tên 30 cây đã duyệt (giữ ID).
- Engine lo (KHÔNG vẽ): biến dị (đổi tông/quầng sáng), tối dần theo màn, tint, chấm "chín" HUD.

## Lore ngắn (để GPT hiểu vai)

Linh Mạch chảy dưới lòng đất sinh ra Linh Thảo: hạt giống do quái mang xuống, gặp mạch thì hóa thành sinh vật nhỏ ngủ trong chậu. Chúng không chiến đấu, không bắt được, không phải linh thú (khác pet: nhỏ hơn, chỉ có cây trong mình, không vũ khí). Khi người chơi thu hoạch, chúng chào rồi hóa thành vật phẩm sáng; không đau, không máu, không chết.

## Quy tắc mặt và tính cách

1. Mỗi Linh Thảo có MẶT đọc được ở 48 px: hai mắt (3×3 đến 5×5 pixel, tối, có 1–2 px sáng), miệng nhỏ, tùy chọn má hồng/lông mày. Mặt ≤ 20% thân. Mặt đặt trên phần thân chính (củ, mũ nấm, quả, tâm hoa, mặt tinh thể).
2. Dáng theo motif trong bảng (thú hoặc người), pha với đặc trưng dược liệu thật (lá, củ, quả, hoa). Vẫn nhận ra là cây thuốc đó. Không chép nhân vật hay linh thú có sẵn; thiết kế gốc.
3. Chân tay: ngắn, chibi (đầu to thân nhỏ), tay là tua/lá/rễ nhỏ. Chân chìm trong đất hoặc ở sau mép chậu; gốc (điểm chạm đất) cố định tại (96,168).
4. Biểu cảm theo giai đoạn (cùng nhân vật ở cả 20 khung): sprout = ngái ngủ/ngơ ngác; grow = tò mò, vui, nhìn quanh; ripe = tự hào/hạnh phúc, tạo dáng; harvest = ngạc nhiên rồi vẫy chào, biến thành tia sáng; plant = tỉnh dậy, ngáp, vươn vai.
5. Chớp mắt ít nhất một khung mỗi hàng lặp. Một cử chỉ nhỏ riêng cho mỗi cây (ví dụ ngửi, vẫy, ngáp, tự soi). Mỗi cây phải có tính cách khác 29 cây còn lại.
6. Hiền, dễ thương, hợp mọi lứa tuổi; không đáng sợ, không đau đớn, không máu.

## Hợp đồng atlas

- `final.png` RGBA 768×960; ô 192×192; 4 cột × 5 hàng; 20 ô đều có nội dung, khác nhau.
- Mọi pixel alpha > 0 nằm trong x và y thuộc [16, 176] của ô (y tối đa 175). Hiệu ứng ở trong ô. Alpha nhị phân; không antialias/blur/bloom; ánh sáng là cụm pixel. Pixel alpha = 0 có RGB = 0.
- Màu: thân 33–48 + hiệu ứng ≤ 12; tổng ≤ 60 màu mỗi atlas.
- Neo gốc (96,168), sai số ≤ 2 px ở MỌI ô hàng 1–3 và khung cuối hàng 5; đo theo tâm x của 6 hàng pixel thấp nhất (không dùng lá/tua rủ). Lệch tâm x giữa các khung ≤ 3 px (trừ sway của lá).
- Chiều cao (từ pixel cao nhất đến y=168): sprout 25–30% (38–45 px), grow 55–65% (83–98 px), ripe 100% (đến 150 px). Rộng ≤ 140 px. Cao hơn mức này = trả.
- CÙNG nhân vật ở 20 khung: cùng mặt, màu, cấu tạo, số chi tiết; chỉ lớn lên và cử động. Tránh vẽ lại mỗi khung (đổ khối nhấp nháy): vẽ khung 1 làm gốc, các khung sau chỉ đổi phần cử động (lá, tay, mắt, miệng, hạt); phần thân giữ nguyên pixel khi có thể.

## Hàng animation

| Hàng | Tên | Phát | Nội dung |
|---|---|---|---|
| 1 | sprout | lặp, 3 fps | Bé con ngái ngủ nhú lên: mắt nhắm hé, ngáp, gật gù; khung 4 → 1 liền |
| 2 | grow | lặp, 3 fps | Lớn hơn, tò mò: nhìn quanh, chớp mắt, đung đưa, vẫy lá/tay |
| 3 | ripe | lặp, 4 fps | Chín rộ, tự hào/vui: chớp mắt, nháy mắt, tạo dáng, cử chỉ riêng; điểm sáng theo họ; đọc rõ ở 48 px |
| 4 | harvest | một lần, 10 fps | Giật mình rồi vẫy chào, bật lên, hóa thành tia sáng/vật phẩm; khung 4 chỉ còn vài tia thưa (không đau) |
| 5 | plant | một lần, 8 fps | Hạt rơi, đất gồ, ló mắt tỉnh dậy, ngáp; khung 4 ≈ khung 1 hàng sprout (pixel khác ≤ 15%) |

Cue theo họ (hàng 3): Rễ và củ: tay lá vẫy, củ phập phồng. Nấm: mũ nhấp nhô, bào tử bay như hơi thở. Dây leo và quả: tua đong đưa, quả lóe. Hoa và thảo dược: cánh lay, phấn bay. Tinh thể: nhịp sáng lướt qua mặt tinh thể, mắt phát sáng.

## anim.json

{"cell":[192,192],"cols":4,"anchor":[96,168],"rows":[{"name":"sprout","fps":3,"loop":true},{"name":"grow","fps":3,"loop":true},{"name":"ripe","fps":4,"loop":true},{"name":"harvest","fps":10,"loop":false},{"name":"plant","fps":8,"loop":false}]}

## 30 Linh Thảo

Họ: R Rễ và củ, N Nấm, D Dây leo và quả, H Hoa và thảo dược, T Tinh thể. Mở = cấp nông trại. Cột Motif và tính cách là hướng vẽ; GPT được tự do chi tiết nhưng giữ nhận diện dược liệu.

| # | id | Tên | Họ | Mở | Hình dược liệu | Motif và tính cách |
|---|---|---|---|---|---|---|
| 1 | cr-bac-ha | Bạc Hà | H | 1 | Bụi lá răng cưa xanh tươi, gié hoa tím nhạt | Mèo bạc hà: tai là hai lá nhọn, mắt xanh to, ngửi gió phấn khích |
| 2 | cr-son-duoc | Sơn Dược | R | 1 | Dây lá tim bám cọc, củ kem | Rắn con hiền: thân dây cuộn, củ kem là bụng tròn, lười biếng |
| 3 | cr-moc-nhi | Mộc Nhĩ | N | 1 | Tai nấm nâu đen gợn sóng trên khúc gỗ | Thỏ tai nấm: hai tai gợn sóng, rụt rè, hay giật mình |
| 4 | cr-cuc-hoa | Cúc Hoa | H | 10 | Cúc vàng nhiều lớp cánh | Cô bé cúc: cánh làm tóc xoăn, má hồng, hay cười |
| 5 | cr-dia-hoang | Địa Hoàng | R | 10 | Hoa thị lá nhăn, chuông hồng tím, củ phình | Chuột chũi củ: mũi hồng, mắt nhỏ tròn, cần cù |
| 6 | cr-huong-co | Hương Cô | N | 10 | Chùm nấm mũ nâu đốm trắng | Người nấm hương: mũ như mũ đầu bếp, hiền, hay nấu nướng giả |
| 7 | cr-hong-tao | Hồng Táo | D | 20 | Táo tàu đỏ bóng, lá rì rào | Bé táo đỏ: má phúng phính, lá làm mũ, nghịch ngợm |
| 8 | cr-cat-can | Cát Căn | R | 20 | Dây sắn lá ba chạc, hoa tím, củ dày | Khỉ dây: đu tua, hiếu động |
| 9 | cr-bach-hop | Bách Hợp | H | 20 | Loa kèn trắng nhụy cam | Nàng tiên loa kèn: mắt nhắm mơ, thanh nhã |
| 10 | cr-ky-tu | Kỷ Tử | D | 30 | Cành cong, quả đỏ cam thon | Đàn chim sẻ quả đỏ đậu cành, líu lo, mỗi quả một mặt |
| 11 | cr-duong-quy | Đương Quy | R | 30 | Tán hoa trắng hình ô, lá xẻ | Bà lão hoa trắng: tán hoa như tóc bạc, hiền, nhớ nhà |
| 12 | cr-phuc-linh | Phục Linh | N | 30 | Tảng nấm tròn nâu vàng nứt vỏ, ruột trắng | Cục mochi ngái ngủ: tròn, hay ngáp, phập phồng như thở |
| 13 | cr-son-tra | Sơn Tra | D | 40 | Cành quả đỏ tròn, lá xẻ thùy | Sóc táo gai: đuôi lá, lém lỉnh |
| 14 | cr-ha-thu-o | Hà Thủ Ô | R | 40 | Dây xoắn lá tim, củ nâu dáng người | Ông lão củ: râu rễ bạc, kể chuyện, mắt hiền |
| 15 | cr-hau-dau-co | Hầu Đầu Cô | N | 40 | Quả nấm trắng tua xù | Khỉ sư tử trắng: tua xù như bờm, nghiêm nghị |
| 16 | cr-moc-qua | Mộc Qua | D | 50 | Cây non, quả vàng xanh to, hoa hồng | Anh chàng gấu quả vàng: to xác hiền, hoa nhỏ trên đầu |
| 17 | cr-tam-that | Tam Thất | R | 50 | Vòng lá chân vịt, chùm quả đỏ đỉnh | Gà con mào quả đỏ: nhanh nhẹn, ba lá làm đuôi |
| 18 | cr-ngan-nhi | Ngân Nhĩ | N | 50 | Cụm nấm tuyết trắng trong suốt | Nàng nấm tuyết: váy xếp bồng, e thẹn |
| 19 | cr-ngu-vi-tu | Ngũ Vị Tử | D | 60 | Dây leo, chuỗi quả đỏ | Rồng dây nhỏ: dây uốn như rồng, quả như ngọc, kiêu hãnh |
| 20 | cr-thach-hoc | Thạch Hộc | H | 60 | Lan thân đốt, hoa kem phớt tím | Hạc lan: thân đốt như chân hạc, hoa như mào, thanh cao |
| 21 | cr-linh-chi | Linh Chi | N | 60 | Nấm lim nhiều tầng đỏ nâu sơn mài | Rùa linh chi: tầng nấm như mai rùa, cụ ông trường thọ, hạt linh khí |
| 22 | cr-kim-anh-tu | Kim Anh Tử | D | 70 | Thân gai, quả cam hình bình, hoa trắng | Nhím quả cam: gai như lông nhím, nhút nhát cuộn tròn |
| 23 | cr-nhan-sam | Nhân Sâm | R | 70 | Thân đơn, chùm quả đỏ đỉnh, củ chẻ dáng người | Bé nhân sâm: đứa trẻ rễ trắng, mũ quả đỏ, tinh nghịch như hay chạy trốn |
| 24 | cr-dong-trung-ha-thao | Đông Trùng Hạ Thảo | N | 70 | Xác sâu vàng nhạt, gậy nấm cam mảnh | Chú sâu ngái ngủ cầm cần nấm cam, huyền bí |
| 25 | cr-tuyet-lien | Tuyết Liên | H | 80 | Sen tuyết xanh trắng giữa lá lông | Cáo tuyết sen: tai sen trắng, lạnh lùng nhưng tinh nghịch |
| 26 | cr-ho-phach-mam | Hổ Phách Mầm | T | 80 | Mầm tinh thể hổ phách trong suốt | Ve hổ phách: hình sâu bọ trong hổ phách, cổ xưa, lõi ấm nhịp sáng |
| 27 | cr-nguyet-huynh-tinh | Nguyệt Huỳnh Tinh | T | 80 | Hoa tinh thể trắng lục nhạt | Đom đóm trăng: mắt sáng như trăng, nhút nhát |
| 28 | cr-tinh-hoa-lien | Tinh Hoa Liên | T | 90 | Sen pha lê tím trắng nhiều mặt | Công chúa pha lê: lăng kính nhiều màu, tự tin |
| 29 | cr-thach-anh-qua | Thạch Anh Quả | T | 90 | Chùm quả thạch anh trong treo dây đá | Cú thạch anh: mắt tròn to, quả trong như trứng, thông thái |
| 30 | cr-dia-mach-ket-tinh | Địa Mạch Kết Tinh | T | 90 | Thân đá sẫm, gai tinh thể vàng theo mạch | Golem Linh Mạch nhỏ: mắt vàng như mạch, trầm tĩnh, canh giữ |

Đợt vẽ: Đợt 0 pilot v2 = #1 Bạc Hà, #3 Mộc Nhĩ, cùng chậu G1 v2. Đợt 1 = #2, #4, #5, #6. Đợt 2 = #7–12. Đợt 3 = #13–18. Đợt 4 = #19–24. Đợt 5 = #25–30.

## Prompt cho image_gen

```text
Bạn là art worker của Phimond (HD-2D Octopath, pixel art). Vẽ MỘT sprite atlas 4 cột × 5 hàng cho một LINH THẢO (sinh vật cây thuốc nhỏ, có mặt, có tính cách, chibi), mỗi ô là một khung hoạt họa, theo chuẩn atlas linh thú. Nhân vật: <id — Tên — họ — hình dược liệu — motif và tính cách trong bảng>.
Ảnh tham chiếu đính kèm (thứ tự): (a) batch-01-octopath/mushroom-ochre, pebbles-01 final.png → style gốc; (b) garden-a/gd-decor-03, gd-roots-hang-04 final.png → họ màu khu vườn; (c) DocDangNu/sprites.png và DaoThienDuong/sprites.png → BỐ CỤC ATLAS 4×5, độ dày outline, đổ khối pixel-cluster, MẶT/BIỂU CẢM chibi và cách chia khung chuyển động; (d) pot-g1-tho-dao final.png (khi có) → tỉ lệ so với chậu. Ghi sha256 vào prompt.md.
Yêu cầu: nền #FF00FF phẳng; mỗi ô cách mép ô ≥ 16 px; hiệu ứng ở trong ô. Nhìn thẳng mặt trước, hơi nhìn xuống như linh thú. Gốc ở (96,168) mọi khung hàng 1–3. Nhân vật có MẶT rõ (2 mắt 3–5 px, miệng nhỏ, má), tính cách thể hiện qua tư thế và cử chỉ. Vẽ khung 1 làm gốc; các khung sau chỉ đổi phần cử động (mắt, miệng, lá, tay, đung đưa), giữ nguyên pixel thân để không nhấp nháy. Ánh sáng key ấm trên-trái-trước; không bóng đổ xuống đất, không sương, không chữ, không glow/bloom.
20 khung: hàng 1 sprout (lặp, ngái ngủ), hàng 2 grow (lặp, tò mò), hàng 3 ripe (lặp, tự hào), hàng 4 harvest (một lần, giật mình rồi vẫy chào và hóa tia sáng, hiền), hàng 5 plant (một lần, tỉnh dậy ngáp). Chiều cao: sprout 38–45 px, grow 83–98 px, ripe tối đa 150 px. Chuyển động nhỏ, rõ nhịp, đọc được ở 48 px. Hiền, dễ thương, không đáng sợ, không máu.
Hậu xử lý: code chỉ cắt ô, khử nền, đưa về bảng màu, ghép nearest-neighbor đúng 768×960, đặt RGB = 0 cho pixel alpha = 0, kiểm. Không dùng code sinh hay vá hình.
```

## Nghiệm thu (Claude)

1. Cơ học: 768×960; 20 ô khác nhau; alpha nhị phân; mọi pixel trong [16,175]; neo (96,168) ±2; chiều cao đúng 3 mức; màu ≤ 60; RGB = 0 ở alpha = 0; báo bounds từng ô.
2. Chuyển động: preview từng hàng; lặp liền; plant → sprout liền; harvest kết thúc thưa.
3. Sống động: mặt đọc được ở 48 px; biểu cảm đúng giai đoạn; có chớp mắt và cử chỉ riêng; nhận ra dược liệu; khác 29 cây kia.
4. Thân không nhấp nháy: so khung liền kề sau căn thẳng, chỉ phần cử động đổi.
5. Ghép thử: cây vào chậu G1–G5 tại neo, 10 chậu một hàng với mix cây, dưới tint tối dần 3 màn.
