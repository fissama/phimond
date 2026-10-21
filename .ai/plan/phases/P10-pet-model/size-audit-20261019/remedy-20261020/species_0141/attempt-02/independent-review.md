# Independent static review — species_0141 attempt-02

Decision: **FAIL pending resolution of a visible detached fragment in R5F3.** Mechanical PASS. Owner approval and runtime acceptance are not granted.

Exact SHA-256: `6531c1efbc5705e1e81cb5b2c3b1942102a42a0207e81e81b5889fd67d2feed7`.
Candidate: `apps/game-client/assets/pets/redraws/size-remedy-20261020/species_0141/attempt-02/packed.png`.
Before metadata identifies `polish-20261008/species_0141/slab-20261009/attempt-02/packed.png`, SHA-256 `06b9f556cd2574059edd497fb42aafc51f22bb656f955e94466589af5413b3e1`.

Inspected all 20 poses at native cells, equal 96px and 192px before/new/Linh Tiên comparisons, and R5F3 composited on a light background. Mechanical check was run directly. Browser playback is being reviewed separately and is not claimed here.

## Blocking static finding

**R5F3 (collapse): unexplained detached opaque bronze/orange arc to the right of the fallen cylinder.** It lies at cell-local x[229,234), y[143,179) at alpha ≥128, separated by visible empty space from the cylindrical body. It looks like a thin separate piece of the bronze rim, and remains visible in native and 192px comparison. The atlas does not otherwise establish a detachable part or this collapse effect, and R5F4 has no matching fragment. This is not merely a faint alpha-support speck. A clean no-foreign-fragment PASS cannot be given until its provenance/intent is established or the source artwork is repaired and repacked. Do not simply erase alpha to manufacture a gate pass. This finding does not assert that it is definitively a neighboring character: it is a visible unexplained fragment requiring disposition.

## Other inspected requirements

- R1F1–F4: gold fan crest, carved turquoise-accented face, barrel/slab body and two armored arms remain consistent; no legs added. Readable idle variations. Mean idle opaque height 155.75px versus old 66px and reference 162.75px. The solid gold body has adequate presence at equal 96px; details no longer collapse into the old tiny sprite.
- R2F1–F4: tilted hover/bob poses with compact square turquoise particles below; two arms/no legs preserved. Locomotion is appropriate to hovering anatomy. No obvious opaque spill from idle into movement found in the normal rendered image.
- R3F1–F4: anticipation, raised fist wind-up, extended screen-left punch, recovery. Both arms preserved; face/crest/palette remain stable. No obvious extra hand or mirrored direction swap.
- R4F1–F4: square-particle gather, one large triangular rune forms on the left, three triangular runes release on the left, compact dissipating squares. Triangle-count change fits form→release rather than anatomical drift. Geometric effect remains crisp and does not hide the face/body. Triangle symbols point right while their group is placed left; flight direction should be confirmed during separate playback, but geometric symbols alone do not prove a direction violation.
- R5F1–F4: stagger, lean/weaken, side-collapse, fully horizontal down. R5F4 is genuinely fully down and holds the same crest/face/two arms. R5F3 fragment is the blocking issue above.

Opaque exclusive bottom y (alpha ≥128) is idle 212/212/212/212; movement 209/209/207/210; attack 209/211/213/211; skill 209/207/209/209; hurt/down 207/213/211/209. These 207–213px values do not reproduce the large cumulative row drift found in species_0138 attempt-04. The slight lean/hover/contact variation is not a registration blocker in this static review.

Dark outlines, compact hard clusters, controlled highlights and gold/turquoise identity are legible at native/equal preview scales. No smooth full-body glow, rectangular haze, text, background or definite hallucinated limb found. Apart from R5F3, no visible foreign anatomical fragment established. Near-transparent residuals must not be treated as body measurement or as intentional FX without evidence.

## Mechanical evidence

Read-only `python3 tools/assets/check_p10_atlas.py <candidate>` returned exit 0 / PASS: PNG RGBA 1124×1405, 20 occupied/distinct cells, every alpha >0 pixel in [22,259). Checker hash matches metadata and the exact reviewed bytes.

No source image, metadata, approval or runtime mapping was changed by this reviewer. Saved only this review. Re-review the new exact hash or documented fragment disposition before a static PASS claim. Direct animation and in-game verification remain outside this static review.
