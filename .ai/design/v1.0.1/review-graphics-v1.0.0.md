# Đánh giá đồ họa Phimond v1.0.0 — góc nhìn người chơi khó tính

Phạm vi: 5 map Đợt A (Triệu Linh Điện, Bìa Rừng Lục Bảo, Rừng Sâu Lục Bảo, Hoàng Môn, Quảng Trường Thạch Trụ).
Căn cứ: ảnh chụp trong game thật ở 1280×720, soi từng khung hình của dải chạy nhân vật, và đọc cách client dựng map.
Chưa kiểm: máy thật (iPhone/Safari). Môi trường chụp không có GPU nên không đánh giá hiệu năng ở đây.

## Kết luận ngắn

Từng asset riêng lẻ (cây, nhà, tượng, giếng, linh thú, HUD) vẽ khá tốt. Cái hỏng là **cách chúng ghép với nhau**: không có chuyển tiếp giữa các loại mặt đất, viền map là cây rải ngẫu nhiên, vật đặt xuống đất không có bóng tiếp xúc, và nhân vật không có chu kỳ đi bộ thật. Người chơi nhìn ra ngay cảm giác "dán" vì các mảnh có độ nét, độ sáng và phong cách không khớp nhau. Vẽ đẹp từng món chưa đủ; phải vẽ cả các mảnh nối.

## Lỗi theo mức nghiêm trọng

### Nặng (người chơi thấy ngay, phá cảm giác chất lượng)

**N1. Nhân vật không có động tác đi bộ thật.** Dải "chạy" của nam và nữ có 8 khung nhưng đều là *cùng một tư thế đứng*, chỉ bị bóp/kéo phần chân bằng code. Chân gần như không bước (khung 4 và khung 8 còn lộ vệt ngang do kéo méo). Trong game nhân vật trượt trên đất. Chỉ có 1 hướng (phải), hướng trái là lật ngang; hoàn toàn không có hướng lên/xuống nên đi lên trên vẫn quay mặt ra trước. Khung chờ 4 khung chỉ khác nhau khoảng 2–5% (chỉ là hít thở).

**N2. Đường đất ở rừng là một hình chữ nhật cắt thẳng.** Ở Bìa Rừng và Rừng Sâu, đường là một mảng ô vuông gạch đất ghép cạnh nhau. Hai mép dài thẳng như dao cắt, hai đầu cụt ngang, không có cỏ lấn ra, không có chỗ đường loe hay hẹp. Texture đất còn *mờ và thô hơn* cây cỏ xung quanh (khác mật độ pixel), nên trông như tấm ảnh nền dán lên.

**N3. Viền map rừng là "tường cây rải ngẫu nhiên".** Cây ở rìa được đặt theo xác suất, nên chỗ dày đặc, chỗ hở, cây trùng lặp cùng mẫu thành hàng. Phía gần camera (mép dưới) để trống hoàn toàn. Bụi cây và cây lớn cùng một độ sáng nên mất chiều sâu: không có lớp tán phía sau, lớp thân giữa, lớp bụi phía trước. Ngoài rìa là một nền cỏ kéo dài cùng một texture, rồi tan vào sương (mình chưa chụp được ảnh các góc map, cần kiểm lại).

**N4. Tấm trải/gạch/bệ ở Quảng Trường và Hoàng Môn là các hình chữ nhật dán nổi.** Bệ lát sáng hơn dưới giếng thiên thần (một ô vuông xám nhạt lộ rõ viền), mảng gạch đỏ và thảm đỏ ở Hoàng Môn đều có mép thẳng, cắt cụt, không có sờn mép, không bóng, không viền đá chuyển. Nền đá cuội là một texture ô 4×4 lặp lại, có nguy cơ lộ nhịp lặp ở dải rộng.

### Trung bình

**T1. Vật thể "lơ lửng".** Quái đồng (nấm, nhện, ốc), NPC, thùng, chậu hoa, sạp chợ hầu như không có bóng tiếp xúc đúng hướng sáng, hoặc bóng quá yếu. Nhìn như sticker đặt trên mặt nền.

**T2. NPC không đồng bộ phong cách.** Có ít nhất 3 nhóm: NPC bản đầu (Odan, Elin, Selka) vẽ thân hình dày, viền đậm; 7 NPC mới nộp tạm (Mira, bia_skill, bia_free, trụ đá, kỹ năng, sàn giao dịch, kho) sáng hơn, mảnh hơn, sắc nét hơn. Chiều cao đầu/thân khác nhau giữa các NPC. Bảy NPC mới còn không có động tác chờ (khác 4 khung thở của nhóm cũ).

**T3. Dãy nhà phía sau lặp và phẳng.** Cùng vài mẫu mặt tiền xếp liền nhau, đáy nhà không có bóng đổ xuống nền, không có vật nối (ngõ, ống máng, cột). Bản v1.0.1 đã thêm một số mảnh nối nhưng cần vẽ lại cho khớp (xem phần yêu cầu vẽ).

**T4. Quái đồng khác tông với NPC.** Nấm đỏ dễ thương dạng chibi đứng cạnh NPC kiểu hiện thực. Không sai, nhưng cần quyết định thống nhất: hoặc làm NPC gần chibi hơn, hoặc quái đồng có viền và độ chi tiết tương đương NPC.

