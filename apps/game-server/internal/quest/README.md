# internal/quest

Quest-domain package — owns `quest.accept`, `quest.claim` and the
shared progress helper.

Today the relevant logic is in:

* `internal/character/apply.go` — the `quest.accept` / `quest.claim`
  case branches;
* `internal/character/helpers.go` — the `progress` helper used by
  many intents.

A follow-up should split `progress` into a shared internal package (or
inline it here) and move the quest-specific branches here once the
Engine.Apply cycle is broken.