# Independent display-scale preview review

Decision: **Conditional PASS for this preview profile as a basis for owner comparison and later scene trials.** No blanket redraw requirement or general overgrowth failure found. Species0147 candidate substitution/re-render was completed during review and its delta was checked. This review does not certify actual-game scale, animation or owner acceptance.

Final reviewed `proposals.json` SHA-256: `dbe86cc224df5789f95447ad27f9d0c7564060801d3637fd209b5ec2abdd31ce`. Initial pass used `bc7d0ca6ef8dff3855caed2e232a16552784e0467636aaa491aff94ec173237c`; intermediate0147 substitution used `2601246371a8edb5a903d2d44154e746a5b9aefd8b0151d6b75a7f5f6eedff49`. The final0088/0156 deltas were inspected against their regenerated20-frame192px proofs and overview03.
Reviewed `verification.json` SHA-256: `82c3b9bc1c9a535e7c4a2a8ecc686f7d4bbc5d3f0b217a6fa34e6632bc454845`.
These dispositions apply to this proposal hash, not a later regenerated document automatically.

## Scope and integrity

Independently counted56 records and56 unique IDs: all32 A/B targets plus24 controls, with no missing target. All56 source files hash-match their proposal records. Species0144 remains factor1.0 at the unchanged approved path `owner-feedback-20261009/species_0144/attempt-01/packed.png`, SHA-256 `63efbba22985c5e938be71bcfb2aebbc9db3ec1b9d12bd8d38c5a5ce5d666dd4`.

Read proposals/verification and preview draw logic. Reviewed overview01–07 (all56), all20-frame192px proofs for0015/0069/0051/0126/0156, plus broad quadruped0087 and dragon0017; final delta includes species0147 all20-frame96/192 proofs and overview06. Also examined all20-frame96px proofs for the five uncertain IDs and192px control0088. Common floor/reference magnification and one factor per species are appropriate for comparison. Species0156 now also has explicitly documented fixed action-row roots; no per-frame auto-fit is present in the inspected draw logic. Verification reports2240 alpha-footprint checks, no alpha erasure and no runtime activation; those flags are not proof of live scene camera behavior.

## Findings and concrete profile actions

1. **Final binding verified — species0147.** The lead regenerated the private preview during this review, replacing the old70.25px approved-source projection (factor2.70463) with independently reviewed remedy attempt09 SHA-256 `d5a7dcc4955deff1db4608104d8f5ffd5472bb213600c0e46dc0b041e0123cff`. Final factor1.11765 correctly targets190px from170px mean idle height, with candidate pivot[140,224.5]; the old factor was not carried over. Inspected regenerated overview06 and all20-frame96/192 proofs. The body has suitable larger-than-reference mass, raised-foot movement/complete mace/prone pose remain readable, ground matches, and no new clipping/overgrowth blocker was found. This is a private preview binding only, not owner selection/runtime approval. All56 hashes/counts were checked again after regeneration.

2. **0156 preview registration corrected; effect envelope caution remains.** Regenerated20-frame192px proof uses fixed manual row roots[202,222,202,212,197] with the same factor1.60714 for every frame. Boots and down-body contact now sit close to the shared floor; the prior movement-row sink is resolved in this preview. The roots are explicit action origins, not automatic per-frame bbox fit; movement flame trail is excluded from boot placement. Source hash remains `a78a94ca0637ee421a946f8cb5cd800bf8162f2cf0bee90aa6f1b414027ce86c`. This corrects the private projection only: runtime art registration has not been fixed or activated by this result. R3F3 and especially R4F3 still have flame/stone envelopes substantially larger than the body; the generously padded preview preserves them, but cannot demonstrate1v3 neighbor/UI clearance. Keep the readable body proposal for scene trial rather than shrinking it to fit the aura; commission a bounded effect/composition repair only if actual overlap fails.

3. **0088 comparative profile corrected in preview.** Regenerated overview03 and all20-frame192px proof use factor1.18412, targeting164px silhouette height and170.51px width. The crouched wolf now has appropriate mass beside the enlarged profiles while keeping its hunched body, muzzle, limbs and flame mane/tail. Skill envelope remains compact relative to the larger body; final down pose remains readable. No overgrowth or source-detail blocker found. Source hash remains `624102b87329b0e683609154ae847d793e1ededdfbb4cb1d437e4f22c6bb4889`. This is still an owner-comparison preview rather than an approved runtime scale.

No other concrete scale correction is compelled by these isolated comparisons. Larger dragon/golem/Special profiles such as0052/0145/0159 appear intentional rather than unacceptable overgrowth at the shared reference magnification. They still require actual battle-layout tests; a large isolated canvas does not prove fit.

## Five uncertain source cases

| ID | Proposal | Static result at96/192 | Remaining limitation |
| --- | --- | --- | --- |
|0015|1.73494×|Cyan skull, dark robe and red scythe are distinct across idle, glide, attack, skill and down. Thin ghost anatomy remains thinner than the flower-reference silhouette; that is appropriate.|Raised scythe contributes much of180px height. Inspect actual body/movement against dark maps; do not inflate further solely to match a bbox. No detail redraw established.|
|0069|1.79487×|Face, silver hair, horns, red sword and grey wings are identifiable; flight opens the wings without per-frame fit pumping. Compact skill remains clear.|Facial expression is still a small cluster at96px. Actual camera/background determines whether this matters; the source does not need automatic redraw.|
|0051|1.54982×|Horns, dark head/body, red membrane wings, tail, breath and down silhouette are readable on this slate background. Dragon has greater length/mass than the reference.|Dark-map contrast remains untested. Static slate preview cannot certify darkest-world readability.|
|0126|1.49573×|Human face/crown, red torso/abdomen and purple spider legs are distinct in all20; hand/skill effects remain compact. Source enlargement is viable.|Face occupies less of total silhouette than legs/hair/abdomen; actual world camera still needs a face/body check.|
|0156|1.60714×|Head/helmet, blade, arms/legs remain recognizable; larger display improves identity at96px. Bright fire remains a deliberate dominant motif.|Wide impact/skill FX still require actual scene checks. Fixed manual row roots now align preview contact; scaling cannot change internal body-to-fire contrast.|

0087 supports the anatomy exception: its lower117px proposed silhouette and190px length read as a substantial four-legged tiger rather than a tiny humanoid. All20 retain stripes, collar, leg poses and attack/skill readability.0017 at215px width gives a clear larger skeletal dragon; skull/ribs/wings/red core remain distinct through flight/attack/down, and large wing poses are preserved. Neither demonstrates a need for new detail simply because the original height is low.

## Boundary of the result

These are isolated source/candidate projections with a common synthetic floor/camera and fixed96/192 display magnifications. They establish comparative scale and source-detail viability more strongly than the earlier source-only triage, but are **not actual gameplay captures**. Player comparison, real world and battle cameras, narrow UI/1v3 layout, foreground/target occlusion, live animation timing, zoom/filter behavior and texture budget remain unverified. No source artwork/approval/selection or runtime configuration is changed by this review.

Only this review Markdown was saved. Owner retains final aesthetic acceptance and a later source hash/proposal regeneration needs the stated delta checks.
