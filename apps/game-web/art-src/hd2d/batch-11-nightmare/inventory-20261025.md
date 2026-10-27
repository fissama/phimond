# Đảo Ác Mộng — kiểm kê trực tiếp 2026-10-25

Nguồn: kit-nightmare.md, REDRAW-QUEUE-20261024.md, manifest.json, từng final.png và qa.json trên filesystem. Không dùng lịch sử hội thoại làm bằng chứng.

- Hàng đợi: 54 map / 14 kit; 13 kit ngoài Nightmare chưa có final tại batch-11 tương ứng.
- Nightmare: 12 final, 12 hash khớp manifest, 12 approved=false. QA đã lưu cho cả 12: actual_complete_4x_dark_and_checker_viewed, failures=[]. Đây là bằng chứng QA lưu trên file; không nói rằng phiên này đã mở lại 12 ảnh.
- Hiện có: rễ 01–03, tinh thể 07–09, landmark-01 của mỗi map.
- asset_drawn là trạng thái từng asset sau kiểm ảnh. map_completed chỉ true khi dựng và kiểm cảnh; cả 6 map hiện false.
- 52 hàng chưa vẽ = 46 hàng kit + 6 landmark-02 tùy chọn. Số hàng KHÔNG phải số artwork độc lập: một số hàng bao gồm nhiều khung hoặc trùng chức năng.

## Phần còn thiếu theo checklist

- [ ] `nightmare-floor-01` (floor) — đất tím nứt — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-floor-02` (floor) — đá đen — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-floor-03` (floor) — nền phế tích — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-04` (prop) — cây khô xoắn (sway-split) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-05` (prop) — cây khô xoắn (sway-split) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-06` (prop) — cây khô xoắn (sway-split) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-10` (prop) — cổng ma pháp đen (dormant/active) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-11` (prop) — xương/di vật — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-12` (prop) — tàn tích tường — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-13` (prop) — trại tàn sinh (lều rách, đống lửa 4 khung) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-prop-14` (prop) — đèn ma trơi (4 khung) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-backdrop-far-01` (backdrop_far) — đảo đen giữa biển tím — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-backdrop-far-02` (backdrop_far) — trăng — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Đảo Ác Mộng, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ.
- [ ] `nightmare-floor-extra-01` (floor) — tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512
- [ ] `nightmare-floor-extra-02` (floor) — tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512
- [ ] `nightmare-floor-extra-03` (floor) — tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512
- [ ] `nightmare-floor-extra-04` (floor) — tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512
- [ ] `nightmare-floor-extra-05` (floor) — tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512
- [ ] `nightmare-edge-01` (edge) — dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc
- [ ] `nightmare-edge-02` (edge) — dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc
- [ ] `nightmare-edge-03` (edge) — dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc
- [ ] `nightmare-decal-01` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-02` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-03` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-04` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-05` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-06` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-07` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-08` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-09` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-10` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-11` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-decal-12` (decal) — decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm
- [ ] `nightmare-shadow-01` (shadow) — bóng procedural alpha mềm, màu kit
- [ ] `nightmare-shadow-02` (shadow) — bóng procedural alpha mềm, màu kit
- [ ] `nightmare-shadow-03` (shadow) — bóng procedural alpha mềm, màu kit
- [ ] `nightmare-shadow-04` (shadow) — bóng procedural alpha mềm, màu kit
- [ ] `nightmare-backdrop-far` (backdrop) — 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác
- [ ] `nightmare-backdrop-mid` (backdrop) — 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác
- [ ] `nightmare-backdrop-near` (backdrop) — 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác
- [ ] `nightmare-portal-dormant` (portal) — cổng nhìn thẳng mặt trước, đúng tông kit
- [ ] `nightmare-portal-active` (portal) — cùng mask với dormant
- [ ] `nightmare-marker-arrival` (marker) — vòng sáng 4 khung
- [ ] `nightmare-fx-01` (fx) — hạt/tia sáng sprite sheet theo chủ đề
- [ ] `nightmare-fx-02` (fx) — hạt/tia sáng sprite sheet theo chủ đề
- [ ] `nightmare-fx-03` (fx) — hạt/tia sáng sprite sheet theo chủ đề
- [ ] `nightmare_island_survivor_camp-landmark-02` (landmark) — (vật nhận diện #2, nếu có)
- [ ] `nightmare_island_east_magic_island-landmark-02` (landmark) — (vật nhận diện #2, nếu có)
- [ ] `nightmare_island_ruins-landmark-02` (landmark) — (vật nhận diện #2, nếu có)
- [ ] `nightmare_island_disaster_gate-landmark-02` (landmark) — (vật nhận diện #2, nếu có)
- [ ] `nightmare_island_resentment_path-landmark-02` (landmark) — (vật nhận diện #2, nếu có)
- [ ] `nightmare_island_despair_land-landmark-02` (landmark) — (vật nhận diện #2, nếu có)

## Ánh xạ và thứ tự làm

1. `nightmare-prop-11`: xương/di vật; `nightmare-prop-12`: tường đổ. `nightmare-camp-tent` là thành phần mới của hàng prop-13; prop-13 vẫn false cho tới khi có lửa trại 4 khung.
2. 8 tile sàn, 3 cây tách lớp, 3 edge; tiếp tới decal/backdrop.
3. Cổng hai trạng thái: hàng prop-10 là nhóm bao phủ bởi portal-dormant + portal-active, không nhân đôi hình. Chỉ đánh dấu nhóm khi cả hai đạt và mask khớp.
4. Far-01 (đảo/biển) có thể phục vụ lớp far nếu đủ hợp đồng; far-02 (trăng) cần xác định là lớp/biến thể riêng. Chưa gán alias tới file chưa có.
5. Lửa trại, đèn ma trơi, arrival và FX cần khung + kiểm chuyển động; không tính ảnh tĩnh là animation hoàn chỉnh.
6. Dựng cảnh sau giai đoạn asset; chưa đổi runtime, collision hay portal.

Lượt đầu camp-relic-wall-08/raw-01.png tự loại: bone269x134 >208x144; wall458x262 >368x240; tent419x312 >368x272. Giữ nguyên raw. Đã lên retry với cùng pixel budget, không thu nhỏ final bằng code.
