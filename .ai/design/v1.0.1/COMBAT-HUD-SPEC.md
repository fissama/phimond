# Combat HUD — 1 pet đấu 2–3 quái, hướng 3v3

Cập nhật 2026-10-22. Chủ game quyết: **đánh quái hoang = 1 pet đấu 2–3 quái GIỐNG NHAU; xác suất 3 quái cao hơn 2 quái**. Tương lai PvP 3v3.

## Căn cứ trong kế hoạch
- Master spec §2: PvE bắt đầu bằng pet solo vs 3 quái; PvP 3 pet mỗi bên (3v3); party ≤3 người, mỗi người 1 pet. HUD/log nằm ngoài vùng làm mờ; mức Thấp/Vừa/Cao vẫn phải thấy mục tiêu, HP, trạng thái.
- Video/audit game gốc: bệ lệnh cyan trên giữa; marker mục tiêu = kim cương cyan dưới chân + mũi tên + tên/thanh HP; marker quái gục; không popup thưởng (chat cập nhật); đồng minh bên phải, quái bên trái.

## Quyết định
| Chủ đề | Quyết định |
|---|---|
| Số quái | `rules.encounter_weights` = `[0, 40, 60]` → 0% một quái, 40% hai, 60% ba. Mảng rỗng = luôn 1 quái (tương thích dữ liệu cũ). Đấu trường luôn 1 đối thủ. |
| Quái | Cùng loài, cùng cấp, mỗi con chỉ số/HP riêng. Cùng tên → hậu tố A/B/C theo đội hình. |
| Mục tiêu | Intent `target_id` (tùy chọn). Thiếu → quái sống đầu tiên; sai/đã gục → lỗi `invalid target`. |
| Hành động nhắm 1 mục tiêu | Tấn công, kỹ năng (target ≠ self), Bắt. Còn 1 quái sống → gửi thẳng; ≥2 → chế độ chọn: kim cương cyan + ▼ trên khung tên, chạm quái để xác nhận, nút Hủy. Phòng thủ/Vật phẩm/Tự động/Chạy không cần chọn. |
| Bắt | Bắt 1 con: con đó rời sân (HP→0), vẫn tính XP; trận chỉ kết thúc `capture` khi không còn quái sống, `win` nếu hạ nốt bằng đánh. |
| Thưởng | XP = tổng theo từng quái bị hạ/bắt (BattleXP × cấp quái). Vàng = BattleGold × số quái (**xem cờ 2**). |
| Kết thúc | Thắng khi hết quái sống; thua khi pet mình hết HP. Mỗi quái sống ra đòn 1 lần/lượt nhắm pet mình. |
| Bố cục | Đặt theo điểm chân trên mặt đất phối cảnh (bóng đúng chân). Ngang: quái chéo A (13%,60%) → B (27%,70%) → C (41%,80%), pet (72%,74%). Dọc (<700px): quái hàng trên, pet hàng dưới. 3v3: phe mình đã render nhiều ally theo slot (68%,60%) · (80%,71%) · (70%,82%), thẻ trạng thái xếp dọc góc trên trái. |

## Cờ cần chủ game quyết
1. **Xung đột master spec P02-R07**: ghi "3 quái với identity riêng" và chưa chốt thành phần encounter, trái với quyết định "2–3 quái giống nhau, P(3)>P(2)". Chưa sửa master spec. Đề xuất sửa: *"Encounter hoang gồm 2–3 quái cùng loài và cùng cấp (xác suất cấu hình, mặc định 40%/60%); identity khác nhau chỉ áp dụng cho boss/sự kiện. Thành phần encounter khi party >1 người quyết riêng."*
2. **Vàng ×số quái**: mới chọn nhân theo số quái để thưởng tăng theo rủi ro; nếu muốn giữ 1 phần vàng cố định, đổi trong `battleAction`.
3. **Cân bằng** (đã xử lý đợt 6): Chạy đi trước mọi đòn; quái hoang ×0.85, đàn ×0.55/×0.4; `damage_scale` 1.0; pet khởi đầu biết đòn hệ; Tự động dùng đòn mạnh nhất. Pet Lv1 auto thắng ≥92% ở Bìa Rừng (xem `REVIEW-v1.0.0-VONG-2.md`).
4. **Chưa có**: AoE, chọn mục tiêu cho đồng đội/hồi máu (3v3), mục tiêu tự đổi khi quái gục giữa lượt (server hiện bỏ qua con gục), hiệu ứng kỹ năng.

## Kiểm
`gt test ./internal/...` (có test tỉ lệ 2/3 quái, thưởng theo số quái, mục tiêu gục bị từ chối), vitest 21, Playwright 8 (thêm test chọn mục tiêu chạy trên server luật thật, cổng 8097/5187; các test đi bộ ép 1 quái bằng `GAME_ENCOUNTER_WEIGHTS=1`, chỉ devserver).

Ảnh: `combat-1v3/combat-1v3-land.png`, `combat-1v3-port-aim.png`, `combat-1v2-port.png`.
