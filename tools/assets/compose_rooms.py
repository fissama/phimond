"""Render static Unity room groups from their serialized sprite transforms.

This is a reference compositor, not a Unity runtime: reports rotated/tiled
sprites instead of silently pretending to reproduce unsupported rendering.
Usage: python compose_rooms.py APK OUTPUT
"""
import json
from pathlib import Path
import sys
import zipfile
from collections import defaultdict
from PIL import Image, ImageChops
import UnityPy
from extract_unity import safe


def compose(source, output):
    out = Path(output)
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source) as z:
        env = UnityPy.load(z.read('assets/bin/Data/data.unity3d'))
    groups = defaultdict(list)
    skipped = []
    for obj in env.objects:
        if obj.type.name != 'SpriteRenderer' or not obj.assets_file.name.startswith('level'):
            continue
        d = obj.read()
        if not d.m_Enabled or not d.m_Sprite.path_id:
            continue
        go = d.m_GameObject.read()
        transform = next((c.component.read() for c in go.m_Component if c.component.type.name == 'Transform'), None)
        if transform is None:
            continue
        chain = [transform]
        while chain[-1].m_Father.path_id:
            chain.append(chain[-1].m_Father.read())
        root_name = chain[-1].m_GameObject.read().m_Name
        if root_name in ('AllNpc', 'AllEnemy', 'BOX', 'Door') or go.m_Name in ('Mini', 'ImgQuest'):
            continue
        if any(abs(t.m_LocalRotation.z) > .0001 or abs(t.m_LocalRotation.x) > .0001 or abs(t.m_LocalRotation.y) > .0001 for t in chain) or d.m_DrawMode != 0:
            skipped.append({'scene': obj.assets_file.name, 'name': go.m_Name, 'reason': 'rotation or non-simple draw mode'})
            continue
        x = y = 0
        sx = sy = 1
        for t in reversed(chain):
            x += t.m_LocalPosition.x * sx
            y += t.m_LocalPosition.y * sy
            sx *= t.m_LocalScale.x
            sy *= t.m_LocalScale.y
        sprite = d.m_Sprite.read()
        im = sprite.image.convert('RGBA')
        # Exported sprite dimensions and pivot are in source-pixel space.
        ppu = sprite.m_PixelsToUnits
        width, height = im.width / ppu * abs(sx), im.height / ppu * abs(sy)
        flip_x, flip_y = bool(d.m_FlipX) != (sx < 0), bool(d.m_FlipY) != (sy < 0)
        pivot_x = 1-sprite.m_Pivot.x if flip_x else sprite.m_Pivot.x
        pivot_y = 1-sprite.m_Pivot.y if flip_y else sprite.m_Pivot.y
        if flip_x:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if flip_y:
            im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        tint = tuple(round(getattr(d.m_Color, c)*255) for c in 'rgba')
        im = ImageChops.multiply(im, Image.new('RGBA', im.size, tint))
        groups[(obj.assets_file.name, root_name)].append((d.m_SortingLayer, d.m_SortingOrder, x-width*pivot_x, y+height*(1-pivot_y), width, height, im))
    rooms = []
    for (scene, name), sprites in groups.items():
        if len(sprites) < 4:
            continue
        left = min(s[2] for s in sprites)
        top = max(s[3] for s in sprites)
        right = max(s[2]+s[4] for s in sprites)
        bottom = min(s[3]-s[5] for s in sprites)
        scale = min(100, 4096/max(right-left, top-bottom, 1))
        canvas = Image.new('RGBA', (max(1, round((right-left)*scale)), max(1, round((top-bottom)*scale))))
        for _, _, x, y, w, h, im in sorted(sprites, key=lambda s: (s[0],s[1])):
            im = im.resize((max(1,round(w*scale)),max(1,round(h*scale))),Image.Resampling.NEAREST)
            canvas.alpha_composite(im,(round((x-left)*scale),round((top-y)*scale)))
        dest = out / (safe(scene+'_'+name)+'.png')
        canvas.save(dest)
        rooms.append({'scene': scene,'group':name,'path':dest.name,'sprites':len(sprites),'bounds':[left,bottom,right,top],'pixels_per_unit':scale})
    (out/'rooms.json').write_text(json.dumps({'rooms':rooms,'skipped':skipped},ensure_ascii=False,indent=2))
    print(json.dumps({'rooms':len(rooms),'unsupported_sprites':len(skipped)}))


if __name__ == '__main__':
    compose(*sys.argv[1:])
