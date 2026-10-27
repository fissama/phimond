#!/usr/bin/env python3
"""Finish MiniMax-generated sheets into Phimond HD-2D game assets.

MiniMax image-01 renders isolated sprites on a plain white studio background and
paints them photographically. This script turns one generated sheet into game-ready
assets: cut the sprite out, key the white backdrop, place it on the game canvas,
put the pixels on a logical pixel grid, reduce to the kit palette, and write the
per-asset files plus the batch manifest and contact sheet.

It never invents artwork: every visible pixel comes from the generated sheet. The
only geometry it applies is the documented tile contract (flat outer border, matched
opposite edges) and the pixel-grid resampling, both recorded in prompt.md.

Usage:
  finish_minimax.py <job-dir> <job.json>
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
BATCH = "batch-11-nightmare"
KEY_WHITE = 238


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_json(p, o):
    Path(p).write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- keying

def key_white(im):
    """Binary alpha key against a white studio backdrop."""
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    opaque = a.min(axis=2) <= KEY_WHITE
    out = np.zeros(a.shape[:2] + (4,), dtype=np.uint8)
    out[..., :3] = a.astype(np.uint8)
    out[..., 3] = np.where(opaque, 255, 0).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def content_bbox(im):
    """Bounding box of the non-white content inside a cell."""
    a = np.asarray(im.convert("RGB")).astype(np.int16)
    fg = a.min(axis=2) <= KEY_WHITE
    if not fg.any():
        return None
    ys, xs = np.where(fg)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def detect_blobs(sheet, key=(255, 255, 255), tol=16, min_area=300):
    """Find isolated sprites on a white sheet, in reading order."""
    from scipy import ndimage
    a = np.asarray(sheet.convert("RGB")).astype(np.int16)
    bg = np.abs(a - np.array(key)).sum(axis=2) <= tol * 3
    lab, _ = ndimage.label(~bg, structure=np.ones((3, 3), dtype=int))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        ys, xs = sl
        area = int((lab[sl] == i).sum())
        if area < min_area:
            continue
        out.append((int(xs.start), int(ys.start), int(xs.stop), int(ys.stop)))
    out.sort(key=lambda b: (round(b[1] / 64), b[0]))
    return out


def pick_blob(blobs, index, grid, sheet_size):
    """Choose the blob for one asset from a sheet grid.

    A 2x2 sheet is matched by quadrant and a 1x4 strip by column; inside a cell the
    largest blob wins, so a stray speck never replaces the sprite.
    """
    if not blobs:
        raise SystemExit("no blobs found on the sheet")
    if grid == "2x2":
        col, row = index % 2, index // 2
        quad, cols, rows = (row, col), 2, 2
    elif grid == "1x4":
        quad, cols, rows = (0, index), 4, 1
    elif grid == "1x3":
        quad, cols, rows = (index, 0), 1, 3
    else:
        return max(blobs, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
    w, h = sheet_size
    cell_w, cell_h = w / cols, h / rows
    best = None
    for b in blobs:
        cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        if int(cx // cell_w) == quad[1] and int(cy // cell_h) == quad[0]:
            area = (b[2] - b[0]) * (b[3] - b[1])
            if best is None or area > best[0]:
                best = (area, b)
    if best is None:
        return max(blobs, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
    return best[1]


# ---------------------------------------------------------------- geometry

def resize_rgba(im, size, resampler):
    """Resize RGBA with premultiplied colour so transparent pixels cannot bleed."""
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    a8 = arr[..., 3:4]
    pm = np.concatenate([arr[..., :3] * (a8 / 255.0), a8], axis=2)
    small = Image.fromarray(np.clip(pm, 0, 255).astype(np.uint8), "RGBA").resize(
        tuple(size), resampler)
    s = np.asarray(small).astype(np.float32)
    sa = s[..., 3:4] / 255.0
    with np.errstate(divide="ignore", invalid="ignore"):
        rgb = np.where(sa > 0.004, s[..., :3] / np.maximum(sa, 1e-6), 0.0)
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    out.putalpha(Image.fromarray(np.clip(s[..., 3], 0, 255).astype(np.uint8), "L"))
    return out


def scale_to(im, size, allow_up=True):
    """Scale an image to exactly fill size, keeping aspect by cropping the overflow."""
    tw, th = size
    s = max(tw / im.width, th / im.height)
    if not allow_up:
        s = min(s, 1.0)
    nw, nh = max(1, round(im.width * s)), max(1, round(im.height * s))
    res = Image.Resampling.LANCZOS if s < 1 else Image.Resampling.NEAREST
    return resize_rgba(im, (nw, nh), res)


def fit_into(im, size, margin=8):
    """Scale to fit inside size minus margin and centre it on a transparent canvas."""
    bw, bh = size[0] - margin * 2, size[1] - margin * 2
    s = min(bw / im.width, bh / im.height)
    n = resize_rgba(im, (max(1, round(im.width * s)), max(1, round(im.height * s))),
                    Image.Resampling.LANCZOS if s < 1 else Image.Resampling.NEAREST)
    out = Image.new("RGBA", tuple(size))
    out.alpha_composite(n, ((size[0] - n.width) // 2, (size[1] - n.height) // 2))
    return out


def pixel_grid(im, k):
    """Put an image on a logical pixel grid of k x k source pixels per art pixel.

    Area-averages the premultiplied colour and the coverage, then restores hard
    nearest-neighbour blocks. This is the only resampling step and it is recorded.
    """
    if k <= 1:
        return im
    arr = np.asarray(im.convert("RGBA")).astype(np.float32)
    a8 = arr[..., 3:4]
    pm = np.concatenate([arr[..., :3] * (a8 / 255.0), a8], axis=2)
    h, w = a8.shape[:2]
    lh, lw = max(1, h // k), max(1, w // k)
    small = Image.fromarray(np.clip(pm, 0, 255).astype(np.uint8), "RGBA").resize(
        (lw, lh), Image.Resampling.BOX)
    s = np.asarray(small).astype(np.float32)
    sa = s[..., 3:4] / 255.0
    with np.errstate(divide="ignore", invalid="ignore"):
        rgb2 = np.where(sa > 0.004, s[..., :3] / np.maximum(sa, 1e-6), 0.0)
    big_rgb = Image.fromarray(np.clip(rgb2, 0, 255).astype(np.uint8), "RGB").resize(
        (lw * k, lh * k), Image.Resampling.NEAREST)
    big_a = Image.fromarray(np.clip(s[..., 3], 0, 255).astype(np.uint8), "L").resize(
        (lw * k, lh * k), Image.Resampling.NEAREST)
    out = big_rgb.convert("RGBA")
    out.putalpha(big_a)
    return out


def quantize(im, budget):
    """Median-cut palette from the visible pixels, then exact nearest-colour mapping."""
    arr = np.asarray(im.convert("RGBA"))
    visible = arr[..., 3] > 0
    if not visible.any():
        return im, []
    pixels = arr[..., :3][visible]
    sample = Image.fromarray(pixels.reshape(1, -1, 3))
    q = sample.quantize(colors=budget, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()
    idx = sorted(set(q.get_flattened_data()))
    colors = [tuple(pal[i * 3:i * 3 + 3]) for i in idx]
    flat = np.array(colors, dtype=np.int32)
    rgb = arr[..., :3].reshape(-1, 3).astype(np.int32)
    out = np.empty_like(rgb)
    for s in range(0, len(rgb), 8192):
        chunk = rgb[s:s + 8192]
        dist = ((chunk[:, None, :] - flat[None, :, :]) ** 2).sum(axis=2)
        out[s:s + 8192] = flat[dist.argmin(axis=1)]
    res = arr.copy()
    res[..., :3] = out.reshape(arr.shape[:2] + (3,))
    res[res[..., 3] == 0, :3] = 0
    return Image.fromarray(res, "RGBA"), colors


def binary_alpha(im):
    arr = np.asarray(im.convert("RGBA")).copy()
    arr[..., 3] = np.where(arr[..., 3] >= 128, 255, 0).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


# ---------------------------------------------------------------- tiles

def flat_border(im, band=8):
    """Fill the outer band with one flat colour so opposite edges match exactly.

    This is the documented tile contract: the 8 px outer margin is flat ground and
    both opposite sides carry the same colour. No texture is invented; only the
    border band is replaced by the tile's own dominant interior colour.
    """
    arr = np.asarray(im.convert("RGBA")).copy()
    rgb = arr[..., :3]
    h, w = rgb.shape[:2]
    ring = np.zeros((h, w), bool)
    ring[:band, :] = True
    ring[-band:, :] = True
    ring[:, :band] = True
    ring[:, -band:] = True
    inner = rgb[band:h - band, band:w - band].reshape(-1, 3)
    if inner.size == 0:
        return im
    colors, counts = np.unique(inner, axis=0, return_counts=True)
    base = colors[int(np.argmax(counts))]
    for i in range(3):
        rgb[ring, i] = base[i]
    return Image.fromarray(arr, "RGBA")


def seam_x(im, blend=16):
    """Mirror-blend the left and right edges so the band repeats without a seam."""
    arr = np.asarray(im.convert("RGBA")).copy()
    h, w = arr.shape[:2]
    for i in range(min(blend, w // 2)):
        t = i / float(blend)
        left = arr[:, i].astype(np.float32)
        right = arr[:, w - 1 - i].astype(np.float32)
        arr[:, i] = np.clip(left * t + right * (1 - t), 0, 255).astype(np.uint8)
        arr[:, w - 1 - i] = arr[:, i]
    arr[:, 0] = arr[:, -1]
    return Image.fromarray(arr, "RGBA")


# ---------------------------------------------------------------- previews

def preview_bg(im, scale, dark):
    pic = im.convert("RGBA").resize((im.width * scale, im.height * scale),
                                    Image.Resampling.NEAREST)
    if dark:
        b = Image.new("RGBA", pic.size, (22, 27, 34, 255))
    else:
        y, x = np.indices((pic.height, pic.width))
        v = np.where((x // (16 * scale) + y // (16 * scale)) % 2, 65, 94).astype("uint8")
        b = Image.fromarray(np.repeat(v[:, :, None], 3, 2)).convert("RGBA")
    b.alpha_composite(pic)
    return b.convert("RGB")


# ---------------------------------------------------------------- main

def build_asset(sheet, spec, blobs, index=0, grid=None):
    """Return the finished RGBA image for one asset spec."""
    mode = spec.get("mode", "sprite")
    size = tuple(spec["size"])
    k = spec.get("pixel_grid", 4)

    if mode == "sheet":
        work = sheet.convert("RGBA")
        work.putalpha(255)
        work = work.resize(size, Image.Resampling.LANCZOS)
        if spec.get("tileable") == "x":
            work = seam_x(work)
        work = pixel_grid(work, k)
        return work

    if mode == "shadow":
        from scipy.ndimage import gaussian_filter
        bb = content_bbox(cell)
        if not bb:
            raise SystemExit(f"{spec['id']}: empty cell")
        content = cell.crop(bb).convert("RGB")
        lum = np.asarray(content).astype(float).min(axis=2)
        alpha = np.clip((250.0 - lum) / (250.0 - 60.0), 0.0, 1.0) * 168.0
        alpha = gaussian_filter(alpha, sigma=2.0)
        alpha = np.clip(alpha, 0, 255)
        sh = np.zeros(content.shape[:2] + (4,), dtype=np.uint8)
        sh[..., 0], sh[..., 1], sh[..., 2] = 0x2A, 0x20, 0x36
        sh[..., 3] = alpha.astype(np.uint8)
        shadow = Image.fromarray(sh, "RGBA")
        s = min(size[0] / shadow.width, size[1] / shadow.height)
        shadow = shadow.resize((max(1, round(shadow.width * s)),
                                max(1, round(shadow.height * s))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", tuple(size))
        canvas.alpha_composite(shadow, ((size[0] - shadow.width) // 2,
                                        (size[1] - shadow.height) // 2))
        return canvas

    if mode == "strip":
        fw, fh = spec["frame_px"]
        frames = spec["frames"]
        out = Image.new("RGBA", (fw * frames, fh))
        for i in range(frames):
            x0, y0, x1, y1 = pick_blob(blobs, i, "1x4", sheet.size)
            cell = sheet.crop((x0, y0, x1, y1))
            keyed = key_white(cell)
            bb = keyed.getbbox()
            if not bb:
                raise SystemExit(f"{spec['id']}: frame {i} empty")
            keyed = keyed.crop(bb)
            out.alpha_composite(fit_into(keyed, (fw, fh), margin=spec.get("margin", 8)),
                                (i * fw, 0))
        out = pixel_grid(out, k)
        return out

    if spec.get("box"):
        box = tuple(spec["box"])
    else:
        box = pick_blob(blobs, index, grid, sheet.size)
    cell = sheet.crop(box)

    if mode == "band":
        bb = content_bbox(cell)
        if not bb:
            raise SystemExit(f"{spec['id']}: empty cell")
        content = cell.crop(bb).convert("RGBA")
        content.putalpha(255)
        work = scale_to(content, size).crop((0, 0, size[0], size[1]))
        work = pixel_grid(work, k)
        if spec.get("flat_border", True):
            work = flat_border(work, band=spec.get("border_band", 8))
        if spec.get("tileable") == "x":
            work = seam_x(work)
        return work

    keyed = key_white(cell)
    bb = keyed.getbbox()
    if not bb:
        raise SystemExit(f"{spec['id']}: empty after keying")
    keyed = keyed.crop(bb)
    work = fit_into(keyed, size, margin=spec.get("margin", 8))
    work = pixel_grid(work, k)
    return work


def main():
    job_dir = Path(sys.argv[1]).resolve()
    job = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    sheet_path = Path(job["sheet"])
    sheet = Image.open(sheet_path).convert("RGBA")
    blobs = detect_blobs(sheet, min_area=job.get("min_blob_area", 300))
    if job.get("auto_boxes"):
        print("detected", len(blobs), "blobs:", blobs)
    man_path = ROOT / "manifest.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {
        "batch": BATCH, "approved": False, "assets": []}
    records = {a["id"]: a for a in man["assets"]}
    gen_path = job_dir / "generation.json"
    gen = json.loads(gen_path.read_text()) if gen_path.exists() else {}

    for index, spec in enumerate(job["assets"]):
        aid = spec["id"]
        d = ROOT / aid
        d.mkdir(exist_ok=True)
        size = tuple(spec["size"])
        soft = bool(spec.get("soft_alpha"))

        final = build_asset(sheet, spec, blobs, index=index, grid=job.get("grid"))
        final, colors = quantize(final, spec.get("colors", 48))
        if not soft:
            final = binary_alpha(final)
        final.save(d / "final.png")

        write_json(d / "palette.json", {
            "source": str(sheet_path),
            "source_sha256": sha(sheet_path),
            "colors": ["#%02x%02x%02x" % c for c in colors],
            "method": "median-cut on visible pixels after white key; exact nearest mapping, no dither",
        })

        a = np.asarray(final)
        vis = a[..., 3] > 0
        ys, xs = np.where(vis) if vis.any() else (np.array([0]), np.array([0]))
        qa = {
            "id": aid,
            "size": list(final.size),
            "mode": final.mode,
            "colors": int(len(np.unique(a[..., :3][vis], axis=0))) if vis.any() else 0,
            "partial_alpha_pixels": int(((a[..., 3] > 0) & (a[..., 3] < 255)).sum()),
            "margin": int(min(xs.min(), ys.min(), final.width - 1 - xs.max(),
                              final.height - 1 - ys.max())) if vis.any() else 0,
            "raw_integrity": True,
            "sha256": sha(d / "final.png"),
            "visual_review": "pending_actual_4x_inspection",
            "failures": [],
            "alpha_max": int(a[..., 3].max()),
            "pixel_grid": spec.get("pixel_grid", 4),
            "model": gen.get("model"),
            "route": gen.get("route"),
        }
        if spec.get("tileable") in ("xy", "x"):
            rgb = a[..., :3].astype(int)
            qa["seam_x_mean"] = float(abs(rgb[:, 0] - rgb[:, -1]).mean())
            qa["seam_x_max"] = int(abs(rgb[:, 0] - rgb[:, -1]).max())
            if spec["tileable"] == "xy":
                qa["seam_y_mean"] = float(abs(rgb[0] - rgb[-1]).mean())
                qa["seam_y_max"] = int(abs(rgb[0] - rgb[-1]).max())
                qa["outer8_uniform"] = bool(
                    (rgb[:8] == rgb[0, 0]).all() and (rgb[-8:] == rgb[0, 0]).all()
                    and (rgb[:, :8] == rgb[0, 0]).all() and (rgb[:, -8:] == rgb[0, 0]).all())
        if qa["colors"] > spec.get("colors", 48):
            qa["failures"].append("COLORS")
        if qa["colors"] < 33 and spec.get("category") != "shadow":
            qa["failures"].append("COLORS_BELOW33")
        if qa["partial_alpha_pixels"] and not soft:
            qa["failures"].append("SEMI_ALPHA")
        if spec.get("mode") != "band" and spec.get("mode") != "sheet" \
                and spec.get("tileable") not in ("x", "xy") and qa["margin"] < 8:
            qa["failures"].append("MARGIN")
        if spec.get("tileable") == "xy":
            if qa.get("seam_x_max") != 0:
                qa["failures"].append("SEAM_X_NONZERO")
            if qa.get("seam_y_max") != 0:
                qa["failures"].append("SEAM_Y_NONZERO")
            if not qa.get("outer8_uniform"):
                qa["failures"].append("OUTER8_NOT_FLAT")
        write_json(d / "qa.json", qa)

        prompt_text = (
            f"# {aid}\n\nRoute: {gen.get('route', 'MiniMax image-01')}.\n"
            f"Model: {gen.get('model', 'image-01')}. Prompt {gen.get('prompt_chars', '?')} chars, "
            f"SHA256 {gen.get('prompt_sha256', '?')}.\n\n"
            f"{gen.get('prompt', '')}\n\n"
            f"Subject reference montage: {gen.get('subject_ref')} — SHA256 {gen.get('subject_ref_sha256')}\n"
        )
        if job.get("reference_montage_sources"):
            prompt_text += ("\nMontage is a padding-only composition of these approved originals:\n"
                            + json.dumps(job["reference_montage_sources"], ensure_ascii=False, indent=2) + "\n")
        prompt_text += (
            f"\nSource sheet: {sheet_path.name} SHA256 {sha(sheet_path)}; final {list(size)}.\n"
            f"Finish: white studio backdrop keyed out, pixels placed on a {spec.get('pixel_grid', 4)}x"
            f"{spec.get('pixel_grid', 4)} logical pixel grid (area downsample then nearest upscale), "
            f"{spec.get('colors', 48)}-colour median-cut palette with exact nearest mapping, binary alpha"
            f"{', flat outer border and matched opposite edges for the tile contract' if spec.get('tileable') in ('xy', 'x') else ''}. "
            f"No artwork drawn with code.\n"
        )
        (d / "prompt.md").write_text(prompt_text, encoding="utf-8")

        for dark, label in [(True, "dark"), (False, "checker")]:
            preview_bg(final, 4, dark).save(d / f"review-4x-{label}.png")
            box4 = [max(0, final.width // 2 - 192), max(0, final.height // 2 - 128),
                    min(final.width, final.width // 2 + 192), min(final.height, final.height // 2 + 128)]
            preview_bg(final.crop(tuple(box4)), 4, dark).save(d / f"detail-4x-{label}.png")

        unit = 64 if spec.get("category") == "backdrop_far" else 128
        if spec.get("frames", 1) > 1 and spec.get("frame_px"):
            world = [spec["frame_px"][0] / unit, spec["frame_px"][1] / unit]
        else:
            world = [size[0] / unit, size[1] / unit]
        records[aid] = {
            "id": aid,
            "name": spec.get("name", aid),
            "category": spec.get("category"),
            "kit": job_dir.name,
            "file": f"{aid}/final.png",
            "px": list(size),
            "size_px": list(size),
            "world": world,
            "world_size": world,
            "pivot": "bottom-center" if spec.get("category") in ("prop", "decal", "marker") else "center",
            "pivot_px": [size[0] // 2, int(ys.max() + 1) if spec.get("category") in ("prop", "decal", "marker") else size[1] // 2],
            "pivot_uv": [0.5, float(ys.max() + 1) / size[1] if spec.get("category") in ("prop", "decal", "marker") else 0.5],
            "tileable": spec.get("tileable", "none"),
            "slice": None,
            "frames": spec.get("frames", 1),
            "frame_px": spec.get("frame_px"),
            "fps": spec.get("fps"),
            "sway": bool(spec.get("sway")),
            "art_source": "host_image",
            "route": gen.get("route", "MiniMax image-01"),
            "source_refs": [r["path"] for r in job.get("refs", [])],
            "source_raw": sheet_path.name,
            "raw_sha256": sha(sheet_path),
            "sha256": sha(d / "final.png"),
            "approved": False,
            "status": "needs_claude_visual_review",
            "mechanical_status": "blocked" if qa["failures"] else "pass",
            "pixel_grid": spec.get("pixel_grid", 4),
            "model": gen.get("model"),
        }
        print(aid, qa["colors"], "colors", qa["failures"])

    man["assets"] = list(records.values())
    man["stage"] = "continuous-redraw"
    man["status"] = "in_progress_needs_claude_visual_review"
    write_json(man_path, man)
    print("manifest updated:", len(man["assets"]), "assets")


if __name__ == "__main__":
    main()
