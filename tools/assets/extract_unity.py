"""Inventory user-supplied Unity APK/XAPK assets without executing the APK.

Usage: python extract_unity.py INPUT OUTPUT
Requires UnityPy==1.25.3 and Pillow==12.3.0.
Output names include the serialized-file name and object ID to prevent collisions.
"""
import collections
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

import UnityPy


def safe(value):
    return re.sub(r"[^\w.-]+", "_", str(value))[:100] or "unnamed"


def extract(source, output):
    source, output = Path(source), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    entries, errors, counts = [], [], collections.Counter()
    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        apk_data = [outer.read(n) for n in outer.namelist() if n.endswith('.apk')] if source.suffix == '.xapk' else [raw]
        for apk in apk_data:
            with zipfile.ZipFile(io.BytesIO(apk)) as archive:
                for bundle in archive.namelist():
                    if not bundle.endswith('data.unity3d'):
                        continue
                    env = UnityPy.load(archive.read(bundle))
                    for obj in env.objects:
                        kind = obj.type.name
                        counts[kind] += 1
                        if kind not in ('Texture2D', 'Sprite', 'TextAsset', 'AnimationClip', 'MonoScript', 'BuildSettings'):
                            continue
                        entry = {'type': kind, 'id': obj.path_id, 'file': obj.assets_file.name}
                        try:
                            data = obj.read()
                            name = getattr(data, 'm_Name', kind)
                            entry['name'] = name
                            stem = safe(obj.assets_file.name) + '_' + str(obj.path_id) + '_' + safe(name)
                            folder = output / kind
                            folder.mkdir(exist_ok=True)
                            if kind in ('Texture2D', 'Sprite'):
                                im = data.image
                                dest = folder / (stem + '.png')
                                im.save(dest)
                                entry.update(width=im.width, height=im.height, path=str(dest.relative_to(output)))
                            elif kind == 'TextAsset':
                                dest = folder / (stem + '.txt')
                                value = data.m_Script
                                dest.write_bytes(value.encode('utf-8', errors='surrogateescape') if isinstance(value, str) else value)
                                entry['path'] = str(dest.relative_to(output))
                            elif kind == 'BuildSettings':
                                dest = folder / (stem + '.json')
                                tree = obj.read_typetree()
                                dest.write_text(json.dumps({'scenes': tree.get('scenes', []), 'unity_version': tree.get('m_Version')}, ensure_ascii=False))
                                entry['path'] = str(dest.relative_to(output))
                            else:
                                dest = folder / (stem + '.json')
                                dest.write_text(json.dumps(obj.read_typetree(), ensure_ascii=False, default=str))
                                entry['path'] = str(dest.relative_to(output))
                        except Exception as exc:
                            entry['error'] = str(exc)
                            errors.append(entry.copy())
                        entries.append(entry)
    report = {'source': source.name, 'sha256': hashlib.sha256(raw).hexdigest(), 'object_counts': counts, 'assets': entries, 'errors': errors}
    (output / 'manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps({'source': source.name, 'counts': counts, 'exported': len(entries)-len(errors), 'errors': len(errors)}))


if __name__ == '__main__':
    extract(*sys.argv[1:])
