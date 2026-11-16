# Prompt B — Đợt C11: Nguyệt Huỳnh Tinh (Lv86), Tuyết Liên (Lv88), Tinh Hoa Liên (Lv90), Thạch Anh Quả (Lv92), Cà Phê (Lv94)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C11 gồm 5 atlas Linh Thảo (cr-nguyet-huynh-tinh, cr-tuyet-lien, cr-tinh-hoa-lien, cr-thach-anh-qua, cr-ca-phe) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-nguyet-huynh-tinh — Nguyệt Huỳnh Tinh (họ T, mở khoá Lv86)
   Hình thể: hoa tinh thể trắng lục nhạt.
   Nhân vật: đom đóm trăng: mắt sáng như trăng, nhút nhát.
   Hành động ripe: nháy sáng nhẹ, nấp.
   Màu chủ đạo: trắng lục nhạt, xanh bạc.
2. cr-tuyet-lien — Tuyết Liên (họ F, mở khoá Lv88)
   Hình thể: sen tuyết xanh trắng giữa lá lông.
   Nhân vật: cáo tuyết sen: tai sen trắng, lạnh lùng nhưng tinh nghịch.
   Hành động ripe: vẫy đuôi, rắc tuyết nhỏ.
   Màu chủ đạo: xanh trắng, bạc.
3. cr-tinh-hoa-lien — Tinh Hoa Liên (họ T, mở khoá Lv90)
   Hình thể: sen pha lê tím trắng nhiều mặt.
   Nhân vật: công chúa pha lê: lăng kính nhiều màu, tự tin.
   Hành động ripe: xoay các mặt pha lê lấp lánh.
   Màu chủ đạo: tím trắng, hồng lam.
4. cr-thach-anh-qua — Thạch Anh Quả (họ T, mở khoá Lv92)
   Hình thể: chùm quả thạch anh trong treo dây đá.
   Nhân vật: cú thạch anh: mắt tròn to, quả như trứng, thông thái.
   Hành động ripe: xoay đầu, quả trong lăn nhẹ.
   Màu chủ đạo: trong suốt, tím nhạt, xám đá.
5. cr-ca-phe — Cà Phê (họ D, mở khoá Lv94)
   Hình thể: cành quả đỏ cherry, lá bóng xanh.
   Nhân vật: bé hạt cà phê: mắt to tỉnh táo, run nhẹ, đội mũ quả đỏ.
   Hành động ripe: rung rung vì tỉnh táo, đưa tách tưởng tượng.
   Màu chủ đạo: nâu đậm, đỏ cherry, xanh bóng.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
