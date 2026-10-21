#!/usr/bin/env python3
"""Export an isolated HTML animation/contact preview after mechanical validation.

Never activates runtime art. Output directory must not exist. Timing is a
review preset, not a combat or original-APK timing contract.
"""
import argparse
import base64
import json
from pathlib import Path
import shutil

from check_p10_atlas import check

HTML = r'''<!doctype html><meta charset="utf-8">
<title>P10 candidate review</title>
<style>
body{font:16px system-ui;background:#242932;color:#eee;margin:24px}
button,select{font:inherit;margin:6px;padding:8px}canvas{image-rendering:pixelated}
.stage{background:#667084;display:inline-block;padding:20px;margin:10px;vertical-align:top}
.light .stage{background:#f3ecd9}.dark .stage{background:#171923}
#cells{display:grid;grid-template-columns:repeat(4,max-content);gap:8px}
.cell{background:#667084;padding:8px}.light .cell{background:#f3ecd9;color:#222}
.dark .cell{background:#171923}code{overflow-wrap:anywhere}h2{font-size:18px}
</style>
<h1>P10 — candidate preview</h1>
<p>Mechanical PASS only. Identity/style/animation require visual review and human approval.</p>
<p>Candidate SHA256: <code>__HASH__</code></p>
<p>Review timing presets; these do not define gameplay timings. All sizes below are cell sizes.</p>
<select id="row"><option>1 Idle — loop</option><option>2 Move — loop</option>
<option>3 Basic attack — one shot</option><option>4 Cast — one shot</option>
<option>5 Hurt/down — one shot</option></select>
<button id="replay">Replay</button><button id="pause">Pause / resume</button>
<button onclick="document.body.className='light'">Light</button>
<button onclick="document.body.className='dark'">Dark</button>
<div id="stages"></div><p id="state"></p><h2>20 frames — row / column</h2><div id="cells"></div>
<script>
const img=new Image(), stages=[], timings=[[200,200,200,200],[120,120,120,120],
 [120,100,80,180],[180,180,120,220],[120,180,220,350]];
let row=0,frame=0,elapsed=0,last=0,paused=false;
function draw(canvas,r,c){let ctx=canvas.getContext('2d');ctx.imageSmoothingEnabled=false;
 ctx.clearRect(0,0,canvas.width,canvas.height);
 ctx.drawImage(img,c*281,r*281,281,281,0,0,canvas.width,canvas.height)}
function reset(){row=document.getElementById('row').selectedIndex;frame=0;elapsed=0;paused=false}
document.getElementById('row').onchange=reset;
document.getElementById('replay').onclick=reset;
document.getElementById('pause').onclick=()=>{paused=!paused};
img.onload=()=>{
 for(let size of [64,96,192]){let box=document.createElement('div');box.className='stage';
 let label=document.createElement('p');label.textContent=size+' px';box.append(label);
 let canvas=document.createElement('canvas');canvas.width=canvas.height=size;box.append(canvas);
 document.getElementById('stages').append(box);stages.push(canvas)}
 for(let r=0;r<5;r++)for(let c=0;c<4;c++){
 let box=document.createElement('div');box.className='cell';let label=document.createElement('p');
 label.textContent='R'+(r+1)+' C'+(c+1);box.append(label);
 let canvas=document.createElement('canvas');canvas.width=canvas.height=192;box.append(canvas);
 document.getElementById('cells').append(box);draw(canvas,r,c)}
 requestAnimationFrame(tick)};
function tick(now){const dt=last?Math.min(now-last,100):0;last=now;
 if(!paused){elapsed+=dt;while(elapsed>=timings[row][frame]){
 elapsed-=timings[row][frame];if(frame<3)frame++;else if(row<2)frame=0;else{elapsed=0;break}}}
 for(let canvas of stages)draw(canvas,row,frame);
 document.getElementById('state').textContent='Row '+(row+1)+' / frame '+(frame+1)+
 (row>=2&&frame===3?' — final frame held':'');requestAnimationFrame(tick)}
img.src='data:image/png;base64,__IMAGE__';
</script>'''


def export(atlas, output):
    from PIL import Image
    report = check(atlas)
    if report['status'] != 'pass':
        raise ValueError('Mechanical atlas validation failed; run check_p10_atlas.py for findings')
    # mkdir is deliberately exclusive: never replace somebody else's review.
    output.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(atlas, output / 'sprites.png')
    with Image.open(atlas) as image:
        image.crop((0, 0, 281, 281)).save(output / 'portrait-preview.png')
    html = HTML.replace('__HASH__', report['sha256']).replace(
        '__IMAGE__', base64.b64encode(atlas.read_bytes()).decode('ascii'))
    (output / 'preview.html').write_text(html)
    (output / 'mechanical.json').write_text(json.dumps(report, indent=2) + '\n')
    (output / 'README.txt').write_text(
        'Review only. sprites.png is a byte-identical candidate copy.\n'
        'portrait-preview.png is idle frame 1 cropped to 281x281; not an approved UI icon.\n'
        'No runtime SpriteFrames or catalog was changed. Open preview.html in a browser.\n'
        'Animation timings are review presets. Human acceptance remains pending.\n')
    return {'status': 'preview_exported', 'candidate_sha256': report['sha256'],
            'preview': str(output / 'preview.html'), 'human_approved': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atlas', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(export(args.atlas, args.out), indent=2))
    except (OSError, ValueError, ImportError) as exc:
        parser.exit(1, f'{exc}\n')


if __name__ == '__main__':
    main()
