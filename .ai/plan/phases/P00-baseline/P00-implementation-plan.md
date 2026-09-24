# P00 — Baseline và đường dữ liệu gameplay: Implementation Plan

> **For agentic workers:** Khi thực thi, dùng `superpowers:executing-plans` để triển khai từng task; chỉ dùng `superpowers:subagent-driven-development` nếu chủ dự án chọn delegation. Checkbox bên dưới là công việc dự kiến, chưa phải kết quả đã thực hiện.

**Goal:** Có baseline chạy lại được, event combat thật hiển thị đúng một lần, kết thúc trận/reconnect rõ ràng, và bộ đo nền cho mục tiêu online 50 CCU.

**Architecture:** Giữ Go quyết định gameplay; Godot nhận public state và event batch có revision rồi trình bày. Tách dữ liệu authoritative khỏi trạng thái animation tạm thời; không đưa history/private RNG vào snapshot để sửa UI. Tái sử dụng checks hiện có, bổ sung phép đo và bằng chứng trước khi tối ưu.

**Tech Stack:** Go, MySQL, Godot 4/GDScript, Node.js cho protocol harness; Next.js companion giữ checks hiện có.

**Spec:** [Master spec](../../PHIMOND_MASTER_SPEC_PLAN.md), P00-R01–P00-R06; [Sprint template](../../SPRINT_SPEC_TEMPLATE.md).

**Trạng thái thực thi — 2026-09-23:** Đã triển khai phạm vi baseline P00; xem [báo cáo verification](P00-verification.md) và [execution ledger](progress.md) để biết kết quả, điều chỉnh và giới hạn bằng chứng. Checklist dưới đây giữ nguyên như kế hoạch gốc, không phải chứng nhận mọi gate. Bài tải 10 account hoàn tất nhưng **không đạt latency budget**; chưa chứng nhận 50 CCU.

## Global constraints

- Server quyết định kết quả; không đổi damage, RNG, capture, reward hoặc chi phí để chữa presentation.
- Chỉ database riêng `phimond_reconstruction`; không đụng `philandz`. Không ghi password/token/DSN vào fixture, report hay log.
- Đồ họa là POC. Giữ silhouette, tỷ lệ cơ thể, nét tạo hình, bảng màu nhận diện và phong cách sprite/raster của nhân vật/quái vật.
- Gameplay/game design review đầu, trong và cuối phase là deliverable bắt buộc.
- Mục tiêu sản phẩm: tối thiểu 50 active CCU. P00 chuẩn bị và đo baseline; chứng nhận đầy đủ hot-map/shared-world ở P06 và release candidate ở P09.
- Prefix mọi lệnh shell bằng `rtk`; dùng `rtk proxy` cho lệnh không được wrapper hỗ trợ.
- Giữ save hiện có. Không bulk-stage asset, `.env`, APK hoặc video; tạo restore point an toàn trước sửa code.
- Không thêm map/loài/party/shared-world, không redesign UI, không rewrite aggregate trong P00.

## Review focus

1. Reconnect vào revision mới trên client mới không phát lại event đã lưu — T03/T04.
2. Hai response có `event.seq = 1` đều phải được trình bày nếu revision khác — T03/T04.
3. Finishing blow làm `battle = null` vẫn có feedback cuối và trả điều khiển đúng — T04.
4. Duplicate/stale/malformed response không rollback state hoặc mở khóa thao tác sai — T03/T04.
5. Bot bị đứng, rate-limit hoặc timeout không được tạo báo cáo tải “pass” giả — T06.

## Sprint và dependency đã thống nhất

| Sprint | Deliverable | Tasks | Requirement |
|---|---|---|---|
| P00-S01 | Baseline, review đầu phase, checks và nguồn tham chiếu | T01–T02 | R01, R03, R05, R06 |
| P00-S02 | Public event bridge, terminal presentation, reconnect | T03–T05 | R02, R05, R06 |
| P00-S03 | Metrics/harness, fault baseline, review đóng phase | T06–T07 | R04, R06 |

