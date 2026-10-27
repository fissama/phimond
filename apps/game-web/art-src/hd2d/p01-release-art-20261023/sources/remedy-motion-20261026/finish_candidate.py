from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


def run_tool(script: str, arguments: list[str], log: Path) -> int:
    command = [sys.executable, str(Path.home() / '.codex/skills/generate2dsprite/scripts' / script), *arguments]
    result = subprocess.run(command, capture_output=True, text=True)
    log.write_text(json.dumps(command) + '\n' + result.stdout + result.stderr)
    return result.returncode


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sheet', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--rows', type=int, required=True)
    parser.add_argument('--cols', type=int, required=True)
    parser.add_argument('--height', type=int, default=164)
    parser.add_argument('--facing', choices=['right', 'left', 'vertical'], default='right')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    registration = args.output / 'registration'
    status = run_tool('scale_frames.py', ['--sheet', str(args.sheet), '--rows', str(args.rows), '--cols', str(args.cols), '--count', '8', '--scale-from', 'union', '--target-body-px', str(args.height), '--resampler', 'box', '--root-lock', 'torso-x', '--lock', 'feet', '--canvas', '192,192', '--anchor-px', '96,184', '--margin', '8', '--emit-clips', '--ticks', '6', '--output-dir', str(registration)], args.output / 'registration.log')
    if status:
        raise SystemExit(status)
    palette = args.output / 'palette'
    status = run_tool('palette_tool.py', ['build', '--input', str(registration / 'frames'), '--colors', '48', '--output-dir', str(palette)], args.output / 'palette.log')
    if status:
        raise SystemExit(status)
    finished = args.output / 'finished'
    status = run_tool('palette_tool.py', ['apply', '--input', str(registration / 'frames'), '--palette', str(palette / 'palette.json'), '--output-dir', str(finished)], args.output / 'finish.log')
    if status:
        raise SystemExit(status)
    frames = sorted((finished / 'frames').glob('*.png'))
    if not frames:
        frames = sorted(path for path in finished.rglob('frame-*.png') if 'indexed' not in path.parts)
    if len(frames) != 8:
        raise ValueError(f'Expected 8 finished frames, found {len(frames)}')
    strip = Image.new('RGBA', (1536, 192))
    images = []
    for index, path in enumerate(frames):
        frame = Image.open(path).convert('RGBA')
        strip.alpha_composite(frame, (index * 192, 0))
        images.append(frame)
    strip.save(args.output / 'candidate.png')
    previews = []
    for frame in images:
        preview = Image.new('RGBA', frame.size, (35, 39, 47, 255))
        preview.alpha_composite(frame)
        previews.append(preview.convert('RGB'))
    previews[0].save(args.output / 'candidate.gif', save_all=True, append_images=previews[1:], duration=100, loop=0)
    for index, frame in enumerate(images):
        dark = Image.new('RGBA', frame.size, (35, 39, 47, 255))
        dark.alpha_composite(frame)
        checker = Image.new('RGBA', frame.size, (170, 170, 170, 255))
        pixels = checker.load()
        for row in range(192):
            for column in range(192):
                if (row // 8 + column // 8) % 2:
                    pixels[column, row] = (220, 220, 220, 255)
        checker.alpha_composite(frame)
        review = Image.new('RGBA', (384, 192))
        review.alpha_composite(dark)
        review.alpha_composite(checker, (192, 0))
        review.resize((1536, 768), Image.Resampling.NEAREST).save(args.output / f'review-{index + 1:02d}-4x.png')
    qc = args.output / 'qc'
    arguments = ['frames', '--frames', *map(str, frames), '--frames-per-row', '8', '--cycle', 'walk' if args.facing != 'vertical' else 'none', '--loop', '--output-dir', str(qc)]
    if args.facing != 'vertical':
        arguments.extend(['--facing', args.facing])
    qc_exit = run_tool('sheet_qc.py', arguments, args.output / 'qc.log')
    report = json.loads((qc / 'sheet-qc.json').read_text())
    summary = {'source_sha256': hashlib.sha256(args.sheet.read_bytes()).hexdigest(), 'candidate_sha256': hashlib.sha256((args.output / 'candidate.png').read_bytes()).hexdigest(), 'qc_exit': qc_exit, 'qa': report, 'approved': False, 'visual_review': 'pending'}
    (args.output / 'candidate-qa.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps({'output': str(args.output), 'qc_exit': qc_exit, 'status': report.get('status', report.get('qa', {}).get('status'))}))


if __name__ == '__main__':
    main()
