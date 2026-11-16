# Prompt B — Đợt C04: Bí Đỏ (Lv18), Lá Lốt (Lv19), Khoai Môn (Lv20), Hoa Hồng (Lv22), Dưa Hấu (Lv24)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C04 gồm 5 atlas Linh Thảo (cr-bi-do, cr-la-lot, cr-khoai-mon, cr-hoa-hong, cr-dua-hau) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-bi-do — Bí Đỏ (họ D, mở khoá Lv18)
   Hình thể: quả bí cam tròn nhiều múi, cuống xoắn, hoa vàng.
   Nhân vật: bé bí đỏ tròn như đèn lồng: bụng múi, hiền lành, hay ngủ gật.
   Hành động ripe: ngáp, phình bụng thở nhẹ.
   Màu chủ đạo: cam, vàng, xanh sẫm.
2. cr-la-lot — Lá Lốt (họ H, mở khoá Lv19)
   Hình thể: lá hình tim bóng xanh đậm, gân rõ.
   Nhân vật: bé quấn lá: cuộn lá lốt làm áo choàng, nhút nhát, hay trốn.
   Hành động ripe: thò đầu khỏi áo lá, nhìn quanh, chớp mắt.
   Màu chủ đạo: xanh đậm bóng, kem.
3. cr-khoai-mon — Khoai Môn (họ R, mở khoá Lv20)
   Hình thể: củ nâu xù lông, lá bồ đại to hình tim.
   Nhân vật: voi con khoai môn: lá to làm tai, củ làm thân xù, hiền, thích hứng nước.
   Hành động ripe: hất vòi phun nước nhỏ qua đầu, tai lá vỗ.
   Màu chủ đạo: nâu xù, tím nhạt, xanh lá lớn.
4. cr-hoa-hong — Hoa Hồng (họ F, mở khoá Lv22)
   Hình thể: hoa đỏ nhung nhiều lớp, gai trên thân.
   Nhân vật: công chúa gai: cánh làm váy, gai nhỏ làm vương miện, kiêu kỳ nhưng dễ thương.
   Hành động ripe: cúi chào xoay váy.
   Màu chủ đạo: đỏ nhung, hồng, xanh sẫm.
5. cr-dua-hau — Dưa Hấu (họ D, mở khoá Lv24)
   Hình thể: quả xanh vằn, cắt lộ ruột đỏ hạt đen.
   Nhân vật: bé dưa hấu: vỏ sọc xanh, miệng cười toe lộ ruột đỏ.
   Hành động ripe: phì hạt dưa tinh nghịch bắn lên.
   Màu chủ đạo: xanh sọc, đỏ, đen.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
