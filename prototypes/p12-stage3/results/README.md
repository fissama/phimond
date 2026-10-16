# Kết quả benchmark Stage 3 (Three.js, iPhone)

Đo ngày 2026-10-16 bằng `three/index.html?tier=high&auto=1&secs=60` (cảnh Emerald HD-2D, nhân vật tự chạy, 60 giây).
Máy: iPhone 17 Pro Max, Safari (iOS 18.7), Apple GPU, WebGL 2.0, 4 core. Canvas 832×290 ở DPR 2 (trang chạy trong khung nhúng, nhỏ hơn màn hình đầy đủ).

| | Lần 2 | Lần 3 |
|---|---|---|
| File | `iphone17promax-safari-three-high-run2.json` | `...-run3.json` |
| FPS trung bình | 60,0 | 59,85 |
| Khung hình | 3601 | 3592 |
| p50 / p95 / p99 | 17 / 17 / 26 ms | 17 / 17 / 27 ms |
| Khung dài nhất | 30 ms | 42 ms |
| Khung > 33 ms / > 50 ms | 0 / 0 | 8 / 0 |
| Mất ngữ cảnh GL | 0 | 0 |
| Dựng map khi qua cửa | 3–7 ms | 3–7 ms |
| Draw call / tam giác | 103 / 190 | 105 / 194 |

Lần 1 bỏ (cache lạnh). Medium/low chưa đo; owner quyết định không đo thêm.

## Cách đọc
- Safari giới hạn rAF ở 60 FPS dù màn 120 Hz: số liệu chỉ chứng minh giữ được 60 FPS, không đo độ dư GPU.
- Mốc thời gian bị làm tròn ms nên p50/p95 luôn 17 ms; `over16_7` trong file không có ý nghĩa. Chỉ p99 và khung dài nhất phản ánh độ giật.
- Canvas nhỏ hơn màn hình thật; tải GPU khi có HUD/canvas đầy đủ sẽ cao hơn.
- macOS Safari chưa đo (không bắt buộc theo quyết định đóng Stage 3).
- Trong các lần đo trước đó, nút Lưu từng ghi đè kết quả bằng bản `frames: null`; đã sửa (`BR[tier]` trong `three/app.js`).
