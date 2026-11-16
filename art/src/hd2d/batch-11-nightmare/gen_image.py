#!/usr/bin/env python3
"""Generate one image sheet through the MiniMax route (image-01) and record provenance.

The prompt must stay under the provider limit; this script fails fast instead of
sending an invalid request. The style montage attached as subject reference is the
only image reference the provider accepts, so the job file must list the approved
originals that were composited into it.

Usage: gen_image.py <job-dir> <prompt-file> <montage.png> <out.png> [--model M]
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PROMPT_LIMIT = 1500


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    job_dir = Path(sys.argv[1])
    prompt_file = Path(sys.argv[2])
    montage = Path(sys.argv[3])
    out = Path(sys.argv[4])
    model = "image-01"
    if "--model" in sys.argv:
        model = sys.argv[sys.argv.index("--model") + 1]

    prompt = prompt_file.read_text(encoding="utf-8").strip()
    if len(prompt) >= PROMPT_LIMIT:
        raise SystemExit(
            f"prompt too long: {len(prompt)} chars, provider limit is <{PROMPT_LIMIT}"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        out.unlink()

    cmd = [
        "mmx", "image", "generate",
        "--model", model,
        "--prompt", prompt,
        "--out", str(out),
        "--quiet", "--non-interactive",
    ]
    if montage and Path(montage).exists():
        cmd += ["--subject-ref", f"type=character,image={montage}"]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 or not out.exists():
        raise SystemExit(f"mmx failed ({proc.returncode}): {proc.stdout[-800:]}{proc.stderr[-800:]}")

    record = {
        "route": "MiniMax image-01 (owner-authorised 2026-10-26; Codex image_gen quota exhausted)",
        "model": model,
        "prompt_file": str(prompt_file),
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "prompt_chars": len(prompt),
        "subject_ref": str(montage) if montage and Path(montage).exists() else None,
        "subject_ref_sha256": sha(montage) if montage and Path(montage).exists() else None,
        "artifact": str(out),
        "artifact_sha256": sha(out),
        "prompt": prompt,
    }
    (job_dir / "generation.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in record.items() if k != "prompt"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
