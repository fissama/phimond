"""Packing tests use temporary images only; production candidates are untouched."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

CLI = Path(__file__).with_name("pack_p10_atlas.py")


class PackingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source.png"
        self.layout_path = self.root / "layout.json"
        self.output = self.root / "packed.png"
        self.image = Image.new("RGBA", (201, 10))
        self.layout = {"destination_pivot": [140, 200], "frames": []}
        for i in range(20):
            self.image.paste((i + 1, 40, 80, 255), (i * 10 + 2, 2, i * 10 + 8, 8))
            self.image.putpixel((i * 10 + 2, 2), (i + 1, 40, 80, 1))
            self.layout["frames"].append({"rect": [i * 10, 0, 10, 10], "pivot": [5, 8]})

    def run_pack(self, code=0):
        self.image.save(self.source)
        self.layout_path.write_text(json.dumps(self.layout))
        before = self.source.read_bytes(), self.source.stat().st_mtime_ns
        old_output = self.output.read_bytes() if self.output.exists() else None
        result = subprocess.run([sys.executable, "-B", str(CLI), "--source", str(self.source),
                                 "--layout", str(self.layout_path), "--output", str(self.output)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(before, (self.source.read_bytes(), self.source.stat().st_mtime_ns))
        if code:
            self.assertEqual(old_output, self.output.read_bytes() if self.output.exists() else None)
        return json.loads(result.stdout)

    def test_common_scale_pivot_exact_geometry_and_faint_alpha(self):
        report = self.run_pack()
        self.assertEqual(report["status"], "packed")
        self.assertAlmostEqual(report["scale"], 178 / 6)
        self.assertEqual(report["destination_pivot"], [140, 200])
        with Image.open(self.output) as packed:
            self.assertEqual(packed.mode, "RGBA")
            self.assertEqual(packed.size, (1124, 1405))
            bounds = []
            for i in range(20):
                x, y = i % 4 * 281, i // 4 * 281
                alpha = packed.crop((x, y, x + 281, y + 281)).getchannel("A")
                bounds.append(alpha.getbbox())
                self.assertGreater(alpha.histogram()[1], 0)
                left, top, right, bottom = bounds[-1]
                self.assertGreaterEqual(min(left, top), 22)
                self.assertLessEqual(max(right, bottom), 259)
            self.assertEqual(len(set(bounds)), 1)
            self.assertEqual(bounds[0][1], 22)
        self.assertEqual(len(report["frames"]), 20)

    def test_repeatable_and_refuses_overwrite(self):
        first = self.run_pack()
        content = self.output.read_bytes()
        self.run_pack(2)
        self.output = self.root / "second.png"
        second = self.run_pack()
        self.assertEqual(content, self.output.read_bytes())
        self.assertEqual(first["output_sha256"], second["output_sha256"])

    def test_source_cannot_be_output(self):
        self.output = self.source
        self.run_pack(2)

    def test_invalid_rectangles_pivots_and_frame_count(self):
        for rect in [[-1, 0, 10, 10], [0, 0, 0, 10], [195, 0, 10, 10],
                     [0.5, 0, 10, 10], [True, 0, 10, 10]]:
            self.layout["frames"][0]["rect"] = rect
            self.run_pack(2)
        self.layout["frames"][0]["rect"] = [0, 0, 10, 10]
        for pivot in [[-1, 5], [11, 5], [float("nan"), 5], [True, 5]]:
            self.layout["frames"][0]["pivot"] = pivot
            self.run_pack(2)
        self.layout["frames"].pop()
        self.run_pack(2)

    def test_overlapping_rectangles_rejected(self):
        self.layout["frames"][1]["rect"] = [9, 0, 10, 10]
        self.run_pack(2)

    def test_uncovered_alpha_one_pixel_rejected(self):
        self.image.putpixel((200, 5), (10, 20, 30, 1))
        self.run_pack(2)

    def test_empty_frame_rejected(self):
        self.image.paste((0, 0, 0, 0), (0, 0, 10, 10))
        self.run_pack(2)

    def test_invalid_destination_pivot_and_mode(self):
        for pivot in [[21, 140], [259, 140], [140, float("inf")]]:
            self.layout["destination_pivot"] = pivot
            self.run_pack(2)
        self.layout["destination_pivot"] = [140, 200]
        self.image = self.image.convert("RGB")
        self.run_pack(2)

    def test_different_pose_sizes_share_one_scale(self):
        self.image.paste((0, 0, 0, 0), (0, 0, 10, 10))
        self.image.paste((100, 40, 80, 255), (4, 4, 6, 6))
        report = self.run_pack()
        self.assertAlmostEqual(report["scale"], 178 / 6)
        small, large = report["frames"][0]["output_alpha_bounds"], report["frames"][1]["output_alpha_bounds"]
        self.assertLess(small[2] - small[0], (large[2] - large[0]) / 2)

    def test_downscale_contains_complete_bounds_and_alpha_one_edges(self):
        self.image = Image.new("RGBA", (6000, 300))
        self.layout = {"destination_pivot": [140, 237], "frames": []}
        for i in range(20):
            self.image.paste((i + 1, 40, 80, 1), (i * 300 + 30, 30, i * 300 + 270, 270))
            self.layout["frames"].append({"rect": [i * 300, 0, 300, 300], "pivot": [150, 270]})
        report = self.run_pack()
        self.assertAlmostEqual(report["scale"], 215 / 240)
        for frame in report["frames"]:
            self.assertEqual(frame["output_alpha_bounds"][1:4:2], [22, 237])
        with Image.open(self.output) as packed:
            self.assertGreater(packed.getchannel("A").histogram()[1], 0)

    def test_different_rect_sizes_and_pivot_offsets_stay_aligned(self):
        self.image = Image.new("RGBA", (210, 10))
        self.layout["frames"] = []
        for i in range(20):
            x = 0 if i == 0 else i * 10 + 10
            offset = 10 if i == 0 else 0
            self.image.paste((i + 1, 40, 80, 255), (x + offset + 2, 2, x + offset + 8, 8))
            self.layout["frames"].append({"rect": [x, 0, 20 if i == 0 else 10, 10], "pivot": [5 + offset, 8]})
        report = self.run_pack()
        self.assertEqual(len({tuple(f["output_alpha_bounds"]) for f in report["frames"]}), 1)

    def test_duplicate_art_is_packed_but_independent_checker_rejects(self):
        first = self.image.crop((0, 0, 10, 10))
        self.image.paste(first, (10, 0))
        self.run_pack()
        result = subprocess.run([sys.executable, "-B", str(CLI.with_name("check_p10_atlas.py")), str(self.output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["atlases"][0]["distinct_cells"], 19)


if __name__ == "__main__":
    unittest.main()
