# Cấu trúc repo Phimond

Cập nhật 2026-11-16 (dọn cấu trúc sau khi đóng P01). Nguyên tắc: **thư mục `apps/` và `data/` chỉ chứa thứ chạy thật; mọi thứ về art nằm trong `art/`; công cụ trong `tools/`; tài liệu trong `docs/` và `.ai/`.**

## Sơ đồ

```
phimond/
├─ apps/
│  ├─ client/          Client web (Vite + TS + Three.js + Preact) — client duy nhất
│  ├─ game-server/     Server Go (luật chơi, map, NPC, trận đấu, MySQL, REST/WS)
│  └─ web/             Trang đồng hành Next.js (bách khoa, công thức, nhật ký)
├─ data/               Catalog chạy thật (map p01, NPC, loài, kỹ năng, vật phẩm)
├─ migrations/         Schema MySQL có version
├─ packages/           Giao thức (protocol, protocol-ts)
├─ deploy/             Docker + manifest homelab (web, homelab)
├─ infra/compose.yml   Chạy server Go với MySQL cấu hình sẵn (tùy chọn)
├─ art/                Kho art nguồn (xem bên dưới)
├─ tools/              Dựng map (p01), cài art, kiểm tra content/art, tải thử
├─ docs/               Kiến trúc, DB, gameplay, nghiên cứu, báo cáo, legacy
└─ .ai/                Master plan, spec phase, đơn đặt art, review
```

## `art/`

| Thư mục | Nội dung | Git |
|---|---|---|
| `art/src/hd2d/<batch>/` | Nguồn art HD-2D theo đợt GPT/Codex: ảnh `final.png`, `manifest.json`, prompt, QA, ảnh giao (`delivery/`, `redo/`) | Chỉ ảnh final/giao + json/md/py. Ảnh trung gian (`raw`, `jobs/`, attempt, contact sheet, crop) **nằm trên đĩa, git bỏ qua** |
| `art/pets/` | `redraws/` (nhiều attempt của 160 loài), `apk84/` (ảnh APK gốc 152 loài) | Chỉ 160 atlas đã duyệt (`owner-atlas-selection-160.json`, 122 MB) + `apk84` + json/md. Attempt khác bỏ qua |
| `art/reference/` | Ảnh tham chiếu UI/HUD từ APK | Theo dõi |
| `art/runtime-src/` | Nguồn dựng asset client mới: `pets/`, `ui/`, `login/`, `actors/`, `i18n/vi.json` (đầu vào của `tools/p01/sync_client_assets.py`) | Theo dõi |
| `art/apk-extracted/` | Ảnh trích từ APK (dựng lại được từ file APK gốc) | Bỏ qua |
| `art/build/` | Cảnh thử/kết quả dựng (`scenes/`) | Bỏ qua |

Quy tắc ignore nằm ở `art/.gitignore` và `art/pets/.gitignore`.

**QUAN TRỌNG — backup:** ảnh trung gian (khoảng 11 GB) chỉ có trên máy bạn, không có trên GitHub. Hãy backup thư mục `art/` (Time Machine hoặc ổ ngoài). Muốn một file trung gian được theo dõi thì thêm quy tắc `!` vào `art/.gitignore`.

**Cổng art** (`sh tools/check_hd2d_art.sh`) cần ảnh trung gian như contact sheet, nên chỉ chạy được ở máy có đủ `art/` (không chạy được trên bản clone mới).

## Bản đồ đường dẫn cũ → mới

Tài liệu cũ trong `.ai/` và `docs/` vẫn ghi đường dẫn cũ (bằng chứng lịch sử, không sửa). Quy đổi:

| Cũ | Mới |
|---|---|
| `apps/game-web/art-src/...` | `art/src/...` |
| `apps/game-client/assets/pets/redraws/...` | `art/pets/redraws/...` |
| `apps/game-client/assets/pets/apk84/...` | `art/pets/apk84/...` |
| `apps/game-client/assets/reference/...` | `art/reference/...` |
| `apps/game-client/assets/extracted/...` | `art/apk-extracted/...` |
| `apps/game-web/public/assets/...` | `art/runtime-src/...` |
| `apps/game-web/public/scenes/...` | `art/build/scenes/...` |
| `apps/game-web/PARITY.md` | `docs/legacy/game-web-PARITY.md` |
| `tools/check_godot.mjs`, `tools/build-wasm-demo.sh` | đã xóa |

Manifest máy đọc (`owner-atlas-selection-160.json`, `done.json`, `mechanical.json`, `manifest.json` các batch, các script trong `tools/`) đã được sửa sang đường dẫn mới; SHA-256 giữ nguyên.

## Đã xóa (xem lại bằng tag)

| Đã xóa | Xem lại |
|---|---|
| `apps/game-client` (client Godot) | `git show archive/game-client-final:apps/game-client/...` |
| `apps/game-web` (client thử Three.js) | `git show archive/game-web-final:apps/game-web/...` |
| `client/` (Phaser), `server/` (Godot server), `shared/`, `docker-compose.yml`, `IMPLEMENTATION_PLAN.md`, `test-*.mjs`, `package.json` gốc, `prototypes/p12-stage3` | lịch sử git trước commit dọn dẹp |

## Lưu ý

- Push `main` kích hoạt release CI; các đường dẫn `art/**`, `tools/**`, md, `.ai/**`, `docs/**`... nằm trong `paths-ignore` nên không ra bản mới. Đổi `apps/client`, `apps/game-server`, `data`, `migrations`, `packages` thì ra bản mới.
- Lịch sử git đã push vẫn chứa art cũ (khoảng 2,2 GB packfile). Quyết định 2026-11-16: không viết lại lịch sử đã push.
- Nhánh local `backup/pre-restructure-20261113` giữ 7 commit art (4,5 GB) chưa từng push; có thể xóa nhánh này khi bạn chắc chắn đã backup `art/`.
