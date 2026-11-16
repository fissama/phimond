# Roadmap khu vườn ngầm — art + tích hợp (2026-11-10)

Quy tắc chung: mỗi lượt giao cho Codex theo một prompt, Codex tự lặp tới khi qua cổng, Claude nghiệm thu độc lập (đo + xem ảnh), duyệt rồi mới sang đợt sau. Không nới tiêu chí.

## Đã xong
- garden-a: 29 asset kit nền (thân, ấn, mạch...) đã duyệt.
- garden-b pilot (2026-11-10): chậu G1 Thổ Đào Bồn, Bạc Hà, Mộc Nhĩ đã duyệt. Pipeline đóng gói Đơn 16 ổn định.

## Giai đoạn A — Art còn lại (15 lượt Codex)
| Lượt | Nội dung | File prompt | Ghi chú |
|---|---|---|---|
| K1 | Hạt theo họ (6) + bong bóng thiếu nước | 23-kit-K1-prompt.md | chạy song song, nhỏ |
| P1 | 5 chậu: G1b, G2a, G2b, G3a, G3b | 21-pots-P1-prompt.md | cần xong trước khi vertical slice |
| C01 | Lv2,4,5,6,8: Rau Má, Khoai Lang, Cúc Hoa, Tía Tô, Củ Mài | 20-batch-C01-prompt.md | |
| C02 | Lv7,9,10,11,12: Cà Chua, Nấm Rơm, Hướng Dương, Ớt, Sả | C02 | |
| C03 | Lv13–17: Củ Đậu, Chuối, Hoa Giấy, Gừng, Nấm Hương | C03 | |
| C04 | Lv18,19,20,22,24: Bí Đỏ, Lá Lốt, Khoai Môn, Hoa Hồng, Dưa Hấu | C04 | |
| C05 | Lv26–34: Ngải Cứu, Nghệ, Đu Đủ, Hoa Súng, Ổi | C05 | |
| C06 | Lv36–44: Riềng, Mướp Đắng, Kỷ Tử, Hoa Mai, Xoài | C06 | |
| C07 | Lv46–54: Sắn, Nấm Đầu Khỉ, Hoa Sen, Bưởi, Tam Thất | C07 | |
| C08 | Lv56–64: Dừa, Hoa Đào, Mít, Linh Chi, Chôm Chôm | C08 | |
| C09 | Lv66–74: Hoa Lan, Nhân Sâm, Thanh Long, Ngân Nhĩ, Măng Cụt | C09 | |
| C10 | Lv76–84: Hoa Quỳnh, Đông Trùng, Vải Thiều, Hổ Phách Mầm, Sầu Riêng | C10 | |
| C11 | Lv86–94: Nguyệt Huỳnh Tinh, Tuyết Liên, Tinh Hoa Liên, Thạch Anh Quả, Cà Phê | C11 | |
| C12 | Lv96–100: Hồ Tiêu, Địa Mạch Kết Tinh, Linh Mạch Mầm | C12 | |
| P2 | 4 chậu: G4a, G4b, G5a, G5b | 22-pots-P2-prompt.md | sau P1 |

Cập nhật 2026-11-10: Đợt 1 cũ (Cúc Hoa, Củ Mài, Nấm Hương đạt hoặc gần đạt, Địa Hoàng bỏ khỏi roster) đã chạy trước; C01–C03 đã bỏ các cây này, các đợt giữ 3–5 cây, xem từng file 20-batch-*.md để biết danh sách đúng (bảng trên là dự kiến ban đầu).

Thứ tự đề xuất: K1 + P1 + C01 → C02 → C03 ... (C theo level mở khóa để build chơi được sớm).

## Giai đoạn B — Tích hợp (bắt đầu sau K1 + P1 + C01 + C02 = lát cắt dọc Lv1–12)
1. Dữ liệu: bảng 60 cây (id, họ, level, thời gian lớn, giá, sản lượng) từ roster-v2; bảng 10 chậu và hạng.
2. Server Go: trạng thái ô (hạt/mầm/lớn/chín/khát), tính giai đoạn theo % thời gian: 0–15% hạt, 15–45% sprout, 45–85% grow, 85–99% grow lấp lánh, 100% ripe.
3. Client Three.js: loader atlas + anim.json; chọn hàng theo trạng thái; tưới = chậu chạy hàng water, cây rung nhẹ bằng engine; khát nước = bong bóng garden-c gắn trên cây; thu hoạch = harvest rồi plant.
4. Cân bằng: tiền, thời gian, level 1–100 (1 cây/level tới Lv20, rồi 1/2 level).
Mốc kiểm: chơi được Lv1–12 với 12 cây + 2 chậu + hạt + bong bóng.

## Giai đoạn C — Art sau (chưa soạn prompt)
Sâu bọ, FX (mưa tưới, ánh thu hoạch), aura đột biến, props trang trí, cổng ấn tầng 10, khung UI vườn.

## Giai đoạn D — QA tổng
Duyệt toàn bộ manifest, contact sheet 60 cây + 10 chậu, kiểm tra kích thước tải, thử thiết bị yếu, tinh chỉnh tint từng màn.
