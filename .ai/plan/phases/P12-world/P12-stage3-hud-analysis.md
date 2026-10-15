# P12 Stage 3 — Phân tích HUD (2026-10-14)

## Vấn đề
Bản prototype Stage 3 đầu tiên dựng HUD debug tự chế (chữ thông số, joystick tròn, nút "Trụ/Bench/JSON") phủ lên cảnh. Owner chốt: **chỉ đổi phần thế giới sang HD-2D, giữ nguyên HUD game hiện tại.**

## Nguồn đã đối chiếu
| Nguồn | Nội dung dùng |
|---|---|
| `apps/game-client/scripts/classic_hud.gd` | Toạ độ từng phần tử trên canvas 960×640 (thế giới 454 px = 71%, dải dưới 186 px) |
| `apps/game-client/assets/reference/hud/` + `hud.json` | 44 sprite Unity trích từ APK 3.2 (dpad, frame_bars, frame_portrait, bar_hp/mp, button_confirm/back, panel_controls, frame_chat, button_*…) |
| `docs/research/HUD_REFERENCE.md`, `VIDEO_UI_AUDIT_2026-09-23.md` | Tỉ lệ vùng đo từ video, nút gold edge/menu tròn, ghi chú "chat không có thanh tab cố định" |
| MonoScript APK (`ChatView`, `ChatController`, `Joystick`) | Chỉ có tên lớp, không có layout/tên tab → tab chat là yêu cầu của owner, không phải dữ liệu APK |

## Bố cục chuẩn (giữ nguyên)
- Trái-trên: `frame_portrait` + chân dung pet + sprite người chơi; `frame_bars` với HP đỏ / MP xanh; "Tên · Lv.N"; 2 nút tròn Linh thú, Nhiệm vụ.
- Phải-trên: tên map, vàng · pha lê, nút Menu.
- Dải dưới: D-pad trái (panel 245 px) · chat giữa (frame_chat) · Chọn / Trở về phải (panel 197 px).

## Thêm theo yêu cầu owner
- Chat có 6 tab: Chung (log chung), Hệ thống, Riêng, Đội, Thế giới, Hội. Lệch với video (không có tab) — owner yêu cầu rõ, nên làm theo.
- Menu bên phải mở lưới 6 nút. Đây là khung hình; các chức năng chưa nối.

## Cách làm ở prototype
HUD là lớp DOM `shared/hud/hud.js`, dùng chung Three.js + Godot Web (benchmark chỉ so phần thế giới). Khi port vào client Godot thật: giữ `classic_hud.gd`, chỉ thay `Room` bằng cảnh HD-2D; thêm 6 tab vào RichTextLabel chat.

## Chưa làm / cần quyết
- Tin nhắn Thế giới/Đội/Hội/Riêng là tin mẫu; hệ thống đội/hội/nhắn riêng chưa có ở server.
- Tên tab "Chung" vs "Log chung" (đang rút gọn cho vừa dải chat trên iPhone).
