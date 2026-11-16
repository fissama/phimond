"""Verify and preview the exported art. Preview labels are not runtime artwork."""
from pathlib import Path
import hashlib, json, math, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont

ROOT=Path(__file__).resolve().parent
records=json.loads((ROOT/"staged-assets.json").read_text())
def dump(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
try:
    FONT=ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",14)
    TITLE=ImageFont.truetype("/System/Library/Fonts/Menlo.ttc",24)
except OSError:
    FONT=ImageFont.load_default()
    TITLE=FONT

checks=[]
for rec in records:
    rec["scene_targets"]=["apps/game-web/public/scenes/forest.json"] if rec["kit"]=="forest" else ["apps/game-web/public/scenes/severa.json"] if rec["kit"]=="city" else []
    # Scene membership is not a one-to-one texture replacement mapping.
    rec["replaces"]=None
    dest=ROOT/rec["file"]
    shutil.copy2(ROOT/rec.get("finished_file", "finished/"+rec["kit"]+"/"+rec["id"]+".png"),dest)
    im=Image.open(dest).convert("RGBA")
    if rec["category"]=="prop":
        # Honor Forge's measured contact, rather than the silhouette's center.
        pack_path=ROOT/rec["forge_extraction_manifest"]
        pack=json.loads(pack_path.read_text())
        item=next(x for x in pack["accepted"]
                  if (pack_path.parent/x["image"]).resolve()==(ROOT/rec["source_file"]).resolve())
        source=Image.open(ROOT/rec["source_file"]).convert("RGBA")
        sb=source.getchannel("A").getbbox()
        tb=im.getchannel("A").getbbox()
        anchor_x=round(tb[0]+(item["anchor_px"][0]-sb[0])*(tb[2]-tb[0])/(sb[2]-sb[0]))
        half=max(anchor_x,im.width-anchor_x)
        centered=Image.new("RGBA",(2*half,im.height))
        centered.alpha_composite(im,(half-anchor_x,0))
        im=centered
        rec["pivot_px"]=[half,im.height-8]
        rec["pivot_uv"]=[0.5,(im.height-8)/im.height]
        rec["transforms"].append("translate to measured ground anchor; no painted pixels")
        im.save(dest)
    else:
        rec["pivot_px"]=[im.width/2,im.height/2]
        rec["pivot_uv"]=[0.5,0.5]
    rec["px"]=list(im.size)
    rec["world"]=[round(im.width/128,6),round(im.height/128,6)]
    arr=np.asarray(im.convert("RGBA"))
    a=arr[:,:,3]
    bbox=im.getchannel("A").getbbox()
    colors=len(np.unique(arr[a>0,:3],axis=0))
    margins=[bbox[0],bbox[1],im.width-bbox[2],im.height-bbox[3]]
    result={"id":rec["id"],"rgba":im.mode=="RGBA","size":list(im.size),
            "colors":colors,"alpha_levels":np.unique(a).tolist(),"margins":margins,
            "binary_alpha":set(np.unique(a)).issubset({0,255}),
            "density":[im.width/rec["world"][0], im.height/rec["world"][1]],
            "failures":[],"warnings":[]}
    if not result["rgba"]:result["failures"].append("rgba")
    if result["size"]!=rec["px"]:result["failures"].append("dimensions")
    if colors>48:result["failures"].append("palette_48")
    if not result["binary_alpha"]:result["failures"].append("partial_alpha")
    if rec["category"]!="floor" and min(margins)<8:result["failures"].append("alpha_margin_8")
    if rec["category"]=="floor":
        rgb=arr[:,:,:3].astype(float)
        seam_x=float(np.abs(rgb[:,0]-rgb[:,-1]).mean())
        seam_y=float(np.abs(rgb[0]-rgb[-1]).mean())
        result["seam_mean_255"]={"x":round(seam_x,4),"y":round(seam_y,4),"threshold":6}
        if seam_x>=6 or seam_y>=6:result["failures"].append("seam_mean_below_6")
        # Forge also checks relative edge steps; preserve its stricter failure.
        result["forge_wrap_seams"]="fail" if rec["kit"]=="forest" else "pass"
        if rec["kit"]=="forest":result["failures"].append("forge_wrap_seams")
        canvas=Image.new("RGBA",(1536,1536))
        for y in range(3):
            for x in range(3):canvas.alpha_composite(im,(x*512,y*512))
        canvas.save(dest.parent/"repeat-3x3.png")
    else:
        w,h=im.size
        canvas=Image.new("RGB",(max(2*w+32,4*w+32),3*h+80),(55,60,72))
        d=ImageDraw.Draw(canvas)
        yy=24
        for scale in (1,2):
            sprite=im.resize((w*scale,h*scale),Image.Resampling.NEAREST)
            for j,bg in enumerate(((235,234,225),(24,29,40))):
                xx=j*(w*scale+16)
                canvas.paste(bg,(xx,yy,xx+w*scale,yy+h*scale))
                canvas.paste(sprite,(xx,yy),sprite)
                d.text((xx,yy-20),f"{scale}x {'light' if j==0 else 'dark'}",font=FONT,fill="white")
            yy+=h*scale+28
        canvas.save(dest.parent/"review-light-dark.png")
    if rec["category"]=="ui_sprite":
        y,x=np.nonzero(a>=128)
        cov=np.cov(np.column_stack([x,-y]),rowvar=False)
        _,vec=np.linalg.eigh(cov)
        axis=vec[:,-1]
        angle=math.degrees(math.atan2(axis[1],axis[0]))%180
        if angle>90:angle=180-angle
        result["principal_axis_degrees"]=round(angle,3)
        result["angle_target"]=37
        if abs(angle-37)>1.5:result["failures"].append("button_axis_37_tolerance_1_5")
    rec["sha256"]=sha(dest)
    rec["qa_file"]=rec["id"]+"/qa.json"
    rec["mechanical_status"]="blocked" if result["failures"] else "pass"
    rec["status"]="blocked" if result["failures"] else "needs_owner_review"
    rec["approved"]=False
    if rec["category"]=="floor" and result["failures"]:
        rec["intended_tileable"]="xy"
        rec["tileable"]="none"
    if result["failures"]:
        rec["notes"]+=" Blocked checks: "+", ".join(result["failures"])+"."
    if rec["id"].startswith("forest-a-"):
        result["warnings"].append("Forge source extraction: 20 visible px belong to no auto box (small or faint parts).")
    if rec["category"]=="ui_9slice":
        result["warnings"].append("Nine-slice margins are proposed; validate stretch preview and owner choice.")
    dump(dest.parent/"qa.json",result)
    identity=("Broadleaf tree, gnarled umber trunk, emerald/lime foliage; full static tree, no sway split in Batch 00."
              if rec["id"].endswith("-tree") else
              "Rounded green shrub with pink and yellow flower accents." if rec["id"].endswith("-bush") else
              "Standing curled fantasy metal street lamp; pale stone foot and amber glass." if "lamp" in rec["id"] else
              "Upright oak barrel with metal hoops, visible lid." if "barrel" in rec["id"] else
              "Navy/gold menu panel with asymmetric left scroll ornament and empty center." if rec["category"]=="ui_9slice" else
              "Blank diagonal blue/gold oval confirm button; state encoded by face color." if rec["category"]=="ui_sprite" else
              "Original-biome ground texture, no props." if rec["category"]=="floor" else
              "Separate low forest grass, fern or flower clump; colors follow the original forest.")
    (dest.parent/"review.md").write_text(
        "# Source identification and review\n\n"+identity+
        f"\n\nDeclared canvas/world: {rec['px']} / {rec['world']}; actual body excludes alpha padding.\n\n"
        f"Mechanical status: {rec['mechanical_status']}. Owner approval: pending.\n"
        f"Failures: {result['failures'] or 'none'}.\nWarnings: {result['warnings'] or 'none'}.\n\n"
        "Review the native-size light/dark PNG and contact sheet. No text is baked into the runtime asset.\n"
        "Finishing: Forge chroma extraction/despill, crop, nearest size normalization, shared 48-color palette with binary alpha. Raw files unchanged.\n"
        "A numeric pass proves file geometry and palette only; it does not approve style, identity, nine-slice behavior or tile repetition by eye.\n")
    checks.append(result)

# A labelled contact sheet grouped by kit and option.
order=sorted(records,key=lambda r:(["forest","city","ui"].index(r["kit"]),r["id"]))
cell_w,cell_h,cols=360,300,4
rows=(len(order)+cols-1)//cols
sheet=Image.new("RGB",(cols*cell_w,rows*cell_h+64),(25,30,41))
d=ImageDraw.Draw(sheet)
d.text((20,16),"PHIMOND / BATCH 00 / UNAPPROVED STYLE CANDIDATES",font=TITLE,fill="white")
for i,rec in enumerate(order):
    x=(i%cols)*cell_w
    y=(i//cols)*cell_h+64
    d.rectangle((x+4,y+4,x+cell_w-5,y+cell_h-5),fill=(40,47,60))
    im=Image.open(ROOT/rec["file"]).convert("RGBA")
    thumb=ImageOps.contain(im,(cell_w-30,cell_h-65),method=Image.Resampling.NEAREST)
    sheet.paste(thumb,(x+(cell_w-thumb.width)//2,y+12),thumb)
    d.text((x+12,y+cell_h-48),rec["id"],font=FONT,fill="white")
    d.text((x+12,y+cell_h-28),rec["mechanical_status"],font=FONT,
           fill=(255,152,117) if rec["mechanical_status"]=="blocked" else (148,213,179))
sheet.save(ROOT/"contact-sheet.png")

# Palette + real artwork samples; all artwork comes from generated PNGs.
guide=Image.new("RGB",(1440,1020),(25,30,41));d=ImageDraw.Draw(guide)
d.text((20,16),"PHIMOND / PROPOSED PIXEL STYLE / OWNER CHOICE PENDING",font=TITLE,fill="white")
for row,kit in enumerate(("forest","city","ui")):
    y=row*310+70
    swatches=Image.open(ROOT/"palettes"/kit/"swatches.png").convert("RGB")
    swatches=ImageOps.contain(swatches,(620,120),method=Image.Resampling.NEAREST)
    guide.paste(swatches,(20,y+35))
    d.text((20,y),kit+" / shared 48-color palette",font=TITLE,fill="white")
    ids={"forest":["forest-a-tree","forest-b-tree"],"city":["city-lamp-a","city-barrel-b"],
         "ui":["ui-panel-a","ui-confirm-b-normal"]}[kit]
    for j,asset_id in enumerate(ids):
        sample=Image.open(ROOT/asset_id/"final.png").convert("RGBA")
        sample=ImageOps.contain(sample,(320,260),method=Image.Resampling.NEAREST)
        guide.paste(sample,(700+j*360,y),sample)
    d.text((20,y+190),"Hue-tinted outline / upper-left warm key / cool shade",font=FONT,fill="white")
    d.text((20,y+215),"No ground shadow, fog or bloom in runtime sprites",font=FONT,fill="white")
guide.save(ROOT/"style-guide.png")
summary={"assets":len(records),"mechanical_pass":sum(not r["failures"] for r in checks),
         "blocked":sum(bool(r["failures"]) for r in checks),"owner_approved":0,
         "status":"needs_owner_review_and_blocker_resolution","checks":checks}
dump(ROOT/"qa-summary.json",summary)
dump(ROOT/"manifest.json",{"batch":"00","status":summary["status"],"approved":False,
                         "density_px_per_world":128,"assets":records})
dump(ROOT/"blocked.json",[{"id":r["id"],"failures":r["failures"]} for r in checks if r["failures"]])
print(json.dumps({k:v for k,v in summary.items() if k!="checks"}))

