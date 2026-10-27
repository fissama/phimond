"""Compose generated final sprites for QA only; never draws game content."""
from pathlib import Path
import json,sys
from PIL import Image, ImageDraw

root = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text())
assets = list(manifest['assets'])
if (root/'aux-manifest.json').exists():
    seen={a['id'] for a in assets}
    assets += [a for a in json.loads((root/'aux-manifest.json').read_text())['assets'] if a['id'] not in seen]
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
    review = qa.get('visual_review', '')
    state = ('local QA: ' + ','.join(qa['failures'])) if qa.get('failures') else ('self rejected' if 'self_reject' in review else ('self inspected / owner pending' if 'actual' in review and 'inspected' in review else 'draft / inspection pending'))
    draw.text((x + 8, y + 27), f"{qa['colors']} colors / {state}", fill=(230, 169, 100) if qa.get('failures') else (170, 190, 175))
sheet.save(root / 'contact-sheet.png')
# Readable QA pages: avoid automatic downscaling of a very tall overview.
rows_per_page = 4
page_height = rows_per_page * cell_h
for page, top in enumerate(range(0, sheet.height, page_height), 1):
    sheet.crop((0, top, sheet.width, min(top + page_height, sheet.height))).save(root / f'contact-page-{page:02}.png')
