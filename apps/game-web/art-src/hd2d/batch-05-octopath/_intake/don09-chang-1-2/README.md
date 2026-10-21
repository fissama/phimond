# Đơn 09 — Chặng 1 + 2 (owner nộp 2026-10-22)

Ảnh owner gửi trong chat, lưu nguyên pixel (đã đối chiếu từng pixel với bản gửi; metadata PNG có thể khác do khâu chép file). `SHA256SUMS` là hash của file trong thư mục này. **Chưa review**: owner yêu cầu đợi đủ các chặng rồi nhận xét một lần. Chưa cắt khung, chưa đưa vào manifest, chưa đổi `approved`.

| File | Nội dung (theo thứ tự owner gửi) |
|---|---|
| `male-down.png`, `male-up.png`, `male-right.png` | Chặng 1 — turnaround nam, 1254×1254, nền trong suốt |
| `female-down.png`, `female-up.png`, `female-right.png` | Chặng 1 — turnaround nữ, 1254×1254, nền trong suốt |
| `contact-sheet-turnaround.png` | Chặng 1 — contact sheet LOCK + 6 hướng |
| `male-idle-sheet-a.png`, `male-idle-sheet-b.png` | Chặng 2 — sheet idle nam, 3 hàng (xuống/lên/ngang) × 6 khung, nền #FF00FF, 1774×887 |
| `male-walk-sheet-a.png`, `male-walk-sheet-b.png` | Chặng 2 — sheet đi nam, cùng bố cục |
| `female-idle-sheet-a.png`, `female-idle-sheet-b.png` | Chặng 2 — sheet idle nữ |
| `female-walk-sheet-a.png`, `female-walk-sheet-b.png` | Chặng 2 — sheet đi nữ |

Hậu tố `a`/`b`: hai bản owner gửi cho cùng một animation (đặt tên theo thứ tự gửi, không ngụ ý bản nào được chọn).

Bước sau (khi owner nộp đủ chặng và yêu cầu review): cắt khung về ô 192×192 pivot (96, 184), đo màu/alpha/pivot, xem 4×, rồi ghi kết quả vào `player-{male,female}-anim/`.
