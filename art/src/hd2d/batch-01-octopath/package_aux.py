"""Export generated terrain, registered FX frames and parallax parts. No procedural artwork."""
from pathlib import Path
import json,sys,subprocess,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
F=Path("/Users/phileanh/.codex/skills")
PY=sys.executable
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+"\n")
def run(args):
    p=subprocess.run([PY,*map(str,args)],capture_output=True,text=True)
    if p.stdout:print(p.stdout.strip(),flush=True)
    if p.stderr:print(p.stderr.strip(),file=sys.stderr)
    return p.returncode
def finish(inputs,palette,output):
    if not output.exists():
        return run([F/"generate2dsprite/scripts/palette_tool.py","apply","--input",inputs,
                    "--palette",palette/"palette.json","--output-dir",output])
    return 0
def own_palette(inputs,dest):
    if not dest.exists():
        run([F/"generate2dsprite/scripts/palette_tool.py","build","--input",inputs,
             "--colors",48,"--balance","--output-dir",dest])
    return dest
records=[]
def seam_crop(im,axes,asset_id):
    """Measured source crop only: no painting, blending, wrapping or mirrored pixels."""
    w,h=im.size;a=np.asarray(im.convert("RGBA")).astype(float)/255
    rgb=a[:,:,:3]*a[:,:,3:4];layers=(rgb,rgb+1-a[:,:,3:4])
    def score(l,r,t,b):
        xx=max(float(np.abs(z[t:h-b or None,l]-z[t:h-b or None,w-1-r]).mean()*255) for z in layers)
        yy=max(float(np.abs(z[t,l:w-r or None]-z[h-1-b,l:w-r or None]).mean()*255) for z in layers) if axes=="xy" else 0
        return max(xx,yy)
    if score(0,0,0,0)<6:return im,None
    limit=16 if w<=512 else 128;step=1 if w<=512 else 2
    pairs=[(score(l,r,0,0),l+r,l,r) for l in range(0,limit+1,step) for r in range(0,limit+1,step)]
    if axes=="x":
        passing=[v for v in pairs if v[0]<6];best=min(passing,key=lambda v:(v[1],v[0])) if passing else min(pairs)
        l,r=best[2:];t=b=0
    else:
        # Keep40 likely X and40 likely Y phases, then evaluate BOTH axes after the combined crop.
        xp=sorted(pairs)[:40]
        yp=sorted((max(float(np.abs(z[t]-z[h-1-b]).mean()*255) for z in layers),t+b,t,b) for t in range(17) for b in range(17))[:40]
        choices=[(score(l,r,t,b),l+r+t+b,l,r,t,b) for _,_,l,r in xp for _,_,t,b in yp]
        passing=[v for v in choices if v[0]<6];best=min(passing,key=lambda v:(v[1],v[0])) if passing else min(choices)
        l,r,t,b=best[2:]
    if l or r or t or b:return im.crop((l,t,w-r,h-b)).resize((w,h),Image.Resampling.NEAREST),[l,t,w-r,h-b]
    return im,None
