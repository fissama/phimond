# Kế hoạch triển khai: chuyển client game sang Three.js (v1.0, M0 được mở)

- **Ngày:** 2026-10-14. **Trạng thái:** DRAFT, đang debate với chủ dự án. Chưa được duyệt để viết code.
- **ADR liên quan:** [ADR-0001](../../../decisions/ADR-0001-threejs-web-client.md) (Proposed).
- **Mục tiêu:** port toàn bộ chức năng client Godot hiện tại sang Three.js (parity), rồi nhận P01 (world HD-2D, traversal, HUD/menu, cấu hình web) trên nền mới.
- **Ngoài phạm vi:** đổi luật game/server, đổi roster/stat/skill (P11/P13), party/PvP/shared world (P06/P07), âm thanh.

## 1. Quyết định đã chốt (chủ dự án, 2026-10-14)

| ID | Quyết định |
|---|---|
| T01 | Chọn Three.js cho client web. Bằng chứng iPhone/Safari vẫn phải thu trong lúc port (ADR-0001 §5). |
| T02 | App riêng `apps/game-web`: Vite + TypeScript strict. Không đặt trong Next.js (P01-R09). |
| T03 | Chiến lược: đóng băng giao thức, đạt parity rồi mới nâng P01. Godot giữ làm đối chứng đến gate parity. |
| T04 | UI (HUD, menu, UI chiến đấu) dựng bằng DOM, Preact + signals. Three chỉ vẽ world và sân khấu trận. Tái dùng `prototypes/p12-stage3/shared/hud/hud.js` làm điểm xuất phát. |
| T05 | Token phiên trong bộ nhớ trang, gửi qua `auth.session`. Cookie HttpOnly của `apps/web` giữ riêng. |
| T06 | ~~Backdrop 2D cũ~~ **Đổi (v0.2):** mọi map dựng qua pipeline HD-2D (`scene.json`) sớm, không dùng backdrop 2D cũ. Phạm vi "mọi map" và nguồn art: xem §9 câu hỏi Q2. |
| T08 | **Atlas P10 làm luôn** (không giữ sprite cũ 14 loài). Cần bảng ánh xạ legacy→P10: §9 Q1. |
| T09 | **Thêm allowlist CORS vào server** (Go, cấu hình bằng env, kèm test). Không đổi giao thức. |
| T10 | **Xóa client Godot sớm**, với điều kiện port hoàn chỉnh để không cần tham khảo lại: §9 Q3. |
| T07 | Chứng minh parity bằng: (a) port script check Godot sang Playwright, (b) bảng đối chiếu từng chức năng (§5), (c) ảnh chụp cùng trạng thái để so bằng mắt, (d) chủ dự án tự chơi route city→forest→city→ranch trên iPhone 17 Pro Max Safari + macOS Safari. |

## 2. Hiện trạng cần port (nguồn thật của parity)

Đường chạy chính: `LoginScreen.tscn` → `MainMap.tscn` → `reference_game.gd`. `main.gd` và `BattleScene.gd` là bản cũ (README: chỉ giữ để tham chiếu), không nằm trong phạm vi parity.

| Godot (nguồn) | Việc nó làm | Module mới |
|---|---|---|
| `PhimondClient.gd` (395 dòng) | HTTP register/login/content, WS, request_id, pending, timeout 15 s, dedup theo revision, chuẩn hóa events null/float | `net/` (api, socket, session) |
| `LoginScreen.gd` | Đăng nhập / đăng ký | `ui/screens/Login` |
| `reference_game.gd` (426) | Điều phối: input, đi, approach NPC/cổng, contact quái, lệnh Chọn/Trở về, menu, shop, skills, items | `game/` (controller, input, travel) + `ui/` |
| `room.gd` (438) | Vẽ world (nền, NPC, quái, người chơi, camera) và sân khấu trận (unit, hiệu ứng, hit area, HP) | `render/world`, `render/battle` |
| `classic_hud.gd` (243) | HUD cổ điển, thanh trận | `ui/hud` (từ `hud.js`) |
| `reference_menus.gd` (344) | Linh thú, Túi đồ, Nhiệm vụ, Lai tạo | `ui/menus/*` |
| `reference_art.gd` (120), `assets/extracted/*`, `assets/reference/*` | Cắt/trim sprite, spriteframes 14 loài, nền 5 map, NPC, HUD | `tools/build-web-assets` + `assets/` |
| 6 script check trong `tools/check_godot.mjs` | client_protocol, world_room, contact, reference_menus, battle_presentation, layout_audit | `tests/` (vitest + Playwright) |

