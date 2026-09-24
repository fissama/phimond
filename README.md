# Phimond

A playable reconstruction of the pet-training and multi-generation synthesis loop of 《靈獸世界 Online》. This is the **first vertical slice**, not a complete or certified 100% replica. Historical rules, deliberate reconstruction, and remaining gaps are recorded in [research](docs/research/fidelity.md) and [delivery status](docs/STATUS.md).

## Play locally

The Go API uses `http://127.0.0.1:8090`; the companion journal uses `http://localhost:3100`. The game itself is a Godot 4 desktop client in `apps/game-client`.

1. Configure the root `.env` from `.env.example`. Use a **new, dedicated MySQL database**. The configured database for this workspace is `phimond_reconstruction`. Existing `philandz` is not used or migrated.
2. Create/migrate that new schema: `./tools/server.sh -migrate`.
3. Start the authoritative server: `./tools/server.sh`.
4. On this Mac, double-click [launch.command](apps/game-client/launch.command), which uses the downloaded local Godot runtime. Otherwise open `apps/game-client/project.godot` in Godot 4 and press F5, or run `godot --path apps/game-client`. See [client instructions](apps/game-client/README.md).
5. Start the companion: `cd apps/web && npm ci && npm run dev`.
6. Register your own account in either client (username 3–24 ASCII letters/digits/underscores, password 10–72 UTF-8 bytes). Both use the same account and pets.

Go 1.25+, Node 20.9+, MySQL 8+, and Godot 4 are required. Credentials live only in ignored root `.env`. Hosted MySQL supports `MYSQL_TLS=true`, `MYSQL_CA_FILE`, and explicit development opt-in `MYSQL_TLS_INSECURE=true`. This workspace uses the latter at the user's request; the default verifies certificates.

## First expedition

You begin in Severa at position 6 beside Trainer Elin, with a Moss Snail, 100 gold, seals and supplies. Accept journal quests, learn Earth Pulse at the trainer, and heal for free. Move right to the forest gateway at 39, enter, then search for beasts. Lower HP before attempting capture. Quests pay gold/experience and supplies; choose your active pet to train it.

Return to the city and use the left gateway to Whisperleaf Ranch. Approach Keeper Oren at position 6 for appraisal, recipe study and synthesis. Two recipe-compatible opposite-gender parents must reach level 20. Synthesis costs a soul and gold; optional blessing consumes a leaf. Parents become retired ancestors, while the child inherits individual qualities, resistances and **only actually learned parental skills**. Repeating this produces multi-generation ancestry. Strengthening consumes an inactive same-star donor and improves future inheritance.

Arena I requires trainer level 10. Win at the Imperial Arena to unlock Treasure Beach. The companion website reads the server catalog for the encyclopedia and synthesis dependency tree; My Journal shows your persistent pets and ancestry.

## Layout

- `apps/game-server`: Go domain, validated content, MySQL persistence, REST and WebSocket server.
- `apps/game-client`: Godot rendering, UI and intent-only network client.
- `apps/web`: Next.js companion encyclopedia, recipe planner and account journal.
- `data`: 14 species, 29 skills, seven statuses, eight race definitions, six recipes, five rooms, four quests and configurable reconstructed rules.
- `migrations`: versioned MySQL schema, restricted to a Phimond-marked database.
- `packages/protocol`: v1 contract.
- `docs`: architecture, database, gameplay, research and remaining scope.
- `infra/compose.yml`: optional separate Go deployment against your configured MySQL.

The old `server/`, `client/`, `shared/`, `data/players` and root Docker Compose project remain intact. Their protocol and saves are separate. [Legacy setup instructions](docs/LEGACY_README.md) describe that previous prototype; its running server still uses port 8080.

## Verify

```sh
cd apps/game-server
go test -race ./...
go vet ./...
# Explicit live integration (only an already marked dedicated database):
set -a; . ../../.env; set +a
MYSQL_TEST=1 go test -race ./internal/persistence ./internal/game
```

`node tools/smoke.mjs` checks the live HTTP/WebSocket boundary. It creates isolated test accounts without logging credentials. Godot's fixture/live smoke commands are in its README. `cd apps/web && npm test && npm run build` checks the companion; `npm run test:live` exercises the running app in Chromium.

Gameplay and economy changes commit immediately. Duplicate request IDs cannot double-spend. No old JSON saves are imported. See [known limits](docs/STATUS.md) before treating this as a production MMO.
