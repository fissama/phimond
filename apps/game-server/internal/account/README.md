# internal/account

Account registration and login orchestration.

Per spec §3, this package is the future home of:

* `/api/register` and `/api/login` HTTP handlers (currently
  `internal/transport/server.go` `credentials`);
* the initial-character payload generation (currently a closure passed
  to `persistence.Store.Register` from `internal/transport/server.go`).

No logic has been moved in this structural refactor. The HTTP routes
remain mounted by `internal/transport/server.go`. A follow-up should
move the handler bodies here and have transport expose them via dependency
// injection so the persistence layer no longer owns account state
// transitions.