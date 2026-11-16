# Bảng parity client Godot → Three.js (ĐÓNG BĂNG tại M0, 2026-10-14)

Nguồn: `.ai/plan/phases/P01-world/P01-threejs-migration-plan.md` §5. Thêm hoặc bớt dòng cần chủ dự án duyệt. Cột Trạng thái: ☐ chưa làm · ◐ đang làm · ✔ xong và có test · ≈ lệch có chữ ký.

| ID | Chức năng | Milestone | Test | Trạng thái |
|---|---|---|---|---|
| F01–F04 | Đăng ký, đăng nhập, đăng xuất, thông báo lỗi thân thiện | M1 | unit + live | ☐ |
| F05–F09 | WS auth, reconnect thủ công, timeout 15 s, khóa khi đang chờ, retry cùng request_id | M1 | unit + live | ☐ |
| F10–F13 | Đi bằng phím (WASD/mũi tên, lên xuống), D-pad giữ lặp 0,18 s, tâm D-pad mở menu, preview/reconcile | M4 | e2e | ☐ |
| F14–F15 | Camera bám người chơi, nền theo map | M4 | e2e + ảnh | ☐ |
| F16–F18 | Click NPC để tới và nói chuyện, phím E (trong 3 ô), click cổng để tới và qua map | M4 | e2e | ☐ |
| F19–F21 | Menu Hành trình, contact quái theo `spawn_id` có latch, encounter ngẫu nhiên cũ khi không có spawn | M4 | e2e | ☐ |
| F22–F23 | Mất focus dừng đi, F3 hiện tọa độ/revision | M4 | e2e | ☐ |
| F30–F33 | HUD: Lv, pet, thanh HP/MP/XP, vàng/pha lê, nút menu phải | M3 | layout + ảnh | ☐ |
| F34–F37 | Chat 6 tab, Chọn/Trở về, Esc/back, thanh hành động trận | M3 | layout + ảnh | ☐ |
| F40–F41 | Menu chính 3×2 (+ kết nối lại, đăng xuất, tiếp tục), menu NPC theo role | M5 | e2e | ☐ |
| F42 | Cửa hàng mua vật phẩm | M5 | e2e | ☐ |
| F43–F48 | Linh thú: xem chi tiết, giám định, đổi pet, học skill, thả (xác nhận), cường hóa | M5 | e2e | ☐ |
| F49–F50 | Nhiệm vụ nhận/trả, Túi đồ dùng vật phẩm | M5 | e2e | ☐ |
| F51–F53 | Lai tạo (công thức, phước, xác nhận), học công thức, xem Lineage | M5 | e2e | ☐ |
| F54–F55 | Hồi phục pet, thách đấu arena | M5 | e2e | ☐ |
| F56 | Điều hướng focus menu bằng D-pad + Chọn | M5 | e2e | ☐ |
| F60–F64 | Vào trận khi contact, hành động trận, chọn mục tiêu, danh sách skill Cấp/MP, vật phẩm trận | M6 | e2e | ☐ |
| F65–F69 | Event phát đúng một lần/revision, phản hồi sát thương/trạng thái, win/loss rồi quay lại world, auto chờ ack, reconnect giữa trận không phát lại | M6 | unit + e2e | ☐ |
| F70–F74 | Nền HD-2D mọi map, loài có animation từ atlas P10, sprite người/NPC, sprite HUD, hiển thị tiếng Việt | M2–M6 | ảnh | ☐ |
| F80–F81 | Provenance asset được giữ, token không ra URL/log | M2, M1 | unit | ☐ |

> HUD/menu: dựng lại bằng sprite APK (xem README → HUD / menu); màn Cường hóa hiển thị +N/10 theo luật server (cùng sao, tối đa 10).
