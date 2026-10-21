# Review: tomb-graveyard-dirt (Lần 3)
- Đối tượng: Đất nghĩa địa cổ ẩm rải rác mảnh xương tàn và dăm cỏ úa (512×512 px).
- Tái thiết kế: Bỏ hoàn toàn dither ô cờ 1×1 (triệt tiêu hiện tượng nhiễu moiré); chuyển sang các cụm màu đất mềm 3–4 tông tự nhiên, phân bổ dăm cỏ và mảnh xương ngẫu nhiên không theo hàng lối.
- Làm liền mạch: Circular wrap-around synthesis (không lật gương).
- Kiểm tra mắt: Đã xem repeat-3x3.png, không thấy lưới/gương/lặp rõ.
- Đo lường: 32 màu (≥20), chênh độ sáng mép–tâm = 0.41 (≤3.0), seam X=0 (≤3), seam Y=0 (≤3), failures=[].
