"""Hermetic CLI checks: each fixture is an independent local Git repository."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CLI = Path(__file__).with_name("p10_provenance.py").resolve()
ASSETS = "apps/game-client/assets/pets/apk84"
MANIFEST = ASSETS + "/manifest.json"


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.invalid",
                        GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.invalid")
        self.git("init", "-q")
        self.manifest = {"species": {}}
        for name in ["zebra", "ant"]:
            self.add_species(name)
        self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args],
                                       env=self.env, stderr=subprocess.PIPE).decode()

    def add_species(self, name):
        row = {}
        for kind in ["portrait", "sprites"]:
            content = (name + kind).encode()
            path = self.repo / ASSETS / name / (kind + ".png")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            row[kind + "_sha256"] = hashlib.sha256(content).hexdigest()
        self.manifest["species"][name] = row

    def commit(self, write_manifest=True):
        if write_manifest:
            (self.repo / MANIFEST).write_text(json.dumps(self.manifest))
        self.git("add", "--all")
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "fixture")

    def snapshot(self):
        return {str(p.relative_to(self.repo)): (p.lstat().st_mode, p.lstat().st_mtime_ns,
                os.readlink(p) if p.is_symlink() else p.read_bytes())
                for p in self.repo.rglob("*") if p.is_file() or p.is_symlink()}

    def run_cli(self, expected, *args):
        before = self.snapshot()
        result = subprocess.run([sys.executable, "-B", str(CLI), "--repo", str(self.repo), *args],
                                env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(before, self.snapshot(), "audit wrote working or Git files")
        return json.loads(result.stdout)

    def test_clean_is_reproducible_and_resolves_commit(self):
        result = self.run_cli(0)
        self.assertEqual(result, self.run_cli(0))
        self.assertEqual(result["base_sha"], self.base)
        self.assertEqual(result["source_status"], "valid")
        self.assertEqual(result["counts"]["assets"], 4)
        self.assertEqual([x["path"] for x in result["assets"]], sorted(x["path"] for x in result["assets"]))

    def test_reports_every_modified_and_missing_asset(self):
        (self.repo / ASSETS / "ant/portrait.png").write_bytes(b"variant")
        (self.repo / ASSETS / "zebra/sprites.png").unlink()
        result = self.run_cli(1)
        self.assertEqual(result["source_status"], "valid")
        self.assertEqual(result["counts"]["working_modified"], 1)
        self.assertEqual(result["counts"]["working_missing"], 1)
        self.assertEqual(len(result["assets"]), 4)

    def test_working_manifest_cannot_hide_asset_drift(self):
        self.manifest["species"].pop("ant")
        (self.repo / MANIFEST).write_text(json.dumps(self.manifest))
        (self.repo / ASSETS / "ant/portrait.png").write_bytes(b"variant")
        result = self.run_cli(1)
        self.assertEqual(result["manifest"]["working_status"], "modified")
        self.assertEqual(result["counts"]["assets"], 4)
        self.assertEqual(result["counts"]["working_modified"], 1)

    def test_missing_working_manifest(self):
        (self.repo / MANIFEST).unlink()
        self.assertEqual(self.run_cli(1)["manifest"]["working_status"], "missing")

    def test_source_ref_pins_manifest_and_blobs_together(self):
        (self.repo / ASSETS / "ant/portrait.png").write_bytes(b"replacement")
        self.manifest["species"]["ant"]["portrait_sha256"] = hashlib.sha256(b"replacement").hexdigest()
        self.commit()
        result = self.run_cli(1, "--source-ref", self.base)
        self.assertEqual(result["base_sha"], self.base)
        self.assertEqual(result["counts"]["working_modified"], 1)
        self.run_cli(0)

    def test_source_missing_blob_is_invalid_even_if_working_copy_exists(self):
        path = ASSETS + "/ant/portrait.png"
        self.git("rm", "--cached", "--", path)
        self.git("-c", "commit.gpgsign=false", "commit", "-qm", "missing")
        result = self.run_cli(2)
        self.assertEqual(result["source_status"], "invalid")
        self.assertEqual(result["counts"]["source_invalid"], 1)

    def test_source_hash_mismatch_is_not_working_drift(self):
        self.manifest["species"]["ant"]["portrait_sha256"] = "0" * 64
        self.commit()
        result = self.run_cli(2)
        self.assertEqual(result["source_status"], "invalid")
        self.assertEqual(result["counts"]["source_invalid"], 1)

    def test_malformed_source_manifest(self):
        for content in ['{', '{"species": {}}', '{"species": [], "species": {}}',
                        '{"species": {"ant": {"portrait_sha256": "oops"}}}']:
            with self.subTest(content=content):
                (self.repo / MANIFEST).write_text(content)
                self.commit(False)
                self.assertEqual(self.run_cli(2)["source_status"], "invalid")

    def test_missing_source_manifest(self):
        (self.repo / MANIFEST).unlink()
        self.commit(False)
        self.assertEqual(self.run_cli(2)["source_status"], "invalid")

    def test_bad_or_noncommit_ref_and_arguments_are_json_errors(self):
        blob = self.git("rev-parse", "HEAD:" + MANIFEST).strip()
        for args in [("--source-ref", "no-such-ref"), ("--source-ref=" + blob,),
                     ("--source-ref=--help",), ("--source-ref=",), ("--unknown",)]:
            with self.subTest(args=args):
                self.assertEqual(self.run_cli(2, *args)["status"], "error")

    def test_safe_filename_characters_are_not_shell_commands(self):
        self.add_species("- space é $(touch INJECTED); ' quote")
        self.commit()
        result = self.run_cli(0)
        self.assertEqual(result["counts"]["assets"], 6)
        self.assertFalse((self.repo / "INJECTED").exists())

    def test_unsafe_source_ids_rejected(self):
        for name in ["..", ".", "../outside", "/absolute", "a/b", "a\\b", "a\nname"]:
            with self.subTest(name=name):
                self.manifest["species"] = {name: {"portrait_sha256": "0" * 64, "sprites_sha256": "0" * 64}}
                self.commit()
                self.assertEqual(self.run_cli(2)["source_status"], "invalid")

    def test_working_symlinks_are_drift_without_following_targets(self):
        path = self.repo / ASSETS / "ant/portrait.png"
        path.unlink()
        path.symlink_to("/nonexistent-outside-target")
        result = self.run_cli(1)
        record = next(x for x in result["assets"] if x["path"].endswith("ant/portrait.png"))
        self.assertEqual(record["working_status"], "modified")
        self.assertIsNone(record["working_sha256"])
        self.assertEqual(record["working_reason"], "symlink")

    def test_working_directory_symlink_and_nonfile_are_not_read(self):
        folder = self.repo / ASSETS / "ant"
        folder.rename(folder.with_name("moved"))
        folder.symlink_to("moved", target_is_directory=True)
        result = self.run_cli(1)
        self.assertEqual(result["counts"]["working_modified"], 2)
        self.assertTrue(all(x["working_reason"] == "symlink" for x in result["assets"]
                            if "/ant/" in x["path"]))
        folder.unlink()
        folder.mkdir()
        (folder / "portrait.png").mkdir()
        result = self.run_cli(1)
        self.assertEqual(result["counts"]["working_missing"], 1)
        self.assertEqual(result["counts"]["working_modified"], 1)

    def test_invalid_repo_is_json_error(self):
        self.assertEqual(self.run_cli(2, "--repo", str(self.repo / "absent"))["status"], "error")
        self.assertEqual(self.run_cli(2, "--repo", str(self.repo / ASSETS))["status"], "error")

    def test_committed_symlink_is_invalid_source(self):
        path = self.repo / ASSETS / "ant/portrait.png"
        path.unlink()
        path.symlink_to("sprites.png")
        self.commit()
        self.assertEqual(self.run_cli(2)["counts"]["source_invalid"], 1)


if __name__ == "__main__":
    unittest.main()
