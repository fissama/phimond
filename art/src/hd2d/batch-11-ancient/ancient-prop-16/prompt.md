# Carved jade wall relief panel — candidate

Use case: HD-2D pixel-art map prop. Original Ancient screenshot supplies content and color; approved Octopath portal/rock and pet sheets set pixel style. Built-in Codex image_gen generated the source sheet. The separated arch halves are combined by alpha compositing because they form one collapsed arch; no art is drawn, mirrored, or repainted.

References:
- Ancient source image SHA-256 `85f51b9e8aa7bd9760b201ecacfc12f4decdb9c97af13dd69c96f948f6786475`
- Approved portal SHA-256 `55934f63667036937733b653177010865db6969905c57d324336c4199282467b`
- Approved rock SHA-256 `880eddcf56b10952735033d68d3f8b97c4e8412933a383fa08317aa7be0843ea01`
- Pet anchors SHA-256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`, `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- Generated raw sheet `raw-01.png` SHA-256 `40ead4da3b30d8761ef8f754307f3221620806a3ffe857761f3ef2bb9f531cba`

Route: built-in image_gen. Finish: boundary magenta flood-fill, transparent crop, 8px pad, binary alpha, nondithered 48-color quantization.
