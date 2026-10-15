# P12 Stage 3 — Benchmark spec: Godot 4 Web vs Three.js (mobile browser)

> **SUPERSEDED 2026-10-15:** owner đã chọn Three.js (ADR-0001, Accepted 2026-10-14). Spec này giữ làm lịch sử; phần đo iPhone/Safari còn lại theo dõi trong [P12-closure-checklist.md](P12-closure-checklist.md).

Ngày: 2026-10-14. Status: ~~DRAFT — chờ owner duyệt~~ SUPERSEDED. Chỉ là tài liệu; **chưa chạy gì** (Stage 3 NOT_RUN, chưa được cấp quyền).
Nguồn quyết định: D21 (benchmark, không chọn engine trước), D22 (hard gate trước, rồi chấm điểm), D23 (FPS tier là target), D24 (tải/cache asset), D25 (Logical/Visual/Asset Manifest tách riêng), SCP-01/SCP-03 trong [P12-spec-change-proposals.md](P12-spec-change-proposals.md).

Mọi con số đánh dấu **[OWNER]** là đề xuất khởi điểm, chưa có cơ sở đo. Owner thay hoặc xác nhận trước khi chạy. Spec này không chọn production renderer, không cho phép migration, và không thay chứng nhận 60Hz riêng của Master §7.

## 1. Mục tiêu
Trả lời một câu: với cùng một cảnh Emerald Forest HD-2D, engine nào **chạy ổn định hơn trên trình duyệt mobile** (iOS Safari, Android Chrome) và đạt chất lượng nhìn, input, chi phí dựng. Ổn định (không crash, không rò bộ nhớ, hồi phục được) được xét trước hiệu năng thuần.

## 2. Nguyên tắc công bằng
1. **Cùng dữ liệu logic.** Một bộ `logical world` (bounds, lưới X/Y, collision, portal, arrival, access, NPC) dùng chung, nạp từ cùng file. Hai bản chạy xong phải sinh **cùng chuỗi sự kiện** (so khớp từng byte) với cùng kịch bản.
2. **Cùng asset và ngân sách.** Cùng texture, cùng sprite atlas (P10: RGBA 1124×1405, 20 frame, 5 animation), cùng độ phân giải canvas, cùng số pet hiển thị. Không bản nào được dùng asset đã tối ưu riêng.
3. **Cùng cách phục vụ.** Cùng host, HTTPS, nén Brotli/gzip, cùng header cache. Không bật COOP/COEP cho riêng bản nào.
4. **Cấu hình pin cố định.**
   - Godot: bản export của project (4.7.2), **Compatibility renderer**, Web **đơn luồng** (mặc định từ 4.3), template tối giản nếu có.
   - three.js: một phiên bản pin, **`WebGLRenderer`**. `WebGPURenderer` còn experimental và không hỗ trợ `ShaderMaterial`, nên chỉ chạy như thử nghiệm phụ, **không tính điểm**.
5. **Cùng người chấm, cùng kịch bản, chạy lặp ≥3 lần**, bỏ 30 giây đầu (warm-up).

## 3. Dataset: "Golden Scene" Emerald
- **Phiên bản dữ liệu:** nếu baseline Stage 2 đã duyệt thì dùng bản đó. Nếu chạy trước baseline thì dùng **Emerald tạm (placeholder)**, gắn nhãn `NON_CANONICAL` trên mọi báo cáo, và kết quả chỉ để tham khảo.
- **Lát cắt S1 (render):** cảnh tĩnh và animation. Camera nghiêng, môi trường 3D đơn giản + texture pixel, vật trang trí dạng billboard, sprite 2D cho nhân vật và pet, smart occlusion (D14), ánh sáng và VFX nhẹ của biome.
- **Lát cắt S2 (traversal):** di chuyển X/Y, collision, đi qua portal tới safe hub và quay lại, arrival an toàn, từ chối truy cập.
- **Mật độ pet:** quét 4 / 8 / 16 pet hiển thị cùng lúc (mỗi pet một atlas khác nhau, tải lazy theo ID).
- Chỉ số tham chiếu khi lên kế hoạch bộ nhớ: mỗi atlas ≈ 6,0 MiB VRAM chưa nén, chưa tính mipmap.

