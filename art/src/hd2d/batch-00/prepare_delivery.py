"""Package image-generated art only. No procedural drawing or runtime activation."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable
FORGE = Path("/Users/phileanh/.codex/skills")
JOBS = json.loads((ROOT / "generation-jobs.json").read_text())
BY_JOB = {j["id"]: j for j in JOBS["jobs"]}
RECORDS = []

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

def stage(asset_id, kit, category, source, job_id, target_body_height=None, target_canvas=None, pack=None):
    job = BY_JOB[job_id]
    dest = ROOT / asset_id
    dest.mkdir(exist_ok=True)
    im = Image.open(source).convert("RGBA")
    bbox = im.getchannel("A").getbbox()
    if category != "floor":
        im = im.crop(bbox)
        if target_canvas:
            max_w, max_h = target_canvas[0]-16, target_canvas[1]-16
            ratio = min(max_w/im.width, max_h/im.height)
            size = (max(1, round(im.width*ratio)), max(1, round(im.height*ratio)))
            im = im.resize(size, Image.Resampling.NEAREST)
            canvas = Image.new("RGBA", target_canvas)
            canvas.alpha_composite(im, ((canvas.width-im.width)//2, (canvas.height-im.height)//2))
        else:
            if target_body_height:
                size = (max(1, round(im.width*target_body_height/im.height)), target_body_height)
                im = im.resize(size, Image.Resampling.NEAREST)
            canvas = Image.new("RGBA", (im.width+16, im.height+16))
            canvas.alpha_composite(im, (8,8))
        im = canvas
    im.save(dest / "crop.png")
    # Every raw remains byte-identical. Never rewrite a raw image.
    for raw in job["raw"]:
        shutil.copy2(ROOT / job_id / raw, dest / raw)
    refs = [{"path": p, "sha256": sha(p)} for p in job["refs"]]
    raw_hashes = {p: sha(dest/p) for p in job["raw"]}
    prompt = "# Image generation provenance\n\n"
    prompt += f"Route: host_image / built-in image_gen\nModel: not exposed by tool\nSource job: {job_id}\n\n"
    for index, text in enumerate(job["prompts"], 1):
        prompt += f"## Attempt {index}\n\n{text}\n\n"
    prompt += "## Ordered source references (first generation)\n\n"
    prompt += "\n".join(f'- {r["path"]} — sha256 {r["sha256"]}' for r in refs) + "\n\n"
    prompt += "Image-edit attempts use the previous raw as their edit target, as recorded in generation-jobs.json.\n\n"
    prompt += "## Raw SHA256\n\n" + "\n".join(f"- {k}: {v}" for k,v in raw_hashes.items()) + "\n"
    (dest/"prompt.md").write_text(prompt)
    input_dir = ROOT/"finish-inputs"/kit
    input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dest/"crop.png", input_dir/(asset_id+".png"))
    rec = {
        "id": asset_id, "category": category, "kit": kit, "file": asset_id+"/final.png",
        "px": list(im.size), "world": [round(im.width/128,6),round(im.height/128,6)],
        "pivot": "center" if category.startswith("ui") or category=="floor" else "bottom_center",
        "tileable": "xy" if category=="floor" else "none",
        "slice": [360,160,120,160] if category=="ui_9slice" else None,
        "frames": 1, "fps": None, "sway": False, "source_refs": job["refs"],
        "replaces": ("apps/game-web/public/scenes/forest.json" if kit=="forest" else
                     "apps/game-web/public/scenes/severa.json" if kit=="city" else None),
        "notes": "Unapproved Batch 00 style candidate. PNG extracted from generated art; no scene activation.",
        "art_source": "host_image", "route": "built-in image_gen", "model": None,
        "source_job": job_id, "source_file": str(Path(source).relative_to(ROOT)),
        "source_sha256": sha(source), "raw_sha256": raw_hashes,
        "transforms": ["Forge extraction/key removal", "alpha crop", "nearest size normalization", "8px alpha padding",
                       "Forge shared 48-color pixel finish"],
        "approved": False, "status": "needs_owner_review",
    }
    if category.startswith("ui"):
        rec["ui_design_canvas"]=[960,640]
        rec["ui_scale"]=3
        rec["design_px"]=[round(im.width/3,4),round(im.height/3,4)]
        rec["world"]=[round(im.width/128,6),round(im.height/128,6)]
        rec["notes"]+=" UI world is schema compatibility only; render in canvas pixels at @3x."
        rec["replaces"]=None
    if category=="ui_sprite":
        rec["text_axis_degrees"]=37
    if pack:
        rec["forge_extraction_manifest"]=pack
    RECORDS.append(rec)

for variant in ("a","b"):
    pack_dir = ROOT/f"forge-forest-{variant}-reviewed"
    pack = json.loads((pack_dir/"prop-pack.json").read_text())
    heights = {"tree":410,"bush":145,"grass":65,"yellow-flowers":80,"pink-flowers":80,"fern":80}
    for item in pack["accepted"]:
        name=item["label"]
        stage(f"forest-{variant}-{name}", "forest", "prop", pack_dir/item["image"],
              f"forest-{variant}-sheet", target_body_height=heights[name],
              pack=f"forge-forest-{variant}-reviewed/prop-pack.json")

pack_dir=ROOT/"forge-city"
for item in json.loads((pack_dir/"prop-pack.json").read_text())["accepted"]:
    name=item["label"]
    stage(f"city-{name}", "city", "prop", pack_dir/item["image"], "city-sheet",
          target_body_height=320 if name.startswith("lamp") else 96,
          pack="forge-city/prop-pack.json")

pack_dir=ROOT/"forge-ui"
for item in json.loads((pack_dir/"prop-pack.json").read_text())["accepted"]:
    name=item["label"]
    stage(f"ui-{name}", "ui", "ui_9slice" if name.startswith("panel") else "ui_sprite",
          pack_dir/item["image"], "ui-sheet",
          target_canvas=(1476,696) if name.startswith("panel") else (201,186),
          pack="forge-ui/prop-pack.json")

# The caller selects a whole generated attempt, never manufactures a seamless border.
terrain_dir=ROOT/BY_JOB["terrain-sheet"].get("selected_extract","forge-terrain")
for kit in ("forest","city"):
    for index, variant in enumerate(("a","b"),1):
        source=terrain_dir/f"{kit}-{index}.png"
        if not source.exists():
            matches=list(terrain_dir.rglob(f"{kit}-{index}.png"))
            if len(matches)!=1:
                raise RuntimeError(f"Cannot locate {kit}-{index}.png")
            source=matches[0]
        stage(f"{kit}-{variant}-floor", kit, "floor", source, "terrain-sheet")

save_json(ROOT/"staged-assets.json", RECORDS)
for job in JOBS["jobs"]:
    path=ROOT/job["id"]
    path.mkdir(exist_ok=True)
    (path/"prompt.md").write_text(
        "\n\n".join(f"## Attempt {i}\n\n{p}" for i,p in enumerate(job["prompts"],1))+
        "\n\n## Ordered source references\n\n"+
        "\n".join(f"- {p} — sha256 {sha(p)}" for p in job["refs"])+"\n")
for kit in ("forest","city","ui"):
    palette=ROOT/"palettes"/kit
    finished=ROOT/"finished"/kit
    script=FORGE/"generate2dsprite/scripts/palette_tool.py"
    # Deterministic palette finishing, not hand-painted code art.
    for args in [
        ["build","--input",str(ROOT/"finish-inputs"/kit),"--colors","48","--balance",
         "--name",f"phimond-{kit}","--output-dir",str(palette)],
        ["apply","--input",str(ROOT/"finish-inputs"/kit),"--palette",str(palette/"palette.json"),
         "--output-dir",str(finished)],
    ]:
        result=subprocess.run([PYTHON,str(script),*args],text=True,capture_output=True)
        print(result.stdout.strip(), flush=True)
        if result.returncode:
            print(result.stderr, file=sys.stderr)
            raise SystemExit(result.returncode)
print(json.dumps({"staged":len(RECORDS)}))