Ghi chú về protocol (`packages/protocol/README.md`): server **đã có** Y (nhân vật, NPC, `height`, `wild_spawns {x,y}`) và `world.move` hỗ trợ `up/down`. Cổng và NPC vẫn xét theo `x` (F03 trong master spec), đó là việc của P01-R01, không phải của giai đoạn port.

## 3. Kiến trúc đích

```
apps/game-web/
  src/
    net/        api.ts  socket.ts  session.ts   // REST + WS, request_id, pending, reconnect
    state/      store.ts                         // signals: character, catalog, battle, ui
    game/       controller.ts input.ts travel.ts contact.ts  // luật phía client (không tính kết quả)
    render/     engine.ts world/ battle/ assets/ // Three: scene, camera, sprite, post
    ui/         hud/ menus/ screens/ components/ // Preact
    dev/        bench.ts panel.ts                // harness đo, chỉ bật khi ?dev=1
  tools/build-web-assets/                         // spriteframes/sheet -> atlas + manifest
  tests/unit/ tests/e2e/ tests/fixtures/
packages/protocol-ts/   // kiểu + schema (zod) + fixtures dùng chung game-web, web, test
```

Nguyên tắc:
1. **Server authoritative.** Client chỉ gửi intent và render. Không tính damage/RNG.
2. **Một luồng dữ liệu:** WS → `session` (dedup theo revision) → `store` → UI (signals) và `render` (đọc snapshot, không giữ state riêng).
3. **Hiệu ứng trận phát đúng một lần mỗi revision**, theo hợp đồng P00 (không dùng `event.seq` làm khóa toàn cục).
4. **Không tự retry intent không chắc kết quả**; retry chủ động phải dùng lại cùng `request_id`.
5. **Input state machine** gom bàn phím, D-pad, chạm, click-to-approach. Menu mở, mất focus hoặc vào trận thì dừng đi.
6. **Giữ cadence 0,18 s/bước** và preview/reconcile như `room.gd` trong giai đoạn parity. Nội suy mượt hơn để P01.
7. **Tài nguyên:** tải theo map và theo nhu cầu, cache LRU hữu hạn, dispose texture khi đổi map (bài học từ log: bản Three prototype rò rỉ texture bóng, đã sửa).
8. **Camera/HD-2D:** tái dùng cảnh vàng của prototype (billboard Y, tilt-shift, bloom, tier low/medium/high) nhưng giai đoạn parity chỉ cần tier mặc định ổn định.

## 4. Lộ trình (milestone)

Mỗi milestone kết thúc bằng bản chạy được trên server thật và danh sách test xanh. Theo AGENTS.md: sau mỗi milestone chạy lại source mới nhất để chủ dự án validate trước khi sang milestone kế.

