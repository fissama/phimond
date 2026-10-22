# P01 v1.0.0 — Kế hoạch triển khai (dev, test, QA, benchmark)

- **Ngày:** 2026-10-22. **Trạng thái:** đề xuất, chờ owner duyệt §9 (5 quyết định) trước sprint S1.
- **Phạm vi:** [`P01-scope.md`](P01-scope.md) §2 (Đợt A, 5 map) và §4 (R01–R10). Không thêm map, không đổi luật chơi.
- **Nguồn yêu cầu:** master spec §2 (budget hiệu năng, frame pacing, 50 CCU), §6 P01-R01…R10, D26.
- **Kết thúc 1.0.0:** tuyến Triệu Linh Điện → Bìa Rừng → Rừng Sâu → Hoàng Môn → Quảng Trường → Trụ → Bìa Rừng chơi trọn trên iPhone 17 Pro Max Safari và macOS Safari bằng client mới `apps/client`, đạt các cổng ở §6–§7.

## 1. Hiện trạng (khảo sát 2026-10-22)

| Phần | Hiện có | Khoảng cách với P01 |
|---|---|---|
| Map server | `data/maps/maps.json`: 5 map cũ (`severa`, `forest`, `beach`, `ranch`, `arena`), lưới `width×height` | Chưa có 5 map Đợt A theo ID P12; **không có collision** (chỉ chặn biên) |
| Di chuyển | `world.move {direction}` = 1 ô nguyên, server kiểm biên | Đủ làm nền; thiếu kiểm va chạm |
| Cổng | `portals [{id,x,to,spawn}]`, xét gần theo **chỉ trục X** (`abs(c.X-p.X)<=2`), đến nơi `c.X = p.Spawn` (Y giữ nguyên) | Vi phạm R01/R04: cần X/Y, vùng cổng, điểm đến X/Y, khóa "chưa mở" |
| NPC | `x,y,roles`; tầm tương tác xét **chỉ X** (`<=3`) | Cần xét hai trục (R04) |
| Quái | `wild_spawns` sinh tự động theo công thức `12+i*9`; contact ±1 ô; không cooldown | Cần vị trí theo spawn plan P12, vòng đời quái solo (R05) |
| Người chơi mới | Đăng ký tạo luôn pet khởi đầu | Cần luồng chọn bệ đá (§7 câu 1) |
| Client | `apps/game-web` (thử Three.js, Vite 7, Preact signals, vitest, Playwright) | Chỉ tham khảo hành vi; viết mới `apps/client` |
| Test/đo | `go test -race`, `tools/check.sh`, `tools/load_gameplay.mjs`, `tools/latency.mjs`, metrics `GAME_METRICS=1` | Thiếu test world 2D, e2e client mới, bench khung hình |

Lưu ý: thư mục gốc `client/` là bản Phaser cũ từ commit đầu, **không liên quan**. Không đụng tới.

## 2. Kiến trúc chốt cho 1.0.0

### 2.1 Một nguồn dữ liệu map (R01, R02)

Mỗi map Đợt A có một file `data/maps/p01/<map_id>.json`, server và client cùng đọc:

```jsonc
{
  "id": "city_square", "kind": "safe_hub", "cell": 1,          // 1 ô = 1 đơn vị world = 128 px
  "width": 48, "height": 32,
  "walk": "<RLE hàng-theo-hàng của lưới 0/1>",                 // collision chuẩn, không suy từ ảnh
  "spawn_default": {"x": 24, "y": 20},
  "respawn_to": "city_square",
  "portals": [{"id":"sq_to_gate","rect":[22,31,4,1],"to":"city_palace_gate","arrive":{"x":24,"y":3,"face":"down"},"locked":false}],
  "pillar": {"npc":"sq_pillar","dest":[{"map":"emerald_forest_main_woods","arrive":{"x":6,"y":12}},{"map":"coast_east","locked":true}]},
  "npcs": [{"id":"sq_skill","x":10,"y":14,"face":"down"}],
  "spawn_zones": [],                                             // map field: vùng + mật độ theo P12-S4-spawn-plan.json
  "scene": "scenes/city_square.scene.json"                       // chỉ client: đặt kit HD-2D, ánh sáng, camera
}
```

