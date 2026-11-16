import hashlib
import json
from pathlib import Path

from PIL import Image


folder = Path(__file__).resolve().parent
first_path = folder / 'elder-side-raw-01.png'
second_path = folder / 'elder-secondhalf-raw-01.png'
first = Image.open(first_path).convert('RGBA')
second = Image.open(second_path).convert('RGBA')
cell_width = second.width // 2
cell_height = second.height // 2
combined = Image.new('RGBA', (cell_width * 4, cell_height * 2), (255, 0, 255, 255))
mapping = []
for index in range(8):
    source = first if index < 4 else second
    source_path = first_path if index < 4 else second_path
    columns = 3 if index < 4 else 2
    source_index = index if index < 4 else index - 4
    source_width = source.width // columns
    source_height = source.height // columns
    left = source_index % columns * source_width
    top = source_index // columns * source_height
    rectangle = (left, top, left + source_width, top + source_height)
    frame = source.crop(rectangle)
    if frame.size != (cell_width, cell_height):
        frame = frame.resize((cell_width, cell_height), Image.Resampling.BOX)
    combined.alpha_composite(frame, ((index % 4) * cell_width, (index // 4) * cell_height))
    mapping.append({'frame': index + 1, 'source': str(source_path), 'source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(), 'rectangle': rectangle, 'uniform_scale': cell_width / source_width})
combined.save(folder / 'elder-combined-raw-02.png')
(folder / 'elder-combined-raw-02.mapping.json').write_text(json.dumps({'operations': 'lossless crop, one uniform source-grid normalization per sheet, row-major packing; no limb edits or mirrored frames', 'mapping': mapping}, indent=2))
