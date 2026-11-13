# P01 — Scope và lộ trình phiên bản (v1.0.0 → v1.2.x)

- **Ngày:** 2026-10-21. **Trạng thái:** owner đã chốt hướng và §7 trong chat 2026-10-21; sẵn sàng viết code. Kế hoạch triển khai: [`P01-implement-plan.md`](P01-implement-plan.md).
- **Nguồn:** master spec §6 P01 (P01-R01…R10), P12 (đã đóng 2026-10-17), duyệt art [`hd2d-art-approval-20261021.md`](../../../design/hd2d-art-approval-20261021.md).
- Thay thế phần lộ trình M0–M8 của [`P01-threejs-migration-plan.md`](P01-threejs-migration-plan.md): `apps/game-web` chỉ là bản thử Three.js, không dùng tiếp (xem §3).

## 1. Quy ước version

`X.Y.Z`. Mỗi **đợt map** tăng `Y`; `Z` là thay đổi nhỏ (sửa lỗi, thay art, trả nợ kỹ thuật). `1.0.0` là bản chơi được đầu tiên.

| Version | Nội dung | Ghi chú |
|---|---|---|
| **1.0.0** | **Đợt A** — tuyến người chơi mới, 5 map (§2) + toàn bộ nền P01 | Mốc đầu tiên |
| 1.0.z | Thay art vẽ lại, sửa lỗi playtest, NPC idle | Không thêm map |
| 1.1.0 | **Đợt B1 — Thành:** Thương Phố, Vương Cung, Vạn Sự Hội Sảnh, Điền Trang Lục Dã (riêng từng người), Phòng thú cưng (riêng từng người), Huyết Chiến Đài (chỉ cảnh + lối vào, xem nợ N01) | Trụ Quảng Trường thêm Điền Trang |
| 1.2.0 | **Đợt B2 — Bãi biển:** Bến Ngư Châu, Bờ Đông Ngọc Bích, Bờ Tây Hoàng Sa, Vực Hải Lam, Đảo Phú Quý | Trụ Quảng Trường thêm Bờ Đông. **P01 exit review** ở bản này |
| 1.2.z | Trả nợ khi phase sở hữu xong (vd N02 sau P15) | |

Không thuộc 1.x của P01: Hải Tặc Hào, Sa Mạc, Mỏm Đá Gió, Lăng Mộ, Đảo Ác Mộng, Giao Điểm, 6 vùng Lv40+, vùng nhiều tầng, Bang hội, Sói–Cừu.

## 2. Đợt A (v1.0.0)

| Map (ID P12) | Tên | Loại | Cấp |
|---|---|---|---|
| `summoning_hall_main_hall` | Triệu Linh Điện | transit_once | — |
| `emerald_forest_main_woods` | Bìa Rừng Lục Bảo | mixed (không safe zone) | 1–5 |
| `emerald_forest_deep_woods` | Rừng Sâu Lục Bảo | field | 5–10 |
| `city_palace_gate` | Hoàng Môn | safe_hub | — |
| `city_square` | Quảng Trường Thạch Trụ | safe_hub | — |

**Đồ thị trong 1.0.0** (theo `stage4/portal-matrix.json`):
Triệu Linh Điện → Bìa Rừng (một chiều) · Bìa Rừng ↔ Rừng Sâu · Rừng Sâu → Hoàng Môn (lần đầu theo cờ nhiệm vụ), các lần sau → Quảng Trường · Hoàng Môn ↔ Quảng Trường · Trụ Quảng Trường → Bìa Rừng.
Cổng sang map chưa mở (Thương Phố, Vương Cung) và đích trụ chưa mở (Bờ Đông, Điền Trang) **hiện nhưng khóa**, có thông báo "chưa mở" — không có cổng cụt.
Hồi sinh/kẹt: Bìa Rừng và Rừng Sâu → Bìa Rừng; Hoàng Môn và Quảng Trường → Quảng Trường (theo registry P12).

## 3. Client mới

- Viết lại client từ đầu (đề xuất thư mục `apps/client`), Three.js + Vite + TypeScript, DOM UI Preact + signals (giữ các quyết định ADR-0001 và 2026-10-14).
- **Giữ gameplay**, không giữ code: server Go (`apps/game-server`) vẫn là nguồn luật chơi; hành vi tham chiếu là bảng parity `apps/game-web/PARITY.md` và client Godot. Được đọc `apps/game-web` để tham khảo, không copy nguyên khối.
- `apps/game-web` và `apps/game-client` giữ tới khi client mới chạy được Đợt A, sau đó gắn tag lưu trữ rồi xóa (owner duyệt lúc đó).

