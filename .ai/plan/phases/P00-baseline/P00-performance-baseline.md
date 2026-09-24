# P00 performance baseline — chưa đạt gate 50 CCU

## Môi trường và phương pháp

Mac Apple M3 Pro, local Go server/generator/client; MySQL Aiven remote, database riêng. TLS dev theo cấu hình người dùng hiện có. Server/DB khác vị trí vật lý; chưa có RTT network shaping hoặc cấu hình staging cùng region. Không suy ra production capacity từ topology này.

Harness public HTTP/WS, không seed tài nguyên: cadence 500ms sau mỗi ack, 10 account gồm 4 world, 4 battle, 2 pet/shop/quest. Provision/travel warmup tách khỏi cửa sổ đo 120s. Hai account reconnect ở giữa run. Mỗi account có session/request IDs độc lập; manifest không credentials. Có native/manual và scripted UI test cạnh bài tải nên metrics server là aggregate của cả chúng, không độc quyền 10 bots.

## Các phép đo đã chạy

| Run | Kết quả workload | Observation |
|---|---|---|
| `evidence/load-1.json` | 1 account, 120s, 238 moves | move p95 3ms, p99 133ms; max 462ms |
| `evidence/load-10.json` | 10 account hoạt động, 120s; không worker errors | 943 moves p95 1ms/p99 104ms; 205 battle actions p95 2961ms/p99 4935ms |
| `evidence/load-10.json.assessment.json` | **Latency budget FAILED** | Đánh giá lại mẫu đã ghi, không phải run mới |
| `evidence/load-10-reviewed.json` | 10 account hoạt động, workload hoàn tất; **latency budget FAILED**, exit 1 | 952 moves p95 4ms/p99 53ms; 301 battle actions p95 1659ms/p99 2344ms; encounter p95 2017ms |
| `evidence/load-stages-final.json` | 10 account, mixed, 120s, reconnect 1; workload_completed TRUE, **performance_budget_met FALSE** | world.move p95 2ms/p99 54ms (n=952, max 432ms); world.encounter p95 1177ms/p99 1422ms (n=32); battle.action p95 1353ms/p99 1826ms (n=300, max 2141ms); pet.activate p95 821ms/p99 1360ms (n=209). Stage metrics: durable_mutation/battle.action max 2108ms, response_ready/battle.action max 2110ms; authority_wait/world.encounter max 171ms (1 outlier); DB pool WaitCount=0, MaxOpenConnections=12. Latency budget FAILED — dev topology only, owner = P06 cho production cert. |

Report đầu tiên có `passed` nghĩa workload hoàn tất; sau review harness đã tách `workload_completed`, `performance_budget_met`, `passed` và giữ sticky stall. Không sửa số liệu report cũ. Run cuối `load-10-reviewed.json` ghi `workload_completed: true`, `performance_budget_met: false`, `passed: false`, `capacity_certified: false`. Chênh lệch giữa hai run không đủ để kết luận đã tối ưu backend; đây là các lần đo riêng trên môi trường có biến động.

Trong mẫu metrics trước run cuối: 212/213 Apply battle ≤1ms, 1 mẫu ≤25ms; phần durable mutation thường 0.5–5s, max ~6.94s. DB pool WaitCount=0 trong samples đã đọc; không có bằng chứng pool-wait là nguyên nhân chính. Peak heap Go ~3.44MB trong mẫu đó **không phải RSS**. Metrics có connection peak 11 vì live client bổ sung. Chưa có CPU/RSS/slow-query/row-lock profiler đủ để quy toàn bộ độ chậm cho một nguyên nhân duy nhất.

Native frame sample 120 frames: median 8.36ms, p95 9.74ms tại forest, renderer OpenGL M3 Pro. Đây là mẫu ngắn, không đạt yêu cầu đo route 10 phút hoặc 50 actor. Không dùng headless frame cadence làm FPS của player.

## Công cụ dùng lại

```sh
rtk proxy node --test tools/load_gameplay_test.mjs
rtk proxy env GAME_METRICS=1 sh tools/server.sh
rtk proxy env LOAD_ALLOW_MUTATION=1 GAME_API_URL=http://127.0.0.1:8092 LOAD_USERS=10 LOAD_SECONDS=120 LOAD_PROFILE=mixed LOAD_RECONNECT=1 LOAD_RUN_ID=p00-next node tools/load_gameplay.mjs
```

`LOAD_OUTPUT` đặt đường dẫn JSON; manifest account nằm cạnh nó. `LOAD_PROFILE=world|battle|pet|mixed`; `LOAD_USERS` 1–75, `LOAD_SECONDS` tối đa7200. Workload battle dùng random encounter legacy, không chứng minh visible-contact/hot-map contention. Account thiếu tài nguyên làm run fail, không tự buff tài khoản hoặc bỏ qua lỗi. Registration pace 3.2s/account để giữ rate-limit20/min/IP.

Metrics opt-in `GAME_METRICS=1`: log aggregate mỗi30s, fixed op/stage labels, duration buckets, heap/GC/goroutines, cached characters/connections, DB pool stats. Không có endpoint debug public, payload, token hoặc DSN. `response_ready` đo sau parse/validation/session/apply/project/marshal tới trước write; `durable_mutation` bao trùm Store.Mutate, chưa phân tách query/commit nội bộ. `socket_write` đo write/backpressure. `response_ready.errors` hiện không phân loại domain rejection; dùng harness errors/operation-stage errors, không dùng counter này để chứng minh không có lỗi.

## Handoff tối ưu

- P02: đo và cải thiện cảm giác pending/turn flow trong giới hạn durability; không trả thưởng trước commit để che latency.
- P06: chạy topology app/DB gần nhau, đo RTT/pool/query/locks/connection churn; thử đúng hot-map, 50 battle/mixed và 10 reconnect/40 tiếp tục.
- P09: 2h soak50, stress75/15min, CPU/RSS/headroom, packet loss/jitter/RTT300 và release candidate.
- Giữ budgets master (ack p95≤250ms/p99≤400ms; server p95≤50ms/p99≤100ms). Môi trường hiện tại không đạt; không giảm chuẩn để đóng gate.

## Đã hoãn — không đo trong P00

| Hạn chế | Lý do không đo ở P00 | Owner |
|---|---|---|
| response_ready.errors chưa tách domain vs rate-limit envelope | minor deferred; dùng stage metrics + harness failures thay thế | P06 |
| 25 / 50 account load ramp | chưa đủ fixture cho hot-map contention | P06 |
| 2h soak50, stress75/15min, RTT300, packet loss, jitter | cần deployment tách khỏi phiên chơi | P09 |
| Production topology (DB region, pool sizing, vCPU/RAM) | local Mac + remote Aiven ≠ production | P06 |
| CPU/RSS profiler đầy đủ + slow-query/row-lock sampling | chưa isolate giữa DB/network/Go stages | P06 |
| Animation seam / route 10 phút / 50 actor | graphics performance POC | P01/P02/P05 |

Mọi item trên cần evidence + sign-off trong phase sở hữu trước khi P06/P09 cert.
