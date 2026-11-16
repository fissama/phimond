# Prompt B — Đợt C08: Dừa (Lv56), Hoa Đào (Lv58), Mít (Lv60), Linh Chi (Lv62), Chôm Chôm (Lv64)
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C08 gồm 5 atlas Linh Thảo (cr-dua, cr-hoa-dao, cr-mit, cr-linh-chi, cr-chom-chom) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-dua — Dừa (họ D, mở khoá Lv56)
   Hình thể: quả dừa xanh nâu xơ, tàu lá cọ.
   Nhân vật: bé dừa: quả dừa làm đầu tròn, tàu lá làm tóc, nghịch ngợm.
   Hành động ripe: lắc đầu nghe nước bì bõm.
   Màu chủ đạo: xanh dừa, nâu xơ, trắng.
2. cr-hoa-dao — Hoa Đào (họ F, mở khoá Lv58)
   Hình thể: đào hồng nhạt nhiều cánh, cành nâu uốn.
   Nhân vật: nai con đào: sừng là cành đào nở hoa, dịu dàng.
   Hành động ripe: lắc sừng rắc cánh hoa hồng.
   Màu chủ đạo: hồng đào, nâu cành, xanh nụ.
3. cr-mit — Mít (họ D, mở khoá Lv60)
   Hình thể: quả gai xanh vàng, múi vàng.
   Nhân vật: tê tê mít: vảy gai như mít, cuộn tròn nhút nhát.
   Hành động ripe: mở mình lộ múi vàng, cười ngượng.
   Màu chủ đạo: xanh vàng gai, cam múi.
4. cr-linh-chi — Linh Chi (họ N, mở khoá Lv62)
   Hình thể: nấm lim nhiều tầng đỏ nâu sơn mài.
   Nhân vật: rùa linh chi: tầng nấm như mai rùa, cụ ông trường thọ.
   Hành động ripe: thở linh khí chậm, tầng nấm rung.
   Màu chủ đạo: đỏ nâu sơn mài, vàng.
5. cr-chom-chom — Chôm Chôm (họ D, mở khoá Lv64)
   Hình thể: quả đỏ phủ lông xù mềm.
   Nhân vật: sinh vật lông xù đỏ: mắt nhỏ, hay lăn, hơi ngố.
   Hành động ripe: lăn tròn rồi lắc cho lông bay.
   Màu chủ đạo: đỏ, vàng, xanh đầu lông.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
