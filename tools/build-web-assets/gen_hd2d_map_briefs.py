#!/usr/bin/env python3
"""Sinh brief bố cục HD-2D cho từng map: neo cố định (cổng, NPC, spawn) quy ra pixel của ảnh map gốc.

Đầu vào (chỉ đọc):
  .ai/plan/phases/P12-world/review/portal-edits/portal-graph.json   (cổng + liên kết, owner đã duyệt)
  .ai/plan/phases/P12-world/review/portal-package.json               (bounds, size ảnh gốc, tên map)
  .ai/plan/phases/P12-world/stage4/P12-S4-npc-roster.json            (NPC + apk_xy)
  .ai/plan/phases/P12-world/stage4/apk-extract/spawn-markers.json    (điểm spawn / TransEnemy)
  .ai/design/hd2d-maps-75-gemini-prompt.md                           (bảng kit → map, để gán kit và bảng màu)
Đầu ra: .ai/design/map-briefs/<kit>/<map_id>.json + .md, và index.json.

Quy ước toạ độ ảnh gốc: 100 px = 1 đơn vị APK. px_x = (x - xmin) * 100 ; px_y = (ymax - y) * 100 (đỉnh ảnh = ymax).
Neo là CHÂN vật (giữa-đáy). Giả định hướng trục Y cần được đối chiếu bằng mắt với ảnh gốc (cờ y_up_assumed).
Chạy: python3 tools/build-web-assets/gen_hd2d_map_briefs.py
"""
import json, re, pathlib, collections

R = pathlib.Path(__file__).resolve().parents[2]
P12 = R / ".ai/plan/phases/P12-world"
OUT = R / ".ai/design/map-briefs"
PXU = 100.0
KEEP = {"door": (200, 260), "arrival": (200, 260), "pillar": (220, 300), "npc": (140, 180),
        "spawn": (110, 110), "trans_enemy": (160, 160)}

graph = json.load(open(P12 / "review/portal-edits/portal-graph.json"))["graph"]
pkg = json.load(open(P12 / "review/portal-package.json"))
npcs = json.load(open(P12 / "stage4/P12-S4-npc-roster.json"))
spawns = json.load(open(P12 / "stage4/apk-extract/spawn-markers.json"))
maps = {m["id"]: m for m in pkg["maps"]}
ports = {p["id"]: p for p in graph["ports"]}

# --- kit từ prompt 75 map
kit_of, kit_meta, cur = {}, {}, None
for line in (R / ".ai/design/hd2d-maps-75-gemini-prompt.md").read_text().splitlines():
    m = re.match(r"### (kit_\w+) — (.+?) \(level", line)
    if m:
        cur = m.group(1); kit_meta[cur] = {"name": m.group(2), "style": ""}; continue
    if cur and line.startswith("**Phong cách/bảng màu:**"):
        kit_meta[cur]["style"] = line.split(":**", 1)[1].strip()
    m = re.match(r"\| `(\w+)` \|", line)
    if cur and m:
        kit_of[m.group(1)] = cur

name = lambda mid: maps.get(mid, {}).get("name", mid)
links_by_port = collections.defaultdict(list)
for l in graph["links"]:
    links_by_port[l["a"]].append((l["b"], l.get("oneway"), l.get("status"), l.get("comment")))
    if not l.get("oneway"):
        links_by_port[l["b"]].append((l["a"], False, l.get("status"), l.get("comment")))

def to_px(m, x, y):
    xmin, ymin, xmax, ymax = m["bounds"]
    return round((x - xmin) * PXU), round((ymax - y) * PXU)

