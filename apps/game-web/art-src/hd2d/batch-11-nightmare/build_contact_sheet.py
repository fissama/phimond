#!/usr/bin/env python3
"""Build the kit contact sheet for visual review.

Only a QA sheet: labels and a checker background are not exported game art.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent


def bg(im, scale=1, dark=False):
    pic = im.convert("RGBA").resize((im.width * scale, im.height * scale),
                                    Image.Resampling.NEAREST)
    if dark:
        b = Image.new("RGBA", pic.size, (22, 27, 34, 255))
    else:
        y, x = np.indices((pic.height, pic.width))
        v = np.where((x // (16 * scale) + y // (16 * scale)) % 2, 65, 94).astype("uint8")
        b = Image.fromarray(np.repeat(v[:, :, None], 3, 2)).convert("RGBA")
    b.alpha_composite(pic)
    return b.convert("RGB")


def fit(im, size, margin=16):
    out = Image.new("RGBA", tuple(size))
    bw, bh = size[0] - margin * 2, size[1] - margin * 2
    s = min(bw / im.width, bh / im.height)
    n = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))),
                  Image.Resampling.NEAREST)
    out.alpha_composite(n, ((size[0] - n.width) // 2, (size[1] - n.height) // 2))
    return out


def main():
    man = json.loads((ROOT / "manifest.json").read_text())
    records = sorted(man["assets"], key=lambda a: a["id"])
    W, H = 640, 400
    sheet = Image.new("RGB", (W * 2, H * ((len(records) + 1) // 2)), (23, 28, 37))
    dr = ImageDraw.Draw(sheet)
    for i, rec in enumerate(records):
        x, y = (i % 2) * W, (i // 2) * H
        p = ROOT / rec["file"]
        if not p.exists():
            continue
        im = Image.open(p).convert("RGBA")
        sheet.paste(bg(fit(im, [W, 340], 16)), (x, y + 30))
        dr.text((x + 12, y + 8), rec["id"] + " / draft", fill=(235, 230, 210))
    sheet.save(ROOT / "contact-sheet.png")
    print("contact sheet:", len(records), "assets", sheet.size)


if __name__ == "__main__":
    main()
