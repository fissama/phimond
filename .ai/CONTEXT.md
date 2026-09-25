# CONTEXT.md — current state of Phimond (cold-start one-pager)

> **Read this first.** Single-screen snapshot of where the project is and
> what to do next. Update at the end of every session / phase delivery.

## Where we are (Sep 25, 2026)

- **Phase**: P00 closed 2026-09-24. **Next**: pick P01 (map/proximity/collision)
  or sprint derived from master spec.
- **Last commit**: see `git log --oneline -5` (changes AGENTS.md + adds this CONTEXT).
- **Server**: `127.0.0.1:8090` PID via `lsof -i :8090`. Healthz must return
  `{"service":"Phimond","status":"ok"}` before any manual UI test.
- **Client**: Godot 4.7.2 at `apps/game-client/.tools/Godot.app`. Editor
  debug port `127.0.0.1:6007` if open.
- **DB**: Aiven MySQL `phimond_reconstruction` (creds in root `.env` —
  never commit). Do not touch `philandz`.

## Stack at a glance

| Layer        | Tech                                                   |
| ------------ | ------------------------------------------------------ |
| Server       | Go 1.x monolith, modular `internal/{auth,character,...}` |
| Client       | Godot 4 + procedural atlas (`reference_game.gd`)       |
| Companion    | Next.js (encyclopedia, lineage, planner only — no HUD) |
| DB           | MySQL 8 (Aiven TLS)                                   |
| Transport    | HTTP + WebSocket (`/api/...`, `/ws`)                   |

## Non-negotiable rules (cheat-sheet)

1. **Server authoritative.** Client predicts movement, renders events.
   Never recompute damage / RNG / capture / rewards on client.
2. **Faithful reconstruction, not redesign.** Match the original game's
   layout & flow. POC-quality art is acceptable per master spec §3.
3. **Spec before code.** Pick from `master plan → phase → sprint spec →
   implementation plan` chain. Never skip a sprint spec.
4. **Phase delivery ritual** (AGENTS.md): implement → build/test →
   self-review → handoff (`phimond-phase-handoff` skill) → commit & push.
5. **No secrets in repo.** `.env` is ignored; test accounts use `p00_*` prefix.
6. **DB isolation.** Use `phimond_reconstruction`. Never query `philandz`.
7. **No silent scope creep.** If you find an obvious fix outside the current
   sprint, log it in `sessions/` and ask before doing it.

## Active phases

| Phase                  | Status      | Owner / next step                          |
| ---------------------- | ----------- | ------------------------------------------ |
| P00 baseline           | closed 09-24 | review/handoff in `plan/phases/P00-baseline/` |
| P01 map/proximity      | not started | pick up next session                       |
| P02 combat UX          | not started |                                              |
| P06 load + fault       | not started |                                              |
| P09 soak/release       | not started |                                              |

## Known carry-over items

- **2D movement** added 2026-09-23 (server + client). Tests:
  `Test2DMovement4Directions`, `Test2DMovementOutOfBounds` PASS.
- **Layout "too big and broken"** fixed in `GameWindow.tscn` (anchor default
  changed from full-rect to top-left; `BattleScene.tscn` opts in explicitly).
- **NPC dialogue readability**: italic removed, font 16, outlined; bg overlay
  0.6 → 0.78.
- **Combat polish**: bigger sprites/bars, TurnIndicator label,
  `_spawn_damage_label` for floating "-N".
- **Stale audit scripts**: `layout_audit.gd` expectations don't match the
  GPT 6 Astra restructure (3 scenes now use `reference_game.gd` wrapper).
  Rewrite or delete before P01.

## How to start a session

```sh
# 1. Sync
git -C /Users/phileanh/rust/phimond pull --rebase
# 2. Sanity
cd /Users/phileanh/rust/phimond/apps/game-server && go build -o /tmp/phimond-server ./cmd/server
go test -race ./... -count=1
curl -s http://127.0.0.1:8090/healthz
# 3. Read
cat /Users/phileanh/rust/phimond/.ai/CONTEXT.md
cat /Users/phileanh/rust/phimond/.ai/plan/PHIMOND_MASTER_SPEC_PLAN.md | head -100
ls /Users/phileanh/rust/phimond/.ai/handoffs/ | tail -5   # most recent
```

If anything in CONTEXT.md is out of date, **fix this file first**, then
do anything else. CONTEXT is the single source of truth for "where are we".
