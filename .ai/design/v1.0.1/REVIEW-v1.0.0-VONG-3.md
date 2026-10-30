# Review v1.0.0 vòng 3 — người chơi khó tính, trước khi deploy

Ngày 2026-10-30. Chơi từ tài khoản mới (1280×720, chất lượng Thấp do container không có GPU; mobile 390×780), qua đăng nhập → đăng ký → chọn nhân vật → Triệu Linh Điện → chọn bệ → Bìa Rừng → Túi đồ/Linh thú/Nhiệm vụ/Cài đặt. Ảnh ở `/tmp/rv` (không commit).

## Kiểm tra máy
- tsc sạch; vitest 27/27; Go `content` + `world` pass; `vite build` ok (JS 742 kB, cảnh báo chunk >500 kB).
- E2E smoke 15/15 pass (5.7 phút); kịch bản chơi thử không có lỗi console/pageerror.
- Không chạy được ở container: build đầy đủ server Go (không tải được module), MySQL thật (migration 003 chưa thử), GPU thật (hiệu năng HD-2D chưa đo).

## Lỗi tìm ra và đã sửa
- **P2 chim tiền cảnh ở Bìa Rừng không hiện:** scene.ts dùng `fg-ambient-birds` nhưng file ảnh tên `ambient-birds.png` → 404 im lặng. Đã thêm `fg-ambient-birds.png` (đúng 388×155 như manifest).

## Chấm điểm (so vòng 2)
| Hạng mục | V2 | V3 | Ghi chú |
|---|---|---|---|
| Màn đăng nhập | — | 8.5 | Cảnh HD-2D thống nhất, thú idle, khung vàng, icon mắt. Chưa kiểm tra hoạt ảnh trên máy thật |
| Đồ họa thế giới | 7.5 | 8 | Cột/mái/cửa sổ vòm mới. Cửa sổ hông đại sảnh nằm sát mép màn hình nên gần như không thấy được |
| HUD / UI | 8 | 8 | Ô vật phẩm có khung; chưa có khung theo độ hiếm |
| Combat | 8 | 8 | Smoke pass; vòng này chưa xem lại ảnh trận |
| Dẫn dắt người mới | 8 | 8 | Mục tiêu rõ |
| Nội dung | 6.5 | 6.5 | Không đổi |

## Điểm còn xấu (không chặn deploy)
1. **Thẻ chọn thú đầu tiên:** icon thú rất nhỏ trong khung lớn; mép trái khung mô tả có răng cưa nhiễu; nút "Chọn" tròn ở góc phải dưới bị đè chữ trên nền tối.
2. **Chữ trong ô chat dưới cùng bị cắt dòng đầu** ("Chọn, phím E hoặc Space.") khi log dài.
3. **Mobile:** chữ "Đăng nhập" trên nút xuống hai dòng; D-pad đè lên khung chat.
4. **Túi đồ:** không có độ hiếm (ô slot-rare/epic/uncommon chưa dùng); mô tả "mở ở bản sau" lộ tính năng chưa có.
5. **Tên NPC mờ** khi ở xa (Thợ Săn Rowan gần như không đọc được).
6. **Tải trang:** public ~62 MB (hd2d 29 MB, ui 13 MB), ảnh lớn nhất 1.4 MB; chưa nén/lazy-load.
7. **Mái nhà `hall-outside-roofs-side`** đã duyệt nhưng không dùng (cửa sổ mới tự có view mái).
8. **79 PNG không có trong manifest** (idle NPC, login-*, idle-*): hợp lệ vì nạp theo tên, nhưng nên có kiểm tra tự động manifest ↔ file để khỏi lặp lỗi chim.

## Việc bắt buộc trước khi deploy (người làm, không làm được ở container)
- Build + chạy `go test ./...` đầy đủ trên máy; chạy migration 003 trên MySQL thật.
- Chơi thử một lần trên máy có GPU ở chất lượng Cao/Trung bình, kiểm tra FPS màn đăng nhập (nhiều lớp parallax) và đại sảnh.
- Điều khoản/Quyền riêng tư pháp lý VN: đã hoãn theo quyết định chủ dự án; không deploy công khai khi chưa có.
- Chưa push: toàn bộ commit đang ở repo local.

## Kết luận
Không có lỗi chặn trong luồng chơi đã kiểm tra. Sẵn sàng deploy **thử nội bộ/staging** sau khi làm 3 việc bắt buộc ở trên; **chưa** nên mở công khai trước khi có phần pháp lý và đo hiệu năng trên máy thật.
