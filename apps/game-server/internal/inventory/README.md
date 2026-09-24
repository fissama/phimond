# internal/inventory

Inventory-domain package — owns `inventory.*` plus the `shop.buy` and
`recipe.learn` branches that today live in `internal/character/apply.go`.

The character's `Inventory map[string]int` field still lives on
`character.Character` because it is part of the persisted aggregate. A
follow-up should move per-op mutation helpers here once the cycle through
`Engine.Apply` is broken.