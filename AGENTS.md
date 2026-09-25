# AGENTS.md

> Phimond — Pokémon-style 2D game MVP. Workspace at `/Users/phileanh/rust/phimond`. Read this file on cold-start before any task.

## Build / Run / Test

```sh
# Build server (cổng 8090 với .env credentials)
cd apps/game-server && go build -o /tmp/phimond-server ./cmd/server

# Start server (sử dụng trực tiếp .env credentials, không qua .env file)
cd apps/game-server && env GAME_METRICS=1 \
  GAME_ADDR=127.0.0.1:8090 \
  GAME_DB_NAME=phimond_reconstruction \
  MYSQL_HOST=philand-philand.i.aivencloud.com MYSQL_PORT=25390 \
  MYSQL_USER=avnadmin MYSQL_PASSWORD='<see .env>' \
  MYSQL_TLS=true MYSQL_TLS_INSECURE=true \
  GAME_DATA_DIR=../../data \
  /tmp/phimond-server > /tmp/p00-serve.log 2>&1 &

# Smoke
curl http://127.0.0.1:8090/healthz    # expect {"service":"Phimond","status":"ok"}

# Canonical check
sh tools/check.sh

# Load harness (opt-in mutation)
env LOAD_ALLOW_MUTATION=1 GAME_API_URL=http://127.0.0.1:8090 \
  LOAD_USERS=10 LOAD_SECONDS=120 LOAD_PROFILE=mixed \
  LOAD_RECONNECT=1 LOAD_RUN_ID=<id> node tools/load_gameplay.mjs

# Godot headless smoke
GAME_API_URL=http://127.0.0.1:8090 \
  apps/game-client/.tools/Godot.app/Contents/MacOS/Godot \
  --path apps/game-client --script res://scripts/reference_live_check.gd
```

## Required workflow rule — manual validation after every task

**Rule (added 2026-09-24):** After completing any task in this workspace, **always run the latest committed source** so the user can manually validate before continuing. Concretely:

1. `git pull` (nếu upstream có commit mới) hoặc `git fetch` để chắc local đã sync.
2. `git status` để xác nhận working tree clean (sau khi commit/push xong).
3. **Rebuild server với code mới nhất** rồi start trên `127.0.0.1:8090` với `GAME_METRICS=1` (để user thấy stage metrics).
4. Confirm `/healthz` returns 200.
5. Báo lại cho user: server PID, port, log path, Godot editor debug port (nếu đang mở).
6. Đợi user validate xong mới chuyển task kế tiếp.

**Lý do:** Người dùng muốn manual test sau mỗi task completion (đặc biệt là khi P00 chốt và sang P01); không được để source "chạy cũ" trong khi user đang ở UI thật.

**Cổng mặc định:** server `127.0.0.1:8090`, Godot editor `127.0.0.1:6007` (debug, nếu editor đang mở).
**Log:** `/tmp/p00-serve.log` (server, rotate khi restart).
**Test accounts:** xem `.ai/plan/phases/P00-baseline/evidence/*.accounts.json` (p00_* prefix + cũ hơn ref_*/contact_*).

## Required workflow rule — Phase delivery ritual

**Rule (added 2026-09-25):** Every phase / sprint delivery in this workspace
must follow this 5-step sequence before reporting "done" to the user or
launching the next task:

1. **Implement** — code the phase per its spec; do not edit code outside the
   agreed scope. Spec lives in `.ai/plan/PHIMOND_MASTER_SPEC.md` +
   `.ai/plan/phases/<phase>/` + `.ai/plan/SPRINT_SPEC_TEMPLATE.md`.
2. **Build / test** — rebuild server + run smoke + unit + race tests:
   ```sh
   cd apps/game-server && go build -o /tmp/phimond-server ./cmd/server
   cd apps/game-server && go test -race ./... -count=1
   curl -s http://127.0.0.1:8090/healthz
   # Client smokes:
   apps/game-client/.tools/Godot.app/Contents/MacOS/Godot \
     --headless --path apps/game-client \
     --script res://scripts/min_smoke.gd
   apps/game-client/.tools/Godot.app/Contents/MacOS/Godot \
     --headless --path apps/game-client \
     --script res://scripts/contact_check.gd
   apps/game-client/.tools/Godot.app/Contents/MacOS/Godot \
     --headless --path apps/game-client \
     --script res://scripts/layout_audit.gd
   ```
   Every smoke must end with the script's `PASS:` line. Failures are blockers.
