Vòng 3 `desert_entrance`: có tiến bộ thật, nhưng hai thay đổi mới làm cảnh xấu đi nên chưa nghiệm thu. Claude tự chạy lại validator, cổng art của repo và xem toàn bộ ảnh.
Đã đúng: 18 asset hết cắt mép (repo gate bbox-edge cho desert = 0), gốc cọ sạch, hàng prop tiền cảnh đã so le, validator 0 lỗi, neo không đổi, ảnh bằng chứng đủ.

Sửa nốt (vòng 4):
1. Cụm đá xoắn góc trái hỏng, tệ hơn vòng 2: sprite xám trắng cắt từ ảnh gốc lệch palette ấm, nằm sau mái cổng tây bị che gần hết, cạnh cắt phẳng; xương rồng xanh lục neon lơ lửng trên trời cạnh đá (cam 0.15 x 245–390, y 75–170). Không dùng crop từ ảnh gốc. Hoặc vẽ asset mới đúng palette (đá xoắn xám ấm + xương rồng) đặt xa cổng ≥300 px ngang hoặc ở cồn xa không bị cổng che, hoặc bỏ cụm và ghi lý do. Nếu vẽ mới, ghi vào manifest như asset thường.
2. Mảng cát quanh xương thú giờ xanh chanh neon (cam 0.15/0.50). Báo cáo ghi #D9B26B nhưng ảnh render nói ngược lại. Kiểm lại file texture thật dùng trong scene; phải đúng tông cát vàng, mép mềm.
3. Decal gió cát xoắn màu cam có viền nhạt, dither và đầu cụt cứng (cam 0.85; zoom cổng đông) — trông dán lên. Vẽ lại mềm, đầu thon tan dần, cùng tông sàn; hoặc bỏ bớt.
4. Vẫn còn vài cạnh thẳng nhỏ dưới ngưỡng 60%: đá nhỏ cạnh xương rồng ở cam 0.15 (khoảng x 797) và cỏ lăn ở khoảng x 550. Soi lại asset small-rock-03 và tumbleweed; mọi cạnh trái/phải của vật phải bo theo hình vật.
5. Chạy `sh tools/check_hd2d_art.sh` của repo (không dùng bản tools/assets/bbox_edge.py riêng, vì nó chỉ quét desert và bỏ qua nhiều loại). Hiện còn 47 lỗi cho cả kit; phần desert: `desert-boulder-01` file 152×117 khác manifest 356×276 (kèm COLORS 510, SEMI_ALPHA), `desert-monster-bones` SEMI_ALPHA 0.034, hai cổng portal COLORS 794 (vượt ≤64), contact-sheet.png cũ hơn manifest. Sửa asset hoặc nêu lý do để Claude cân nhắc miễn trừ; không tự sửa script/waiver.
Ghi chú nhỏ: xoáy cổng vẫn là vòng đồng tâm phẳng, nên vẽ có chiều sâu hơn khi có thời gian.
"check.sh 100% green" không còn đúng: check.sh nay chạy thêm cổng art và đang đỏ.
Nộp: layout.json, 3 cam + zoom (cổng tây, cổng đông, Edda, cụm góc trái) mới render, `check_hd2d_art.sh` phần desert = 0 lỗi, tự nhìn ảnh trước khi nói "đạt".
Phong Thạch chỉ bắt đầu sau khi vòng 4 đạt.
