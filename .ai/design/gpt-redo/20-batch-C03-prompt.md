# Prompt B — Đợt C03: cr-cu-dau, cr-chuoi, cr-hoa-giay, cr-gung
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C03 gồm 4 atlas Linh Thảo (cr-cu-dau, cr-chuoi, cr-hoa-giay, cr-gung) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-cu-dau — Củ Đậu (họ R, mở khoá Lv13)
   Hình thể: củ trắng tròn dẹt như con quay, dây leo hoa tím.
   Nhân vật: con quay cười: thân củ dẹt tròn, ham chơi, hay xoay.
   Hành động ripe: xoay tròn trên mũi củ, dừng lại chóng mặt cười.
   Màu chủ đạo: trắng kem, tím nhạt, xanh lá.
2. cr-chuoi — Chuối (họ D, mở khoá Lv14)
   Hình thể: nải chuối vàng, lá chuối to, hoa chuối tím.
   Nhân vật: khỉ con chuối: nải chuối làm tay, lá chuối làm ô, tinh nghịch.
   Hành động ripe: bóc vỏ chuối làm trò, chớp mắt láu lỉnh.
   Màu chủ đạo: vàng chuối, xanh lá chuối, tím hoa.
3. cr-hoa-giay — Hoa Giấy (họ F, mở khoá Lv15)
   Hình thể: bông giấy hồng tím mỏng như giấy, cành có gai.
   Nhân vật: vũ công hoa giấy: cánh giấy hồng làm váy, tinh nghịch, mỏng manh.
   Hành động ripe: xoay váy một vòng, cánh giấy rung.
   Màu chủ đạo: hồng cánh sen đậm, cam, xanh.
4. cr-gung — Gừng (họ R, mở khoá Lv16)
   Hình thể: củ gừng nhiều ngón, lá thon.
   Nhân vật: người gừng: ngón củ làm tay chân, mặt cau có nhưng tốt bụng.
   Hành động ripe: giận dỗi giậm chân, má đỏ lên rồi cười hòa.
   Màu chủ đạo: vàng nâu, kem, xanh lá.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
