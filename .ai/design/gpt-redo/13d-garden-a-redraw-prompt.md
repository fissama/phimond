# Đơn 13d — garden-a vòng 3: trunk-02, seal strip, vein-01

- Ngày: 2026-11-09. Dán master v2 + file này. Giữ raw/final cũ trong thư mục asset, raw mới `raw-04.png`. Ảnh tham chiếu đính kèm trực tiếp, ghi sha256.
- Trunk-01 KHÔNG vẽ lại (chờ owner quyết tiêu chí hash, xem REVIEW-CLAUDE-20261109.md). Không đụng 25 asset đã duyệt.

```text
Bạn là art worker của Phimond (HD-2D Octopath, pixel art). Luật chung: master v2. Vẽ bằng built-in image_gen; code chỉ cắt, khử nền, đưa về bảng màu, kiểm. Cấm vá hàng biên bằng code.

Tham chiếu đính kèm: garden-a/gd-trunk-seg-01 final.png (dải đai rễ chuẩn), gd-trunk-join-01..03 final.png, gd-pillar-01 final.png, gd-pillar-vein-02 final.png, gd-seal-strip final.png (thiết kế HIỆN HÀNH, chấp nhận), DocDangNu và DaoThienDuong sprites.png.

=== JOB 1 — gd-trunk-seg-02 (384×512) ===
Lỗi: hai dải đầu/cuối khác màu (103,24,17 so với 97,23,17) và không phẳng (3–5 màu); silhouette dải ngắn hơn trunk-01; thân hẹp hơn 01 làm ghép 01/02 bị bậc.
1. Dải 8 hàng trên (0–7) và 8 hàng dưới (504–511): PHẲNG, đúng MỘT màu RGB (79,21,19), giống hệt dải của gd-trunk-seg-01. Sau finish, 8 cặp hàng (r và 504+r) bằng nhau từng pixel.
2. Silhouette tại dải: x từ 0 đến 312 (giống trunk-01 chính xác, 313 pixel đặc mỗi hàng). Giữa hai dải, mép phải lượn trong x 296–335 (cùng khoảng với trunk-01), không thu hẹp về 267.
3. Ruột giữ như bản hiện tại (rễ bện, ≥ 2 hốc cây khác cao độ), cách dải ≥ 8 px (hàng 16–495). 40–48 màu, alpha nhị phân, họ nâu đỏ như trunk-join.
4. Tự kiểm: báo hash hàng 0 và 511, số pixel khác (phải = 0), x-range hai dải, ghép 3 bản và ghép xen 01-02-01 (không bậc quá 8 px ở mép phải tại chỗ nối).

=== JOB 2 — gd-seal-strip (512×160) + lớp rune sáng ===
Chấp nhận thiết kế hiện hành của gd-seal-strip (đá cam nâu, rune mê cung). Sửa:
1. Bỏ dải tối dọc ở hai mép (cột 0–2 và 509–511 đang sẫm hơn thân ~2 lần). Cột x = 0 và x = 511 phải tiếp nối họa tiết như phần giữa (không viền tile). Cột 0 và cột 511 có cùng alpha profile; ghép ngang 3 bản không thấy vạch nối ở zoom 3×.
2. Giữ lề: ≥ 12 px trong suốt trên và dưới (hiện 15/16, đạt).
3. THAY gd-seal-strip-lit bằng LỚP PHỦ RUNE: `gd-seal-rune-glow` 512×160 chỉ chứa pixel rune màu ngà/vàng nhạt (2–4 tông), nền trong suốt, KHÔNG vẽ đá. Từng pixel rune phải nằm đúng trên pixel rune của gd-seal-strip (vẽ theo hình rune đã có). Engine vẽ unlit rồi chồng lớp này để "sáng". Alpha nhị phân; 12–20 màu; cùng quy tắc nối ngang (cột 0 và 511 tiếp nối nhau). Báo: số pixel của lớp nằm ngoài vùng rune của unlit (phải = 0).
(Thư mục gd-seal-strip-lit cũ giữ lại, đánh dấu rejected.)

=== JOB 3 — gd-pillar-vein-01 (160×340) ===
Lỗi: phủ 12.43% (cần 5–8%), nét dày như tia sét, không bám đường xoắn rễ của pillar-01.
1. Mạch phân nhánh MẢNH (nét 1 px, chỗ hợp lưu tối đa 2 px) chạy dọc theo các đường rễ nổi của pillar-01, cùng kiểu và cỡ nét với gd-pillar-vein-02.
2. Phủ 5–8% diện tích mask pillar-01; ≥ 33 màu (nhiều sắc ngà đến vàng nhạt); alpha nhị phân; 0 px ngoài mask; lề ≥ 8 px; không halo.
3. Không giống vein-02 (tương quan mask < 0.5).

Nộp: số đo từng asset (hash hàng đầu/cuối, x-range dải, pixel khác, lề, pixel ngoài mask, coverage, màu), preview ghép 3 bản (trunk dọc, seal ngang) và ảnh phóng 4× nền caro + nền tối, contact-sheet mới, 3 asset yếu nhất. Không commit, không đụng runtime.
```