| M | Nội dung | Exit criteria |
|---|---|---|
| **M0** Nền tảng ✔ (code xong 2026-10-14; còn chờ bạn chạy kiểm tra thật, xem README game-web) | ADR duyệt, scaffold `apps/game-web` (Vite, TS strict, ESLint, vitest, Playwright), `packages/protocol-ts`, thêm allowlist CORS vào server Go (env `GAME_CORS_ORIGINS`, preflight cho `Authorization`, `go test -race`), cấu hình `GAME_ALLOWED_ORIGINS` cho WS. Đóng băng bảng parity (§5). Mở rộng `tools/check.sh` (typecheck + vitest + build). | `npm run build` sạch; kết nối `/healthz` và WS auth từ trình duyệt thành công; server chỉ đổi phần CORS. |
| **M1** Lõi mạng | Port `PhimondClient`: register/login/logout, content, WS `auth.session`, `request_id`, pending/timeout 15 s, dedup theo revision, chuẩn hóa `events: null`, `wild_spawns: null`, ép số nguyên khi gửi, thông báo lỗi thân thiện, reconnect thủ công. | Port `client_protocol_check` thành vitest + fixtures; test live đăng ký/đăng nhập tài khoản dùng một lần. |
| **M2** Pipeline asset | `tools/build-web-assets`: sprite người chơi/NPC, HUD, **atlas P10 theo `species_id`** (20 frame/5 animation, khóa SHA-256, lazy load + LRU, không nạp cả 152), bảng ánh xạ legacy→P10, và **pipeline HD-2D cho mọi map** (`gen_scene` → `scene.json` + texture). | Manifest khớp `assets/reference/provenance.json`; xem được từng loài trong trang dev. |
| **M2b** Art HD-2D | Khung phong cách trên severa (chủ dự án duyệt), áp cho forest/beach/ranch/arena, dựng lại Emerald; chuẩn ở §11. | Cả 5 map được chủ dự án duyệt art. M4 chỉ nhận cảnh đã qua bước này. |
| **M3** Vỏ + HUD | Khung 960×640 co giãn, màn Login, HUD (Lv, pet, thanh HP/MP/XP, vàng/pha lê, menu phải, D-pad, Chọn/Trở về, chat 6 tab), Esc/back, safe area, xoay/resize. Port từ `hud.js`. | Port `layout_audit`; ảnh chụp HUD khớp Godot về bố cục. |
| **M4** World | Cảnh HD-2D cho mọi map server đang có (nạp theo map, dispose khi đổi), người chơi, NPC, quái hoang (`wild_spawns`), camera, bước đi + preview/reconcile, approach NPC/cổng, nút E, contact + latch rời vùng, đổi map, mất focus dừng đi. | Port `world_room_check` và `contact_check`; chạy được city→forest→city→ranch bằng phím/D-pad/click. |
| **M5** Menu | Menu chính, Bản đồ/Hành trình, NPC (quest/shop/heal/breed/arena), Cửa hàng, Linh thú (thuộc tính, kháng, kỹ năng, growth, đổi pet, giám định, học skill, thả có xác nhận, cường hóa), Nhiệm vụ, Túi đồ, Lai tạo (cha mẹ, công thức, phước, xác nhận), Lineage, menu kết nối. Điều hướng focus bằng D-pad. | Port `reference_menus_check`; mọi thao tác có xác nhận trước khi tiêu tài nguyên. |
| **M6** Trận đấu | Sân khấu trận (unit, vị trí, animation, hiệu ứng, số sát thương, HP/MP, trạng thái), thanh hành động (đánh/kỹ năng/vật phẩm/bắt/thủ/chạy/auto), chọn mục tiêu, phát event đúng một lần, win/loss rồi quay lại world, auto chờ ack, reconnect giữa trận không phát lại. | Port `battle_presentation_check`; trận 1v1 và 1v3 thật qua server. |
| **M7** Gate parity | Điền đủ bảng §5, ảnh chụp song song Godot/Three, harness đo giữ lại (`?dev=1`), chạy `tools/e2e_gameplay_full.mjs` và `tools/load_gameplay.mjs` không đổi. Chủ dự án chơi route trên iPhone + macOS Safari. | Mọi dòng bảng parity "xanh" hoặc "chấp nhận lệch" có chữ ký chủ dự án. |
| **M8** Cutover | Viết **sổ hành vi Godot** (§9 Q3) trước khi xóa; gắn tag + lưu tarball của `apps/game-client`; xóa `apps/game-client` và `tools/check_godot.mjs`; cập nhật `AGENTS.md`, README, `tools/check.sh`, ACTIVE.md. | Một lệnh khởi chạy game web; tài liệu khớp. |
| **P01+** | Sau parity, nhận P01-R01…R10: X/Y thống nhất (kể cả cổng/NPC theo Y), collision/walkable, nội suy mượt, asset lifecycle/preset, HUD Cài đặt → Đồ họa (Low/Medium/High, 30/60 FPS), spawn lifecycle, bằng chứng thiết bị. | Theo exit gate P01 trong master spec. |