- Server chỉ dùng phần luật (lưới đi, cổng, NPC, vùng quái). File `scene` chỉ client đọc, không ảnh hưởng luật.
- Map cũ được giữ trong `maps.json` để test cũ không gãy, nhưng **tài khoản mới không vào** map cũ (xem migration §9 D3).

### 2.2 Server (Go, `apps/game-server`)

| Gói | Thay đổi |
|---|---|
| `internal/world` (đang trống) | Lưới đi, `Walkable(x,y)`, vùng cổng hình chữ nhật, điểm đến an toàn (không nằm trong vùng cổng, cách ≥1 ô), BFS kiểm map liền mạch, khoảng cách Chebyshev hai trục |
| `internal/content` | Nạp `data/maps/p01/*.json`, kiểm hợp lệ khi khởi động (sai thì không chạy) |
| `internal/character/apply.go` | `world.move` chặn ô không đi được; `world.portal` xét hai trục + khóa + đến X/Y; `npc.interact` xét hai trục; contact quái theo vùng và cooldown |
| Người chơi mới | Tài khoản mới ở `summoning_hall_main_hall` chưa có pet; intent mới chọn bệ đá (§9 D2) → nhận pet → đặt sang Bìa Rừng |
| Vòng đời quái (R05) | Quái riêng từng người (không tranh chấp). Trạng thái: hiện → contact → trận → thắng/bắt/chạy/thua → ẩn N giây (cooldown) → hiện lại. Reconnect giữ trạng thái trận; contact không tự kích hoạt lại khi vừa ra trận |
| Migration | Tài khoản cũ đổi map theo bảng §9 D3, đặt về điểm hồi sinh hợp lệ. Có test |

### 2.3 Client mới (`apps/client`)

- **Ngăn xếp:** Vite + TypeScript strict + Three.js (ghim cùng bản `0.170.0` với bản thử) + Preact + `@preact/signals`. Dùng chung `packages/protocol-ts`. Không copy nguyên khối từ `apps/game-web`.
- **Thư mục:**

```
apps/client/src/
  net/      phiên WS, hàng đợi intent, request_id, reconnect, khử lặp theo revision
  state/    signals: character, map, battle, settings, ui
  world/    tọa độ, lưới đi, A* (4 hướng), dự đoán + đối soát vị trí, contact, tương tác
  render/   renderer, camera HD-2D, scene loader, sprite actor + animation, bóng, LOD theo preset, cache tài nguyên
  input/    bàn phím, D-pad, chạm/click-to-move, máy trạng thái dừng (menu/blur/trận)
  ui/       HUD gốc, menu, Cài đặt → Đồ họa, hội thoại NPC, trận đấu, thông báo khóa
  bench/    chế độ đo (?bench=1) ghi frame time, tải, bộ nhớ ra JSON
```

- **Di chuyển:** client di chuyển mượt (nội suy), mỗi lần vào ô mới gửi một `world.move`, không chờ ack ô trước (pipeline tối đa 4 lệnh chưa ack). Server từ chối → client kéo về vị trí xác thực cuối, hiển thị lý do. Click-to-move: A* trên cùng lưới đi, bị chặn thì dừng và báo. Không bao giờ dịch chuyển qua vật cản.
- **Tốc độ đi:** khởi đầu 4 ô/s, chỉnh trong review R06.
- **Cài đặt đồ họa (R10):** Low/Medium/High tách khỏi giới hạn 30/60 FPS. Lưu `localStorage` (bọc try/catch, mặc định Medium/60). Low thực sự giảm: độ phân giải render, kích thước texture môi trường, bóng, blur/DOF, mật độ trang trí. Không giấu quái, NPC hay tín hiệu gameplay.
- **Tài nguyên (R08):** chỉ tải map hiện tại và tải trước cổng kề theo budget. Cache LRU giới hạn theo MB. Giải phóng texture/geometry khi rời map. Làm nóng shader trong màn tải.

## 3. Lộ trình sprint

Mỗi sprint kết thúc bằng nghi thức trong `AGENTS.md`: build, test, self-review, handoff, commit. Sau mỗi sprint chạy server mới nhất để owner tự kiểm.

