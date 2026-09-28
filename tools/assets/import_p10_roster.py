"""Import the approved APK 8.4 roster and original art without running the APK.

Usage: tools/.cache/asset-venv/bin/python tools/assets/import_p10_roster.py XAPK ROOT
Requires the existing UnityPy/Pillow asset environment. The identity catalog
does not replace runtime species.json; stats/elements/save migration are pending.
"""
import collections
import hashlib
import io
import json
import math
from pathlib import Path
import re
import struct
import sys
import zipfile

import UnityPy
from PIL import Image

source = Path(sys.argv[1])
root = Path(sys.argv[2]).resolve()
output = root / ".ai/plan/phases/P10-pet-model/evidence"
output.mkdir(parents=True, exist_ok=True)
raw = source.read_bytes()
source_sha256 = hashlib.sha256(raw).hexdigest()
assert source_sha256 == "b8e02a75e49d5d02703a0b05ec52b450cdfaf69d544f04df2f4a2a465199a18e", "Review a different APK before importing"
outer = zipfile.ZipFile(io.BytesIO(raw))
apk = zipfile.ZipFile(io.BytesIO(outer.read("com.HCGame.SpiritBeastWorld.apk")))
metadata = apk.read("assets/bin/Data/Managed/Metadata/global-metadata.dat")
magic, version = struct.unpack_from("<II", metadata)
assert magic == 0xFAB11BAF and version == 31
string_offset, string_size = struct.unpack_from("<II", metadata, 24)
type_offset, type_size = struct.unpack_from("<II", metadata, 160)
field_offset, _ = struct.unpack_from("<II", metadata, 96)
default_offset, default_size = struct.unpack_from("<II", metadata, 64)
value_offset, _ = struct.unpack_from("<II", metadata, 72)


def string_at(index):
    assert 0 <= index < string_size
    start = string_offset + index
    return metadata[start:metadata.index(b"\0", start)].decode("utf8")


defaults = {
    struct.unpack_from("<3i", metadata, offset)[0]:
    struct.unpack_from("<3i", metadata, offset)[1:]
    for offset in range(default_offset, default_offset + default_size, 12)
}
types = {}
assert type_size % 88 == 0
for offset in range(type_offset, type_offset + type_size, 88):
    definition = struct.unpack_from("<16I8H2I", metadata, offset)
    name = string_at(definition[0])
    if name in ("PokeModelData", "HePokes", "SaoPoke", "PokeInfo", "InfoPokePanel"):
        fields = []
        for index in range(definition[8], definition[8] + definition[18]):
            field = struct.unpack_from("<3I", metadata, field_offset + index * 12)
            entry = {"name": string_at(field[0]), "index": index}
            if index in defaults:
                value = metadata[value_offset + defaults[index][1]]
                # v31 compressed signed integer: these enum values fit one byte.
                assert value < 128 and value % 2 == 0
                entry["default"] = value >> 1
            fields.append(entry)
        types[name] = fields

assert [f["name"] for f in types["PokeModelData"]] == [
    "Stt", "ID", "Avata", "NamePoke", "Chinh", "Phu", "He", "Sao", "GioiThieu"
]
race_translation = {
    "BatTu": "undead", "ThucVat": "plant", "Rong": "dragon", "AcMa": "demon",
    "DaThu": "beast", "Chim": "bird", "Sau": "insect", "LinhThe": "spirit",
}
star_translation = {
    "S1": (1, "normal"), "S2": (2, "normal"), "S3": (3, "normal"),
    "S4": (4, "normal"), "TT4S": (4, "special"),
    "S5": (5, "normal"), "TT5S": (5, "special"),
}
races = {f["default"]: race_translation[f["name"]] for f in types["HePokes"]
         if f["name"] in race_translation}
stars = {f["default"]: star_translation[f["name"]] for f in types["SaoPoke"]
         if f["name"] in star_translation}
env = UnityPy.load(apk.read("assets/bin/Data/data.unity3d"))
objects = {(obj.assets_file.name, obj.path_id): obj for obj in env.objects}
candidates = []
for obj in env.objects:
    if obj.type.name == "MonoBehaviour":
        data = obj.read(check_read=False)
        if data.m_Script.read().m_ClassName == "DataPoke":
            candidates.append(obj)
