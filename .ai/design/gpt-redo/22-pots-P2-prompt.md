# Prompt P2 — 4 chậu (G4 x2, G5 x2)
Copy khối dưới gửi Codex sau khi P1 được duyệt.

```
NHIỆM VỤ: Vẽ và đóng gói 4 atlas chậu hạng cao của khu vườn ngầm (garden-b): pot-g4a-lam-su, pot-g4b-linh-thach, pot-g5a-dong-co, pot-g5b-tinh-mach. KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng chậu; chỉ báo xong khi cả 4 atlas qua đủ cổng của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 14-garden-pots-anim-prompt.md, pilot garden-b/pot-g1-tho-dao, và các chậu P1 đã duyệt trong garden-b/.

CHUNG: Giống P1 (21-pots-P1-prompt.md): pipeline image_gen -> pack_atlas.py -> measure_atlas.py; atlas 768x960 RGBA, 4x5 ô 192, đáy y=175, tâm x=96, miệng quanh y≈112; hàng idle (lặp), wet (lặp, đất sẫm hơn >=15% + bóng nước), water, upgrade, clear (một lần); thân chậu đứng yên IoU liền kề >=0.95, khung nối >=0.93; chậu không mặt; <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked; bề ngang <=158 px, cao thân <=100 px; đổi hẳn chất liệu, màu không bão hòa quá mức. Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Hạng cao hơn thì tinh xảo hơn nhưng không rối (palette gọn).

CÁC CHẬU:
1. pot-g4a-lam-su — Lam Sứ Bồn (hạng G4): chậu sứ men lam trắng kiểu Bát Tràng, họa tiết hoa văn sóng và sen nhỏ, miệng loe viền vàng nhạt. water: men lam sáng hơn, nước đọng; upgrade: hoa văn nổi thêm một lớp; clear: viền vàng lóe.
2. pot-g4b-linh-thach — Linh Thạch Bồn (hạng G4): khối đá xám xanh khoét rỗng, vài mảnh tinh thể xanh ngọc mọc ở viền. water: mảnh tinh thể sáng hơn (đổi màu, không glow baked); upgrade: thêm tinh thể; clear: tinh thể rung.
3. pot-g5a-dong-co — Đồng Cổ Bồn (hạng G5): chậu đồng xanh rỉ kiểu trống đồng Đông Sơn, mặt hoa văn ngôi sao nhiều cạnh, chim lạc và vòng tròn đồng tâm quanh thân, quai nhỏ hai bên. water: gỉ đồng sẫm lại, nước lăn; upgrade: hoa văn nổi sắc hơn; clear: tiếng ngân (vòng rung nhỏ).
4. pot-g5b-tinh-mach — Tinh Mạch Bồn (hạng G5): thân đá tím sẫm, mạch tinh thể vàng chạy ngoằn ngoèo, miệng gắn tinh thể lớn. water: mạch vàng chạy sáng (đổi màu, không glow baked); upgrade: mạch dày thêm; clear: tinh thể nứt rồi lành.

LẶP TỰ SỬA, GIAO: như P1 (pack -> measure -> vẽ lại khung fail; mỗi chậu tối đa 8 lượt ImageGen; final.png, anim.json, prompt.md, review.md, qa.json, preview, ảnh 4x; cập nhật manifest approved:false, contact-sheet). Báo cuối: bảng atlas x cổng, file đã tạo/sửa, điểm sát ngưỡng.
```
