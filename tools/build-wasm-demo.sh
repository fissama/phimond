#!/usr/bin/env bash
# Biên dịch engine server thật sang wasm cho bản demo trong trình duyệt.
# Dùng: tools/build-wasm-demo.sh  → apps/game-web/public/engine/{engine.wasm,wasm_exec.js}
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
srv="$root/apps/game-server"
out="$root/apps/game-web/public/engine"
mkdir -p "$out"
rm -rf "$srv/cmd/wasmdemo/data" && cp -R "$root/data" "$srv/cmd/wasmdemo/data"
trap 'rm -rf "$srv/cmd/wasmdemo/data"' EXIT
( cd "$srv" && GOOS=js GOARCH=wasm go build -trimpath -ldflags="-s -w" -o "$out/engine.wasm" ./cmd/wasmdemo )
cp "$(go env GOROOT)/lib/wasm/wasm_exec.js" "$out/wasm_exec.js" 2>/dev/null || cp "$(go env GOROOT)/misc/wasm/wasm_exec.js" "$out/wasm_exec.js"
ls -l "$out"
