#!/usr/bin/env python3
"""Pack 20 explicit poses using one nearest-neighbor scale; never overwrite.

Usage: pack_p10_atlas.py --source raw.png --layout layout.json --output new.png
Layout JSON (exactly 20 frames in row-major output order):
{"destination_pivot": [140, 237], "frames": [
  {"rect": [x, y, width, height], "pivot": [local_x, local_y]}, ...]}
Rectangles use integer source-pixel edges; pivots use finite local pixel-edge
coordinates, including rectangle boundaries. Destination pivot is in [22,259).
All visible source pixels (alpha>0) must belong to exactly one rectangle.

Source rectangles and RGBA pixels are not repaired or alpha-thresholded. One
common scale fits all alpha bounds around a shared destination pivot; output
is a 1124x1405 RGBA PNG with 4x5 cells of 281px. Normal nearest-neighbor
resampling may lose subpixel detail when shrinking; inspect poses visually.
Typical body height 155–202px is guidance, not a machine gate. Pivots/rectangles
are human inputs, not inferred anatomy. Run check_p10_atlas.py separately and
review style/identity/animation before accepting any output.
Stdout JSON includes hashes and geometry. Exit 0 packed; 2 invalid input/error.
"""
import argparse
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
import sys


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate layout key: " + key)
        result[key] = value
    return result


def point(value, name):
    require(isinstance(value, list) and len(value) == 2 and
            all(type(v) in (int, float) and math.isfinite(v) for v in value),
            name + " must contain two finite numbers")
    return value


def pack(source_path, layout_path, output_path):
    from PIL import Image
    require(source_path.resolve() != output_path.resolve(), "output must differ from source")
    require(not output_path.exists() and not output_path.is_symlink(), "output already exists")
    source_data = source_path.read_bytes()
    layout_data = layout_path.read_bytes()
    layout = json.loads(layout_data, object_pairs_hook=unique_object)
    require(isinstance(layout, dict) and set(layout) == {"destination_pivot", "frames"}, "invalid layout fields")
    destination = point(layout["destination_pivot"], "destination_pivot")
    require(all(22 <= v < 259 for v in destination), "destination pivot outside safe area")
    frames = layout["frames"]
    require(isinstance(frames, list) and len(frames) == 20, "expected exactly 20 frames")
    report = {"status": "packed", "source": str(source_path), "output": str(output_path),
              "source_sha256": hashlib.sha256(source_data).hexdigest(),
              "layout_sha256": hashlib.sha256(layout_data).hexdigest(),
              "destination_pivot": destination, "frames": [],
              "visual_review_required": True}
    with Image.open(BytesIO(source_data)) as source:
        require(source.format == "PNG" and source.mode == "RGBA" and
                getattr(source, "n_frames", 1) == 1, "source must be a single RGBA PNG")
        source.load()
        uncovered = source.getchannel("A")
        boxes, prepared, constraints = [], [], []
        for index, frame in enumerate(frames):
            require(isinstance(frame, dict) and set(frame) == {"rect", "pivot"}, "invalid frame fields")
            rect = frame["rect"]
            require(isinstance(rect, list) and len(rect) == 4 and all(type(v) is int for v in rect), "rect must contain four integers")
            x, y, width, height = rect
            require(x >= 0 and y >= 0 and width > 0 and height > 0 and
                    x + width <= source.width and y + height <= source.height, "rectangle outside source")
            box = (x, y, x + width, y + height)
            require(all(box[2] <= old[0] or box[0] >= old[2] or
                        box[3] <= old[1] or box[1] >= old[3] for old in boxes), "overlapping rectangles")
            boxes.append(box)
            pivot = point(frame["pivot"], "frame pivot")
            require(0 <= pivot[0] <= width and 0 <= pivot[1] <= height, "pivot outside rectangle")
            pose = source.crop(box)
            bounds = pose.getchannel("A").getbbox()
            require(bounds is not None, "empty frame: " + str(index))
            # Bounds include every alpha>0 pixel, including faint effects.
            for extent, room in [(pivot[0] - bounds[0], destination[0] - 22),
                                 (bounds[2] - pivot[0], 259 - destination[0]),
                                 (pivot[1] - bounds[1], destination[1] - 22),
                                 (bounds[3] - pivot[1], 259 - destination[1])]:
                if extent > 0:
                    constraints.append(room / extent)
            uncovered.paste(0, box)
            prepared.append((pose, pivot))
            report["frames"].append({"index": index, "rect": rect, "pivot": pivot,
                                      "source_alpha_bounds": list(bounds)})
        require(uncovered.getbbox() is None, "visible source pixels outside rectangles")
        scale = min(constraints)
        require(math.isfinite(scale) and scale > 0, "no positive common scale fits pivots")
        # Move one floating-point step inward to avoid rounding outside bounds.
        scale = math.nextafter(scale, 0.0)
        report["scale"] = scale
        atlas = Image.new("RGBA", (1124, 1405))
        for index, (pose, pivot) in enumerate(prepared):
            # One inverse affine mapping keeps scale identical even when source
            # rectangle sizes differ; no independently rounded pose resizing.
            cell = pose.transform((281, 281), Image.Transform.AFFINE,
                                  (1 / scale, 0, pivot[0] - destination[0] / scale,
                                   0, 1 / scale, pivot[1] - destination[1] / scale),
                                  resample=Image.Resampling.NEAREST)
            bounds = cell.getchannel("A").getbbox()
            require(bounds is not None, "resampling emptied frame: " + str(index))
            require(bounds[0] >= 22 and bounds[1] >= 22 and bounds[2] <= 259 and bounds[3] <= 259,
                    "resampled alpha outside safe area: " + str(index))
            report["frames"][index]["output_alpha_bounds"] = list(bounds)
            atlas.paste(cell, ((index % 4) * 281, (index // 4) * 281))
        output = BytesIO()
        atlas.save(output, format="PNG", compress_level=9)
        png = output.getvalue()
    # Exclusive creation also prevents overwriting a file created during packing.
    with output_path.open("xb") as handle:
        handle.write(png)
    report["output_sha256"] = hashlib.sha256(png).hexdigest()
    return report


def main(argv=None):
    try:
        parser = Parser(description=__doc__)
        parser.add_argument("--source", required=True, type=Path)
        parser.add_argument("--layout", required=True, type=Path)
        parser.add_argument("--output", required=True, type=Path)
        args = parser.parse_args(argv)
        report = pack(args.source, args.layout, args.output)
        code = 0
    except (OSError, ValueError, ImportError) as exc:
        report = {"status": "error", "errors": [str(exc)]}
        code = 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