def record(job,spec,im,raw,frames=1,fps=None,tileable="none",extra=None):
    dest=R/spec["id"];dest.mkdir(exist_ok=True)
    crop_box=None
    if tileable!="none":
        original=im
        im,crop_box=seam_crop(im,tileable,spec["id"])
        if crop_box:original.save(dest/"before-seam-crop.png")
    im.convert("RGBA").save(dest/"final.png")
    for attempt in raw.parent.glob("raw-*.png"):
        if not (dest/attempt.name).exists():(dest/attempt.name).write_bytes(attempt.read_bytes())
    refs=[{"path":p,"sha256":sha(p)} for p in job["refs"]]
    (dest/"prompt.md").write_text(job["prompt"]+"\n\nOrdered reference images:\n"+
        "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs)+
        "\n\nRoute: built-in image_gen; model not exposed. Raw SHA256: "+sha(raw)+"\n")
    density=spec.get("density",128);fw=im.width//frames
    rec={"id":spec["id"],"category":spec["category"],"kit":"forest","file":spec["id"]+"/final.png",
         "px":list(im.size),"frame_px":[fw,im.height],"world":[fw/density,im.height/density],
         "pivot":"center","pivot_px":[fw/2,im.height/2],"pivot_uv":[.5,.5],"tileable":tileable,
         "slice":None,"frames":frames,"fps":fps,"sway":False,"source_refs":job["refs"],"replaces":None,
         "art_source":"host_image","route":"built-in image_gen","source_job":job["id"],
         "source_raw":raw.name,"raw_sha256":sha(raw),"sha256":sha(dest/"final.png"),
         "approved":False,"status":"needs_owner_review","notes":"Octopath-directed generated art. Engine integration pending."}
    qa={"failures":[],"warnings":[],"frame_margins":[]}
    for n in range(frames):
        part=im.crop((n*fw,0,(n+1)*fw,im.height)).convert("RGBA")
        a=np.asarray(part)
        box=part.getchannel("A").getbbox()
        if box is None:qa["failures"].append("empty_frame");continue
        margins=[box[0],box[1],fw-box[2],im.height-box[3]]
        qa["frame_margins"].append(margins)
        if spec["category"] in ("fx","light") and min(margins)<8:qa["failures"].append("frame_margin_8")
    a=np.asarray(im.convert("RGBA"))
    if tileable!="none":
        rgba=a.astype(float)/255
        # Check visible seam over both dark and light; transparent pixels cannot hide RGB spikes.
        black=rgba[:,:,:3]*rgba[:,:,3:4]
        white=black+(1-rgba[:,:,3:4])
        sx=max(float(np.abs(b[:,0]-b[:,-1]).mean()*255) for b in (black,white))
        sy=max(float(np.abs(b[0]-b[-1]).mean()*255) for b in (black,white))
        qa["seam_mean_255"]={"x":round(sx,4),"y":round(sy,4),"threshold":6}
        if sx>=6 or (tileable=="xy" and sy>=6):
            qa["failures"].append("seam_mean_below_6")
            rec["intended_tileable"]=tileable;rec["tileable"]="none"
        repeats=Image.new("RGBA",(im.width*3,im.height*(3 if tileable=="xy" else 1)))
        for y in range(3 if tileable=="xy" else 1):
            for x in range(3):repeats.alpha_composite(im,(x*im.width,y*im.height))
        repeats.save(dest/("repeat-3x3.png" if tileable=="xy" else "repeat-3x1.png"))
    if frames>1:
        views=[]
        for n in range(frames):
            part=im.crop((n*fw,0,(n+1)*fw,im.height))
            part=part.resize((fw*3,im.height*3),Image.Resampling.NEAREST)
            bg=Image.new("RGB",part.size,(28,34,45));bg.paste(part,(0,0),part)
            views.append(bg)
        views[0].save(dest/"preview.gif",save_all=True,append_images=views[1:],
                      duration=round(1000/fps),loop=0,optimize=False)
        qa["warnings"].append("Frame timing suggested; loop aesthetics require visual review.")
        rec["notes"]+=" world and pivot refer to ONE frame, not the full sheet."
    if extra:rec.update(extra)
    if crop_box:
        rec["seam_crop"]=crop_box
        rec["notes"]+=" Border correction uses only a measured smaller crop and nearest resize; no repaint or blending."
    rec["mechanical_status"]="blocked" if qa["failures"] else "pass"
    if qa["failures"]:rec["status"]="blocked"
    write(dest/"qa.json",qa)
    (dest/"review.md").write_text("# Source identification\n\n"+job["source_card"]+
        "\n\nMechanical status: "+rec["mechanical_status"]+"\nFailures: "+str(qa["failures"])+
        "\nWarnings: "+str(qa["warnings"])+
        "\n\nOwner approval and in-engine review pending. Raw artwork unchanged; only extraction, sizing, palette/alpha finishing.\n")
    records.append(rec)

# Terrain: actual atlas sizes are measured, never assumed from the prompt.
folder=R/"terrain"
if (folder/"raw-01.png").exists():
    job=json.loads((folder/"job.json").read_text())
    raw=folder/job.get("selected_raw","raw-01.png")
    atlas=Image.open(raw).convert("RGBA")
    inp=folder/"inputs";inp.mkdir(exist_ok=True)
    for index,name in enumerate(job["assets"]):
        row,col=divmod(index,2)
        box=(round(col*atlas.width/2),round(row*atlas.height/4),
             round((col+1)*atlas.width/2),round((row+1)*atlas.height/4))
        im=atlas.crop(box).resize((512,512),Image.Resampling.NEAREST)
        im.save(inp/(name+".png"))
    finish(inp,R/"palette",folder/"finished")
    for index,name in enumerate(job["assets"]):
        im=Image.open(folder/"finished"/(name+".png")).convert("RGBA")
        spec={"id":name,"category":"floor" if index<5 else "edge"}
        record(job,spec,im,raw,tileable="xy" if index<5 else "x",
               extra={"transition_orientation":"grass_north_other_material_south"} if index>=5 else None)

