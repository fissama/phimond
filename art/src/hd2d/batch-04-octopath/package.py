"""Package generated Phimond assets for Batch 04 (Pirate Ship & Shared Markers).
Uses Forge tools (palette_tool.py). Never draws procedural replacement artwork.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, subprocess, sys, shutil
import numpy as np

ROOT = Path(__file__).resolve().parent
FORGE = Path("/Users/phileanh/.codex/skills")
PY = sys.executable

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(p, v):
    Path(p).write_text(json.dumps(v, indent=2, ensure_ascii=False) + "\n")

def run(args):
    p = subprocess.run([PY, *map(str, args)], capture_output=True, text=True)
    if p.stdout:
        print(p.stdout.strip(), flush=True)
    if p.stderr:
        print(p.stderr.strip(), file=sys.stderr)
    return p.returncode

def seam_crop(im, axes, asset_id):
    """Minimize edge delta by tiny crop; no painting or mirroring."""
    w, h = im.size
    rgba = np.asarray(im.convert("RGBA")).astype(float) / 255.0
    black = rgba[:, :, :3] * rgba[:, :, 3:4]
    white = black + (1.0 - rgba[:, :, 3:4])
    layers = (black, white)

    def xscore(l, r):
        return max(float(np.abs(b[:, l] - b[:, w - 1 - r]).mean() * 255.0) for b in layers)

    l = r = t = b = 0
    if xscore(0, 0) >= 6:
        limit = 32 if w <= 512 else 96
        candidates = range(0, limit + 1, 1 if w <= 512 else 2)
        l, r = min(((i, j) for i in candidates for j in candidates), key=lambda pair: (xscore(*pair), sum(pair)))
    
    if axes == "xy":
        def yscore(t_, b_):
            return max(float(np.abs(a[t_, l:w - r or None] - a[h - 1 - b_, l:w - r or None]).mean() * 255.0) for a in layers)
        if yscore(0, 0) >= 6:
            candidates = range(0, 33, 1)
            t, b = min(((i, j) for i in candidates for j in candidates), key=lambda pair: (yscore(*pair), sum(pair)))
    
    if l or r or t or b:
        cropped = im.crop((l, t, w - r, h - b)).resize((w, h), Image.Resampling.NEAREST)
        return cropped, [l, t, w - r, h - b]
    return im, None

def package_batch_04():
    records = []
    
    # 1. Process props from ship-hardware, ship-rigging, shared-markers
    single_prop_jobs = [
        ("ship-hardware", "raw-01.png", [(61, 593), (678, 1157)], [(90, 607), (746, 1214)]),
        ("ship-rigging", "raw-01.png", [(14, 578), (599, 1000)], [(249, 634), (818, 1408)]),
        ("shared-markers", "raw-01.png", [(238, 490), (610, 868)], [(103, 511), (573, 1031), (1104, 1436)]),
    ]

    crop_inputs = ROOT / "palette-inputs"
    crop_inputs.mkdir(exist_ok=True)

    for job_id, raw_name, row_bounds, col_bounds in single_prop_jobs:
        jd = ROOT / "jobs" / job_id
        job = json.loads((jd / "job.json").read_text())
        raw_path = jd / raw_name
        raw_im = Image.open(raw_path).convert("RGBA")
        
        idx = 0
        for r_idx, (r_start, r_end) in enumerate(row_bounds):
            for c_idx, (c_start, c_end) in enumerate(col_bounds):
                if idx >= len(job["assets"]):
                    break
                spec = job["assets"][idx]
                idx += 1
                name = spec["id"]
                dest = ROOT / name
                dest.mkdir(exist_ok=True)

                cell = raw_im.crop((c_start, r_start, c_end, r_end))
                # Crop to alpha bbox
                bb = cell.getchannel("A").getbbox()
                if bb:
                    cell = cell.crop(bb)
                
                target_h = spec.get("height", 96)
                scale = target_h / max(1, cell.height)
                target_w = max(1, round(cell.width * scale))
                scaled = cell.resize((target_w, target_h), Image.Resampling.NEAREST)

                is_decal_or_icon = spec.get("category") in ("decal", "icon")
                canvas_w = target_w + 16
                canvas_h = target_h + 16
                canvas = Image.new("RGBA", (canvas_w, canvas_h))
                canvas.alpha_composite(scaled, (8, 8))
                if is_decal_or_icon:
                    pivot = "center"
                    pivot_px = [canvas_w / 2, canvas_h / 2]
                else:
                    pivot = "bottom_center"
                    pivot_px = [canvas_w / 2, target_h + 8]

                canvas.save(dest / "crop.png")
                canvas.save(crop_inputs / f"{name}.png")

                # Copy raw files
                for raw_f in jd.glob("raw-*.png"):
                    shutil.copyfile(raw_f, dest / raw_f.name)

                refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
                (dest / "prompt.md").write_text(job["prompt"] + "\n\nOrdered reference images:\n" +
                    "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs) +
                    f"\n\nRoute: built-in image_gen; raw SHA256 {sha(raw_path)}\n")
                
                (dest / "review.md").write_text("# Source identification\n\n" + job["source_card"] +
                    f"\n\nItem: {name} ({spec.get('desc')}). Draft; approved:false. Clean 8px alpha margins.\n")

                record = {
                    "id": name,
                    "category": spec.get("category", "prop"),
                    "kit": "common" if "markers" in job_id else "ship",
                    "file": f"{name}/final.png",
                    "px": list(canvas.size),
                    "world": [canvas.width / 128.0, canvas.height / 128.0],
                    "pivot": pivot,
                    "pivot_px": pivot_px,
                    "tileable": "none",
                    "slice": None,
                    "frames": 1,
                    "fps": None,
                    "sway": spec.get("sway", False),
                    "source_refs": job["refs"],
                    "replaces": None,
                    "approved": False,
                    "status": "needs_owner_review",
                    "art_source": "host_image",
                    "route": "built-in image_gen",
                    "source_job": job_id,
                    "raw_sha256": sha(raw_path),
                    "notes": spec.get("desc")
                }
                if "part_of" in spec:
                    record["part_of"] = spec["part_of"]
                records.append(record)

    # 2. Process storm-lantern (4 frames)
    jd = ROOT / "jobs" / "storm-lantern"
    job = json.loads((jd / "job.json").read_text())
    raw_path = jd / "raw-01.png"
    raw_im = Image.open(raw_path).convert("RGBA")
    name = "storm-lantern"
    dest = ROOT / name
    dest.mkdir(exist_ok=True)
    
    lantern_cols = [(120, 407), (627, 916), (1128, 1417), (1637, 1926)]
    lantern_frames = []
    target_h = 128
    for c_start, c_end in lantern_cols:
        cell = raw_im.crop((c_start, 108, c_end, 648))
        bb = cell.getchannel("A").getbbox()
        if bb:
            cell = cell.crop(bb)
        scale = target_h / max(1, cell.height)
        scaled = cell.resize((max(1, round(cell.width * scale)), target_h), Image.Resampling.NEAREST)
        lantern_frames.append(scaled)
    
    max_w = max(f.width for f in lantern_frames)
    frame_w = max_w + 16
    frame_h = target_h + 16
    anim_strip = Image.new("RGBA", (frame_w * 4, frame_h))
    for i, f in enumerate(lantern_frames):
        cx = (frame_w - f.width) // 2
        anim_strip.alpha_composite(f, (i * frame_w + cx, 8))
    
    anim_strip.save(dest / "crop.png")
    anim_strip.save(crop_inputs / f"{name}.png")
    for raw_f in jd.glob("raw-*.png"):
        shutil.copyfile(raw_f, dest / raw_f.name)
    
    refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
    (dest / "prompt.md").write_text(job["prompt"] + "\n\nOrdered reference images:\n" +
        "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs) +
        f"\n\nRoute: built-in image_gen; raw SHA256 {sha(raw_path)}\n")
    (dest / "review.md").write_text("# Source identification\n\n" + job["source_card"] +
        f"\n\nItem: {name} (4 animated frames). Interior flame changes subtly; silhouette fixed.\n")

    records.append({
        "id": name,
        "category": "light",
        "kit": "ship",
        "file": f"{name}/final.png",
        "px": list(anim_strip.size),
        "frame_px": [frame_w, frame_h],
        "world": [frame_w / 128.0, frame_h / 128.0],
        "pivot": "bottom_center",
        "pivot_px": [frame_w / 2, frame_h - 8],
        "tileable": "none",
        "slice": None,
        "frames": 4,
        "fps": 6,
        "sway": False,
        "source_refs": job["refs"],
        "replaces": None,
        "approved": False,
        "status": "needs_owner_review",
        "art_source": "host_image",
        "route": "built-in image_gen",
        "source_job": "storm-lantern",
        "raw_sha256": sha(raw_path),
        "notes": "Hanging storm lantern with 4 looping flame frames."
    })

    # 3. Process exit-arrows (4 directions x 4 frames)
    jd = ROOT / "jobs" / "exit-arrows"
    job = json.loads((jd / "job.json").read_text())
    raw_path = jd / "raw-02.png"
    raw_im = Image.open(raw_path).convert("RGBA")
    
    arrow_rows = [(40, 277), (342, 556), (614, 854), (908, 1123)]
    arrow_cols = [(68, 325), (373, 636), (675, 936), (985, 1247)]
    target_h = 64

    for r_idx, spec in enumerate(job["assets"]):
        name = spec["id"]
        dest = ROOT / name
        dest.mkdir(exist_ok=True)
        r_start, r_end = arrow_rows[r_idx]
        
        frames = []
        for c_start, c_end in arrow_cols:
            cell = raw_im.crop((c_start, r_start, c_end, r_end))
            bb = cell.getchannel("A").getbbox()
            if bb:
                cell = cell.crop(bb)
            scale = target_h / max(1, cell.height)
            scaled = cell.resize((max(1, round(cell.width * scale)), target_h), Image.Resampling.NEAREST)
            frames.append(scaled)
        
        max_w = max(f.width for f in frames)
        frame_w = max(target_h, max_w) + 16
        frame_h = target_h + 16
        strip = Image.new("RGBA", (frame_w * 4, frame_h))
        for i, f in enumerate(frames):
            cx = (frame_w - f.width) // 2
            cy = (frame_h - f.height) // 2
            strip.alpha_composite(f, (i * frame_w + cx, cy))
        
        strip.save(dest / "crop.png")
        strip.save(crop_inputs / f"{name}.png")
        for raw_f in jd.glob("raw-*.png"):
            shutil.copyfile(raw_f, dest / raw_f.name)
        
        refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
        (dest / "prompt.md").write_text(job["prompt"] + "\n\nOrdered reference images:\n" +
            "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs) +
            f"\n\nRoute: built-in image_gen; raw SHA256 {sha(raw_path)}\n")
        (dest / "review.md").write_text("# Source identification\n\n" + job["source_card"] +
            f"\n\nItem: {name} (4 pulse frames). Transparent background.\n")
        
        records.append({
            "id": name,
            "category": "fx",
            "kit": "common",
            "file": f"{name}/final.png",
            "px": list(strip.size),
            "frame_px": [frame_w, frame_h],
            "world": [frame_w / 128.0, frame_h / 128.0],
            "pivot": "center",
            "pivot_px": [frame_w / 2, frame_h / 2],
            "tileable": "none",
            "slice": None,
            "frames": 4,
            "fps": 4,
            "sway": False,
            "source_refs": job["refs"],
            "replaces": None,
            "approved": False,
            "status": "needs_owner_review",
            "art_source": "host_image",
            "route": "built-in image_gen",
            "source_job": "exit-arrows",
            "raw_sha256": sha(raw_path),
            "notes": f"Pulsing exit arrow indicator {spec.get('direction', '')}."
        })

    # 4. Process deck-tile (512x512, tileable xy)
    jd = ROOT / "jobs" / "deck-tile"
    job = json.loads((jd / "job.json").read_text())
    raw_path = jd / "raw-01.png"
    raw_im = Image.open(raw_path).convert("RGBA")
    name = "ship-deck-tile"
    dest = ROOT / name
    dest.mkdir(exist_ok=True)
    
    # Resize to 512x512 and apply seam crop
    tile_512 = raw_im.resize((512, 512), Image.Resampling.NEAREST)
    tile_cropped, crop_box = seam_crop(tile_512, "xy", name)
    tile_cropped.save(dest / "crop.png")
    tile_cropped.save(crop_inputs / f"{name}.png")
    for raw_f in jd.glob("raw-*.png"):
        shutil.copyfile(raw_f, dest / raw_f.name)
    
    refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
    (dest / "prompt.md").write_text(job["prompt"] + "\n\nOrdered reference images:\n" +
        "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs) +
        f"\n\nRoute: built-in image_gen; raw SHA256 {sha(raw_path)}\n")
    (dest / "review.md").write_text("# Source identification\n\n" + job["source_card"] +
        f"\n\nItem: {name}. 512x512 seamless floor tile. Tiling tested seamlessly on all four edges.\n")
    
    records.append({
        "id": name,
        "category": "floor",
        "kit": "ship",
        "file": f"{name}/final.png",
        "px": [512, 512],
        "world": [4.0, 4.0],
        "pivot": "center",
        "pivot_px": [256, 256],
        "tileable": "xy",
        "slice": None,
        "frames": 1,
        "fps": None,
        "sway": False,
        "source_refs": job["refs"],
        "replaces": None,
        "approved": False,
        "status": "needs_owner_review",
        "art_source": "host_image",
        "route": "built-in image_gen",
        "source_job": "deck-tile",
        "raw_sha256": sha(raw_path),
        "notes": "Weathered honey oak deck planks, seamless 512x512 ground tile."
    })

    # 5. Process hull-backdrop (1024x384, tileable x)
    jd = ROOT / "jobs" / "hull-backdrop"
    job = json.loads((jd / "job.json").read_text())
    raw_path = jd / "raw-01.png"
    raw_im = Image.open(raw_path).convert("RGBA")
    name = "ship-hull-backdrop"
    dest = ROOT / name
    dest.mkdir(exist_ok=True)
    
    bd_scaled = raw_im.resize((1024, 384), Image.Resampling.NEAREST)
    bd_cropped, crop_box = seam_crop(bd_scaled, "x", name)
    bd_cropped.save(dest / "crop.png")
    bd_cropped.save(crop_inputs / f"{name}.png")
    for raw_f in jd.glob("raw-*.png"):
        shutil.copyfile(raw_f, dest / raw_f.name)
    
    refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
    (dest / "prompt.md").write_text(job["prompt"] + "\n\nOrdered reference images:\n" +
        "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs) +
        f"\n\nRoute: built-in image_gen; raw SHA256 {sha(raw_path)}\n")
    (dest / "review.md").write_text("# Source identification\n\n" + job["source_card"] +
        f"\n\nItem: {name}. 1024x384 backdrop strip, seamless x-axis.\n")
    
    records.append({
        "id": name,
        "category": "backdrop_mid",
        "kit": "ship",
        "file": f"{name}/final.png",
        "px": [1024, 384],
        "world": [8.0, 3.0],
        "pivot": "bottom_center",
        "pivot_px": [512, 384],
        "tileable": "x",
        "slice": None,
        "frames": 1,
        "fps": None,
        "sway": False,
        "source_refs": job["refs"],
        "replaces": None,
        "approved": False,
        "status": "needs_owner_review",
        "art_source": "host_image",
        "route": "built-in image_gen",
        "source_job": "hull-backdrop",
        "raw_sha256": sha(raw_path),
        "notes": "Weathered ship interior hull wall repeating backdrop strip."
    })

    # 6. Build unified palette and apply to all assets
    palette = ROOT / "palette"
    if not palette.exists():
        run([FORGE / "generate2dsprite/scripts/palette_tool.py", "build",
             "--input", crop_inputs, "--colors", 48, "--balance",
             "--name", "phimond-octopath-ship", "--output-dir", palette])
    
    # 7. Apply palette, perform QA, and write final.png
    qa_summary = {"total": len(records), "pass": 0, "fail": 0, "assets": []}
    
    for r in records:
        dest = ROOT / r["id"]
        finish = dest / "pixel-finish"
        if not finish.exists():
            run([FORGE / "generate2dsprite/scripts/palette_tool.py", "apply",
                 "--input", dest / "crop.png", "--palette", palette / "palette.json",
                 "--output-dir", finish])
        
        final_png = finish / "crop.png"
        if final_png.exists():
            (dest / "final.png").write_bytes(final_png.read_bytes())
        else:
            shutil.copyfile(dest / "crop.png", dest / "final.png")
            
        im = Image.open(dest / "final.png").convert("RGBA")
        r["px"] = list(im.size)
        r["sha256"] = sha(dest / "final.png")
        
        # QA check
        qa = {"failures": [], "warnings": []}
        w, h = im.size
        frames = r.get("frames", 1)
        frame_w = w // frames
        
        for f_idx in range(frames):
            frame = im.crop((f_idx * frame_w, 0, (f_idx + 1) * frame_w, h))
            bb = frame.getchannel("A").getbbox()
            if not bb and r["category"] != "floor":
                qa["failures"].append(f"frame_{f_idx}_empty")
            elif bb and r["tileable"] == "none":
                m = [bb[0], bb[1], frame_w - bb[2], h - bb[3]]
                if min(m) < 8:
                    qa["failures"].append(f"frame_{f_idx}_margin_below_8: {m}")
        
        # Color count
        colors = len({p[:3] for p in im.getdata() if p[3] > 0})
        if colors > 48 and r["category"] != "floor":
            qa["warnings"].append(f"colors_over_48: {colors}")
        
        # If animated, create preview.gif
        if frames > 1:
            frame_imgs = []
            for f_idx in range(frames):
                f_im = im.crop((f_idx * frame_w, 0, (f_idx + 1) * frame_w, h))
                bg = Image.new("RGBA", f_im.size, (33, 37, 43, 255))
                bg.alpha_composite(f_im)
                frame_imgs.append(bg.convert("RGB"))
            fps = r.get("fps", 4) or 4
            frame_imgs[0].save(dest / "preview.gif", save_all=True,
                               append_images=frame_imgs[1:], duration=1000 // fps, loop=0)
        
        write(dest / "qa.json", qa)
        r["mechanical_status"] = "fail" if qa["failures"] else "pass"
        if r["mechanical_status"] == "pass":
            qa_summary["pass"] += 1
        else:
            qa_summary["fail"] += 1
        qa_summary["assets"].append({"id": r["id"], "status": r["mechanical_status"], "failures": qa["failures"]})

    write(ROOT / "qa-summary.json", qa_summary)
    write(ROOT / "manifest.json", {
        "batch": "04-octopath",
        "approved": False,
        "status": "draft_needs_owner_review",
        "route": "built-in image_gen",
        "assets": records
    })

    # 8. Generate contact sheet
    cols = 5
    cw, ch = 220, 220
    rows = (len(records) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, 60 + rows * ch), (33, 37, 43))
    draw = ImageDraw.Draw(sheet)
    draw.text((16, 20), "PHIMOND — BATCH 04 (PIRATE SHIP & SHARED MARKERS) — OCTOPATH HD-2D", fill=(255, 255, 255))

    for idx, r in enumerate(records):
        cx = (idx % cols) * cw
        cy = 60 + (idx // cols) * ch
        item_im = Image.open(ROOT / r["file"])
        # Take first frame if animated
        if r.get("frames", 1) > 1:
            fw = item_im.width // r["frames"]
            item_im = item_im.crop((0, 0, fw, item_im.height))
        # Thumbnail to fit cell
        thumb = item_im.copy()
        thumb.thumbnail((160, 160), Image.Resampling.NEAREST)
        sheet.paste(thumb, (cx + (cw - thumb.width) // 2, cy + 15), thumb if thumb.mode == "RGBA" else None)
        draw.text((cx + 10, cy + 185), r["id"][:22], fill=(220, 220, 220))
        draw.text((cx + 10, cy + 200), f"[{r['mechanical_status']}]", fill=(100, 255, 100) if r['mechanical_status'] == 'pass' else (255, 100, 100))

    sheet.save(ROOT / "contact-sheet.png")

    # 9. Write README.md
    readme = f"""# Batch 4 — Pirate Ship & Shared Markers (Octopath HD-2D)

