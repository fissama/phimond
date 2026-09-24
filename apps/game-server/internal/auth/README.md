# internal/auth

Authentication primitives for the Phimond Go backend.

Per spec §3, this package is the future home of:

* bcrypt credential validation (currently in
  `internal/persistence/store.go` `validateCredentials`);
* the 7-day bearer session lifecycle (`Register`, `Login`,
  `Authenticate`, `Logout` — currently on `persistence.Store`);
* the WebSocket bearer-token handshake currently mixed into
  `internal/transport/server.go` and `internal/transport/live.go`.

No logic has been moved in this structural refactor. The transport layer
still receives a `persistence.Storage` interface and uses it for both
account persistence and auth. A follow-up pass should pull the
credential/session code into `auth/` and have `account/` depend on it.