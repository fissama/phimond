# P00 — Continuation Beads (session 2026-09-24)

> **For agentic workers:** Mỗi bead là một work unit nhỏ đủ để chốt P00 mà **không** tự lấn sang P06/P09 scope. Không chứng nhận 50 CCU, không rewrite battle formula, không merge map/loài mới.

**Goal:** Đóng T06 (metrics + fault baseline) và T07 (review cuối phase + handoff) cho P00 để baseline gọn và sang được P01/P02 mà không treo gate "chưa đo".

**Phạm vi session này:**
- T06 đóng: validate lại metrics post-fix, ghi evidence bottleneck ở dev topology, document giới hạn.
- T07 đóng: cập nhật `P00-review.md` cuối phase, reconcile checklist R01–R06, handoff notes.
- Reconnect Godot client smoke + commit phần đóng P00.

**Không thuộc session này (owner khác, đã tagged):**
- 25 / 50 CCU load ramp, 2h soak50, stress75/15min, RTT300, packet loss, jitter — **P06/P09**
- Topology DB-region, vCPU/RAM headroom, CPU/RSS profiler đầy đủ, slow-query/row-lock sampling — **P06**
- Shared-world fan-out, 50 actor cùng tọa độ, party — **P10–P12**
- Map seam / animation timing / art final — **P01 / P02 / P05**
- Battle formulas / capture / reward — **master constant** (không đụng)

## Trạng thái hiện tại

| Item | Trạng thái | Bằng chứng hiện có |
|---|---|---|
| T01 baseline + archive + runtime | ✅ pass | `P00-baseline.md`, `evidence/source-before-p00.tgz` |
| T02 reference ledger + canonical checks | ✅ pass | `P00-reference-ledger.md`, `tools/check.sh` |
| T03 public WS contract | ✅ pass | `transport/presentation.go`, `presentation_test.go` |
| T04 atomic client update + terminal playback | ✅ pass | `PhimondClient.gd` `state_batch_received`, `room.gd` |
| T05 live MySQL + native input + reconnect | ✅ pass | `live-after-review.log`, `native-playtest.log`, `wire-visual.log`, fixtures |
| T06 metrics harness | ✅ partial | `load_gameplay_test.mjs` pass, `load-10-reviewed.json` workload_done; perf budget FAILED |
| T06 per-mutation stages, authority-lock wait, rejected-response metrics | ⚠ active | `mutation-observation-green.log` (PASS once), `metrics-stages-server.log` |
| T07 final review + handoff doc | ⚠ active | `P00-review.md` thiếu mục cuối |
| Master findings / `docs/STATUS.md` close | ⚠ active | thiếu P00 close note |
| Godot client reconnect smoke sau code mới | ❌ chưa làm | cần `live-after-review.log` mới + screenshot |

**Acceptance của P00 exit:** mỗi bead dưới có evidence hoặc tag "owner = P0X" rõ ràng. Không có item nào "chưa chốt".

---

## Beads

### T06 closure — Metrics, load harness, fault baseline

#### B-T06-01 — Validate rejected-response metrics fix
**Goal:** Xác nhận envelope rejection (rate-limit / domain) hiện tăng đúng counter trong metrics log; tránh lỗi "Errors=0" trong WS test khi run có rate-limit.

**Files:**
- `apps/game-server/internal/transport/metrics.go`
- `apps/game-server/internal/transport/live.go`
- `evidence/metrics-final-server.log`
- (tạo) `evidence/metrics-rejected-check.log`

**Steps:**
1. Đọc `wire-faults.log` → tìm run có rejected response.
2. Chạy lại transport test đã thêm (xem `transport/metrics_test.go`) với seed rate-limit envelope; assert counter > 0.
3. Nếu chưa có test rejected-domain → thêm subtest trong `metrics_test.go` hoặc `live_test.go` (theo convention hiện có).

**Acceptance:**
- Re-run → counter tăng khi envelope rejected.
- `metrics-final-server.log` mới có stage `rejected_response` với `n > 0` trong ít nhất một scenario.
- Doc-note trong `P00-performance-baseline.md > Handoff tối ưu`: vẫn dùng stage metrics, không tuyên bố "zero errors" từ `response_ready.errors`.