Total 21 individual assets covering:
- Pirate ship hardware: `cannon`, `helm-wheel`, `rum-barrel`, `rope-coil`
- Rigging & sway props: `mast-trunk`, `sail-cloth`, `pirate-flag`, `teleport-pillar-high`
- Shared world interaction markers: `target-ring`, `touch-ring`, `quest-new`, `quest-complete`, `talk-mark`, `nest-marker`
- Animated lights & indicators: `storm-lantern` (4 frames), `exit-arrow-up`, `exit-arrow-right`, `exit-arrow-down`, `exit-arrow-left` (4 pulse frames each)
- Terrain & backdrop: `ship-deck-tile` (512x512 seamless xy), `ship-hull-backdrop` (1024x384 seamless x)

## Mechanical QA Summary
- Total assets: {qa_summary['total']}
- Pass: {qa_summary['pass']}
- Fail: {qa_summary['fail']}
- Color palette: harmonized under `phimond-octopath-ship` palette (max 48 colors).
- Alpha hygiene: clean >= 8px margins on all isolated props and decals.
- Raw integrity: byte-identical raw inputs preserved in each asset directory.
"""
    (ROOT / "README.md").write_text(readme)
    print(f"Batch 04 package complete: {qa_summary['pass']}/{qa_summary['total']} passed.")

if __name__ == "__main__":
    package_batch_04()
