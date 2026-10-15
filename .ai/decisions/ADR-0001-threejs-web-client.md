# ADR-0001: Client game web dùng Three.js (apps/game-web), thay Godot Web

- **Status**: Accepted
- **Date**: 2026-10-14
- **Deciders**: Chủ dự án (Phimond) + Claude (brainstorm/debate cùng ngày)

## Context

- Master spec (§P12 Stage 3) yêu cầu: "Engine selection/migration riêng sau benchmark evidence".
- Prototype Stage 3 (`prototypes/p12-stage3/`) dựng cùng một cảnh Emerald HD-2D bằng Three.js r170 và Godot 4.7.2 Web (Compatibility). Log đo ngày 2026-10-14 (Android, Edge): Three ≈ 3,4 MB tải, ≈ 20 MB texture ước tính, đổi map ≈ 6 ms; Godot ≈ 13,9 MB tải (wasm ≈ 39 MB chưa nén), ≈ 116 MB video memory, đổi map ≈ 10 ms. Log đó **không có dữ liệu khung hình** (`frames: null`) và không chạy trên iPhone/Safari, nên **không đủ để kết luận hiệu năng**.
- Chủ dự án quyết định chọn Three.js (2026-10-14), chấp nhận rằng bằng chứng iPhone/Safari vẫn phải được thu trong quá trình port.
- Spec P01-R09: không biến Next.js thành HUD gameplay thứ hai.

## Decision

1. Client game web mới là app riêng `apps/game-web` (Vite + TypeScript strict + Three.js, UI DOM bằng Preact + signals).
2. Giao thức server giữ nguyên trong giai đoạn port (parity). Nâng cấp P01 (X/Y thống nhất, collision, tier đồ họa) chỉ bắt đầu sau khi qua gate parity.
3. Token phiên nằm trong bộ nhớ trang (như client Godot), gửi qua frame `auth.session`; không đưa vào URL/log/storage.
4. Client Godot bị đóng băng (không thêm tính năng) và giữ làm bản đối chứng cho đến khi qua gate parity.
5. Điều kiện kèm theo: bằng chứng frame time/bộ nhớ trên iPhone 17 Pro Max Safari + macOS Safari phải được thu trước khi sản xuất hàng loạt môi trường (theo P01-R07/R08). Nếu bằng chứng cho thấy Three.js không đạt, ADR này bị Superseded bằng ADR mới.

## Consequences

- Phải viết lại ≈ 2,3k dòng GDScript đang hoạt động (reference_game, room, classic_hud, reference_menus, reference_art, LoginScreen, PhimondClient) thành TypeScript.
- Mất công cụ editor của Godot; đổi lại payload nhỏ, nhúng web và test e2e bằng Playwright dễ hơn.
- Phải tự dựng: pipeline chuyển asset Godot (spriteframes, sheet) sang atlas web, lớp UI, hệ thống input/focus.
- `tools/check.sh` phải được mở rộng (typecheck, vitest, build) và `tools/check_godot.mjs` giữ đến khi cutover.

## Alternatives considered

- Giữ Godot Web: tích hợp rẻ nhất vì client đã có, nhưng payload và GPU memory lớn, rủi ro iOS Safari chưa được loại trừ.
- Trang /play trong Next.js: bị loại vì P01-R09 và vòng đời SSR không phục vụ game.
- Port và nâng P01 cùng lúc: bị loại vì khó phân biệt lỗi do port với lỗi do thiết kế mới.
