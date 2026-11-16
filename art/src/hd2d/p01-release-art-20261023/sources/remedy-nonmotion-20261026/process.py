"""Mechanical processing only: existing key/despill, uniform resize, Forge palette/QC."""
from pathlib import Path
import sys,json,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path('/Users/phileanh/rust/phimond')
S=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/p01'))
import cut_city_batch12 as c
FORGE=Path('/Users/phileanh/.codex/skills/generate2dsprite/scripts')
def run(args):
 p=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True)
 print(p.stdout,p.stderr)
 return p.returncode
def preview(im,dest):
 dest.mkdir(exist_ok=True,parents=True)
 for scale in (1,4):
  for bg in ('dark','checker'):
   v=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
   b=Image.new('RGBA',v.size,(22,27,35,255));d=ImageDraw.Draw(b)
   if bg=='checker':
    for y in range(0,b.height,16):
     for x in range(0,b.width,16):
      if (x//16+y//16)%2:d.rectangle((x,y,x+15,y+15),fill=(56,62,71,255))
   b.alpha_composite(v);b.convert('RGB').save(dest/f'{scale}x-{bg}.png')
for name,raw in [('fx-beast','fx-beast-raw-01.png'),('fx-insect','fx-insect-raw-02.png'),('fx-plant','fx-plant-raw-01.png')]:
 dest=S/name;dest.mkdir(exist_ok=True)
 rgba=c.despill(Image.fromarray(c.key(S/raw)),45)
 frames=[rgba.crop((j%3*512,j//3*512,j%3*512+512,j//3*512+512)) for j in range(6)]
 boxes=[f.getchannel('A').getbbox() for f in frames]
 maxdim=max(max(b[2]-b[0],b[3]-b[1]) for b in boxes)
 scale=168/maxdim
 strip=Image.new('RGBA',(1152,192))
 anchors=[]
 for j,(f,b) in enumerate(zip(frames,boxes)):
  # Translate each source phase only; preserve one common scale across the sheet.
  # Base of the first five grounded effects; last phase floats above same strike.
  ax=(b[0]+b[2])/2
  ay=b[3] if j<5 else b[3]+30
  anchors.append([ax,ay])
  pic=f.crop(b).resize((max(1,round((b[2]-b[0])*scale)),max(1,round((b[3]-b[1])*scale))),Image.Resampling.NEAREST)
  x=round(96+(b[0]-ax)*scale);y=round(180+(b[1]-ay)*scale)
  assert x>=8 and y>=8 and x+pic.width<=184 and y+pic.height<=184,(name,j,x,y,pic.size)
  strip.alpha_composite(pic,(192*j+x,y))
 strip.save(dest/'unquantized.png')
 if not (dest/'palette').exists():
  assert run([FORGE/'palette_tool.py','build','--input',dest/'unquantized.png','--colors',48,'--name',name+'-remedy','--output-dir',dest/'palette'])==0
 if not (dest/'finished').exists():
  assert run([FORGE/'palette_tool.py','apply','--input',dest/'unquantized.png','--palette',dest/'palette/palette.json','--output-dir',dest/'finished'])==0
 final=Image.open(dest/'finished/unquantized.png').convert('RGBA');final.save(dest/'candidate.png')
 preview(final,dest/'review')
 if not (dest/'forge-qc').exists():run([FORGE/'sheet_qc.py','spill','--input',dest/'candidate.png','--rows',1,'--cols',6,'--key','none','--safe-margin','0.04','--min-area',1,'--output-dir',dest/'forge-qc'])
 details={'raw':raw,'raw_sha256':hashlib.sha256((S/raw).read_bytes()).hexdigest(),'source_boxes':boxes,'source_anchors':anchors,'uniform_scale':scale,'processing':'Existing cut_city_batch12.key/despill; fixed 3x2 cuts; one nearest scale across all frames; translation registration only; Sprite Forge palette build/apply 48; Sprite Forge sheet_qc spill. No invented artwork.'}
 (dest/'processing.json').write_text(json.dumps(details,indent=2))
