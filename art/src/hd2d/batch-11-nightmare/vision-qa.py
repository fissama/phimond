#!/usr/bin/env python3
"""Visual QA helper for the nightmare kit: sends an image to a VLM and prints its answer.

Read-only. Never writes game assets. Used because this harness cannot open images inline.
Usage: vision-qa.py <image> "<question>"
"""
import json
import subprocess
import sys

if len(sys.argv) < 3:
    raise SystemExit("usage: vision-qa.py <image> <question>")

image, question = sys.argv[1], sys.argv[2]
out = subprocess.run(
    ["mmx", "vision", "describe", "--image", image, "--prompt", question,
     "--output", "json", "--quiet", "--non-interactive"],
    capture_output=True, text=True, check=True,
)
print(json.loads(out.stdout)["content"])
