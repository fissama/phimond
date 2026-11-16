"""QA only: composite the actual generated trunk/canopy parts; no scene assembly."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
r=Path(__file__).resolve().parent
m=json.loads((r/"manifest.json").read_text())
byid={a["id"]:a for a in m["assets"]}
board=Image.new("RGB",(1536,576),(25,31,42))
d=ImageDraw.Draw(board)
groups=[]
for index in (1,2,3):
    name=f"tree-large-0{index}"
    parts=[]
    canvas=Image.new("RGBA",(512,512))
    for suffix,above in (("trunk",0),("canopy",110)):
        rec=byid[name+"-"+suffix]
        im=Image.open(r/rec["file"]).convert("RGBA")
        px,py=rec["pivot_px"]
        x=256-round(px);y=490-above-round(py)
        canvas.alpha_composite(im,(x,y))
        parts.append({"asset_id":rec["id"],"offset_world":[0,above/128],"sway":suffix=="canopy"})
    canvas.save(r/(name+"-assembly-preview.png"))
    board.paste(canvas,((index-1)*512,0),canvas)
    d.text(((index-1)*512+16,540),name+" / trunk + canopy / 410px body",fill="white")
    groups.append({"id":name,"parts":parts,"body_height_px":410,"approved":False,
                   "notes":"QA assembly; review continuity before engine placement. Trunk is fixed; canopy rotates around attachment point."})
(r/"tree-parts.json").write_text(json.dumps(groups,indent=2)+"\n")
board.save(r/"tree-assembly-preview.png")
print("Rendered 3 assembly previews from actual generated layers.")

