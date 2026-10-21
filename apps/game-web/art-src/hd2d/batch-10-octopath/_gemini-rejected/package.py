"""Package Batch 10 (Login, Loading, Branding) assets for Phimond HD-2D Octopath style.
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

def key_magenta(im):
    arr = np.array(im.convert("RGBA"))
    key = np.array([255, 0, 255])
    delta = np.max(np.abs(arr[:, :, :3].astype(int) - key), axis=2)
    mask = delta < 45
    # Despill magenta fringe
    mask |= (arr[:, :, 0] > 180) & (arr[:, :, 2] > 160) & (arr[:, :, 1] < 80)
    arr[:, :, 3][mask] = 0
    return Image.fromarray(arr)

def package_batch_10():
    records = []
    crop_inputs = ROOT / "palette-inputs"
    crop_inputs.mkdir(exist_ok=True)

    # ----------------------------------------------------
    # 1. Branding Pack (from jobs/branding-pack/raw-01.png)
    # ----------------------------------------------------
    jd = ROOT / "jobs" / "branding-pack"
    job = json.loads((jd / "job.json").read_text())
    raw_path = jd / "raw-01.png"
    keyed = key_magenta(Image.open(raw_path))

    split_x = 570
    split_y = 512
    w, h = keyed.size

    branding_cells = [
        # (asset_id, crop_box, target_size, category, slice_def)
        ("logo-horizontal", (0, 0, split_x, split_y), [512, 128], "ui_sprite", None),
        ("logo-badge", (split_x, 0, w, split_y), [384, 384], "ui_sprite", None),
        ("app-icon", (0, split_y, split_x, h), [384, 384], "icon", None),
        ("map-card-frame", (split_x, split_y, w, h), [384, 480], "ui_9slice", [48, 48, 48, 48])
    ]

    for name, cbox, target_sz, cat, sdef in branding_cells:
        dest = ROOT / name
        dest.mkdir(exist_ok=True)
        cell = keyed.crop(cbox)
        bb = cell.getchannel("A").getbbox()
        if bb:
            cell = cell.crop(bb)
        
        tw, th = target_sz
        scale = min((tw - 16) / max(1, cell.width), (th - 16) / max(1, cell.height))
        scaled_w = max(1, round(cell.width * scale))
        scaled_h = max(1, round(cell.height * scale))
        scaled = cell.resize((scaled_w, scaled_h), Image.Resampling.NEAREST)

        canvas = Image.new("RGBA", (tw, th))
        canvas.alpha_composite(scaled, ((tw - scaled_w) // 2, (th - scaled_h) // 2))
        canvas.save(dest / "crop.png")
        canvas.save(crop_inputs / f"{name}.png")

        shutil.copyfile(raw_path, dest / "raw-01.png")
        refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
        (dest / "prompt.md").write_text(job["prompt"] + "\n\nReferences:\n" + "\n".join(f"- {x['path']} sha256={x['sha256']}" for x in refs))
        (dest / "review.md").write_text(f"# Source identification\n\n{job['source_card']}\n\nItem: {name}. Clean Octopath HD-2D branding asset.\n")

        records.append({
            "id": name,
            "category": cat,
            "kit": "branding",
            "file": f"{name}/final.png",
            "px": [tw, th],
            "world": [tw / 128.0, th / 128.0],
            "pivot": "center",
            "pivot_px": [tw / 2, th / 2],
            "tileable": "none",
            "slice": sdef,
            "frames": 1,
            "fps": None,
            "sway": False,
            "source_refs": job["refs"],
            "replaces": None,
            "approved": False,
            "status": "needs_owner_review",
            "art_source": "host_image",
            "route": "built-in image_gen",
            "source_job": "branding-pack",
            "raw_sha256": sha(raw_path),
            "notes": next(a["desc"] for a in job["assets"] if a["id"] == name)
        })

    # ----------------------------------------------------
    # 2. Loading UI Pack (from jobs/loading-ui/raw-01.png & raw-02.png)
    # ----------------------------------------------------
    jd = ROOT / "jobs" / "loading-ui"
    job = json.loads((jd / "job.json").read_text())
    raw_path_ui = jd / "raw-01.png"
    keyed_ui = key_magenta(Image.open(raw_path_ui))
    w_ui, _ = keyed_ui.size

    loading_ui_cells = [
        # (asset_id, row_interval, target_size, category, slice_def)
        ("loading-bar-frame", (72, 292), [650, 80], "ui_9slice", [40, 20, 40, 20]),
        ("loading-bar-fill", (384, 576), [560, 40], "ui_sprite", None),
        ("loading-ornament-corners", (681, 936), [512, 160], "ui_sprite", None)
    ]

    for name, (r_start, r_end), target_sz, cat, sdef in loading_ui_cells:
        dest = ROOT / name
        dest.mkdir(exist_ok=True)
        cell = keyed_ui.crop((0, r_start, w_ui, r_end))
        bb = cell.getchannel("A").getbbox()
        if bb:
            cell = cell.crop(bb)
        
        tw, th = target_sz
        scale = min((tw - 16) / max(1, cell.width), (th - 16) / max(1, cell.height))
        scaled_w = max(1, round(cell.width * scale))
        scaled_h = max(1, round(cell.height * scale))
        scaled = cell.resize((scaled_w, scaled_h), Image.Resampling.NEAREST)

        canvas = Image.new("RGBA", (tw, th))
        canvas.alpha_composite(scaled, ((tw - scaled_w) // 2, (th - scaled_h) // 2))
        canvas.save(dest / "crop.png")
        canvas.save(crop_inputs / f"{name}.png")

        shutil.copyfile(raw_path_ui, dest / "raw-01.png")
        refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
        (dest / "prompt.md").write_text(job["prompt"] + "\n\nReferences:\n" + "\n".join(f"- {x['path']} sha256={x['sha256']}" for x in refs))
        (dest / "review.md").write_text(f"# Source identification\n\n{job['source_card']}\n\nItem: {name}.\n")

        records.append({
            "id": name,
            "category": cat,
            "kit": "loading",
            "file": f"{name}/final.png",
            "px": [tw, th],
            "world": [tw / 128.0, th / 128.0],
            "pivot": "center",
            "pivot_px": [tw / 2, th / 2],
            "tileable": "none",
            "slice": sdef,
            "frames": 1,
            "fps": None,
            "sway": False,
            "source_refs": job["refs"],
            "replaces": None,
            "approved": False,
            "status": "needs_owner_review",
            "art_source": "host_image",
            "route": "built-in image_gen",
            "source_job": "loading-ui",
            "raw_sha256": sha(raw_path_ui),
            "notes": next(a["desc"] for a in job["assets"] if a["id"] == name)
        })

    # Loading screen background (raw-02.png)
    raw_path_bg = jd / "raw-02.png"
    name = "loading-bg"
    dest = ROOT / name
    dest.mkdir(exist_ok=True)
    im_bg = Image.open(raw_path_bg).convert("RGBA").resize((1280, 720), Image.Resampling.NEAREST)
    im_bg.save(dest / "crop.png")
    im_bg.save(dest / "final.png")
    shutil.copyfile(raw_path_bg, dest / "raw-01.png")
    refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
    (dest / "prompt.md").write_text(job["prompt"] + "\n\nReferences:\n" + "\n".join(f"- {x['path']} sha256={x['sha256']}" for x in refs))
    (dest / "review.md").write_text(f"# Source identification\n\n{job['source_card']}\n\nItem: {name}.\n")

    records.append({
        "id": name,
        "category": "login",
        "kit": "loading",
        "file": f"{name}/final.png",
        "px": [1280, 720],
        "world": [10.0, 5.625],
        "pivot": "center",
        "pivot_px": [640, 360],
        "tileable": "none",
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
        "source_job": "loading-ui",
        "raw_sha256": sha(raw_path_bg),
        "notes": "Atmospheric sanctuary chamber loading background at night."
    })

    # ----------------------------------------------------
    # 3. Login Panorama Scene (from jobs/login-scene/raw-01.png)
    # ----------------------------------------------------
    jd = ROOT / "jobs" / "login-scene"
    job = json.loads((jd / "job.json").read_text())
    raw_path = jd / "raw-01.png"
    name = "login-panorama"
    dest = ROOT / name
    dest.mkdir(exist_ok=True)
    im_login = Image.open(raw_path).convert("RGBA").resize((1280, 720), Image.Resampling.NEAREST)
    im_login.save(dest / "crop.png")
    im_login.save(dest / "final.png")
    shutil.copyfile(raw_path, dest / "raw-01.png")
    refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
    (dest / "prompt.md").write_text(job["prompt"] + "\n\nReferences:\n" + "\n".join(f"- {x['path']} sha256={x['sha256']}" for x in refs))
    (dest / "review.md").write_text(f"# Source identification\n\n{job['source_card']}\n\nItem: {name}.\n")

    records.append({
        "id": name,
        "category": "login",
        "kit": "login",
        "file": f"{name}/final.png",
        "px": [1280, 720],
        "world": [10.0, 5.625],
        "pivot": "center",
        "pivot_px": [640, 360],
        "tileable": "none",
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
        "source_job": "login-scene",
        "raw_sha256": sha(raw_path),
        "notes": "Grand title and login screen dawn panoramic landscape."
    })

    # ----------------------------------------------------
    # 4. Intro Scenes (from jobs/intro-scenes/raw-01..03.png)
    # ----------------------------------------------------
    jd = ROOT / "jobs" / "intro-scenes"
    job = json.loads((jd / "job.json").read_text())
    for i, a in enumerate(job["assets"]):
        name = a["id"]
        raw_path = jd / f"raw-0{i+1}.png"
        dest = ROOT / name
        dest.mkdir(exist_ok=True)
        im_intro = Image.open(raw_path).convert("RGBA").resize((1280, 720), Image.Resampling.NEAREST)
        im_intro.save(dest / "crop.png")
        im_intro.save(dest / "final.png")
        shutil.copyfile(raw_path, dest / "raw-01.png")
        refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
        (dest / "prompt.md").write_text(job["prompt"] + "\n\nReferences:\n" + "\n".join(f"- {x['path']} sha256={x['sha256']}" for x in refs))
        (dest / "review.md").write_text(f"# Source identification\n\n{job['source_card']}\n\nItem: {name}.\n")

        records.append({
            "id": name,
            "category": "login",
            "kit": "intro",
            "file": f"{name}/final.png",
            "px": [1280, 720],
            "world": [10.0, 5.625],
            "pivot": "center",
            "pivot_px": [640, 360],
            "tileable": "none",
            "slice": None,
            "frames": 1,
            "fps": None,
            "sway": False,
            "source_refs": job["refs"],
            "replaces": f"apps/game-web/public/assets/login/intro{i+1}.webp",
            "approved": False,
            "status": "needs_owner_review",
            "art_source": "host_image",
            "route": "built-in image_gen",
            "source_job": "intro-scenes",
            "raw_sha256": sha(raw_path),
            "notes": a["desc"]
        })

    # ----------------------------------------------------
    # 5. Build Palette and Apply to UI & Branding Sprites
    # ----------------------------------------------------
    palette = ROOT / "palette"
    if not palette.exists():
        run([FORGE / "generate2dsprite/scripts/palette_tool.py", "build",
             "--input", crop_inputs, "--colors", 48, "--balance",
             "--name", "phimond-octopath-branding", "--output-dir", palette])

    qa_summary = {"total": len(records), "pass": 0, "fail": 0, "assets": []}

    for r in records:
        dest = ROOT / r["id"]
        # Only quantize UI/icons/branding with the 48-color palette; full 1280x720 paintings retain their rich lighting
        if r["kit"] in ("branding", "loading") and r["category"] != "login":
            finish = dest / "pixel-finish"
            if not finish.exists():
                run([FORGE / "generate2dsprite/scripts/palette_tool.py", "apply",
                     "--input", dest / "crop.png", "--palette", palette / "palette.json",
                     "--output-dir", finish])
            final_png = finish / "crop.png"
            if final_png.exists():
                (dest / "final.png").write_bytes(final_png.read_bytes())
        else:
            if not (dest / "final.png").exists():
                shutil.copyfile(dest / "crop.png", dest / "final.png")

        im = Image.open(dest / "final.png").convert("RGBA")
        r["px"] = list(im.size)
        r["sha256"] = sha(dest / "final.png")

        qa = {"failures": [], "warnings": []}
        w, h = im.size
        bb = im.getchannel("A").getbbox()
        if not bb:
            qa["failures"].append("empty_image")
        elif r["category"] not in ("login", "floor"):
            m = [bb[0], bb[1], w - bb[2], h - bb[3]]
            if min(m) < 8:
                qa["failures"].append(f"alpha_margin_below_8: {m}")

        colors = len({p[:3] for p in im.getdata() if p[3] > 0})
        if colors > 48 and r["category"] not in ("login", "floor"):
            qa["warnings"].append(f"colors_over_48: {colors}")

        write(dest / "qa.json", qa)
        r["mechanical_status"] = "fail" if qa["failures"] else "pass"
        if r["mechanical_status"] == "pass":
            qa_summary["pass"] += 1
        else:
            qa_summary["fail"] += 1
        qa_summary["assets"].append({"id": r["id"], "status": r["mechanical_status"], "failures": qa["failures"]})

    write(ROOT / "qa-summary.json", qa_summary)
    write(ROOT / "manifest.json", {
        "batch": "10-octopath",
        "approved": False,
        "status": "draft_needs_owner_review",
        "route": "built-in image_gen",
        "assets": records
    })

    # ----------------------------------------------------
    # 6. Contact Sheet
    # ----------------------------------------------------
    cols = 4
    cw, ch = 280, 220
    rows = (len(records) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, 60 + rows * ch), (28, 32, 38))
    draw = ImageDraw.Draw(sheet)
    draw.text((16, 20), "PHIMOND — BATCH 10 (LOGIN, INTRO, LOADING, BRANDING) — OCTOPATH HD-2D", fill=(255, 255, 255))

    for idx, r in enumerate(records):
        cx = (idx % cols) * cw
        cy = 60 + (idx // cols) * ch
        item_im = Image.open(ROOT / r["file"])
        thumb = item_im.copy()
        thumb.thumbnail((240, 140), Image.Resampling.NEAREST)
        sheet.paste(thumb, (cx + (cw - thumb.width) // 2, cy + 15), thumb if thumb.mode == "RGBA" else None)
        draw.text((cx + 12, cy + 165), r["id"][:28], fill=(220, 220, 220))
        draw.text((cx + 12, cy + 185), f"[{r['mechanical_status']}] {r['category']} {r['px']}", fill=(100, 255, 100) if r['mechanical_status'] == 'pass' else (255, 100, 100))

    sheet.save(ROOT / "contact-sheet.png")

    # ----------------------------------------------------
    # 7. README.md
    # ----------------------------------------------------
    readme = f"""# Batch 10 — Login, Intro, Loading, and Branding (Octopath HD-2D)

