"""Categorize previously-extracted Unity assets into UI subfolders.

Improvements over the first cut:
  1. Vietnamese diacritic transliteration → snake_case ASCII filenames
  2. Smarter classification rules reduce the "misc" bucket
  3. De-duplicates Sprite vs Texture2D by image SHA1 (only when bytes match)
  4. Light tileable detection (top==bottom, left==right) recorded in manifest
  5. Eng/Vietnamese comment headers on each category for downstream consumers

Input:
    apps/game-client/assets/extracted/sbw_v32/Texture2D/*.png (+Sprite)
    apps/game-client/assets/extracted/sbw_v84/Texture2D/*.png (+Sprite)

Output (per deliverable):
    apps/game-client/assets/extracted/extended/
    ├── ui/         ornamental panels, dialog backgrounds, frames
    ├── icons/      small (<=128px) square icons (items, skills, status, money)
    ├── buttons/    button 4-state textures
    ├── chat/       chat panel bg + tabs
    ├── hud/        portrait, avatar, rank badge, status bar
    ├── pets/       pet portraits + frames (pb_*)
    ├── rooms/      large background maps (>=500px)
    ├── fonts/      bitmap fonts
    ├── misc/       sprite-sheet slices, designer dumps
    └── manifest.json
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image

REPO = Path("/Users/phileanh/rust/phimond")
EXT_OUT = REPO / "apps/game-client/assets/extracted/extended"
RAW_DIRS = [
    REPO / "apps/game-client/assets/extracted/sbw_v32",
    REPO / "apps/game-client/assets/extracted/sbw_v84",
]

CATEGORIES = (
    "ui",
    "icons",
    "buttons",
    "chat",
    "hud",
    "pets",
    "rooms",
    "fonts",
    "misc",
)

RE_PIXIL = re.compile(r"pixil-frame-\d+", re.IGNORECASE)
RE_ITEM = re.compile(r"item\d+", re.IGNORECASE)
RE_PB = re.compile(r"pb_[a-z0-9]+", re.IGNORECASE)
RE_RANK = re.compile(r"^rank\d+", re.IGNORECASE)
RE_BG = re.compile(r"^Background[_\s(]", re.IGNORECASE)
RE_FONT = re.compile(r"^(font|bitmap)", re.IGNORECASE)
RE_CHAT = re.compile(r"(chat|tuchat|textchat)", re.IGNORECASE)
RE_BTN = re.compile(r"(^button|_button|button_|btn\d|^btn_|^btn$)", re.IGNORECASE)
RE_FRAME = re.compile(r"(frame|panel|bg\d|fogbg|tableitem|slotlight|grid\d|selgrid)", re.IGNORECASE)
RE_MMEXPORT = re.compile(r"mmexport\d+", re.IGNORECASE)
RE_VI_DIACRITIC = re.compile(r"Dự_án_mới")
RE_VIETNAMESE_CHAR = re.compile(
    r"[ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]"
)

VI_DIACRITIC_TABLE = {
    "á": "a", "à": "a", "ả": "a", "ã": "a", "ạ": "a",
    "ă": "a", "ắ": "a", "ằ": "a", "ẳ": "a", "ẵ": "a", "ặ": "a",
    "â": "a", "ấ": "a", "ầ": "a", "ẩ": "a", "ẫ": "a", "ậ": "a",
    "đ": "d",
    "é": "e", "è": "e", "ẻ": "e", "ẽ": "e", "ẹ": "e",
    "ê": "e", "ế": "e", "ề": "e", "ể": "e", "ễ": "e", "ệ": "e",
    "í": "i", "ì": "i", "ỉ": "i", "ĩ": "i", "ị": "i",
    "ó": "o", "ò": "o", "ỏ": "o", "õ": "o", "ọ": "o",
    "ô": "o", "ố": "o", "ồ": "o", "ổ": "o", "ỗ": "o", "ộ": "o",
    "ơ": "o", "ớ": "o", "ờ": "o", "ở": "o", "ỡ": "o", "ợ": "o",
    "ú": "u", "ù": "u", "ủ": "u", "ũ": "u", "ụ": "u",
    "ư": "u", "ứ": "u", "ừ": "u", "ử": "u", "ữ": "u", "ự": "u",
    "ý": "y", "ỳ": "y", "ỷ": "y", "ỹ": "y", "ỵ": "y",
    "Á": "A", "À": "A", "Ả": "A", "Ã": "A", "Ạ": "A",
    "Ă": "A", "Ắ": "A", "Ằ": "A", "Ẳ": "A", "Ẵ": "A", "Ặ": "A",
    "Â": "A", "Ấ": "A", "Ầ": "A", "Ẩ": "A", "Ẫ": "A", "Ậ": "A",
    "Đ": "D",
    "É": "E", "È": "E", "Ẻ": "E", "Ẽ": "E", "Ẹ": "E",
    "Ê": "E", "Ế": "E", "Ề": "E", "Ể": "E", "Ễ": "E", "Ệ": "E",
    "Í": "I", "Ì": "I", "Ỉ": "I", "Ĩ": "I", "Ị": "I",
    "Ó": "O", "Ò": "O", "Ỏ": "O", "Õ": "O", "Ọ": "O",
    "Ô": "O", "Ố": "O", "Ồ": "O", "Ổ": "O", "Ỗ": "O", "Ộ": "O",
    "Ơ": "O", "Ớ": "O", "Ờ": "O", "Ở": "O", "Ỡ": "O", "Ợ": "O",
    "Ú": "U", "Ù": "U", "Ủ": "U", "Ũ": "U", "Ụ": "U",
    "Ư": "U", "Ứ": "U", "Ừ": "U", "Ử": "U", "Ữ": "U", "Ự": "U",
    "Ý": "Y", "Ỳ": "Y", "Ỷ": "Y", "Ỹ": "Y", "Ỵ": "Y",
}


def transliterate(s: str) -> str:
    return "".join(VI_DIACRITIC_TABLE.get(c, c) for c in s)


def safe_filename(s: str, max_len: int = 80) -> str:
    s = transliterate(s).strip()
    s = s.replace(" ", "_").replace("-", "_").replace(".", "_")
    s = re.sub(r"[^A-Za-z0-9_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    if len(s) > max_len:
        s = s[:max_len].rstrip("_")
    return s or "unnamed"


def is_tileable(im: Image.Image, sample: int = 6) -> bool:
    if im.mode not in ("RGBA", "RGB"):
        return False
    if im.width < 4 or im.height < 4:
        return False
    rgba = im.convert("RGBA")
    w, h = im.width, im.height
    top = [rgba.getpixel((x, 0)) for x in range(0, w, max(1, w // sample))]
    bottom = [rgba.getpixel((x, h - 1)) for x in range(0, w, max(1, w // sample))]
    left = [rgba.getpixel((0, y)) for y in range(0, h, max(1, h // sample))]
    right = [rgba.getpixel((w - 1, y)) for y in range(0, h, max(1, h // sample))]
    same = sum(1 for a, b in zip(top, bottom) if a == b) + sum(
        1 for a, b in zip(left, right) if a == b
    )
    total = len(top) + len(left)
    return total > 0 and same / total > 0.85


def classify(name: str, bundle: str, w: int, h: int, mode: str) -> tuple[str, str, str]:
    """Return (category, sub_kind, reason)."""
    if not name or name == "unnamed":
        return ("misc", "unnamed", "missing or default name")

    n = name.lower()

    if RE_FONT.match(n):
        return ("fonts", "font", "name starts with font/bitmap")

    if RE_CHAT.search(n):
        return ("chat", "chat", "name has chat keyword")

    if RE_BTN.search(n):
        return ("buttons", "button", "name matches button/btn pattern")

    if RE_PIXIL.search(n):
        return ("misc", "npc_spriteframe", "pixil-frame-* (sprite-sheet slice)")

    if RE_MMEXPORT.search(n):
        if 80 <= w <= 250 and w == h:
            return ("hud", "phone_dump_portrait", "mmexport* 120×120 portrait")
        return ("misc", "designer_dump", "mmexport* phone screenshot dump")

    if RE_VI_DIACRITIC.search(name):
        # Translated by safe_filename later; classify as misc designer dump
        return ("misc", "designer_upload", "Dự_án_mới designer upload")

    if RE_ITEM.search(n):
        if w <= 64 and h <= 64:
            return ("icons", "item_icon", "item### ≤64px")
        if w <= 128 and h <= 128:
            return ("icons", "item_icon_large", "item### ≤128px")
        return ("icons", "item_icon_unusual", f"item### unusual {w}×{h}")

    if RE_PB.search(n):
        # pet portraits: roughly square 30-220 px
        if 30 <= w <= 220 and 30 <= h <= 220 and abs(w - h) <= 12:
            return ("pets", "pet_portrait", f"pb_### {w}×{h} pet portrait")
        return ("pets", "pet_asset", f"pb_### {w}×{h}")

    if RE_RANK.match(n):
        return ("hud", "rank_badge", "rank##")

    if RE_BG.match(n):
        if w >= 500 or h >= 500:
            return ("rooms", "background_map", "Background_* ≥500px")
        return ("ui", "background_panel", "Background_* small")

    if RE_FRAME.search(n):
        return ("ui", "frame", "frame/panel/slot/grid keyword")

    if w >= 512 or h >= 512:
        return ("rooms", "large_background", f"≥512px ({w}×{h})")

    if w == h and w <= 64 and mode == "RGBA":
        return ("icons", f"{w}×{h}_square", f"{w}×{h} RGBA square")

    if w == h and w <= 96 and mode == "RGBA":
        return ("icons", f"{w}×{h}_square", f"{w}×{h} RGBA square ≤96")

    if mode == "RGB" and w * h >= 20000:
        return ("rooms", "tile", "RGB large asset (tile)")

    return ("misc", "unclassified", "no rule matched")


def main() -> None:
    EXT_OUT.mkdir(parents=True, exist_ok=True)
    for cat in CATEGORIES:
        (EXT_OUT / cat).mkdir(exist_ok=True)

    manifest: list[dict] = []
    counters: Counter = Counter()
    size_buckets: dict[str, list[int]] = defaultdict(list)
    dim_buckets: dict[str, list[tuple[int, int]]] = defaultdict(list)
    mode_buckets: dict[str, Counter] = defaultdict(Counter)
    sha_dedup: dict[str, str] = {}  # sha1 -> relative path of first occurrence

    # Reset destination folders first (idempotent rerun)
    for cat in CATEGORIES:
        for old in (EXT_OUT / cat).glob("*.png"):
            old.unlink()

    for raw_dir in RAW_DIRS:
        src_version = raw_dir.name
        for kind in ("Texture2D", "Sprite"):
            src_root = raw_dir / kind
            if not src_root.exists():
                continue
            for png_path in sorted(src_root.glob("*.png")):
                rel = png_path.relative_to(raw_dir)
                stem = png_path.stem
                parts = stem.split("_", 2)
                if len(parts) < 3:
                    continue
                bundle = parts[0]
                path_id = parts[1]
                tex_name = parts[2]

                # Read image bytes for dedupe
                raw_bytes = png_path.read_bytes()
                sha = hashlib.sha1(raw_bytes).hexdigest()[:12]
                if sha in sha_dedup:
                    manifest.append({
                        "source": src_version,
                        "kind": kind,
                        "original_path": str(rel),
                        "category": "dedupe",
                        "sub_kind": "duplicate_of",
                        "duplicate_of": sha_dedup[sha],
                        "sha1_short": sha,
                    })
                    continue
                sha_dedup[sha] = str(rel)

                try:
                    im = Image.open(png_path)
                    im.verify()
                    im = Image.open(png_path)
                except Exception as exc:
                    manifest.append({
                        "source": src_version,
                        "kind": kind,
                        "original_path": str(rel),
                        "category": "errors",
                        "sub_kind": "verify_fail",
                        "reason": str(exc),
                    })
                    continue

                w, h = im.width, im.height
                mode = im.mode
                tileable = is_tileable(im)
                cat, sub, reason = classify(tex_name, bundle, w, h, mode)
                counters[cat] += 1
                size_buckets[cat].append(png_path.stat().st_size)
                dim_buckets[cat].append((w, h))
                mode_buckets[cat][mode] += 1

                safe_name = safe_filename(f"{src_version}_{kind}_{tex_name}_{w}x{h}")
                dest = EXT_OUT / cat / f"{safe_name}.png"
                # Avoid overwriting (shouldn't happen after dedupe)
                counter = 1
                while dest.exists():
                    dest = EXT_OUT / cat / f"{safe_name}_{counter}.png"
                    counter += 1
                try:
                    shutil.copyfile(png_path, dest)
                except OSError as exc:
                    manifest.append({
                        "source": src_version,
                        "kind": kind,
                        "original_path": str(rel),
                        "category": "errors",
                        "sub_kind": "copy_fail",
                        "reason": str(exc),
                    })
                    continue

                manifest.append({
                    "source": src_version,
                    "kind": kind,
                    "original_path": str(rel),
                    "extracted_path": str(dest.relative_to(EXT_OUT)),
                    "category": cat,
                    "sub_kind": sub,
                    "reason": reason,
                    "bundle": bundle,
                    "path_id": int(path_id) if path_id.isdigit() else path_id,
                    "unity_name": tex_name,
                    "width": w,
                    "height": h,
                    "mode": mode,
                    "tileable_guess": tileable,
                    "size_bytes": dest.stat().st_size,
                    "sha1_short": sha,
                })

    stats = {}
    for cat in CATEGORIES:
        sizes = size_buckets.get(cat, [])
        dims = dim_buckets.get(cat, [])
        modes = dict(mode_buckets.get(cat, Counter()))
        if sizes:
            sizes_sorted = sorted(sizes)
            median = sizes_sorted[len(sizes_sorted) // 2]
            mean = sum(sizes_sorted) // max(1, len(sizes_sorted))
            total = sum(sizes_sorted)
        else:
            median = mean = total = 0
        stats[cat] = {
            "count": counters.get(cat, 0),
            "size_mean_bytes": mean,
            "size_median_bytes": median,
            "size_total_bytes": total,
            "mode_distribution": modes,
            "common_dimensions": Counter(dims).most_common(8),
        }

    summary = {
        "sources": [d.name for d in RAW_DIRS],
        "extracted_to": str(EXT_OUT),
        "categories": list(CATEGORIES),
        "totals": dict(counters),
        "errors": sum(1 for r in manifest if r.get("category") == "errors"),
        "deduped": sum(1 for r in manifest if r.get("category") == "dedupe"),
        "stats_per_category": stats,
        "files": manifest,
    }
    (EXT_OUT / "manifest.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )
    print(json.dumps({
        "sources": summary["sources"],
        "totals": dict(counters),
        "errors": summary["errors"],
        "deduped": summary["deduped"],
        "manifest_size_mb": round((EXT_OUT / 'manifest.json').stat().st_size / 1e6, 2),
    }, indent=2))


if __name__ == "__main__":
    main()
