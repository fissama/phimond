# internal/status

Status-effect package — owns the `Statuses` / `Buffs` mutation helpers
and the `blocked` predicate originally in `internal/game/battle.go`.

The current implementations live on `*character.Engine` in
`internal/character/battle_methods.go` and are referenced by the battle
dispatcher (also in `internal/character`). They are kept here for cycle
avoidance; a follow-up should split them into dedicated types once the
cycle through `Engine.Apply` is broken.