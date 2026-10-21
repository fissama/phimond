"""Stage A only. Crop generated pixels, key magenta with Forge, palette-map, QA.
No scene content is drawn by this script. Checkerboards, labels and composites are QA only.
Reuses batch01 package.py workflow with measured 2x2 ownership and full viewport canvases.
"""
from pathlib import Path
import sys,json,hashlib,shutil
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parent
sys.path.insert(0,"/Users/phileanh/.codex/skills/generate2dmap/scripts")
from extract_prop_pack import key_sheet
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):Path(p).write_text(json.dumps(o,indent=2,ensure_ascii=False)+"\n")
def palette_map(im,colors):
    pal=Image.new("P",(1,1));flat=[v for c in colors for v in c];pal.putpalette(flat+flat[:3]*(256-len(colors)))
    result=im.convert("RGB").quantize(palette=pal,dither=Image.Dither.NONE).convert("RGBA")
    result.putalpha(im.getchannel("A"))
    a=np.array(result);a[a[:,:,3]==0,:3]=0
    return Image.fromarray(a)
def load_colors(p):return [tuple(bytes.fromhex(c["hex"][1:])) for c in json.loads(p.read_text())["colors"]]
def preview(im,scale,checker):
    pic=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
    if checker:
        y,x=np.indices((pic.height,pic.width));v=np.where(((x//(16*scale)+y//(16*scale))%2)==0,65,94).astype("uint8")
        bg=Image.fromarray(np.repeat(v[:,:,None],3,axis=2)).convert("RGBA")
    else:bg=Image.new("RGBA",pic.size,(22,27,34,255))
    bg.alpha_composite(pic);return bg.convert("RGB")
cfg=json.loads((R/"jobs/login-stage-a/selection.json").read_text())
job=json.loads((R/"jobs/login-stage-a/job.json").read_text())
palroot=R/"palette";palroot.mkdir(exist_ok=True)
forestpath=R.parent/"batch-01-octopath/palette/palette.json"
townpath=R.parent/"batch-02-octopath/jobs/city-facades/palette/palette.json"
forest_all=load_colors(forestpath)
# No violet materials in these leaf/earth layers; exclude the approved palette's violet-flower ramp.
forest=[c for c in forest_all if not (c[0]>c[1]+25 and c[2]>c[1]+25)]
town=load_colors(townpath)
# Supplement town masonry/wood ramp with16 actual forest greens; never invent RGB art.
greens=[c for c in forest if c[1]>c[0]*1.02 and c[1]>c[2]*1.15]
greens=[greens[i] for i in np.linspace(0,len(greens)-1,min(16,len(greens))).astype(int)]
townplus=list(dict.fromkeys(town+greens))
write(palroot/"forest.json",{"source":str(forestpath),"sha256":sha(forestpath),"colors":[{"hex":"#%02x%02x%02x"%c} for c in forest]})
write(palroot/"town.json",{"source":str(townpath),"sha256":sha(townpath),"supplement":str(forestpath),"colors":[{"hex":"#%02x%02x%02x"%c} for c in townplus]})
records=[];finals={}
for spec in cfg["assets"]:
    name=spec["id"];d=R/name;d.mkdir(exist_ok=True)
    selected=R/"jobs/login-stage-a"/spec["raw"]
    raw=Image.open(selected).convert("RGBA");cropped=raw.crop(tuple(spec["source_box"]))
    if name.endswith("sky"):
        keyed=cropped
        p=cropped.convert("RGB").quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
        rgb=p.getpalette();indexes=sorted(set(p.get_flattened_data()));colors=[tuple(rgb[i*3:i*3+3]) for i in indexes]
        write(palroot/"dawn.json",{"source":str(selected),"raw_sha256":sha(selected),"colors":[{"hex":"#%02x%02x%02x"%c} for c in colors],"note":"Only additional dawn palette;64color nondithered quantization of generated pixels."})
        finish=p.convert("RGBA");palette="palette/dawn.json";despill={"mode":"not_needed_opaque_sky"}
    else:
        aa,despill=key_sheet(np.asarray(cropped),"chroma_key",180,220,3)
        # Remaining key-hue contamination only; actual objects have no violet material.
        rgb=aa[:,:,:3].astype(int)
        residue=(rgb[:,:,0]>rgb[:,:,1]+30)&(rgb[:,:,2]>rgb[:,:,1]+30)
        aa[residue]=0
        despill["additional_key_hue_removed_px"]=int(residue.sum())
        keyed=Image.fromarray(aa)
        finish=palette_map(keyed,townplus if name.endswith("citadel") else forest)
        palette="palette/town.json" if name.endswith("citadel") else "palette/forest.json"
    keyed.save(d/"keyed-source.png")
    finish=finish.resize((1280,720),Image.Resampling.NEAREST)
    finish.save(d/"final.png")
    for rp in sorted((R/"jobs/login-stage-a").glob("raw-*.png")):shutil.copyfile(rp,d/rp.name)
    attempts=[]
    for attempt in cfg["attempts"]:
        refs=[{"path":p,"sha256":sha(p)} for p in attempt["refs"]]
        attempts.append({**attempt,"reference_hashes":refs,"raw_sha256":sha(R/"jobs/login-stage-a"/attempt["raw"])})
    text="# Generation provenance\n\n"
    for at in attempts:
        text+=f"## {at['raw']}\n\n{at['prompt']}\n\nRoute: built-in image_gen; model not exposed.\nRaw SHA256: {at['raw_sha256']}\n\nActual ordered attachments:\n"
        text+="\n".join(f"{n+1}. {ref['path']} — SHA256 {ref['sha256']}" for n,ref in enumerate(at["reference_hashes"]))+"\n\n"
    text+=f"Selected source: {spec['raw']}; measured source box: {spec['source_box']}. Palette: {palette}. Nearest resize to1280x720. No repaint, synthesized pixels, mirroring, glow or alpha fade.\n"
    (d/"prompt.md").write_text(text)
    a=np.asarray(finish);alpha=a[:,:,3];visible=alpha>0;ys,xs=np.where(visible)
    colors=len(np.unique(a[:,:,:3][visible],axis=0))
    margins=[int(xs.min()),int(ys.min()),int(1279-xs.max()),int(719-ys.max())]
    # Magenta-dominant visible pixels include neither real leafgreen nor legitimate ochre.
    rgb=a[:,:,:3].astype(int)
    pink=visible&(rgb[:,:,0]>rgb[:,:,1]+45)&(rgb[:,:,2]>rgb[:,:,1]+45)&(rgb[:,:,0]>100)&(rgb[:,:,2]>100)
    q={"id":name,"px":[1280,720],"mode":finish.mode,"colors":colors,"color_limit":64,
       "partial_alpha_pixels":int(((alpha>0)&(alpha<255)).sum()),"key_residue_pixels":int(pink.sum()),
       "alpha_margins":margins,"backdrop_edge_exception":"Side/bottom coverage intentional; whole viewport layer, no isolated prop is clipped.",
       "bottom_24px_fully_opaque":bool((alpha[-24:]==255).all()),"source_raw":spec["raw"],
       "raw_integrity":sha(d/spec["raw"])==sha(selected),"sha256":sha(d/"final.png"),"despill":despill,
       "visual_review":"pending_actual_4x_inspection"}
    q["failures"]=[]
    if colors>64:q["failures"].append("COLORS")
    if q["partial_alpha_pixels"]:q["failures"].append("SEMI_ALPHA")
    if q["key_residue_pixels"]:q["failures"].append("CHROMA_RESIDUE")
    if not q["raw_integrity"]:q["failures"].append("RAW_INTEGRITY")
    if not q["bottom_24px_fully_opaque"]:q["failures"].append("BOTTOM_OVERLAP24")
    write(d/"qa.json",q)
    for checker,label in ((True,"checker"),(False,"dark")):
        preview(finish,4,checker).save(d/f"review-4x-{label}.png")
        region=finish.crop(tuple(spec["review_crop"]))
        preview(region,4,checker).save(d/f"detail-4x-{label}.png")
    density=64 if spec["category"]=="backdrop_far" else 128
    rec={"id":name,"category":spec["category"],"kit":"login","file":name+"/final.png","px":[1280,720],
       "size_px":[1280,720],"world":[1280/density,720/density],"world_size":[1280/density,720/density],
       "pivot":"center","pivot_px":[640,360],"pivot_uv":[.5,.5],"tileable":"none","slice":None,
       "frames":1,"fps":None,"sway":False,"art_source":"host_image","route":"built-in image_gen",
       "source_refs":job["refs"],"source_raw":spec["raw"],"source_box":spec["source_box"],
       "raw_sha256":sha(selected),"sha256":sha(d/"final.png"),"palette":palette,
       "approved":False,"status":"needs_claude_visual_review","mechanical_status":"blocked" if q["failures"] else "pass",
       "notes":spec["notes"]+" Camera-aligned1280x720 layer. Binaryalpha.24px bottom coverage. No runtime activation."}
    records.append(rec);finals[name]=finish
# Only visual QA stacking. Approved login-panorama deliverable deferred until owner accepts layers.
stack=Image.new("RGBA",(1280,720))
for spec in cfg["assets"]:stack.alpha_composite(finals[spec["id"]])
stack.save(R/"qa-layer-stack.png")
overlaps=[]
for back,front in zip(cfg["assets"],cfg["assets"][1:]):
    ab=np.asarray(finals[back["id"]])[:,:,3]>0;af=np.asarray(finals[front["id"]])[:,:,3]>0
    shared=ab&af
    runs=[]
    for x in range(1280):
        y=719
        while y>=0 and shared[y,x]:y-=1
        runs.append(719-y)
    overlaps.append({"behind":back["id"],"front":front["id"],"minimum_contiguous_bottom_overlap_px":min(runs),"required_minimum":24,"pass":min(runs)>=24})
write(R/"overlap-qa.json",{"pairs":overlaps,"note":"Fullscreen aligned layer masks, measured shared opaque bottomcoverage. Lateral parallax reveal outside1280canvas not certified."})
write(R/"manifest.json",{"batch":"10-octopath","stage":"A","status":"needs_claude_visual_review","approved":False,"assets":records,
       "deferred_stages":["B branding","C loading","D intro"],"login_panorama":"Not published before layer approval; qa-layer-stack.png is review-only."})
sheet=Image.new("RGB",(1280,840),(23,28,37));dr=ImageDraw.Draw(sheet)
for i,rec in enumerate(records):
    x=(i%2)*640;y=(i//2)*420
    thumb=preview(finals[rec["id"]],1,True).resize((640,360),Image.Resampling.NEAREST);sheet.paste(thumb,(x,y+30))
    dr.text((x+12,y+8),rec["id"]+" / unapproved draft",fill=(235,230,210))
    q=json.loads((R/rec["id"]/"qa.json").read_text());dr.text((x+12,y+396),f"{q['colors']}colors / binaryalpha /1280x720",fill=(210,215,220))
sheet.save(R/"contact-sheet.png")
write(R/"qa-summary.json",{"assets":len(records),"mechanical_failures":[r["id"] for r in records if r["mechanical_status"]!="pass"],
      "visual_approval":False,"overlap_pairs":overlaps,"route":"built-in image_gen"})
print(json.dumps({"assets":len(records),"colors":{r["id"]:json.loads((R/r["id"]/"qa.json").read_text())["colors"] for r in records},"mechanical_blocked":[r["id"] for r in records if r["mechanical_status"]!="pass"]}))