assert len(candidates) == 1
obj = candidates[0]
blob = obj.get_raw_data()
position = 28  # serialized MonoBehaviour header before m_Name


def integer():
    global position
    value = struct.unpack_from("<i", blob, position)[0]
    position += 4
    return value


def text():
    global position
    size = integer()
    assert 0 <= size <= len(blob) - position
    value = blob[position:position + size].decode("utf8")
    position = (position + size + 3) // 4 * 4
    return value


def pointer():
    global position
    file_id, path_id = struct.unpack_from("<iq", blob, position)
    position += 12
    return {"file_id": file_id, "path_id": path_id}


asset_name = text()
count = integer()
rows = []
for _ in range(count):
    start = position
    row = {
        "record_offset": start, "stt": integer(), "id": text(), "avatar": pointer(),
        "name": text(), "parent_main": text(), "parent_secondary": text(),
        "race_enum": integer(), "star_enum": integer(), "description": text(),
    }
    row["race"] = races[row["race_enum"]]
    row["star"], row["species_class"] = stars[row["star_enum"]]
    assert row["avatar"]["file_id"] == 0
    portrait = objects[(obj.assets_file.name, row["avatar"]["path_id"])]
    assert portrait.type.name == "Sprite"
    row["avatar"]["name"] = portrait.read().m_Name
    rows.append(row)
assert position == len(blob)
assert len({row["id"] for row in rows}) == count
by_id = {row["id"]: row for row in rows}
for row in rows:
    if row["species_class"] == "special":
        parents = [by_id[row["parent_main"]], by_id[row["parent_secondary"]]]
        assert all(parent["star"] == row["star"] for parent in parents)
        assert parents[0]["race"] == row["race"]

report = {
    "source": source.name, "sha256": source_sha256,
    "metadata_version": version, "field_schema": types,
    "asset_file": obj.assets_file.name, "path_id": obj.path_id, "asset_name": asset_name,
    "record_count": count, "bytes_consumed": position, "byte_length": len(blob), "rows": rows,
    "limits": ["Embedded client catalog; does not prove every species is obtainable online.",
               "Parent fields do not recover server validation or numeric formulas."],
}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def pointer_source(ptr):
    target = ptr.deref()
    return {"file": target.assets_file.name, "path_id": target.path_id}


def key(value):
    return re.sub(r"[^a-z0-9]", "", value.lower())


actors = {}
for candidate in env.objects:
    if candidate.type.name == "Animator" and candidate.assets_file.name == "resources.assets":
        animator = candidate.read()
        name = animator.m_GameObject.read().m_Name
        if name not in ("Boy", "Girl", "GAUHE"):
            assert key(name) not in actors
            actors[key(name)] = (candidate, animator, name)

# Source prefab has a one-character spelling difference. Explicit, reviewable
# alias; never approximate-match arbitrary species to another actor.
aliases = {"QuaiVatNhamThach": "QUAIVATNHAMTHAC"}
pack_relative = Path("apps/game-client/assets/pets/apk84")
pack = root / pack_relative
manifest = {"source_sha256": source_sha256, "species": {}}
catalog = {
    "schema_version": 1,
    "status": "accepted_identity_and_asset_baseline",
    "source_sha256": source_sha256,
    "runtime_status": "not_loaded_by_legacy_species_catalog",
    "unresolved_fields": ["element", "base_stats", "growth", "native_skills", "acquisition", "numeric_fusion_rules"],
    "species": {},
}
frame_total = 0
clip_total = 0
image_cache = {}


def sprite_image(ptr):
    source_key = tuple(pointer_source(ptr).values())
    if source_key not in image_cache:
        image_cache[source_key] = ptr.read().image.convert("RGBA")
    return image_cache[source_key]


