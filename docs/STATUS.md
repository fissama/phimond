# Delivery status

## Current P00 implementation — 2026-09-23

Active client is LoginScreen → shared `reference_game.gd` world/battle renderer, with four-direction movement, visible-monster contact and source raster art (still POC). P00 adds atomic public combat events, sanitized terminal presentation, auth/read/duplicate no-replay, nullable spawn handling, offline Godot gates, opt-in aggregate metrics and a public-protocol load harness. Existing gameplay formulas and actor art are retained.

Canonical check: `rtk proxy sh tools/check.sh`. Detailed status, limitations, measurements and evidence: [P00 verification](../.ai/plan/phases/P00-baseline/P00-verification.md). Local-server/remote-MySQL baseline at 10 active test accounts completed without worker errors but **failed latency budgets**; this is not 50-CCU certification. Shared world, party and release-quality visuals remain future work.

## Historical delivery — 2026-09-17

Update: first integration of user-supplied APK artwork is complete: five composed room backgrounds, ten mapped creatures, player sprites and source panel art in Godot, plus creature portraits in the companion. See `research/APK_VIDEO_RECONSTRUCTION.md` for extraction counts, video evidence, verification and unresolved fidelity gaps. Earlier procedural-art statements below describe the initial delivery. Full original art/animation and gameplay parity remain incomplete.

## Implemented and exercised

- New Go modular monolith with real MySQL storage and first-frame-authenticated WebSocket.
- Isolated database bootstrap, checksummed migrations, secure defaults plus requested development TLS override.
- 14 species, 29 skills, seven statuses, eight race definitions, six synthesis recipes, five room definitions, five NPCs, five items, four quests.
- Species/instance separation, variance, capture, hidden appraisal, training/XP, skills, strengthening, blessing, synthesis, retired ancestors and recursive lineage.
- Deterministic turn combat, MP, generic statuses/counters/buffs, defend, item consumption, capture, one-step auto, battle resume and bounded historical log.
- Room movement, portals, NPC proximity, shop, quests and one arena tier.
- Godot game client with login, world/battle/ranch/pet/quest/inventory interfaces and procedural original presentation.
- Next.js companion with live encyclopedia, recipe dependency trees, registration/login, owned pets and lineage.
- Server rejects forged result fields, unlearned skills, foreign pets, invalid turns and double quest claims; MySQL serializes and deduplicates costs/rewards.
- Historical sources and conflicting synthesis versions recorded explicitly.

## Verification

Go unit/race tests, two 100,000-attempt distribution simulations, content validation, remote MySQL rollback/concurrency tests, persistent synthesis lineage test, actual HTTP/WebSocket smoke, actual Godot HTTP/WS/resume smoke, Next production build/typecheck/tests, browser account/catalog/planner/ancestry journey and desktop/mobile screenshots. Detailed commands live in README and client READMEs.

## Not completed / not parity claims

Full original species/300+ skill/recipe/quest/drop/map data; original numeric formulas; production balance; actual original art/audio/animation; all historical subrooms/late-game zones; multi-pet/party combat and PvP; spatial player presence; friends/party/guild/chat; auction, bidding, mail and trading; daily/repeatable quest scheduling; unattended auto-grinding; learned skill rank upgrades; full admin/GM tooling; long-lived battle log tables; character selection; inventory capacity and storage limits; load testing, deployment hardening and full online-world position checkpointing.

These are follow-on implementation phases, not working placeholder features. The deliverable is the requested architecture transition plus a lineage-centered first vertical slice. It is not a finished MMORPG or a verified 100% clone.

## Next phases

1. Reduce remote movement latency with map ownership/in-memory positions and timed/map/logout checkpoints; add room presence and multi-pet target selection.
2. Recover and validate version-specific original content, separate ruleset selection from the current hybrid, expand room topology and progression.
3. Transactional auction/bids/mail/trade, followed by party/chat/guild/PvP.
4. Daily content, auto strategies, admin audit/content tooling, assets/animation/audio and production-scale verification.
