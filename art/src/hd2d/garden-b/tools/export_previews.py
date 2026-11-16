#!/usr/bin/env python3
"""Export non-destructive visual reviews from packed garden-b atlases."""
from pathlib import Path
from PIL import Image, ImageDraw
import argparse

ROOT=Path(__file__).resolve().parents[1]
CELL=192
ROWS=['idle','wet','water','upgrade','clear']
DURATIONS={'pot':[333,333,333,333], 'crop':[333,333,333,333]}

def checker(size,step=24):
    im=Image.new('RGBA',size,(35,38,45,255)); d=ImageDraw.Draw(im)
    for y in range(0,size[1],step):
        for x in range(0,size[0],step):
            if (x//step+y//step)%2==0: d.rectangle((x,y,min(size[0]-1,x+step-1),min(size[1]-1,y+step-1)),fill=(93,99,108,255))
    return im

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--id',required=True); ap.add_argument('--kind',choices=['pot','crop'],required=True); args=ap.parse_args()
    folder=ROOT/args.id; atlas=Image.open(folder/'final.png').convert('RGBA')
    for name,bg in [('review-4x-checker.png',checker(atlas.size)),('review-4x-dark.png',Image.new('RGBA',atlas.size,(27,30,37,255)) )]:
        bg.alpha_composite(atlas); bg.resize((atlas.width*4,atlas.height*4),Image.Resampling.NEAREST).save(folder/name)
    # Full atlas with cell divisions and target pivot marks, for placement review only.
    grid=checker(atlas.size,32); grid.alpha_composite(atlas); draw=ImageDraw.Draw(grid)
    for x in (192,384,576): draw.line((x,0,x,960),fill=(220,220,220,220),width=1)
    for y in (192,384,576,768): draw.line((0,y,768,y),fill=(220,220,220,220),width=1)
    px,py=(96,175) if args.kind=='pot' else (96,168)
    for r in range(5):
        ox=0; oy=r*192
        draw.line((ox+px-5,oy+py,ox+px+5,oy+py),fill=(0,255,255,255),width=1)
        draw.line((ox+px,oy+py-5,ox+px,oy+py+5),fill=(255,80,80,255),width=1)
        for c in range(1,4):
            ox=c*192
            draw.line((ox+px-5,oy+py,ox+px+5,oy+py),fill=(0,255,255,255),width=1)
            draw.line((ox+px,oy+py-5,ox+px,oy+py+5),fill=(255,80,80,255),width=1)
    grid.resize((atlas.width*4,atlas.height*4),Image.Resampling.NEAREST).save(folder/'review-pivot-grid.png')
    # Row strips and per-row animated GIFs.
    for r in range(5):
        frames=[atlas.crop((c*CELL,r*CELL,(c+1)*CELL,(r+1)*CELL)) for c in range(4)]
        strip=Image.new('RGBA',(CELL*4,CELL),(30,32,38,255))
        for c,fr in enumerate(frames): strip.alpha_composite(fr,(c*CELL,0))
        strip.resize((CELL*16,CELL*4),Image.Resampling.NEAREST).save(folder/f'preview-row-{r+1}.png')
        anim=[f.resize((CELL*3,CELL*3),Image.Resampling.NEAREST).convert('P',palette=Image.Palette.ADAPTIVE,colors=256) for f in frames]
        anim[0].save(folder/f'preview-row-{r+1}.gif',save_all=True,append_images=anim[1:],duration=250 if r==2 else 333,loop=0,disposal=2)
    allframes=[]; durations=[]
    for r in range(5):
        for c in range(4):
            f=atlas.crop((c*CELL,r*CELL,(c+1)*CELL,(r+1)*CELL)).resize((CELL*2,CELL*2),Image.Resampling.NEAREST)
            allframes.append(f.convert('P',palette=Image.Palette.ADAPTIVE,colors=256))
            durations.append((333 if r<2 else 250 if r==2 else 100 if r==3 else 125))
    allframes[0].save(folder/'preview-anim.gif',save_all=True,append_images=allframes[1:],duration=durations,loop=0,disposal=2)
    print('EXPORTED',args.id)

if __name__=='__main__': main()
