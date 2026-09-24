// Package arena will own the arena.challenge intent (wire namespace
// `arena.*`).
//
// In this structural refactor the case branch lives in
// internal/character/apply.go because it shares helpers (near, startBattle)
// with other intents. A follow-up should move it here once the cycle
// through Engine.Apply is broken.
package arena