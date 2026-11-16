import json
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
FINAL = ROOT / "final.png"
Image.open(ROOT / "palette-finish-final-03" / "raw.png").convert("RGBA").save(FINAL)
im = Image.open(FINAL).convert("RGBA")
alpha = im.getchannel("A")
palette_qa = json.loads((ROOT / "palette-finish-final-03" / "apply-qa.json").read_text())
centers = [200, 606, 1012, 1418, 1824, 2230]
qa = {
    "status": "pass" if palette_qa.get("status") == "pass" and im.size == (2432, 384) and alpha.getextrema() == (0, 255) else "fail",
    "asset_id": "summoning-hall-colonnade",
    "file": "final.png",
    "sha256": hashlib.sha256(FINAL.read_bytes()).hexdigest(),
    "dimensions": list(im.size),
    "opaque_colors": len(im.convert("RGB").getcolors(maxcolors=1000000) or []),
    "alpha_extrema": list(alpha.getextrema()),
    "alpha_bbox": list(alpha.getbbox()),
    "column_count": 6,
    "column_centers_px": centers,
    "center_spacing_px": [b - a for a, b in zip(centers, centers[1:])],
    "spacing_even": len(set(b - a for a, b in zip(centers, centers[1:]))) == 1,
    "palette_apply_status": palette_qa.get("status"),
    "palette_apply_checks": palette_qa.get("checks", []),
    "art_source": "host_image",
    "runtime_integrated": False,
    "owner_approval": "pending",
}
(ROOT / "qa.json").write_text(json.dumps(qa, indent=2) + "\n")

reference = Image.open("/Users/phileanh/Downloads/Phimond-P12-Review/map-images/summoning_hall_main_hall.png").convert("RGB")
panel_w, panel_h = 850, 286
old_panel = reference.resize((panel_w, panel_h), Image.Resampling.LANCZOS)

# Candidate composition study: skyline window, aligned columns, then the approved floor tile.
new_panel = Image.new("RGBA", (panel_w, panel_h), (0, 0, 0, 0))
city = Image.open(ROOT.parent / "city-backdrop" / "final.png").convert("RGBA")
city = city.resize((panel_w, round(city.height * panel_w / city.width)), Image.Resampling.LANCZOS)
city_crop = city.crop((0, 110, panel_w, 210)).resize((panel_w, 112), Image.Resampling.LANCZOS)
floor = Image.open(ROOT.parent / "stone-floor" / "final.png").convert("RGBA").resize((192, 192), Image.Resampling.LANCZOS)
for y in range(112, panel_h, floor.height):
    for x in range(0, panel_w, floor.width):
        piece = floor.crop((0, 0, min(floor.width, panel_w - x), min(floor.height, panel_h - y)))
        new_panel.alpha_composite(piece, (x, y))
new_panel.alpha_composite(city_crop, (0, 0))
front = im.resize((panel_w, round(im.height * panel_w / im.width)), Image.Resampling.LANCZOS)
new_panel.alpha_composite(front, (0, 0))

board = Image.new("RGB", (1720, 330), (25, 26, 31))
font_path = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
font = ImageFont.truetype(str(font_path), 18) if font_path.is_file() else ImageFont.load_default()
draw = ImageDraw.Draw(board)
draw.text((20, 6), "V1.0.0", fill=(235, 232, 222), font=font)
draw.text((870, 6), "CANDIDATE — 6 CỘT ĐỀU NHỊP", fill=(235, 232, 222), font=font)
board.paste(old_panel, (10, 34))
board.paste(new_panel.convert("RGB"), (860, 34))
board.save(ROOT / "columns-context-preview.jpg", quality=92)
