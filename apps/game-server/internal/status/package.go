// Package status will own the status-effect helpers split out of
// internal/game/battle.go:80-110 (blocked, status application and
// expiry).
//
// In this structural refactor those helpers remain as *Engine methods in
// internal/character/battle_methods.go so that Engine.Apply can call
// them directly without an import cycle. A follow-up should move them
// here once a non-cycling dispatch strategy exists.
package status