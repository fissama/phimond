#!/usr/bin/env python3
"""Chuyển đổi layout.json của desert_entrance thành scene Three.js:
apps/game-web/public/scenes/desert_entrance_hd2d.json
Phục vụ render 3 góc camera (0.15, 0.50, 0.85) và zoom 2x khu vực Cổng, NPC Edda.
"""
import json, os, shutil, pathlib

R = pathlib.Path(__file__).resolve().parents[2]
layout_p = R / ".ai/design/map-layouts/desert/desert_entrance.json"
man_p = R / "apps/game-web/art-src/hd2d/batch-11-desert/manifest.json"
tex_dir = R / "apps/game-web/public/scenes/tex"
out_scene_p = R / "apps/game-web/public/scenes/desert_entrance_hd2d.json"

layout = json.load(open(layout_p))
manifest = json.load(open(man_p))
man_map = {a["id"]: a for a in manifest["assets"]}

# Đảm bảo sprite cho NPC Edda
npc_src = R / "apps/game-web/art-src/hd2d/batch-05-octopath/player-female/final.png"
npc_dst = tex_dir / "hd2d_npc-desert-edda.png"
if npc_src.exists():
    shutil.copyfile(npc_src, npc_dst)
    print(f"Copied NPC sprite to {npc_dst}")

# World conversion parameters
# Map width = 2514 px -> world x from 0.0 to 25.14
# Walkable Y band center ~ 560 px -> world z = 0.0
# px_y: 370 -> z = -2.09, px_y: 510 -> z = -0.55, px_y: 740 -> z = +1.98
def to_world(px_x, px_y):
    wx = round(px_x / 100.0, 3)
    wz = round((px_y - 560.0) / 100.0 * 1.1, 3)
    return wx, wz

props = []
flats = []
back = []

# 1. Backdrop
w_far = 16.0
for k in range(-1, 3):
    back.append({
        "tex": "hd2d_desert-dunes-wall-far.png",
        "x": round(6.0 + k * w_far, 3),
        "y": -0.45,
        "z": -3.8,
        "w": w_far,
        "h": 4.3
    })

w_mid = 8.0
for k in range(-2, 5):
    back.append({
        "tex": "hd2d_desert-dunes-mid.png",
        "x": round(4.0 + k * w_mid, 3),
        "y": -0.25,
        "z": -3.4,
        "w": w_mid,
        "h": 3.0
    })

w_near = 8.0
for k in range(-2, 5):
    back.append({
        "tex": "hd2d_desert-ruins-near.png",
        "x": round(4.0 + k * w_near, 3),
        "y": -0.10,
        "z": -3.0,
        "w": w_near,
        "h": 3.0
    })

# 2. Placements
for p in layout["placements"]:
    aid = p["asset"]
    a = man_map.get(aid)
    if not a:
        continue
    cat = a["category"]
    x, z = to_world(p["px"][0], p["px"][1])
    sc = p.get("scale", 1.0)
    w = round(a["world"][0] * sc, 3)
    h = round(a["world"][1] * sc, 3)
    tex_name = f"hd2d_{aid}.png"

    if cat in ("decal", "tile", "shadow", "edge"):
        flat_z = z
        if "shadow" in aid:
            # Shift shadow slightly backwards (z-) so it aligns cleanly under the sprite foot in 24-deg pitch
            flat_z = round(z - h * 0.20, 3)
        flats.append({
            "tex": tex_name,
            "x": x,
            "z": flat_z,
            "w": w,
            "d": h
        })
    elif cat in ("backdrop", "backdrop_far"):
        continue
    else:
        prop_entry = {
            "tex": tex_name,
            "x": x,
            "z": z,
            "w": w,
            "h": h
        }
        if aid == "desert-palm-canopy":
            prop_entry["y"] = 1.45
            prop_entry["sway"] = 1
        elif p.get("sway"):
            prop_entry["sway"] = 1
        if "anim" in aid:
            prop_entry["frames"] = 4
            prop_entry["fps"] = 5
            if aid in ("desert-dust-devil-anim", "desert-magic-rune-anim"):
                prop_entry["additive"] = 1
        props.append(prop_entry)

# 3. Add NPC Edda as standing sprite with shadow
edda_x, edda_z = to_world(1220, 510)
props.append({
    "tex": "hd2d_npc-desert-edda.png",
    "x": edda_x,
    "z": edda_z,
    "w": 1.31,
    "h": 1.31,
    "bob": 1
})
flats.append({
    "tex": "hd2d_desert-shadow-small-01.png",
    "x": edda_x,
    "z": round(edda_z + 0.02, 3),
    "w": 1.2,
    "d": 0.5
})

# Sort props and flats by depth (z) for clean draw ordering
props.sort(key=lambda p: p["z"])
flats.sort(key=lambda f: f["z"])

scene_data = {
    "id": "desert_entrance_hd2d",
    "name": "Cửa Ngõ Hoàng Mạc HD-2D",
    "bg": [0.24, 0.16, 0.08],
    "len": [-4.0, 29.0],
    "floor": [
        {
            "tex": "hd2d_desert-sand-floor-01.png",
            "x0": -10.0,
            "x1": 35.0,
            "z0": -9.0,
            "z1": 6.0,
            "tw": 4.0,
            "td": 4.0
        }
    ],
    "flats": flats,
    "back": back,
    "props": props,
    "lights": [],
    "particles": [
        {
            "kind": "dust",
            "count": 45,
            "color": [1.0, 0.88, 0.6],
            "size": 0.05
        },
        {
            "kind": "ember",
            "count": 10,
            "color": [1.0, 0.65, 0.25],
            "size": 0.06
        }
    ],
    "anim": [],
    "water": None,
    "ambient": {
        "color": [1.0, 0.96, 0.9],
        "strength": 1.2
    },
    "grade": {
        "sat": 1.05,
        "contrast": 1.04,
        "warm": 0.03,
        "vignette": 0.25,
        "fog": [0.78, 0.70, 0.55],
        "fogNear": 30,
        "fogFar": 75
    },
    "walk": {
        "x0": 0.5,
        "x1": 24.64,
        "z0": -2.4,
        "z1": 2.8
    }
}

with open(out_scene_p, "w", encoding="utf-8") as f:
    json.dump(scene_data, f, indent=2, ensure_ascii=False)

print(f"Generated scene JSON: {out_scene_p}")
print(f"Props: {len(props)}, Flats: {len(flats)}, Back: {len(back)}")
