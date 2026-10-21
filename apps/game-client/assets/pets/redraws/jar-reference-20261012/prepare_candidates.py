"""Use the existing P10 packer and preview exporter; preserve all raw pixels."""
from pathlib import Path
import sys, json, hashlib
from PIL import Image

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[5]
sys.path.insert(0, str(PROJECT / 'tools/assets'))
from pack_p10_atlas import pack
from check_p10_atlas import check
from preview_p10_redraw import export

for species in (sys.argv[1:] or ['species_0151', 'species_0143']):
    attempt = 9 if species == 'species_0151' else 11
    folder = ROOT / species / f'attempt-{attempt:02d}'
    source = folder / 'raw.png'
    image = Image.open(source)
    width, height = image.size
    frames = []
    for row in range(5):
        for column in range(4):
            x0, x1 = round(column * width / 4), round((column + 1) * width / 4)
            y0, y1 = round(row * height / 5), round((row + 1) * height / 5)
            if species == 'species_0151' and attempt == 8:
                # Generated source spacing is not exactly regular. These
                # visually reviewed gutter cuts partition the complete raw
                # canvas without discarding any pixels or altering alpha.
                source_rows = [0, 272, 532, 844, 1106, height]
                source_columns = [[0, 293, 567, 836, width],
                                  [0, 294, 573, 843, width],
                                  [0, 291, 591, 857, width],
                                  [0, 293, 567, 840, width],
                                  [0, 291, 583, 862, width]]
                y0, y1 = source_rows[row:row+2]
                x0, x1 = source_columns[row][column:column+2]
            # Full source rectangles retain all pixels. Foot/lamp ground is
            # the last visible row, reviewed on the raw poses; effects also
            # remain intact. One shared scale is calculated by the packer.
            bounds = image.crop((x0, y0, x1, y1)).getchannel('A').getbbox()
            if bounds is None: raise ValueError('Empty source pose')
            frames.append({'rect': [x0, y0, x1-x0, y1-y0],
                           'pivot': [(x1-x0)/2, bounds[3]]})
    # Preserve hopping/hover altitude: all four poses in a row share one
    # source groundline; never align each hopping lamp to its own bottom.
    for row in range(5):
        ground = max(f['pivot'][1] for f in frames[row*4:row*4+4])
        for frame in frames[row*4:row*4+4]: frame['pivot'][1] = ground
    layout = folder / 'layout.json'
    layout.write_text(json.dumps({'destination_pivot': [140, 237], 'frames': frames}, indent=2))
    packed = folder / 'packed.png'
    packing = pack(source, layout, packed)
    (folder / 'packing.json').write_text(json.dumps(packing, indent=2))
    mechanical = check(packed)
    (folder / 'mechanical.json').write_text(json.dumps(mechanical, indent=2))
    if mechanical['status'] != 'pass':
        raise ValueError(species + ' mechanical validation failed')
    preview = export(packed, folder / 'preview')
    result = {'species_id': species, 'status': 'candidate_for_owner_review',
              'candidate_path': str(packed.relative_to(PROJECT)),
              'candidate_sha256': hashlib.sha256(packed.read_bytes()).hexdigest(),
              'mechanical': 'pass', 'generation_calls': attempt,
              'human_approved': False, 'runtime_activated': False,
              'independent_review': 'not yet performed',
              'preview': preview['preview']}
    (ROOT / species / 'result.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
