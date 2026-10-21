"""Compose generated final sprites for QA only; never draws game content."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text())
assets = manifest['assets']
cell_w, cell_h = 480, 320
sheet = Image.new('RGB', (cell_w * 3, cell_h * ((len(assets) + 2) // 3)), (23, 28, 37))
draw = ImageDraw.Draw(sheet)
for i, asset in enumerate(assets):
    folder = root / asset['id']
    qa = json.loads((folder / 'qa.json').read_text())
    if not (folder / 'review.md').exists():
        (folder / 'review.md').write_text('DRAFT — actual final/4x inspection pending. No self pass or Claude approval.\nMechanical failures: ' + ', '.join(qa.get('failures', [])) + '\n')
    pic = Image.open(root / asset['file']).convert('RGBA')
    pic.thumbnail((cell_w - 32, cell_h - 64), Image.Resampling.NEAREST)
    x, y = i % 3 * cell_w, i // 3 * cell_h
    sheet.paste(pic, (x + (cell_w - pic.width) // 2, y + 52 + (cell_h - 64 - pic.height) // 2), pic)
    draw.text((x + 8, y + 8), asset['id'], fill=(235, 230, 210))
    state = 'BLOCKED' if qa.get('failures') else 'draft / visual review pending'
    draw.text((x + 8, y + 27), f"{qa['colors']} colors / {state}", fill=(230, 169, 100) if qa.get('failures') else (170, 190, 175))
sheet.save(root / 'contact-sheet.png')
