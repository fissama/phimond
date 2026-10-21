"""Prepare Batch 10 (Login, Loading, Branding) job manifests and raw files.
"""
from pathlib import Path
import json, hashlib, shutil
from PIL import Image

R = Path(__file__).resolve().parent
REPO = Path("/Users/phileanh/rust/phimond")
BRAIN = Path("/Users/phileanh/.gemini/antigravity-ide/brain/011c27ea-b148-400e-9b78-4882eb990740")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def prepare_jobs():
    jobs_dir = R / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)

    # 1. Branding pack job
    branding_job_dir = jobs_dir / "branding-pack"
    branding_job_dir.mkdir(exist_ok=True)
    branding_raw = BRAIN / "branding_pack_magenta_1792071787471.jpg"
    shutil.copyfile(branding_raw, branding_job_dir / "raw-01.png")

    branding_job = {
        "id": "branding-pack",
        "rows": 2,
        "cols": 2,
        "key": [255, 0, 255],
        "assets": [
            {"id": "logo-horizontal", "desc": "Horizontal logo banner with crisp pixel typography spelling PHIMOND with spirit beast crest", "category": "ui_sprite", "px": [512, 128]},
            {"id": "logo-badge", "desc": "Square/circular logo medallion with stylized spirit beast crest and geometric bronze ring", "category": "ui_sprite", "px": [384, 384]},
            {"id": "app-icon", "desc": "App icon badge featuring golden spirit beast crest on deep sapphire shield", "category": "icon", "px": [384, 384]},
            {"id": "map-card-frame", "desc": "Map card frame with antique brass corners, parchment inner border, and emerald gem sockets", "category": "ui_9slice", "px": [384, 480], "slice": [48, 48, 48, 48]}
        ],
        "refs": [
            str(REPO / "apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png"),
            str(REPO / "apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png")
        ],
        "prompt": "Production branding asset sheet for Phimond RPG, authentic Octopath Traveler HD-2D pixel art style. 4 isolated branding elements arranged in 2x2 grid with wide spacing on flat magenta #FF00FF.",
        "source_card": "Master plan Batch 10 branding: Phimond custom logo, crest badge, app icon, and world map transition frame."
    }
    (branding_job_dir / "job.json").write_text(json.dumps(branding_job, indent=2))
    (branding_job_dir / "prompt.md").write_text(branding_job["prompt"] + "\n\nReferences:\n" + "\n".join(branding_job["refs"]))

    # 2. Login panorama job
    login_job_dir = jobs_dir / "login-scene"
    login_job_dir.mkdir(exist_ok=True)
    login_raw = BRAIN / "login_bg_scene_1792071814061.jpg"
    shutil.copyfile(login_raw, login_job_dir / "raw-01.png")

    login_job = {
        "id": "login-scene",
        "rows": 1,
        "cols": 1,
        "assets": [
            {"id": "login-panorama", "desc": "Grand title and login screen panoramic landscape, morning sun shafts over emerald forest and distant royal palace", "category": "login", "px": [1280, 720]}
        ],
        "refs": [
            str(REPO / "apps/game-client/assets/extracted/extended/rooms/sbw_v32_Texture2D_2020_06_14_231047_1470x603.png"),
            str(REPO / "apps/game-client/assets/extracted/extended/rooms/sbw_v32_Texture2D_ld_900x680.png")
        ],
        "prompt": "Grand title and login screen panoramic landscape for Phimond RPG, authentic Octopath Traveler HD-2D pixel art style. 16:9 wide composition.",
        "source_card": "Original APK rooms 2020_06_14_231047 (1470x603) and ld_900x680 inspected. HD-2D dawn landscape with palace, forest, and ancient waypoint."
    }
    (login_job_dir / "job.json").write_text(json.dumps(login_job, indent=2))
    (login_job_dir / "prompt.md").write_text(login_job["prompt"] + "\n\nReferences:\n" + "\n".join(login_job["refs"]))

    # 3. Intro scenes job
    intro_job_dir = jobs_dir / "intro-scenes"
    intro_job_dir.mkdir(exist_ok=True)
    intro_raws = [
        BRAIN / "phimond_intro_01_1792071836379.jpg",
        BRAIN / "phimond_intro_02_1792071857340.jpg",
        BRAIN / "phimond_intro_03_1792071882020.jpg"
    ]
    for i, raw_f in enumerate(intro_raws):
        shutil.copyfile(raw_f, intro_job_dir / f"raw-0{i+1}.png")

    intro_job = {
        "id": "intro-scenes",
        "rows": 1,
        "cols": 3,
        "assets": [
            {"id": "intro-01-world", "desc": "Story intro 1: Young adventurer looking out over continent with winged companion", "category": "login", "px": [1280, 720]},
            {"id": "intro-02-companion", "desc": "Story intro 2: Sacred sanctuary grove, raising spirit beasts with elemental orbs", "category": "login", "px": [1280, 720]},
            {"id": "intro-03-journey", "desc": "Story intro 3: Adventuring party exploring ancient ruins gateway under starry twilight", "category": "login", "px": [1280, 720]}
        ],
        "refs": [
            "/Users/phileanh/Downloads/Pokezoo-100-extracted/viewable/assets/original-png/intro1.png",
            "/Users/phileanh/Downloads/Pokezoo-100-extracted/viewable/assets/original-png/intro2.png",
            "/Users/phileanh/Downloads/Pokezoo-100-extracted/viewable/assets/original-png/intro3.png"
        ],
        "prompt": "3 story intro illustrations for Phimond RPG, Octopath Traveler HD-2D pixel art style.",
        "source_card": "Original Pokezoo intro1-3.png and public/assets/login/intro1-3.webp replacement."
    }
    (intro_job_dir / "job.json").write_text(json.dumps(intro_job, indent=2))
    (intro_job_dir / "prompt.md").write_text(intro_job["prompt"] + "\n\nReferences:\n" + "\n".join(intro_job["refs"]))

    # 4. Loading UI & Screen job
    loading_job_dir = jobs_dir / "loading-ui"
    loading_job_dir.mkdir(exist_ok=True)
    shutil.copyfile(BRAIN / "loading_ui_pack_1792071902537.jpg", loading_job_dir / "raw-01.png")
    shutil.copyfile(BRAIN / "loading_bg_screen_1792071922467.jpg", loading_job_dir / "raw-02.png")

    loading_job = {
        "id": "loading-ui",
        "rows": 3,
        "cols": 1,
        "key": [255, 0, 255],
        "assets": [
            {"id": "loading-bar-frame", "desc": "Ornate antique bronze and dark iron progress bar frame with corner ornaments and gem setting", "category": "ui_9slice", "px": [650, 80], "slice": [40, 20, 40, 20]},
            {"id": "loading-bar-fill", "desc": "Progress bar inner fill strip of segmented luminous teal-cyan and gold spirit crystal", "category": "ui_sprite", "px": [560, 40]},
            {"id": "loading-ornament-corners", "desc": "Ornamental decorative filigree corner trim pieces and crystal spinner symbol", "category": "ui_sprite", "px": [512, 160]},
            {"id": "loading-bg", "desc": "Atmospheric loading screen background, sanctuary chamber with star-map altar and crescent moon", "category": "login", "px": [1280, 720]}
        ],
        "refs": [
            str(REPO / "apps/game-client/assets/extracted/extended/rooms/sbw_v32_Sprite_loadingbg_653x79.png"),
            str(REPO / "apps/game-client/assets/extracted/extended/rooms/sbw_v32_Sprite_loadingbar_564x43.png"),
            str(REPO / "apps/game-client/assets/extracted/extended/rooms/sbw_v32_Texture2D_ld_900x680.png")
        ],
        "prompt": "Loading screen elements and atmospheric background for Phimond RPG, Octopath Traveler HD-2D pixel art style.",
        "source_card": "Original loadingbg (653x79) and loadingbar (564x43) replacements."
    }
    (loading_job_dir / "job.json").write_text(json.dumps(loading_job, indent=2))
    (loading_job_dir / "prompt.md").write_text(loading_job["prompt"] + "\n\nReferences:\n" + "\n".join(loading_job["refs"]))

    print("Batch 10 jobs prepared successfully!")

if __name__ == "__main__":
    prepare_jobs()
