# Prompt B — Đợt C01: cr-rau-ma, cr-khoai-lang, cr-tia-to, cr-ca-chua
Copy khối dưới gửi Codex.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT C01 gồm 4 atlas Linh Thảo (cr-rau-ma, cr-khoai-lang, cr-tia-to, cr-ca-chua) của khu vườn ngầm (garden-b). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi mọi atlas trong đợt qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (lore Linh Thảo, luật mặt, hợp đồng atlas), 15b-garden-crops-roster-v2.md (roster 60 cây), và pilot đã duyệt garden-b/cr-bac-ha, garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm chuẩn phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây là sinh vật nhỏ đáng yêu: mắt/mũi/miệng nhỏ, đọc được ở 48 px, tuyệt đối không kinh dị. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 PHẢI gần như lặp lại đường bao sprout f1 (IoU>=0.80): vẽ plant f4 bằng cách dùng khung sprout f1 của chính cây đó làm ảnh tham chiếu trong image_gen, giữ nguyên mũ/lá/rễ/tư thế/tỉ lệ, chỉ đổi biểu cảm; nên vẽ sprout f1 trước rồi mới vẽ plant f4. Cây to (chuối, dừa, mít, sầu riêng...) vẫn vẽ như sinh vật chibi nhỏ gọn trong khung, phần còn lại gợi ý bằng mũ/đuôi/tay.
KHÁC BIỆT: mỗi cây khác rõ về hình khối và màu so với các cây khác, kể cả pilot và các cây cùng đợt (silhouette đọc được khi thu nhỏ). Họ H/F/D/R/N/T chỉ là nhóm logic, không bắt buộc cùng kiểu.

NHÂN VẬT TRONG ĐỢT NÀY:
1. cr-rau-ma — Rau Má (họ H, mở khoá Lv2)
   Hình thể: bụi lá tròn hình quạt xanh non, thân bò thấp.
   Nhân vật: ếch con mát lạnh: hai lá tròn to làm tai hai bên, điềm tĩnh, hay buồn ngủ.
   Hành động ripe: ngồi thiền, thở ra bong bóng nước nhỏ, chớp mắt chậm.
   Màu chủ đạo: xanh lá mát, xanh ngọc, kem.
2. cr-khoai-lang — Khoai Lang (họ R, mở khoá Lv4)
   Hình thể: củ tím tròn dài lòi nửa trên đất, dây lá tim.
   Nhân vật: heo con củ khoai tím: mũi hồng, tham ăn, hay đỏ mặt.
   Hành động ripe: ôm bụng củ, hít mùi khoai nướng, nước dãi lấp lánh nhỏ.
   Màu chủ đạo: tím khoai, kem, xanh lá.
3. cr-tia-to — Tía Tô (họ H, mở khoá Lv6)
   Hình thể: lá răng cưa nhăn, mặt trên xanh mặt dưới tím.
   Nhân vật: dơi con: hai lá tía tô to làm cánh/tai, tinh ranh, hay ngáp ban ngày.
   Hành động ripe: xòe cánh lá rồi gập lại như áo choàng, lè lưỡi tinh nghịch.
   Màu chủ đạo: tím đậm, xanh lục, hồng tím.
4. cr-ca-chua — Cà Chua (họ D, mở khoá Lv7)
   Hình thể: quả đỏ tròn bóng, đài lá xanh năm cánh.
   Nhân vật: bé cà chua: má phúng phính, đài lá làm mũ, vui tính, hay lăn.
   Hành động ripe: lăn qua lại cười khúc khích, má đỏ hơn.
   Màu chủ đạo: đỏ tươi, xanh đài, vàng nhạt.
LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
