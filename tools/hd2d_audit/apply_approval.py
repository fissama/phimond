#!/usr/bin/env python3
"""Áp quyết định duyệt art HD-2D từ một file JSON vào manifest các batch.

Cách dùng (từ gốc repo):
    python3 tools/hd2d_audit/apply_approval.py .ai/design/hd2d-approval-20261021.json [--dry-run]

Mỗi asset trong `scope` được đặt approved=true, status="approved", trừ những id nằm
trong `redo` (approved=false, status="redo", redo_reason=...) và `unused`
(approved=false, status="unused": asset không gán cho nội dung nào). Script chỉ sửa
manifest.json; không động vào ảnh, qa.json hay batch ngoài scope.
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "apps/game-web/art-src/hd2d"

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit(__doc__)
    dec = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    stamp = f"{dec['reviewer']} {dec['date']} (owner-delegated)"
    total = {"approved": 0, "redo": 0, "unused": 0}
    for batch in dec["scope"]:
        mf = ART / batch / "manifest.json"
        data = json.loads(mf.read_text(encoding="utf-8"))
        assets = data if isinstance(data, list) else data["assets"]
        redo = dec.get("redo", {}).get(batch, {})
        unused = dec.get("unused", {}).get(batch, {})
        ids = {a["id"] for a in assets}
        unknown = (set(redo) | set(unused)) - ids
        if unknown:
            sys.exit(f"{batch}: id không có trong manifest: {sorted(unknown)}")
        for a in assets:
            if a["id"] in unused:
                a.update(approved=False, status="unused", unused_reason=unused[a["id"]], reviewed_by=stamp)
                a.pop("approved_by", None); a.pop("redo_reason", None)
                total["unused"] += 1
            elif a["id"] in redo:
                a.update(approved=False, status="redo", redo_reason=redo[a["id"]], reviewed_by=stamp)
                a.pop("approved_by", None)
                total["redo"] += 1
            else:
                a.update(approved=True, status="approved", approved_by=stamp)
                a.pop("redo_reason", None); a.pop("unused_reason", None)
                total["approved"] += 1
        if isinstance(data, dict):
            data["approved"] = not redo
            data["status"] = "approved" if not redo else "approved_with_redo"
            data["review"] = {"by": stamp, "decision_file": args[0], "redo": len(redo)}
        if not dry:
            mf.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{batch}: {len(assets) - len(redo) - len(unused)} duyệt, {len(redo)} vẽ lại, {len(unused)} không dùng")
    print(f"Tổng: {total['approved']} duyệt, {total['redo']} vẽ lại, {total['unused']} không dùng" + (" (dry-run)" if dry else ""))

if __name__ == "__main__":
    main()
