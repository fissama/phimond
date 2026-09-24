# internal/capture

Capture-domain package — owns the capture-chance formula and the
in-battle capture intent.

The current implementation is the `CaptureChance` method on
`*character.Engine` (in `internal/character/breeding_methods.go`) and the
"capture" case branch in `internal/character/apply.go` (which lives
inside the `battleMethods`-style dispatcher path). Both will move here
once a non-cycling dispatch strategy is in place.