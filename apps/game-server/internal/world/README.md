# internal/world

World-domain package — owns `world.*` intents (move, portal, encounter).

The case branches currently live in `internal/character/apply.go`
because `Engine.Apply` calls unexported helpers on `*Engine` that
remain in `internal/character` to avoid the package becoming a
circular importer of every domain.

When this package gains its own functions, the dispatcher should call
into them — for example:

```go
// world/world.go (future)
func Move(data *content.Catalog, c *character.Character, d character.Intent) ([]character.Event, error) {...}
func Portal(data *content.Catalog, c *character.Character, d character.Intent) ([]character.Event, error) {...}
func Encounter(data *content.Catalog, c *character.Character, d character.Intent) ([]character.Event, error) {...}
```

— which requires either lifting the helpers onto an interface, or
breaking the cycle another way.