// Package breeding is the future home of the breeding / synthesis
// pipeline (wire namespace `breeding.*`).
//
// Per docs/PROJECT_REQUIREMENTS.md §3 the breeding logic must live here.
// In this structural refactor the Inherit, breed and CaptureChance
// methods on *Engine stay in internal/character (breeding_methods.go)
// because they read e.Data and operate on Character — moving them into
// this package would import-cycle through Engine.Apply.
package breeding