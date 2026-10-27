#!/usr/bin/env python3
"""Run every MiniMax job for the nightmare kit: generate, then finish.

Usage: run_jobs.py [job-name ...]
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import jobs_minimax as J

ROOT = Path(__file__).resolve().parent
MONTAGE_DIR = ROOT / "montages"
MONTAGE_SOURCES = {
    "decals": [
        ROOT / ".." / "batch-01-octopath" / "mud-patch" / "final.png",
        ROOT / ".." / "batch-01-octopath" / "moss-patch-01" / "final.png",
        ROOT / "nightmare-floor-01" / "final.png",
        ROOT / "nightmare-prop-07" / "final.png",
    ],
    "props": [
        ROOT / "nightmare-prop-04" / "final.png",
        ROOT / ".." / "batch-01-octopath" / "stump" / "final.png",
        ROOT / "nightmare-prop-07" / "final.png",
    ],
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ensure_montage(key):
    """Build (once) the style montage for a key and return its path plus sources."""
    if key in MONTAGE_SOURCES:
        out = MONTAGE_DIR / f"{key}.png"
        if not out.exists():
            MONTAGE_DIR.mkdir(exist_ok=True)
            srcs = [str(p) for p in MONTAGE_SOURCES[key]]
            subprocess.run([sys.executable, str(ROOT / "build_style_montage.py"),
                            str(out), "512", *srcs], check=True,
                           capture_output=True, text=True)
        sources = [{"path": str(p), "sha256": sha(p)} for p in MONTAGE_SOURCES[key]]
        return out, sources
    p = ROOT / key
    return p, [{"path": str(p), "sha256": sha(p)}]


def main():
    wanted = set(sys.argv[1:])
    for job in J.JOBS:
        if wanted and job["name"] not in wanted:
            continue
        job_dir = ROOT / "jobs" / f"mm-{job['name']}"
        job_dir.mkdir(parents=True, exist_ok=True)
        (job_dir / "prompt.txt").write_text(job["prompt"], encoding="utf-8")

        montage, sources = ensure_montage(job["montage"])
        gen = subprocess.run(
            [sys.executable, str(ROOT / "gen_image.py"), str(job_dir),
             str(job_dir / "prompt.txt"), str(montage),
             str(job_dir / "raw-01.png")],
            capture_output=True, text=True)
        if gen.returncode != 0:
            print(f"[{job['name']}] GENERATION FAILED:\n{gen.stdout[-500:]}{gen.stderr[-500:]}")
            continue
        print(f"[{job['name']}] generated")

        spec = {
            "sheet": str(job_dir / "raw-01.png"),
            "refs": sources,
            "reference_montage_sources": sources,
            "assets": job["assets"],
        }
        (job_dir / "job.json").write_text(
            json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fin = subprocess.run(
            [sys.executable, str(ROOT / "finish_minimax.py"), str(job_dir),
             str(job_dir / "job.json")], capture_output=True, text=True)
        if fin.returncode != 0:
            print(f"[{job['name']}] FINISH FAILED:\n{fin.stdout[-1500:]}{fin.stderr[-1500:]}")
            continue
        print(f"[{job['name']}] {fin.stdout.strip()}")


if __name__ == "__main__":
    main()
