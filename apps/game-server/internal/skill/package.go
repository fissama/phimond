// Package skill will own skill-related dispatch (the pet.learn intent)
// plus any skill-casting helpers split out of internal/character.
//
// In this structural refactor the pet.learn case branch lives in
// internal/character/apply.go and the skill execution lives in
// internal/character/battle_methods.go (cast). Moving them here would
// cycle through Engine.Apply.
package skill