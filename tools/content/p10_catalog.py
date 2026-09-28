#!/usr/bin/env python3
"""Build/check the P10 authoring catalog. Never modifies legacy runtime content.

Source IDs and asset paths stay in the evidence layer. id_registry.json is a
frozen allocation table, not generated from display names on every run.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/p10"
SOURCE = ROOT / "data/pets/roster_apk84.json"
ITEM_SOURCE = ROOT / ".ai/plan/phases/P10-pet-model/evidence/apk84-selected-items.json"
HASH = "b8e02a75e49d5d02703a0b05ec52b450cdfaf69d544f04df2f4a2a465199a18e"
MATRIX = {
    "insect": [7, 4, 3, 2, 4], "spirit": [5, 2, 3, 3, 4],
    "bird": [7, 4, 3, 3, 4], "demon": [6, 4, 3, 3, 2],
    "beast": [7, 4, 3, 4, 4], "plant": [7, 4, 3, 2, 4],
    "undead": [7, 4, 3, 2, 4], "dragon": [4, 4, 3, 2, 1],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key: {key} in {path}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def display(value):
    return unicodedata.normalize("NFC", value).strip()


def build():
    raw, item_raw = read(SOURCE), read(ITEM_SOURCE)
    registry = read(OUT / "id_registry.json")
    require(all(v["source_sha256"] == HASH for v in [raw, item_raw, registry]), "source hash mismatch")
    require(registry["schema_version"] == 1, "unsupported registry version")
    source_species = raw["species"]
    source_items = {r["id"]: r for r in item_raw["records"]}
    special = {k for k, v in source_species.items() if v["species_class"] == "special"}
    require(set(registry["species"]) == set(source_species), "species mapping coverage")
    require(set(registry["items"]) == set(source_items), "item mapping coverage")
    require(set(registry["special_recipes"]) == special, "recipe mapping coverage")
    ids = [v for domain in ["species", "items", "special_recipes"] for v in registry[domain].values()]
    require(len(ids) == len(set(ids)), "duplicate canonical ID")
    patterns = {"species": r"species_[0-9]{4,}", "items": r"item_[a-z0-9]+(?:_[a-z0-9]+)*",
                "special_recipes": r"recipe_special_[0-9]{4,}"}
    for domain, pattern in patterns.items():
        require(all(re.fullmatch(pattern, v) for v in registry[domain].values()), f"invalid {domain} ID")
    require(len(source_species) == 152 and len(special) == 17, "baseline counts")
    require(len(source_items) == 8, "selected item reference count")
    actual = Counter((v["race"], v["star"]) for v in source_species.values())
    require(actual == Counter({(race, star): count for race, counts in MATRIX.items()
                               for star, count in enumerate(counts, 1)}), "Race x Star changed")
    species, recipes, items = {}, {}, {}
    manifest = read(ROOT / "apps/game-client/assets/pets/apk84/manifest.json")
    for source_id, row in source_species.items():
        canonical = registry["species"][source_id]
        require(row["id"] == source_id, "source key/id mismatch")
        require(source_id in manifest["species"], "missing source actor")
        for path in row["assets"].values():
            require(path.startswith("res://assets/pets/apk84/"), "unexpected asset root")
            require((ROOT / "apps/game-client" / path.removeprefix("res://")).is_file(), f"missing {path}")
        folder = ROOT / "apps/game-client/assets/pets/apk84" / source_id
        for file, field in [("portrait.png", "portrait_sha256"), ("sprites.png", "sprites_sha256")]:
            require(hashlib.sha256((folder / file).read_bytes()).hexdigest() ==
                    manifest["species"][source_id][field], f"asset hash changed: {source_id}/{file}")
        species[canonical] = {
            "id": canonical, "display_name": {"vi": display(row["name"])},
            "description": {"vi": display(row["description_original"])},
            "description_status": "source_reference_not_gameplay_rules",
            "race_id": row["race"], "star": row["star"], "species_class": row["species_class"],
            "assets": row["assets"],
            "source": {"namespace": "apk84", "species_id": source_id, **row["source"]},
        }
        recipe = row["special_recipe"]
        if recipe:
            main, secondary = recipe["parent_main"], recipe["parent_secondary"]
            require(main != secondary, "duplicate recipe parent")
            for parent in [main, secondary]:
                require(parent in source_species, "missing parent")
                require(source_species[parent]["star"] == row["star"] and
                        source_species[parent]["species_class"] == "normal", "invalid source parent")
            require(source_species[main]["race"] == row["race"], "source main race mismatch")
            recipe_id = registry["special_recipes"][source_id]
            recipes[recipe_id] = {
                "id": recipe_id, "kind": "special_fusion", "enabled": False,
                "target_species_id": canonical,
                "main_species_id": registry["species"][main],
                "secondary_species_id": registry["species"][secondary],
                "material_item_id": registry["items"][recipe["material_source_id"]],
                "material_quantity": None,
                "blocked_by": ["P10-O01"],
                "unverified_rules": recipe["unverified_server_rules"],
                "source": {"namespace": "apk84", "target_species_id": source_id},
            }
    for source_id, row in source_items.items():
        canonical = registry["items"][source_id]
        adopted_material = source_id in {"KetHopTT4S", "KetHopTT5S"}
        items[canonical] = {
            "id": canonical, "display_name": {"vi": display(row["name"])},
            "description": {"vi": display(row["description"])},
            "adoption_status": "accepted_material_identity" if adopted_material else "source_reference_only",
            "enabled": False,
            "source": {"namespace": "apk84", "item_id": source_id,
                       "item_group_id": row["item_id"], "asset_file": item_raw["asset_file"],
                       "catalog_path_id": item_raw["path_id"]},
        }
    def package(records, missing):
        return {"schema_version": 1, "status": "authoring_only_not_runtime",
                "source_sha256": HASH, "unresolved_fields": missing, "records": records}
    return {
        "species.json": package(species, ["element_id", "base_stats", "growth_baseline",
                                         "role_ids", "native_skill_ids", "acquisition"]),
        "items.json": package(items, ["item_kind", "effect", "cost", "stack_limit", "binding", "assets"]),
        "special_recipes.json": package(recipes, ["plus_result", "cost", "success_chance",
                                                "minimum_level", "inheritance", "parent_order"]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate authoring catalogs; default is check only")
    args = parser.parse_args()
    expected = build()
    for name, value in expected.items():
        path = OUT / name
        if args.write:
            path.write_text(encoded(value), encoding="utf-8")
        else:
            require(path.is_file() and path.read_text(encoding="utf-8") == encoded(value),
                    f"stale/missing {path}; review sources then run --write")
    print("PASS: P10 IDs unique; 152 species, 8 item references, 17 disabled Special recipes; "
          "source mappings, Race x Star, references, asset paths/hashes and generated files verified")


if __name__ == "__main__":
    main()
