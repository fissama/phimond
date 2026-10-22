# Review v1.0.0 vòng 2 — người chơi khó tính chơi lại sau khi sửa

Ngày 2026-10-22. Chơi lại từ tài khoản mới (ngang 1280×720 và dọc 430×932, chất lượng Trung bình và Thấp), đi trọn
Triệu Linh Điện → chọn bệ → Bìa Rừng → nhận nhiệm vụ → trận 3 quái bằng Tự động → Rừng Sâu → Hoàng Môn → Quảng Trường.
Không có lỗi console. Ảnh: `review-v1.0.0-vong2/`. Vòng 1: `REVIEW-v1.0.0-TOAN-DIEN.md`.

## Chấm lại

| Hạng mục | Vòng 1 | Vòng 2 | Còn thiếu gì để lên 9 |
|---|---|---|---|
| Đồ họa thế giới | 6.5 | 7.5 | Đường đất/thảm đỏ vẫn mép chữ nhật (cần art), Rừng Sâu chưa có bản sắc riêng |
| HUD / UI | 5 | 8 | Nút có khung 9-slice khá to; chân dung NPC vẫn là sprite (cần art) |
| Combat | 3 | 8 | Nền trận vẫn là thế giới làm mờ (ảnh nền GPT đang chờ), hiệu ứng theo hệ là CSS tạm |
| Dẫn dắt người mới | 4 | 8 | Ổn: mục tiêu luôn nói gặp ai, ở đâu |
| Nội dung | 2.5 | 6.5 | 10 nhiệm vụ, thoại xoay; vẫn ít so với một game thật, 4 điểm "chưa mở" còn đó |
| Cảm giác game thật | 4 | 7 | Đã có âm thanh tổng hợp; chưa có nhạc nền và âm thanh vẽ riêng |

**Kết luận của người chơi khó tính:** v1.0.0 giờ là một vòng chơi trọn vẹn và công bằng: chọn pet có thông tin, trận đầu
thắng được, có lý do đi tiếp, không mất dấu nhân vật, không UI nào bị cắt. Mình hài lòng để làm nền cho các bản sau. Những gì
còn lại đều cần **art/âm thanh vẽ riêng** hoặc **tính năng phase sau**, không còn lỗi chặn trải nghiệm.

## Đã sửa so với vòng 1

**P0 (chặn chơi)**
- Cân bằng: quái hoang ×0.85, đàn 2 con ×0.55, đàn 3 con ×0.4 (HP và sát thương), `damage_scale` 0.6 → 1.0. Pet khởi đầu biết sẵn đòn hệ; Tự động dùng đòn mạnh nhất còn đủ MP.
  Mô phỏng 200–300 trận/ô, pet Lv1 chỉ bấm Tự động: Bìa Rừng thắng 92–100% (1–3 quái, 3.4–6.3 lượt); Rừng Sâu Lv1 48–74%, Lv5 ≥96%. Có test khóa mục tiêu (`balance_test.go`).
- Chạy trốn đi trước mọi đòn (không mất máu). Thẻ pet nháy đỏ dưới 30% HP, chat nhắc nơi hồi phục.
- Thua: bảng giữ tới khi chạm, kèm gợi ý. Thắng: tự đóng sau 2.4 s.

**Combat**
- Đặt theo điểm chân: bóng nằm đúng chân (dùng `footPad` của atlas), không còn "bay trên trời".
- Đội hình chéo kiểu Octopath: quái so le lùi về phía sau trái, gần camera thì to hơn và đè lên con phía sau; khung tên không đè thân con khác. Dọc: quái hàng trên, pet hàng dưới.
- Khung tên "Hoa Loa A · Lv 2" (server gửi `level`), không gãy dòng. Nút Kỹ năng ẩn khi không có.
- Hiệu ứng đòn (vệt chém/quả cầu phép), tốc độ ×1/×2 nhớ theo máy, log trận cùng khung xanh nhạt với chat, thẻ HUD thế giới không còn lộ bóng mờ sau trận.

**UI**
- Một bộ khung cho mọi bảng; mỗi bảng chỉ còn X và "Trở về menu".
- Cài đặt gọn (nhãn trái, lựa chọn phải), có Âm thanh, không bị cắt.
- Chi tiết linh thú (chỉ số, hệ, tộc, kỹ năng, kháng); Túi đồ có mô tả và nút Dùng ngoài trận; thẻ chọn starter có hệ, tộc, đòn biết sẵn, 4 thanh chỉ số.
- Nhãn nút ngữ cảnh xuống dòng trong hình bầu dục; chat hiện ở màn dọc; minimap sáng, có chấm quái đỏ; tên NPC rõ khi lại gần, mờ khi xa, tránh vùng HUD.

**Thế giới**
- Cây/nhà phía trước mờ đi khi che nhân vật (trước đây nhân vật mất hẳn sau tán cây), kèm bóng xuyên vật cản.
- Vòng đỏ nhấp nháy dưới quái hoang để phân biệt với đồ trang trí.
- Sảnh có tiền sảnh ngoài lan can, hết khoảng đen.

**Nội dung**
- Chuỗi 10 nhiệm vụ Đợt A có `requires`/`giver`: Đòn đầu tiên → Bắt bạn đầu tiên → Gặp Rowan → Thắng 3 trận → Vào Rừng Sâu → Hỏi Cụ Rêu → Săn sói → Tới Hoàng Môn → Báo cáo Tessa → (Điền Trang, bản sau).
- 19 NPC có 1–3 câu thoại thêm, xoay theo tiến độ và số lần ghé.
- Âm thanh tổng hợp WebAudio: đánh, phép, trượt, thắng/thua, lên cấp, tiền, bấm nút, mở bảng.

## Còn lại (không chặn v1.0.0, đã ghi nợ)

- **Cần art** (`GPT-REMAINING.md` mục 5, 8, 9, 10, 14–16): nền trận 5 map, chân dung bán thân NPC, đường đất cong và thảm/gạch thành phố, hiệu ứng kỹ năng theo hệ.
- **Cần âm thanh thật**: nhạc nền theo map và bộ hiệu ứng thay bản tổng hợp (D16).
- **Phase sau**: Hội bang, Sàn giao dịch, Kho, Hòm thư, Đấu trường vẫn là biển báo (D1); chọn mục tiêu cho đồng đội/AoE cho 3v3 (D15).

## Quyết định mình tự chọn, cần bạn xác nhận
1. Hệ số cân bằng (`wild_scale` 0.85, `pack_scale` [1, 0.55, 0.4], `damage_scale` 1.0). `damage_scale` cũng làm trận Đấu trường nhanh hơn.
2. Pet khởi đầu biết sẵn đòn hệ (lệch `learn_level` 2 của dữ liệu).
3. Chạy trốn luôn thành công và đi trước (game gốc có thể có tỉ lệ thất bại).
4. Một bộ khung UI duy nhất (khung hội thoại xanh viền vàng) thay 5 khung GPT đã vẽ cho từng bảng.
5. Cây phía trước tự mờ khi che nhân vật (Octopath không làm vậy, nhưng camera của mình thấp hơn nên cần).
6. Thanh dưới (D-pad, chat, nút) giữ nguyên ảnh nền GPT theo kiểu game gốc, không làm trong suốt.
