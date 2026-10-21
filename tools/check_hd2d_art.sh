#!/bin/sh
# Cổng chất lượng art HD-2D (asset + layout). Dùng riêng: sh tools/check_hd2d_art.sh [--all]
set -eu
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec python3 "$root/tools/hd2d_audit/art_gate.py" "$@"