Thứ tự T01 → T02 → T03 → T04 → T05 → T06 → T07. Review mỗi task bằng deliverable và test; commit riêng khi đã có repository an toàn. Trước mỗi sprint, tạo `P00-S0N-spec.md` theo template, lấy scope và acceptance từ bảng/task tương ứng; plan này là implementation plan chung của P00, không cần sao chép thành ba bản lệch nhau.

## File ownership

| File hiện có | Thay đổi dự kiến |
|---|---|
| `tools/check.sh` | Bổ sung gate Godot active, phân biệt offline/live |
| `tools/server.sh` | Giữ entry server; xác nhận cách chạy/config trong docs |
| `apps/game-client/scripts/PhimondClient.gd` | Một public update batch atomic, validation/revision/session handling |
| `apps/game-client/scripts/reference_game.gd` | Nối update batch vào room, điều phối HUD/input khi finishing |
| `apps/game-client/scripts/room.gd` | Nhận events trực tiếp, giữ battle render cuối, bỏ phụ thuộc history |
| `apps/game-client/scripts/client_protocol_check.gd`, `world_room_check.gd` | Kiểm thử public envelope, không dùng private battle events/history |
| `apps/game-server/internal/transport/server.go`, `live.go` | Phân biệt initial/read/action response, public presentation và metrics |
| `apps/game-server/internal/character/engine.go` | Tái sử dụng public projection; không nới lỏng Snapshot |
| `apps/game-server/internal/character/battle_methods.go` | Đọc lifecycle terminal; chỉ sửa nếu cần projector, không đổi rules |
| `apps/game-server/internal/transport/server_test.go`, `live_test.go` | Public contract, retry/resume và terminal response tests |
| `packages/protocol/README.md` | Document snapshot/event/presentation/replay semantics |
| `docs/STATUS.md`, `docs/GAMEPLAY.md`, `apps/game-client/README.md` | Active entry/checks, giới hạn và cách chơi thử |

File mới được chỉ rõ trong task; đường dẫn code tính từ project root. Đường dẫn evidence tính từ folder plan này.

## T01 — Baseline có thể khôi phục và gameplay review đầu phase

**Files:** tạo `P00-baseline.md`, `P00-gameplay-gamedesign-review.md`, `P00-S01-spec.md`, `P00-S01-verification.md` trong folder này; đọc `.gitignore`, scene/project config và docs active.

**Consumes:** workspace và save hiện có. **Produces:** baseline ID, active commands, test-account policy, findings có severity/owner.

- [x] Kiểm tra `rtk proxy git rev-parse --show-toplevel`; nếu chưa là repository, ghi nhận rõ. Tạo bản sao chọn lọc code/config không secrets vào restore location được định danh trước khi init/version-control; kiểm tra ignore cho `.env`, build/import caches, APK/video và asset dung lượng lớn trước staging. Không yêu cầu git để mới có thể lưu evidence. (evidence: `evidence/source-before-p00.tgz`)
- [x] Ghi Godot/Go/Node version, entry scene, autoload, catalog hash, server port, schema migration version và cấu hình DB đã che secrets. Xác minh scripts nào thực sự gắn với scene, đánh dấu legacy trong docs; không xóa chúng. (evidence: `evidence/asset-hashes.txt`, `evidence/catalog-hashes.txt`)
- [x] Chạy gate hiện có một lần: `rtk proxy sh tools/check.sh`. Ghi exit code và lỗi có sẵn; không mô tả lỗi baseline là regression mới. (evidence: `evidence/baseline-checks.log`, `evidence/checks-reviewed.log`)
- [x] Dùng account test riêng có prefix `p00_`; lưu danh sách ID tạo bởi lần test, owner và thời hạn giữ. Dọn account chỉ theo manifest ID đã tạo, không xóa bằng prefix toàn DB. (evidence: `evidence/load-10-reviewed.json.accounts.json`)
- [x] Playtest login → di chuyển → NPC → contact quái → attack/skill → kết thúc/flee → pet/inventory → logout/login. Capture cùng build; tách bug, friction, design gap và unknown reference. (evidence: `evidence/live-reference.log`, `evidence/live-after-review.log`, `evidence/native-playtest.log`)
- [x] Report review ghi thời gian tới encounter, số lần thao tác hụt, chỗ người chơi không hiểu bước tiếp theo; ghi POC visual debt và các tạo hình phải giữ. Chưa tune gameplay trong task này. (evidence: `evidence/actor-audit.log`, `evidence/asset-verification.log`, `evidence/catalog-verification.log`)

