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
    """Choose a minimally smaller source crop; no pixels are painted, blended or mirrored."""
    w,h=im.size
    rgba=np.asarray(im.convert("RGBA")).astype(float)/255
    black=rgba[:,:,:3]*rgba[:,:,3:4];white=black+(1-rgba[:,:,3:4])
    layers=(black,white)
    def xscore(l,r):return max(float(np.abs(b[:,l]-b[:,w-1-r]).mean()*255) for b in layers)
    original_x=xscore(0,0)
    l=r=t=b=0
    if original_x>=6:
        limit=(16 if asset_id=="grass-floor-02" else 8) if w<=512 else (88 if asset_id=="forest-hedge-front" else 64)
        candidates=range(0,limit+1,1 if w<=512 else 2)
        l,r=min(((i,j) for i in candidates for j in candidates),key=lambda pair:(xscore(*pair),sum(pair)))
    if axes=="xy":
        def yscore(t,b):return max(float(np.abs(a[t,l:w-r or None]-a[h-1-b,l:w-r or None]).mean()*255) for a in layers)
        if yscore(0,0)>=6:
            bound=17 if asset_id=="grass-floor-02" else 9
            t,b=min(((i,j) for i in range(bound) for j in range(bound)),key=lambda pair:(yscore(*pair),sum(pair)))
    if l or r or t or b:
        return im.crop((l,t,w-r,h-b)).resize((w,h),Image.Resampling.NEAREST),[l,t,w-r,h-b]
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
    (dest/"prompt.md").write_text(job["prompt"]+("\n\n"+(raw.parent/job["revision_prompt_file"]).read_text() if job.get("revision_prompt_file") else "")+"\n\nOrdered reference images:\n"+
        "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs)+
        "\n\nRoute: built-in image_gen; model not exposed. Raw SHA256: "+sha(raw)+"\n")
    density=spec.get("density",128);fw=im.width//frames
    rec={"id":spec["id"],"category":spec["category"],"kit":spec.get("kit",job.get("kit","city")),"file":spec["id"]+"/final.png",
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

# Equal texture cells, actual output dimensions measured.
folder=R/"terrain"
if (folder/"raw-01.png").exists():
    job=json.loads((folder/"job.json").read_text());raw=folder/job.get("selected_raw","raw-01.png")
    atlas=Image.open(raw).convert("RGBA")
    tag=hashlib.sha256(json.dumps([job.get("selected_raw"),job.get("selected_raw_by_asset")],sort_keys=True).encode()).hexdigest()[:8]
    inp=folder/("inputs-"+tag);inp.mkdir(exist_ok=True)
    for i,spec in enumerate(job["assets"]):
        selected=folder/job.get("selected_raw_by_asset",{}).get(spec["id"],raw.name)
        atlas=Image.open(selected).convert("RGBA")
        row,col=divmod(i,job["cols"])
        box=(round(col*atlas.width/job["cols"]),round(row*atlas.height/job["rows"]),round((col+1)*atlas.width/job["cols"]),round((row+1)*atlas.height/job["rows"]))
        atlas.crop(box).resize(tuple(spec["px"]),Image.Resampling.NEAREST).save(inp/(spec["id"]+".png"))
    pal=own_palette(inp,folder/("palette-"+tag));finish(inp,pal,folder/("finished-"+tag))
    for spec in job["assets"]:
        finished=folder/job.get("selected_finished_by_asset",{}).get(spec["id"],"finished-"+tag+"/"+spec["id"]+".png")
        im=Image.open(finished).convert("RGBA")
        selected=folder/job.get("selected_raw_by_asset",{}).get(spec["id"],raw.name)
        record(job,spec,im,selected,tileable=spec.get("tileable","none"),extra={"art_review_status":"pending","seam_certification":"mechanical edge test only; inspect repeat preview for mortar/ridge discontinuities"})
folder=R/"fx"
if (folder/"raw-01.png").exists():
    job=json.loads((folder/"job.json").read_text());raw=folder/"raw-01.png"
    out=folder/"extracted-measured"
    if not out.exists():
        run([F/"generate2dmap/scripts/extract_prop_pack.py","--input",raw,
             "--boxes-file",folder/"measured-boxes.json","--keep-canvas","--component-mode","all",
             "--min-component-area",1,"--background-mode","chroma_key","--despill-radius",3,
             "--output-dir",out,"--art-source","host_image"])
    if (out/"prop-pack.json").exists():
        pack=json.loads((out/"prop-pack.json").read_text())
        inp=folder/"frame-inputs-measured";inp.mkdir(exist_ok=True)
        for item in pack["accepted"]:
            index=int(item["label"][1:]);row,col=divmod(index,4)
            size=job["assets"][row]["cell"]
            source=Image.open(out/item["image"]).convert("RGBA")
            factor=(size-24)/max(source.size)
            scaled=source.resize((round(source.width*factor),round(source.height*factor)),Image.Resampling.NEAREST)
            im=Image.new("RGBA",(size,size));im.alpha_composite(scaled,((size-scaled.width)//2,(size-scaled.height)//2))
            im.save(inp/(item["label"]+".png"))
        pal=own_palette(inp,folder/"palette-measured")
        finish(inp,pal,folder/"finished-measured")
        for row,spec in enumerate(job["assets"]):
            size=spec["cell"];sheet=Image.new("RGBA",(size*4,size))
            for col in range(4):
                frame=Image.open(folder/"finished-measured"/f"f{row*4+col:02}.png").convert("RGBA")
                sheet.alpha_composite(frame,(col*size,0))
            record(job,spec,sheet,raw,frames=4,fps=spec["fps"])

# Six teleport phases; register using the enclosed inner hole, not changing ornament extents.
folder=R/"teleport-ring"
if (folder/"raw-01.png").exists():
    sys.path.insert(0,str(F/"generate2dmap/scripts"))
    import forge_core
    job=json.loads((folder/"job.json").read_text());raw=folder/"raw-01.png";out=folder/"extracted"
    if not out.exists():
        run([F/"generate2dmap/scripts/extract_prop_pack.py","--input",raw,"--rows",2,"--cols",3,
             "--grid-rounding","nearest","--labels",",".join(f"f{i:02}" for i in range(6)),"--keep-canvas",
             "--component-mode","all","--min-component-area",1,"--background-mode","chroma_key",
             "--despill-radius",3,"--output-dir",out,"--art-source","host_image"])
    pack=json.loads((out/"prop-pack.json").read_text());sources=[];anchors=[];radius=0
    for item in pack["accepted"]:
        im=Image.open(out/item["image"]).convert("RGBA");a=np.asarray(im)[:,:,3]
        holes=[c for c in forge_core.connected_components(a==0) if not c["touches_edge"]]
        if not holes:raise RuntimeError("Teleport inner hole is not closed; manual registration needed")
        hb=holes[0]["bbox"];anchor=((hb[0]+hb[2])/2,(hb[1]+hb[3])/2)
        bb=im.getchannel("A").getbbox();radius=max(radius,anchor[0]-bb[0],bb[2]-anchor[0],anchor[1]-bb[1],bb[3]-anchor[1])
        sources.append(im);anchors.append(anchor)
    size=job["assets"][0]["cell"];factor=(size-32)/(radius*2);inp=folder/"registered-inputs";inp.mkdir(exist_ok=True)
    for i,(im,anchor) in enumerate(zip(sources,anchors)):
        scaled=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST)
        frame=Image.new("RGBA",(size,size));frame.alpha_composite(scaled,(round(size/2-anchor[0]*factor),round(size/2-anchor[1]*factor)))
        frame.save(inp/f"f{i:02}.png")
    write(folder/"registration.json",{"method":"largest enclosed alpha hole bbox center; shared uniform scale; translation only","anchors_source_px":anchors,"uniform_scale":factor,"frame_pivot_px":[size/2,size/2]})
    pal=own_palette(inp,folder/"palette");finish(inp,pal,folder/"finished")
    sheet=Image.new("RGBA",(size*6,size))
    for i in range(6):sheet.alpha_composite(Image.open(folder/"finished"/f"f{i:02}.png").convert("RGBA"),(i*size,0))
    record(job,job["assets"][0],sheet,raw,frames=6,fps=8,extra={"registration":"teleport-ring/registration.json"})
write(R/"aux-manifest.json",{"assets":records})
print(json.dumps({"aux_assets":len(records),"pass":sum(a["mechanical_status"]=="pass" for a in records),"blocked":[a["id"] for a in records if a["mechanical_status"]=="blocked"]}))