3. **Self-review** — re-read `git diff <base>..HEAD`, list what is *actually*
   live (not aspirational). Confirm the implementation matches the spec's
   behavior contract. Be honest about flaky / known issues; do not paper
   over failures.
4. **Handoff package** — invoke the `phimond-phase-handoff` skill. Output
   goes to `.ai/plan/phases/<phase>/handoff-<YYYYMMDD>.md` for the audit
   trail and is also printed so the user can forward it to GPT 6 Astra
   unchanged.
5. **Commit & push** — `git add -A && git commit -m "<phase>: <summary>" &&
   git push origin main`. Never commit secrets, `.env`, `node_modules`, or
   `.tools/` (already in `.gitignore`).

**Lý do:** Two reasons.
- Handoff package gives GPT 6 Astra (or any other agent) the exact context
  to continue work without re-reading the whole repo.
- Self-review forces honesty: what passes a smoke is *live*; what fails is
  a known issue. The handoff is not marketing copy.

**Handoff format (mandatory — used by `phimond-phase-handoff` skill):**

```
Phase: <ID + name>

Implemented:
- <bullets>

Files changed:
- <bullets>

Architecture decisions:
- <bullets>

Tests:
- <N> passed
- <N> skipped
- <N> flaky: <reason>

Known issues:
- <bullets>

Git diff:
<attach diff / branch / changed files>
```

Diff size policy: inline if ≤ 500 lines, else save to
`/tmp/phase-<id>-<short-sha>.diff` and reference the path.

## Plans / phases

Phase plan ở `.ai/plan/phases/P00-baseline/` (P00 baseline + event contract).
Master spec ở `.ai/plan/PHIMOND_MASTER_SPEC.md`.

Active plan (cập nhật gần nhất):
- P00 — baseline + measurement → đã đóng 2026-09-24 (commit `e66350b`). Latency budget FAILED trên dev topology; 50 CCU NOT certified.
- P01 — map/proximity/collision (sẽ start ở session sau).
- P02 — combat UX pacing.
- P06 — production load + fault matrix + topology.
- P09 — soak/release candidate.
- P10–P12 — shared-world + party (chỉ trong master; chưa có plan chi tiết).

## Conventions

- Prefix shell command bằng `rtk` (or `rtk proxy` nếu wrapper không hỗ trỗ). Nhiều tool cũng có thể gọi trực tiếp.
- Server authoritative: không sửa damage/RNG/capture/reward để che presentation bug.
- DB chỉ dùng `phimond_reconstruction` (từ `.env`). Không touch `philandz`.
- `.env` ignored; **never** commit. Account manifest dùng cho test prefix `p00_*`.
- Godot binary + zip ở `apps/game-client/.tools/` đã ignore qua `apps/**/.tools/`. Cỡ ~700MB.
- Godot warnings về UID `tab_unselected.tres` cũ — engine tự fallback path, không phải lỗi load.

## Roles of agents

Các task beads (khi chia nhỏ) ưu tiên 3 workers song song:
- **Code** (worker): sửa Go internal; chạm `apps/game-server/internal/{transport,character,persistence}/`.
- **Docs** (worker): chỉ `.md` files; không đụng code.
- **Operational** (worker): chạy server + load + Godot smoke; tạo evidence trong `evidence/`.

Khi chạy parallel, **mỗi worker owns file scope riêng** để không revert chéo. File scope conflict (cùng file được 2 worker edit) phải sequence hoặc gộp vào 1 worker.

## Reconnect / refresh thường gặp

```sh
# Stop server đang chạy (nếu cần)
lsof -iTCP:8090 -sTCP:LISTEN -n -P | awk 'NR>1 {print $2}' | xargs -I{} kill {}

# Re-run server sau khi code đổi
cd apps/game-server && go build -o /tmp/phimond-server ./cmd/server
cd apps/game-server && env GAME_METRICS=1 GAME_ADDR=127.0.0.1:8090 \
  GAME_DB_NAME=phimond_reconstruction \
  MYSQL_HOST=philand-philand.i.aivencloud.com MYSQL_PORT=25390 \
  MYSQL_USER=avnadmin MYSQL_PASSWORD='AVNS_zlIsmS1_dmZ-hQ2460r' \
  MYSQL_DATABASE=phimond_reconstruction MYSQL_TLS=true MYSQL_TLS_INSECURE=true \
  GAME_DATA_DIR=../../data \
  /tmp/phimond-server > /tmp/p00-serve.log 2>&1 &

# Godot: trong editor đã mở (PID 57609 LoginScreen scene), chỉ cần
# reconnect WS bằng cách Play scene hoặc tắt/mở LoginScreen.
```
