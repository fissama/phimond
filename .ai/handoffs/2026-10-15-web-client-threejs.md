# Handoff

- **Date**: 2026-10-15
- **Agent**: Claude (Sonnet 5.5), session claude.ai/code `session_01Pjz8cNUYLtRnHs73S3F3SJ`
- **Commit / working tree state**: xem `git log` — các commit "web:" của ngày này; cây làm việc còn nhiều thay đổi P10–P13 không thuộc handoff này (không đụng tới)
- **Related phase**: P01-world (port client Godot → Three.js, ADR-0001) + P12 Stage 3
- **Related sprint**: P01 M0–M6 (web client)

## Goal

Dựng lại client game trên web (`apps/game-web`: Three.js HD-2D + Preact signals, UI bằng DOM) khớp HUD APK gốc nhưng hiện đại, nói chuyện với server Go qua giao thức đã đóng băng. Có chế độ demo chạy engine Go trong trình duyệt (wasm) để chủ dự án thử trên iPhone 17 Pro Max Safari, macOS Safari, Edge mà không cần server.

## Completed

- [x] Client `apps/game-web`: đăng nhập/đăng ký, thế giới 5 map (Severa, Bìa Rừng Lục Bảo, Bãi biển, Nông trại, Đấu trường), NPC, cổng dịch chuyển, contact quái theo `spawn_id`, trận đấu, menu (linh thú, túi đồ, nhiệm vụ, lai tạo, cường hóa, cửa hàng, arena), i18n tiếng Việt.
- [x] Renderer HD-2D (`src/render/*`), scene sinh bởi `tools/build-web-assets/build_scenes.py` → `public/scenes/*.json` + `tex/`.
- [x] Server: CORS (`transport/cors.go`), `cmd/devserver` (kho RAM), `cmd/wasmdemo` + `transport/local.go` (engine chạy trong trình duyệt), `tools/build-wasm-demo.sh`.
- [x] Giao thức TS: `packages/protocol-ts`.
- [x] Map rộng 40→60 ô, mỗi bên thêm 10 ô, giữ nguyên vị trí cột mốc (cổng/NPC dời theo). Quái đi tuần quanh tổ (`Wild`/`wander` trong `stage.ts`), phát hiện người chơi ~4,2 đơn vị thì quay về tổ.
- [x] Biên chuyển cảnh liền mạch, bỏ sprite hình khối ở Nông trại (dùng tường cây của rừng).
- [x] Nút nền nghiêng (`button_confirm.png`/`button_back.png`, viên thuốc ~37°): chữ bọc `<span class="rt">` xoay `-37deg` (`styles.css`).
- [x] Nhãn tên/HP quái trong trận hạ sát đầu, chặn `y ≥ 96` để không đè tiêu đề bản đồ.
- [x] Tên linh thú qua `tn()` (map tên gốc server → tên Việt); biệt danh người chơi không bị đổi.
- [x] Bản demo đã xuất bản dạng claude.ai artifact (Version 7): https://claude.ai/artifact/DnnroqgMxB4xAoHjuQXQjy (riêng tư, chủ sở hữu mở được).

## Current state

- Dev: `cd apps/game-web && npm ci && npm run dev` (thêm `?local=1` để dùng wasm, sau `tools/build-wasm-demo.sh`). Chi tiết ở `apps/game-web/README.md`.
- Chất lượng đồ họa `?q=low|medium|high`, đo hiệu năng `?bench=1` (kết quả ở `window.__bench`).
- `public/engine/engine.wasm` bị gitignore; sinh lại bằng `tools/build-wasm-demo.sh` (nhúng `data/`).
- Quy tắc đã ghi vào mã: encounter cần người chơi trong 1 ô quanh tổ (`apply.go`); NPC trong 3 ô; cổng |dx|≤2. Cổng: Severa x=43 (spawn 1 vào rừng/nông trại/arena); rừng cổng thành x0→Severa spawn 48, cổng biển x59→biển spawn 1; biển x0→rừng spawn 58; nông trại và arena x0→Severa spawn 48. Mọi NPC ở x=19; spawn mặc định nhân vật x=16.
- Tên map dùng tên Việt đã duyệt, KHÔNG dùng tên từ APK/JAR.

## Partial / uncommitted work

