# Còn nợ GPT vẽ (khi hết giới hạn)

Quy tắc chung: 1 ô = 128 px, người cao ~168 px trong khung 192×192, chân ở (96,184), nền ma-gen-ta #FF00FF, alpha nhị phân, ≤64 màu, nhìn chéo kiểu Octopath. Dùng công cụ tạo ảnh, không ghép/kéo méo bằng code. Gửi từng ảnh kèm prompt, không gửi zip.

1. **Đi hướng lên** (nam, nữ): 6 khung, như dải đã có. Hiện lên trên dùng dải bên.
2. **Đi hướng xuống (nữ)**: 6 khung. Lưu ý dải xuống nam có hàng 2 thấp hơn hàng 1 một chút; vẽ lại cho đều.
3. **Chờ 4 khung cho 7 NPC nộp tạm**: Mira, bia_skill, bia_free, trụ đá, kỹ năng, sàn giao dịch, kho.
4. **Bóng tiếp xúc** (tròn nhỏ/lớn, chữ nhật, dài theo tán), cùng hướng sáng.
5. **Thảm/gạch/bệ ở Hoàng Môn và Quảng Trường**: viền thảm có tua, bậc đá, mép gạch vỡ vào đá cuội, 2–3 biến thể đá cuội, bệ giếng tròn có bóng.
6. **Mảnh nối mặt tiền nhà** (ngõ, ống máng, cột).
7. **Khung UI**: bản đồ nhỏ, khung Mục tiêu, hộp chat cùng ngôn ngữ khung vàng với HUD; bảng Menu có vùng nội dung rộng hơn nút (đã sửa bằng CSS, vẽ lại cho đẹp hơn).
8. **Biến thể mảnh chuyển đường đất** để phá nhịp lặp (xem DEBT D10).

## Bổ sung đợt 3 (combat, HUD, chat)
9. **Nền trận đấu theo từng map** (5 ảnh 1920×1080: forest, deep_forest, gate, city, hall): prompt và ảnh mẫu đã soạn sẵn trong `battle-bg/PROMPTS.md`. Đặt vào `apps/client/public/battle/battle-bg-<key>.png`.
10. **Hiệu ứng kỹ năng** theo hệ (lửa, nước, cây, đất, thú, côn trùng): 6 khung/hiệu ứng, nền ma-gen-ta, kiểu pixel cùng độ phân giải pet.
11. **Khung thanh chỉ số có nhãn** (HP, MP, EXP) tách riêng nhãn khỏi thanh để không phải vẽ chữ đè lên khung.
12. **Khung chat màu xanh nhạt** như game gốc (hiện dùng `chat-panel` xanh đậm), kèm tab xếp sát nhau cùng ngôn ngữ khung vàng.
13. **Dải trang trí thanh dưới** (thanh đá có hoa văn ở giữa) để D-pad, chat, nút Chọn nằm trên một khung liền.
