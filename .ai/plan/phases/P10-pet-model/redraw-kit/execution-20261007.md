# P10 redraw150 — delivery for human review

Scope: separate sprite-art work, not a P10 gameplay phase delivery. Built-in imagegen used from the GPT-6.1 Sol task; no MiniMax or procedural artwork. Canonical IDs and Vietnamese names remain in manifest.json.

## Delivered

- 150 newly drawn species outside apk84/, excluding approved species0037 DocDangNu and0150 DaoThienDuong anchors.
- Each selected candidate is1124×1405 RGBA,4×5 cells of281px,20 occupied/distinct frames. All source alpha is retained by common nearest-neighbor packing; no pixel erasure to force validation.
- Original APK portrait/atlas define identity; two approved anchors define style. Fresh wrong-identity attempts were rejected and repaired, including0022 planthead,0073 secondface and0102 crest/forehead/one-tail anatomy.
- All selected candidates have self-review, exact-hash independent static review, prompt/reference records, packing evidence and local animation previews. Rejected attempts remain isolated as repair history and are not identity/style references.
- Gallery compares originals against selected candidates and provides64/96/192px preview controls. Idle/movement loop; attack/cast/hurt hold final frame. Timings are review presets, not gameplay rules.

## Verification

- Asset-tool unit tests:27 passed,0 failed.
- check-inputs:150 jobs and2 anchors verified; artwork_accepted=false.
- final-static-audit-20261007.json records exact selected hashes, whole-pose packing lineage, preview byte equality, metadata and current independent reviews.
- resume-C-provenance-20261007.json verifies304 original PNGs, original manifest and both anchor hashes unchanged; other-species redraw references forbidden.
- Five stale preview copies were regenerated from exact selected atlases. Selected raw metadata now points to its actual packed attempt; historical generation paths are labeled as history. All150 selected atlases have byte/hash-matched packing lineage from their selected raw, including an independent byte-identical repack for0094.
- Four missing selected call records (0002/0005/0008/0011) were recovered from exact recorded tool history and raw-byte hashes rather than inferred reference lists.

## Acceptance still pending

This is a static-review candidate delivery, not certification that all152 are game-ready. Human approval and continuous animation playback are explicitly false/pending for every candidate. No runtime activation was performed.

105 selected species have opaque idle height below the typical155px guidance. This measurement is diagnostic: wide silhouettes can require smaller composition, and containment takes priority. Check their readability at64px and relative scale against the two anchors before accepting them; smaller body size is not silently treated as approved. The exact list is in final-static-audit-20261007.json.

## Review entry points

- Local gallery: http://127.0.0.1:8124/index.html (art-only server).
- Workspace gallery: apps/game-client/assets/pets/redraws/batches/20261005/index.html.
- Selected file map: final-static-audit-20261007.json and each species/result.json.
- Prompts and actual reference paths/hashes: selected attempt's prompt and inputs*.json.

No push, merge, deploy, database mutation, server8090 restart or gameplay/spec migration belongs to this art scope. Existing peer client changes were preserved.

## Final verification — 2026-10-08

final-provenance-20261008.json: PASS150 selected candidates,304 unchanged originals,2 unchanged anchors,327 attempt input files and1415 reference records; zero issues. Recovered exact call metadata for0002/0005/0008/0011 is included. All150 selected raw paths, prompt/input paths, preview hashes and current independent review hashes were rechecked. Human acceptance, continuous playback and runtime activation remain pending;105 smaller silhouettes remain explicitly flagged.
