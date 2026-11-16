from pathlib import Path
from PIL import Image


ROOT = Path(__file__).parent
SOURCE = ROOT / "palette-finish" / "raw-01.png"
OUT = ROOT / "assembled-03"
OUT.mkdir(exist_ok=False)

src = Image.open(SOURCE).convert("RGBA")
width, height = 2432, 384
header_h = 60
col_h = 300
layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))

# Keep the continuous carved lintel, but fit its height to the reference scene.
lintel = src.crop((132, 4, 2074, 108)).resize((width, header_h), Image.Resampling.LANCZOS)
layer.alpha_composite(lintel, (0, 0))

# Measured source boxes around each identical column, excluding the shared lintel.
boxes = [(12, 101, 181, 676), (418, 101, 591, 676), (778, 101, 959, 676),
         (1116, 101, 1287, 676), (1487, 101, 1662, 676), (1878, 101, 2058, 676)]
centers = [200, 606, 1012, 1418, 1824, 2230]
for box, center in zip(boxes, centers, strict=True):
    pillar = src.crop(box).resize((round((box[2] - box[0]) * col_h / (box[3] - box[1]) * 1.5), col_h), Image.Resampling.LANCZOS)
    x = center - pillar.width // 2
    layer.alpha_composite(pillar, (x, header_h - 8))

layer.save(OUT / "raw.png")

# Context board: show the new colonnade over the same v1.0.0 crop, clearly marked as a mockup.
reference = Image.open("/Users/phileanh/Downloads/Phimond-P12-Review/map-images/summoning_hall_main_hall.png").convert("RGBA")
preview_w = 1600
preview_h = round(reference.height * preview_w / reference.width)
reference = reference.resize((preview_w, preview_h), Image.Resampling.LANCZOS)
strip_h = round(preview_h * 0.39)
preview = reference.copy()
city = Image.open(ROOT.parent / "city-backdrop" / "final.png").convert("RGBA")
city = city.resize((preview_w, strip_h), Image.Resampling.LANCZOS)
preview.alpha_composite(city, (0, 0))
front = layer.resize((preview_w, round(height * preview_w / width)), Image.Resampling.LANCZOS)
preview.alpha_composite(front, (0, 0))
preview.convert("RGB").save(OUT / "columns-context-preview.jpg", quality=92)