| Sprint | Mục tiêu | Đầu ra kiểm được | Ước lượng |
|---|---|---|---|
| **S0 — Nền móng** | Khung `apps/client`, script `dev/build/test/e2e/bench`, ESLint + tsc strict, ADR định dạng map (§2.1), duyệt §9 | `npm run dev` lên trang trống kết nối server, đăng nhập được | 1–2 ngày |
| **S1 — World server** | `internal/world`, nạp map p01, collision/cổng/NPC hai trục, migration, intent người chơi mới; greybox 5 map (lưới đi + cổng + NPC + vùng quái) | `go test -race` xanh; validator báo 5 map liền mạch; e2e protocol (node) đi hết tuyến bằng intent | 4–5 ngày |
| **S2 — Client lõi** | Renderer, camera HD-2D, scene từ file map, sprite người chơi (ảnh tạm), input 3 kiểu, dự đoán/đối soát, A* | Đi lại mượt trên greybox, không xuyên tường; unit test world/input xanh | 4–5 ngày |
| **S3 — Cổng, NPC, HUD** | Chuyển map + màn tải, cổng khóa, trụ đá, hội thoại NPC, chức năng có sẵn (hồi phục, cửa hàng, học skill), NPC chưa có chức năng báo "chưa mở"; HUD gốc, menu, back/focus, safe area, xoay (R09) | e2e: đi hết đồ thị §2 scope; review HUD/menu với owner **trước** S4 | 4 ngày |
| **S4 — Quái và trận** | Vòng đời quái solo, contact, UI trận (attack/skill/capture/defend/item/auto/flee), thắng/thua/bắt/chạy, hồi sinh, reconnect giữa trận | e2e: gặp quái → mỗi kết quả trận → cooldown → hiện lại; reconnect test | 4–5 ngày |
| **S5 — Người chơi mới và dựng cảnh** | Luồng 3 bệ đá → xác nhận → nhận pet → dịch chuyển một chiều; dựng 5 cảnh bằng kit đã duyệt, ánh sáng, bóng, occlusion | e2e tài khoản mới chơi trọn tuyến; ảnh chụp 5 cảnh để owner duyệt | 4–5 ngày |
| **S6 — Hiệu năng và Cài đặt** | Preset Low/Medium/High, FPS cap, nạp/giải phóng map, cache, làm nóng shader; chạy benchmark §7 | Báo cáo benchmark có số; Low chứng minh giảm tài nguyên | 3–4 ngày |
| **S7 — QA, playtest, RC** | Test plan §6 trên thiết bị thật, review R06 cuối, sửa lỗi, thay art đã duyệt, RC `v1.0.0-rc.N` | QA sign-off, benchmark pass, owner duyệt → tag `v1.0.0` | 4–5 ngày |

Tổng khoảng 28–36 ngày làm việc. Song song với S1–S5 là luồng art §4. Review R06 chạy ba lần: đầu (cuối S2), giữa (cuối S4), cuối (S7).

## 4. Luồng art song song

| Việc | Khi nào | Chặn |
|---|---|---|
| Review và cắt nhân vật chính (chặng 1–2): khung 192×192, pivot (96,184), 3 hướng, idle 6 + walk 6 | Trong S1 | S2 dùng ảnh tạm; **chặn RC** |
| Xử lý tile: lượng tử hóa `paving-01`, `hall-floor-stone`, `brick-path`; sửa `paving-02`; roll hàng `paving-03` | Trong S2 | Chặn S5 (cảnh thành) |
| Skyline: cắt 2048×512, alpha nhị phân, nối mép, phủ đáy | Trong S2 | Chặn S5 |
| Cắt 7 NPC (sheet 1, sheet 2) + hòm thư 2 trạng thái; kiểm trùng hash/mask | Trong S3 | Chặn S5 |
| Idle NPC (chặng 6) | Khi owner nộp | Không chặn 1.0.0 (1.0.1) |

Mỗi asset qua `tools/check_hd2d_art.sh` và cập nhật `manifest.json` (`approved`) trước khi vào client. Client có bảng thay thế: thiếu asset thì dùng ảnh tạm có đánh dấu, không lỗi.

