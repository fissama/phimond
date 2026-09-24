// Package auth owns account-credential authentication for the Go backend.
//
// It will host the bcrypt-backed credential validation, bearer-token
// lifecycle and WebSocket handshake currently sitting alongside
// persistence.Store and transport.Server. No code has been moved in yet;
// the credential store and token plumbing continue to live in
// internal/persistence and internal/transport to keep this refactor
// behavior-preserving. See docs/PROJECT_REQUIREMENTS.md §3 and the
// websocket-authentication sections of the spec.
package auth