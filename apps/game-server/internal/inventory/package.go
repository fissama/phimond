// Package inventory will own the inventory / shop / recipe-learning
// handlers (wire namespaces `inventory.*` and the `shop.*` family).
//
// In this structural refactor the case branches stay in
// internal/character/apply.go because they are inline in the Apply
// dispatcher. A follow-up should move them here once the cycle through
// Engine.Apply is broken.
package inventory