**Effort:** ~10–15 phút.

---

#### B-T06-02 — Per-mutation SQL stage labels completeness
**Goal:** Đảm bảo stage histogram `apply_mutation`, `db_select`, `db_check`, `db_commit` (và `db_rollback` nếu lỗi) đều có mẫu trong một mutation thật.

**Files:**
- `apps/game-server/internal/persistence/*.go`
- `apps/game-server/internal/transport/live.go`
- `evidence/metrics-stages-server.log`
- (tạo) `evidence/mutation-stages-final.log`

**Steps:**
1. Đọc `metrics-stages-server.log` → xác nhận các nhãn đã phát ra; nếu thiếu nhãn nào, thêm measurement ngay đầu/cuối hàm tương ứng trong `character.Mutate` hoặc store layer.
2. Chạy `mysql-integration` opt-in suite lại, snapshot stages.

**Acceptance:**
- `metrics-stages-server.log` (mới) cho thấy ≥4 stage labels đều có `count > 0` cho một mutation thật (không phải chỉ `apply_mutation`).
- `apply_mutation` không che stage bên trong DB; stage durations vẫn dùng `duration monotonic`.

**Effort:** ~10–15 phút.

---

#### B-T06-03 — Authority-lock wait metric
**Goal:** Bổ sung (hoặc verify) `authority_lock_wait_ms` để quan sát contention per-character khi ≥2 mutation trỏ cùng character.

**Files:**
- `apps/game-server/internal/character/engine.go` (lock acquisition)
- `apps/game-server/internal/transport/metrics.go`

**Steps:**
1. Search codebase cho `sync.Mutex` / trước `apply` → thêm `prometheus.NewHistogram` hoặc peer metric (server-internal) đo `time.Since(lockStart)`.
2. Replay một workload 2 cùng character (fixture test) để có mẫu `n > 0`.

**Acceptance:**
- `metrics-final-server.log` có stage `authority_lock_wait` với `n` và `p95_ms`.
- Nếu đã có từ trước → chỉ verify + link evidence, không đụng code.

**Effort:** ~5 phút nếu đã có, ~15 phút nếu cần thêm.

---

#### B-T06-04 — Record bottleneck evidence tại dev topology
**Goal:** Re-run load 10-account mixed profile với code + metrics mới nhất, so sánh với `load-stages-10b.json` (cũ) để xem các stage nào đã thay đổi; gắn evidence mới vào `P00-performance-baseline.md`.

**Files (evidence):**
- (tạo) `evidence/load-stages-final.json`
- (tạo) `evidence/load-stages-final.json.accounts.json`
- `P00-performance-baseline.md` (cập nhật bảng "Các phép đo đã chạy")

**Steps:**
```sh
env LOAD_ALLOW_MUTATION=1 GAME_API_URL=http://127.0.0.1:8092 \
  LOAD_USERS=10 LOAD_SECONDS=120 LOAD_PROFILE=mixed \
  LOAD_RECONNECT=1 LOAD_RUN_ID=p00-stages-final \
  node tools/load_gameplay.mjs
```
1. Capture JSON + manifest.
2. Đọc `operations["world.encounter"]` p95/p99 + `pet.activate` p95/p99 → đối chiếu với `load-10-reviewed.json`.
3. Đối chiếu `metrics-stages-server.log` mới để xem stage nào dominate (`db_select` / `db_commit` / `apply_mutation`) → ghi vào `P00-performance-baseline.md`.

**Acceptance:**
- Có evidence mới tên `load-stages-final.json`, summary 1 dòng vào bảng.
- Đánh giá dev topology vẫn viết "owner = P06 cho production topology", không nới budget master.

**Effort:** ~10 phút (re-run + parse + 1 dòng doc).

---

#### B-T06-05 — Document deferred items trong P00-performance-baseline.md
**Goal:** Đảm bảo các hạn chế đã biết có chỗ ghi rõ, không "treo lủng lẳng" giữa pass/fail.

