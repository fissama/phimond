"""Focused corruption tests for the authoring-catalog safety gate (stdlib only)."""
import copy
import importlib.util
from pathlib import Path
import unittest
import tempfile
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("p10_catalog", Path(__file__).with_name("p10_catalog.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CatalogTests(unittest.TestCase):
    def test_duplicate_json_key_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text('{"id": "first", "id": "second"}')
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                module.read(path)

    def mutate(self, path, change):
        original_read = module.read
        document = copy.deepcopy(original_read(path))
        change(document)
        def read(current):
            return document if current == path else original_read(current)
        return patch.object(module, "read", side_effect=read)

    def test_baseline_and_disabled_rules(self):
        output = module.build()
        self.assertEqual(152, len(output["species.json"]["records"]))
        recipes = output["special_recipes.json"]["records"]
        self.assertEqual(17, len(recipes))
        self.assertTrue(all(not r["enabled"] and r["material_quantity"] is None for r in recipes.values()))
        self.assertTrue(all(not r["enabled"] for r in output["items.json"]["records"].values()))

    def test_duplicate_id_rejected(self):
        def change(d):
            keys = list(d["species"])
            d["species"][keys[1]] = d["species"][keys[0]]
        with self.mutate(module.OUT / "id_registry.json", change), self.assertRaisesRegex(ValueError, "duplicate"):
            module.build()

    def test_missing_mapping_rejected(self):
        with self.mutate(module.OUT / "id_registry.json", lambda d: d["species"].pop("NhenVongLinh")), self.assertRaisesRegex(ValueError, "coverage"):
            module.build()

    def test_localized_id_rejected(self):
        with self.mutate(module.OUT / "id_registry.json", lambda d: d["species"].update(NhenVongLinh="Nhện Vong Linh")), self.assertRaisesRegex(ValueError, "invalid"):
            module.build()

    def test_changed_star_rejected(self):
        with self.mutate(module.SOURCE, lambda d: d["species"]["NhenVongLinh"].update(star=2)), self.assertRaisesRegex(ValueError, "Race x Star"):
            module.build()

    def test_missing_asset_rejected(self):
        def change(d):
            d["species"]["NhenVongLinh"]["assets"]["portrait"] = "res://assets/pets/apk84/missing/portrait.png"
        with self.mutate(module.SOURCE, change), self.assertRaisesRegex(ValueError, "missing"):
            module.build()

    def test_wrong_parent_star_rejected(self):
        def change(d):
            row = next(r for r in d["species"].values() if r["special_recipe"])
            row["special_recipe"]["parent_main"] = "NhenVongLinh"
        with self.mutate(module.SOURCE, change), self.assertRaisesRegex(ValueError, "invalid source parent"):
            module.build()

    def test_source_hash_rejected(self):
        with self.mutate(module.OUT / "id_registry.json", lambda d: d.update(source_sha256="bad")), self.assertRaisesRegex(ValueError, "hash"):
            module.build()


if __name__ == "__main__":
    unittest.main()
