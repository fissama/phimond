#!/usr/bin/env python3
"""Extract 9-slice + auxiliary pieces from UI.png + right_btn0.png.

Frame layout in UI.png (520 x 320):
  - Outer frame visible at y=44..275, x=22..508
  - Top corner caps ~y=44-50
  - Top gold band y=48..52 (rgb ~(149,132,81))
  - Top full border y=44..70
  - Middle (interior fill) y=70..250
  - Bottom full border y=250..275
  - Bottom gold band y=268..272

Outputs a set of PNGs in this directory. Re-runs are idempotent.
"""
from PIL import Image
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
UI_SRC = os.path.normpath(os.path.join(
    ROOT, "..", "..", "assets", "reference", "ui", "UI.png"))
BTN_SRC = os.path.normpath(os.path.join(
    ROOT, "..", "..", "assets", "reference", "ui", "right_btn0.png"))

# Calibrated frame coordinates inside UI.png
TL = (22, 44)        # inner corner (just inside the rim)
BR = (508, 275)
BORDER = 14          # corner-piece size in pixels (outer rim thickness)
S = 16               # 9-slice cell size (output pixels)


def _clip(src, box):
    return src.crop(box).convert("RGBA")


def make_panel_9slice():
    """Compose a 3*BORDER x 3*BORDER 9-slice texture.

    Cell layout (3 rows x 3 cols of BORDER x BORDER):
        +-----+--------+-----+
        | TL  |  top   | TR  |
        +-----+--------+-----+
        | lft | mid    | rgt |
        +-----+--------+-----+
        | BL  |  bot   | BR  |
        +-----+--------+-----+
    """
    src = Image.open(UI_SRC).convert("RGBA")
    fx0, fy0 = TL
    fx1, fy1 = BR
    s = BORDER

    tl = _clip(src, (fx0, fy0, fx0 + s, fy0 + s))
    tr = _clip(src, (fx1 - s, fy0, fx1, fy0 + s))
    bl = _clip(src, (fx0, fy1 - s, fx0 + s, fy1))
    br = _clip(src, (fx1 - s, fy1 - s, fx1, fy1))

    # Top edge: 2 px tall horizontal slice across the gold band, then tiled
    top_slice = _clip(src, (fx0 + s, fy0 + s // 2 - 1, fx1 - s, fy0 + s // 2 + 1))
    bot_slice = _clip(src, (fx0 + s, fy1 - s // 2 - 1, fx1 - s, fy1 - s // 2 + 1))

    # Left/right edges: 2 px wide vertical slice, tiled
    left_slice = _clip(src, (fx0 + s // 2 - 1, fy0 + s, fx0 + s // 2 + 1, fy1 - s))
    right_slice = _clip(src, (fx1 - s // 2 - 1, fy0 + s, fx1 - s // 2 + 1, fy1 - s))

    # Middle fill: sampled dark blue interior
    mid = _clip(src, (fx0 + s + 8, fy0 + s + 8, fx0 + s + 24, fy0 + s + 24))
    if mid.size != (s, s):
        mid = mid.resize((s, s))

    # Tile edges to s wide
    def _h_tile(strip, target_w, target_h):
        w, h = strip.size
        if w <= 0 or h <= 0:
            return Image.new("RGBA", (target_w, target_h), (0, 22, 32, 255))
        tiled = Image.new("RGBA", (target_w, h))
        for x in range(0, target_w, w):
            tiled.paste(strip, (x, 0))
        return tiled.resize((target_w, target_h))

    def _v_tile(strip, target_w, target_h):
        w, h = strip.size
        if w <= 0 or h <= 0:
            return Image.new("RGBA", (target_w, target_h), (0, 22, 32, 255))
        tiled = Image.new("RGBA", (w, target_h))
        for y in range(0, target_h, h):
            tiled.paste(strip, (0, y))
        return tiled.resize((target_w, target_h))

    top16 = _h_tile(top_slice, s, s)
    bot16 = _h_tile(bot_slice, s, s)
    left16 = _v_tile(left_slice, s, s)
    right16 = _v_tile(right_slice, s, s)

    out = Image.new("RGBA", (s * 3, s * 3), (0, 0, 0, 0))
    out.paste(tl, (0, 0))
    out.paste(top16, (s, 0))
    out.paste(tr, (s * 2, 0))
    out.paste(left16, (0, s))
    out.paste(mid, (s, s))
    out.paste(right16, (s * 2, s))
    out.paste(bl, (0, s * 2))
    out.paste(bot16, (s, s * 2))
    out.paste(br, (s * 2, s * 2))
    out.save(os.path.join(ROOT, "panel_9slice.png"), "PNG")


def make_inner_fill():
    """8x8 dark-blue tile (interior fill)."""
    img = Image.new("RGBA", (8, 8), (8, 52, 93, 255))
    img.save(os.path.join(ROOT, "panel_inner_fill.png"), "PNG")


def make_lineedit_frame():
    """32x16 horizontal frame strip — taken from UI.png top inner border.

    We sample a strip 32 wide by 16 tall starting just past the corner.
    The top row of pixels shows the gold band; the bottom shows the dark interior.
    """
    src = Image.open(UI_SRC).convert("RGBA")
    fx0, fy0 = TL
    # 32 wide, 16 tall — middle of the top border so we see both the gold band and the interior shadow
    crop = _clip(src, (fx0 + 16, fy0 + 2, fx0 + 16 + 32, fy0 + 2 + 16))
    if crop.size != (32, 16):
        crop = crop.resize((32, 16))
    crop.save(os.path.join(ROOT, "lineedit_frame.png"), "PNG")


def make_chat_panel():
    """64x32 translucent dark-blue panel (chat background)."""
    img = Image.new("RGBA", (64, 32), (8, 20, 38, 200))
    img.save(os.path.join(ROOT, "chat_panel.png"), "PNG")


def make_top_hud():
    """128x16 top status bar (dark blue + thin gold accent on top)."""
    img = Image.new("RGBA", (128, 16), (10, 24, 42, 230))
    for x in range(128):
        img.putpixel((x, 0), (149, 132, 81, 255))
        img.putpixel((x, 1), (149, 132, 81, 180))
    img.save(os.path.join(ROOT, "top_hud.png"), "PNG")


def make_button_corners():
    """Extract the four corners of right_btn0.png."""
    src = Image.open(BTN_SRC).convert("RGBA")
    w, h = src.size
    s = 8
    src.crop((0, 0, s, s)).save(os.path.join(ROOT, "button_tl.png"), "PNG")
    src.crop((w - s, 0, w, s)).save(os.path.join(ROOT, "button_tr.png"), "PNG")
    src.crop((0, h - s, s, h)).save(os.path.join(ROOT, "button_bl.png"), "PNG")
    src.crop((w - s, h - s, w, h)).save(os.path.join(ROOT, "button_br.png"), "PNG")


def main():
    make_panel_9slice()
    make_inner_fill()
    make_lineedit_frame()
    make_chat_panel()
    make_top_hud()
    make_button_corners()
    print("OK - extracted pieces to", ROOT)
    for f in sorted(os.listdir(ROOT)):
        if f.endswith(".png"):
            p = os.path.join(ROOT, f)
            img = Image.open(p)
            non_trans = sum(1 for px in img.getdata() if px[3] > 30)
            total = img.size[0] * img.size[1]
            print(f"  {f:32s} {img.size} non_trans={non_trans}/{total}")


if __name__ == "__main__":
    main()