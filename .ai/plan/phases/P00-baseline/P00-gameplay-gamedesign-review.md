# P00 — Gameplay và game design review

Reviewer: Codex, 2026-09-23. Build identity: source restore archive + file changes + verification của P00, không có Git commit. Phương pháp: đọc active flow, automated real-server UI journey, native keyboard/click trên test account và xem screenshot; chưa có nhóm người chơi bên ngoài.

## Đầu phase

F01/F02: packet và renderer không cùng contract; private fixtures có thể pass nhưng live thiếu feedback. Auth/read có last events gây replay. Đồ họa POC; giữ tạo hình actor. Không có đo trước/sau về độ vui hoặc retention, không tuyên bố đã tối ưu balance.

## Trong phase

- Thử native: hai lần Right từ forest (9,10) vào combat snail, click Đánh rồi enemy; thấy lượt 2, HP enemy 26/33 và player 80/87 trong lần chơi này. Server action đi qua MySQL thật. Hai phía nhìn vào nhau; không thay source art.
- Live script: login/register, 4 hướng, NPC/shop/quest, portal, skill/item/defend/attack/capture/flee, reconnect/login/save. Kết quả và latency ở `evidence/live-reference.log`.
- Phát hiện peaceful-map `wild_spawns:null` tạo lỗi mỗi frame dù script cuối in PASS; normalize public content và bổ sung gate đọc diagnostics. Đây là bug runtime, không tuning game design.
- Phát hiện click NPC trong terminal animation mở panel sớm; thêm lock và regression. Mục tiêu: người chơi luôn thấy hành động cuối trước khi quay lại khám phá.
- Metrics cho thấy Apply nhanh nhưng durable DB roundtrips chậm trên dev topology. Chưa thể mô tả gameplay là không lag; thêm feedback/input pacing tiếp ở P02 cùng tối ưu persistence/deployment sau profile.

## Finding và quyết định

| ID | Loại / quyết định | Bằng chứng / phase sở hữu |
|---|---|---|
| F01/F02 | Chỉnh trong P00 | public WS test + active-room regression + live capture |
| P00-G01 | Chỉnh: auth/read/duplicate không replay | WebSocket integration + reconnect regression |
| P00-G02 | Chỉnh: terminal input/NPC lock | regression red→green, timer tự trả quyền điều khiển |
| P00-G03 | Chỉnh: nullable spawn content | red native diagnostics→green full live check |
| P00-G04 | Hoãn: rừng seam/layer, art POC | P01 map + P05 polish; giữ actor art direction |
| P00-G05 | Hoãn: DB/network làm chờ action | P02 cảm giác combat; P06/P09 topology/latency, phải đo lại |
| P00-G06 | Hoãn: đủ bộ loài/action và balance mới chơi | P02 actor matrix/P03 pet mapping/P04 clean-account pacing |

## Cuối phase

Kết luận cuối và blocker xem `P00-verification.md`; không đóng gate visual/live hiếm chỉ vì mock pass. Số đo FPS 120 frame là sample ngắn, không đủ chứng nhận gate 10 phút/50 actor. Report giữ/chỉnh/hoãn này phải được mang vào sprint tiếp theo.
