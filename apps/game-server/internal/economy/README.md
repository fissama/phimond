# internal/economy

Economy-domain package — owns gold operations, trainer XP and Magic
Crystal flows.

Today the corresponding code is:

* `internal/character/helpers.go` — `trainerXP`;
* `internal/character/pet_methods.go` — `petXP`;
* gold credits / debits are inlined in each case branch in
  `internal/character/apply.go`;
* Magic Crystal operations are spec §3 placeholder only — TBD.

A follow-up should centralise the gold arithmetic here once the cycle
through `Engine.Apply` is broken.