# Prompt B — Đợt C06: Riềng (Lv36), Mướp Đắng (Lv38), Kỷ Tử (Lv40), Hoa Mai (Lv42), Xoài (Lv44)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C06 gồm 5 atlas Linh Thảo (cr-rieng, cr-muop-dang, cr-ky-tu, cr-hoa-mai, cr-xoai) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-rieng — Riềng (họ R, mở khoá Lv36)
   Hình thể: củ nâu hồng đốt, lá thẳng.
   Nhân vật: cua đồng riềng: củ đốt làm càng, nóng tính, hay kẹp.
   Hành động ripe: giơ càng đe dọa rồi lại cười.
   Màu chủ đạo: nâu hồng, kem, xanh lá.
2. cr-muop-dang — Mướp Đắng (họ D, mở khoá Lv38)
   Hình thể: quả xanh sần sùi, hoa vàng.
   Nhân vật: cá sấu con mướp đắng: sần sùi cau có nhưng hiền (đắng đầu ngọt hậu).
   Hành động ripe: nhăn mặt rồi mỉm cười.
   Màu chủ đạo: xanh đậm sần, vàng.
3. cr-ky-tu — Kỷ Tử (họ D, mở khoá Lv40)
   Hình thể: cành cong, quả đỏ cam thon.
   Nhân vật: đàn sẻ quả đỏ đậu cành, líu lo, mỗi quả một mặt.
   Hành động ripe: líu lo, quả đỏ nghiêng đầu.
   Màu chủ đạo: đỏ cam, xanh lá nhạt.
4. cr-hoa-mai — Hoa Mai (họ F, mở khoá Lv42)
   Hình thể: mai vàng năm cánh nhiều nụ, cành nâu.
   Nhân vật: chim én hoa mai: cánh vàng như cánh hoa, báo xuân, vui.
   Hành động ripe: vỗ cánh rắc cánh mai nhỏ, ngậm lì xì tưởng tượng.
   Màu chủ đạo: vàng mai, nâu cành, xanh nụ.
5. cr-xoai — Xoài (họ D, mở khoá Lv44)
   Hình thể: quả vàng cong, lá thon xanh.
   Nhân vật: vẹt xoài: quả làm thân, lá làm đuôi, nói nhiều.
   Hành động ripe: mở mỏ nói liên hồi, vỗ cánh.
   Màu chủ đạo: vàng, xanh lá, cam.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