folder=R/"fx"
if (folder/"raw-01.png").exists():
    job=json.loads((folder/"job.json").read_text());raw=folder/"raw-01.png"
    out=folder/"extracted"
    if not out.exists():
        run([F/"generate2dmap/scripts/extract_prop_pack.py","--input",raw,
             "--rows",4,"--cols",4,"--grid-rounding","nearest","--labels",
             ",".join(f"f{i:02}" for i in range(16)),"--keep-canvas","--component-mode","all",
             "--min-component-area",1,"--background-mode","chroma_key","--despill-radius",3,
             "--output-dir",out,"--art-source","host_image"])
    if (out/"prop-pack.json").exists():
        pack=json.loads((out/"prop-pack.json").read_text())
        inp=folder/"frame-inputs";inp.mkdir(exist_ok=True)
        for item in pack["accepted"]:
            index=int(item["label"][1:]);row,col=divmod(index,4)
            size=job["assets"][row]["cell"]
            im=Image.open(out/item["image"]).convert("RGBA").resize((size,size),Image.Resampling.NEAREST)
            im.save(inp/(item["label"]+".png"))
        pal=own_palette(inp,folder/"palette")
        finish(inp,pal,folder/"finished")
        for row,spec in enumerate(job["assets"]):
            size=spec["cell"];sheet=Image.new("RGBA",(size*4,size))
            for col in range(4):
                frame=Image.open(folder/"finished"/f"f{row*4+col:02}.png").convert("RGBA")
                sheet.alpha_composite(frame,(col*size,0))
            record(job,spec,sheet,raw,frames=4,fps=spec["fps"])

folder=R/"backdrops"
if (folder/"raw-01.png").exists():
    job=json.loads((folder/"job.json").read_text());raw=folder/"raw-01.png"
    out=folder/"extracted-measured"
    if not out.exists():
        run([F/"generate2dmap/scripts/extract_prop_pack.py","--input",raw,
             "--boxes-file",folder/"measured-boxes.json",
             "--keep-canvas","--component-mode","all","--min-component-area",1,
             "--background-mode","chroma_key","--despill-radius",3,"--output-dir",out,
             "--art-source","host_image"])
    if (out/"prop-pack.json").exists():
        pack=json.loads((out/"prop-pack.json").read_text())
        inp=folder/"inputs-measured";inp.mkdir(exist_ok=True)
        for item,spec in zip(pack["accepted"],job["assets"]):
            im=Image.open(out/item["image"]).convert("RGBA");box=im.getchannel("A").getbbox()
            # Preserve the full horizontal interval, including actual repeating endpoints.
            im=im.crop((0,box[1],im.width,box[3]))
            w,h=spec["px"];body_h=min(h,round(im.height*w/im.width))
            im=im.resize((w,body_h),Image.Resampling.NEAREST)
            canvas=Image.new("RGBA",(w,h));canvas.alpha_composite(im,(0,h-body_h))
            canvas.save(inp/(spec["id"]+".png"))
        pal=own_palette(inp,folder/"palette")
        finish(inp,pal,folder/"finished-measured")
        for spec in job["assets"]:
            im=Image.open(folder/"finished-measured"/(spec["id"]+".png")).convert("RGBA")
            a=np.array(im)
            fade=min(64,im.height//4)
            for y in range(im.height-fade,im.height):
                a[y,:,3]=(a[y,:,3].astype(float)*(im.height-1-y)/(fade-1)).astype("uint8")
            im=Image.fromarray(a)
            record(job,spec,im,raw,tileable="x",extra={"alpha_finish":"bottom 64px alpha removal fade",
                    "render_layer":"foreground" if "front" in spec["id"] else "background"})
write(R/"aux-manifest.json",{"assets":records})
print(json.dumps({"aux_assets":len(records),"pass":sum(a["mechanical_status"]=="pass" for a in records),
                  "blocked":[a["id"] for a in records if a["status"]=="blocked"]}))