## 5. Kiểm thử tự động

| Tầng | Công cụ | Bao phủ bắt buộc |
|---|---|---|
| Server unit | `go test -race ./... -count=1` | `world`: walkable, biên, vùng cổng, điểm đến an toàn, khoảng cách hai trục; `apply`: move bị chặn không tăng revision, cổng khóa, cổng ngoài tầm, NPC ngoài tầm theo Y; vòng đời quái; người chơi mới; migration map cũ |
| Validator dữ liệu | `go test ./internal/content` + `tools/p01/validate_maps` | Mỗi map: BFS từ điểm đến mọi cổng/NPC/vùng quái; điểm đến không nằm trong vùng cổng; mọi cổng trỏ map có thật hoặc `locked`; NPC đúng roster P12; vùng quái khớp spawn plan |
| Protocol e2e (node) | `tools/p01/e2e_route.mjs` | Tài khoản mới đi trọn tuyến bằng intent thật, gặp quái, mỗi kết quả trận, reconnect giữa trận, request_id trùng |
| Client unit | `vitest` | A*, máy trạng thái input (thả phím, mất focus, mở menu, vào trận đều dừng), dự đoán + đối soát (bị từ chối, trễ, sai thứ tự), khử lặp revision, cache LRU, lưu cài đặt khi storage lỗi |
| Client e2e | Playwright (Chromium + WebKit) với server local | Luồng người chơi mới; đi hết đồ thị; cổng khóa báo đúng; NPC hội thoại; trận và kết quả; reconnect; đổi preset trong world/trận/chuyển map |
| Ảnh chụp | Playwright screenshot so sánh | 5 cảnh × 3 preset tại camera cố định; HUD ở 440×956, 956×440, 1440×900 |
| Lỗi mạng | Playwright + CDP throttle / proxy trễ | RTT 50/150/300 ms, jitter, rớt WS: không mất intent, không nhân phần thưởng, không kẹt |

Lệnh gộp `sh tools/check.sh` được mở rộng gọi thêm `apps/client` (`tsc`, `vitest`, `build`) và validator map. CI cục bộ: mọi test trên phải xanh trước mỗi commit sprint.

## 6. QA thủ công

**Ma trận thiết bị (đề xuất, §9 D4):** iPhone 17 Pro Max Safari (dọc + ngang) · macOS Safari · macOS Chrome. Android Chrome để P05.

**Test plan** lưu tại `.ai/plan/phases/P01-world/qa/P01-v1.0.0-testplan.md`, mỗi ca có ID, bước, kỳ vọng, kết quả, ảnh/video bằng chứng:

1. **Người chơi mới:** đăng ký → Triệu Linh Điện → 3 bệ đá → hủy/xác nhận → nhận pet → sang Bìa Rừng; F5 giữa chừng; không quay lại được Triệu Linh Điện.
2. **Di chuyển:** phím, D-pad, chạm/click; giữ và thả; đổi hướng nhanh; đi sát tường/góc; click vào vật cản; click xa qua nhiều chướng ngại; mất focus tab; mở menu khi đang đi.
3. **Cổng:** mỗi cạnh của đồ thị cả hai chiều; đến nơi không kích hoạt lại cổng; cổng khóa báo "chưa mở"; Rừng Sâu → Hoàng Môn lần đầu theo cờ nhiệm vụ, lần sau → Quảng Trường; trụ đá chỉ hiện đích đủ cấp.
4. **NPC:** mọi NPC Đợt A hiện đúng chỗ; hội thoại; hồi phục/cửa hàng/học skill chạy; NPC chưa có chức năng báo đúng; tương tác từ trên/dưới/trái/phải.
5. **Quái:** gặp quái tự nhiên, không gặp ngoài ý muốn; thắng/thua/bắt/chạy; cooldown và hiện lại; thua → hồi sinh đúng map; reconnect giữa trận.
6. **HUD/menu:** bố cục gốc; back/đóng; safe area tai thỏ; xoay màn hình; bàn phím ảo khi chat không che nút.
7. **Cài đặt:** đổi Low/Medium/High và 30/60 trong world, trận, giữa chuyển map; reload giữ lựa chọn; chế độ riêng tư Safari (storage lỗi) vẫn chạy.
8. **Hồi quy:** tài khoản cũ đã migration vào được game, pet và vật phẩm nguyên vẹn.

