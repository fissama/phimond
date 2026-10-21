import json,subprocess,sys
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(".ai/plan/phases/P10-pet-model/redraw-kit/polish-20261008/qa_tools").resolve()))
from pack_cohesive import gutter
root=Path("apps/game-client/assets/pets/redraws/polish-20261008/species_0068/cohesive-20261009/attempt-03")
im=Image.open(root/"raw.png").convert("RGBA");w,h=im.size
sig=im.getchannel("A").point(lambda v:255 if v>=128 else 0);pix=sig.load()
rows=[0,502,731,998,1273,h]
for boundary in rows[1:-1]:
 assert not sig.crop((0,boundary-2,w,boundary+2)).getbbox(),"nonempty row gutter"
cuts=[]
for y0,y1 in zip(rows,rows[1:]):
 xs=[sum(bool(pix[x,y]) for y in range(y0,y1)) for x in range(w)]
 cuts.append([0]+[gutter(xs,k*w/4,w/4*.18) for k in range(1,4)]+[w])
anchors=[]
for c in range(4):
 x0,x1=cuts[0][c:c+2];box=sig.crop((x0,0,x1,rows[1])).getbbox();assert box
 anchors.append(x0+(box[0]+box[2])/2)
frames=[];audit=[]
for r in range(5):
 for c in range(4):
  x0,x1=cuts[r][c:c+2];y0,y1=rows[r:r+2];box=sig.crop((x0,y0,x1,y1)).getbbox();assert box
  frames.append({"rect":[x0,y0,x1-x0,y1-y0],"pivot":[anchors[c]-x0,box[3]]})
  audit.append({"row":r+1,"column":c+1,"visible_alpha_bounds":list(box)})
(root/"layout.json").write_text(json.dumps({"destination_pivot":[140,210],"frames":frames},indent=2)+"\n")
p=root/"inputs.json";j=json.loads(p.read_text());j.update(row_boundaries=rows,column_boundaries_by_row=cuts,source_frames=audit,packing_status="layout_ready",layout_rule="Manually selected verified empty horizontal gutters because original has 264px top blank margin. Columns use actual empty gutters. Complete source cells, original alpha unchanged, one common NN scale, no per-frame fitting.");p.write_text(json.dumps(j,indent=2)+"\n")
for command,name in [
(["pack_p10_atlas.py","--source",str(root/"raw.png"),"--layout",str(root/"layout.json"),"--output",str(root/"packed.png")],"packing.json"),
(["check_p10_atlas.py",str(root/"packed.png")],"mechanical.json"),
(["preview_p10_redraw.py","--atlas",str(root/"packed.png"),"--out",str(root/"preview")],"preview-export.json")]:
 run=subprocess.run([sys.executable,"tools/assets/"+command[0],*command[1:]],capture_output=True,text=True);(root/name).write_text(run.stdout);assert run.returncode==0,run.stderr+run.stdout
bg=Image.new("RGBA",im.size,(235,230,217,255));bg.alpha_composite(im);bg.save(root/"raw-review.png")
print("PASS: complete 20 poses preserved; verified empty source gutters, common NN scale")

