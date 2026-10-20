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
# Cổng thiết kế P13 (skill/roster candidate V7.1, review server)
(cd "$root/tools/content" && python3 -B -m unittest -q test_p13_design test_p13_roster_review)
(cd "$root/tools/p13_review" && python3 -B -m unittest -q test_server)
cd "$root/apps/web"
npm test
npm run typecheck
cd "$root/apps/game-web"
npm run typecheck
npm test
npm run build
