# P11 — Layout delivery gate repair, 2026-10-12

Scope: repair obsolete client verification; no P11 runtime activation or UI change.

## Cause and behavior

The old audit expected a 360×480 login window at (300,80), but the current scene
uses a centered 491×264 window. It read anchors synchronously before layout,
observing negative offsets instead of the actual centered position (234.5,188).
BattleScene now builds the reference HUD dynamically and has no Window node.
These two failures blocked the mandatory smoke gate; they were unrelated to
stat formulas. The old fallback could accept uncomputed battle layout and the
script lacked the canonical positive PASS: marker.

The repaired audit waits two process frames, checks actual full viewport roots,
login/NPC/shop rectangles, the battle world rectangle, and required HUD/action
controls inside the 960×640 viewport. It checks six battle buttons and rejects
missing/empty/offscreen controls. It checks the menu even while hidden.
No fallback accepts incomplete layout. The canonical Godot runner includes it.

## Verification

- Original audit reproduced: exit 1, login and missing battle Window failures.
- Repaired audit: exit 0 with PASS: marker.
- Temporary negative fixture changed expected login coordinates to old values:
  exit 1, incorrect LoginScreen/Window geometry detected, no PASS: marker;
  fixture removed afterward.
- tools/check.sh passed: server race tests/vet, six Godot checks including contact
  and layout, seven load harness tests, three web planner tests and typecheck.
- Server rebuild passed; min_smoke completed with its existing overall PASS output.

## P11 status

Layout is no longer a closure blocker. P11 remains open for the owner-directed
catalog identity revision: seven other Race profiles, Species distinctions,
authored descriptions and Element coverage. Earlier handoff failure records are
historical evidence and are not rewritten as if they passed.
