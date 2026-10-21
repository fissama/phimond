#!/usr/bin/env python3
"""Read-only P10 redraw inventory, hash preflight and batch prompt renderer."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / '.ai/plan/phases/P10-pet-model/redraw-kit'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(manifest, root=ROOT):
    jobs = manifest['jobs']
    records = json.loads((root / 'data/p10/species.json').read_text())['records']
    excluded = {'DocDangNu', 'DaoThienDuong'}
    errors = []
    expected = {key for key, value in records.items()
                if Path(value['assets']['portrait']).parent.name not in excluded}
    if len(jobs) != 150 or {j['species_id'] for j in jobs} != expected:
        errors.append('Expected exactly the 150 canonical IDs excluding the two style anchors')
    if len({j['output_dir'] for j in jobs}) != 150:
        errors.append('Duplicate output directories')
    if manifest['batch_count'] != 30 or manifest['batch_size'] != 5:
        errors.append('Expected 30 batches of 5')
    if any(sum(j['batch'] == b for j in jobs) != 5 for b in range(1, 31)):
        errors.append('Invalid batch membership')
    if {a['source_species_id'] for a in manifest['anchors']} != excluded:
        errors.append('Invalid style anchors')
    paths = [(a['path'], a['sha256']) for a in manifest['anchors']]
    for job in jobs:
        record = records.get(job['species_id'], {})
        source_id = Path(record.get('assets', {}).get('portrait', '')).parent.name
        if source_id != job['source_species_id']:
            errors.append(f"{job['species_id']}: source mapping mismatch")
        for key in ('race_id', 'star', 'species_class'):
            if record.get(key) != job[key]:
                errors.append(f"{job['species_id']}: {key} mismatch")
        for key, leaf in (('source_portrait', 'portrait.png'), ('source_atlas', 'sprites.png')):
            expected_path = f'apps/game-client/assets/pets/apk84/{source_id}/{leaf}'
            if job[key] != expected_path:
                errors.append(f"{job['species_id']}: {key} path mismatch")
            paths.append((job[key], job[key + '_sha256']))
        if job['output_dir'] != 'apps/game-client/assets/pets/redraws/batches/20261005/' + job['species_id']:
            errors.append(f"{job['species_id']}: output scope mismatch")
    for relative, expected_hash in paths:
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append(f'Path escapes workspace: {relative}')
        elif not path.is_file() or digest(path) != expected_hash:
            errors.append(f'Missing or changed input: {relative}')
    return errors


def render(manifest, batch):
    jobs = [j for j in manifest['jobs'] if j['batch'] == batch]
    parts = [(KIT / 'worker-prompt.md').read_text(),
             f'\n## Assigned batch {batch:02d} — exactly five species\n',
             'Workspace: `/Users/phileanh/rust/phimond`\n',
             'Run from workspace root:\n```sh\n'
             f'rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch {batch}\n```\n',
             'Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`\n',
             'Repair/review templates and exact tool commands are in the same kit README.\n']
    for anchor in manifest['anchors']:
        parts.append(f"Style anchor: `{anchor['path']}` SHA256 `{anchor['sha256']}`\n")
    for job in jobs:
        parts.append(f"\n### {job['species_id']} — {job['display_name_vi']}\n\n```json\n"
                     + json.dumps(job, indent=2, ensure_ascii=False) + '\n```\n')
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['list', 'check-inputs', 'prompt'])
    parser.add_argument('--batch', type=int, choices=range(1, 31))
    args = parser.parse_args()
    manifest = json.loads((KIT / 'manifest.json').read_text())
    errors = validate(manifest)
    if errors:
        print(json.dumps({'status': 'fail', 'errors': errors}, ensure_ascii=False, indent=2))
        return 1
    selected = [j for j in manifest['jobs'] if args.batch is None or j['batch'] == args.batch]
    if args.command == 'check-inputs':
        print(json.dumps({'status': 'pass', 'verified_jobs': 150, 'style_anchors': 2,
                          'selected_jobs': len(selected), 'artwork_accepted': False}, indent=2))
    elif args.command == 'prompt':
        if args.batch is None:
            parser.error('prompt requires --batch')
        print(render(manifest, args.batch))
    else:
        for job in selected:
            print(f"{job['batch']:02d}\t{job['species_id']}\t{job['source_species_id']}\t{job['display_name_vi']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
