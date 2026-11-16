# Đơn 13e — garden-a: gd-trunk-seg-02 (ĐÃ ĐÓNG — lựa chọn 1)

Owner đã chọn dùng `gd-trunk-seg-01` làm biến thể thân duy nhất. Không chạy prompt chỉnh sửa có mặt nạ; asset 02 đã retired khỏi manifest và được giữ lại trên disk chỉ để audit. Tool image_gen hiện không có tham số mask/inpaint. Nội dung prompt bên dưới là lịch sử, không còn là yêu cầu đang hoạt động.

- Ngày: 2026-11-09. Dán master v2 + file này. Raw mới `raw-05.png`; giữ raw/final cũ.
- Hai lần vẽ độc lập không đạt dải biên. trunk-01 đã đạt (hash chặt) nên dùng chính nó làm nền biên.

```text
Vẽ lại gd-trunk-seg-02 (384×512) bằng CHỈNH SỬA ẢNH có mặt nạ (image edit/inpaint) từ gd-trunk-seg-01 final.png, KHÔNG sinh mới từ đầu:
1. Mặt nạ bảo vệ: 16 hàng trên (0–15) và 16 hàng dưới (496–511) của trunk-01 giữ nguyên, không được vẽ lại (dải đai rễ phẳng màu 79,21,19 + 8 hàng tiếp). Chỉ vùng giữa (hàng 16–495) được vẽ lại.
2. Vùng giữa vẽ ruột kiểu rễ bện xoắn với ≥ 2 hốc cây ở cao độ khác nhau, đúng như bản trunk-02 hiện hành (tham chiếu đính kèm gd-trunk-seg-02 final.png hiện hành làm hình mẫu ruột). Khác trunk-01 rõ (tương quan < 0.7), không lật/đổi màu.
3. Silhouette: mép phải giữa hai dải nằm trong x 296–335 (như trunk-01); chỗ chạm dải liền với silhouette sẵn có. Mép trái tràn x = 0.
4. Họ màu nâu đỏ như trunk-join; 40–48 màu; alpha nhị phân; chi tiết cách dải ≥ 8 px.
5. Sau finish phải đạt: hash hàng 0 = hàng 511; 8/8 cặp hàng (r, 504+r) bằng nhau từng pixel; mọi pixel alpha=0 có RGB=0. Báo hash, số pixel khác (phải 0), x-range hai dải, preview ghép 3 bản và ghép xen 01-02-01 (không bậc > 8 px ở mép phải tại chỗ nối). Nếu chưa đạt: vẽ lại, không vá bằng code.
Nếu image_gen không hỗ trợ chỉnh sửa có mặt nạ: báo cáo, KHÔNG chuyển sang phương án khác.
```
