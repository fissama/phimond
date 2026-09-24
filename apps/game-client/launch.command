#!/bin/sh
set -eu
client_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bundled_engine="$client_dir/.tools/Godot.app/Contents/MacOS/Godot"
if [ -x "$bundled_engine" ]; then
  exec "$bundled_engine" --path "$client_dir" "$@"
fi
if command -v godot >/dev/null 2>&1; then
  exec godot --path "$client_dir" "$@"
fi
printf '%s\n' 'Godot is not available. Install Godot 4.3+ or restore the verified engine in .tools/Godot.app.'
exit 1
