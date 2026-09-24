# Implemented gameplay rules

The Go server alone resolves gameplay. Godot submits intentions; Next.js reads definitions/account state. Data is loaded and validated at server startup; restart after editing it.

## Pets and inheritance

Species describe reusable race/element/star/base stats/learnable skills. Persistent individuals have stable IDs, gender, seven qualities, growth, resistances, known skills, XP, star, generation, refinement, parents, appraisal state, strengthening and blessing. New captures keep the actual encountered individual; hidden qualities are not transmitted until appraisal.

Derived stats are centralized in `apps/game-server/internal/character/pet_methods.go::Recalculate`: species base × quality/1000 plus level × growth/100 × star. Stamina contributes HP, spirit MP, strength physical attack, intelligence magic attack, agility speed; defense/critical have separate values. Scaling/caps are reconstructed.

Synthesis validates proximity, parents, ownership, recipe knowledge, species order, configurable level/gender/star/race restrictions, materials and gold. Child generation is max parental generation + 1. Quality is parental average + configurable generation gain + strengthening/blessing + bounded mutation. Growth and both resistance maps inherit separately. Eligible **learned** parental skills are sorted and independently sampled; species pools are never silently inherited. Parent-consuming recipes retire both parents and keep ancestry. Strengthening uses a same-star inactive donor and is separate from training. No real-money items exist.

## Battle

One active player pet versus one enemy in the first slice. The battle records seed/RNG, turn, commands and events. Phase transitions: WAIT_COMMAND, LOCK_COMMANDS, CALCULATE_ORDER, EXECUTE_ACTIONS, APPLY_END_TURN_EFFECTS, CHECK_VICTORY, then next turn or FINISHED. Speed determines execution order; valid Defend covers the entire round. Input must name current battle/turn. Learned skill and MP validation precedes RNG/costs.

Generic status definitions express action blocks, wake-on-damage, defense/hit multipliers, fatal countdown and random targeting. Skills support damage, status, healing, cleansing and stat buffs. Buffs refresh by stat and expire; HP/MP cap changes are applied. Tie order is stable. Confusion can target either living unit; a confused support action can mis-target. Cleanse/heal to self does not use Blind's attack penalty. Current content includes no enemy-targeted debuff skills, though modifier <1 can express them.

Capture consumes a seal and depends on species, HP, trainer/target level, star, status and battle RNG. Dead/arena/uncatchable targets cannot be captured. Capture and wins give reconstructed XP/gold; losses/flee do not. Potions/ether consume inventory. Auto currently delegates one turn to server basic attack; autonomous grinding is not yet implemented.

## World and progression

Five rooms with X/Y movement: city, forest, beach, ranch, arena. The active Godot client moves in four directions and starts a server-validated encounter after contact with a visible creature. Contact uses both axes and a latch preventing immediate re-entry after fleeing; legacy random-pool encounter remains supported. NPC/portal proximity still has an X-only server gap assigned to P01; collision/pathfinding is not complete. NPCs offer training, healing, shopping, appraisal, recipe study and synthesis. Four quests are accepted, progressed by server events, and claimed once. Arena I (level 10) unlocks the beach.

P00 presents `data.events` from the public response, retains sanitized final battle visuals when authoritative battle is already null, and locks exploration until feedback completes. Auth/read/retry do not replay previous events. No damage/capture/progression formula changed for this presentation fix.

One character/account and one active combat pet are current limits. Party combat, multi-pet formation, PvP, regional presence, social communication and later zones need further implementation. The numeric balance is editable, not historically certified.
