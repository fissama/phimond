# internal/breeding

Breeding / synthesis pipeline.

Currently the relevant `*Engine` methods (`Inherit`, `breed`,
`CaptureChance`) live in `internal/character/breeding_methods.go` for the
same cycle-avoidance reasons described in `internal/world/README.md`.

The capture formula `CaptureChance` is a candidate to migrate into
`internal/capture/` once that package gains its own helpers.