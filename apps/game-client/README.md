# Phimond game client

Godot gameplay client with the source-asset presentation reconstructed from the confirmed 4:33 Pokezoo video. Go/MySQL remains authoritative. See the [video audit](../../docs/research/VIDEO_UI_AUDIT_2026-09-23.md), [comparison gallery](../../docs/research/ui-comparison-2026-09-23/index.html), and [verification/known gaps](../../docs/research/UI_RECONSTRUCTION_VERIFICATION_2026-09-23.md).

## Run and manual test

Start the game server on `127.0.0.1:8090` using the repository server instructions, then double-click [launch.command](launch.command). It uses the existing bundled Godot in `.tools/Godot.app`, falling back to `godot` on PATH. The website on port 3100 is not the gameplay client.

> After P00 baseline close (2026-09-24), restart Godot client to load new scripts. Server default `127.0.0.1:8090` đã chạy code mới.

1. Register a test account or log in. Main entry is `scenes/LoginScreen.tscn`.
2. Use WASD/arrows or all four D-pad directions. The center opens the menu. F3 toggles coordinates/revision for diagnosis.
3. Click an NPC to approach and talk, or press E near one. NPC options open shop/quests/healing as supported by that NPC.
4. Click a portal to approach and travel. The right-edge icon opens pet, inventory, quest and journey menus. Esc / Trở về closes overlays. In menus, D-pad cycles focus and Chọn activates the focused button.
5. In the forest, walk into a wild creature to enter combat with that species. Clicking one approaches it first. Its position and species come from the server catalog; the server validates proximity before starting combat. Standing still after fleeing does not retrigger; walk away and return, or select the creature again. Choose attack or skill, then click the opponent or press Chọn. The bag offers usable items and capture. Auto waits for acknowledged turns/effects; flee returns to the field.
6. Open the pet interface for actual attributes/resistances/skills/growth, switching, appraisal, skill learning and confirmed release. Ranch offers explicit parent/recipe selections and confirmation before consuming pets.
7. If disconnected, open the connection menu and reconnect. The server snapshot restores progress; uncertain mutations are never replayed automatically.

Source images retain their APK variant differences from the video. Some item/skill icons have no verified mapping; unsupported social/party/equipment systems are not simulated. Menus outside the video are adaptations. Default fixed logical viewport: 960×640, displayed at 1152×768 with preserved aspect.

## Checks

Canonical offline gate: `rtk proxy sh tools/check.sh` from project root. It includes Go race/vet, five active Godot checks, load-harness unit checks and companion tests/typecheck. `GODOT_BIN` overrides the bundled executable. Godot script diagnostics are checked even when the engine returns exit code zero.

For a separate test server, set `GAME_API_URL=http://127.0.0.1:8092`; the client derives its WS URL. The default remains 8090. Both `reference_live_check.gd` and `contact_live_check.gd` create disposable accounts and write real test progress; they are deliberately excluded from the offline gate.

P00 verification and load limitations: [phase evidence](../../.ai/plan/phases/P00-baseline/P00-verification.md). Combat now consumes public event batches and keeps terminal feedback before returning to exploration. Account reconnect does not replay stored effects. Art remains POC and actor design is preserved.

Run from repository root:

```sh
apps/game-client/launch.command --headless --editor --quit
apps/game-client/launch.command --headless --script res://scripts/world_room_check.gd
apps/game-client/launch.command --headless --script res://scripts/client_protocol_check.gd
apps/game-client/launch.command --script res://scripts/reference_menus_check.gd
apps/game-client/launch.command --script res://scripts/visual_audit.gd -- /tmp/phimond-ui
apps/game-client/launch.command --script res://scripts/reference_live_check.gd
apps/game-client/launch.command --headless --script res://scripts/contact_check.gd
apps/game-client/launch.command --script res://scripts/contact_live_check.gd
```

The last check creates a random account in the running reconstruction database and exercises real authentication, persistence and gameplay. It never prints credentials. Fixture captures and integration tests do not replace direct mouse/keyboard playtesting.

`MainMap.tscn` and `BattleScene.tscn` now share `reference_game.gd`. Older standalone scripts/scenes remain for historical reference and are not the active presentation. Credentials/tokens stay in memory; use HTTPS/WSS before a remote deployment.
