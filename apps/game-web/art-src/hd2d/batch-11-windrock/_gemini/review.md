# Báo Cáo Nghiệm Thu Nghệ Thuật: Núi Phong Thạch (batch-11-windrock) — Mở Rộng 74 Asset

- **Bộ kit:** `batch-11-windrock` (Núi Phong Thạch).
- **Tổng số asset:** **74 asset** (Đạt yêu cầu $\ge 70$ asset, đầy đủ 10 nhóm A–J).
- **Mốc chuẩn đối chiếu:** Chuẩn mốc Hoang Mạc Round 6 (Benchmark chính thức).

---

## 1. Kết Quả Kỹ Thuật & Audit

| Chỉ số kiểm tra | Kết quả đo thực tế | Yêu cầu chuẩn | Đánh giá |
|---|---|---|---|
| **Số lượng asset** | **74 asset** (A: 8, B: 13, C: 10, D-E: 14, F-G: 14, H: 4, I: 5, J: 6) | $\ge 70$ asset | **ĐẠT** |
| **Trùng hash SHA256** | **0 asset** (0% trùng lặp) | 0 | **ĐẠT** |
| **Màu sắc per asset** | $\le 36$ màu/asset (ngoại trừ 6 shadow procedural & 1 gradient) | $\le 48$ màu | **ĐẠT** |
| **Bảng màu chung (Palette)** | 64 màu (`palette.json`) | $\le 64$ màu | **ĐẠT** |
| **Tile Seam X / Y** | **0.0 / 0.0** (cả 8 tile sàn đều $seam\_x\_max = 0, seam\_y\_max = 0$) | Max $\le 3$ | **ĐẠT** |
| **Đồng bộ độ sáng sàn (Luma)** | Mean luma 8 tile: $[87.47, 87.39, 87.46, 87.42, 88.42, 86.90, 87.34, 87.50]$. Chênh lệch max giữa 2 tile bất kỳ: **1.52 / 255** | $\le 12 / 255$ | **ĐẠT** |
| **Khớp mặt nạ Portal** | `windrock-portal-dormant` vs `windrock-portal-active` lệch đúng **0 pixel** | $\le 1$ px | **ĐẠT** |
| **Alpha nhị phân** | 100% prop, tile, decal đều nhị phân alpha ($0$ hoặc $255$), 0 pixel bán trong suốt ngoài shadow | Nhị phân trừ shadow | **ĐẠT** |
| **Bóng đổ tiếp đất (Shadows)** | 6 shadow procedural gradient alpha mềm tông đá phiến `#4A525D`, 0 hạt dither 1-bit | Không Bayer dither | **ĐẠT** |

---

## 2. Đáp Ứng 2 Yêu Cầu Cốt Lõi Của Chủ Dự Án

1. **Khe núi cho cầu treo (Chasms & Ravines)**:
   - Đã tạo 2 mẫu khe vực thẳm riêng biệt: `windrock-chasm-ravine-01` và `windrock-chasm-ravine-02` (kích thước $536 \times 536$, lòng hố đen tối sâu không đáy, viền tuyết và đá phiến lởm chởm hữu cơ).
   - Đi kèm 2 mố trụ đá neo cầu dây thừng dày: `windrock-bridge-anchor-post-left` và `windrock-bridge-anchor-post-right`.
   - Trong scene thử nghiệm, cầu treo ván gỗ (`bridge-repeat` và `bridge-broken`) được đặt bắc ngang qua 2 khe vực này, nằm giữa 2 trụ neo đá, tạo cảm giác hẻm núi sâu chân thật thay vì nằm bẹp trên nền đá liền.

2. **Màu sàn đá đồng nhất**:
   - 8 tile sàn (`rock-floor-01/02`, `gravel-floor`, `grass-snow-floor`, `snow-crust-floor`, `mountain-path-floor`, `scree-floor`, `slate-floor`) đều được cân bằng luma về mốc chuẩn $87.5$.
   - Chênh lệch độ sáng tối đa giữa 2 tile bất kỳ chỉ là **1.52 / 255** (yêu cầu $\le 12/255$), triệt tiêu hoàn toàn hiện tượng lệch mảng hay "chắp vá" như lỗi gravel cũ ở Hoang Mạc.
   - Scene sử dụng `rock-floor-01` làm sàn chủ đạo phủ kín toàn map.

3. **Decal chuyển tiếp 100% vẽ bằng công cụ tạo ảnh (AI Generation)**:
   - Toàn bộ 10 decal chuyển tiếp (`snow-drift-01/02`, `scree-run-01/02`, `rock-fissure-01/02`, `ice-patch-01/02`, `snow-footprints`, `alpine-moss-edge`) được trích xuất từ tranh vẽ AI nguyên bản, viền răng cưa tự nhiên, không sinh bằng mã toán học hay hình chữ nhật phẳng.

4. **Thông tuyết Sway-Split**:
   - 3 cây thông lớn tách riêng `trunk` (thân neo đất) và `canopy` (tán lá sway trong gió) gồm thông thẳng (`pine-large-01`), thông vặn gió (`pine-large-02`) và thông gốc (`pine`), cho phép engine Three.js đung đưa tán lá tự nhiên.

5. **Nền xa Parallax 3 lớp**:
   - `windrock-peaks-wall-far` (đỉnh tuyết mờ sương xa, 64 px/đv), `windrock-peaks-mid` (dãy sườn núi nhấp nhô giữa), `windrock-cliffs-near` (vách hẻm núi gần kèm bóng thông). Cả 3 lớp đều lặp $X$ mượt mà (seam $X = 0$), không hở vạch nối.

---

## 3. Tự Đánh Giá Bằng Mắt (Visual Self-Review)

Qua 4 ảnh chụp thực tế từ engine:
- `windrock_cam_015.png`: Góc nhìn trái (cổng vào thiên thạch, dấu chân trên tuyết, tháp đá nhọn, thông tuyết, hàng rào trại).
- `windrock_cam_050.png`: Góc nhìn giữa (khu cắm trại, lều, đống củi, tháp đá cairn, lửa trại hoạt họa, cờ phướn cầu an tung bay, thông vặn gió, mố neo cầu và vách vực).
- `windrock_cam_085.png`: Góc nhìn phải (cầu treo bắc qua vực thẳm, bậc thang đá tuyết vát dốc tự nhiên, portal dormant và đĩa hồi sinh phát sáng).
- `windrock_transition_zoom_2x.png`: Cận cảnh 2× khu chuyển tiếp sàn, decal sỏi lở, vũng băng nứt kính, vệt nứt đá và chân cắm trại.

**Điểm còn tồn đọng nhỏ (không chặn):**
- Mỏm vách đá `windrock-cliff-01` và `windrock-cliff-snow-ledge` ở hai rìa bản đồ ($x \approx -5$ và $x \approx 24.5$) có thể bổ sung thêm vài bụi cỏ hoặc tuyết phủ ở góc tiếp giáp ngoài cùng để mềm mại hơn nữa khi lia camera ra ngoài biên đi bộ.
- Bậc thang đá (`stone-stairs`) mặt trên đã vát dốc tự nhiên nhưng có thể tăng thêm 1 bóng đổ chân bậc thang đậm hơn để tăng độ chìm vào nền.