## 5. Bảng parity (đóng băng ở M0, cập nhật trạng thái mỗi milestone)

Cột trạng thái: ☐ chưa làm · ◐ đang làm · ✔ xong + có test. Nguồn: README client + code Godot. Chat 6 tab hiện là placeholder ở Godot nên parity chỉ yêu cầu khung tab và log tin sản xuất tại chỗ, không yêu cầu chat thật.

| ID | Chức năng | Milestone | Test |
|---|---|---|---|
| F01–F04 | Đăng ký, đăng nhập, đăng xuất, thông báo lỗi thân thiện | M1 | unit + live |
| F05–F09 | WS auth, reconnect thủ công, timeout 15 s, khóa khi đang chờ, retry cùng request_id | M1 | unit + live |
| F10–F13 | Đi bằng phím (WASD/mũi tên, lên xuống), D-pad giữ lặp 0,18 s, tâm D-pad mở menu, preview/reconcile | M4 | e2e |
| F14–F15 | Camera bám người chơi, nền theo map | M4 | e2e + ảnh |
| F16–F18 | Click NPC để tới và nói chuyện, phím E (trong 3 ô), click cổng để tới và qua map | M4 | e2e |
| F19–F21 | Menu Hành trình, contact quái theo `spawn_id` có latch, encounter ngẫu nhiên cũ khi không có spawn | M4 | e2e |
| F22–F23 | Mất focus dừng đi, F3 hiện tọa độ/revision | M4 | e2e |
| F30–F33 | HUD: Lv, pet, thanh HP/MP/XP, vàng/pha lê, nút menu phải | M3 | layout + ảnh |
| F34–F37 | Chat 6 tab, Chọn/Trở về, Esc/back, thanh hành động trận | M3 | layout + ảnh |
| F40–F41 | Menu chính 3×2 (+ kết nối lại, đăng xuất, tiếp tục), menu NPC theo role | M5 | e2e |
| F42 | Cửa hàng mua vật phẩm | M5 | e2e |
| F43–F48 | Linh thú: xem chi tiết, giám định, đổi pet, học skill, thả (xác nhận), cường hóa | M5 | e2e |
| F49–F50 | Nhiệm vụ nhận/trả, Túi đồ dùng vật phẩm | M5 | e2e |
| F51–F53 | Lai tạo (công thức, phước, xác nhận), học công thức, xem Lineage | M5 | e2e |
| F54–F55 | Hồi phục pet, thách đấu arena | M5 | e2e |
| F56 | Điều hướng focus menu bằng D-pad + Chọn | M5 | e2e |
| F60–F64 | Vào trận khi contact, hành động trận, chọn mục tiêu, danh sách skill Cấp/MP, vật phẩm trận | M6 | e2e |
| F65–F69 | Event phát đúng một lần/revision, phản hồi sát thương/trạng thái, win/loss rồi quay lại world, auto chờ ack, reconnect giữa trận không phát lại | M6 | unit + e2e |
| F70–F74 | Nền HD-2D mọi map, loài có animation từ atlas P10, sprite người/NPC, sprite HUD, hiển thị tiếng Việt | M2–M6 | ảnh |
| F80–F81 | Provenance asset được giữ, token không ra URL/log | M2, M1 | unit |

## 6. Kiểm thử và bằng chứng

- **Unit (vitest):** giao thức, dedup revision, chuẩn hóa dữ liệu, input state machine, travel/contact.
- **E2E (Playwright, server thật, tài khoản dùng một lần):** port 6 script Godot; loại live nằm ngoài `tools/check.sh` offline, đúng như `reference_live_check`.
- **Ảnh chụp song song:** cùng trạng thái ở Godot và Three, chủ dự án xem cạnh nhau (không so pixel).
- **Đo hiệu năng:** giữ harness của prototype (`?dev=1`), bản sửa gồm: bot không qua cửa, `recentFrames`, mốc tải tính từ lúc điều hướng. Không đặt ngưỡng đạt/không đạt ở giai đoạn parity. Ngưỡng do P01 chốt sau khi có tier (đúng ghi nhận của chủ dự án).
- **Thiết bị:** iPhone 17 Pro Max Safari + macOS Safari. Mỗi tier chạy đủ 60 s, 3 lần, bỏ lần đầu.

