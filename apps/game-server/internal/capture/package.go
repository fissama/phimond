// Package capture will own the capture chance formula and the in-battle
// capture intent (battle.go:188-198 area).
//
// In this structural refactor the formula lives on *Engine in
// internal/character/breeding_methods.go (CaptureChance) and is invoked
// from internal/character/apply.go. A follow-up should move it here
// once the cycle through Engine.Apply is broken.
package capture