## 4. Phạm vi kỹ thuật v1.0.0 (theo yêu cầu P01)

| Hạng mục | Làm trong 1.0.0 | Yêu cầu |
|---|---|---|
| Dữ liệu world | 5 map Đợt A vào server theo ID P12, kích thước/bounds mới, cổng/trụ/khóa theo §2, người chơi mới bắt đầu ở Triệu Linh Điện | R01, R04 |
| Tọa độ | Một hệ X/Y chung cho map, renderer, NPC, cổng, spawn; khoảng cách tương tác xét cả hai trục; xuất hiện cách cổng ~1 đơn vị, không kích hoạt lại cổng | R01, R04 |
| Va chạm | Walkable/collision mới cho từng map theo bố cục HD-2D (không khôi phục bản gốc) | R02 |
| Di chuyển | Phím, D-pad, chạm/click đi tới đích theo đường hợp lệ; menu/mất focus/vào trận thì dừng | R03 |
| Cảnh HD-2D | 5 cảnh dựng từ kit đã duyệt; camera, bóng, layer; tải/giải phóng theo map | R07, R08 |
| HUD/menu | Bố cục HUD gốc (Lv + pet trái trên, menu phải, D-pad trái dưới, Chọn/Trở về phải dưới, chat 6 tab giữa dưới); back/focus/safe area/xoay màn hình | R09 |
| Cài đặt đồ họa | Low/Medium/High + giới hạn 30/60 FPS, lưu lựa chọn, đo được mức Low thực sự nhẹ hơn | R10 |
| Quái | Spawn theo kế hoạch P12; contact → trận đấu hiện có của server; thắng/thua/bắt/chạy, cooldown, hồi sinh, reconnect. Loài: 14 loài cũ hiển thị bằng atlas P10 (nợ N02) | R05 |
| NPC | Hiện đủ NPC roster Đợt A; hội thoại; chức năng đã có ở server (hồi phục, cửa hàng, học skill) chạy được; chức năng chưa có báo "chưa mở" (nợ N04) | R04 |
| Đo và review | iPhone 17 Pro Max Safari + macOS Safari; review cảm giác di chuyển, mật độ quái, thao tác hụt, kẹt | R06, R08 |

## 5. Art cho Đợt A

Chi tiết ở [`hd2d-art-approval-20261021.md`](../../../design/hd2d-art-approval-20261021.md) §3. Tóm tắt: **dựng được cả 5 map ngay**; 4 nhóm cần GPT vẽ lại trước khi phát hành 1.0.0, dùng placeholder trong lúc chờ. Đơn hàng: [`gpt-redo/09-v1.0.0-full-redo-prompt.md`](../../../design/gpt-redo/09-v1.0.0-full-redo-prompt.md) (chặng 1–5 chặn 1.0.0).

## 6. Sổ nợ (làm sau, có chủ)

*Cập nhật 2026-11-13 khi đóng P01: thêm N07–N16 (xem [`P01-closure.md`](P01-closure.md)).*

