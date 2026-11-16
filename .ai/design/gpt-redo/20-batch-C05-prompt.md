# Prompt B — Đợt C05: Ngải Cứu (Lv26), Nghệ (Lv28), Đu Đủ (Lv30), Hoa Súng (Lv32), Ổi (Lv34)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C05 gồm 5 atlas Linh Thảo (cr-ngai-cuu, cr-nghe, cr-du-du, cr-hoa-sung, cr-oi) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-ngai-cuu — Ngải Cứu (họ H, mở khoá Lv26)
   Hình thể: lá xẻ xám bạc, lông trắng mịn.
   Nhân vật: cừu con lông xám bạc: lá lông như len, hiền, tỏa khói thơm nhẹ.
   Hành động ripe: cuộn tròn ngủ, khói thơm xanh nhạt bay lên.
   Màu chủ đạo: xanh xám bạc, trắng.
2. cr-nghe — Nghệ (họ R, mở khoá Lv28)
   Hình thể: củ cam vàng đậm, hoa búp trắng hồng.
   Nhân vật: hổ con vằn nghệ: cam rực, vằn củ, dũng cảm, hay làm dữ.
   Hành động ripe: gầm bé xíu, vằn sáng lên.
   Màu chủ đạo: cam vàng đậm, kem.
3. cr-du-du — Đu Đủ (họ D, mở khoá Lv30)
   Hình thể: quả thon cam, thân thẳng, lá chân vịt như dù.
   Nhân vật: hươu cao cổ con: thân dài, quả làm bờm, lá làm tán, tò mò.
   Hành động ripe: vươn cổ nhìn quanh, hái sao.
   Màu chủ đạo: cam, xanh lá, nâu nhạt.
4. cr-hoa-sung — Hoa Súng (họ F, mở khoá Lv32)
   Hình thể: hoa súng tím hồng nổi trên lá tròn.
   Nhân vật: tiên cá nhỏ ngồi trên lá súng: mơ màng, hay hát.
   Hành động ripe: hát nhỏ, vòng nước lan quanh.
   Màu chủ đạo: tím hồng, xanh ngọc, vàng nhị.
5. cr-oi — Ổi (họ D, mở khoá Lv34)
   Hình thể: quả xanh tròn, hoa trắng, lá bầu dục.
   Nhân vật: chuột lang ổi: tròn xanh nhạt, hay ăn, nhút nhát.
   Hành động ripe: nhai gặm quả ổi nhỏ, má phồng.
   Màu chủ đạo: xanh nhạt, trắng, hồng ruột.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
