# Prompt B — Đợt C10: Hoa Quỳnh (Lv76), Đông Trùng Hạ Thảo (Lv78), Vải Thiều (Lv80), Hổ Phách Mầm (Lv82), Sầu Riêng (Lv84)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C10 gồm 5 atlas Linh Thảo (cr-hoa-quynh, cr-dong-trung-ha-thao, cr-vai, cr-ho-phach-mam, cr-sau-rieng) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-hoa-quynh — Hoa Quỳnh (họ F, mở khoá Lv76)
   Hình thể: hoa trắng cánh dài nở đêm.
   Nhân vật: bé quỳnh ngái ngủ: ban ngày khép cánh, ban đêm bừng nở.
   Hành động ripe: mở cánh bung hoa, ngáp.
   Màu chủ đạo: trắng, vàng nhạt, xanh.
2. cr-dong-trung-ha-thao — Đông Trùng Hạ Thảo (họ N, mở khoá Lv78)
   Hình thể: xác sâu vàng nhạt, gậy nấm cam mảnh.
   Nhân vật: chú sâu ngái ngủ cầm cần nấm cam, huyền bí.
   Hành động ripe: ngáp, gậy nấm rung.
   Màu chủ đạo: vàng nhạt, cam.
3. cr-vai — Vải Thiều (họ D, mở khoá Lv80)
   Hình thể: quả đỏ gai nhỏ, vỏ nứt lộ cùi trắng.
   Nhân vật: bé vải: vỏ đỏ như áo, lộ mặt trắng tròn, ngọt ngào, má hồng.
   Hành động ripe: lột vỏ ngượng ngùng.
   Màu chủ đạo: đỏ, trắng, xanh.
4. cr-ho-phach-mam — Hổ Phách Mầm (họ T, mở khoá Lv82)
   Hình thể: mầm tinh thể hổ phách trong suốt.
   Nhân vật: ve hổ phách: hình sâu bọ trong hổ phách, cổ xưa, lõi ấm nhịp sáng.
   Hành động ripe: nhịp sáng chậm, mắt mở khẽ.
   Màu chủ đạo: hổ phách, cam nâu.
5. cr-sau-rieng — Sầu Riêng (họ D, mở khoá Lv84)
   Hình thể: quả gai nhọn lớn, múi kem.
   Nhân vật: dũng sĩ sầu riêng: vỏ gai là giáp, lạnh lùng nhưng ngọt bên trong, đỏ mặt khi được khen.
   Hành động ripe: hạ giáp lộ múi kem, khói mùi vàng xanh.
   Màu chủ đạo: xanh vàng gai, kem.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
