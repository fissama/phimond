#!/usr/bin/env python3
"""Kiểm tra layout.json do Gemini nộp cho một map so với brief và manifest kit.
Dùng: python3 validate_hd2d_map_layout.py <layout.json> [brief.json] [manifest.json ...]
Nếu bỏ brief: tìm .ai/design/map-briefs/*/<map_id>.json. Manifest mặc định: art-src/hd2d/batch-11-<kit>/manifest.json
Lỗi = thoát mã 1. Kiểm tra: neo không bị đổi chỗ, vật không đè vùng cấm, đủ ngân sách trang trí, asset tồn tại, vị trí trong ảnh, neo CẦN ĐẶT đã có vị trí."""
import json, sys, glob, pathlib

R = pathlib.Path(__file__).resolve().parents[2]
lay = json.load(open(sys.argv[1]))
mid = lay["map_id"]
bp = sys.argv[2] if len(sys.argv) > 2 else next(iter(glob.glob(str(R / f".ai/design/map-briefs/*/{mid}.json"))))
brief = json.load(open(bp))
kit = brief["kit"].replace("kit_", "")
mp = sys.argv[3:] or glob.glob(str(R / f"apps/game-web/art-src/hd2d/batch-11-{kit}/manifest.json"))
man = {}
for p in mp:
    for a in json.load(open(p))["assets"]:
        man[a["id"]] = a
W, H = brief["size_px"]
errs, warn = [], []

# 1. neo
by = {a["id"]: a for a in lay.get("anchors", [])}
keep = []
for a in brief["anchors"]:
    got = by.get(a["id"])
    if got is None:
        errs.append(f"thiếu neo {a['id']} trong layout"); continue
    if a.get("px"):
        if got.get("moved"):
            if not got.get("reason"): errs.append(f"neo {a['id']} bị dời nhưng không có reason")
            else: warn.append(f"neo {a['id']} dời: {got['reason']}")
        else:
            d = max(abs(got["px"][0] - a["px"][0]), abs(got["px"][1] - a["px"][1]))
            if d > 12: errs.append(f"neo {a['id']} lệch {d}px so với brief nhưng không đánh dấu moved")
        px = got["px"]
    else:
        if not got.get("px"): errs.append(f"neo CẦN ĐẶT {a['id']} chưa có px"); continue
        px = got["px"]
    ko = a.get("keepout_px")
    if ko:
        dx, dy = px[0] - a["px"][0], px[1] - a["px"][1]
        keep.append((a["id"], [ko[0] + dx, ko[1] + dy, ko[2] + dx, ko[3] + dy]))
    else:
        w, h = a["keepout_size_px"]; keep.append((a["id"], [px[0] - w // 2, px[1] - h, px[0] + w // 2, px[1]]))

# 2. vật đặt
cnt = {"small": 0, "medium": 0, "large": 0, "floor": 0}
for i, p in enumerate(lay.get("placements", [])):
    aid = p["asset"]; a = man.get(aid)
    if not a: errs.append(f"placement #{i}: asset '{aid}' không có trong manifest"); continue
    x, y = p["px"]; sc = p.get("scale", 1.0)
    if not (0 <= x <= W and 0 <= y <= H + 60): errs.append(f"placement #{i} {aid} ngoài ảnh ({x},{y})")
    ww, wh = a["world"]; w, h = ww * 100 * sc, wh * 100 * sc
    cat = a["category"]
    if cat in ("decal", "tile", "shadow", "edge"):
        cnt["floor"] += 1; continue
    if cat in ("backdrop", "backdrop_far"): continue
    box = [x - w / 2, y - 40, x + w / 2, y]  # chân vật: dải sâu 40px
    for kid, k in keep:
        if p.get("layer") == "back": continue
        if box[0] < k[2] and box[2] > k[0] and box[1] < k[3] and box[3] > k[1]:
            errs.append(f"{aid} tại ({x},{y}) đè vùng cấm của {kid}")
    hh = h
    cnt["large" if hh > 190 else "medium" if hh > 90 else "small"] += 1
b = brief["decor_budget_min"]
for k, kk in (("small", "small"), ("medium", "medium"), ("large", "large"), ("floor", "floor_decals")):
    if cnt[k] < b[kk]: errs.append(f"thiếu trang trí {k}: {cnt[k]} < {b[kk]}")
print(f"{mid}: placements {len(lay.get('placements', []))} đếm {cnt}  lỗi {len(errs)}  cảnh báo {len(warn)}")
for e in errs: print("  LỖI", e)
for w in warn: print("  lưu ý", w)
sys.exit(1 if errs else 0)
