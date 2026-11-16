# Thần Đèn — cohesive atlas review

- Original APK ThanDen portrait and sprite sheet were the only imagegen references; raw and original hashes preserved in inputs.json.
- Source verification corrects prior brief: gold lamp is below body, hands free; long blue ribbon begins at head knot; orange lower curl, no legs. One lamp persists in all twenty frames, spout points right.
- Attempt01 rejected for outward Attack/Cast effects crossing vertical source dividers. Attempt02 limits magic to palms and preserves source art without alpha deletion.
- Source rows are visibly separated but unevenly spaced. Source rectangles use the actual empty gutters y=323,589,856,1125. Every significant pixel belongs to an intact pose; no automatic uniform-grid clipping. Vertical pose boundaries clear at alpha>=128. Full original alpha retained.
- One common NN pack scale 0.712230215827338 applies to all20; no per-frame resize. Source pivots align lamp base, destination pivot [140,220].
- Mechanical PASS: 20 occupied/distinct frames, RGBA1124x1405, safe alpha bounds. Beige alpha composite clean, no rectangular backdrops.
- Browser Idle/Move/Attack/Cast/Down viewed at64/96/192. Move uses hover/arm/ribbon changes, no invented leg walk; Attack short punch and recovery; Cast compact cyan palm light; final2 Down frames collapse over lamp. Light and dark previews checked.
- Pending owner approval, final independent review and shared battle size/UI layout gate. Runtime not active.
- Candidate SHA256: ee960bc6331965b69c4b0457ed59877064b77764faff0fc5c0695c942cab7fdd
