"""Package generated Phimond assets with Forge. Never draws replacement artwork."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import hashlib,json,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parent
FORGE=Path("/Users/phileanh/.codex/skills")
PY=sys.executable
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+"\n")
def run(args):
    p=subprocess.run([PY,*map(str,args)],capture_output=True,text=True)
    print(p.stdout.strip(),flush=True)
    if p.stderr:print(p.stderr.strip(),file=sys.stderr)
    return p.returncode
records=[]
for job_file in sorted((ROOT/"jobs").glob("*/job.json")):
    job=json.loads(job_file.read_text())
    jobdir=job_file.parent
    raw=jobdir/job.get("selected_raw","raw-01.png")
    if not raw.exists():continue
    extracted=jobdir/job.get("extracted_dir","extracted")
    labels=[a["id"] for a in job["assets"]]
    if not extracted.exists():
        layout=(["--boxes-file",jobdir/job["boxes_file"]] if job.get("boxes_file") else ["--rows",job["rows"],"--cols",job["cols"],"--grid-rounding","nearest","--labels",",".join(labels)]
                if job.get("extraction")=="grid" else
                ["--auto-boxes","--labels",",".join(f"sprite-{i+1}" for i in range(sum(x not in ("skip","empty","-") for x in labels)))])
        args=[FORGE/"generate2dmap/scripts/extract_prop_pack.py","--input",raw,
              "--output-dir",extracted,*layout,
              "--component-mode","all","--alpha-hygiene","both",
              "--min-component-area",job.get("min_component_area","auto"),
              "--component-padding",16,"--background-mode","chroma_key",
              "--despill-radius",3,"--reject-edge-touch","--art-source","host_image"]
        if run(args):
            write(jobdir/"blocked.json",{"reason":"Forge extraction failed; keep raw and revise layout."})
            continue
    pack=json.loads((extracted/"prop-pack.json").read_text())
    items={}
    source_w,source_h=pack["source_size"]
    mapping=[]
    for item in pack["accepted"]:
        x0,y0,x1,y1=item["cell_box"]
        col=min(job["cols"]-1,int(((x0+x1)/2)/source_w*job["cols"]))
        row=min(job["rows"]-1,int(((y0+y1)/2)/source_h*job["rows"]))
        name=labels[row*job["cols"]+col]
        if name in items:raise RuntimeError(f"Ambiguous source ownership: {job['id']} / {name}")
        items[name]=item
        mapping.append({"asset_id":name,"source_label":item["label"],"source_box":item["cell_box"]})
    write(jobdir/"reviewed-identity-map.json",mapping)
    for spec in job["assets"]:
        name=spec["id"]
        if name in ("skip","empty","-"):continue
        if name not in items:continue
        item=items[name]
        dest=ROOT/name
        dest.mkdir(exist_ok=True)
        src=extracted/item["image"]
        im=Image.open(src).convert("RGBA")
        box=im.getchannel("A").getbbox()
        cropped=im.crop(box)
        height=round(cropped.height*spec["width"]/cropped.width) if spec.get("width") else spec.get("height",96)
        scale=height/cropped.height
        width=height if spec.get("square_body") else max(1,round(cropped.width*scale))
        cropped=cropped.resize((width,height),Image.Resampling.NEAREST)
        anchor_x=round((item["anchor_px"][0]-box[0])*width/(box[2]-box[0]))
        if spec.get("category")=="decal":anchor_x=width//2
        half=max(anchor_x,width-anchor_x)+8
        canvas=Image.new("RGBA",(half*2,height+16))
        canvas.alpha_composite(cropped,(half-anchor_x,8))
        if spec.get("repeat_x"):
            bb=canvas.getchannel("A").getbbox();canvas=canvas.crop((bb[0],0,bb[2],canvas.height));half=canvas.width/2
        canvas.save(dest/"crop.png")
        for original in jobdir.glob("raw-*.png"):
            if not (dest/original.name).exists():(dest/original.name).write_bytes(original.read_bytes())
        refs=[{"path":p,"sha256":sha(p)} for p in job["refs"]]
        revision=(jobdir/job["revision_prompt_file"]).read_text() if job.get("revision_prompt_file") else ""
        (dest/"prompt.md").write_text(job["prompt"]+"\n\n"+revision+"\n\nOrdered reference images:\n"+
            "\n".join(f"- {x['path']} / sha256 {x['sha256']}" for x in refs)+
            "\n\nRoute: built-in image_gen; model not exposed; raw SHA256 "+sha(raw)+"\n")
        (dest/"review.md").write_text("# Source identification\n\n"+job["source_card"]+
            "\n\nItem: "+name+". Owner approval pending. Review silhouette, material and scale.\n"+
            "Transform: Forge key/despill; crop; nearest size normalization; measured contact centering; 8px padding.\n")
        record={"id":name,"category":spec.get("category","prop"),"kit":spec.get("kit",job.get("kit","beach")),
          "file":name+"/final.png","px":list(canvas.size),"world":[canvas.width/128,canvas.height/128],
          "pivot":"bottom_center","pivot_px":[half,height+8],"pivot_uv":[.5,(height+8)/(height+16)],
          "tileable":"x" if spec.get("repeat_x") else "none","slice":None,"frames":1,"fps":None,"sway":spec.get("sway",False),
          "source_refs":job["refs"],"replaces":None,"approved":False,"status":"needs_owner_review",
          "art_source":"host_image","route":"built-in image_gen","source_job":job["id"],
          "raw_sha256":sha(raw),"source_raw":raw.name,"notes":"Octopath-directed review candidate. Not activated.",
          "pixel_finish_dir":"pixel-finish-repeat-x" if spec.get("repeat_x") else job.get("finish_dir","pixel-finish-job-palette"),
          "forge_manifest":str((extracted/"prop-pack.json").relative_to(ROOT))}
        if "part_of" in spec:record["part_of"]=spec["part_of"]
        if "attachment_offset_world" in spec:record["attachment_offset_world"]=spec["attachment_offset_world"]
        if spec.get("category")=="decal":
            record["pivot"]="center"
            record["pivot_px"]=[canvas.width/2,canvas.height/2]
            record["pivot_uv"]=[.5,.5]
        if spec.get("source_attachment_px"):
            sx,sy=spec["source_attachment_px"]
            record["attachment_socket_px"]=[half-anchor_x+(sx-item["cell_box"][0]-box[0])*width/(box[2]-box[0]),8+(sy-item["cell_box"][1]-box[1])*height/(box[3]-box[1])]
            record["source_attachment_px"]=[sx,sy]
        if spec.get("square_body"):
            record["notes"]+=" Flat circular decal normalized to equal body width/height for placement on a ground plane; source ellipse and original raw preserved."
        records.append(record)
for n in range(1,4):
    trunk=next((a for a in records if a["id"]==f"palm-{n:02}-trunk"),None)
    crown=next((a for a in records if a["id"]==f"palm-{n:02}-canopy"),None)
    if trunk and crown and trunk.get("attachment_socket_px") and crown.get("attachment_socket_px"):
        tx,ty=trunk["attachment_socket_px"];cx,cy=crown["attachment_socket_px"]
        tp=trunk["pivot_px"];cp=crown["pivot_px"]
        crown["attachment_offset_world"]=[(tx-tp[0]-cx+cp[0])/128,(tp[1]-ty-cp[1]+cy)/128,0]
        crown["sway_pivot_px"]=[cx,cy]
        crown["notes"]+=" Align measured socket to trunk socket; offset derived in128px/world with y up."
write(ROOT/"staged-assets.json",records)
# A fresh palette only includes the current delivery's cropped sprites.
palette=ROOT/"palette"
if not palette.exists() and records:
    inputs=ROOT/"palette-inputs"
    inputs.mkdir(exist_ok=True)
    for rec in records:
        (inputs/(rec["id"]+".png")).write_bytes((ROOT/rec["id"]/"crop.png").read_bytes())
    if run([FORGE/"generate2dsprite/scripts/palette_tool.py","build","--input",inputs,
            "--colors",48,"--balance","--name","phimond-octopath-beach","--output-dir",palette]):
        raise SystemExit(1)
# Per-job finishing allows resumable additions without rewriting accepted output.
# Job-balanced palettes retain cloth hues absent from the first utility sheet.
for job_id in sorted({rec["source_job"] for rec in records}):
    jd=ROOT/"jobs"/job_id
    jp=jd/"palette"
    if not jp.exists():
        ji=jd/"palette-inputs";ji.mkdir(exist_ok=True)
        for rec in records:
            if rec["source_job"]==job_id:
                (ji/(rec["id"]+".png")).write_bytes((ROOT/rec["id"]/"crop.png").read_bytes())
        if run([FORGE/"generate2dsprite/scripts/palette_tool.py","build","--input",ji,
                "--colors",48,"--balance","--output-dir",jp]):raise SystemExit(1)
for rec in records:
    dest=ROOT/rec["id"]
    finish=dest/rec["pixel_finish_dir"]
    if not finish.exists():
        if run([FORGE/"generate2dsprite/scripts/palette_tool.py","apply",
                "--input",dest/"crop.png","--palette",ROOT/"jobs"/rec["source_job"]/"palette/palette.json","--output-dir",finish]):
            rec["status"]="blocked"
            continue
    (dest/"final.png").write_bytes((finish/"crop.png").read_bytes())
    im=Image.open(dest/"final.png").convert("RGBA")
    box=im.getchannel("A").getbbox()
    margin=[box[0],box[1],im.width-box[2],im.height-box[3]]
    colors=len({p[:3] for p in im.get_flattened_data() if p[3]})
    partial=sum(p[3] not in (0,255) for p in im.get_flattened_data())
    failures=[]
    if min(margin[1::2] if rec["tileable"]=="x" else margin)<8:failures.append("alpha_margin_8")
    if colors>48:failures.append("palette_48")
    if partial:failures.append("binary_alpha")
    seam=None
    if rec["tileable"]=="x":
        a=np.asarray(im).astype(float)/255;rgb=a[:,:,:3]*a[:,:,3:4]
        seam=max(float(np.abs(b[:,0]-b[:,-1]).mean()*255) for b in (rgb,rgb+1-a[:,:,3:4]))
        if seam>=6:failures.append("seam_mean_below_6");rec["intended_tileable"]="x";rec["tileable"]="none"
        repeated=Image.new("RGBA",(im.width*3,im.height))
        for k in range(3):repeated.alpha_composite(im,(k*im.width,0))
        repeated.save(dest/"repeat-3x1.png")
        rec["notes"]+=" Horizontal alpha padding removed for repeated strip; vertical8px padding retained."
    qa={"seam_x_mean_255":seam,"seam_threshold":6,"colors":colors,"alpha_margins":margin,"partial_alpha":partial,"failures":failures,
        "raw_integrity":sha(dest/rec["source_raw"])==rec["raw_sha256"],"source_job":rec["source_job"]}
    write(dest/"qa.json",qa)
    rec["sha256"]=sha(dest/"final.png")
    rec["mechanical_status"]="blocked" if failures else "pass"
    if failures:rec["status"]="blocked"
    w,h=im.size
    preview=Image.new("RGB",(4*w+48,3*h+100),(55,61,70))
    draw=ImageDraw.Draw(preview)
    yy=25
    for scale in (1,2):
        pic=im.resize((w*scale,h*scale),Image.Resampling.NEAREST)
        for j,bg in enumerate(((235,232,220),(23,28,37))):
            xx=j*(w*scale+16)
            preview.paste(bg,(xx,yy,xx+pic.width,yy+pic.height))
            preview.paste(pic,(xx,yy),pic)
            draw.text((xx,yy-18),f"{scale}x / {'light' if j==0 else 'dark'}",fill="white")
        yy+=pic.height+32
    preview.save(dest/"review-light-dark.png")
if (ROOT/"aux-manifest.json").exists():
    records.extend(json.loads((ROOT/"aux-manifest.json").read_text())["assets"])
manifest={"batch":"03-octopath","approved":False,"status":"in_progress","assets":records}
write(ROOT/"manifest.json",manifest)
if records:
    cw,ch,cols=300,280,4
    sheet=Image.new("RGB",(cols*cw,64+((len(records)+cols-1)//cols)*ch),(26,31,41))
    d=ImageDraw.Draw(sheet)
    d.text((16,16),"PHIMOND / OCTOPATH DIRECTION / BEACH / OWNER REVIEW PENDING",fill="white")
    for i,rec in enumerate(records):
        if not (ROOT/rec["file"]).exists():continue
        im=Image.open(ROOT/rec["file"]).convert("RGBA")
        thumb=ImageOps.contain(im,(cw-24,ch-64),Image.Resampling.NEAREST)
        x=i%cols*cw;y=i//cols*ch+64
        sheet.paste(thumb,(x+(cw-thumb.width)//2,y),thumb)
        d.text((x+10,y+ch-42),rec["id"],fill="white")
        d.text((x+10,y+ch-24),rec.get("mechanical_status","blocked"),fill="white")
    sheet.save(ROOT/"contact-sheet.png")
print(json.dumps({"packaged":len(records),"pass":sum(x.get("mechanical_status")=="pass" for x in records)}))