### Nhẹ

**L1. Triệu Linh Điện (sảnh):** tường và cột đẹp nhưng sàn gỗ tối, hai bên chân tường có vùng đen "hộp rỗng"; đèn lửa nhỏ thấp. Mira đứng sát tường nhưng sprite bị tường che hoàn toàn (xem báo cáo gameplay).

**L2. Khung UI:** bảng Menu có chữ tiêu đề đè lên khung, các nút xanh tràn ra ngoài viền khung kim loại (khung và nút không cùng kích thước). Hộp chat xanh phẳng, không cùng ngôn ngữ trang trí với các nút/biểu tượng vàng. Nhãn tên NPC là chữ trắng trơn trôi lơ lửng, đôi khi chồng lên tán cây.

**L3. Hoa văn lặp:** bụi hoa và nấm cùng mẫu lặp lại; lá rụng/đá cuội rải thưa quá, không phá được cảm giác "thảm cỏ một ô".

## Điểm đạt (giữ nguyên)

- Pixel-art cây, mặt tiền nhà, tượng, giếng, sạp chợ chất lượng tốt, đồng bộ bảng màu ấm.
- Linh thú trong trận (Sơn Chu, Hoa Loa) sắc nét, có hồn.
- Biểu tượng HUD/menu bên phải đẹp, thống nhất.

## Yêu cầu vẽ lại / vẽ mới (gửi GPT)

Mọi asset dùng hệ tỉ lệ hiện tại: 1 ô = 128 px, nhân vật cao khoảng 168 px trong khung 192×192, chân ở (96,184), nền ma-gen-ta #FF00FF để tách, alpha nhị phân, ≤64 màu, nhìn chéo từ trên xuống kiểu Octopath. **Bắt buộc dùng công cụ tạo ảnh, không dùng Python/code để ghép hay kéo méo** (vòng 2 từng bị ghép bằng code).

**A. Chu kỳ đi bộ nhân vật chính (nam + nữ)** — ưu tiên số 1.
- 3 hướng: bên (phải), trước (xuống), sau (lên). Trái dùng lật từ phải.
- Mỗi hướng 6 khung đi: tiếp xúc – hạ – qua – tiếp xúc (chân đối) – hạ – qua. Hai chân phải đổi bước thật, tay và áo choàng lắc ngược chiều.
- 4 khung chờ mỗi hướng (thở, áo choàng khẽ lay).
- Yêu cầu nghiệm thu: so các khung, chân không được là bản sao kéo giãn của khung khác; đường viền và bảng màu giữ y nhân vật gốc.

**B. Đường đất / đường lát cong tự nhiên** (rừng).
- Bộ mảnh rìa: đất → cỏ (4 cạnh, 4 góc trong, 4 góc ngoài), cỏ lấn ra bất quy tắc, vết bánh xe, đá nhỏ.
- Mảnh đầu/cuối đường (mòn dần vào cỏ), mảnh ngã ba, mảnh uốn cong.
- Cùng mật độ pixel với cây cỏ (không được mờ hơn), tile lặp ngang/dọc được.

**C. Viền map rừng theo lớp.**
- Lớp tán sau (tối, hơi mờ), lớp thân cây giữa, lớp bụi/dương xỉ trước; vài mẫu "đoạn tường cây" liền nhau, ghép nối được ở hai đầu.
- Mảnh góc map, mảnh viền phía camera (bụi rậm/đá thấp/gờ đất) để không lộ khoảng trống.
- Mảnh lối ra (cổng cây, đường mòn) rõ ràng cho các portal.

**D. Chuyển tiếp mặt đất thành phố.**
- Viền thảm đỏ có tua/sờn mép, bậc thềm đá, mép gạch đỏ vỡ dần vào đá cuội; nền đá cuội thêm 2–3 biến thể ô để phá nhịp lặp.
- Bệ giếng: bậc đá tròn có bóng và đá viền khớp nền cuội (thay ô vuông xám).

**E. Bóng tiếp xúc.** Bộ bóng mềm (tròn nhỏ, tròn lớn, chữ nhật, dài theo tán) cùng hướng sáng với nhà/cây; tông tối ấm, alpha nhị phân hoặc dithering.

**F. Đồng bộ NPC.** Chọn 1 chuẩn chiều cao (đầu:thân) và độ dày viền, vẽ lại NPC lệch chuẩn. Mỗi NPC có 4 khung chờ. Danh sách ưu tiên: 7 NPC nộp tạm trước.

**G. Khung UI.** Vẽ lại bảng Menu với khung có vùng nội dung cố định rộng hơn nút, tiêu đề nằm trên dải riêng; hộp chat cùng phong cách khung vàng với HUD.

## Tiêu chí duyệt chung cho người chơi khó tính

1. Dán sprite vào game, nhìn ở 1280×720 không thấy mép chữ nhật, không thấy nhịp lặp trong 8 giây đi bộ.
2. Mọi vật đặt xuống đất có bóng tiếp xúc.
3. Đi bộ nhìn ra *bước chân*, đổi hướng nhìn đổi tư thế thân.
4. Không có hai asset cùng loại khác phong cách (độ dày viền, độ bão hòa).
