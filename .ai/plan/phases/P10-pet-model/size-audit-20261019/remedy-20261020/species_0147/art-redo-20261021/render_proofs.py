from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
out=Path(__file__).resolve().parent
meta=json.loads((out/'profile.json').read_text());font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',14);checked=0
for cell in [96,192]:
 sc=cell/96;tw=round(145*sc);th=round(201*sc);sheet=Image.new('RGBA',(tw*12,5*(th+30)+40),'#202936');d=ImageDraw.Draw(sheet);d.text((5,4),f'0147 art redo / shared cell{cell} / prior vs candidate13 vs fairy; NOT runtime',font=font,fill='white')
 for k,p in enumerate(meta['profiles']):
  im=Image.open(out/p['file']).convert('RGBA')
  for f in range(20):
   row=f//4;col=f%4;scale=cell/281*p['factor'];side=round(281*scale);pose=im.crop((col*281,row*281,(col+1)*281,(row+1)*281)).resize((side,side),Image.Resampling.NEAREST);tile=Image.new('RGBA',(tw,th),'#202936');dd=ImageDraw.Draw(tile);gy=round(159*sc);dd.line((0,gy,tw,gy),fill='#647386');pivot=p.get('frame_pivots',[p['pivots'][i//4] for i in range(20)])[f];x=round(72*sc-pivot[0]*scale);y=round(159*sc-pivot[1]*scale);bb=pose.getchannel('A').getbbox();assert x+bb[0]>=0 and y+bb[1]>=0 and x+bb[2]<=tw and y+bb[3]<=th,(cell,k,f,bb,x,y);tile.alpha_composite(pose,(x,y));sheet.alpha_composite(tile,((k*4+col)*tw,40+row*(th+30)));checked+=1
 sheet.convert('RGB').save(out/f'20-frame-stage-{cell}.jpg',quality=98)
(out/'preview-verification.json').write_text(json.dumps({'alpha_footprints_checked':checked,'full_source_alpha_preserved':True,'per_frame_scale':False,'runtime_activated':False,'manual_contact_registration':True},indent=2));print(f'{checked} full alpha footprints fit at96/192')