**Phân loại lỗi:** S1 (mất dữ liệu, kẹt không thoát, crash) chặn RC · S2 (sai luật, cổng/NPC/trận sai) chặn RC · S3 (hiển thị, cảm giác) sửa nếu kịp, còn lại vào 1.0.z · S4 (nhỏ) ghi sổ.

**Review gameplay R06** (đầu/giữa/cuối), lưu `.ai/plan/phases/P01-world/review/`: cảm giác di chuyển, đọc map, mật độ quái, contact/cooldown, nhịp khám phá, silhouette nhân vật/quái trên nền. Đo trong 3 phiên chơi 15 phút: số thao tác hụt (click không đi tới), số lần kẹt, số lần gặp quái ngoài ý muốn, thời gian đi trọn tuyến.

**Tiêu chí QA sign-off:** 0 lỗi S1/S2 mở; 100% ca test plan đã chạy trên ma trận; tỉ lệ pass ≥ 95% (ca fail còn lại đều S3/S4 có ticket); review R06 cuối được owner duyệt.

## 7. Benchmark

### 7.1 Client (R08, R10)

**Công cụ:** chế độ `?bench=<scene>&preset=<p>&cap=<30|60>` trong `apps/client`: đi một lộ trình camera cố định 60 giây sau 10 giây làm nóng, ghi frame time bằng `requestAnimationFrame`, số draw call, số texture/geometry, bộ nhớ texture ước tính, thời gian tải. Xuất JSON và hiện bảng để chụp màn hình trên iPhone. Desktop chạy tự động bằng Playwright (`npm run bench`), iPhone chạy tay và lưu JSON vào `evidence/bench/`.

| Chỉ số | Cổng (hard gate) | Ghi chú |
|---|---|---|
| Frame time, cap 60 | p95 ≤ 16,7 ms, p99 ≤ 33,3 ms sau làm nóng | macOS Safari và iPhone 17 Pro Max ở Medium; Low phải đạt trên iPhone |
| Frame time, cap 30 | p95 ≤ 33,3 ms, p99 ≤ 50 ms | Budget riêng, không thay cho chứng nhận 60 |
| Tải lần đầu (cold) | ≤ 6 s tới khi điều khiển được, Wi-Fi tốt | Tách thời gian tải mạng / giải mã / shader |
| Chuyển map | ≤ 1,5 s (có tải trước cổng kề), không giật > 100 ms sau khi vào | Đo cả 7 cạnh đồ thị |
| Low so với High | Bộ nhớ texture giảm ≥ 40%, thời gian GPU/khung giảm ≥ 30% trên cùng cảnh | Bằng chứng R10: giảm thật, không chỉ đổi nhãn |
| Bộ nhớ | Báo riêng JS heap, bộ nhớ texture/GPU ước tính, phần không đo được; không cộng thành "RAM" | Theo R08 |
| Phiên dài | 20 phút đi vòng tuyến: p95 không tăng > 20%, bộ nhớ không tăng liên tục | Phát hiện rò và nhiệt |

Các con số tải/chuyển map/Low-High là **đề xuất ban đầu**, chốt với owner sau lần đo đầu ở S6 (master spec: chốt budget theo bằng chứng, không hạ gate để qua).

### 7.2 Server và mạng

**Công cụ:** mở rộng `tools/load_gameplay.mjs` thêm profile `p01-route` (đi bộ theo lưới, qua cổng, contact, trận, reconnect) và `tools/latency.mjs`; bật `GAME_METRICS=1`.

