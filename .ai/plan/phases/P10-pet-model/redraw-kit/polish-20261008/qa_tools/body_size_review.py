"""Whole-cell nearest-neighbor trial at tier body sizes, preserving one factor."""
import argparse, json, math
from pathlib import Path
from PIL import Image, ImageDraw

p=argparse.ArgumentParser();p.add_argument('candidate',type=Path);p.add_argument('--height',type=int,default=74);a=p.parse_args()
atlas=Image.open(a.candidate/'packed.png').convert('RGBA')
cells=[atlas.crop((c*281,r*281,(c+1)*281,(r+1)*281)) for r in range(5) for c in range(4)]
bounds=[im.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox() for im in cells]
factor=min(a.height/(bounds[0][3]-bounds[0][1]),108/max(b[2]-b[0] for b in bounds))
side=math.ceil(281*factor);tilew=side+24;tileh=side+36
out=Image.new('RGB',(tilew*8,tileh*5));d=ImageDraw.Draw(out)
for i,im in enumerate(cells):
    for theme,color in enumerate([(94,100,114),(240,234,211)]):
        tile=Image.new('RGBA',(tilew,tileh),color+(255,));tile.alpha_composite(im.resize((side,side),Image.Resampling.NEAREST),(12,24))
        x=(theme*4+i%4)*tilew;y=(i//4)*tileh;out.paste(tile.convert('RGB'),(x,y));d.text((x+4,y+4),f'R{i//4+1}C{i%4+1} body {a.height}',fill=(255,255,255) if theme==0 else (20,20,20))
out.save(a.candidate/'body-size-review.png')
(a.candidate/'body-size-trial.json').write_text(json.dumps({'nominal_idle_body_height':a.height,'max_pose_width':108,'display_factor':factor,'whole_cell_side':side,'purpose':'art readability trial only, not runtime configuration or battle layout clearance'},indent=2)+'\n')
print(a.candidate/'body-size-review.png')
