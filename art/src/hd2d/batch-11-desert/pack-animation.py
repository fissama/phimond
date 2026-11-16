"""Pack already generated/cut frames. No content drawing or frame interpolation."""
from pathlib import Path
import json, sys, shutil, hashlib
from PIL import Image
import numpy as np

root = Path(__file__).resolve().parent
job_dir = root / 'jobs' / sys.argv[1]
job = json.loads((job_dir / 'job.json').read_text())
plan = job['frame_plan']
asset_id = plan['id']
target = root / asset_id
target.mkdir(exist_ok=True)
manifest = json.loads((root / 'manifest.json').read_text())
records = {a['id']: a for a in manifest['assets']}
frame_ids = [a['id'] for a in job['assets']]
frames = [Image.open(root / records[i]['file']).convert('RGBA') for i in frame_ids]
fw, fh = plan['frame_size']
assert all(f.size == (fw, fh) for f in frames)
sheet = Image.new('RGBA', (fw * len(frames), fh))
for index, frame in enumerate(frames):
    sheet.alpha_composite(frame, (index * fw, 0))
sheet.save(target / 'final.png')
for raw in job_dir.glob('raw-*.png'):
    dest = target / raw.name
    if dest.exists() and dest.read_bytes() != raw.read_bytes():
        raise RuntimeError('Refuse to replace preserved animation raw: ' + str(dest))
    shutil.copy2(raw, dest)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
array = np.asarray(sheet)
visible = array[:, :, 3] > 0
colors = len(np.unique(array[:, :, :3][visible], axis=0))
q = dict(id=asset_id, size=list(sheet.size), colors=colors,
         partial_alpha_pixels=int(((array[:, :, 3] > 0) & (array[:, :, 3] < 255)).sum()),
         sha256=sha(target / 'final.png'), raw_integrity=True, failures=[],
         visual_review='pending_actual_4x_and_animation_inspection')
if not 33 <= colors <= 48:
    q['failures'].append('COLORS')
(target / 'qa.json').write_text(json.dumps(q, indent=2) + '\n')
record = dict(records[frame_ids[0]])
record.update(id=asset_id, file=asset_id + '/final.png', px=list(sheet.size),
              size_px=list(sheet.size), frames=len(frames), frame_px=[fw, fh],
              fps=plan['fps'], world=plan['world_size_per_frame'],
              world_size=plan['world_size_per_frame'],
              sha256=q['sha256'], mechanical_status='blocked' if q['failures'] else 'pass',
              pivot_px=[fw // 2, fh], pivot_uv=[.5, 1],
              frame_files=[records[i]['file'] for i in frame_ids])
records[asset_id] = record
aux_path = root / 'aux-manifest.json'
aux = json.loads(aux_path.read_text()) if aux_path.exists() else {'approved': False, 'assets': []}
aux_records = {a['id']: a for a in aux['assets']}
for frame_id in frame_ids:
    aux_records[frame_id] = records.pop(frame_id)
manifest['assets'] = list(records.values())
aux['assets'] = list(aux_records.values())
for path, obj in [(root / 'manifest.json', manifest), (aux_path, aux)]:
    path.write_text(json.dumps(obj, indent=2) + '\n')
refs = '\n'.join(f"{i + 1}. {r['path']} — SHA256 {r['sha256']}" for i, r in enumerate(job['refs']))
(target / 'prompt.md').write_text(
    '# ' + asset_id + '\n\nBuilt-in image_gen; original generated 2x2 sheet preserved.\n\n'
    + job['prompt'] + '\n\nActual ordered attachments:\n' + refs
    + '\n\nPacking only: cut frames registered by translation; no interpolated/recolored frames.\n'
    + job.get('registration_note', '') + '\nRaw SHA256: ' + sha(job_dir / job['raw']) + '\n')
(target / 'frames.json').write_text(json.dumps(dict(
    frames=[dict(index=k, file=records[asset_id]['frame_files'][k],
                 rect=[k * fw, 0, fw, fh], pivot=[fw // 2, fh]) for k in range(len(frames))],
    fps=plan['fps'], loop=True), indent=2) + '\n')
if not (target / 'review.md').exists():
    (target / 'review.md').write_text('DRAFT: full4x and animated QA pending; approved=false.\n')
# QA only: backgrounds and nearest zoom do not become exported game art.
for index, frame in enumerate(frames):
    preview = Image.new('RGBA', frame.size, (22, 27, 34, 255))
    preview.alpha_composite(frame)
    preview.convert('RGB').resize((fw * 4, fh * 4), Image.Resampling.NEAREST).save(target / f'qa-frame4x-{index:02}.png')
previews = []
for frame in frames:
    preview = Image.new('RGBA', frame.size, (22, 27, 34, 255))
    preview.alpha_composite(frame)
    previews.append(preview.convert('RGB').resize((fw * 3, fh * 3), Image.Resampling.NEAREST))
previews[0].save(target / 'qa-loop.gif', save_all=True, append_images=previews[1:],
                 duration=round(1000 / plan['fps']), loop=0, disposal=2)
print(asset_id, len(frames), 'frames', colors, 'colors', q['failures'])
