"""Install the reviewed subset into Phimond, preserving a provenance manifest.

Run from repository root after extraction/composition/export into
tools/.cache/reference/{apk-3.2,rooms,actors}.
"""
import hashlib
import json
from pathlib import Path
import shutil

BASE = Path('tools/.cache/reference')
OUT = Path('apps/game-client/assets/reference')
ROOMS = {'severa': 'level3_QTTP.png', 'forest': 'level4_Map2.png',
         'beach': 'level5_BaiBien.png', 'ranch': 'level3_NongTrai.png',
         'arena': 'level3_DauTruong.png'}
SPECIES = {'snail': 'OCSENHOA', 'flower_fairy': 'YEUTINHHOA',
           'mushroom': 'NAMHOA', 'spider': 'NHENDOC', 'wolf': 'SOINGONGAN',
           'dark_crab': 'CUAHACAM', 'wealth_turtle': 'RUAPHUQUY',
           'treasure_chest': 'QUAIVATRUONGBAU', 'sea_demon': 'TIEUACMA',
           'windmill_spirit': 'CHONGCHONGGIO'}


def main():
    provenance = []
    def copy(src, dest):
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        provenance.append({'path': str(dest), 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
                           'extracted_from': str(src.relative_to(BASE))})
    for key, path in ROOMS.items():
        copy(BASE/'rooms'/path, OUT/'rooms'/f'{key}.png')
    actors = json.loads((BASE/'actors/actors.json').read_text())
    selected = {name: actors[name] for name in ['Boy', 'Girl', *SPECIES.values()]}
    for actor in selected.values():
        for animation in actor.values():
            for frame in animation['frames']:
                copy(BASE/'actors'/frame, OUT/'actors'/frame)
    (OUT/'actors.json').write_text(json.dumps(selected, ensure_ascii=False, indent=2))
    extracted = json.loads((BASE/'apk-3.2/manifest.json').read_text())
    for name in ['UI', 'tableitem', 'tableitem1', 'right_btn0', 'right_btn1', 'right_btn2']:
        asset = next(a for a in extracted['assets'] if a['type'] == 'Texture2D' and a['name'] == name and 'path' in a)
        copy(BASE/'apk-3.2'/asset['path'], OUT/'ui'/f'{name}.png')
    for species, actor in SPECIES.items():
        copy(BASE/'actors'/actors[actor]['idle']['frames'][0], Path('apps/web/public/creatures')/(species+'.png'))
    (OUT/'provenance.json').write_text(json.dumps({
        'source': extracted['source'], 'source_sha256': extracted['sha256'],
        'notes': ['User-supplied APK assets; ownership is not asserted.',
                  'Room/species mappings are reconstruction choices; not a parity claim.',
                  'Animation references are recovered; preview timing is evenly spaced.'],
        'rooms': ROOMS, 'species': SPECIES, 'files': provenance,
    }, ensure_ascii=False, indent=2))
    print(f'Imported {len(provenance)} files; provenance recorded.')


if __name__ == '__main__':
    main()
