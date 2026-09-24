// Package economy will own gold / trainer-XP / Magic Crystal operations
// split out of game/service.go.
//
// In this structural refactor trainerXP and petXP remain as *Engine
// methods in internal/character (helpers.go and pet_methods.go), and the
// gold mutations are inlined in the case branches in apply.go. Magic
// Crystal operations are spec §3 placeholder only — TBD.
package economy