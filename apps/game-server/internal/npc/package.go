// Package npc will own the NPC distance/interaction helpers split out of
// game/service.go:60-90 (wire namespace `npc.*`).
//
// In this structural refactor the `npc.interact` branch and the `near`
// helper remain in internal/character (apply.go / helpers.go) because
// they are methods on *Engine. A follow-up should move them here once
// the cycle through Engine.Apply is broken.
package npc