**Files:**
- `P00-performance-baseline.md`

**Acceptance — list sau phải xuất hiện ở cuối doc (hoặc mục mới "Đã hoãn"):**

| Hạn chế | Lý do không đo ở P00 | Owner |
|---|---|---|
| `response_ready.errors` chưa tách domain vs rate-limit envelope | minor deferred, dùng stage metrics + harness failures thay thế | P06 |
| 25 / 50 account load ramp | chưa đủ fixture cho hot-map contention | P06 |
| 2h soak50, stress75/15min, RTT300, packet loss, jitter | cần deployment tách khỏi phiên chơi | P09 |
| Production topology (DB region, pool sizing, vCPU/RAM) | local Mac + remote Aiven ≠ production | P06 |
| CPU/RSS profiler đầy đủ + slow-query/row-lock sampling | chưa có evidence isolation giữa DB/network/Go stages | P06 |
| Animation seam / route 10 phút / 50 actor | graphics performance POC | P01/P02/P05 |

**Effort:** ~5 phút (chỉ doc).

---

### T07 closure — Final review + handoff

#### B-T07-01 — Update `P00-review.md` (cuối phase)
**Goal:** Bổ sung mục "Cuối phase (final)" confirm:
- Native keyboard/click đã chạy (`native-playtest.log`, `native-battle.png`, `native-after-attack.png`).
- Reviewer đã không chạy live DB recovery / fault matrix / visual / 50-CCU.
- P02/P01/P05/P06/P09 ownership của friction còn lại.

**Files:**
- `.ai/plan/phases/P00-baseline/P00-review.md`

**Acceptance:**
- Có mục "Cuối phase (final)" ngay sau "Cuối phase" cũ, không xóa nội dung cũ.
- Đảm bảo F01–F02 và P00-G01–G06 đều có status rõ (chỉnh/hoãn/chuyển phase).

**Effort:** ~5 phút.

---

#### B-T07-02 — Master findings / status handoff
**Goal:** Cập nhật `docs/STATUS.md` + `apps/game-client/README.md` + (optional) `apps/game-server/README.md` với dòng close P00.

**Files:**
- `docs/STATUS.md`
- `apps/game-client/README.md`
- `docs/GAMEPLAY.md` (verify đã đủ từ T02 — không thêm nếu đủ)

**Nội dung tối thiểu cần chèn:**
- Server default `127.0.0.1:8090` chạy code mới; reconnect Godot client để nạp scripts.
- P01 / P02 / P06 / P09 owner map (link tương ứng).
- P00 latency budget FAILED — không có cert 50 CCU.

**Acceptance:**
- `docs/STATUS.md` có dòng "P00 closed, owners: P01 (map), P02 (combat UX), P06 (release load), P09 (soak)" hoặc tương đương.
- `apps/game-client/README.md` có ghi chú reconnect sau khi nâng code.

**Effort:** ~5–10 phút.

---

#### B-T07-03 — Reconcile checklist trong `P00-implementation-plan.md`
**Goal:** Mỗi checkbox `[ ]` cũ → link sang evidence file tương ứng hoặc ghi rõ owner. Tránh doc báo "đã xong" mà evidence chưa chốt.

**Files:**
- `.ai/plan/phases/P00-baseline/P00-implementation-plan.md`

**Steps:**
1. Với mỗi task T01–T07, scan checklists; thay `[ ]` thành `[x]` + evidence path (đường dẫn tương đối trong folder).
2. Item nào không thuộc P00 (đã tag owner P0X) → thêm dòng `→ owner: P0X (ghi lý do)`.

**Acceptance:**
- Mỗi requirement R01–R06 trong `P00-verification.md` map được sang evidence file.
- Không còn `[ ]` nào không giải thích.

**Effort:** ~15 phút.

---

### Handoff

#### B-HAND-01 — Reconnect Godot client smoke
**Goal:** Reconnect Godot client với code mới sau khi server đã chạy; capture native screenshot.