**Acceptance:** một người khác có thể chạy cùng build/check và tìm đúng evidence; không cần được cung cấp secrets trong report. Có restore point và review đầu phase, kể cả baseline còn fail.

## T02 — Reference ledger và canonical checks

**Files:** tạo `P00-reference-ledger.md`; sửa `tools/check.sh`, `docs/STATUS.md`, `docs/GAMEPLAY.md`, `apps/game-client/README.md`; tái dùng `docs/research/VIDEO_UI_AUDIT_2026-09-23.md` và gallery hiện có.

**Consumes:** T01 baseline. **Produces:** ledger screen/actor và offline/live command matrix.

- [x] Mỗi screen login/world/NPC/combat/pet/inventory/synthesis có hàng: timestamp video nếu thấy, source path/hash/version, screenshot implementation, observed/inferred/reconstructed/unknown, gap, reviewer. Screen không thấy trong 4:33 ghi unknown; không bịa timestamp. (evidence: `evidence/screens/*`, `P00-reference-ledger.md`)
- [x] Lưu bộ ảnh chuẩn nhân vật/quái vật theo loài/action/hướng hiện có. Ghi riêng species chưa map art; không bổ sung tạo hình khác phong cách chỉ để checklist đầy. (evidence: `evidence/actors/*`, `P00-reference-ledger.md`)
- [x] Chạy và phân loại `client_protocol_check.gd`, `world_room_check.gd`, `contact_check.gd`, `reference_menus_check.gd`; fixture private-history hiện có phải ghi hạn chế và được sửa tại T04. (evidence: `evidence/checks-reviewed.log`)
- [x] Mở rộng `tools/check.sh` bằng allowlist các offline checks đã xác minh. Godot binary có override `GODOT_BIN`; thiếu executable trả lỗi rõ, không skip rồi pass. Live tests tách lệnh để fast check không âm thầm đăng ký tài khoản/đụng DB. (evidence: `evidence/checks-final.log`)

```sh
rtk proxy apps/game-client/.tools/Godot.app/Contents/MacOS/Godot --headless --path apps/game-client --script res://scripts/client_protocol_check.gd
rtk proxy apps/game-client/.tools/Godot.app/Contents/MacOS/Godot --headless --path apps/game-client --script res://scripts/world_room_check.gd
```

- [x] Cập nhật docs với flow LoginScreen → active reference client; ghi cả check đang fail do F01/F02, không sửa expectation để che lỗi. (evidence: `apps/game-client/README.md`, `docs/STATUS.md`, `docs/GAMEPLAY.md`)
- [x] Review S01: chọn tối đa các friction chặn đọc/hiểu state đưa S02; phần world/balance/art polish dẫn về phase sở hữu. Lưu kết luận giữ/chỉnh/hoãn. (evidence: `P00-gameplay-gamedesign-review.md`)

**Acceptance:** ledger không biến suy đoán thành dữ liệu lịch sử; active/offline/live commands phân biệt rõ; tạo hình chuẩn có evidence dùng lại được.

## T03 — Chốt và kiểm thử public update contract

**Files:** sửa `packages/protocol/README.md`, `transport/server.go`, `transport/live_test.go`, `transport/server_test.go`; tạo `apps/game-server/internal/transport/presentation.go` và `presentation_test.go` nếu projector cần dùng lại; tái dùng serializer trong `character/engine.go`.

**Code evidence:** `Apply` đặt `ev[i].Seq = i + 1` cho từng response; `Snapshot` xóa battle events/history/RNG; transport hiện dùng cùng `state` closure cho auth và mutation. Vì vậy `event.seq` không phải khóa toàn phiên, auth response không được phát last events.

**Contract mới đề xuất (additive):**

```json
{"op":"state","request_id":"action-17","sequence":42,"data":{
  "character":{"id":"test-character","battle":null},
  "events":[{"seq":1,"type":"damage","actor_id":"p1","target_id":"e1","amount":18,"message":""}],
  "presentation":{"battle_id":"b1","completed_battle":{"id":"b1","units":[],"result":"win"}}
}}
```

