# internal/npc

NPC-domain package — owns the `npc.interact` intent and the
NPC-distance helper (`Engine.near`) currently used by every NPC-gated
intent (appraise, learn, heal, recipe, shop, quest, breed, arena).

Today both the helper and the case branch are in
`internal/character/helpers.go` and `internal/character/apply.go`. They
are kept there because Engine.Apply calls `near` directly; moving them
out would require either lifting `near` onto an interface or letting
this package import `internal/character` (creating a cycle through the
dispatcher).