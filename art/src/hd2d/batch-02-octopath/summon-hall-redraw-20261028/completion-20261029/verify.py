"""Read-only acceptance checks on the six delivered PNGs."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image

out = Path(__file__).resolve().parent
root = out.parent
qa = json.loads((out / 'qa.json').read_text())
assert len(qa['assets']) == 6
for spec in qa['assets']:
    p = root / (spec['name'] + '.png')
    a = np.array(Image.open(p).convert('RGBA'))
    assert [a.shape[1], a.shape[0]] == spec['size']
    limit = 32 if spec['name'].startswith('floor-light') else 48
    assert len(np.unique(a.reshape(-1, 4), axis=0)) <= limit
    assert set(np.unique(a[..., 3])) <= {0, 255}
    assert not np.any((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    assert spec['pass']
    spec['sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()

def load(name):
    return np.array(Image.open(root / name).convert('RGBA'))

floor = load('stone-floor-b.png')
original = load('scene-edges/stone-floor/final.png')
assert np.array_equal(floor[0], original[0])
assert np.array_equal(floor[-1], original[-1])
assert np.array_equal(floor[:, 0], original[:, 0])
assert np.array_equal(floor[:, -1], original[:, -1])
def seams(a):
    a = a[..., :3].astype(float)
    return dict(lr_mae=float(abs(a[:, 0] - a[:, -1]).mean()),
                tb_mae=float(abs(a[0] - a[-1]).mean()),
                interior_lr_mae=float(abs(a[:, 1:] - a[:, :-1]).mean()),
                interior_tb_mae=float(abs(a[1:] - a[:-1]).mean()))

city = load('city-backdrop-wide.png')
roofs = load('city-near-roofs.png')
assert np.all(city[..., 3] == 255)
assert len(np.unique(city[:48, :, :3].reshape(-1, 3), axis=0)) == 1
assert np.all(roofs[-1, :, 3] == 255)
lights = [load(f'floor-light-{n}.png') for n in range(1, 4)]
assert len({hashlib.sha256(a.tobytes()).hexdigest() for a in lights}) == 3
result = dict(status='technical-checks-pass; visual-review-required',
              checks=['6 exact sizes', '6 palette limits including transparent entry',
                      '6 binary alpha checks', '6 no-magenta checks',
                      'floor A/B boundary equality on all four edges',
                      'city opaque with flat top sky', 'roofs flat opaque base',
                      '3 distinct light variants'],
              floor_seams=seams(floor), reference_seams=seams(original),
              roof_seams=seams(roofs),
              floor_interior_changed_fraction=float(np.any(floor[8:-8,8:-8] != original[8:-8,8:-8], axis=2).mean()),
              limitations=qa['warnings'])
(out / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
(out / 'qa.json').write_text(json.dumps(qa, indent=2) + '\n')
print(json.dumps(result, indent=2))
