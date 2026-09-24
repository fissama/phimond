#!/bin/sh
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ -f "$root/.env" ]; then
  set -a
  . "$root/.env"
  set +a
fi
cd "$root/apps/game-server"
exec go run ./cmd/server "$@"
