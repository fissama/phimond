# internal/skill

Skill-domain package — owns `pet.learn` (wire namespace `pet.*`) and
the casting-side status / hit / damage logic split out of battle.go.

Today the corresponding functions are methods on `*character.Engine`:
the `pet.learn` case branch sits in `internal/character/apply.go` and
the `cast` / `blocked` helpers sit in `internal/character/battle_methods.go`.
A follow-up should extract them once the cycle through `Engine.Apply` is
broken (for example by lifting the helpers onto a registered interface).