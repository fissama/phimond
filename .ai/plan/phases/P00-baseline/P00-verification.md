# P00 verification — 2026-09-23

## Kết luận

Đã triển khai event/presentation contract, client batch validation/playback, reconnect no-replay, canonical checks, reference/actor baselines và metrics/load harness. P00 là phase nền tảng và đo baseline; **không phải chứng nhận game đã hoàn thiện hoặc đạt 50 CCU**. Môi trường local server + remote DB hiện vượt latency budget, cần tối ưu/test lại ở phase sở hữu.

## Requirement → evidence

| Requirement | Kết quả hiện tại | Evidence |
|---|---|---|
| P00-R01 | Có runtime/entry baseline và source restore point; không tạo Git history giả | [Baseline](P00-baseline.md), archive/hash |
| P00-R02 | Public event bridge, terminal render, no-replay, schema validation đã qua tests/live flow | `checks-reviewed.log`, `live-after-review.log`, `wire-visual.log`, native screenshots |
| P00-R03 | Ledger video/source/gap và bộ ảnh actor giữ art direction | [Reference ledger](P00-reference-ledger.md), `screens/`, `actors/`, asset hashes |
| P00-R04 | Metrics/harness có regression, baseline1/10 và reconnect; latency budget chưa đạt | [Performance baseline](P00-performance-baseline.md), load JSON + assessment |
| P00-R05 | Active commands/docs đồng bộ; offline gate không tạo account; load manifest có ID | `tools/check.sh`, client README/protocol, `.accounts.json` |
| P00-R06 | Có review đầu/trong/cuối, native input và handoff findings | [Gameplay/game design review](P00-gameplay-gamedesign-review.md) |

## Các gate đã chạy

- `rtk proxy sh tools/check.sh`: Go race toàn module + vet; 5 Godot checks; 7 load harness tests; 3 companion tests + TypeScript check. Output [checks-reviewed.log](evidence/checks-reviewed.log). Unit suite mặc định skip các MySQL tests cần opt-in; live verification được ghi riêng.
- `TestStatePresentationContract`: WS thật qua httptest với engine thật, memory persistence; auth/read không events, terminal public units, privacy, duplicate receipt state-only.
- Opt-in MySQL thật: cả 4 tests `TestMySQLAtomicMutation`, `TestMySQLConcurrentMutations`, `TestMySQLMovementCheckpoint`, `TestMySQLAuditBatchPreservesEscapedJSON` PASS; [mysql-integration.log](evidence/mysql-integration.log). Không suy ra khả năng phục hồi mọi kiểu mất mạng/DB từ các tests này.
- `TestPublicBattleFeedbackFixtures`: chọn seed fixture cho damage/heal/status/miss/win/loss/capture/flee, gửi lại qua WS handler thật, export chính received frames. Godot active client/renderer nhận các frame này; native ảnh trong `evidence/feedback/`. Fixture có chuẩn bị pet/skill/HP; không chứng minh progression tự nhiên hoặc backend MySQL cho mọi event hiếm.
- `reference_live_check.gd`: MySQL thật, login/register, bốn hướng, menu/NPC/shop/quest/portal, defend/item/skill/attack/capture/flee, reconnect/login và persisted state; [live-after-review.log](evidence/live-after-review.log), không script errors.
- `contact_live_check.gd`: walk contact đúng species, attack/flee, không đứng yên retrigger, click-to-approach. Native keyboard/click xác nhận thêm qua `native-playtest.log` và ảnh `native-battle.png`, `native-after-attack.png`.
- Art và catalog SHA256 verification không thay bytes curated source/rules. Atlas actor là render source, không artwork mới. Godot vẫn có warning UID cũ `tab_unselected.tres`, engine dùng path fallback; chưa phải lỗi load.

## Review độc lập và sửa sau review

Một reviewer độc lập đọc code; không sửa workspace hoặc tạo load mới. Hai Important findings đã có red→green regressions:

1. Recovered stall >30s từng bị report bỏ sót: lưu `max_gap_ms` gồm initial/inter-success/final gaps; không pass sau khi bot hoạt động lại.
2. Packet character rỗng/sequence ép kiểu/nested payload lỗi từng clear pending: validate supported shape trước acknowledgment/state mutation. Stale **valid** reply vẫn clear đúng pending mà không rollback state.

Minor deferred: `response_ready.errors` chưa phân loại domain/rate-limit error envelopes; dùng operation-stage metrics và harness failures để đánh giá. Đã ghi rõ trong performance doc. Không dùng counter luôn0 này làm bằng chứng zero errors.

## Quyết định và giới hạn

- Không Git repo: selective restore archive + ledger thay commit/worktree. Rủi ro: rollback cần diff/chọn file, không có commit ranges; archive không là backup save.
- Duplicate receipt state-only, kể cả response mang state mới hơn: tránh replay event không thuộc request. Đổi lại khi mất ack, reconnect phục hồi state mà không tua feedback lịch sử.
- Sửa vet named fields và nullable-spawn bug trong P00 vì chúng chặn canonical/live gate; không thay battle formulas hay topology map.
- P00 chỉ đo capacity của các account độc lập. Shared-world fan-out/50 actor/party chưa có; 2h soak50, stress75, CPU/RSS, network shaping và production topology chưa được chứng minh. Đã giao P06/P09, không đánh dấu verified.
- Review ảnh xác nhận hướng/nhận diện, không chứng nhận đồ họa cuối cho player. P01/P02/P05 còn map seams, animation/frame timing và polish.
- Không merge/push/deploy remote/schema migration/cleanup account người dùng. Tài khoản test giữ lại để điều tra; chỉ cleanup theo manifest đã xác minh.

## Bước tiếp

Server local mặc định 8090 đã được khởi động bằng code mới và `/healthz` trả `ok`. Mở lại Godot client để nạp scripts mới; phiên client cũ đang chạy có thể cần kết nối lại.

P01 dựa trên baseline này để thống nhất world/proximity/collision. P02 xử lý combat UX/pacing và resource presentation sâu hơn. Trước release online phải có cấu hình server/DB rõ và report đạt đủ 50 CCU; báo cáo tải hiện tại là bằng chứng cần tối ưu, không phải bằng chứng “không lag”.