Ví dụ trên chỉ minh họa shape; test phải dùng đầy đủ public units. `completed_battle` lấy trận vừa kết thúc của chính action, qua public sanitizer, gồm các field renderer cần (id/turn/result/public units), không copy nguyên history. Khi không có terminal transition, field này null/omitted. `battle_id` gắn batch với trận, không suy từ trận mới nhất khi nhiều response tới gần nhau.

- [x] Viết test tái hiện auth/read trả persisted last events: kỳ vọng `events: []`, không `completed_battle`; chạy test xác nhận fail trước sửa. (evidence: `apps/game-server/internal/transport/presentation_test.go`)
- [x] Viết test action nonterminal/terminal: cùng response có public character/events, terminal còn public units để render dù character.battle null; không có seed/rng/commands/wild/private appraisal/full history ở bất kỳ nhánh payload nào. (evidence: `evidence/feedback/*`, `apps/game-server/internal/transport/presentation_test.go`)
- [x] Phân biệt response context auth/read/action trong transport; initial/read là state-only. Mutation response lấy events và terminal projection từ đúng kết quả committed action; duplicate request giữ semantics idempotency của `live.go`, không Apply lần hai. (evidence: `apps/game-server/internal/transport/server.go`, `apps/game-server/internal/transport/live.go`)
- [x] Dùng helper test có signature đề xuất `func TestStatePresentationContract(t *testing.T)` với subtests `auth_without_replay`, `read_without_replay`, `live_damage`, `terminal_public_only`, `duplicate_no_mutation`. Dùng fixture character và catalog hiện có để tạo trận, không tạo RNG rules mới. (evidence: `apps/game-server/internal/transport/presentation_test.go`)

```sh
rtk proxy go -C apps/game-server test ./internal/transport ./internal/character -run 'StatePresentation|Snapshot|Battle' -count=1
```

- [x] Document semantics: envelope sequence = character revision; event seq chỉ thứ tự trong batch; auth/read không replay; old clients có thể bỏ qua additive presentation. Nếu không xác định được đúng terminal battle của action, test phải fail thay vì lấy tùy tiện history cuối. (evidence: `packages/protocol/README.md`)

**Acceptance:** public-wire tests pass và không mở rộng quyền đọc dữ liệu private. Không migration save để sửa trình bày.

## T04 — Atomic client update và finishing playback

**Files:** sửa `PhimondClient.gd`, `reference_game.gd`, `room.gd`, `client_protocol_check.gd`, `world_room_check.gd`; tạo `apps/game-client/scripts/battle_presentation_check.gd`.

**Consumes:** T03 wire contract. **Produces:** signal/method mới sau, các signal cũ giữ cho consumer khác sau khi kiểm tra usages.

```gdscript
# PhimondClient.gd: phát một lần cho accepted state, sau validation/revision gate.
signal state_batch_received(revision: int, character: Dictionary, events: Array, presentation: Dictionary)
```

Method mới của room: `apply_state_batch(revision: int, next_character: Dictionary, next_catalog: Dictionary, events: Array, presentation: Dictionary) -> void`. Thứ tự xử lý được xác định ở checklist bên dưới; không dùng stub khi triển khai.

