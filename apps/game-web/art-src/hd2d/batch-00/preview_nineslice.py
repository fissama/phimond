"""Render proposed nine-slice margins without changing any delivered asset."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

root=Path(__file__).resolve().parent
manifest=json.loads((root/"manifest.json").read_text())
board=Image.new("RGB",(1800,1150),(30,35,46))
d=ImageDraw.Draw(board)
font=ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",17)
for column,name in enumerate(("ui-panel-a","ui-panel-b")):
    rec=next(x for x in manifest["assets"] if x["id"]==name)
    im=Image.open(root/rec["file"]).convert("RGBA")
    left,top,right,bottom=rec["slice"]
    sx=[0,left,im.width-right,im.width]
    sy=[0,top,im.height-bottom,im.height]
    for row,(w,h) in enumerate(((1476,696),(1920,960),(960,960))):
        dx=[0,left,w-right,w]
        dy=[0,top,h-bottom,h]
        out=Image.new("RGBA",(w,h))
        for y in range(3):
            for x in range(3):
                piece=im.crop((sx[x],sy[y],sx[x+1],sy[y+1]))
                piece=piece.resize((dx[x+1]-dx[x],dy[y+1]-dy[y]),Image.Resampling.NEAREST)
                out.alpha_composite(piece,(dx[x],dy[y]))
        out.save(root/name/f"slice-preview-{w}x{h}.png")
        thumb=out.copy()
        thumb.thumbnail((840,290),Image.Resampling.NEAREST)
        x=column*900+20
        y=row*360+54
        d.text((x,y-28),f"{name} / {w}x{h} source px",font=font,fill="white")
        board.paste(thumb,(x,y),thumb)
board.save(root/"nineslice-preview.png")
print("Rendered 6 nine-slice previews; visual approval pending.")
