// Package world is the future home of map / movement / portal /
//
//	encounter handlers (wire namespace `world.*`).
//
// Per docs/PROJECT_REQUIREMENTS.md §3 the world.* dispatch must live
// here. In this structural refactor the case branches remain inline in
// internal/character.apply.go because the *Engine methods they call are
// defined alongside the dispatcher to avoid an import cycle through
// Engine. A follow-up refactor should move them here once a registration
// or interface-based dispatch strategy is in place.
package world