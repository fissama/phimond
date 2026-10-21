"""Mechanical atlas contract tests; generated fixtures never enter game assets."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

CLI = Path(__file__).with_name("check_p10_atlas.py")


class AtlasTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "fixture.png"
        self.image = Image.new("RGBA", (1124, 1405))
        for i in range(20):
            x, y = (i % 4) * 281, (i // 4) * 281
            self.image.putpixel((x + 22, y + 22), (i + 1, 50, 100, 255))
            self.image.putpixel((x + 258, y + 258), (100, 80, 60, 1))

    def run_check(self, expected, fmt="PNG"):
        self.image.save(self.path, format=fmt)
        before = (self.path.read_bytes(), self.path.stat().st_mtime_ns)
        result = subprocess.run([sys.executable, "-B", str(CLI), str(self.path)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(before, (self.path.read_bytes(), self.path.stat().st_mtime_ns))
        return json.loads(result.stdout)["atlases"][0]

    def test_exact_safe_boundaries_and_observations(self):
        report = self.run_check(0)
        self.assertEqual(report["occupied_cells"], 20)
        self.assertEqual(report["distinct_cells"], 20)
        self.assertEqual(report["cells"][0]["alpha_bounds"], [22, 22, 259, 259])
        self.assertEqual(report["cells"][0]["height_pixels"], 237)
        self.assertEqual(report["cells"][0]["scale_observation"], "above_typical")
        self.assertTrue(report["visual_review_required"])

    def test_faint_alpha_outside_safe_box_fails_on_all_four_edges(self):
        for pos in [(21, 80), (259, 80), (80, 21), (80, 259)]:
            with self.subTest(pos=pos):
                self.image.putpixel(pos, (40, 30, 20, 1))
                report = self.run_check(1)
                self.assertIn("outside_safe_area", report["cells"][0]["issues"])
                self.image.putpixel(pos, (0, 0, 0, 0))

    def test_empty_cell_is_failure(self):
        self.image.paste((0, 0, 0, 0), (0, 0, 281, 281))
        report = self.run_check(1)
        self.assertEqual(report["occupied_cells"], 19)
        self.assertIn("empty", report["cells"][0]["issues"])

    def test_duplicate_cells_fail_despite_invisible_rgb_noise(self):
        self.image.paste(self.image.crop((0, 0, 281, 281)), (281, 0))
        self.image.putpixel((281, 0), (255, 0, 80, 0))
        report = self.run_check(1)
        self.assertEqual(report["distinct_cells"], 19)
        self.assertEqual(report["cells"][1]["duplicate_of"], 0)

    def test_wrong_dimensions_fail(self):
        self.image = Image.new("RGBA", (20, 25))
        self.assertIn("dimensions", self.run_check(1)["issues"])

    def test_rgb_and_palette_png_are_not_rgba(self):
        for mode in ["RGB", "P"]:
            self.image = self.image.convert(mode)
            self.assertIn("mode", self.run_check(1)["issues"])

    def test_non_png_format_rejected(self):
        self.assertIn("format", self.run_check(1, "TIFF")["issues"])

    def test_small_silhouette_is_guidance_not_rejection(self):
        self.image = Image.new("RGBA", (1124, 1405))
        for i in range(20):
            self.image.putpixel(((i % 4) * 281 + 100, (i // 4) * 281 + 100), (i, 50, 100, 255))
        self.assertEqual(self.run_check(0)["cells"][0]["scale_observation"], "below_typical")

    def test_missing_and_invalid_inputs_are_json_errors(self):
        for args in [[], [str(self.path)], ["--unknown"]]:
            result = subprocess.run([sys.executable, "-B", str(CLI), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["status"], "error")
        self.path.write_bytes(b"not an image")
        result = subprocess.run([sys.executable, "-B", str(CLI), str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "error")


if __name__ == "__main__":
    unittest.main()