| Chỉ số | Cổng | Kịch bản |
|---|---|---|
| Server xử lý intent | p95 ≤ 50 ms, p99 ≤ 100 ms | 10 CCU (bắt buộc) và 50 CCU (đo, chưa bắt buộc vì P00 chưa đạt) |
| Gửi → ack (client) | p95 ≤ 250 ms, p99 ≤ 400 ms | RTT ≤ 150 ms |
| Lỗi nội bộ/timeout | < 0,1% intent hợp lệ | Từ chối đúng luật không tính lỗi |
| Toàn vẹn | 0 mất/nhân phần thưởng, pet, vật phẩm | Đối chiếu DB trước/sau, có reconnect 10/50 người |
| Tải di chuyển | Đo số intent/s mỗi người (dự kiến ~4/s khi đi) | Cơ sở cho quyết định §9 D1 |

Combat p95 1659 ms đo ở P00 là rủi ro đã biết. 1.0.0 cần **không tệ hơn P00**; đạt budget 50 CCU không thuộc cổng 1.0.0 (§9 D5).

**Báo cáo:** `.ai/plan/phases/P01-world/evidence/P01-v1.0.0-benchmark.md` gồm cấu hình (máy, trình duyệt, độ phân giải, mạng, cache nóng/lạnh), bảng số, ảnh chụp, JSON thô, kết luận pass/fail từng gate.

## 8. Cổng phát hành v1.0.0

1. Mọi test tự động §5 xanh, `go test -race` xanh.
2. QA sign-off §6, review R06 cuối được duyệt.
3. Benchmark §7 đạt mọi hard gate trên ma trận thiết bị.
4. Art chặn 1.0.0 đã duyệt và thay xong ảnh tạm (nhân vật chính, sàn thành, nền xa thành, NPC Đợt A, hòm thư).
5. Handoff package `handoff-<ngày>.md`; tag `v1.0.0`.
6. Sau khi owner ký: tag lưu trữ `archive/game-web-final`, `archive/game-client-final` rồi xóa `apps/game-web`, `apps/game-client` (việc riêng, owner duyệt lúc đó), cập nhật `AGENTS.md` thay smoke Godot bằng smoke client mới.

## 9. Quyết định cần owner chốt trước S1

| ID | Câu hỏi | Đề xuất |
|---|---|---|
| D1 | Di chuyển gửi mỗi ô một `world.move` hay thêm intent gửi cả đường đi? | **Giữ mỗi ô một intent**, pipeline tối đa 4. Chỉ thêm intent gộp nếu benchmark §7.2 vượt budget |
| D2 | Cho phép mở rộng protocol kiểu cộng thêm (không phá client cũ)? Gồm: map có lưới đi, cổng có `rect/arrive/locked`, trụ đá; intent chọn bệ đá; trạng thái cooldown quái trong snapshot | **Đồng ý**, ghi vào `packages/protocol/README.md` và `protocol-ts` cùng commit |
| D3 | Tài khoản cũ: ánh xạ map cũ sang map mới, hay xóa dữ liệu dev? | **Ánh xạ**: `severa`→`city_square`, `forest`→`emerald_forest_main_woods`, còn lại (`beach`, `ranch`, `arena`)→`city_square`, đặt ở điểm hồi sinh. Giữ pet/vật phẩm |
| D4 | Ma trận thiết bị cho 1.0.0 | iPhone 17 Pro Max Safari, macOS Safari, macOS Chrome. Android sang P05 |
| D5 | 50 CCU có là cổng của 1.0.0? | **Không**: đo và báo cáo, cổng là 10 CCU + không tệ hơn P00 |

## 10. Rủi ro

| Rủi ro | Giảm thiểu |
|---|---|
| Safari iOS: shader/texture lớn gây giật hoặc bị kill tab | Làm nóng shader trong màn tải, texture nén/giới hạn kích thước theo preset, đo sớm ở S2 thay vì đợi S6 |
| Cảm giác đi bị khựng vì trễ ack | Dự đoán phía client + pipeline; test RTT 300 ms từ S2 |
| Greybox lệch với cảnh đã dựng (đi xuyên vật trang trí) | Lưới đi là nguồn chuẩn; S5 có lớp debug vẽ lưới đè cảnh; validator chạy mỗi commit |
| Art nhân vật chính chưa đạt kịp RC | Review chặng 1–2 ngay trong S1; nếu lỗi, đặt GPT vẽ lại sớm |
| Combat chậm từ P00 | Không thuộc cổng 1.0.0, nhưng đo và báo; mở ticket riêng nếu tệ hơn |