- [x] Viết regression trước: response revision 4 và 5 đều chứa event.seq=1 phải tạo hai effect; phát lại revision 5 chỉ một lần. Stale response vẫn resolve request tương ứng nhưng không đổi authoritative state; malformed không thay state hay giả ack thành công. (evidence: `evidence/wire-after-review.log`, `evidence/checks-reviewed.log`)
- [x] Đổi active `reference_game` sang nhận batch duy nhất; không đồng thời gọi room từ `state_updated` lẫn signal mới. Initial scene dùng state-only batch với events rỗng, không replay `last_events`. (evidence: `apps/game-client/scripts/reference_game.gd`, `evidence/screens/login.png`)
- [x] Trong room: validate batch → giữ bản render battle cũ nếu cần → áp snapshot authoritative → chọn public terminal battle nếu có → schedule effects theo array order → redraw. Bỏ đọc `character.history` và dedup bằng `_event_sequence` toàn battle; dedup cấp batch dùng revision, reset khi đổi identity/session, không reset tùy tiện khi vào menu. (evidence: `apps/game-client/scripts/room.gd`)
- [x] `completed_battle` chỉ là presentation cache; không gán lại vào `client.state.battle`. Giữ render đến effect cuối hoàn tất rồi chuyển world; reset khi logout/session đổi. Nếu thiếu presentation trên server cũ, trở về state đúng với feedback giới hạn, không crash hoặc dựng reward giả. (evidence: `evidence/screens/battle.png`, `evidence/screens/world.png`)
- [x] Chặn movement, contact, auto và chọn lệnh khi terminal playback còn active; pending network và animation là hai điều kiện riêng. Sau effect cuối phải sync HUD/return control dù không có response tiếp theo. (evidence: `apps/game-client/scripts/room.gd`, `evidence/native-after-attack.png`)
- [x] Khi reconnect, hủy queue/cache cũ, nhận snapshot state-only; resume active battle không tua lại lượt cũ. Request timeout không tự resend mutation chưa rõ kết quả. (evidence: `apps/game-client/scripts/PhimondClient.gd`, `evidence/live-after-review.log`)

**Regression assertions dự kiến:**

```gdscript
# Test fixture tạo room/catalog/public battle trước đoạn này.
room.apply_state_batch(4, live_character, catalog, [{"seq":1,"type":"damage","target_id":"e1","amount":5}], {"battle_id":"b1"})
var first_count: int = room._effects.size()
room.apply_state_batch(5, live_character, catalog, [{"seq":1,"type":"heal","target_id":"p1","amount":3}], {"battle_id":"b1"})
assert(room._effects.size() == first_count + 1)
room.apply_state_batch(5, live_character, catalog, [{"seq":1,"type":"heal","target_id":"p1","amount":3}], {"battle_id":"b1"})
assert(room._effects.size() == first_count + 1)
# Thêm terminal case: character.battle null, public completed_battle còn units;
# assert cache còn đến hết effect rồi hết animation và world input hoạt động.
```

- [x] Sửa world fixture sang đúng public envelope; xóa fixture dựa trên history/private battle.events. Test riêng damage/heal/miss/status, finishing blow, flee/capture/loss, actor unknown, event array rỗng và terminal update lặp. (evidence: `evidence/feedback/*`, `apps/game-client/scripts/world_room_check.gd`, `apps/game-client/scripts/client_protocol_check.gd`)
- [x] Chạy ba Godot checks protocol/world/battle presentation; kiểm tra hình ảnh thật cho hướng/anchor của cả hai phía, giữ fix facing hiện tại. (evidence: `evidence/checks-reviewed.log`, `evidence/screens/world.png`, `evidence/screens/battle.png`)

**Acceptance:** event qua public wire chạy thật, hai response seq lặp không mất feedback, terminal/reconnect không phát lại hoặc làm người chơi mắc kẹt.

## T05 — Live acceptance và review S02

**Files:** sửa `apps/game-client/scripts/reference_live_check.gd` hoặc bổ sung scenario vào `contact_live_check.gd`; tạo `P00-S02-verification.md`; cập nhật review phase.

- [x] Chạy Go race/vet và offline client checks qua `rtk proxy sh tools/check.sh` sau khi bổ sung T02/T04; sửa regression thuộc change, ghi riêng lỗi baseline không liên quan. (evidence: `evidence/checks-final.log`, `evidence/checks-after.log`)
- [x] Với tài khoản test riêng, UI thật contact → combat → action → terminal → world → reconnect. Capture damage và finishing feedback; lặp flee/capture/loss bằng scenario có điều kiện domain hợp lệ. (evidence: `evidence/live-after-review.log`, `evidence/live-reference-final.log`, `evidence/native-playtest.log`, `evidence/native-battle.png`, `evidence/native-after-attack.png`)
- [x] Các event hiếm như miss/status/heal dùng seeded integration fixture trên test instance qua public transport; ghi rõ seeded, không dùng làm bằng chứng progression tự nhiên. Không sửa tài khoản thật hay buff game rules để dễ test. (evidence: `evidence/feedback/*`, `evidence/mutation-observation-green.log`)
- [x] Ngắt kết nối trước ack và sau commit; login lại xác nhận state/reward đúng và không replay effect. Không chỉ xem console “PASS”; đối chiếu trace đã che secrets và UI capture. (evidence: `evidence/wire-after-review.log`, `evidence/wire-faults.log`, `evidence/live-after-review.log`)
- [x] Review game design: người chơi nhận biết lượt, mục tiêu, kết quả và lúc được điều khiển lại; ghi thời gian chờ/thao tác nhầm trước-sau. Friction cần redesign/tuning chiến đấu chuyển P02 với scenario cụ thể. (evidence: `P00-gameplay-gamedesign-review.md`)

