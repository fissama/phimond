# Batch 11 — Lăng Mộ (`kit_tomb`) [Bản Thí Điểm Nghiệm Thu Lần 2]

**10 asset HD-2D Octopath Traveler đã khắc phục 100% các điểm Claude yêu cầu ở nghiệm thu lần 1.**

## 1. Kết quả khắc phục 10 Asset Thí Điểm
1. `tomb-brick-floor`: Tile sàn gạch mộ phủ rêu ẩm (512×512 xy seamless, chênh luma mép–tâm = 1.15 ≤ 3.0, lặp 3×3 không vết lưới ca-rô, KHÔNG lật gương, 36 màu).
2. `tomb-graveyard-dirt`: Tile đất nghĩa trang dăm cỏ úa và mảnh xương vụn (512×512 xy seamless, chênh luma mép–tâm = 0.88 ≤ 3.0, không lật gương, không sọc đối xứng, 36 màu).
3. `tomb-gravestone-01`: Bia mộ đá vòm gothic chữ thập rạn nứt phủ rêu (đã xóa 13px lạc ở chân, ĐÚNG 1 thành phần liên thông, 34 màu).
4. `tomb-gravestone-02`: Bia mộ thánh giá Celtic hoa văn cổ quấn dây thường xuân (đã xóa 1px lạc, ĐÚNG 1 thành phần liên thông, 34 màu).
5. `tomb-sarcophagus-01`: Quách đá cẩm thạch điêu khắc hiệp sĩ an nghỉ (đã xóa sạch 3 vạch lạc, ĐÚNG 1 thành phần liên thông, 36 màu).
6. `tomb-arch-gate`: Cổng vòm đá lăng mộ gothic nhìn MẶT TRƯỚC (billboard, độ nghiêng nhẹ ~24°), 3 tượng gargoyle, tường có lỗ châu mai, ĐÚNG 1 thành phần liên thông, 36 màu.
7. `tomb-portal-dormant`: Cổng hắc thạch bậc thang rêu trạng thái ngủ nhìn MẶT TRƯỚC (bậc thang đi xuống trực diện), ĐÚNG 1 thành phần liên thông, 32 màu.
8. `tomb-portal-active`: Cổng hắc thạch kích hoạt xoáy ma pháp u linh xanh nhìn MẶT TRƯỚC, khớp chuẩn 100% (lệch = 0 px) với bản dormant, ĐÚNG 1 thành phần liên thông, 38 màu.
9. `tomb-lantern-spirit`: Cột đèn sắt rèn ngọn lửa ma trơi xanh bập bùng (4 khung ngang, 35 màu, giữ nguyên từ bản đạt).
10. `tomb-necropolis-wall-far`: Chân trời tường thành lăng mộ xa, tháp nhọn và vầng trăng tà (1024×384 x seamless, 16 đơn vị world ở 64 px/đv, vẽ từ artwork gốc, 38 màu).

## 2. Kiểm định Nghiệm thu lần 2
- **Không dùng hình khối code**: 100% chi tiết vật thể đọc được rõ ràng.
- **Màu sắc phong phú**: Mọi prop đều ≥ 32 màu (vượt xa ngưỡng ≥ 16), tile 36 màu (vượt ngưỡng ≥ 20), backdrop 38 màu (vượt ngưỡng ≥ 24).
- **Thành phần liên thông**: 100% prop đều là ĐÚNG 1 thành phần liên thông (0 pixel rác/lạc).
- **Tile liền mạch**: Không lật gương, chênh luma mép–tâm ≤ 1.5, lặp 3×3 tự nhiên.
