"""QA-only collage of generated assets. Native props are never resized."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text())
assets = {a['id']: a for a in manifest['assets']}
scenes = [
    ('01-shicheng-entrance', 'desert-sand-floor-01', [
        ('desert-shicheng-dome-ruin', 500, 850),
        ('desert-entrance-wind-gate', 1450, 900),
        ('desert-cactus-03', 1860, 1200),
        ('desert-small-rock-01', 1000, 1050),
        ('desert-dry-well', 750, 1200),
        ('desert-pottery-urn-broken', 1200, 1200)]),
    ('02-sealed-hulu', 'desert-sand-floor-03', [
        ('desert-sealed-land-disk', 500, 900),
        ('desert-hulu-gourd-pavilion', 1500, 900),
        ('desert-nomad-tent', 800, 1250),
        ('desert-camp-wood-crate', 1150, 1200),
        ('desert-camp-canvas-pack', 1700, 1200),
        ('desert-camp-canvas-sack', 1900, 1200)]),
    ('03-barren-disaster', 'desert-gravel-floor', [
        ('desert-barren-compass-cairn', 450, 900),
        ('desert-disaster-fossil-chasm', 1450, 950),
        ('desert-cactus-dead', 1840, 1250),
        ('desert-camp-charcoal-stove', 400, 1200),
        ('desert-tumbleweed-01', 800, 1150),
        ('desert-small-skull', 1000, 1200)])]
outputs = []
for name, floor_id, props in scenes:
    canvas = Image.new('RGBA', (2048, 1280), (22, 27, 34, 255))
    far = Image.open(root / 'desert-dunes-wall-far/final.png').convert('RGBA')
    # Camera presentation only; source backdrop/floor/prop files stay untouched.
    far = far.resize((2048, 614), Image.Resampling.NEAREST)
    canvas.alpha_composite(far)
    floor = Image.open(root / assets[floor_id]['file']).convert('RGBA')
    for y in range(512, 1280, 512):
        for x in range(0, 2048, 512):
            canvas.alpha_composite(floor, (x, y))
    placed = []
    for asset_id, cx, foot in sorted(props, key=lambda a: a[2]):
        pic = Image.open(root / assets[asset_id]['file']).convert('RGBA')
        bounds = pic.getbbox()
        px, py = cx - pic.width // 2, foot - bounds[3]
        assert px + bounds[0] >= 0 and px + bounds[2] <= 2048, asset_id
        assert py + bounds[1] >= 0 and py + bounds[3] <= 1280, asset_id
        shadow_id = ('desert-shadow-small-01' if bounds[2] - bounds[0] < 192
                     else 'desert-shadow-large-01')
        shadow = Image.open(root / assets[shadow_id]['file']).convert('RGBA')
        canvas.alpha_composite(shadow, (cx - shadow.width // 2, foot - shadow.height // 2))
        canvas.alpha_composite(pic, (px, py))
        placed.append(dict(id=asset_id, source=assets[asset_id]['file'],
                           sha256=hashlib.sha256((root / assets[asset_id]['file']).read_bytes()).hexdigest(),
                           top_left_px=[px, py], source_size_px=list(pic.size),
                           scale=1, resampling=False))
    # QA annotations are not exported art.
    draw = ImageDraw.Draw(canvas)
    draw.line([(64, 1100), (64, 932)], fill=(235, 230, 210), width=3)
    draw.line([(56, 1100), (72, 1100)], fill=(235, 230, 210), width=3)
    draw.line([(56, 932), (72, 932)], fill=(235, 230, 210), width=3)
    draw.text((82, 940), 'PLAYER 168px / 1.31world', fill=(235, 230, 210))
    draw.text((20, 18), 'QA ONLY / ' + name + ' / all props native 1:1', fill=(60, 50, 40))
    filename = 'qa-composition-' + name + '.png'
    canvas.convert('RGB').save(root / filename)
    outputs.append(dict(file=filename, floor=floor_id, props=placed))
(root / 'qa-compositions.json').write_text(json.dumps(dict(
    purpose='Flat image collages for palette/scale review only; no runtime/scene edits.',
    canvas_px=[2048, 1280], pixels_per_world_unit=128,
    player_height_px=168, player_height_world=1.31,
    backdrop_presentation='QA camera fit only; exported backdrop remains unchanged.',
    prop_resampling=False, approved=False, scenes=outputs), indent=2) + '\n')
print('Created 3 QA collages, 6 distinct props per scene, all prop pixels 1:1.')
