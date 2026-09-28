# P10 — Pet model foundation

Status: **design review in progress**, not a phase delivery.

- [Design decisions](P10-design-decisions.md): imported user baseline plus explicit decisions confirmed in this conversation; unresolved sections are labeled.
- [Species roster](P10-roster.md): all 152 original species, Race/Star/Special classification, portraits and exact Special parent pairs.
- [Review queue](P10-review.md): original-game evidence, selected changes and questions to debate one at a time.
- [Verification](P10-verification.md): source and asset checks for the accepted data package.
- `evidence/`: source metadata, decoded roster and compact import summary.

Machine-readable catalog: `data/pets/roster_apk84.json`.
Godot assets: `apps/game-client/assets/pets/apk84/`.

The source catalog/art baseline is approved. Runtime numeric stats, Element
assignment, skills, acquisition routes and legacy save migration are not supplied
by this import. Unknown source server rules must not be filled with guesses.
