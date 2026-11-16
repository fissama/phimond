# Prompt B — Đợt 1: 4 Linh Thảo (Sơn Dược, Cúc Hoa, Địa Hoàng, Hương Cô)
Copy khối dưới gửi Codex. Pilot garden-b đã duyệt (Claude 2026-11-10) là chuẩn phong cách.

```
NHIỆM VỤ: Vẽ và đóng gói ĐỢT 1 garden-b: 4 atlas Linh Thảo — cr-son-duoc (#2), cr-cuc-hoa (#4), cr-dia-hoang (#5), cr-huong-co (#6). KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng cây; chỉ báo xong khi cả 4 atlas qua đủ cổng a–j của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 15-garden-crops-anim-prompt.md (v2: lore Linh Thảo, luật mặt, bảng 30 dòng, hợp đồng atlas), và pilot đã duyệt: garden-b/cr-bac-ha và garden-b/cr-moc-nhi (final.png, anim.json, prompt.md, review.md) làm mẫu phong cách, kích thước, hiệu ứng.

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py (căn pivot, một tỉ lệ chung, nearest-neighbor) -> tools/measure_atlas.py. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, pivot gốc (96,168), hàng: sprout, grow, ripe (lặp), harvest, plant (một lần). Mỗi hàng lặp có ít nhất một khung chớp mắt. Chiều cao: sprout 45–75, grow 85–112, ripe 120–150 (<=148 để chừa lề), rộng <=140. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Cây không có mặt-người kinh dị; mắt/mũi/miệng nhỏ, đọc được ở 48 px. Hái = vẫy tay chào rồi hóa ánh sáng (không đau). Plant f4 phải khớp sprout f1 (IoU>=0.80).

NHÂN VẬT (theo bảng 15):
1. cr-son-duoc Sơn Dược: dây lá tim bám cọc, củ kem. Tính cách: rắn con hiền, thân dây cuộn, củ kem là bụng tròn, lười biếng. Ripe: ngẩng đầu ngáp, đuôi dây quẫy nhẹ.
2. cr-cuc-hoa Cúc Hoa: cúc vàng nhiều lớp cánh. Tính cách: cô bé cúc, cánh làm tóc xoăn, má hồng, hay cười. Ripe: lắc đầu cười, cánh đung đưa.
3. cr-dia-hoang Địa Hoàng: hoa thị lá nhăn, chuông hồng tím, củ phình. Tính cách: chuột chũi củ, mũi hồng, mắt nhỏ tròn, cần cù. Ripe: đánh hơi, chuông hoa rung.
4. cr-huong-co Hương Cô: chùm nấm mũ nâu đốm trắng. Tính cách: người nấm hương, mũ như mũ đầu bếp, hiền, hay nấu nướng giả. Ripe: khuấy nồi tưởng tượng.
Mỗi cây KHÁC rõ về hình khối và màu so với Bạc Hà/Mộc Nhĩ và so với nhau (silhouette đọc được khi thu nhỏ).

LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi 4/4 atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo, face notes (mắt, miệng, khung chớp). Mỗi cây tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi cây: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png gồm cả pilot. Báo cuối: bảng 4 atlas x cổng a–j (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
