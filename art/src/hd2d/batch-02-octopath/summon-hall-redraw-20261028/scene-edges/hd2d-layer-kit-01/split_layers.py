from pathlib import Path
from PIL import Image


ROOT = Path(__file__).parent
SOURCE = ROOT.parent / "columns-redraw-01" / "palette-finish" / "raw-01.png"
src = Image.open(SOURCE).convert("RGBA")

# Isolate a clean reusable column with transparent breathing room. The source
# sheet's lintel is cut away; the separate lintel module remains behind props.
column = src.crop((778, 114, 959, 676))
padded = Image.new("RGBA", (column.width + 16, column.height + 16), (0, 0, 0, 0))
padded.alpha_composite(column, (8, 8))
padded.save(ROOT / "raw" / "column-source.png")

# A continuous background trim becomes its own depth layer in the HD-2D scene.
src.crop((132, 4, 2074, 104)).save(ROOT / "raw" / "lintel-module.png")

# Reuse approved candidate sources as independent far/floor layers.
Image.open(ROOT.parent / "city-backdrop" / "final.png").convert("RGBA").save(ROOT / "raw" / "far-city.png")
Image.open(ROOT.parent / "stone-floor" / "final.png").convert("RGBA").save(ROOT / "raw" / "stone-floor.png")