| ID | Nợ | Làm khi |
|---|---|---|
| N01 | Huyết Chiến Đài: chỉ có cảnh + lối vào tạm (NPC Quảng Trường dịch chuyển vào); chưa có lịch sự kiện hằng ngày, điều kiện, phần thưởng | Phase nhiệm vụ/arena |
| N02 | Quái dùng 14 loài cũ; làm lại danh tính quái theo map | Sau P15, một bản `.z` |
| N03 | Chọn pet ở Triệu Linh Điện: bản tối giản trong 1.0.0 (§7 câu 1), trải nghiệm đầy đủ thuộc P04 | P04 |
| N04 | NPC chưa có chức năng server (đổi vật phẩm, kho, hòm thư, hội) chỉ báo "chưa mở" | P19 / phase social |
| N05 | Art vẽ lại ngoài Đợt A (tile thành/nông trại/đấu trường/biển, nền xa, NPC trùng còn lại) | Trước 1.1.0 / 1.2.0 — **B1 xong ở 1.1.0**; còn Bãi biển (N16) |
| N06 | Rừng Sâu dùng chung kit Bìa Rừng (tối hơn bằng ánh sáng); bộ "rừng sâu" riêng | 1.0.z |
| N07 | **R10:** chưa chứng minh Low nhẹ hơn High bằng đo (mục tiêu đề xuất: texture giảm ≥40%, thời gian GPU/khung giảm ≥30% cùng cảnh; chốt số sau lần đo đầu) | P05-R07/R08, trước P06 |
| N08 | **R08:** chưa có chế độ `?bench=`, chưa đo frame time p95/p99 (60 và 30 FPS), tải lần đầu, đổi map (≤1,5 s), bộ nhớ (JS heap / texture / không đo được), phiên 20 phút, rò tài nguyên khi lặp portal/đổi preset; chưa có budget theo thiết bị | P05, gate P09; làm trước khi cảnh đông ở P06 |
| N09 | Chưa chạy thật trên iPhone 17 Pro Max Safari, macOS Safari, macOS Chrome cho `apps/client`; chưa lập bảng thiết bị đạt/chưa đạt; Android | P05 |
| N10 | Chưa có test plan QA thủ công có kết quả (`qa/`), chưa có review R06 cuối có số đo (thao tác hụt, kẹt, encounter ngoài ý muốn, thời gian đi trọn tuyến) | P05-R05/R06 |
| N11 | E2E: chưa chạy WebKit + iPhone giả lập (đã cấu hình); chưa có e2e reconnect giữa trận; chưa có test throttle RTT 50/150/300 ms; chưa so ảnh 5 cảnh × 3 preset | P05 |
| N12 | Tải server: profile `p01-route` 10 CCU (+50 CCU để đo), "không tệ hơn P00" | P06 |
| N13 | Hạ tầng thật: test `fault_mysql` với MySQL thật; WS idle ≥ 3 phút qua ingress prod; sao lưu MySQL và theo dõi log; nợ UI nhỏ (D-pad che chat, icon thẻ khởi đầu, nút đăng nhập mobile) | Bản 1.1.z / P09 |
| N14 | Dọn client cũ: `apps/game-web` và `apps/game-client` chưa xóa. `apps/game-web/art-src` là nguồn art (hơn 800 file, GPT/Codex còn ghi vào) và ≥ 14 script trong `tools/` tham chiếu; `apps/game-client/assets/pets/apk84` là asset APK gốc. Cần chuyển nguồn art/asset sang chỗ riêng, đặt tag lưu trữ `archive/game-web-final`, `archive/game-client-final`, cập nhật `AGENTS.md` (thay smoke Godot), rồi mới xóa | Sau khi owner ký, một việc riêng |
| N15 | Art B1 còn nợ: Điền Trang 1 hàng ruộng (rìa rừng che), nhà rơm mờ khi đứng gần, sàn Vương Cung nhạt, `palace-throne-dais` và `farm-soil-edge-01/02` chưa dùng, glow ở Hội Sảnh, NPC chưa có idle | Bản 1.1.z |
| N16 | Đợt B2 — Bãi biển (Bến Ngư Châu, Bờ Đông Ngọc Bích, Bờ Tây Hoàng Sa, Vực Hải Lam, Đảo Phú Quý), trụ Quảng Trường thêm Bờ Đông | Cập nhật nội dung sau (owner chốt 2026-11-05) |

## 7. Owner đã chốt (2026-10-21)

1. **Người chơi mới ở Triệu Linh Điện:** phương án (a) — bấm 1 trong 3 bệ đá → xác nhận → nhận pet → dịch chuyển một chiều tới Bìa Rừng. Server vẫn chạy 14 loài cũ, nên 3 pet khởi đầu Tiên Chưởng / Sa Hạt / Xích Ưng tạm gắn với 3 loài cũ gần nhất cho tới N02. Trải nghiệm đầy đủ (hội thoại Mira, giới thiệu) thuộc P04 (N03).
2. **Client mới:** thư mục `apps/client`.

## 8. Owner đã chốt (2026-11-05) — đóng P01 ở v1.1.0

1. v1.0.0 (Đợt A, 5 map) đã golive tại `play.philand.io.vn`. **P01 đóng ở v1.1.0** (Đợt B1: thành/nông trại/đấu trường). Đợt B2 (Bãi biển, trước là 1.2.0) chuyển thành **bản cập nhật nội dung sau**, không chặn đóng P01.
2. Giữa 1.0.0 và 1.1.0 chỉ ra bản `1.0.z` ổn định hoá: kiểm thử WS idle ≥ 3 phút (thêm ping nếu rớt), đo trên thiết bị thật (iPhone/Safari), sửa bộ tách câu lệnh migration trong `bootstrap.go` (KHÔNG sửa file migration 003 vì checksum đã nằm trong DB prod), sao lưu MySQL và theo dõi log, nợ UI nhỏ (D-pad che chat, icon thẻ khởi đầu, nút đăng nhập mobile).
3. Có người chơi thật: mọi thay đổi `characters.state` từ nay phải có migration/tương thích ngược (D31 không còn chấp nhận được).
4. P19 (vật phẩm, thư) bắt đầu song song; xem [`../P19-items/P19-scope.md`](../P19-items/P19-scope.md).
