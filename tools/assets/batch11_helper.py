#!/usr/bin/env python3
"""
Master generator for 75 Phimond Maps across 17 HD-2D Octopath Kits (Batch 11).
Follows .ai/design/hd2d-maps-75-gemini-prompt.md strictly.
"""

import os
import json
import hashlib
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Path config
WORKSPACE = Path("/Users/phileanh/rust/phimond")
HD2D_DIR = WORKSPACE / "apps/game-web/art-src/hd2d"
MAP_SOURCES = Path("/Users/phileanh/Downloads/Phimond-P12-Review/map-images")

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def quantize_octopath(im, max_colors=42):
    """Quantize image to max_colors, enforcing binary alpha."""
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    mask = alpha > 128
    
    vis_pixels = rgb[mask]
    if len(vis_pixels) == 0:
        return im
        
    vis_im = Image.fromarray(rgb)
    q = vis_im.quantize(colors=max_colors, method=Image.Quantize.MEDIANCUT)
    q_rgb = np.array(q.convert('RGB'))
    
    res = np.zeros_like(arr)
    res[:, :, :3] = q_rgb
    res[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
    return Image.fromarray(res)

def make_seamless_xy(arr_rgb):
    """Enforce seamless tiling on XY boundaries by mirroring and blending edges."""
    h, w, c = arr_rgb.shape
    blend = 24
    res = arr_rgb.copy()
    for i in range(blend):
        t = i / float(blend)
        # horizontal blend
        res[:, i, :] = (res[:, i, :] * t + res[:, w - 1 - i, :] * (1.0 - t)).astype(np.uint8)
        res[:, w - 1 - i, :] = res[:, i, :]
        # vertical blend
        res[i, :, :] = (res[i, :, :] * t + res[h - 1 - i, :, :] * (1.0 - t)).astype(np.uint8)
        res[h - 1 - i, :, :] = res[i, :, :]
    # Hard copy exact 1px edge
    res[:, 0, :] = res[:, -1, :]
    res[0, :, :] = res[-1, :, :]
    return res

def make_seamless_x(arr_rgb):
    """Enforce seamless horizontal tiling on X boundary."""
    h, w, c = arr_rgb.shape
    blend = 24
    res = arr_rgb.copy()
    for i in range(blend):
        t = i / float(blend)
        res[:, i, :] = (res[:, i, :] * t + res[:, w - 1 - i, :] * (1.0 - t)).astype(np.uint8)
        res[:, w - 1 - i, :] = res[:, i, :]
    res[:, 0, :] = res[:, -1, :]
    return res

def compute_qa(im, is_tile=False, is_backdrop=False):
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    
    # Binary alpha check
    partial_alpha = int(np.sum((alpha > 0) & (alpha < 255)))
    
    # Color count
    vis_pixels = arr[alpha > 0]
    colors = len(set(tuple(p) for p in vis_pixels)) if len(vis_pixels) > 0 else 0
    
    # Magenta despill check
    r = rgb[:, :, 0].astype(int)
    g = rgb[:, :, 1].astype(int)
    b = rgb[:, :, 2].astype(int)
    pink_mask = (alpha > 0) & (r > 190) & (b > 190) & (g < 60)
    pink_count = int(np.sum(pink_mask))
    
    # Margins
    ys, xs = np.where(alpha > 0)
    if len(ys) == 0:
        margins = [im.size[1], im.size[1], im.size[0], im.size[0]]
    else:
        margins = [int(ys.min()), int(im.size[1] - 1 - ys.max()), int(xs.min()), int(im.size[0] - 1 - xs.max())]
        
    # Seam check
    seam_x_diff = 0
    seam_y_diff = 0
    if is_tile:
        seam_x_diff = int(np.max(np.abs(rgb[:, 0, :].astype(int) - rgb[:, -1, :].astype(int))))
        seam_y_diff = int(np.max(np.abs(rgb[0, :, :].astype(int) - rgb[-1, :, :].astype(int))))
    elif is_backdrop:
        seam_x_diff = int(np.max(np.abs(rgb[:, 0, :].astype(int) - rgb[:, -1, :].astype(int))))
        
    failures = []
    if partial_alpha > 0: failures.append(f"partial_alpha: {partial_alpha}")
    if colors > 48: failures.append(f"colors: {colors} > 48")
    if pink_count > 0: failures.append(f"pink_count: {pink_count}")
    if not is_tile and not is_backdrop:
        if any(m < 8 for m in margins):
            failures.append(f"margins < 8: {margins}")
    if is_tile and (seam_x_diff > 0 or seam_y_diff > 0):
        failures.append(f"seam diffs: x={seam_x_diff}, y={seam_y_diff}")
    if is_backdrop and seam_x_diff > 0:
        failures.append(f"seam_x diff: {seam_x_diff}")
        
    return {
        "dimensions": list(im.size),
        "colors": colors,
        "partial_alpha": partial_alpha,
        "pink_pixels": pink_count,
        "alpha_margins": margins,
        "seam_x_diff": seam_x_diff,
        "seam_y_diff": seam_y_diff,
        "failures": failures
    }

print("Loaded base helper modules.")
