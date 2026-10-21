#!/usr/bin/env python3
"""Read-only mechanical P10 atlas check (Pillow required; no installs or edits).

RGBA PNG 1124x1405, 4x5 cells of 281px, alpha>0 only in [22,259) per
axis. All 20 cells must be occupied and pixel-distinct (transparent RGB ignored).
Height 55–72% is observational guidance, never a pass/fail gate. Pixel distinction
does not establish meaningful animation. Style, identity consistency, pivot,
row semantics and animation require separate visual review, even after PASS.
Exit 0 mechanical pass, 1 contract failure, 2 input/decode/dependency error.
"""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import sys


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def check(path):
    from PIL import Image
    data = path.read_bytes()
    report = {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
              "status": "fail", "issues": [], "cells": [],
              "occupied_cells": 0, "distinct_cells": 0,
              "visual_review_required": True}
    with Image.open(BytesIO(data)) as atlas:
        report.update(format=atlas.format, mode=atlas.mode, dimensions=list(atlas.size))
        if atlas.format != "PNG":
            report["issues"].append("format")
        if atlas.mode != "RGBA":
            report["issues"].append("mode")
        if atlas.size != (1124, 1405):
            report["issues"].append("dimensions")
        if getattr(atlas, "n_frames", 1) != 1:
            report["issues"].append("animated_image")
        if report["issues"]:
            return report
        atlas.load()
        seen = {}
        for index in range(20):
            x, y = (index % 4) * 281, (index // 4) * 281
            cell = atlas.crop((x, y, x + 281, y + 281))
            alpha = cell.getchannel("A")
            bounds = alpha.getbbox()
            height = bounds[3] - bounds[1] if bounds else 0
            ratio = height / 281
            row = {"index": index, "row": index // 4, "column": index % 4,
                   "alpha_bounds": list(bounds) if bounds else None,
                   "height_pixels": height, "height_cell_ratio": round(ratio, 6),
                   "width_pixels": bounds[2] - bounds[0] if bounds else 0,
                   "scale_observation": "below_typical" if ratio < 0.55 else
                       ("above_typical" if ratio > 0.72 else "typical"),
                   "issues": [], "duplicate_of": None}
            if bounds is None:
                row["issues"].append("empty")
            else:
                report["occupied_cells"] += 1
                if bounds[0] < 22 or bounds[1] < 22 or bounds[2] > 259 or bounds[3] > 259:
                    row["issues"].append("outside_safe_area")
            # RGB under alpha=0 cannot make visually identical frames distinct.
            visible = Image.new("RGBA", cell.size)
            visible.paste(cell, mask=alpha.point(lambda value: 255 if value else 0))
            fingerprint = hashlib.sha256(visible.tobytes()).hexdigest()
            if fingerprint in seen:
                row["duplicate_of"] = seen[fingerprint]
                row["issues"].append("duplicate")
            else:
                seen[fingerprint] = index
            report["cells"].append(row)
        report["distinct_cells"] = len(seen)
    if any(cell["issues"] for cell in report["cells"]):
        report["issues"].append("cell_contract")
    report["status"] = "fail" if report["issues"] else "pass"
    return report


def main(argv=None):
    report = {"status": "error", "atlases": [], "errors": [], "visual_review_required": True}
    try:
        parser = Parser(description=__doc__)
        parser.add_argument("paths", type=Path, nargs="+")
        args = parser.parse_args(argv)
        for path in sorted(set(args.paths), key=str):
            report["atlases"].append(check(path))
        failed = any(atlas["status"] != "pass" for atlas in report["atlases"])
        report["status"] = "fail" if failed else "pass"
        code = 1 if failed else 0
    except (OSError, ValueError, ImportError) as exc:
        report["errors"].append(str(exc))
        code = 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
