// Package account owns account registration and login flows that today
// are served directly from internal/transport.Server.credentials plus
// the persistence-side validateCredentials / Register / Login helpers.
//
// This stub reserves the package per the §3 layout. Implementation will be
// added once auth/ extracts the credential and session plumbing, so the
// account flow can sit on top of an auth.SessionReader/Writer
// abstraction.
package account