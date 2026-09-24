# Classic gameplay reconstruction and latency repair

User request: play-test and rebuild the UI/battle experience to match the supplied APK/video, and repair gameplay lag. Existing reconstruction is authorized; no deployment or unrelated account changes.

Design: 960×640 logical game viewport with the field filling the upper ~70%, source HUD around its edges, bottom D-pad/log/confirm controls, and transient blue/gold menus over the field. Combat stays in the field with selection, source actor animations and authoritative feedback. No permanent desktop sidebar. Preserve existing server-authoritative economics and the known current content while making available gameplay accessible through the classic flow.

1. Backend owner: benchmark live HTTP/WS; reduce remote database work, implement authoritative low-latency movement with safe persistence boundaries, and distinguish temporary storage errors from expired sessions. Regression tests for concurrency, durability boundaries and logout.
2. Field owner: full-stage scene rendering, proportional source actors/NPCs, targeting, movement interpolation/reconciliation, battle animations and HP/damage feedback; preload/cache textures outside drawing.
3. Reference owner: recover and document original HUD sprite regions and compare representative video frames.
4. Main owner: classic HUD and overlay menus, compact skill/item/capture commands, held movement, responsive pending feedback, real auto-action loop, source HUD integration, no per-movement menu reconstruction.
5. Integration: run Godot/Go tests, benchmark after restarting server, native rendered screenshots, exercise UI controls and a real account gameplay path. Record gaps without claiming undocumented original formulas or full MMO parity.

Interfaces: room exposes set_snapshot(character,catalog), preview_move(direction), cancel_preview(), and NPC/portal/enemy/target/ground signals. HUD exposes world, menu content, log/status labels and user-intent signals. Backend retains existing auth/WS envelopes and operations so UI can be developed independently.

Ruling: workspace has no Git metadata; edit authorized files directly and keep an explicit report instead of inventing a branch or commit. The supplied video is the visual reference; APK 3.2 provides available source sprites. Source latency test completed in 56.99s before this change. Gameplay formulas remain labeled reconstructed until verifiable evidence exists.
