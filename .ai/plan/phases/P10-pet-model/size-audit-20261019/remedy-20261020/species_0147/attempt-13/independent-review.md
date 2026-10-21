# Independent review — species_0147 attempt-13, APK identity correction

Decision: **PASS for inspected static identity/art and mechanical containment; conditional PASS for the explicitly registered display preview.** No remaining mandatory visible art blocker found on this binding. Direct playback, owner art acceptance and runtime verification remain pending. Native atlas used without the registered origins still has inconsistent row/frame ground contact and is not independently certified for direct runtime use.

Exact candidate SHA-256: `44f0e06157dc418e030b14cb413d73aa37640780b54f0e6791bb72e4a79e7021`.
Candidate: `apps/game-client/assets/pets/redraws/size-remedy-20261020/species_0147/attempt-13/packed.png`.
Registered preview: `../art-redo-20261021/profile.json`, SHA-256 `aac53dc35d44a3574e15f6f20c1abbb74c3ae2abeeb6bdfba13cdd34a9508ebc`.

## Inspection and identity

Inspected all20 poses in actual-alpha native dark/light JPGs and fixed96/192 source comparisons, the supplied `original-reference-20261021.png`, and regenerated all20-frame96/192 registered stages. Also inspected the candidate-only center of the192 stage to avoid relying only on the resized three-panel sheet. Read profile and HTML origin selection; no playback-watching claim is made.

The candidate materially restores APK identity: heavy hunched shoulder/back silhouette; layered shaggy ivory fur with slate shadows; dark slate face with narrow yellow eyes; olive/khaki chest/belly; two long ivory tusks; one rough pale axe head on a brown handle. It no longer reads as the white round gorilla/red-eye/gold-tusk/orange-star-mace redesign rejected by the owner. No new armor, jewelry or duplicate weapon was found.

## All20 pose observations

- R1F1–F4: four subtle changes preserve the same head, shaggy coat, long tusks and axe. Face/eye/tusks stay recognizable at96px once the registered190px display profile is applied.
- R2F1–F4: heavy step/contact and passing poses are materially different. F2 raises one foot; F4 brings the opposing foot through, rather than only translating one standing pose. Two arms/two legs remain coherent; the axe remains with its holding arm. Temporal4→1 rhythm still needs playback.
- R3F1–F4: preparation, raised axe wind-up, down-left strike with compact ground ice, recovery. The raised hand/axe remain connected; the other hand moves in front of the chest/body without establishing a second axe. Axe head and tips appear complete. Ground-ice alpha extends below the boot contact in F3 and must not determine its root.
- R4F1–F4: small gathering ice particles, formed ice around the existing axe, three released ice shards on the left, dissipating particles. The ice-covered axe head is a weapon effect rather than a second weapon. Face/body remain visible.
- R5F1–F4: stagger, weakened kneel, collapse, fully prone. Both long tusks belong to the same head; the one axe remains beside it in the final pose. Final frame is genuinely down, not upright stunned.

Layered hard fur clusters, dark outlines, face and pale axe remain legible against light and dark backgrounds. No visible rectangular background haze, text, borders, definite neighboring anatomical fragment, missing weapon tip or definite hallucinated limb found. The preview keeps a broad heavy creature rather than matching the fairy anatomy.

## Size and registration binding — important limitation

Mean native opaque idle height is **140.25px**, versus prior rejected attempt09 **170px**, original before70.25px, and Linh Tiên162.75px. The new artwork is not a native170px atlas and is not the same pixel-detail density as attempt09. The retained190px display target is achieved by one common factor **1.3547237076648841** for every pose, not by adding new pixels or changing scale frame by frame.

Raw packed exclusive opaque bottoms by row:

- Idle235/235/235/236.
- Move215/215/215/220.
- Attack213/207/222/213, where F3 low ice contributes to222 while boot contact is near213.
- Skill207/207/207/209.
- Hurt/down202/201/210/207.

The initial fixed-row registration alone left within-row differences. Final inspected profile instead records explicit manual contact origins for all20 poses:
`235,235,235,236,215,215,215,220,213,207,213,213,207,207,207,209,202,201,210,207`, all x140. HTML actually reads `frame_pivots[row*4+frame]` before falling back to a row pivot. Inspected final stage proofs show the corresponding soles/prone body returning to the common floor without changing body scale; attack F2 hover and move F4/down contact offsets are resolved in this private projection. F3 ice sits naturally below boot ground rather than being cropped or used to shrink the character.

This is a **conditional registered-preview result**, not a claim that native PNG registration or runtime rendering has been fixed. Future runtime must consume the matching source origins and common scale and pass real camera/UI/animation checks; otherwise the native offsets above return. Owner approval of the prior190px size target is not acceptance of these new art pixels.

## Mechanical/provenance and tooling

Read-only `python3 tools/assets/check_p10_atlas.py <candidate>` returned exit0 / PASS: RGBA PNG1124×1405;20 occupied/distinct cells; every alpha>0 pixel in cell-local[22,259). Exact checker SHA agrees with metadata.

Packing scale0.8353982300884955 and destination[140,258] are recorded. Declared source rectangles cover every alpha>0 pixel of the current raw image; raw SHA agrees with packing metadata. This proves coverage of the current generated raw, not equality with earlier rejected artwork.

Review reading/checking/writing tools succeeded in this review; no quota failure occurred in these calls. This does not erase or contradict any earlier generation quota failure recorded by the lead. No generative tool was called by this reviewer.

Only this Markdown report was saved. Source/candidate pixels, owner selection, approval state, display configuration and runtime were not changed by this reviewer. Direct playback and final human approval remain separate.
