# GPT redo — BATCH 10 (login, intro, loading, branding) — dán sau Master v2

Bản Gemini (`apps/game-web/art-src/hd2d/batch-10-octopath`, 16 asset) bị trả vì: sơn dầu/nhiều màu, không cùng ngôn ngữ pixel với batch 00–09; chữ nướng sẵn trong ảnh nền; logo/app-icon không khớp anh khuyển thú; viền khung UI không khớp batch UI GPT (batch 06–09). Vẽ lại toàn bộ 16 asset. Thư mục đích: `apps/game-web/art-src/hd2d/batch-10-octopath/` (di chuyển bản cũ sang `batch-10-octopath/_gemini-rejected/`, không xóa).

```text
[Dán Master v2 trước.] ĐỢT: Batch 10 — 16 asset.

THAM CHIẾU RIÊNG ĐỢT NÀY
 a. Nội dung gốc: ảnh login/loading/intro gốc nếu có trong tools/build-web-assets/source (tìm `login`, `loading`, `logo`); nếu không có, dùng tên bản đồ Việt và mô tả dưới đây.
 b. Style: contact-sheet.png của batch-01 (rừng), batch-02/03 (thành, nội thất), batch-06 và batch-07/08/09 (UI/icon/FX) — chọn 2–3 ảnh sát loại nhất với từng asset.
 c. Anchor linh thú (hai sprites.png).

QUY TẮC RIÊNG
- Bảng màu: dùng palette `phimond-octopath-forest`, `phimond-octopath-town` (batch-02) và thêm tối đa 1 palette trời bình minh. Màn hình lớn (1280×720): pixel art 64–96 màu, vẫn nhị phân alpha khi có alpha, không gradient mượt (trời dùng dải cụm pixel bậc thang), không sơn dầu, không nhiễu hạt.
- Mỗi tầng parallax là PNG RGBA riêng; mỗi tầng có đáy/đỉnh khớp tầng kế (rìa chồng 24 px). Không chữ, không sương, không ánh sáng nướng trong tầng.
- CHỈ `logo-horizontal`, `logo-badge`, `app-icon` được chứa chữ/huy hiệu. Chữ "PHIMOND" vẽ bằng pixel font tự vẽ (không dùng font hệ thống), chữ nằm trong khung ≥ 24 px lề.
- Khung UI (9-slice): tuân theo style khung batch 06–07 (đồng cổ, góc nhấn ngọc lục bảo). Vẽ bản 3×: góc 48×48, cạnh lặp được; nghiệm thu bằng ảnh ghép 9-slice ở 3 kích cỡ.
- Intro: 3 màn tách rõ nhân vật (tamer, linh thú) theo anchor linh thú; không vẽ gương mặt người cận (giữ bóng/ba phần tư lưng). Không ghi chữ phụ đề.

DANH SÁCH (id giữ nguyên để manifest/runtime không đổi)
 Branding: logo-horizontal, logo-badge, app-icon (1024 master + xuất 256), map-card-frame (9-slice)
 Login: login-layer-1-sky, login-layer-2-citadel, login-layer-3-forest, login-layer-4-foreground, login-panorama (= ghép 4 tầng, chỉ để xem; tự ghép từ tầng đã duyệt, không vẽ riêng)
 Intro (1280×720): intro-01-world, intro-02-companion, intro-03-journey
 Loading: loading-bar-frame (9-slice), loading-bar-fill (tile ngang lặp), loading-ornament-corners (4 góc + spinner 8 khung), loading-bg

THỨ TỰ VÀ NỘP THEO CHẶNG (dừng và đợi Claude sau mỗi chặng)
 Chặng A: 3 tầng login (sky/citadel/forest) + foreground → 1 contact sheet → chờ.
 Chặng B: branding + map-card-frame.
 Chặng C: loading (4 asset).
 Chặng D: intro (3 màn).
Mỗi chặng chạy `sh tools/check_hd2d_art.sh` (batch-10 được thêm vào cổng qua `HD2D_ART_GATE_KITS` hoặc `--all`) và nộp như Master v2 mục 5.
```

Ghi chú cho Claude/owner: cổng art hiện chỉ quét `batch-11-*`; trước khi giao, chạy `python3 tools/hd2d_audit/art_gate.py --all` hoặc sửa mặc định để gồm batch-10 (việc của Claude, không giao cho GPT).