## 7. Rủi ro và điểm cần debate tiếp

| # | Vấn đề | Quan điểm hiện tại của Claude | Phản biện có thể |
|---|---|---|---|
| R1 (đã chốt: làm luôn atlas P10) | Atlas pet P10 (152) so với sprite cũ 14 loài trong giai đoạn parity | Giữ sprite cũ cho parity, nhưng `ArtRegistry` định tuyến theo `species_id` để đổi sang atlas P10 không đụng code khác. | Làm routing atlas ngay vì Three loader đã có, tránh làm 14 loài hai lần. |
| R2 (đã làm ở M0) | CORS | `GAME_CORS_ORIGINS` (allowlist đầy đủ origin, mặc định tắt) + `GAME_ALLOWED_ORIGINS` cho WS | — |
| R3 | iOS Safari treo tab nền, WS bị cắt | Thiết kế reconnect + khôi phục snapshot ngay từ M1, test bằng giả lập mất kết nối. | Đợi thiết bị thật rồi mới làm. |
| R4 | Font tiếng Việt | Webfont có license rõ ràng, fallback hệ thống; chốt ở M3. | Dùng font hệ thống cho khỏi tải thêm. |
| R5 (đã chốt: HD-2D mọi map) | Nền ảnh 2D cũ trong cảnh Three trông phẳng, lệch với HD-2D | Chấp nhận trong parity, ghi rõ là tạm. | Dựng nhanh vài map bằng pipeline scene.json để người chơi thấy HD-2D sớm. |
| R6 | Texture/GPU trên iOS | Cache LRU, dispose khi đổi map, KTX2 là tối ưu hóa sau parity nếu số đo cần. | Làm KTX2 từ đầu vì Three hỗ trợ tốt. |
| R7 (đã chốt: xóa sớm) | Số phận `apps/game-client` sau cutover | Giữ nguyên + gắn tag đến khi chủ dự án duyệt xóa. | Xóa sớm để khỏi duy trì hai client. |
| R8 | Hosting bản build | Quyết định ở M0: Go phục vụ tĩnh hay CDN. | — |
| R9 | `AGENTS.md` lưu mật khẩu MySQL dạng rõ | Chủ dự án nên xoay mật khẩu và chuyển sang `.env` (đã báo trước đó). | — |

## 8. Việc cần chủ dự án duyệt tiếp

1. ADR-0001 (Proposed → Accepted).
2. Bảng parity §5 (thêm/bớt dòng).
3. Các điểm R1–R8.
4. Cho phép mở M0 (cần cấp quyền riêng theo quy ước dự án).

## 9. Hệ quả của các quyết định ngày 2026-10-14 (v0.2) và câu hỏi còn mở

**Hệ quả:**
- Parity không còn là "chơi lại y hệt bằng art cũ" mà là "đúng chức năng, art mới". Ảnh chụp song song Godot/Three (T07c) chỉ còn so bố cục và trạng thái, không so hình nền hay sprite.
- Parity phụ thuộc art: nếu một map hoặc loài chưa có art HD-2D/atlas thì milestone M4/M6 bị chặn. Cần danh sách rõ ràng ở M0.
- Thêm CORS là thay đổi server nhỏ, vẫn phải qua quy trình AGENTS.md (build, `go test -race`, `/healthz`, chạy lại để chủ dự án validate).
- Xóa Godot sớm làm mất khả năng "chạy bản cũ xem nó làm gì". Vì vậy cần sổ hành vi (Q3) và test Playwright thay thế vai trò đối chứng. Git giữ lịch sử và tag nên không mất mã.

