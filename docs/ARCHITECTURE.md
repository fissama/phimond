# Phimond reconstruction architecture

## Existing system inspected
The existing server/ is Godot GDScript: world owns name-keyed players, a 20×15 map, one pet per player and per-player battles. net/message_router routes HELLO/MOVE/ACTION through a TCP-to-WebSocket Node bridge. storage/player_save writes JSON files. The Phaser/Vite client/ renders primitive creatures and event-driven battle UI. Assets include Pokémon-inspired content. Existing README/IMPLEMENTATION_PLAN describe the superseded architecture. There is no Git repository in this workspace.

Reuse: server-authoritative intent/event separation, data loading approach, event-rendered HP animations, local Docker workflow. Existing code, saves, assets and running server remain available unchanged. New content does not use Pokémon names/assets. Direct code reuse is limited by different languages and protocol.

Conflicts: GDScript server rather than Go; Phaser rather than Godot client; JSON saves rather than MySQL; name-only authentication; fixed species stats with no lineage; no real capture, inheritance, status system, or companion site. New work lives in apps/ and packages/ with data/ definitions. No in-place save conversion.

## Target and first delivery
Go modular monolith: content -> domain -> transactional persistence -> HTTP/WebSocket transport. Godot 4 GDScript renders authoritative snapshots and events. Next.js/React companion reads Go content and account APIs. Static JSON is versioned in data/; rules carry confidence/source metadata. Original presentation is replaceable.

### Backend package layout (spec §3)
The Go server in `apps/game-server/internal/` follows the §3 domain split:

```
internal/
├── auth/          (stub — credential / session primitives to be extracted from transport + persistence)
├── account/       (stub — registration / login handler to be extracted from transport)
├── character/     (Character aggregate + Engine + Apply dispatcher + all *Engine methods)
├── world/         (reserved — world.move / portal / encounter case branches live in character/apply.go today)
├── battle/        (Battle, Unit, ActiveStatus, Buff structs)
├── pet/           (Pet struct)
├── breeding/      (reserved — Inherit / breed / CaptureChance methods live in character/ today)
├── capture/       (reserved — CaptureChance will move here in a follow-up)
├── skill/         (reserved — pet.learn + cast helpers live in character/ today)
├── status/        (reserved — blocked / status mutation helpers live in character/battle_methods.go today)
├── quest/         (reserved — quest.accept / claim / progress live in character/ today)
├── inventory/     (reserved — shop.buy / recipe.learn / pet.heal live in character/ today)
├── economy/       (reserved — gold + trainerXP + petXP live in character/ today; Magic Crystal TBD)
├── auction/       (stub — spec §36, TBD)
├── mail/          (stub — spec §37, TBD)
├── arena/         (reserved — arena.challenge lives in character/ today)
├── party/         (stub — spec §38, TBD)
├── guild/         (stub — spec §38, TBD)
├── chat/          (stub — spec §38, TBD)
├── npc/           (reserved — npc.interact + near() live in character/ today)
├── content/       (data-driven catalog, unchanged)
├── persistence/   (MySQL store, unchanged)
└── transport/     (HTTP / WebSocket server, unchanged structure; imports updated to character/)
```

`character/` keeps the `Engine` orchestrator and the `Apply` dispatcher
together with the `*Engine` methods the dispatcher calls. Moving those
methods into their §3 domain packages would import-cycle through
`Engine.Apply`. The reserved packages exist as directories with a
`package.go` + `README.md` so a follow-up pass can split them out once a
non-cycling dispatch strategy (e.g. a registered interface, or a thin
intermediate) is adopted.

MySQL bootstrap must CREATE a genuinely new database and refuse an existing unmarked schema. A marker identifies the dedicated Phimond schema; migrations only operate inside it. MYSQL_DATABASE/GAME_DB_NAME configurable. No existing DB/schema writes. The supplied hosted MySQL service now contains a newly created dedicated phimond_reconstruction schema; the original database was not targeted.

Each command runs against a character aggregate under SELECT FOR UPDATE; inventory, pets, rewards, ancestry edges, command deduplication and audit records commit together. Character JSON is authoritative for this slice, relational pet ownership and lineage projections are transactionally updated. Battles include seed, PRNG position, commands and events in durable aggregate; replay reads the retained battle record. Movement persists at map changes and checkpoints; gameplay commands commit immediately. The initial implementation persists discrete movement intents as checkpoints; no frame updates. This introduces remote latency and is documented for the next world-ownership phase.

First delivery covers three connected rooms plus ranch/arena, at least ten species, 20+ skills, eight race definitions, seven statuses, pet instance variance, appraisal, learned skills, capture, breeding, strengthening, blessing, lineage, basic quests, inventory/shop and one arena gate. Production-scale social, auction, mail, multi-pet PvP, full original content and polished art remain later phases. No claim of exact formulas.
