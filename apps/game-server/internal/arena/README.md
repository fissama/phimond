# internal/arena

Arena-domain package — owns `arena.challenge`.

The current `arena.challenge` branch in `internal/character/apply.go`
delegates to `Engine.near` and `Engine.startBattle`. Both helpers live
on `*Engine` in `internal/character` for cycle-avoidance reasons, so the
branch is co-located with the dispatcher today. A follow-up should
move it here once a non-cycling dispatch strategy is in place.