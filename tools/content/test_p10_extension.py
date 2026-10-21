"""Extension acceptance and fail-closed corruption checks (stdlib only)."""
import copy
import unittest

import p10_extension as extension
from p10_catalog import read


class ExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = read(extension.OUT / "id_registry.json")
        cls.baseline = read(extension.OUT / "species.json")
        cls.candidate = read(extension.CANDIDATE)

    def build(self, registry=None, candidate=None):
        return extension.build(registry or self.registry, self.baseline, candidate or self.candidate)

    def test_effective_count_and_frozen_records(self):
        registry, authored, effective, mapping = self.build()
        self.assertEqual(160, len(effective["records"]))
        self.assertEqual(152, len(self.baseline["records"]))
        for key, record in self.baseline["records"].items():
            self.assertEqual(record, effective["records"][key])
        self.assertEqual(self.registry["species"], registry["species"])
        self.assertEqual(8, len(authored["records"]))
        self.assertEqual(extension.MAPPING, mapping["proposal_to_stable"])

    def test_six_normal_two_special_all_five_star(self):
        records = list(self.build()[1]["records"].values())
        self.assertEqual(6, sum(row["species_class"] == "normal" for row in records))
        self.assertEqual(2, sum(row["species_class"] == "special" for row in records))
        self.assertTrue(all(row["star"] == 5 for row in records))
        self.assertEqual(["hybrid", "support"], records[-2]["role_ids"])
        self.assertEqual(["hybrid", "disruptor"], records[-1]["role_ids"])

    def test_collision_against_existing_namespace_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["unrelated_reserved"] = {"reservation": "species_0153"}
        with self.assertRaisesRegex(ValueError, "collision"):
            self.build(registry=registry)

    def test_conflicting_authored_mapping_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["authored_species"] = {"P13-NEW-01": "species_0160"}
        with self.assertRaisesRegex(ValueError, "conflicting"):
            self.build(registry=registry)

    def test_duplicate_original_id_rejected(self):
        registry = copy.deepcopy(self.registry)
        registry["species"]["ChienSiDauLau"] = "species_0001"
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.build(registry=registry)

    def test_numeric_candidate_preserved_without_promotion(self):
        authored = self.build()[1]["records"]
        for proposal, stable in extension.MAPPING.items():
            record = authored[stable]
            expected = copy.deepcopy(self.candidate["records"][proposal])
            expected["id"] = stable
            expected["registry_status"] = "P10_stable_id_registered"
            self.assertEqual(expected, record["design_candidate"]["record"])
            self.assertNotIn("base_stats", record)
            self.assertNotIn("growth_baseline", record)
            self.assertNotIn("mp_profile", record)

    def test_authored_provenance_and_art_gates(self):
        authored = self.build()[1]["records"]
        for stable, record in authored.items():
            self.assertEqual("phimond_authored", record["provenance"]["namespace"])
            self.assertFalse(record["provenance"]["source_recovered"])
            self.assertNotIn("source", record)
            self.assertNotIn("assets", record)
            self.assertNotIn("source_sha256", record["provenance"])
            self.assertFalse(record["art"]["approved"])
            self.assertFalse(record["art"]["runtime_activated"])
            self.assertEqual(stable, record["art"]["species_id"])
            self.assertNotIn("candidate_path", record["art"])
            self.assertTrue(record["art"]["manifest_path"].endswith("art-manifest.json"))

    def test_fake_apk_provenance_rejected(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["records"]["P13-NEW-01"]["source_identity"]["namespace"] = "apk84"
        with self.assertRaisesRegex(ValueError, "provenance"):
            self.build(candidate=candidate)

    def test_wrong_star_rejected(self):
        candidate = copy.deepcopy(self.candidate)
        candidate["records"]["P13-SPECIAL-01"]["star"] = 6
        with self.assertRaisesRegex(ValueError, "star"):
            self.build(candidate=candidate)

    def test_no_runtime_or_recipes_promoted(self):
        _, authored, effective, mapping = self.build()
        self.assertEqual("authoring_only_not_runtime", authored["status"])
        self.assertFalse(effective["runtime_activated"])
        self.assertFalse(mapping["runtime_activated"])
        self.assertNotIn("recipes", effective)
        self.assertTrue(all(not item["enabled"] for item in
                            read(extension.OUT / "special_recipes.json")["records"].values()))


if __name__ == "__main__":
    unittest.main()
