#!/bin/sh
# Fast local gates; live DB/browser tests are explicit and separate.
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root/apps/game-server"
go test -race ./...
go vet ./...
cd "$root"
node tools/check_godot.mjs
node --test tools/load_gameplay_test.mjs
cd "$root/apps/web"
npm test
npm run typecheck