- Cây làm việc còn thay đổi P10–P13, Godot (`apps/game-client`), `prototypes/`, `Claude outputs/`, `.serena/` — của các phiên khác, handoff này không đụng.
- `apps/game-web/PARITY.md` vẫn ghi toàn bộ ☐ (chưa cập nhật trạng thái) và `README` chưa nhắc các thay đổi mới.

## Decisions already made

- Three.js thay Godot (ADR-0001, `.ai/decisions/ADR-0001-threejs-web-client.md`). Giao thức đóng băng, không đổi.
- Godot client chỉ xóa ở M8 (cần chủ dự án duyệt).
- Không commit bí mật. Không dùng tên map từ APK/JAR.
- HUD dựng từ sprite APK nhưng hiện đại hóa; bố cục tham chiếu video gốc.

## Do not redo

- Đừng thu hẹp map về 40 ô hay dời lại NPC/cổng — đã căn lại cho 60 ô; đổi một thì phải sửa `maps.json`, `npcs.json`, `content.go`, test (vị trí cứng trong `character_test.go`, `battle_test.go`, `contact_test.go`, `transport/live_test.go`, `controller.test.ts`) và chạy lại `build_scenes.py`.
- Đừng thêm sprite khối cứng vào tường Nông trại.
- Đừng xoay chữ bằng ảnh nút; dùng `.rt`.

## Remaining work

- [ ] Nhãn linh thú phe mình trong trận ở màn điện thoại hơi chạm khung HUD góc trên trái.
- [ ] Chữ ô túi đồ quá nhỏ; dải gợi ý đôi khi chồng nhãn NPC; màn đăng nhập hở lớn giữa ô tích và nút.
- [ ] Chạy trọn một trận đến màn kết quả (cần chạm mục tiêu địch) và kiểm tra khung 844×390 và dọc.
- [ ] Chủ dự án thử lại Arena (hộp đen), đo `?bench=1` trên iPhone thật.
- [ ] Nhân vật đã lưu bị lệch 10 ô sau khi mở rộng map (cần migrate hoặc bỏ qua).
- [ ] Godot client vẫn đọc `maps.json` cũ; `README`/`PARITY.md` chưa cập nhật; M8.
- [ ] Chủ dự án duyệt 4 tên Việt cho loài tiến hóa; xóa artifact cũ "Phimond Emerald Bench" (JysCQbKLmCm53SnTgeWJzR) chỉ khi chủ nói "xóa"; đổi mật khẩu MySQL trong AGENTS.md.

## Verification already performed

- `tsc --noEmit` sạch; vitest và Go tests cập nhật theo vị trí mới (đã sửa các giá trị cứng).
- Playwright (Chromium SwiftShader) trên sandbox: ảnh chụp trận đấu 932×430 và 1280×720, các màn đăng nhập/menu/túi đồ, đi qua các cổng. GPU sandbox là SwiftShader nên số hiệu năng không có giá trị tuyệt đối.
- Chưa chạy lại toàn bộ `tools/check.sh` trong lần commit này.

## Known failures

- Chuyển map trong chế độ wasm chỉ ~40 ms nên lớp phủ đen `.mapcover` thường không hiện; chưa tái hiện được "lộ nền xanh" chủ dự án báo — nếu còn, cần ảnh chụp.
- Publish artifact: phải `read` các file khác nhau trước khi đăng lại; `build_art.sh` (sandbox) dựng `art/` và danh sách file.

## Relevant files

- `apps/game-web/src/render/stage.ts` (cảnh, quái đi tuần, nhãn trận ~dòng 396–412), `src/ui/App.tsx`, `src/ui/Menus.tsx`, `src/ui/styles.css` (`.rt`), `src/game/controller.ts`, `src/i18n.ts` (`tn`).
- `tools/build-web-assets/build_scenes.py`, `data/maps/maps.json`, `data/npcs/npcs.json`.
- `apps/game-server/internal/transport/{cors,local,server}.go`, `cmd/devserver`, `cmd/wasmdemo`, `internal/content/content.go`, `internal/character/engine.go`.
- `.ai/plan/phases/P01-world/P01-threejs-migration-plan.md`, `apps/game-web/PARITY.md`.

## Recommended next action

Chạy `npm ci && npm run dev` rồi `tools/check.sh`, xử lý các mục "Remaining work" về giao diện điện thoại, rồi cập nhật `PARITY.md` theo thực tế.
