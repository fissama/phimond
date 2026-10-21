# Prompt mở kit Hoang Mạc + Núi Phong Thạch (batch-11) — 2026-10-16

Kit Lăng Mộ và map Rừng đã nghiệm thu. Prompt dưới đây dán vào đầu mỗi phiên kit tiếp theo, kèm Phần A và khối kit tương ứng (Phần C) của `.ai/design/hd2d-maps-75-gemini-prompt.md`.

```text
Mở kit HOANG MẠC (6 map) và kit NÚI PHONG THẠCH (6 map). Làm lần lượt từng kit, nộp mỗi kit một lần, chờ Claude nghiệm thu rồi mới làm kit sau. Tuân thủ Phần A của prompt 75 map, cộng thêm 3 điều bắt buộc rút ra từ Lăng Mộ và Rừng:

1. ĐO SEAM BẰNG CHÊNH LỆCH TỐI ĐA, KHÔNG DÙNG TRUNG BÌNH.
   - Tile và backdrop lặp: chênh pixel lớn nhất giữa cột/hàng mép trái-phải (và trên-dưới với tile xy) ≤ 3 trên mỗi kênh. Ghi seam_x_max, seam_y_max vào qa.json.
   - Độ sáng trung bình viền 10 px so với vùng giữa chênh ≤ 3. Không lật gương, không dither ô cờ, không khối lớn nổi bật lặp thấy rõ khi ghép 3×3 (đính kèm repeat-3x3.png thật và đã xem).

2. MÉP TRÊN KHÔNG ĐƯỢC CẮT PHẲNG.
   - Tán lá, bụi, vách đá, cồn cát, dãy núi, tường nền: mép trên phải có lề alpha ≥ 8 px phía trên và đường viền lồi lõm hữu cơ.
   - Cấm bước nhảy alpha đột ngột theo hàng ngang (một hàng chuyển từ 0% lên > 50% bề ngang ảnh). Tự đo: bước nhảy lớn nhất giữa hai hàng liên tiếp ≤ 10% bề ngang. Ghi vào qa.json.
   - Các lớp nền (far / mid / front) phải xếp chồng liền nhau, không để dải trống giữa chân lớp nền xa và mặt đất.

3. CỔNG VÀ CỔNG DỊCH CHUYỂN VẼ NHÌN MẶT TRƯỚC (FRONT-FACING).
   - Bậc thang đi xuống phía người xem, không chéo, không isometric 45°. Thấy hơi mặt trên (~24°), giống bia mộ và cổng vòm Lăng Mộ.
   - Cặp dormant/active: cùng kích thước khung, cùng pivot giữa-đáy, cùng mặt nạ alpha (độ lệch ≤ 1 px); chỉ khác lõi phát sáng và rune. Ghi hai số: khác biệt mặt nạ alpha, độ lệch vòm.

GIỮ NGUYÊN các quy tắc cũ: tự vẽ bằng công cụ tạo ảnh (không code vẽ nội dung), ≤ 48 màu, alpha nhị phân, lề ≥ 8 px, prop đúng 1 thành phần liên thông (ghi nếu có mảnh phụ có chủ đích), tách tán/thân với cây, không chữ, không bóng đổ nướng sẵn, backdrop xa 64 px/đv (1024 px = 16 đv), mỗi asset ≥ 16 màu (tile ≥ 20, backdrop ≥ 24), không hai id trùng hash hoặc trùng mặt nạ (trừ dormant/active).

Mỗi kit nộp: thư mục batch-11-<kit>/ với final.png từng mảnh, manifest.json, palette.json, contact-sheet.png, qa.json (có các số đo trên), review.md (đã xem từng ảnh, điểm yếu). Mỗi kit phải có: tile nền chính ×2, tile phụ, decal chuyển tiếp nền, 6–10 prop đặc trưng riêng theo kit (hình khác nhau), cổng dormant/active, marker 4 khung, 1 backdrop xa đúng chủ đề. Xem bảng mảnh tối thiểu trong khối kit.

Nhắc thêm theo kit:
- Hoang Mạc: cát vàng ấm, đá sa thạch đỏ cam, xương quái khổng lồ, xương rồng, lều du mục, phế tích cột/tường, cổng phong ấn. Cồn cát/đỉnh đụn cát có đường viền gợn, không cắt phẳng.
- Núi Phong Thạch: đá xám lam, cỏ núi khô, tuyết lốm đốm, cầu treo (đoạn lặp + cọc + đoạn đứt), cột đá gió bào, thông núi (tách tán/thân), trại và lửa trại 4 khung. Dãy núi nền xa có đỉnh gồ ghề, không cắt phẳng.
```