def clip_schedule(clip):
    """Decode the one discrete SpriteRenderer curve present in these clips."""
    binding = clip.m_ClipBindingConstant.genericBindings
    native = clip.m_MuscleClip.m_Clip.data
    stream = native.m_StreamedClip
    assert len(binding) == 1 and binding[0].isPPtrCurve == 1 and binding[0].typeID == 212
    assert stream.curveCount == 0 and stream.discreteCurveCount == 1
    assert native.m_DenseClip.m_CurveCount == 0 and not native.m_ConstantClip.data
    payload = struct.pack("<" + "I" * len(stream.data), *stream.data)
    offset = 0
    keys = []
    refs = clip.m_ClipBindingConstant.pptrCurveMapping
    start, stop = clip.m_MuscleClip.m_StartTime, clip.m_MuscleClip.m_StopTime
    assert start == 0 and stop > start
    while offset < len(payload):
        time, size = struct.unpack_from("<fi", payload, offset)
        offset += 8
        assert 0 <= size <= 1
        for _ in range(size):
            index, a, b, c, value = struct.unpack_from("<i4f", payload, offset)
            offset += 20
            assert index == 0 and (a, b, c) == (0, 0, 0)
            assert value == int(value) and 0 <= value < len(refs)
            if time < stop:
                keys.append((max(start, time), int(value)))
    assert offset == len(payload) and keys and keys[0][0] == start
    frames = []
    for i, (time, ref_index) in enumerate(keys):
        end = keys[i + 1][0] if i + 1 < len(keys) else stop
        assert end >= time
        if end > time:
            frames.append((refs[ref_index], end - time))
    assert math.isclose(sum(d for _, d in frames), stop - start, abs_tol=1e-6)
    return frames


