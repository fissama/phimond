# Đơn 13c — garden-a: vẽ lại 5 asset chưa duyệt

- Ngày: 2026-11-09. Dán master v2 (`00-master-v2.md`) + file này. Một phiên làm cả 5 asset.
- Chỉ vẽ lại 5 asset dưới đây. 25 asset còn lại đã duyệt, KHÔNG đụng. Giữ raw/final cũ trong thư mục asset, raw mới là `raw-0N.png`.
- Thư mục: `art/src/hd2d/garden-a/<asset_id>/`. Cập nhật manifest.json và contact-sheet.png; giữ `approved:false`, `status:needs_claude_review`.
- Mọi ảnh tham chiếu ĐÍNH KÈM TRỰC TIẾP vào image_gen (không zip), ghi sha256 vào prompt.md.

```text
Bạn là art worker của Phimond. Bối cảnh: Căn Mạch Linh Viên, khu vườn dưới lòng đất, HD-2D Octopath, pixel art. Luật chung: master v2 (33–48 màu, alpha nhị phân, viền cùng sắc vật thể, không bóng/glow/sương/chữ vẽ sẵn, lề alpha ≥ 8 px trừ trục tile). Vẽ bằng built-in image_gen; code chỉ để cắt, khử nền #FF00FF, đưa về bảng màu, kiểm. CẤM dùng code chép/blend/vá hàng biên, lật gương, đổi màu để thành asset mới.

Ảnh tham chiếu đính kèm (thứ tự cố định):
 a. garden-a/gd-trunk-join-01, -02, -03 final.png (đã duyệt) → họ màu nâu đỏ của thân cây.
 b. garden-a/gd-ledge-cap-l final.png, gd-pillar-01 final.png → độ dày outline, đổ khối.
 c. batch-01-octopath/exposed-roots/final.png, deep-woods-giant-tree/final.png → style gốc.
 d. Với JOB 2: garden-a/gd-seal-strip/final.png và gd-seal-strip-lit/final.png HIỆN HÀNH → thiết kế cần GIỮ.
 e. Với JOB 3: garden-a/gd-pillar-01 final.png, gd-pillar-vein-02 final.png.
 f. Anchor linh thú DocDangNu/sprites.png, DaoThienDuong/sprites.png (chỉ độ dày outline).

=== JOB 1 — gd-trunk-seg-01 và gd-trunk-seg-02 (384×512, ghép dọc) ===
Lý do vẽ lại: ba lần cố ép vân gỗ liền mạch bằng cách sinh ảnh đều không ra hàng biên pixel-identical. Đổi cách đạt seam theo quy tắc tile của Master ("mép ngoài 8 px là dải phẳng cùng màu hai phía đối nhau"):

1. VÒNG ĐAI RỄ: 8 hàng trên cùng (0–7) và 8 hàng dưới cùng (504–511) là một dải PHẲNG, một màu duy nhất (nâu đỏ sẫm nhất của bảng màu, cùng sắc outline), phủ đúng silhouette của thân tại hàng đó. Sau finish, hàng 0 và hàng 511 phải bằng nhau từng pixel RGBA (cả màu lẫn alpha). Nhìn như vòng rễ xiết quanh thân cây, một vòng mỗi 512 px.
2. Silhouette hàng 0 và hàng 511 phải cùng đoạn x: tràn ra mép trái (x = 0) và dừng ở x = 312 ở cả hai hàng. Giữa hai dải, mép phải được lượn trong x 272–336, KHÔNG loe thành tam giác như bản cũ.
3. Chi tiết vân/rễ cách dải phẳng ≥ 8 px (hàng 16–495). Không có rêu hay hốc chạm dải.
4. Hai biến thể phải cùng silhouette tại hai dải để dùng thay nhau được, nhưng ruột khác hẳn nhau:
   - 01: rễ dọc song song chảy xuống, vài mảng rêu olive nhỏ.
   - 02: rễ xoắn bện, ≥ 2 hốc cây ở cao độ KHÁC nhau và không lặp theo chu kỳ trong đoạn; không hốc nào chạm dải.
5. Màu: họ nâu đỏ như trunk-join-01..03 (không nâu vàng nhạt như bản cũ), 2–4 tông mỗi vật liệu, 40–48 màu.
6. Tự kiểm: ghép 3 bản dọc, xem 4× trên nền caro và nền tối; báo hash hàng 0 và hàng 511, số pixel khác nhau (phải = 0), alpha equal. Nếu hàng không bằng nhau: vẽ lại, KHÔNG vá bằng code.

=== JOB 2 — gd-seal-strip và gd-seal-strip-lit (512×160, tile ngang) ===
GIỮ NGUYÊN thiết kế đã được duyệt về hình (đá ochre khắc rune, viền gạch trên, không dây leo). Chỉ sửa lề:
1. Vùng đặc nằm trong hàng 12–147 (cao 136 px); tối thiểu 12 px trong suốt ở trên và 12 px ở dưới. Không còn hàng đặc chạm mép dưới.
2. Cột x = 0 và x = 511 có alpha profile giống hệt nhau; nối ngang liền mạch (xem ghép 3 bản).
3. lit và unlit CÙNG mask. Ngoài các pixel rune, pixel lit == unlit từng pixel (chỉ rune đổi sang ngà sáng). Báo số pixel khác nhau và đảm bảo chúng nằm trong rune.
4. 40–48 màu mỗi bản.

=== JOB 3 — gd-pillar-vein-01 (160×340, overlay) ===
Overlay mạch sáng cho gd-pillar-01 (đã duyệt). Cùng kiểu với gd-pillar-vein-02: mạch phân nhánh màu ngà, mảnh, bám theo đường xoắn rễ của pillar-01.
1. ≥ 33 màu (nhiều sắc ngà từ nhạt đến vàng nhạt), alpha nhị phân, không halo, không blur.
2. 0 pixel nằm ngoài mask của gd-pillar-01. Phủ 5–8% diện tích pillar.
3. Lề alpha ≥ 8 px.
4. Không giống vein-02 (tương quan < 0.5).

Nộp: danh sách file; số liệu đo cho từng asset (kích thước, màu, alpha, hash hàng đầu/cuối của trunk, lề, pixel ngoài mask); contact-sheet mới; 3 asset yếu nhất tự đánh giá. Không commit, không đụng runtime.
```