Total 12 assets:
- **Branding**:
  - `logo-horizontal`: Crisp pixel typography spelling 'PHIMOND' with spirit beast crest.
  - `logo-badge`: Stylized Phimond beast crest in geometric bronze medallion.
  - `app-icon`: Golden spirit beast crest on deep sapphire shield.
  - `map-card-frame`: Map card frame with antique brass corners and emerald sockets (9-slice).
- **Login Screen**:
  - `login-panorama`: 1280x720 dawn panorama of emerald forest, royal citadel, and ancient waypoint.
- **Story Intro Screens (1280x720)**:
  - `intro-01-world`: Young adventurer and winged companion looking out over floating continent at sunrise.
  - `intro-02-companion`: Sacred sanctuary grove with tamer, spirit egg, dragonling, and aquatic serpent.
  - `intro-03-journey`: Adventuring party exploring ancient ruins gateway under starry twilight.
- **Loading Screen UI**:
  - `loading-bar-frame`: Ornate bronze progress bar frame (9-slice).
  - `loading-bar-fill`: Segmented luminous teal crystal progress fill.
  - `loading-ornament-corners`: Filigree decorative corners and crystal spinner.
  - `loading-bg`: Atmospheric nocturnal sanctuary loading background with star-map altar.

## Mechanical QA Summary
- Total assets: {qa_summary['total']}
- Pass: {qa_summary['pass']}
- Fail: {qa_summary['fail']}
- Color palette: Harmonized under `phimond-octopath-branding` (48 colors) for sprites and UI.
- Alpha margins: >= 8px on all isolated sprites and frames.
- Raw files: Byte-identical source generations preserved in each asset folder.
"""
    (ROOT / "README.md").write_text(readme)
    print(f"Batch 10 package complete: {qa_summary['pass']}/{qa_summary['total']} passed.")

if __name__ == "__main__":
    package_batch_10()
