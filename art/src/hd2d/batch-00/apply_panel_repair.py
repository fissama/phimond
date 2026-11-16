from pathlib import Path
import hashlib,json,shutil
from PIL import Image
r=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=json.loads((r/"staged-assets.json").read_text())
pack=json.loads((r/"forge-ui-repaired/prop-pack.json").read_text())
inputs=r/"finish-inputs-panel-repair"
inputs.mkdir(exist_ok=True)
repair=(r/"ui-sheet/repair-prompt.md").read_text()
for item in pack["accepted"]:
    asset_id="ui-"+item["label"]
    rec=next(x for x in records if x["id"]==asset_id)
    source=r/"forge-ui-repaired"/item["image"]
    im=Image.open(source).convert("RGBA")
    im=im.crop(im.getchannel("A").getbbox())
    ratio=min(1460/im.width,680/im.height)
    im=im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.NEAREST)
    canvas=Image.new("RGBA",(1476,696))
    canvas.alpha_composite(im,((1476-im.width)//2,(696-im.height)//2))
    dest=r/asset_id
    shutil.copy2(dest/"crop.png",dest/"crop-before-repair.png")
    canvas.save(dest/"crop.png")
    canvas.save(inputs/(asset_id+".png"))
    shutil.copy2(r/"ui-sheet/raw-02.png",dest/"raw-02.png")
    (dest/"prompt.md").write_text((dest/"prompt.md").read_text()+"\n\n## Targeted nine-slice repair\n\n"+repair+
                                "\nSHA256 raw-02.png: "+sha(dest/"raw-02.png")+"\n")
    rec["source_file"]=str(source.relative_to(r))
    rec["source_sha256"]=sha(source)
    rec["raw_sha256"]["raw-02.png"]=sha(dest/"raw-02.png")
    rec["forge_extraction_manifest"]="forge-ui-repaired/prop-pack.json"
    rec["finished_file"]="finished/ui-panel-repair/"+asset_id+".png"
    rec["slice"]=[400,240,120,240]
    rec["notes"]+=" Repaired side rails: ornaments confined to fixed corners; slice preview available."
(r/"staged-assets.json").write_text(json.dumps(records,indent=2,ensure_ascii=False)+"\n")
jobs=json.loads((r/"generation-jobs.json").read_text())
job=next(x for x in jobs["jobs"] if x["id"]=="ui-sheet")
job["prompts"].append(repair)
job["raw"].append("raw-02.png")
job["repair_reference"]={"path":"ui-sheet/raw-01.png","sha256":sha(r/"ui-sheet/raw-01.png")}
job["notes"]="Buttons use raw-01; repaired panels use raw-02; same UI palette."
(r/"generation-jobs.json").write_text(json.dumps(jobs,indent=2,ensure_ascii=False)+"\n")
print("Prepared 2 panel repairs, raw files unchanged.")

