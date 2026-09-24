# UI reconstruction verification — 2026-09-23

## Active implementation

`LoginScreen.tscn` → `MainMap.tscn` uses `reference_game.gd`, `classic_hud.gd`, `room.gd`, `reference_menus.gd`, and the `PhimondClient` autoload. `BattleScene.tscn` uses the same persistent composition. Older `MainMap.gd`, `BattleScene.gd`, `main.gd` and standalone NPC/shop scenes remain inactive legacy files; their tests are not proof of the active client.

- Source raster HUD, field combat, six-command platform, target confirmation, floating authoritative damage/heal feedback and turn label.
- Persistent bottom controls/chat, compact world-region pet/quest/inventory overlays, contextual NPC speech/options, source-framed authentication.
- Four-direction keyboard/D-pad movement including visible Y interpolation; catalog map dimensions; click NPC/portal approach; world creature click starts the server's encounter pool selection, not a guaranteed clicked species.
- Skills/items use actual owned data. Appraisal, switching, learning, release, synthesis and strengthening use existing server intents. Release and consuming pet operations require explicit local confirmation.
- Cached artwork, 30Hz field redraw, 10Hz HUD refresh; one pending mutation; timeout/error/disconnect recovery and duplicate event suppression. Go gameplay rules/schema unchanged.

## Executed evidence

Godot 4.7.2 native OpenGL renderer on Apple M3 Pro:

1. Editor import/parse: passed.
2. `visual_audit.gd`: rendered login/world/NPC/pet/inventory/quest/ranch/battle from active scenes; no runtime errors. Multiple iterations fixed menu transparency, unreadable chat shadow, and collapsed pet detail scroll.
3. `world_room_check.gd`: passed cached art, horizontal/vertical preview, reconcile, target/event deduplication, final battle retention.
4. `client_protocol_check.gd`: passed pending cleanup, stale/malformed state, event deduplication, HTTP overlap and reconnect without replay. Its warning lines are intentionally injected failures.
5. `reference_menus_check.gd`: passed page/tab construction, empty/retired pets, explicit consuming confirmations, selected quest dispatch and reward eligibility.
6. `reference_live_check.gd`: real localhost API/MySQL-backed registration, login, catalog, WebSocket, four directions through active UI controller, menu rendering, NPC, purchase, heal, quest accept/progress/reward, portal, battle commands and reconnect/persistence. Random test accounts remain in the dedicated reconstruction database; no credentials are logged.

First live run: 40 acknowledged mutations, median 21ms, maximum 825ms. These are end-to-end request measurements for one session, not an FPS benchmark or a universal no-lag guarantee. Field animation deliberately delays the next command until feedback finishes.

Final expanded run also passed real potion consumption, owned skill dispatch and capture-seal consumption, in addition to attack/defend/flee. Its 41 timed helper mutations measured median 21ms and maximum 679ms; UI-controller battle actions were checked for authoritative results but are not included in that latency sample. Final native capture and menu tests also exited cleanly after release/learning controls were integrated.

## Comparison and limitations

[Side-by-side gallery](ui-comparison-2026-09-23/index.html) includes unaltered primary video frames with true timestamps and deterministic native captures. Reference black recording margins are outside its game area. Fixture creatures/maps/statistics differ from the recorded account.

Original D-pad variant, shield icon, gold HUD chrome, item-icon mapping, particles/timings and exact map topology remain unmatched. Pet equipment/description tabs, nearby-player/party systems and multi-character selection cannot truthfully be reproduced without their corresponding game systems. Existing backend names/descriptions are largely English; user-facing transport/control feedback is Vietnamese. Login/shop/ranch are source-style adaptations because verified footage does not establish those screens. No 100% fidelity claim.

The Mac was locked: CUA could not access the native game window. Native renderer tests and controller-level server integration are complete; direct mouse/keyboard playtesting remains unverified until the Mac is unlocked. No lock bypass was attempted.
