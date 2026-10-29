# Chơi thử v1.0.0 như người chơi khó tính — còn thiếu gì để ra chất Octopath (2026-10-29)

Cách chơi: chromium SwiftShader, mức Trung bình, ban ngày, 1280×720; Sảnh → chọn bệ → Bìa Rừng → trận 3 quái → Quảng Trường, Cổng Cung Điện, Rừng Sâu (chụp theo bản đồ), menu túi/linh thú/nhiệm vụ/cài đặt/NPC. Chưa chạy được: đường đi liền mạch rừng→thành bằng script `tour2` (trận không mở ở bước 1, lỗi script dev chưa điều tra; test smoke thật vẫn qua) và màn đăng nhập/chọn nhân vật (chưa xem lần này). Không nghe được âm thanh.

## Đã đạt sau bước 1–2 (render)
Tilt-shift, bloom, camera thấp, lớp nhân sáng/tối, quầng chân, rừng và thành phố đã có cảm giác mô hình thu nhỏ.

## Còn thiếu — cần asset (xếp theo mức ảnh hưởng tới chất Octopath)
**A. Nặng nhất**
1. Hoạt họa đi/chạy 4 hướng cho nhân vật và NPC (R01–R24, S23–S24 trong CHECKLIST-REDRAW-CODEX): người chơi đứng/đi chưa có nhịp bước đúng kiểu Octopath; NPC phần lớn đứng im (idle chưa cài).
2. Sân khấu trận đấu riêng theo địa hình: hiện nền là ảnh thế giới làm mờ, phẳng. Cần nền trận (rừng, thành, sảnh, rừng sâu) + bệ/đất dưới chân hai phe (thư mục `battle-bg` đã có thiết kế).
3. Hiệu ứng kỹ năng/va chạm theo hệ (lửa, nước, đất, gió, quang, ám, vật lý), tia trúng đòn, hiệu ứng bắt thú, hiệu ứng thua/biến mất: trận hiện chỉ lướt tới và nhấp nháy.
4. Khung giao diện kiểu Octopath: bảng (9-slice), nút, tab, ô chọn, thanh trượt, khung chân dung linh thú, khung thoại; hiện các menu là bảng xanh phẳng kiểu web, khung chat xanh nhạt lệch tông HUD, Cài đặt như form.
5. Lớp tiền cảnh mờ phủ mép màn (cành lá, dây cờ, tán cây, rèm): dấu hiệu nhận ra Octopath nhất mà cảnh còn thiếu; làm bằng sprite lớn + bộ mờ có sẵn.

**B. Nên có**
6. Sinh vật nền cho rừng (bướm, đom đóm, chim, lá rơi) như thành phố đã có bồ câu; cỏ/hoa đung đưa thêm lớp.
7. Hiệu ứng bước chân (bụi, cỏ, nước), vết dấu, gợn nước ở chỗ có nước.
8. Biển tên khu vực khi vào map (khung trang trí) và chuyển cảnh vào trận (xoáy/quét).
9. Mảnh nối còn trống của Sảnh: góc trước/sau và cảnh bên ngoài tường (đã báo ở review viền hai bên).
10. Phông chữ: sans hiện tại lệch hẳn; cần phông serif/pixel có giấy phép (không phải GPT vẽ).
11. Biểu tượng menu chính và biểu tượng vật phẩm to rõ hơn (túi đồ đang dùng icon nhỏ, nhãn chữ).
12. Hoạt họa chờ cho thú cưng trên bệ và bóng đổ dài (bóng đổ là code, không cần vẽ).

**C. Chưa kiểm được / cần bạn quyết**
- Âm thanh: nhạc nền từng khu, nhạc trận, SFX; Octopath dựa rất nhiều vào nhạc. Chưa biết trong repo đã có bao nhiêu.
- Màn đăng nhập/chọn nhân vật, thời tiết, đêm: chưa xem lại ở bước này.
