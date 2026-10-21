#!/bin/sh
# Chép scene.json + texture từ shared/ vào godot-src/data (đuôi .bin để Godot không import, chỉ đóng gói vào .pck).
cd "$(dirname "$0")/.." || exit 1
rm -rf godot-src/data && mkdir -p godot-src/data/tex
cp shared/scene.json godot-src/data/scene.json.bin
for f in shared/tex/*.png; do cp "$f" "godot-src/data/tex/$(basename "$f").bin"; done
echo ok
