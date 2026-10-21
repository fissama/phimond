#!/usr/bin/env python3
"""Read-only P10 portrait/sprites PNG provenance audit; no network or repairs.

Compare every record in the committed APK manifest with blobs from the same
resolved commit, then compare those hashes with working files. The working
manifest is compared byte-for-byte but never trusted for enumeration. This
checks source integrity, not approval of art variants, PNG validity, frames.tres,
client behavior, catalog correctness, or Special recipe eligibility.

Exit: 0 intact, 1 working drift with valid source, 2 invalid/unverifiable source
or input/I/O error. JSON is written only to stdout. --repo must name a worktree
root; --source-ref defaults to HEAD and is resolved once to a commit SHA.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

ASSETS = "apps/game-client/assets/pets/apk84"
MANIFEST = ASSETS + "/manifest.json"


class AuditError(ValueError):
    pass


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise AuditError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    # Ignore inherited repository overrides; prevent promisor fetch and optional
    # writes. Object IDs must describe the selected repository's actual objects.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_NO_LAZY_FETCH="1",
               GIT_NO_REPLACE_OBJECTS="1", GIT_TERMINAL_PROMPT="0",
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_ALLOW_PROTOCOL="")
    result = subprocess.run(["git", "--no-replace-objects", "-C", str(repo), *args],
                            env=env, capture_output=True, check=False)
    if result.returncode:
        raise AuditError("Git could not verify " + args[0])
    return result.stdout


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise AuditError("duplicate manifest JSON key: " + key)
        result[key] = value
    return result


def manifest_records(data):
    manifest = json.loads(data, object_pairs_hook=unique_object)
    species = manifest.get("species") if isinstance(manifest, dict) else None
    if not isinstance(species, dict) or not species:
        raise AuditError("manifest species must be a nonempty object")
    records = []
    for name, row in species.items():
        if (not name or name in (".", "..") or any(c in name for c in "/\\")
                or any(ord(c) < 32 or ord(c) == 127 for c in name)):
            raise AuditError("unsafe manifest species ID: " + repr(name))
        if not isinstance(row, dict):
            raise AuditError("invalid manifest record: " + name)
        for kind in ("portrait", "sprites"):
            sha = row.get(kind + "_sha256")
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
                raise AuditError("invalid SHA256: " + name + "/" + kind)
            records.append({"path": ASSETS + "/" + name + "/" + kind + ".png",
                            "expected_sha256": sha})
    return sorted(records, key=lambda row: row["path"])


def working_hash(repo, path, expected):
    # Reject symlinks at every component before reading, including broken links.
    current = repo
    try:
        parts = path.split("/")
        for index, part in enumerate(parts):
            current = current / part
            mode = current.lstat().st_mode
            if stat.S_ISLNK(mode):
                return "modified", None, "symlink"
            if index < len(parts) - 1 and not stat.S_ISDIR(mode):
                return "modified", None, "non_directory_parent"
        if not stat.S_ISREG(mode):
            return "modified", None, "not_regular_file"
        actual = digest(current.read_bytes())
        return ("intact", actual, None) if actual == expected else ("modified", actual, "hash_mismatch")
    except FileNotFoundError:
        return "missing", None, "missing"


def audit(repo, source_ref, report):
    if not source_ref or source_ref.startswith("-") or any(ord(c) < 32 for c in source_ref):
        raise AuditError("invalid source ref")
    repo = repo.resolve(strict=True)
    top = Path(os.fsdecode(git(repo, "rev-parse", "--show-toplevel")).rstrip("\n")).resolve()
    if top != repo:
        raise AuditError("--repo must name the repository worktree root")
    base = git(repo, "rev-parse", "--verify", "--end-of-options", source_ref + "^{commit}").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", base):
        raise AuditError("source ref did not resolve to a commit SHA")
    report["base_sha"] = base
    tree = {}
    for entry in git(repo, "ls-tree", "-r", "-z", "--full-tree", base).split(b"\0"):
        if entry:
            metadata, path = entry.split(b"\t", 1)
            mode, kind, oid = metadata.decode("ascii").split()
            tree[os.fsdecode(path)] = (mode, kind, oid)

    def source_blob(path):
        entry = tree.get(path)
        if entry is None:
            return "missing", None
        mode, kind, oid = entry
        if mode not in ("100644", "100755") or kind != "blob":
            return "invalid_type", None
        return "valid", git(repo, "cat-file", "blob", oid)

    source_status, manifest_data = source_blob(MANIFEST)
    if source_status != "valid":
        report.update(status="source_invalid", source_status="invalid")
        report["errors"].append("committed manifest: " + source_status)
        return 2
    report["manifest"]["source_sha256"] = digest(manifest_data)
    try:
        records = manifest_records(manifest_data)
    except (ValueError, UnicodeError) as exc:
        report.update(status="source_invalid", source_status="invalid")
        report["errors"].append(str(exc))
        return 2
    report["assets"] = records
    for row in records:
        status, data = source_blob(row["path"])
        row["source_sha256"] = digest(data) if data is not None else None
        if status == "valid" and row["source_sha256"] != row["expected_sha256"]:
            status = "hash_mismatch"
        row.update(source_status=status, working_status="not_checked", working_sha256=None)
    report["counts"]["assets"] = len(records)
    report["counts"]["source_invalid"] = sum(row["source_status"] != "valid" for row in records)
    report["source_status"] = "invalid" if report["counts"]["source_invalid"] else "valid"

    # Report working observations separately even when committed source fails.
    for row in [report["manifest"], *records]:
        expected = row.get("expected_sha256", row.get("source_sha256"))
        row["working_status"], row["working_sha256"], row["working_reason"] = working_hash(repo, row["path"], expected)
    counts = Counter(row["working_status"] for row in records)
    report["counts"].update({"working_" + key: counts[key] for key in ("intact", "modified", "missing")})
    drift = counts["modified"] + counts["missing"] or report["manifest"]["working_status"] != "intact"
    report["working_status"] = "drift" if drift else "intact"
    if report["source_status"] != "valid":
        report["status"] = "source_invalid"
        return 2
    report["status"] = "working_drift" if drift else "intact"
    return 1 if drift else 0


def main(argv=None):
    report = {"status": "error", "base_sha": None, "source_ref": None,
              "source_status": "unverifiable", "working_status": "not_checked",
              "manifest": {"path": MANIFEST, "source_sha256": None,
                           "working_status": "not_checked", "working_sha256": None},
              "counts": {"assets": 0, "source_invalid": 0, "working_intact": 0,
                         "working_modified": 0, "working_missing": 0},
              "assets": [], "errors": []}
    parser = Parser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--source-ref", default="HEAD")
    try:
        args = parser.parse_args(argv)
        report["source_ref"] = args.source_ref
        code = audit(args.repo, args.source_ref, report)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        report["status"] = "error"
        report["errors"].append(str(exc))
        code = 2
    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
