#!/usr/bin/env python3
"""Build the garden-b contact sheet from current manifest finals."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
COLS = 7
TILE_W, TILE_H = 150, 168


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    assets = manifest["assets"]
    rows = (len(assets) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * TILE_W, rows * TILE_H), (25, 27, 33))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()
    for index, asset in enumerate(assets):
        image = Image.open(ROOT / asset["file"]).convert("RGBA")
        background = Image.new("RGBA", image.size, (25, 27, 33, 255))
        background.alpha_composite(image)
        thumb = background.convert("RGB")
        thumb.thumbnail((TILE_W - 8, TILE_H - 25), Image.Resampling.NEAREST)
        x0, y0 = (index % COLS) * TILE_W, (index // COLS) * TILE_H
        x = x0 + (TILE_W - thumb.width) // 2
        y = y0 + 2 + (TILE_H - 24 - thumb.height) // 2
        sheet.paste(thumb, (x, y))
        draw.text((x0 + 3, y0 + TILE_H - 19), asset["id"], fill=(235, 235, 240), font=font)
    sheet.save(ROOT / "contact-sheet.png")
    print(f"CONTACT SHEET {len(assets)} tiles: {sheet.size}")


if __name__ == "__main__":
    main()
