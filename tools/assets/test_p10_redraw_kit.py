"""Dispatch safety and preview export regression checks; no model calls."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image, ImageDraw
import p10_redraw_jobs as jobs
from preview_p10_redraw import export


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((jobs.KIT / 'manifest.json').read_text())

    def test_exact_coverage_and_actual_input_hashes(self):
        self.assertEqual(jobs.validate(self.manifest), [])
        rendered = [jobs.render(self.manifest, b) for b in range(1, 31)]
        for prompt in rendered:
            self.assertEqual(prompt.count('"output_dir":'), 5)

    def test_duplicate_species_rejected(self):
        changed = copy.deepcopy(self.manifest)
        changed['jobs'][1] = changed['jobs'][0]
        self.assertTrue(jobs.validate(changed))

    def test_hash_drift_rejected(self):
        changed = copy.deepcopy(self.manifest)
        changed['jobs'][0]['source_atlas_sha256'] = '0' * 64
        self.assertTrue(any('changed input' in e for e in jobs.validate(changed)))

    def test_scope_escape_rejected(self):
        changed = copy.deepcopy(self.manifest)
        changed['jobs'][0]['output_dir'] = '../../outside'
        self.assertTrue(any('scope mismatch' in e for e in jobs.validate(changed)))


class PreviewTests(unittest.TestCase):
    def fixture(self, path):
        image = Image.new('RGBA', (1124, 1405))
        draw = ImageDraw.Draw(image)
        for i in range(20):
            x, y = i % 4 * 281, i // 4 * 281
            draw.rectangle((x+80, y+60, x+180, y+220), fill=(40+i*8, 150, 90, 255))
        image.save(path)

    def test_export_preserves_hash_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / 'source.png', root / 'preview'
            self.fixture(source)
            report = export(source, output)
            self.assertFalse(report['human_approved'])
            self.assertEqual(source.read_bytes(), (output / 'sprites.png').read_bytes())
            self.assertIn(hashlib.sha256(source.read_bytes()).hexdigest(),
                          (output / 'preview.html').read_text())
            with Image.open(output / 'portrait-preview.png') as portrait:
                self.assertEqual(portrait.size, (281, 281))
            with self.assertRaises(FileExistsError):
                export(source, output)

    def test_invalid_art_creates_no_preview(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / 'source.png', root / 'preview'
            Image.new('RGBA', (1124, 1405)).save(source)
            with self.assertRaises(ValueError):
                export(source, output)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
