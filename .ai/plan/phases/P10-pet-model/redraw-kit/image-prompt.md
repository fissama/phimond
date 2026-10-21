# Image-generation prompt template

Worker: fill each [FIELD] from the job and an inspected identity card. This is
an image-tool prompt template, not permission to guess identity from the name.
Attach the two actual approved style sheets and original species images to the
image tool. Referring to filenames in text without attaching images is insufficient.

```text
Use case: style-transfer.
Asset: a production pixel-sprite animation atlas for the 2D RPG Phimond.
Species: [VIETNAMESE DISPLAY NAME], canonical ID [SPECIES_ID].

REFERENCE ROLES:
Image 1 = this species' original blurry APK portrait: PRIMARY IDENTITY and palette.
Image 2 = this species' original APK actor atlas: PRIMARY anatomy/silhouette.
Image 3 = approved DocDangNu sheet: STYLE ONLY, not anatomy or plant motifs.
Image 4 = approved DaoThienDuong sheet: STYLE ONLY, not bird anatomy or colors.
The original actor atlas may contain a generic gravestone. DO NOT copy the
stone; row 5 must depict this same creature becoming fully down.

SOURCE POLICY: Only the original APK assets and these TWO approved anchors
may inform the art. No previous/rejected redraw or procedural/minimax output.
Reconstruct clean readable pixels from the blurry original; preserve its
silhouette and proportions. Do not upscale blur or redesign from the name.

IDENTITY LOCK — repeat unchanged in all 20 frames:
[BODY FORM, HEAD/FACE, LIMB/WING/HORN COUNTS, PALETTE, CLOTHING, ACCESSORIES,
EXACT WEAPON COUNT AND WHICH HAND, SIGNATURE SILHOUETTE, PERSONALITY].
[LOCOMOTION: walk/scuttle/slither/hover/fly according to observed anatomy].
Do not replace this species with the anchors' characters. Do not add new limbs,
weapons, outfits, wings or markings. Keep held objects in every frame; if laid
on the ground in defeat they remain visibly present. Do not conceal them behind
large effects. Keep scale, face and proportions consistent.

PIXEL STYLE:
Match the anchors' dark colored pixel outlines, crisp larger color clusters,
clustered 2–4 tone shading and controlled saturation. Readable at 64–96px.
No smooth anime, vector edges, painted gradients, bloom, blurred resampling,
full-body glow, noisy microtexture, text, watermark, borders or scenery.

LAYOUT:
ONE SPECIES only. EXACT 1124×1405 RGBA PNG, genuine transparent background.
Four columns × five rows, each 281×281. Every nontransparent pixel including
faint effects must stay within local x/y [22,259) in its cell. Keep at least 22px
clear alpha margin on all sides. Body typically 155–202px tall; wide creatures
may be smaller to preserve the margin. Never stretch individual poses to fill
cells. Fixed three-quarter camera, opponent screen-left, stable ground/hover
pivot, generous spacing. No grid lines or baked checkerboard.

ORIENTATION LOCK: same three-quarter LEFT-facing view in ALL 20 frames,
including attack, cast and fallen poses. Nose/eyes/torso always orient left;
never flip/mirror, turn right, reverse equipment hands or show another camera.

ROW 1 IDLE (loop): four genuinely different subtle breathing/wing/hair/tail
poses; frame 4 joins frame 1 without jumping.
ROW 2 MOVE (loop): contact/passing/opposite contact/passing, or four coherent
wingbeat/slither phases. The only locomotion row. Keep body/feet cadence real.
ROW 3 BASIC ATTACK (one-shot): anticipation → wind-up → forward impact LEFT
→ recovery. [SPECIES-APPROPRIATE PHYSICAL ACTION]. Weapon/beak/claw follows
through toward the opponent; no backwards hit or four identical poses.
ROW 4 SIGNATURE CAST (one-shot): gather → form → release LEFT → dissipate.
[COMPACT VISUAL MOTIF DERIVED FROM ORIGINAL IDENTITY, NOT A NEW GAMEPLAY SKILL].
ROW 5 HURT/DOWN (one-shot): stagger → weakened → collapse → fully down resting
on the ground, non-gory. The last pose is not standing/stunned or just closing
eyes. Preserve anatomy and all equipment even when prone.

Keep basic impact effects compact, roughly ≤20–25% of safe-area width;
cast effects roughly ≤35–40%. These are guides; strict cell containment wins.
All 20 poses must be complete, distinct and clearly assigned to their row.
Idle differences may be subtle but must articulate body/wing/tail/cloth, not
just particle/position changes. Movement must change limb articulation through
a real contact/passing cycle. Attack/cast/down must show different body actions.
Do not simply shift, mirror or recolor one drawing to fabricate 20 frames.
```

The skill/cast motif is visual artwork only: never assign combat Element,
new abilities or numeric stats from it. Species Star/class remain registry data.
