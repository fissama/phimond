"""Remove magenta-key color contamination from opaque sprite-edge pixels."""
from __future__ import annotations

import colorsys
import numpy as np


def is_purple_hue(rgb: tuple[int, int, int]) -> bool:
    """Whether an RGB color falls in the requested purple hue/saturation range."""
    red, green, blue = (int(channel) / 255.0 for channel in rgb)
    hue, saturation, _ = colorsys.rgb_to_hsv(red, green, blue)
    degrees = hue * 360.0
    return 270.0 <= degrees <= 345.0 and saturation > 0.2


def _edge_mask(alpha: np.ndarray) -> np.ndarray:
    opaque = alpha > 0
    padded = np.pad(opaque, 1, constant_values=False)
    interior4 = (
        padded[:-2, 1:-1]
        & padded[2:, 1:-1]
        & padded[1:-1, :-2]
        & padded[1:-1, 2:]
    )
    return opaque & ~interior4


def _opaque_colors(rgba: np.ndarray) -> set[tuple[int, int, int]]:
    visible = rgba[:, :, 3] > 0
    return {tuple(map(int, row)) for row in rgba[:, :, :3][visible]}


def _purple_edge_count(rgba: np.ndarray, edge: np.ndarray) -> int:
    total = 0
    for y, x in zip(*np.where(edge)):
        if is_purple_hue(tuple(map(int, rgba[y, x, :3]))):
            total += 1
    return total


def purple_edge_count_rgba(image: np.ndarray) -> int:
    """Count purple-hued opaque pixels that touch transparent alpha in 4 directions."""
    rgba = np.asarray(image, dtype=np.uint8)
    if rgba.ndim != 3 or rgba.shape[2] != 4:
        raise ValueError("purple_edge_count_rgba expects an H×W×4 RGBA array")
    edge = _edge_mask(rgba[:, :, 3])
    return _purple_edge_count(rgba, edge)


def _darkness(rgb: np.ndarray) -> int:
    red, green, blue = map(int, rgb)
    return 299 * red + 587 * green + 114 * blue


def defringe_rgba(image: np.ndarray) -> tuple[np.ndarray, dict[str, int]]:
    """Replace suspicious purple edge pixels with the darkest nearby stable rim color.

    Pixels are considered from the original image snapshot, so replacements do not
    cascade. Alpha and transparent RGB are never changed.
    """
    source = np.asarray(image, dtype=np.uint8)
    if source.ndim != 3 or source.shape[2] != 4:
        raise ValueError("defringe_rgba expects an H×W×4 RGBA array")
    result = source.copy()
    alpha = source[:, :, 3]
    edge = _edge_mask(alpha)
    opaque = alpha > 0
    purple = np.zeros(alpha.shape, dtype=bool)
    for y, x in zip(*np.where(opaque)):
        purple[y, x] = is_purple_hue(tuple(map(int, source[y, x, :3])))

    before = int(np.count_nonzero(edge & purple))
    height, width = alpha.shape
    changes: list[tuple[int, int, tuple[int, int, int]]] = []
    for y, x in zip(*np.where(edge & purple)):
        stable_neighbors: list[tuple[int, int, int]] = []
        all_stable_purple = True
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                ny, nx = y + dy, x + dx
                if not (0 <= ny < height and 0 <= nx < width):
                    continue
                if not opaque[ny, nx] or edge[ny, nx]:
                    continue
                color = tuple(map(int, source[ny, nx, :3]))
                stable_neighbors.append(color)
                if not purple[ny, nx]:
                    all_stable_purple = False

        if not stable_neighbors or all_stable_purple:
            continue
        darkest = min(stable_neighbors, key=lambda color: (_darkness(color), color))
        changes.append((y, x, darkest))

    for y, x, color in changes:
        result[y, x, :3] = color

    after_edge = _edge_mask(result[:, :, 3])
    after_purple = np.zeros(alpha.shape, dtype=bool)
    for y, x in zip(*np.where(opaque)):
        after_purple[y, x] = is_purple_hue(tuple(map(int, result[y, x, :3])))
    stats = {
        "purple_edge_before": before,
        "purple_edge_after": int(np.count_nonzero(after_edge & after_purple)),
        "replaced_pixels": len(changes),
        "opaque_color_count_before": len(_opaque_colors(source)),
        "opaque_color_count_after": len(_opaque_colors(result)),
    }
    return result, stats
