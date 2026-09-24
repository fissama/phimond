# Contact combat and movement playtest

## Root causes and changes

The previous field creatures were illustrative pool previews. Walking had no contact check; clicking sent an unqualified random encounter. Map catalog now publishes stable `wild_spawns` with identity/species/coordinates. The client draws those positions and requests the contacted spawn after an acknowledged move. Server validation rejects remote, foreign-map and invalid IDs, then starts the correct species using existing battle calculations. Legacy random encounters remain compatible. No MySQL migration or balance change.

Movement reached each grid target in ~71ms but issued steps at 180ms, leaving a visible pause. Interpolation now takes the full step interval. Field redraw follows native frame cadence instead of a timer that discarded fractional time. Mutation serialization and authoritative correction remain intact.

Contact is latched after encounter so standing still on the creature does not immediately restart combat after flee. Leaving and returning re-arms it; clicking explicitly approaches/re-engages. Contact remains a separate durable action after movement, preserving the existing persistence/checkpoint boundary.

## Verification

- Before fix: server test rejected the new spawn identifier; client motion test reproduced early step completion. Both passed after implementation.
- Full `go test ./...`: passed, including wrong/remote spawn rejection and state preservation.
- `contact_check.gd`, `world_room_check.gd`, `client_protocol_check.gd`: passed. Protocol warnings are deliberate fault injections.
- Native `contact_live_check.gd` with live server: walking contact → correct snail → attack → flee → no standing retrigger → click approach → same species, passed.
- A concurrent native test timed out on leaving contact when switching focus to the manual game cleared held input. Re-running without competing UI interaction passed; do not run interactive native tests in parallel.
- Final 120-frame native sample: median 8.27ms, p95 10.06ms on this Mac. This is observed frame cadence for the sampled field, not a whole-game performance guarantee.
- Direct Computer Use: Right-key movement at forest (9,10) → (10,10) → (11,10) entered snail combat. Mouse selected Attack and opponent; next screenshot showed turn 2, opponent 51/59 HP and player 56/62 HP. Mouse selected Flee; field returned without retriggering. [Live screenshot after flee](ui-comparison-2026-09-23/contact-playtest-field.png).

Local server was gracefully restarted to load the extended catalog. Test accounts are confined to the existing reconstruction database. A separate temporary copy of the installed engine (`/tmp/PhimondPlaytest.app`, locally signed) disambiguated game windows from the user's Godot editor for direct playtesting. The latest game remains open near the forest snail for the user.

Spawn placement is a reconstructed contact layout derived from existing map pools, not claimed to reproduce original historical spawn coordinates or a persistent multiplayer creature population.
