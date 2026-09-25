# Phimond Context

Stable, high-value project context only. Update on architectural change,
not on every commit.

- **Last verified**: 2026-09-25
- **Verified against commit**: `452dbc0`

## Product

Reconstruction of 《靈獸世界 Online》 / PokeZoo Online — a 2D
room-based monster-taming MMORPG. Faithful rebuild, not a redesign.
Spec: `.ai/plan/PHIMOND_MASTER_SPEC.md`.

## Current architecture

| Layer        | Tech                                                   |
| ------------ | ------------------------------------------------------ |
| Server       | Go 1.x modular monolith (`internal/{auth,character,...}`) |
| Client       | Godot 4.7.2 + procedural atlas (`reference_game.gd`)   |
| Companion    | Next.js (encyclopedia, lineage, planner — no gameplay HUD) |
| DB           | MySQL 8 (Aiven, TLS)                                  |
| Transport    | HTTP REST + WebSocket (`/api/...`, `/ws`)              |

Server is authoritative for RNG, damage, capture, rewards, and
ownership. Client predicts motion and renders events.

## Repository map

```
/Users/phileanh/rust/phimond
├── apps/
│   ├── game-server/         (Go backend)
│   ├── game-client/         (Godot 4 client)
│   └── web/                 (Next.js companion)
├── data/                    (JSON content: species, skills, maps, npcs, …)
├── migrations/              (DB schema migrations)
├── docs/                    (research, reports — read-only history)
├── tools/                   (helper scripts)
├── AGENTS.md                (project-level agent rules — read on cold-start)
└── .ai/                     (this folder)
```

## Important system boundaries

- Server PID lives on `127.0.0.1:8090`. Health check: `curl http://127.0.0.1:8090/healthz` must return `{"service":"Phimond","status":"ok"}`.
- DB name **must** be `phimond_reconstruction`. Never query `philandz`.
- `.env` (workspace root) holds DB creds — gitignored. Test accounts use `p00_*` prefix.
- Godot binary at `apps/game-client/.tools/Godot.app` — gitignored (`.tools/` rule).

## Core development commands

```sh
# Build server
cd apps/game-server && go build -o /tmp/phimond-server ./cmd/server

# Run server (env from root .env, MYSQL creds inline)
cd apps/game-server && env GAME_METRICS=1 GAME_ADDR=127.0.0.1:8090 \
  GAME_DB_NAME=phimond_reconstruction \
  MYSQL_HOST=philand-philand.i.aivencloud.com MYSQL_PORT=25390 \
  MYSQL_USER=avnadmin MYSQL_PASSWORD='<see .env>' \
  MYSQL_TLS=true MYSQL_TLS_INSECURE=true \
  GAME_DATA_DIR=../../data \
  /tmp/phimond-server > /tmp/p00-serve.log 2>&1 &

# Test (race + count=1)
cd apps/game-server && go test -race ./... -count=1

# Client smoke
apps/game-client/.tools/Godot.app/Contents/MacOS/Godot --headless \
  --path apps/game-client --script res://scripts/min_smoke.gd

# Canonical pre-commit check
sh tools/check.sh
```

Full workflow + per-task ritual: see `AGENTS.md` (workspace root).

## Canonical documentation

- **Master spec**: `.ai/plan/PHIMOND_MASTER_SPEC.md`
- **Sprint spec template**: `.ai/plan/SPRINT_SPEC_TEMPLATE.md`
- **Active work pointer**: `.ai/ACTIVE.md`
- **Glossary**: `.ai/GLOSSARY.md`

## Important architectural constraints

1. Server-authoritative: never recompute damage / RNG / capture / rewards on the client.
2. Faithful reconstruction: do not redesign layout, flow, or art direction.
3. Spec before code: master spec → phase spec → sprint spec → implementation plan → code.
4. Phase delivery ritual (AGENTS.md): implement → build/test → self-review → handoff → commit & push.
5. No secrets in repo. Test accounts prefix `p00_*`.
6. DB isolation: `phimond_reconstruction` only.
7. No silent scope creep: if you spot a fix outside the current sprint, log a note and ask first.

## Current work

See `.ai/ACTIVE.md` for current phase, sprint, blockers, and next action.
