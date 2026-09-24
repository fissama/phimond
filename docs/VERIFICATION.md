# Verification record

2026-09-17, macOS host with Go 1.25, Godot 4.7.2 via isolated Docker and the verified native macOS runtime, Node 24, and the supplied remote MySQL connection targeting only the new `phimond_reconstruction` schema.

| Check | Result |
|---|---|
| `go test -race ./...` | Passed, 28 tests reported; explicit MySQL tests opt-in |
| `go vet ./...` | Passed |
| `go build -o phimond-server ./cmd/server` | Passed |
| `MYSQL_TEST=1 go test -race ./internal/persistence -count=1 -v` | Passed including concurrent duplicate/distinct transactions, rollback and logout |
| `MYSQL_TEST=1 go test -race ./internal/game -run TestMySQLBreedingSurvivesReconnect -count=1 -v` | Passed; parents/child/costs, relational ancestry, one audit event after duplicate request |
| Distribution tests | 100,000 captures and 100,000 offspring; weakened capture probability, bounded quality mean/variance and 95% learned-skill inheritance tolerance |
| `node tools/smoke.mjs` | Passed against live API: HTTP/WS auth, foreign pet isolation, request dedup, forged damage rejection, persisted movement, logout |
| Godot editor import/start and fixture smoke | Passed |
| Native Mac launcher `--headless --version` | Passed: 4.7.2.stable.official.ed1daf0bf |
| Godot `scripts/live_smoke.gd` | Passed registration, catalog, six panels, NPC/shop/heal/lineage, room movement/portal, quest rewards, battle turn, exact mid-battle reconnect, flee and saved login |
| Next.js `npm run build`, `npm run typecheck`, `npm test` | Passed |
| Companion live browser | Passed catalog/search/tabs/planner, registration/login/logout, cookie flags, owned pet, ancestry; no page errors or mobile horizontal overflow |
| `docker compose -f infra/compose.yml config --quiet` | Passed; image deployment not run |

Test accounts are isolated randomly named fixtures left in the new database for inspection. Game data and legacy JSON saves are not truncated. No production deployment, load test, full original-content comparison, or proof of 100% fidelity has been performed. Screenshots under apps/web/artifacts document the companion UI; runtime caches/artifacts are ignored.

Native macOS follow-up: official Godot 4.7.2 archive SHA-256/ZIP and macOS codesign verified; fixture smoke passed on native Apple Silicon renderer. Rendered UI inspected at apps/game-client/artifacts/first-expedition.png. Room clipping and integer/effect formatting were corrected in that pass. Native client left open at login; no account credentials are saved.