**Acceptance:** F01/F02 có evidence đã giải quyết hoặc được ghi còn fail; không đánh dấu verified dựa trên fixture alone.

## T06 — Metrics, load harness và fault baseline 50 CCU

**Files:** tạo `tools/load_gameplay.mjs`, `tools/load_gameplay_test.mjs`, `P00-performance-baseline.md`; sửa metrics quanh transport/live/persistence theo điểm đo thực tế; tham khảo `tools/latency.mjs`, không coi script một account là load test.

**Interface harness đề xuất:** `GAME_API_URL`, `LOAD_USERS`, `LOAD_SECONDS`, `LOAD_PROFILE`, `LOAD_RUN_ID`, `LOAD_ALLOW_MUTATION=1`; không in token. Output JSON chứa run/config fingerprint, active users, action counts, expected rejections, errors/timeouts, achieved actions/sec và p50/p95/p99 theo op.

- [x] Test bằng mock WS: N account không dùng chung token/request ID; timeout dọn waiter; disconnect không replay mutation; bot không có successful action trong 30s bị báo stalled; lỗi đăng nhập/bot thiếu count làm run fail; empty latency samples không trả percentile 0/pass. (evidence: `tools/load_gameplay_test.mjs`)

```sh
rtk proxy node --test tools/load_gameplay_test.mjs
rtk proxy env LOAD_ALLOW_MUTATION=1 LOAD_USERS=1 LOAD_SECONDS=120 LOAD_PROFILE=mixed LOAD_RUN_ID=p00-smoke node tools/load_gameplay.mjs
```

- [x] Chặn mutation mặc định nếu thiếu opt-in. Trước chạy, xác minh test instance dùng DB riêng, account manifest riêng. Đăng ký theo batch chậm hoặc provision trước để rate-limit auth không bị nhầm với gameplay capacity; vẫn ghi failures thực. (evidence: `tools/load_gameplay.mjs`, `evidence/load-1.json.accounts.json`)
- [x] Implement movement cadence hợp lệ, battle actions chỉ khi có turn, mutation khi đủ tài nguyên; seed chuẩn bị chỉ ở test environment và report rõ. Không spam invalid intents rồi tính là 50 active users. (evidence: `tools/load_gameplay.mjs`, `evidence/p00-final-10-mixed.json`, `evidence/p00-final-25-mixed.json`)
- [x] Instrument receive→response-ready, Apply, DB wait/commit, outbound bytes/errors và queue/checkpoint lag; dùng duration monotonic, label theo op/result, không label account/request làm metrics cardinality tăng vô hạn. RTT đo trên client; frame-time đo riêng trong Godot. (evidence: `apps/game-server/internal/transport/metrics.go`, `evidence/metrics-final-server.log`, `evidence/metrics-stages-server.log`)
- [x] Baseline ramp 1/10/25/50; đo mixed 20 world/20 combat/10 pet-shop-quest và 50 independent battles khi fixture đủ điều kiện. Những tính năng thiếu ghi unsupported; không coi 50 người cùng tọa độ hiện tại là đã có shared-world fan-out. Phần 25/50 account chưa đo ở P00 (chưa đủ fixture cho hot-map contention). (evidence: `evidence/load-1.json`, `evidence/load-10.json`, `evidence/load-10-reviewed.json`) → owner: P06 (chạy 25/50 mixed battle và 50 independent battles trên test deployment tách)
- [x] Ghi máy/vCPU/RAM/DB region/pool/RTT, warmup và achieved load. Full 2h soak/75-user stress dùng test deployment tách khỏi phiên chơi đang dùng; ở P00 chưa có deployment này thì ghi gate chưa đo, owner P06, không chế kết quả. (evidence: `P00-performance-baseline.md` mục "## Môi trường và phương pháp") → owner: P06 (2h soak50, stress75/15min, RTT300, packet loss/jitter, production CPU/RSS)
- [x] Khóa budgets dự kiến của master bằng decision record: 50 CCU, RTT≤150ms/jitter≤30ms; server p95≤50ms/p99≤100ms; ack p95≤250ms/p99≤400ms; errors<0.1%; client 60Hz p95≤16.7ms/p99≤33.3ms. Chưa đạt phải có bottleneck và task phase sở hữu, không âm thầm nới số. Performance budget FAILED on dev topology; do not relax numbers. (evidence: `P00-performance-baseline.md` mục "## Handoff tối ưu" và "## Đã hoãn — không đo trong P00")
- [ ] Fault matrix: 10 reconnect/40 còn hoạt động; slow consumer; timeout-after-commit; RTT300ms đánh giá recovery riêng. Nếu P00 chưa chạy đủ 50, harness phải chạy lại được và report giới hạn rõ, P06 vẫn giữ release-blocking gate. → owner: P06 (ghi lý do: harness chạy lại được trên test deployment tách; P00 chỉ có reconnect smoke + 10 mixed, chưa đủ fault matrix)

