// Package quest will own the quest accept / claim / progress handlers
// (wire namespace `quest.*`).
//
// In this structural refactor the case branches stay in
// internal/character/apply.go and the progress helper stays in
// internal/character/helpers.go. A follow-up should move them here
// once the cycle through Engine.Apply is broken.
package quest