# Prompt B — Đợt C07: Sắn (Lv46), Nấm Đầu Khỉ (Lv48), Hoa Sen (Lv50), Bưởi (Lv52), Tam Thất (Lv54)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C07 gồm 5 atlas Linh Thảo (cr-san, cr-hau-dau-co, cr-hoa-sen, cr-buoi, cr-tam-that) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-san — Sắn (họ R, mở khoá Lv46)
   Hình thể: củ nâu dài, lá chân vịt năm thùy.
   Nhân vật: chó con sắn: củ dài làm đuôi, hiền, trung thành.
   Hành động ripe: vẫy đuôi củ, sủa nhỏ vui.
   Màu chủ đạo: nâu, kem, xanh.
2. cr-hau-dau-co — Nấm Đầu Khỉ (họ N, mở khoá Lv48)
   Hình thể: quả nấm trắng tua xù.
   Nhân vật: khỉ sư tử trắng: tua xù như bờm, nghiêm nghị.
   Hành động ripe: vuốt bờm, gật đầu nghiêm trang.
   Màu chủ đạo: trắng kem, xám nhạt.
3. cr-hoa-sen — Hoa Sen (họ F, mở khoá Lv50)
   Hình thể: sen hồng, lá tròn lớn, gương sen.
   Nhân vật: bé sen bình thản ngồi giữa lá, ngón tay chạm nước.
   Hành động ripe: chạm nước tạo gợn sóng, nở nhẹ cánh.
   Màu chủ đạo: hồng sen, xanh lá, vàng nhị.
4. cr-buoi — Bưởi (họ D, mở khoá Lv52)
   Hình thể: quả to xanh vàng, hoa trắng.
   Nhân vật: ông bưởi tròn hiền: râu bằng xơ trắng, hay mỉm cười, ngồi vững.
   Hành động ripe: vuốt râu xơ, cười hiền.
   Màu chủ đạo: xanh vàng, trắng.
5. cr-tam-that — Tam Thất (họ R, mở khoá Lv54)
   Hình thể: vòng lá chân vịt, chùm quả đỏ đỉnh.
   Nhân vật: gà con mào quả đỏ: nhanh nhẹn, ba lá làm đuôi.
   Hành động ripe: mổ nhanh, mào quả đỏ rung.
   Màu chủ đạo: xanh, đỏ, kem.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
