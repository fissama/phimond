"""Extract timestamped video evidence and pair it with native Godot captures."""
import html
from pathlib import Path
import shutil
import subprocess
import sys

video, captures, output = map(Path, sys.argv[1:4])
output.mkdir(parents=True, exist_ok=True)
states = [("world", 49, "00:49 — world"), ("npc", 73, "01:13 — NPC"),
          ("quests", 78, "01:18 — quest"), ("inventory", 99, "01:39 — inventory"),
          ("companions", 114, "01:54 — pet attributes"), ("battle", 193, "03:13 — battle")]
sections = []
for name, seconds, title in states:
    reference = output / f"reference-{name}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(seconds), "-i", str(video),
                    "-frames:v", "1", str(reference)], check=True)
    shutil.copy2(captures / f"{name}.png", output / f"current-{name}.png")
    sections.append(f'<section><h2>{html.escape(title)}</h2><div class="pair">'
                    f'<figure><img src="{reference.name}"><figcaption>Original video, full frame</figcaption></figure>'
                    f'<figure><img src="current-{name}.png"><figcaption>Phimond native client, fixture state</figcaption></figure>'
                    '</div></section>')
for name in ("login", "ranch"):
    shutil.copy2(captures / f"{name}.png", output / f"current-{name}.png")
    sections.append(f'<section><h2>{name.title()} — adapted, no matching video screen</h2>'
                    f'<img class="adapted" src="current-{name}.png"></section>')
(output / "index.html").write_text('''<!doctype html><meta charset="utf-8"><title>Phimond visual comparison</title>
<style>body{background:#101b29;color:#f1ead4;font:16px system-ui;margin:28px}h1{font-size:25px}h2{font-size:19px;margin-top:32px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}figure{margin:0}img{width:100%;display:block}figcaption{padding:8px;color:#addce7}.adapted{max-width:900px}p{max-width:1000px}</style>
<h1>Phimond — source / implementation</h1><p>Primary reference: Pokezoo, 4:33. Video frames are unaltered, including their external player surround. Compare the active game area. Captures are deterministic UI fixtures, not live server screenshots. Original version differences and missing mapped assets remain; this report does not assert pixel equivalence.</p>
''' + ''.join(sections), encoding="utf-8")
print(output / "index.html")