## 4. Ma trận thiết bị — **[OWNER điền thiết bị thật]**
| Nhóm | Mô tả | Trình duyệt |
|---|---|---|
| A | iPhone đời cũ (ví dụ SE 2 hoặc 12) | Safari |
| B | iPhone mới | Safari |
| C | Android tầm trung | Chrome |
| D | Android yếu | Chrome |
| R | Desktop tham chiếu | Chrome, Safari |

**Owner chốt 2026-10-14 (giai đoạn đầu):** thiết bị thử là **iPhone 17 Pro Max (Safari)** và **macOS Safari**; các nhóm A, C, D chưa dùng. Chạy ở chế độ **chỉ ghi số liệu, chưa đặt ngưỡng đậu/rớt**; ngưỡng sẽ tính sau khi có các mức cấu hình **thấp / trung bình / cao** do người chơi chọn trong cài đặt. Hard gate vẫn ghi nhận đạt/không, nhưng chưa loại bản nào.

Ghi OS, phiên bản trình duyệt, RAM, chế độ tiết kiệm pin, mức pin và nhiệt độ cho mỗi lần chạy. Mọi trình duyệt iOS đều dùng WebKit, nên Chrome iOS không cần ma trận riêng (có thể thử một lần để xác nhận).

## 5. Hard gate (đậu/rớt trước khi chấm điểm)
Rớt bất kỳ gate nào trên thiết bị thuộc nhóm bắt buộc thì bản đó **không thể thắng điểm** (D22).

| Gate | Điều kiện | Ngưỡng đề xuất [OWNER] |
|---|---|---|
| G1 Tương thích | Tải, vẽ đúng, không canvas trắng trên mọi thiết bị | 100% thiết bị nhóm A–D |
| G2 Ổn định | Soak 30 phút kịch bản hỗn hợp: không crash, không tự reload, không mất context không hồi phục | 0 sự cố / 3 lần chạy |
| G3 Bộ nhớ | Sau warm-up, bộ nhớ không tăng liên tục | độ dốc ≤ 5% / 10 phút (thay bằng baseline đo được) |
| G4 Chức năng | Kịch bản S2 đạt, chuỗi sự kiện logic khớp byte | 100% |
| G5 FPS | Tier mục tiêu D23 (~30 / ~30–60 / ~60) | p95 frame time theo tier; ghi p50/p95/p99 |
| G6 Tải | Cold load tới có thể chơi; kích thước payload | giây và MB theo mạng 4G chuẩn |
| G7 Hồi phục | Nền/tiền cảnh, khóa màn hình 60 giây, xoay màn hình, resize ×20, mất context giả lập | hồi phục không cần reload |
| G8 Input | Chạm, đa điểm, không kẹt input sau `touchcancel`, độ trễ chạm→phản hồi | ngưỡng ms [OWNER] |

## 6. Kịch bản có script
1. K-01 Cold load (cache trống) và warm load.
2. K-02 Idle 60 giây trên Golden Scene.
3. K-03 Đi vòng cố định 5 phút (mỗi bản dùng cùng đường đi).
4. K-04 Portal ping-pong Emerald ↔ safe hub ×20 (kiểm tra giải phóng texture khi đổi map).
5. K-05 Quét mật độ pet 4 / 8 / 16.
6. K-06 Nền/tiền cảnh, khóa màn hình, xoay, resize.
7. K-07 Giả lập mất WebGL context (`WEBGL_lose_context`) rồi khôi phục.
8. K-08 Soak 30 phút trộn K-03, K-04, K-05.
9. K-09 Âm thanh: mở khóa bằng chạm, lặp hiệu ứng 30 phút. Godot chạy hai biến thể: playback **Sample** và **Stream**.

