# P12 Stage 3 — Golden Scene Emerald HD-2D (benchmark Godot Web vs Three.js)

Cùng một cảnh (rừng Emerald, dựng lại HD-2D từ sprite APK) chạy trên 2 engine, dùng chung `shared/scene.json` + `shared/tex/*.png`.

## Chạy
    python3 serve.py            # in ra URL Mac + iPhone (cổng 8765)
    Mac Safari : http://localhost:8765/three/   và   /godot/
    iPhone     : http://<IP-Mac>:8765/three/    và   /godot/   (cùng Wi-Fi)

Tham số URL: `tier=low|medium|high`, `dpr=1..3` (trần DPR), `auto=1` (tự chạy bench), `secs=60`, `warm=120` (khung bỏ qua), `map=...`.
Nút: "Trụ → Rừng sâu" (đo đổi map), "Chạy bench 60s", "Xuất JSON". Kết quả POST về `/__result` → lưu `results/`, đồng thời log `BENCH_RESULT`.
Mỗi cấu hình (engine × tier × thiết bị) nên chạy ≥3 lần, bỏ lần đầu (cache).

## Cấu trúc
- `shared/` scene.json + texture + `hud/` (sinh bởi `tools/extract.py`, `tools/gen_scene.py` từ APK)
- `three/` Three.js r170 (vendored)
- `godot-src/` project Godot 4.7.2 (GL Compatibility); `godot/` bản export Web nothreads (~39 MB wasm; không cần COOP/COEP)
- Xuất lại: `godot --headless --path godot-src --export-release "Web" ../godot/index.html` (cần export template 4.7.2 web_nothreads)

## Giới hạn đã biết
- Số liệu chạy trên cloud (SwiftShader, 2–5 fps) CHỈ để kiểm tra harness; số thật phải đo trên iPhone 17 Pro Max Safari + macOS Safari.
- Safari không công bố JS heap; dùng Web Inspector / Instruments khi cần bộ nhớ.
- Bloom của Godot (Environment glow, Compatibility) chưa xác nhận trên GPU thật; tilt-shift/grade qua shader ColorRect.
- Three: bóng blob còn lốm đốm, cờ `sway` theo tier chưa áp dụng. Asset là sprite APK bên thứ ba (chỉ dùng nội bộ để đo).

## HUD (đã sửa 2026-10-14)
Bản trước dùng HUD debug tự chế — sai. Nay HUD giữ nguyên bố cục game hiện tại (`apps/game-client/scripts/classic_hud.gd`, canvas tham chiếu 960×640, thế giới 71% trên / dải điều khiển 29% dưới) và dùng đúng sprite HUD trích từ APK (`shared/hud/*.png`, nguồn `apps/game-client/assets/reference/hud/`).
- `shared/hud/hud.js`: lớp DOM dùng chung cho cả Three.js và Godot Web → chỉ phần thế giới khác nhau giữa 2 engine. Port sang client Godot thật: giữ nguyên `classic_hud.gd`, chỉ thay lớp `Room` bằng cảnh HD-2D.
- Trái-trên: chân dung + thanh HP/MP pet, "Tên · Lv" người chơi, tên · Lv pet; 2 nút tròn Linh thú / Nhiệm vụ. Phải-trên: tên map, vàng/pha lê, nút Menu (lưới 6 nút: Linh thú, Vật phẩm, Nhiệm vụ, Cửa hàng, Hội, Cài đặt).
- Dưới: D-pad trái (tâm = menu) · chat giữa với 6 tab **Chung / Hệ thống / Riêng / Đội / Thế giới / Hội** · phải **Chọn** / **Trở về**.
- "Cài đặt" mở bảng dev (tier, Trụ → Rừng sâu, bench, xuất JSON, số liệu). Số FPS gọn ở giữa trên. `?hud=0` tắt HUD (đo thuần engine); `?chatdemo=0` bỏ tin mẫu.
- Tin chat Thế giới/Đội/Hội/Riêng và các nút menu là **dữ liệu mẫu**, chưa nối server (chưa có hệ thống đội/hội/nhắn riêng).
- Camera dịch xuống theo chiều cao dải dưới để nhân vật nằm giữa vùng thế giới nhìn thấy.

- Vòng 4: Godot đóng gói scene.json + texture vào .pck (`tools/sync_godot_data.sh` rồi export) thay vì HTTPRequest, vì trên host công khai việc tải ảnh qua mạng từng thất bại một phần (thế giới đen). Three thử lại 3 lần, thất bại thì dùng texture hồng. Mọi lỗi trang/engine hiện trong tab Hệ thống dưới dạng `[lỗi]`.
