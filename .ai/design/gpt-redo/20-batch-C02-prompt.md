# Prompt B — Đợt C02: cr-nam-rom, cr-huong-duong, cr-ot, cr-sa
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C02 gồm 4 atlas Linh Thảo (cr-nam-rom, cr-huong-duong, cr-ot, cr-sa) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-nam-rom — Nấm Rơm (họ N, mở khoá Lv9)
   Hình thể: mũ nấm xám nâu hình trứng, bẹ trắng ở gốc.
   Nhân vật: bác nông dân nhỏ: mũ nấm như nón, cần cù, hay lau mồ hôi.
   Hành động ripe: vươn vai, lau trán, vẫy nón chào.
   Màu chủ đạo: xám nâu, trắng kem, vàng rơm.
2. cr-huong-duong — Hướng Dương (họ F, mở khoá Lv10)
   Hình thể: hoa vàng lớn tâm nâu hạt, thân thẳng lá to.
   Nhân vật: sư tử con hướng dương: cánh vàng quanh mặt như bờm, tự tin, mắt luôn nhìn lên trời.
   Hành động ripe: nhìn mặt trời, gầm nhỏ vui vẻ, bờm xoay nhẹ.
   Màu chủ đạo: vàng rực, nâu hạt, xanh lá.
3. cr-ot — Ớt (họ D, mở khoá Lv11)
   Hình thể: quả ớt đỏ cong thon, đài xanh.
   Nhân vật: rồng lửa nhỏ: thân ớt cong như đuôi rồng, nóng tính nhưng dễ thương.
   Hành động ripe: phì tia lửa cam nhỏ, rồi tự quạt cho mát.
   Màu chủ đạo: đỏ, cam, xanh cuống.
4. cr-sa — Sả (họ H, mở khoá Lv12)
   Hình thể: cụm lá dài nhọn, bẹ trắng tím ở gốc.
   Nhân vật: kiếm sĩ nhỏ: lá sả làm kiếm, nghiêm túc, thơm.
   Hành động ripe: múa kiếm lá một đường, tạo hương thơm nhẹ.
   Màu chủ đạo: xanh vàng, trắng tím nhạt.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
