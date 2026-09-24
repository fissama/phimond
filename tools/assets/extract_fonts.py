"""Extract Font objects (TTF/OTF data) from a Unity APK/XAPK.

The main `extract_unity.py` doesn't handle Font objects. This small script
fills the gap and writes the binary font data (TTF/OTF) directly.

Usage:
    python tools/assets/extract_fonts.py <apk_or_xapk> <output_dir>
"""
from __future__ import annotations

import io
import json
import re
import sys
import zipfile
from pathlib import Path

import UnityPy


def main():
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    if len(sys.argv) > 3:
        subdir = sys.argv[3]
    else:
        # Default: derive subdir from APK name (3.2.apk → v32; 8.4.xapk → v84)
        m = re.search(r"(\d+)\.(\d+)", src.name)
        subdir = f"v{m.group(1)}{m.group(2)}" if m else src.stem
    fonts_dir = out / "fonts" / subdir
    fonts_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out / f"fonts_manifest_{subdir}.json"

    raw = src.read_bytes()
    written = []
    errors = []

    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        apk_data = ([outer.read(n) for n in outer.namelist() if n.endswith(".apk")] if src.suffix == ".xapk" else [raw])
        for apk in apk_data:
            with zipfile.ZipFile(io.BytesIO(apk)) as archive:
                for bundle in archive.namelist():
                    if not bundle.endswith("data.unity3d"):
                        continue
                    env = UnityPy.load(archive.read(bundle))
                    for obj in env.objects:
                        if obj.type.name != "Font":
                            continue
                        try:
                            d = obj.read()
                        except Exception as exc:
                            errors.append({"bundle": bundle, "id": obj.path_id, "err": str(exc)})
                            continue
                        name = (getattr(d, "m_Name", None) or f"font_{obj.path_id}").strip()
                        data = getattr(d, "m_FontData", b"")
                        if isinstance(data, list):
                            data = bytes(data)
                        if not data:
                            continue
                        safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)[:60] or f"font_{obj.path_id}"
                        dest = fonts_dir / f"{safe}_id{obj.path_id}.ttf"
                        dest.write_bytes(data)
                        written.append({"bundle": Path(bundle).stem, "id": obj.path_id, "name": name, "size": len(data), "path": str(dest.relative_to(out))})

    manifest_path.write_text(
        json.dumps({"source": src.name, "subdir": subdir, "fonts": written, "errors": errors}, indent=2, ensure_ascii=False)
    )
    print(json.dumps({"source": src.name, "written": len(written), "errors": len(errors)}, indent=2))


if __name__ == "__main__":
    main()
