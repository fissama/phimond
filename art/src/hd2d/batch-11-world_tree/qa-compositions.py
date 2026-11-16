"""QA-only map-scale mockups over the source-map references; never exported to runtime."""
from pathlib import Path
import json, hashlib
from PIL import Image

root = Path(__file__).resolve().parent
repo = root.parents[4]
refs = repo / '.ai/design/map-checklists/refs'
manifest = json.loads((root / 'manifest.json').read_text())
assets = {a['id']: a for a in manifest['assets']}
# Coordinates are screen pixels in the 1400x map-reference preview. Scale approximates
# the source screenshot's 100 px/world-unit versus kit art's 128 px/world-unit.
scenes = [
    ('world_tree_gate', 'world_tree_gate.jpg', [
        ('world_tree-portal-dormant', .40, 990, 220, 'portal arch at existing central doorway'),
        ('world_tree-prop-07', .32, 300, 380, 'giant mushroom at left path edge'),
        ('world_tree-prop-10', .40, 590, 390, 'branch stairs on path foreground')]),
    ('world_tree_deep_woods', 'world_tree_deep_woods.jpg', [
        ('world_tree-decal-02', .42, 160, 455, 'shared moss-root rosette at foreground edge'),
        ('world_tree-prop-01', .32, 360, 330, 'buttress root at left'),
        ('world_tree-prop-05', .35, 1040, 330, 'giant leaf at right')]),
    ('world_tree_secret_chamber', 'world_tree_secret_chamber.jpg', [
        ('world_tree_secret_chamber-landmark-01', .42, 690, 380, 'central forked trunk landmark'),
        ('world_tree-portal-active', .35, 460, 365, 'active portal near left entry'),
        ('world_tree-prop-08', .35, 1100, 380, 'glowing sacred fruit on right ledge')]),
]
report=[]
for map_id, ref_name, placements in scenes:
    bg_path=refs/ref_name
    canvas=Image.open(bg_path).convert('RGBA')
    placed=[]
    for asset_id, scale, cx, foot, note in sorted(placements,key=lambda p:p[3]):
        a=assets[asset_id]; path=root/a['file']; src=Image.open(path).convert('RGBA')
        size=(round(src.width*scale), round(src.height*scale))
        im=src.resize(size,Image.Resampling.NEAREST)
        alpha=im.getchannel('A'); box=alpha.getbbox()
        px=cx-size[0]//2; py=foot-box[3]
        canvas.alpha_composite(im,(px,py))
        placed.append({'id':asset_id,'file':a['file'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                       'source_size_px':list(src.size),'preview_scale':scale,'preview_size_px':list(size),
                       'top_left_px':[px,py],'foot_anchor_px':[cx,foot],'note':note})
    out=f'qa-composition-{map_id}.png'; canvas.convert('RGB').save(root/out)
    report.append({'map_id':map_id,'source_map':str(bg_path.relative_to(repo)),
                   'source_map_sha256':hashlib.sha256(bg_path.read_bytes()).hexdigest(),
                   'file':out,'canvas_px':list(canvas.size),'placements':placed})
(root/'qa-compositions.json').write_text(json.dumps({'purpose':'Visual QA mockups only; placement and preview scaling are approximate, no runtime/map data is changed.','approved':False,'maps':report},indent=2)+'\n')
print('Created 3 QA-only map mockups.')
