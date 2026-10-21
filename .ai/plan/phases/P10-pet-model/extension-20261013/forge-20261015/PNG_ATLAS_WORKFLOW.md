# Phimond — quy trình atlas PNG

Owner correction, 15/10/2026: dùng ảnh atlas, không tạo video.

Mỗi loài xuất **một PNG RGBA 1124×1405**, 4 cột × 5 hàng; mỗi ô 281×281, tổng 20 pose khác nhau. Alpha của nhân vật và hiệu ứng nằm trong cell-local [22,259). Hướng cơ sở bên trái. Giữ anatomy, tóc, vũ khí, palette, tỷ lệ và pivot nhất quán.

| Hàng | Animation | Bốn frame | Phát |
|---|---|---|---|
| 1 | Idle | Bốn pose thở/dao động nhẹ, nối về pose đầu | Lặp |
| 2 | Move | Bốn pose bước/di chuyển/lơ lửng liên tục | Lặp |
| 3 | Basic attack | Chuẩn bị → lấy đà → đánh → hồi | Một lần, giữ frame cuối |
| 4 | Skill | Tụ phép → tạo hình → phóng → tan hiệu ứng | Một lần, giữ frame cuối |
| 5 | Hurt → down | Trúng đòn → yếu → ngã → nằm gục hoàn toàn | Một lần, giữ frame cuối |

Mẫu nhân vật một pose đã duyệt là reference để vẽ đủ 20 pose; duyệt mẫu không đồng nghĩa duyệt atlas hoàn thiện. Không nhân cùng một pose thành 20 ô. Không cần API video, clip video hoặc trích frame từ video.

Đã đọc trực tiếp:

- Thần Đèn: `assets/pets/redraws/owner-feedback-20261009/species_0143/attempt-01/packed.png`.
- Đại Vương Bọ Cạp: `assets/pets/redraws/owner-feedback-20261009/species_0151/attempt-01/packed.png`.
- Các atlas đã duyệt species_0154, species_0156, species_0158 trong extension-20261013.
- Contract `P10-redraw-plan.md`; playback `reference_art.gd`, `preview_p10_redraw.py` và `p10_review.html`.

Áp dụng Sprite Forge cho spec/pose, nhận diện, kiểm tràn ô và đóng gói. Chỉ dẫn trực tiếp của chủ dự án ghi đè nhánh video của skill trong task này; không sửa skill toàn cục. Các kết quả doctor về video được giữ làm lịch sử, không dùng để chặn việc vẽ atlas.

Kiểm tra geometry và 20 frame khác nhau, rồi xem từng hàng ở 64/96/192 px. Geometry PASS không thay thế kiểm anatomy, pose, vũ khí, hướng đánh và hiệu ứng. Giữ bản raw, không cắt mất phần nhìn thấy hay xóa alpha để làm số PASS. Atlas mới cần chủ dự án duyệt trước khi chọn art/runtime. 152 atlas và 3 atlas mới đã duyệt giữ nguyên.