for row in rows:
    species_id = row["id"]
    actor_obj, actor, actor_name = actors[key(aliases.get(species_id, species_id))]
    folder = pack / species_id
    folder.mkdir(parents=True, exist_ok=True)
    avatar = objects[(obj.assets_file.name, row["avatar"]["path_id"])].read().image.convert("RGBA")
    avatar.save(folder / "portrait.png")
    clips = {}
    unique_frames = {}
    for ptr in actor.m_Controller.read().m_AnimationClips:
        clip = ptr.read()
        schedule = clip_schedule(clip)
        entry = {"source": pointer_source(ptr), "loop": clip.m_MuscleClip.m_LoopTime,
                 "duration_seconds": clip.m_MuscleClip.m_StopTime,
                 "timing": "decoded_discrete_sprite_curve", "frames": []}
        for sprite_ptr, duration in schedule:
            identity = tuple(pointer_source(sprite_ptr).values())
            if identity not in unique_frames:
                sprite = sprite_ptr.read()
                unique_frames[identity] = {
                    "index": len(unique_frames), "image": sprite_image(sprite_ptr),
                    "source": pointer_source(sprite_ptr),
                    "pivot": [sprite.m_Pivot.x, sprite.m_Pivot.y],
                    "pixels_per_unit": sprite.m_PixelsToUnits,
                }
            entry["frames"].append({"index": unique_frames[identity]["index"], "duration_seconds": duration})
            frame_total += 1
        clips[clip.m_Name.lower()] = entry
        clip_total += 1
    assert set(clips) == {"idle", "run", "die", "attack", "magic"}
    frames = list(unique_frames.values())
    # Align sprites at the original Unity pivot (Godot AnimatedSprite2D is centered).
    left = max(math.ceil(f["image"].width * f["pivot"][0]) for f in frames)
    right = max(math.ceil(f["image"].width * (1 - f["pivot"][0])) for f in frames)
    top = max(math.ceil(f["image"].height * (1 - f["pivot"][1])) for f in frames)
    bottom = max(math.ceil(f["image"].height * f["pivot"][1]) for f in frames)
    cell_w, cell_h = 2 * max(left, right), 2 * max(top, bottom)
    columns = min(8, len(frames))
    sheet = Image.new("RGBA", (columns * cell_w, math.ceil(len(frames) / columns) * cell_h))
    public_frames = []
    for frame in frames:
        i = frame["index"]
        x, y = (i % columns) * cell_w, (i // columns) * cell_h
        im = frame["image"]
        draw_x = x + round(cell_w / 2 - im.width * frame["pivot"][0])
        draw_y = y + round(cell_h / 2 - im.height * (1 - frame["pivot"][1]))
        sheet.paste(im, (draw_x, draw_y))
        # Packing must preserve every source pixel, including alpha.
        assert sheet.crop((draw_x, draw_y, draw_x + im.width, draw_y + im.height)).tobytes() == im.tobytes()
        public_frames.append({k: v for k, v in frame.items() if k != "image"} |
                             {"region": [x, y, cell_w, cell_h], "source_image_size": list(im.size),
                              "draw_offset": [draw_x - x, draw_y - y]})
    sheet.save(folder / "sprites.png")
    res_folder = f"res://assets/pets/apk84/{species_id}"
    resource = [f'[gd_resource type="SpriteFrames" load_steps={len(frames) + 2} format=3]',
                f'[ext_resource type="Texture2D" path="{res_folder}/sprites.png" id="1"]']
    for frame in public_frames:
        resource += [f'[sub_resource type="AtlasTexture" id="F{frame["index"]}"]',
                     'atlas = ExtResource("1")',
                     'region = Rect2(%s)' % ', '.join(map(str, frame['region']))]
    animations = []
    for name, clip in clips.items():
        # speed=1 means each Godot frame duration is the decoded duration in seconds.
        values = ['{"duration": %.9f, "texture": SubResource("F%d")}' %
                  (f["duration_seconds"], f["index"]) for f in clip["frames"]]
        animations.append('{"name": &"%s", "speed": 1.0, "loop": %s, "frames": [%s]}' %
                          (name, str(clip["loop"]).lower(), ', '.join(values)))
    resource += ['[resource]', 'animations = [' + ',\n'.join(animations) + ']']
    (folder / "frames.tres").write_text('\n\n'.join(resource) + '\n')
    manifest["species"][species_id] = {
        "actor_name": actor_name, "actor_source": {"file": actor_obj.assets_file.name, "path_id": actor_obj.path_id},
        "actor_mapping": "explicit_source_spelling_alias" if species_id in aliases else "unique_case_insensitive_source_id",
        "portrait_source": {"file": obj.assets_file.name, "path_id": row["avatar"]["path_id"]},
        "portrait_sha256": hashlib.sha256((folder / "portrait.png").read_bytes()).hexdigest(),
        "sprites_sha256": hashlib.sha256((folder / "sprites.png").read_bytes()).hexdigest(),
        "frames": public_frames, "clips": clips,
    }
    recipe = None
    if row["species_class"] == "special":
        recipe = {"kind": "special_same_star", "parent_main": row["parent_main"],
                  "parent_secondary": row["parent_secondary"], "target_star": row["star"],
                  "material_source_id": f"KetHopTT{row['star']}S",
                  "unverified_server_rules": ["parent_order_interchangeable", "minimum_level", "plus_result", "cost", "success_chance", "inheritance_formula"]}
    catalog["species"][species_id] = {
        "id": species_id, "name": row["name"], "race": row["race"], "star": row["star"],
        "species_class": row["species_class"], "description_original": row["description"],
        "special_recipe": recipe,
        "assets": {"portrait": res_folder + "/portrait.png", "sprite_frames": res_folder + "/frames.tres"},
        "source": {"catalog_path_id": obj.path_id, "record_offset": row["record_offset"],
                   "race_enum": row["race_enum"], "star_enum": row["star_enum"]},
    }

assert len(catalog["species"]) == 152 and clip_total == 760
write_json(output / "apk84-roster-extraction.json", report)
write_json(root / "data/pets/roster_apk84.json", catalog)
write_json(pack / "manifest.json", manifest)
summary = {"records": count, "classes": collections.Counter(r["species_class"] for r in rows),
           "stars": collections.Counter(r["star"] for r in rows), "all_bytes_consumed": position == len(blob),
           "portraits": count, "actor_mappings": count, "animations": clip_total, "frame_keyframes": frame_total,
           "source_sha256": source_sha256}
write_json(output / "apk84-import-summary.json", summary)
print(json.dumps(summary, ensure_ascii=False))
