# Đơn 15 — Căn Mạch Linh Viên: 30 cây trồng có chuyển động (sprite atlas)

- Ngày: 2026-11-09. Dán master v2 + file này. Một phiên = MỘT cây (một atlas 20 khung). 30 cây = 5 đợt × 6 cây theo cặp tầng.
- **Pilot trước:** `cr-bac-ha` (lá, đung đưa) và `cr-moc-nhi` (nấm, bào tử) + chậu G1 (Đơn 14). Duyệt pipeline rồi mới vẽ tiếp.
- **Bảng 30 cây là DỰ THẢO chờ owner duyệt tên và thứ tự mở khóa** (sau đó đổi vào data P19/P15). Tên mượn dược liệu thật.
- Cây KHÔNG gắn tầng: trồng ở tầng nào cũng được; cột "mở" chỉ là cấp nông trại mở khóa (tầng 1 → Lv1, tầng N → Lv (N-1)×10).
- Engine lo (KHÔNG vẽ sẵn): biến dị (đổi tông hoặc quầng sáng cây chín), tối dần theo màn, tint, dấu chấm "chín" ở HUD.
- Thư mục: `art/src/hd2d/garden-b/<id>/` (raw-01.png, final.png, anim.json, prompt.md, review.md, qa.json, preview strip).

## Hợp đồng atlas

- `final.png` RGBA 768×960; ô 192×192; 4 cột × 5 hàng; 20 ô có nội dung và khác nhau.
- Mọi pixel alpha > 0 nằm trong [16, 176) theo x và y của ô. Hiệu ứng ở trong ô. Alpha nhị phân, không antialias/bloom/blur; ánh sáng là cụm pixel.
- Màu: thân cây 33–48 màu + hiệu ứng ≤ 12 màu; tổng ≤ 60 màu mỗi atlas.
- Neo gốc: điểm gốc/chỗ chạm đất của cây ở đúng (96, 168) ở mọi ô của hàng 1–3 và khung cuối hàng 5; sai số ≤ 2 px. Engine đặt điểm này lên neo miệng chậu (96,112) của Đơn 14.
- Chiều cao tối đa: chín ≈ 150 px (từ y 18 đến 168). Chiều cao các giai đoạn: sprout ≈ 25–30%, grow ≈ 55–65%, ripe = 100%. Cây rộng ≤ 140 px.
- Cùng một loài ở cả 20 khung: cùng hình dạng lá/quả/màu; chỉ lớn lên và chuyển động.

## Hàng animation (4 khung)

| Hàng | Tên | Phát | Nội dung |
|---|---|---|---|
| 1 | sprout | lặp, 3 fps | Mầm nhỏ vừa nhú, rung nhẹ theo gió dưới lòng đất |
| 2 | grow | lặp, 3 fps | Giai đoạn đang lớn: lá/thân/mũ nấm hình thành, đung đưa |
| 3 | ripe | lặp, 4 fps | Chín: hình đầy đủ, dễ nhận ra ở 48 px, có điểm sáng/lấp lánh theo họ (bảng dưới) |
| 4 | harvest | một lần, 10 fps | Nhổ/hái: cây bật lên, tung lá/vụn, tan thành tia sáng; khung 4 chỉ còn vài tia thưa |
| 5 | plant | một lần, 8 fps | Hạt rơi vào đất → đất gồ lên → mầm nhú; khung 4 ≈ khung 1 hàng sprout |

Cue chuyển động theo họ (hàng 3 ripe): Rễ và củ: lá đung đưa, củ phập phồng nhẹ. Nấm: mũ lấp bóng ẩm, bào tử bay lên. Dây leo và quả: dây đong đưa, quả lóe. Hoa và thảo dược: cánh lay, hạt phấn. Tinh thể: nhịp sáng chạy qua mặt tinh thể và lấp lánh cụm pixel.

## anim.json

{"cell":[192,192],"cols":4,"anchor":[96,168],"rows":[{"name":"sprout","fps":3,"loop":true},{"name":"grow","fps":3,"loop":true},{"name":"ripe","fps":4,"loop":true},{"name":"harvest","fps":10,"loop":false},{"name":"plant","fps":8,"loop":false}]}

## 30 cây (dự thảo)

Họ: R = Rễ và củ (7), N = Nấm (7), D = Dây leo và quả (6), H = Hoa và thảo dược (5), T = Tinh thể (5). Gold và thời gian chín tăng theo cấp mở (số cụ thể do P15).