## 7. Đo lường
- **Frame time:** ghi timestamp mỗi frame bằng cùng một bộ đo JS cho cả hai bản (xuất JSON cùng schema). Với Godot, đọc qua cầu JS; không dùng số FPS riêng của engine.
- **Bộ nhớ:** Safari Web Inspector / Instruments (iOS), Chrome remote DevTools (Android). Thêm bộ đếm **texture bytes ước tính** do chính app báo cáo. Ghi mọi sự kiện kill/reload.
- **Tải:** payload bytes, thời gian tới tương tác, số request.
- **Ghi kèm mỗi lần chạy:** thiết bị, OS, trình duyệt, cache cold/warm, preset chất lượng, trạng thái nhiệt, pin, nền/tiền cảnh. Preset không phải giới hạn FPS.
- Lưu raw JSON và log; báo cáo phải dẫn tới file thô.

## 8. Chấm điểm (chỉ sau khi qua hard gate; D22)
| Tiêu chí | Trọng số | Cách chấm |
|---|---|---|
| Chất lượng nhìn và độ dễ đọc | 30 | Owner xem Golden Scene theo tiêu chí Art Bible (D27), có ảnh chụp cạnh nhau |
| Hiệu năng mobile | 30 | Từ số đo gate (FPS, frame time, bộ nhớ, tải) |
| Input | 15 | Độ trễ, độ chính xác chạm, ổn định đa điểm |
| Tái sử dụng | 15 | Chi phí ước lượng để dùng lại HUD, protocol Go WebSocket, pipeline asset, `apps/web` hiện có |
| Bảo trì | 10 | Độ phức tạp build, phụ thuộc engine, khả năng gỡ lỗi bộ nhớ trên mobile |

Tổng 100. Điểm là thông tin hỗ trợ quyết định, không tự chọn engine.

## 9. Điểm rủi ro cần soi riêng (từ báo cáo công khai, chưa kiểm chứng trên bản 4.7.2)
- Godot Web trên Safari từng tăng bộ nhớ đến khi bị kill (godot#89169) và crash trên mobile browser (forum 4.4.1).
- Godot 4.5.1: crash âm thanh trên iOS sau 10–30 phút với playback Sample (godot#116750); có workaround Stream.
- Giới hạn bộ nhớ Wasm 2GB trên iOS cũ (godot#70621).
- iOS kill tab khi vượt khoảng 300–400 MB trên máy cũ (số ước chừng); mất context khi nền lâu.
- three.js: nguy cơ rò khi quên `dispose()` geometry/material/texture; cần handler `webglcontextlost` / `webglcontextrestored` và dựng lại tài nguyên.

## 10. Việc owner cần chốt trước khi chạy
1. Danh sách thiết bị thật (mục 4).
2. Ngưỡng của mọi ô **[OWNER]** ở mục 5.
3. Chạy trên Emerald tạm hay chờ baseline Stage 2.
4. Phiên bản three.js pin và xác nhận chỉ tính điểm `WebGLRenderer`.
5. Cấu hình export Godot (Compatibility, đơn luồng, template tùy biến hay mặc định).
6. Thư mục đặt mã benchmark (đề xuất tách khỏi `apps/` chính, ví dụ `bench/godot-web` và `bench/three-web`) và host thử nghiệm.

## 11. Ngoài phạm vi
Không đổi engine, không gameplay (combat, farm, XP thuộc phase khác), không phải chứng nhận 60Hz hay 50 CCU, không phải đóng P01 hay P12. Mọi quyết định production renderer và migration cần quyền riêng sau khi có bằng chứng đo.

## 12. Đầu ra
Raw JSON và log từng lần chạy; ảnh chụp cạnh nhau; bảng gate theo thiết bị; bảng điểm; ghi chú các sự cố. Một memo khuyến nghị cho owner quyết định, có nêu rõ phần nào là suy luận.
