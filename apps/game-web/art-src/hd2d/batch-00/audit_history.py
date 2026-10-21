"""Collate every published Forge warning/failure and verify delivery provenance."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
history=[]
for path in sorted(root.rglob("*.json")):
    if path.name in {"qa-history.json","integrity.json"}:
        continue
    doc=json.loads(path.read_text())
    if not isinstance(doc,dict):
        continue
    qa=doc.get("qa")
    if isinstance(qa,dict):
        nonpass=[c for c in qa.get("checks",[]) if c.get("status") in ("warn","fail")]
        if nonpass or qa.get("status") in ("warn","fail"):
            history.append({"file":str(path.relative_to(root)),"status":qa.get("status"),
                            "checks":nonpass,"warnings":doc.get("warnings",doc.get("qc",{}).get("warnings",[]))})
(root/"qa-history.json").write_text(json.dumps(history,indent=2,ensure_ascii=False)+"\n")
manifest=json.loads((root/"manifest.json").read_text())
problems=[]
raw_count=0
for rec in manifest["assets"]:
    p=root/rec["file"]
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual!=rec["sha256"]:
        problems.append(rec["id"]+": final sha256")
    for raw,expected in rec["raw_sha256"].items():
        raw_count+=1
        if hashlib.sha256((p.parent/raw).read_bytes()).hexdigest()!=expected:
            problems.append(rec["id"]+": "+raw+" sha256")
    for name in ("prompt.md","review.md","qa.json"):
        if not (p.parent/name).exists():
            problems.append(rec["id"]+": missing "+name)
    if rec["status"]=="blocked" and rec["tileable"]!="none":
        problems.append(rec["id"]+": blocked but tileable")
report={"final_files":len(manifest["assets"]),"raw_copies_checked":raw_count,
        "qa_history_envelopes_with_warn_or_fail":len(history),"problems":problems,
        "integrity_pass":not problems}
(root/"integrity.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report))
raise SystemExit(bool(problems))