| # | id | Tên | Họ | Mở (Lv farm) | Hình lúc chín |
|---|---|---|---|---|---|
| 1 | cr-bac-ha | Bạc Hà | H | 1 | Bụi thấp, lá răng cưa xanh tươi, gié hoa tím nhạt |
| 2 | cr-son-duoc | Sơn Dược | R | 1 | Dây khoai lá hình tim bám cọc nhỏ, một củ kem lộ trên đất |
| 3 | cr-moc-nhi | Mộc Nhĩ | N | 1 | Tai nấm nâu đen gợn sóng trên khúc gỗ mục, bóng ẩm |
| 4 | cr-cuc-hoa | Cúc Hoa | H | 10 | Cúc vàng nhiều lớp cánh trên thân mảnh |
| 5 | cr-dia-hoang | Địa Hoàng | R | 10 | Cụm lá nhăn dạng hoa thị, hoa chuông hồng tím, củ phình |
| 6 | cr-huong-co | Hương Cô | N | 10 | Chùm nấm mũ nâu đốm trắng trên gốc gỗ |
| 7 | cr-hong-tao | Hồng Táo | D | 20 | Cây táo tàu non, quả đỏ bóng, lá rì rào |
| 8 | cr-cat-can | Cát Căn | R | 20 | Dây sắn dây lá ba chạc, gié hoa tím, củ dày ở gốc |
| 9 | cr-bach-hop | Bách Hợp | H | 20 | Loa kèn trắng nhụy cam trên thân cao |
| 10 | cr-ky-tu | Kỷ Tử | D | 30 | Bụi cành cong, quả đỏ cam thon lủng lẳng |
| 11 | cr-duong-quy | Đương Quy | R | 30 | Tán hoa trắng hình ô, lá xẻ lông chim |
| 12 | cr-phuc-linh | Phục Linh | N | 30 | Tảng nấm tròn nâu vàng nứt vỏ, nửa chìm trong đất, ruột trắng, phập phồng |
| 13 | cr-son-tra | Sơn Tra | D | 40 | Cành táo gai quả đỏ tròn, lá xẻ thùy |
| 14 | cr-ha-thu-o | Hà Thủ Ô | R | 40 | Dây xoắn lá tim, củ nâu sẫm xù xì dáng người nhô lên |
| 15 | cr-hau-dau-co | Hầu Đầu Cô | N | 40 | Quả nấm trắng tua xù như đầu sư tử, tua rủ chậm |
| 16 | cr-moc-qua | Mộc Qua | D | 50 | Cây mộc qua non, quả vàng xanh to, hoa hồng nhạt |
| 17 | cr-tam-that | Tam Thất | R | 50 | Vòng lá chân vịt trên một thân, chùm quả đỏ trên đỉnh |
| 18 | cr-ngan-nhi | Ngân Nhĩ | N | 50 | Cụm nấm tuyết trắng ngà trong suốt, rìa nhăn, gợn sóng |
| 19 | cr-ngu-vi-tu | Ngũ Vị Tử | D | 60 | Dây leo, chùm quả đỏ tươi từng chuỗi |
| 20 | cr-thach-hoc | Thạch Hộc | H | 60 | Lan thân đốt vàng xanh, hoa kem phớt tím |
| 21 | cr-linh-chi | Linh Chi | N | 60 | Nấm lim nhiều tầng đỏ nâu bóng như sơn mài, viền ngà, vệt sáng lướt qua, vài hạt linh khí |
| 22 | cr-kim-anh-tu | Kim Anh Tử | D | 70 | Thân gai, quả cam hình bình, hoa trắng |
| 23 | cr-nhan-sam | Nhân Sâm | R | 70 | Thân đơn, chùm quả đỏ trên đỉnh, củ chẻ dáng người lộ nửa trên đất |
| 24 | cr-dong-trung-ha-thao | Đông Trùng Hạ Thảo | N | 70 | Xác sâu vàng nhạt, một gậy nấm cam mảnh nhô lên, uốn nhẹ, bào tử |
| 25 | cr-tuyet-lien | Tuyết Liên | H | 80 | Sen tuyết cánh xanh trắng xếp tầng giữa lớp lá phủ lông, sao băng cụm pixel |
| 26 | cr-ho-phach-mam | Hổ Phách Mầm | T | 80 | Mầm tinh thể hổ phách trong suốt, lõi ấm nhịp sáng |
| 27 | cr-nguyet-huynh-tinh | Nguyệt Huỳnh Tinh | T | 80 | Hoa tinh thể trắng lục nhạt, cánh nhọn như thạch anh, nhịp sáng lục nhạt |
| 28 | cr-tinh-hoa-lien | Tinh Hoa Liên | T | 90 | Sen pha lê tím trắng nhiều mặt cắt, lấp lánh lăng kính |
| 29 | cr-thach-anh-qua | Thạch Anh Quả | T | 90 | Chùm quả thạch anh trong, treo trên dây đá, mặt cắt lóe |
| 30 | cr-dia-mach-ket-tinh | Địa Mạch Kết Tinh | T | 90 | Thân đá sẫm, gai tinh thể vàng hổ phách dọc theo mạch như Linh Mạch, nhịp sáng |