def anchor(kind, m, xy, **kw):
    px, py = to_px(m, *xy)
    kw_, kh = KEEP[kind if kind in KEEP else "door"]
    d = dict(kind=kind, apk_xy=list(xy), px=[px, py], keepout_px=[px - kw_ // 2, py - kh, px + kw_ // 2, py])
    d.update(kw)
    return d

index = []
for mid, kit in sorted(kit_of.items(), key=lambda t: (t[1], t[0])):
    m = maps.get(mid)
    if not m:
        print("thiếu map", mid); continue
    W, H = m["size"]
    A = []
    for p in graph["ports"]:
        if p["map"] != mid: continue
        dests = []
        for (b, one, st, cm) in links_by_port.get(p["id"], []):
            q = ports.get(b)
            if q: dests.append(dict(to_map=q["map"], to_name=name(q["map"]), oneway=bool(one), status=st))
        a = anchor(p["kind"], m, p["xy"], id=p["id"], label=p["label"], origin=p["origin"],
                   needs_placement=(p.get("flag") == "cần đặt"), links=dests)
        A.append(a)
    for n in npcs:
        if n["map_id"] != mid: continue
        if n.get("apk_xy"):
            A.append(anchor("npc", m, n["apk_xy"], id=n["id"], name=n["name_vi"], tier=n["tier"], roles=n["roles"], needs_placement=False))
        else:
            A.append(dict(kind="npc", id=n["id"], name=n["name_vi"], tier=n["tier"], roles=n["roles"], apk_xy=None, px=None,
                          needs_placement=True, keepout_size_px=list(KEEP["npc"])))
    sp = spawns.get(mid)
    if sp:
        for x, y in sp.get("marker_xy", []):
            A.append(anchor("spawn", m, (x, y), id="monster_marker"))
        for x, y in sp.get("trans_enemy", []):
            A.append(anchor("trans_enemy", m, (x, y), id="monster_trigger"))
    decor = dict(small=max(10, round(W / 180)), medium=max(5, round(W / 450)), large=max(3, round(W / 800)), floor_decals=max(8, round(W / 250)))
    brief = dict(map_id=mid, name_vi=m["name"], group=m["group"], kit=kit, kit_name=kit_meta[kit]["name"],
                 style=kit_meta[kit]["style"], original_image=f"map-images/{mid}.png", size_px=[W, H],
                 bounds_apk=m["bounds"], px_per_unit=PXU, y_up_assumed=True, anchors=A, decor_budget_min=decor,
                 has_monster_zone=bool(sp and (sp.get("marker_xy") or sp.get("trans_enemy"))))
    d = OUT / kit; d.mkdir(parents=True, exist_ok=True)
    (d / f"{mid}.json").write_text(json.dumps(brief, ensure_ascii=False, indent=1))
    L = [f"# {mid} — {m['name']} ({kit_meta[kit]['name']})", "",
         f"- Ảnh gốc: `map-images/{mid}.png` {W}×{H}px (100px = 1 đơn vị APK). Phong cách kit: {kit_meta[kit]['style']}",
         f"- Ngân sách trang trí tối thiểu: {decor['small']} nhỏ, {decor['medium']} vừa, {decor['large']} lớn, {decor['floor_decals']} decal sàn", "",
         "| loại | id | tên/nhãn | px (chân) | vùng cấm đặt vật (x0,y0,x1,y1) | ghi chú |", "|---|---|---|---|---|---|"]
    for a in A:
        note = []
        if a.get("needs_placement"): note.append("CẦN ĐẶT (Gemini đề xuất)")
        for l in a.get("links", []): note.append(("→ " if not l["oneway"] else "→(1 chiều) ") + l["to_name"])
        if a.get("roles"): note.append("vai: " + "/".join(a["roles"]))
        L.append(f"| {a['kind']} | {a['id']} | {a.get('label') or a.get('name') or ''} | {a['px']} | {a.get('keepout_px') or ('~%dx%d' % tuple(a['keepout_size_px']))} | {'; '.join(note)} |")
    (d / f"{mid}.md").write_text("\n".join(L) + "\n")
    index.append(dict(map_id=mid, kit=kit, anchors=len(A), needs_placement=sum(1 for a in A if a.get("needs_placement"))))
(OUT / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1))
print("maps", len(index), "anchors", sum(i["anchors"] for i in index), "cần đặt", sum(i["needs_placement"] for i in index))