**Q1 Ánh xạ legacy→P10.** Server chạy 14 loài cũ (snail, flower_fairy, mushroom, dark_crab, wealth_turtle, treasure_chest, sea_demon, spider, wolf, windmill_spirit, grove_guardian, tide_sentinel, moon_warden, dawn_sovereign). `data/p10/id_registry.json` dùng ID `species_0001…0152` theo tên APK và **không có** ánh xạ nào tới 14 ID cũ. Theo ACTIVE.md, 4 loài chưa có art. Cần: bảng ánh xạ 14→P10 do chủ dự án duyệt, và quyết định cho loài không khớp (giữ placeholder, hoặc gắn tạm một loài P10 khác chỉ để hiển thị).

**Q2 "Mọi map" nghĩa là gì.** Server hiện có 5 map (severa, forest, beach, ranch, arena). P12 có 92 map (35 đã duyệt nguồn). Cần chốt: (a) 5 map server hiện có, mỗi map gán một cảnh HD-2D đã/đang vẽ trong P12; hay (b) cả 35 map đã duyệt, kéo theo thay đổi catalog server (ngoài đóng băng giao thức). Kèm theo: nguồn art cho severa/ranch/arena, vì Emerald là map APK còn ba map này là bản dựng riêng của Phimond.

**Q3 Điều kiện "không cần tham khảo lại Godot".** Đề xuất: (1) sổ hành vi Godot liệt kê từng quy tắc ngầm (cadence 0,18 s, latch contact, thứ tự ưu tiên Esc/back, xử lý focus, thông điệp lỗi, kích thước UI, thứ tự phát event) kèm test tương ứng; (2) mọi dòng parity có test Playwright hoặc vitest; (3) bạn ký gate M7; (4) tag `godot-client-final` và tarball lưu trữ; (5) rồi mới xóa ở M8.

## 10. Chốt Q1–Q3 (2026-10-14) và bảng đề xuất chờ duyệt

**Đã chốt:** (Q1) Claude đề xuất ánh xạ loài theo tên/hình, chủ dự án duyệt, loài không khớp dùng tạm loài P10 gần nhất; (Q2) "mọi map" = 5 map server hiện có, mỗi map gán một cảnh HD-2D; (Q3) đồng ý 5 điều kiện trước khi xóa Godot.

### 10.1 Ánh xạ 14 loài cũ → species P10 (ĐỀ XUẤT)

10 loài có tên actor APK khớp chính xác `id_registry.json` (nguồn: `assets/reference/provenance.json`):

| ID cũ | Actor APK | species P10 |
|---|---|---|
| snail | OcSenHoa | species_0111 |
| flower_fairy | YeuTinhHoa | species_0022 |
| mushroom | NamHoa | species_0023 |
| spider | NhenDoc | species_0112 |
| wolf | SoiNgoNgan | species_0074 |
| dark_crab | CuaHacAm | species_0003 |
| wealth_turtle | RuaPhuQuy | species_0073 |
| treasure_chest | QuaiVatRuongBau | species_0127 |
| sea_demon | TieuAcMa | species_0053 |
| windmill_spirit | ChongChongGio | species_0128 |

4 loài còn lại là nội dung gốc Phimond. **Chủ dự án chốt (2026-10-14): dùng art của 4 loài P10 sau, đúng với 4 sprite Godot đang mượn tạm:**

| ID cũ (server) | Art hiển thị | species P10 |
|---|---|---|
| grove_guardian | Xích Linh Chi (1★, thực vật) | species_0023 |
| tide_sentinel | Bảo Tương Yêu (1★, linh thể) | species_0127 |
| moon_warden | Hắc Giải (1★, linh thể) | species_0003 |
| dawn_sovereign | Phong Xa Linh (1★, linh thể) | species_0128 |

Đây là ánh xạ **art hiển thị**; client không đổi Sao/Race/stat của server (server vẫn ghi 2★–5★). Bốn dòng này gắn `art_pending: true` để chủ dự án thay art riêng sau; thay bằng cách sửa một dòng trong `legacy-species-map.json`. Lưu ý: mỗi loài trong 4 loài này dùng chung sprite với một loài khác (mushroom, treasure_chest, dark_crab, windmill_spirit), nên người chơi sẽ thấy hai loài giống hệt nhau cho đến khi có art riêng.

