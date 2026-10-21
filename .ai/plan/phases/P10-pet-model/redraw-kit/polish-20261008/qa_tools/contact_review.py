"""Render untouched packed poses on light/dark at literal 64/96px cell sizes."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

parser=argparse.ArgumentParser()
parser.add_argument('candidate',type=Path)
args=parser.parse_args()
atlas=Image.open(args.candidate/'packed.png').convert('RGBA')
panel=Image.new('RGB',(896,1000),(40,43,50))
draw=ImageDraw.Draw(panel)
for r in range(5):
    for theme,color in enumerate([(94,100,114),(240,234,211)]):
        for c in range(4):
            cell=atlas.crop((c*281,r*281,(c+1)*281,(r+1)*281))
            for size,oy in [(96,0),(64,116)]:
                x=(theme*4+c)*112;y=r*200+oy
                tile=Image.new('RGBA',(112,116 if size==96 else 84),color+(255,))
                tile.alpha_composite(cell.resize((size,size),Image.Resampling.NEAREST),((112-size)//2,16))
                panel.paste(tile.convert('RGB'),(x,y))
                draw.text((x+3,y+2),f'R{r+1} C{c+1} {size}',fill=(255,255,255) if theme==0 else (25,25,25))
panel.save(args.candidate/'contact-64-96.png')
print(args.candidate/'contact-64-96.png')
