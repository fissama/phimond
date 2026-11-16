# Prompt B — Đợt C12: Hồ Tiêu (Lv96), Địa Mạch Kết Tinh (Lv98), Linh Mạch Mầm (Lv100)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C12 gồm 3 atlas Linh Thảo (cr-ho-tieu, cr-dia-mach-ket-tinh, cr-linh-mach-mam) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-ho-tieu — Hồ Tiêu (họ H, mở khoá Lv96)
   Hình thể: dây leo, chùm hạt tiêu xanh đỏ đen.
   Nhân vật: ong tiêu hay hắt xì: nhanh nhẹn, chùm hạt làm thân.
   Hành động ripe: hắt xì làm bụi tiêu bay.
   Màu chủ đạo: xanh, đỏ, đen.
2. cr-dia-mach-ket-tinh — Địa Mạch Kết Tinh (họ T, mở khoá Lv98)
   Hình thể: thân đá sẫm, gai tinh thể vàng theo mạch.
   Nhân vật: golem Linh Mạch nhỏ: mắt vàng như mạch, trầm tĩnh, canh giữ.
   Hành động ripe: mạch vàng chạy dọc thân, gật đầu.
   Màu chủ đạo: xám đá, vàng tinh thể.
3. cr-linh-mach-mam — Linh Mạch Mầm (họ T, mở khoá Lv100)
   Hình thể: mầm nhỏ mọc từ khối đá, vòng linh khí.
   Nhân vật: linh hồn của Linh Mạch: mầm trong thân đá, mắt vàng trầm xưa cũ, hiền và uy nghi.
   Hành động ripe: vòng linh khí xoay quanh mầm, nở lá.
   Màu chủ đạo: vàng linh khí, xanh ngọc, đá sẫm.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