Đợt vẽ: Đợt 0 pilot = #1, #3 (cùng chậu G1). Đợt 1 = #2, #4, #5, #6. Đợt 2 = #7–12. Đợt 3 = #13–18. Đợt 4 = #19–24. Đợt 5 = #25–30. Cây cấp cao có chi tiết nhiều hơn nhưng không vượt 150 px.

## Prompt cho image_gen

```text
Bạn là art worker của Phimond (HD-2D Octopath, pixel art). Vẽ MỘT sprite atlas 4 cột × 5 hàng cho một cây dược liệu trồng trong chậu dưới lòng đất, mỗi ô là một khung hoạt họa, theo chuẩn atlas linh thú. Cây: <id — Tên — họ — hình lúc chín trong bảng>.
Ảnh tham chiếu đính kèm (thứ tự): (a) batch-01-octopath/tree-large-01, mushroom-ochre, pebbles-01 final.png → style gốc; (b) garden-a/gd-decor-03, gd-decor-04, gd-roots-hang-04 final.png (đã duyệt) → họ màu của khu vườn; (c) DocDangNu/sprites.png và DaoThienDuong/sprites.png → BỐ CỤC ATLAS 4×5, độ dày outline, đổ khối, cách chia khung chuyển động; (d) asset pot G1 final.png (khi có) → cỡ tỉ lệ so với chậu. Ghi sha256 vào prompt.md.
Yêu cầu: nền #FF00FF phẳng, mỗi ô cách mép ô ≥ 16 px, mọi hiệu ứng ở trong ô. Nhìn thẳng mặt trước. Gốc cây ở (96,168) của ô 192×192 ở mọi khung hàng 1–3 (không vẽ chậu, không vẽ đất ngoài vệt đất nhỏ ở gốc). Ánh sáng: key ấm từ trên-trái-trước. Không bóng đổ xuống đất, không sương, không chữ, không nhân vật, không glow/bloom, ánh sáng bằng cụm pixel.
20 khung: hàng 1 sprout (lặp), hàng 2 grow (lặp), hàng 3 ripe (lặp), hàng 4 harvest (một lần), hàng 5 plant (một lần), như bảng. Chuyển động nhỏ (đung đưa ≤ 6 px), rõ nhịp, đọc được ở 48 px. Mỗi khung khác nhau thật. Cùng một loài ở mọi khung, chỉ lớn lên.
Hậu xử lý: code chỉ để cắt ô, khử nền, đưa về bảng màu, ghép nearest-neighbor đúng 768×960, kiểm. Không dùng code sinh hay vá hình.
```

## Nghiệm thu (Claude)

1. Cơ học: 768×960; 20 ô có nội dung và khác nhau; alpha nhị phân; mọi pixel trong [16,176); gốc (96,168) ±2 hàng 1–3; màu ≤ 60; chiều cao theo giai đoạn đạt tỉ lệ; báo bounds từng ô.
2. Chuyển động: preview từng hàng; hàng 1–3 lặp liền mạch; plant → sprout liền; harvest kết thúc thưa.
3. Hình: nhận ra loài ở 48 px; khác nhau rõ giữa 30 cây (silhouette và màu); đồng nhất 20 khung; style khớp.
4. Ghép thử: đặt cây vào chậu G1–G5 tại neo, 10 chậu một hàng với mix cây, xem dưới tint tối dần của 3 màn.
