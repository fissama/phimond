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

## Plans / phases

Phase plan ở `.ai/plan/phases/P00-baseline/` (P00 baseline + event contract).
Master spec ở `.ai/plan/PHIMOND_MASTER_SPEC_PLAN.md`.

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
