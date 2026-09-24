"""Extract UI scene-graph references from Unity APKs.

Walks each GameObject in `data.unity3d`, recording:
  - its name, PathID, components
  - which Texture2D / Sprite / Font are referenced by Image / RawImage / Text components
  - any UI keywords (Panel, Button, Chat, ...) for later filtered lookups

Outputs:
  extended/scene_graph.json     ← master index
  extended/scene_graph/<bundle>_<id>.json per GameObject (only for UI-tagged ones)

Usage:
    python tools/assets/scan_ui_references.py <apk_or_xapk> <output_dir>
"""
from __future__ import annotations

import collections
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import UnityPy

UI_KEYWORDS = re.compile(
    r"(Panel|Button|Btn|Chat|Hud|Menu|Avatar|Portrait|Tab|Dialog|Popup|Title|"
    r"Header|Footer|Slot|Grid|Frame|Rank|Gem|Coin|Skill|Item|Inventory|Shop|"
    r"Guild|Farm|Poke|Pet|Monster|Npc|Magic|Attack|Defend|Setting|Option|"
    r"Reward|Confirm|Cancel|Back|Slider|Bar|Label|Background|HP|MP|XP|SliderHP|"
    r"HpBar|MpBar|XpBar|Notif|IAP|RewardIAP|ChatPanel)",
    re.IGNORECASE,
)


def short(s, n=120):
    return (s or "")[:n]


def safe(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_.]+", "_", name or "")
    return (s[:80] or "unnamed").strip("_")


def main():
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    raw = src.read_bytes()

    references = []  # flat list: {src, go_id, go_name, comp_id, comp_name, asset_kind, asset_id, asset_name}
    scene_nodes = []
    errors = []
    apk_bundles = []

    with zipfile.ZipFile(io.BytesIO(raw)) as outer:
        apk_data = ([outer.read(n) for n in outer.namelist() if n.endswith(".apk")] if src.suffix == ".xapk" else [raw])
        for apk in apk_data:
            with zipfile.ZipFile(io.BytesIO(apk)) as archive:
                for bundle in archive.namelist():
                    if not bundle.endswith("data.unity3d"):
                        continue
                    bundle_name = Path(bundle).stem
                    apk_bundles.append(bundle_name)
                    env = UnityPy.load(archive.read(bundle))

                    # First pass: build Texture2D / Sprite / Font name+id index
                    tex_index = {}
                    spr_index = {}
                    font_index = {}
                    for obj in env.objects:
                        kind = obj.type.name
                        if kind not in ("Texture2D", "Sprite", "Font"):
                            continue
                        try:
                            data = obj.read()
                            n = getattr(data, "m_Name", "") or ""
                        except Exception:
                            continue
                        if kind == "Texture2D":
                            tex_index[obj.path_id] = n
                        elif kind == "Sprite":
                            spr_index[obj.path_id] = n
                        else:
                            font_index[obj.path_id] = n

                    # Second pass: walk GameObjects
                    for obj in env.objects:
                        if obj.type.name != "GameObject":
                            continue
                        try:
                            go = obj.read()
                            go_name = getattr(go, "m_Name", "") or ""
                        except Exception as exc:
                            errors.append({"bundle": bundle_name, "id": obj.path_id, "err": str(exc)})
                            continue

                        if not go_name:
                            continue

                        is_ui = bool(UI_KEYWORDS.search(go_name))
                        if not is_ui:
                            continue

                        node = {
                            "bundle": bundle_name,
                            "id": obj.path_id,
                            "name": go_name,
                            "components": [],
                        }
                        for comp in getattr(go, "m_Components", []) or []:
                            try:
                                c = comp.read()
                            except Exception:
                                continue
                            cname = c.__class__.__name__
                            comp_info = {"type": cname, "fields": {}}
                            # Common UI bindings:
                            for attr in ("m_Sprite", "m_Texture", "m_Material", "m_FontData", "m_Font", "m_SourceImage"):
                                if hasattr(c, attr):
                                    ref = getattr(c, attr)
                                    if ref is None:
                                        continue
                                    rid = getattr(ref, "m_PathID", None) if hasattr(ref, "m_PathID") else None
                                    if rid is not None:
                                        comp_info["fields"][attr] = rid
                                        # resolve to name
                                        if rid in spr_index:
                                            references.append({
                                                "bundle": bundle_name,
                                                "go_id": obj.path_id,
                                                "go_name": go_name,
                                                "asset_kind": "Sprite",
                                                "asset_id": rid,
                                                "asset_name": spr_index[rid],
                                            })
                                        elif rid in tex_index:
                                            references.append({
                                                "bundle": bundle_name,
                                                "go_id": obj.path_id,
                                                "go_name": go_name,
                                                "asset_kind": "Texture2D",
                                                "asset_id": rid,
                                                "asset_name": tex_index[rid],
                                            })
                                        elif rid in font_index:
                                            references.append({
                                                "bundle": bundle_name,
                                                "go_id": obj.path_id,
                                                "go_name": go_name,
                                                "asset_kind": "Font",
                                                "asset_id": rid,
                                                "asset_name": font_index[rid],
                                            })
                            node["components"].append(comp_info)
                        scene_nodes.append(node)

    summary = {
        "source": src.name,
        "bundles": apk_bundles,
        "ui_gameobject_count": len(scene_nodes),
        "ui_reference_count": len(references),
        "error_count": len(errors),
        "errors_sample": errors[:20],
    }
    (out / "scene_graph.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    (out / "scene_graph_references.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in references)
    )
    # Per-GameObject dump
    (out / "scene_graph_nodes.jsonl").write_text(
        "\n".join(json.dumps(n, ensure_ascii=False) for n in scene_nodes)
    )
    print(json.dumps({k: v for k, v in summary.items() if k != "errors_sample"}, indent=2))


if __name__ == "__main__":
    main()