### 10.2 Gán 5 map server → cảnh HD-2D (ĐỀ XUẤT)

`provenance.json` cho biết 5 nền cũ đều lấy từ APK, và mỗi nền trùng một map trong bảng tên P12:

| Map server | Nền APK hiện dùng | Cảnh HD-2D đề xuất (ID P12) | Tình trạng art |
|---|---|---|---|
| severa | level3_QTTP | `city_square` — Quảng Trường Thạch Trụ | chưa dựng; cần chạy pipeline |
| forest | level4_Map2 | `emerald_forest_main_woods` — Bìa Rừng Lục Bảo | **đã có** (cảnh vàng Stage 3) |
| beach | level5_BaiBien | `treasure_beach_fishermen_beach` — Bến Ngư Châu | chưa dựng |
| ranch | level3_NongTrai | `city_farm` — Điền Trang Lục Dã | chưa dựng |
| arena | level3_DauTruong | `city_deathmatch_arena` — Huyết Chiến Đài | chưa dựng |

Ghi chú: ID server (severa, forest…) giữ nguyên, vì đóng băng giao thức. Phần ánh xạ nằm ở dữ liệu client. `emerald_forest_deep_woods` dùng cho Trụ dịch chuyển/vùng sâu sau này. Lưới 40×24 của server được đặt lên cảnh HD-2D bằng hệ số tỷ lệ riêng từng map (P01-R01 sẽ thay bằng tọa độ thống nhất). Walkable/collision mới do P01 dựng, parity dùng bounds của server.

### 10.3 Điều kiện trước khi xóa `apps/game-client` (đã đồng ý)

1. Sổ hành vi Godot (cadence 0,18 s, latch contact, thứ tự Esc/back, focus, thông điệp lỗi, kích thước UI, thứ tự phát event), mỗi dòng trỏ tới test.
2. Mọi dòng bảng parity §5 có test vitest hoặc Playwright.
3. Chủ dự án ký gate M7.
4. Tag `godot-client-final` và bản lưu trữ `.tar.gz` ngoài cây mã nguồn.
5. Xóa `apps/game-client` và `tools/check_godot.mjs` ở M8, cập nhật `tools/check.sh`.

### 10.4 Việc còn chờ chủ dự án

- ~~Duyệt bảng 10.1 và 10.2~~ Đã duyệt (2026-10-14).
- Xác nhận việc dựng 4 cảnh mới (city_square, treasure_beach_fishermen_beach, city_farm, city_deathmatch_arena) bằng pipeline `gen_scene` từ nguồn APK là hướng "vẽ lại HD-2D" bạn muốn, hay bạn sẽ cung cấp art vẽ tay.
- Duyệt ADR-0001 và cấp quyền mở M0.

## 11. Cập nhật 2026-10-14 (v1.0)

- **ADR-0001 Accepted; M0 được mở.**
- **Chuẩn art 5 map nâng lên:** bản Emerald của Stage 3 bị đánh giá là tạm bợ, chưa hợp một game 2026. Cả 5 map phải vẽ lại hoàn thiện hơn. Thêm milestone **M2b — Art HD-2D**: (1) chốt "khung phong cách" trên một map (severa) và chủ dự án duyệt; (2) áp cho 4 map còn lại và dựng lại Emerald; (3) mỗi map qua review của chủ dự án. Chuẩn cần đạt gồm: nhiều lớp chiều sâu thật, ánh sáng/bóng và tông màu thống nhất, vật thể trang trí có chủ đích thay vì rải ngẫu nhiên, nước và cây có chuyển động, không còn mép cắt cứng. M4 chỉ nhận cảnh sau khi qua M2b. Giới hạn cần nói rõ: nguồn là sprite APK, nên chất lượng tối đa phụ thuộc vào chúng; nếu khung phong cách vẫn chưa đạt, hai hướng tiếp theo là art do chủ dự án cung cấp hoặc dựng thêm bằng công cụ khác.
- **4 loài:** xem §10.1 (đã chốt).