**Acceptance P00:** harness có kiểm thử chống pass giả, metrics/budget/workload đã định nghĩa và baseline tối thiểu 1/10 account trên test instance. 50 CCU chỉ được tuyên bố đạt sau report đủ profiles/soak/client thực ở P06/P09; P00 không tự triển khai shared-world để lấp thiếu hụt.

## T07 — Review cuối phase và handoff

**Files:** tạo `P00-verification.md`, cập nhật `P00-gameplay-gamedesign-review.md`, master findings/status và docs active.

- [x] Chạy core loop bị ảnh hưởng lần cuối trên build đã định danh; kiểm tra save/relogin và art chuẩn nhân vật/quái vật không đổi thiết kế. (evidence: `evidence/live-after-review.log`, `evidence/native-playtest.log`, `evidence/screens/*`)
- [x] Report mỗi requirement R01–R06: task/evidence/result, pass/fail/unmeasured, reviewer và ngày. Không ghi planned thành implemented. (evidence: `P00-verification.md`)
- [x] Review giữ/chỉnh/hoãn: blocker event/terminal/replay đóng trong P00; world friction→P01, battle pacing/visual→P02, pet mapping→P03, progression→P04, polish→P05, shared load→P06. Mỗi finding hoãn có owner phase và acceptance. (evidence: `P00-gameplay-gamedesign-review.md`)
- [x] Xác nhận rollback: restore source/build pair; contract additive tương thích; không xóa dữ liệu durable. Nếu có migration ngoài dự kiến, dừng task liên quan và bổ sung migration/restore plan trước triển khai. (evidence: `evidence/source-before-p00.tgz`)
- [x] Exit: live damage/heal/miss/status + terminal đã có evidence, reconnect không replay, public fixtures, canonical docs, reference ledger, load baseline và review hoàn tất. **Có gate fail (latency budget FAILED, 50 CCU NOT certified) → phase closed với owner map P01/P02/P05/P06/P09.**

## Verification và giới hạn của chính plan này

Đã đọc code để xác nhận F01/F02, event seq theo response, auth replay risk và fixture history không đại diện public wire. Các file mới/interface ở trên là thiết kế cần triển khai, không phải API đã tồn tại. Chưa chạy benchmark hoặc thay đổi gameplay khi viết tài liệu này.

Khi bắt đầu thực thi, chọn S01/T01 trước; không nhảy thẳng tới load 50 người trên instance người dùng đang chơi. Mỗi sprint có review gameplay/game design và evidence riêng, cùng cập nhật report phase.
