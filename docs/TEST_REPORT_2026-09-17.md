# Phimond test report — 2026-09-17

Result: core gameplay passes in an isolated live run, but database reliability failures remain.

## Passed

- `tools/check.sh`: Go race tests, Go vet, three planner tests, TypeScript checking.
- `node tools/smoke.mjs`: live registration, authenticated WebSocket, account ownership isolation, duplicate purchase protection, forged input rejection, saved movement, logout.
- Godot `scripts/smoke.gd`: six panels, battle UI construction, stale revision rejection, error display, recursive lineage, unique request IDs.
- Godot `scripts/live_smoke.gd`, isolated retry: registration and login, six panels, NPC interaction, shop, healing, lineage, movement, forest portal, quest acceptance/progress/reward, battle defend, exact battle/turn/HP restoration after reconnect, fleeing, and saved character/quest restoration after logout/login.
- Live MySQL atomic mutation/rollback test and breeding persistence test.
- Browser: signed-in character and ancestry visible; encyclopedia search and synthesis planner navigation passed. The user's signed-in account was not modified.

## Failures

1. The first live Godot run disconnected during `world.move`. The server logged a MySQL read timeout. `Store.Authenticate` maps every database query error to `ErrSession`; the WebSocket handler consequently closes the connection as an expired session even for a database outage. Re-run of the gameplay suite alone passed. The intermittent failure remains unresolved.
2. `TestMySQLConcurrentMutations` failed with read timeouts and invalid connections during eight simultaneous requests; its duplicate-request callback count was zero instead of one. This does not establish duplicate writes or data loss, but concurrent persistence was not verified successfully in this run.

## Scope

Tests created separate QA accounts in the configured reconstruction database. No credentials are recorded here. The live Godot run was headless and exercised the real client networking and UI construction; it was not a manual visual/playability review. This report does not certify full MMO load capacity, all content, or parity with the original game. No application code was changed during this testing pass.