**Files (evidence):**
- (ghi đè) `evidence/live-after-review.log`
- (tạo) `evidence/screens/p00-reconnect.png`
- (tạo) `evidence/screens/p00-reconnect-map.png`

**Steps:**
```sh
rtk proxy apps/game-client/.tools/Godot.app/Contents/MacOS/Godot \
  --path apps/game-client \
  --script res://scripts/reference_live_check.gd
```
1. Capture log → ghi đè `live-after-review.log` (đã có, mục đích xác nhận code hiện tại cũng pass sau refresh).
2. Screenshot post-login → world → reconnect.
3. Đảm bảo 0 script errors.

**Acceptance:**
- Có log + screenshot mới, no script error.
- Đối chiếu với manifest reconnect trong native accounts (`native-battle.png`, `native-after-attack.png`).

**Effort:** ~5 phút nếu Godot đã mở; ~15 phút nếu cần mở mới.

---

#### B-HAND-02 — Commit + push P00 closure
**Goal:** Ghi lại evidence + doc changes mới vào git; không commit `.ai/.../*.tgz` mới hoặc evidence binary lớn ngoài whitelist.

**Files (staged ngoài evidence đã track):**
- `.ai/plan/phases/P00-baseline/P00-continuation-beads.md`
- `.ai/plan/phases/P00-baseline/P00-review.md`
- `.ai/plan/phases/P00-baseline/P00-implementation-plan.md`
- `.ai/plan/phases/P00-baseline/P00-performance-baseline.md`
- `.ai/plan/phases/P00-baseline/P00-verification.md`
- `docs/STATUS.md`
- `apps/game-client/README.md`
- `evidence/load-stages-final.json*` (nếu B-T06-04 chạy)
- `evidence/metrics-final-server.log`, `evidence/metrics-rejected-check.log`, `evidence/mutation-stages-final.log`
- `evidence/screens/p00-reconnect*.png`, `evidence/live-after-review.log`

**Skip:**
- Bất kỳ `.tgz` mới trong evidence.
- `evidence/source-before-p00.tgz` đã commit đợt trước.

**Acceptance:**
- Một commit duy nhất với message rõ ràng (tiếng Việt OK), push lên `origin/main`.
- Không có secret / `.env` ngoài allowlist (đã verify trong commit lần trước).

**Effort:** ~3 phút.

---

## Completion checklist (P00 exit)

- [ ] B-T06-01: rejected-response metrics validated → evidence mới
- [ ] B-T06-02: per-mutation stage labels đầy đủ → evidence mới
- [ ] B-T06-03: authority-lock wait metric visible → evidence
- [ ] B-T06-04: dev-topology bottleneck evidence mới + 1 dòng trong `P00-performance-baseline.md`
- [ ] B-T06-05: deferred-list chốt trong `P00-performance-baseline.md`
- [ ] B-T07-01: `P00-review.md` có mục cuối phase final
- [ ] B-T07-02: `docs/STATUS.md` + `apps/game-client/README.md` có P00 close + owner map
- [ ] B-T07-03: checklist `P00-implementation-plan.md` reconciled, evidence-linked hoặc owner-linked
- [ ] B-HAND-01: Godot reconnect smoke + ảnh + log mới
- [ ] B-HAND-02: commit + push

**Definition of Done cho P00:**
- Mọi R01–R06 có evidence path rõ, hoặc unmeasured có owner.
- Không còn checklist "mở" mà không giải thích.
- Không sửa battle formula / ruleset / topology production.
- Source đã push `fissama/phimond` private main.

## Out-of-session note (giữ trong master)
P01 sẽ thống nhất world/proximity/collision trên baseline này.
P02 cải thiện pending/turn pacing combat UX, không đụng persistence durability budget.
P06 đo RTT/pool/query/locks/connection churn + 50 mixed battle; certify production resilience.
P09 2h soak50, stress75/15min, RTT300; release candidate.

---

*Plan này được tạo trong session 2026-09-24, sau khi initial commit đẩy lên `origin/main`. Không thuộc phạm vi sửa plan master P0X trong sprint; chỉ đóng dở P00 để P01 sẵn sàng.*
