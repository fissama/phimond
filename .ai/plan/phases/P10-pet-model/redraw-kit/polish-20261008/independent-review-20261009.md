# Independent whole-package art review — 2026-10-09

**Disposition: 39 visual passes, 8 failures, 1 anatomy decision unresolved. This package is not 48/48 QA passed.**

This is one fresh independent visual review of the exact 48 manifest candidates. It covers art only: no runtime activation, owner approval, server validation, progress/result updates, or asset edits were performed. The manifest described 46 selected/lead-reviewed images plus two pending drafts (species_0019 attempt-02 and species_0086 attempt-04). All 48 files matched their manifest SHA-256 at the frozen snapshot. Subsequent replacements require their own exact-hash review; this report does not approve them automatically.

## Evidence and method

- Read AGENTS.md, RTK.md, implementation-plan.md and owner-art-direction-20261009.md, with later owner corrections taking precedence.
- Inspected all 48 original APK portraits alongside all 20 selected packed poses. Generated 48 QA panels using only nearest-neighbor resampling and layout; original assets were not changed. Panels show all poses on a pale background and Cast at each manifest's actual trial factor on a dark background.
- Inspected native raw-review sheets where ambiguity warranted it: 0146, 0148, 0145, 0088, 0018; inspected 0152 raw-composite. Inspected enlarged Move strips for 0146, 0019, 0145, 0147, 0088, 0016, 0067, 0086 and 0138. Inspected enlarged original sprites for0018 after the weapon discrepancy arose.
- Temporary evidence: `/tmp/p10-independent-audit/`, including frozen manifest-snapshot.json, 48 species panels, and nine move-ID.png strips. Stable exact paths/hashes and judgments are also retained in the adjacent independent-review-20261009.json.
- Frame references use R1 Idle, R2 Move, R3 Attack, R4 Cast, R5 Hurt/Down; C1–C4 are temporal order. All48 had visibly lying/collapsed final Down images.
- **Limits:** this review inspected ordered frames rather than independently playing every loop in a browser. It does not certify playback timing, all raw source-cell gutters, exact alpha geometry, or runtime UI collisions. A visual pass means no important art blocker found in these inspected views; it is not a replacement for the other plan gates. Original full sprites were not inspected for every species; the original portrait and latest explicit owner anatomy contract were the reference for most entries.

## Important blockers

| ID | Exact candidate | Blocker | Required correction |
|---|---|---|---|
| 0146 | cohesive/attempt-02 | R2 keeps image-left/front support; rear foot flexes/lifts without a clear opposite stepping phase. | Redraw opposite lead/support phase while retaining identity and weapon. |
| 0019 | cohesive/attempt-02, pending draft | R2 keeps same leading leg through all four frames. | Complete alternating walk; this report does not cover newer drafts. |
| 0152 | identity-correction | R4C4 has the widest bilateral gold arcs and sparkles, following an earlier release. There is no diminishing final phase. | Replace C4 with visibly reduced residual FX. |
| 0148 | cohesive/attempt-02 | Raw and battle-size R4 only change pose; Cast has no readable magical charge/release/decay. | Add compact thematic FX at64px without covering the face. |
| 0088 | cohesive/attempt-01 | R2C1/C3 repeat lead contact; C2/C4 lift the same front leg while rear foot remains back/planted. | Add opposite foot stride/support. |
| 0016 | cohesive/attempt-02 | Same leading side all four Move frames; only that forward toe lifts in C3. | Add unmistakable opposite leading phase. |
| 0086 | cohesive/attempt-04, pending draft | C1/C3 extend same leg; C2/C4 return toward same support. | Add opposite foot step with a readable contact phase. |
| 0138 | cohesive/attempt-01 | Same large leg leads all four Move frames; opposite leg stays rear support. | Add opposite lead/support instead of only body bob and toe-angle variation. |

The gait findings concern readable opposing phases, not byte uniqueness. A static strip cannot prove timing, but timing cannot create a missing opposite stepping drawing. The author should verify corrected Move loops at actual size before counting them.

## Unresolved anatomy decision

**species_0018:** the selected sheet intentionally has empty claw hands. The implementation plan explicitly requests one axe throughout, and the enlarged original sprites contain a grey blade/brown-shaft object. No trusted owner supersession is recorded. Parent confirmed it has asked the owner. Weapon/anatomy acceptance is unresolved; do not invent an axe interpretation or count this candidate accepted before that answer. The rest of the sheet was visually reviewed.

## Size and minor observations

- **0087 has the strongest size concern:** actual idle height39.49px versus nominal64px (61.7%). The white tiger silhouette, gold shoulder armor and cyan Cast remain readable, so this is not an automatic art failure. Its reduced presence must be judged in the complete battle composition with early-tier comparison; geometry pass alone cannot approve the size-A intention.
- **0017 and0124** are also substantially reduced (51.91/74px and49.74/74px). Their wide skeletal/mandible silhouettes and high-contrast face features remain identifiable in the inspected trial. Keep this explicit when reviewing final battle presence; do not describe them as actually74px tall.
- **0145 Cast** reads as materializing/spanning/disappearing green vines, but its effect is less emphatic than neighboring species. A small clear core or stronger edge would improve readability; this is a minor preference, not a required whole-sheet redraw.
- Small face/crown details on the slimmer humanoids necessarily simplify at trial size. I found their head direction and defining expression readable, and did not reject them merely for losing raw-scale ornament detail.

## Per-candidate exact-hash judgments

“Pass” below is the scoped visual result defined above. Every entry identifies the reviewed bytes, including failed/pending drafts. Atlas paths are relative to the repository root.


### 01. species_0146 — Ma Vương Hút Máu — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0146/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `2b26d696cef97cc2326e0657421b2e2cdc10883cefe8b35fcac7b6d9f997ebec`.
- Actual trial idle height: 77.47px; nominal 82px.
- Visual evidence: Important: Move R2C1–C4 never gives a clear opposite stepping phase: the image-left/front foot remains the support while the rear foot flexes/lifts. Rebuild the four-pose gait with visible alternating foot support. Horned teal face, jaw, attached wings/tail and cleaver remain coherent; red mouth-core/ring/bolts/motes Cast reads at 77.47 px.


### 02. species_0037 — Độc Đằng Nữ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0037/cohesive-20261009/attempt-05/packed.png` (selected).
- SHA-256: `1d6033147a727270b8b76cb299e6b7f110be551988adc2e690fa4b4fd486cd6e`.
- Actual trial idle height: 65.29px; nominal 74px.
- Visual evidence: Compact botanical face, two round gold buns with pink blossoms and no hanging hair tails. Two leafy hands stay separate from thorn vines; dominant flower base has no feet. Sliding Move, vine lash, and bright pink core/ring/shards/decay are legible at 65.29 px. Flower remains layered in Down.


### 03. species_0150 — Đảo Thiên Đường — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0150/packed-v2.png` (selected).
- SHA-256: `4e4ed7a3c2b1d7a9679dea43a3045880082c5b27c5d3c74b9e8172ff8401cad2`.
- Actual trial idle height: 82.00px; nominal 82px.
- Visual evidence: Original red/gold face and chest, purple crest, blue wings/tail preserved. Beak/eye and talons remain clear; Move visibly changes wing stroke. Cast builds gold light, releases fan shapes, then leaves sparse fragments. Last two Down poses lie flat.


### 04. species_0142 — Thần Tướng Cự Ma — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0142/attempt-02/packed-v2.png` (selected).
- SHA-256: `9d357ca18f8e03a4d06ae5cf483ffef03bfde4ed50225e0a7d9dc4dc88f23b54`.
- Actual trial idle height: 72.30px; nominal 82px.
- Visual evidence: Original small recessed head opening, large grey segmented armor, asymmetrical gold shield and red spirit tail preserved. Fists attach through punch; shield persists in Cast/Down. Hover/glide fits tail body. Red fist core, release and residual fragments read at 72.30 px.


### 05. species_0020 — Thủ Lĩnh Hắc Ám — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0020/identity-correction-20261008/packed.png` (selected).
- SHA-256: `d8bf9beb416916a6f88479b6db2bc9d8d43800d7491ceb7b248dce21224734fb`.
- Actual trial idle height: 66.98px; nominal 82px.
- Visual evidence: Separate armored rider sits visibly on a four-legged horse; no centaur fusion. Rider helmet, horse muzzle, reins/body armor and sword maintain identity. Horse legs articulate; sword lift/thrust stays attached. Cyan weapon charge, crescent release and sparse decay remain legible at 66.98 px.


### 06. species_0126 — Trùng Mẫu Mào Vàng — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0126/identity-correction-20261008/packed.png` (selected).
- SHA-256: `fa39f2b59f01092c506b0e7ee61944919255cfebc83840fe90c6e62a1e589f47`.
- Actual trial idle height: 77.44px; nominal 82px.
- Visual evidence: Adult woman torso/face and gold crown stay separate from red abdomen and articulated purple spider legs; overlapping rear legs are naturally occluded, not replaced by humanoid feet. Two upper arms remain readable through thrust and Cast. Orange palm charge/ring/projectile/decay reads at 77.44 px.


### 07. species_0019 — Nữ Đế Minh Giới — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0019/cohesive-20261009/attempt-02/packed.png` (pending draft).
- SHA-256: `3f53168406d95d81d208e3a1ea0ae5ff7e0b0f7630936aa00cdf80cc67e65d62`.
- Actual trial idle height: 82.00px; nominal 82px.
- Visual evidence: Draft, not selected: Move R2C1–C4 retains the same image-left leading leg and never visibly swaps the step. Face, horns, red hair, staff and cape are otherwise coherent; staff orb/ring/red shard/decay sequence reads at 82 px. This judgment covers attempt-02 only.


### 08. species_0151 — Đại Vương Bọ Cạp — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0151/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `a3b30734203361a352865e492899359f7b525a2cbc5a67d1db76a4652ebd5281`.
- Actual trial idle height: 80.09px; nominal 82px.
- Visual evidence: Adult muscular purple male upper torso with two pincer arms, articulated scorpion lower body and one curved tail/stinger. Clear brow/jaw avoids child mascot proportions. Pincers connect through attacks; purple charge/release/fragments read at 80.09 px, ending in fully collapsed Down.


### 09. species_0149 — Thú Vàng Một Sừng — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0149/identity-correction-20261009/packed.png` (selected).
- SHA-256: `f2ad4006980986019af191a7895e0cf06395bed83a37863af4c166b8a82e0613`.
- Actual trial idle height: 70.62px; nominal 82px.
- Visual evidence: Proud cream/gold unicorn with orange mane/tail, one attached horn and no invented armor. Face/muzzle remain distinct from mane and four legs articulate through Move. Horn glow grows into a small ring and short emission before sparse decay; visible at 70.62 px, though subtler than most Casters.


### 10. species_0152 — Chim Ái Thần — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0152/identity-correction-20261009/packed.png` (selected).
- SHA-256: `2a3c87cf9af49f781b830a72a17eba3d71e680a653bcc840a84f3f247b99161d`.
- Actual trial idle height: 66.13px; nominal 82px.
- Visual evidence: Important: Cast R4C4 expands into the widest bilateral gold arcs and sparkles after C3; it is another release/peak, not decay. Replace the final Cast image with a visibly diminished residual effect. Feminine face, hands, purple feather wings and wing-beat Move otherwise preserve original identity. Confirmed in raw-composite and actual 66.13 px trial.


### 11. species_0145 — Cây Cự Linh — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0145/proportion-fix-20261009/attempt-02/packed.png` (selected).
- SHA-256: `cdea5c254e5074541d3942443124b1fcb1b6196a5141d1a82c6a78d7589bbd07`.
- Actual trial idle height: 74.13px; nominal 82px.
- Visual evidence: Weathered log face with yellow eyes, two massive banded wooden arms and two lower supports remain distinct; Move includes opposite-foot support configurations. Punches preserve cylindrical arm construction. Green vines materialize/wrap/span the arms and disappear in C4, providing a charge/release/decay reading. Minor: the 74.13 px Cast is less emphatic than neighboring species and would benefit from a clearer small core or brighter vine edge.


### 12. species_0143 — Thần Đèn — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0143/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `ee960bc6331965b69c4b0457ed59877064b77764faff0fc5c0695c942cab7fdd`.
- Actual trial idle height: 82.00px; nominal 82px.
- Visual evidence: Blue round genie face, two muscular arms, orange spirit lower body and one gold lamp stay coherent. Hover motion and fist thrust suit anatomy. Cyan hand charge grows, lifts into a flame-like release, then disappears; expression stays visible at 82 px. Lamp persists through Down.


### 13. species_0144 — Linh Tiên Hoa Hương — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0144/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `42b663529b304ab584f61e3819c709f491dbc4cb1cd459666686f2c94625ea45`.
- Actual trial idle height: 82.00px; nominal 82px.
- Visual evidence: Warm yellow face is distinct within pink petals; leaf torso and purple flower base preserve original silhouette. Petal sway/glide and hand gestures are coherent. Chest glow develops into a bright flower and green-pink released motes, then clears. Down folds the whole plant sideways.


### 14. species_0148 — Ngựa Bùn Cỏ — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0148/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `5fcea0d7fe9ffad0bf6d9713a494516da0ed41ad619f6cf68277c60707e3860f`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Important: Cast R4C1–C4 only tilts the head and shifts the body; no distinct charge, release or decay effect exists in the raw sheet or at the approved 64 px cute-body exception. Add a compact thematic magical sequence. Orange wool, small face, blue saddle ornament, four legs and lying Down are otherwise coherent.


### 15. species_0052 — Thánh Rồng Thái Cổ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0052/cohesive-20261009/attempt-03/packed.png` (selected).
- SHA-256: `2a98e32f403563c3e5dad300ae99e6a78522203f84bf52ac1d0be78c85137e9e`.
- Actual trial idle height: 74.00px; nominal 74px.
- Visual evidence: Adult orange dragon with defined muzzle/jaw, pale horns/chest, attached wings and tail. Wing up/down/spread poses produce flight; limbs stay attached. Mouth charge increases before release and dwindles to small motes. At 74 px face and claws remain readable; Down is flat.


### 16. species_0069 — Trụy Thiên Sứ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0069/cohesive-20261009/attempt-06/packed.png` (selected).
- SHA-256: `bf12fca5f13b3e433b8b1546fd552bca7ae1af4a06adb520c4a6dd396559073c`.
- Actual trial idle height: 65.64px; nominal 74px.
- Visual evidence: Sharp adult pale face, dark armor, red sword and layered grey wings remain distinct. Move has real wing articulation; sword follows the hand through attack and remains in Down. Red core/rune/three shards/decay reads at 65.64 px without obscuring face.


### 17. species_0017 — Rồng Xương Băng — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0017/quadruped-20261009/attempt-02/packed.png` (selected).
- SHA-256: `4b38aa656023f6211adf2e7361dba15281acae47d2502dfdf0979884384ffce6`.
- Actual trial idle height: 51.91px; nominal 74px.
- Visual evidence: Four-legged elongated undead dragon, ivory skeletal structure, brown membrane wings and red core inside the ribcage. Wing up/down/spread/lift poses articulate attached wings; no held core. Red chest charge/mouth emission/decay remains readable. Width cap reduces idle height to 51.91 px: broad silhouette and high-contrast skull/ribs still identify it; see size caveat.


### 18. species_0124 — Trùng Bất Tử Địa Huyệt — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0124/cohesive-20261009/attempt-03/packed.png` (selected).
- SHA-256: `c21af4a87b11d61483d6714fdb61855d95f9d1f1aeda23909f2d78dba2b3ff6c`.
- Actual trial idle height: 49.74px; nominal 74px.
- Visual evidence: Segmented dark insect with large separate curved mandibles, blue functional wings and green carapace. Wing stroke is clear; mandibles open for physical contact. Green mouth charge/arc/decay reads at actual 49.74 px. Broad silhouette remains distinct despite substantial height cap; see size caveat.


### 19. species_0125 — Nhện Phu Nhân — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0125/soft-humanoid-20261009/attempt-02/packed.png` (selected).
- SHA-256: `2703cadc60ee1928eb7cb65e027ce786f075eb025459016a26015f57c90956c6`.
- Actual trial idle height: 74.00px; nominal 74px.
- Visual evidence: Soft adult feminine face, long sensory antennae, insect-derived green body/joints and blue-green butterfly wings. Does not become an armored insect mask. Wing Move has distinct up/down/spread poses. Cyan butterfly charge/release/residual motif remains clear at 74 px and avoids covering the face.


### 20. species_0141 — Totem Thượng Cổ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0141/slab-20261009/attempt-02/packed.png` (selected).
- SHA-256: `06b9f556cd2574059edd497fb42aafc51f22bb656f955e94466589af5413b3e1`.
- Actual trial idle height: 74.00px; nominal 74px.
- Visual evidence: One weathered brown carved slab, two attached arms/fists and no legs. Grave face and restrained turquoise details suit spiritual identity. Move tilts/glides, and punch extends a jointed arm. Cyan/gold seal/shards/decay reads at 74 px; slab falls sideways in Down.


### 21. species_0147 — Người Tuyết Viễn Cổ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0147/cohesive-20261009/attempt-07/packed.png` (selected).
- SHA-256: `d296b1a816b0dd1a2fc3073e1bd904be1d8f2bcd82be5d1506db0b7e13910e80`.
- Actual trial idle height: 60.88px; nominal 74px.
- Visual evidence: Heavy white fur, visible eyes/brow and tusks, two legs and two arms. Brown shaft with pale pointed club head remains naturally gripped through overhead swing and Down; no axe conversion. Move shows lifted feet/opposite supports. Cyan club charge/ring/ice shards/decay reads at 60.88 px.


### 22. species_0018 — Nữ Vương Bạch Cốt — UNREVIEWED

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0018/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `9d1d2f4fbe5420d2b2f2d90885c18540befc420fbc18b88c5b803a915892cf53`.
- Actual trial idle height: 67.18px; nominal 74px.
- Visual evidence: Anatomy acceptance unresolved: selected sheet has two empty claw hands, while implementation-plan demands one axe and enlarged original sprites include an axe-like grey blade/brown shaft. Parent confirms no trusted owner supersession and has asked the owner. Face/crown/robe/wings, flight, claw attack and cyan seal/bone-shards/decay were visually reviewed, but weapon/anatomy compliance cannot pass pending the answer. Do not count this as QA accepted.


### 23. species_0038 — Tinh Linh Bách Hoa — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0038/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `49a501324edad9b6a744b804efa4abf09657fb1280d37c059df84f837a9e9931`.
- Actual trial idle height: 67.22px; nominal 74px.
- Visual evidence: Pink botanical hair/face, small blue wings, green-held staff and two legs retain fairy identity. Wing stroke changes through Move, staff stays in grip through thrust and Down. Pink flowers build beside hand, release left and decay into petals; clear at 67.22 px.


### 24. species_0088 — Sói Xích Viêm — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0088/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `624102b87329b0e683609154ae847d793e1ededdfbb4cb1d437e4f22c6bb4889`.
- Actual trial idle height: 67.79px; nominal 74px.
- Visual evidence: Important: Move R2C1/C3 repeat the same lead-foot contact and R2C2/C4 lift the same image-left/front leg; rear foot remains the planted rear support. No opposite lead-foot phase is shown. Rebuild alternating gait. Red wolf muzzle/teeth, horn, flame mane/tail, attached claws and bright fire charge/ring/bolts/embers otherwise read well.


### 25. species_0106 — Chim Cú Địa Ngục — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0106/cohesive-20261009/attempt-04/packed.png` (selected).
- SHA-256: `977237ecdca2f6a5e32d3f3859b09969f8885b8683fe41288039c1f8484d8196`.
- Actual trial idle height: 65.13px; nominal 74px.
- Visual evidence: Brown beast/demon head with green elongated muzzle and glowing eyes, wing-like ears, four long slender taloned legs, and attached blue flight wings. Move changes wing stroke and tucks all legs coherently. Green core/crescent release/decay is visible; no round owl-beak interpretation.


### 26. species_0107 — Đại Bàng Vàng — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0107/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `74948ef8d365131cc29584139528699898346c9061cd540f99604bf391642b55`.
- Actual trial idle height: 74.00px; nominal 74px.
- Visual evidence: Orange/gold bird head, white-purple chest/wings, talons and orange tail preserve source. Wing stroke and talon reach are functional. Mouth gold charge/ring/feather-like shards/decay is readable at 74 px; lowered and lying Down poses remain complete.


### 27. species_0140 — Nhân Sư — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0140/cohesive-20261009/attempt-05/packed.png` (selected).
- SHA-256: `7ba46f0ecf387643fa9cb6430c14be5e78d8f40269824e10145db7de6de0e485`.
- Actual trial idle height: 64.86px; nominal 74px.
- Visual evidence: Compact calm gold pharaonic mask, two striped nemes lappets and cobra crest. Fitted gold chest/waist armor follows four-legged lion body and leaves leg joints exposed. No fur mane or oversized humanoid shoulders. Paw action and ankh/core/shards/decay maintain attachments; face survives 64.86 px trial.


### 28. species_0068 — Thanh Long — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0068/cohesive-20261009/attempt-03/packed.png` (selected).
- SHA-256: `c96964ca10ba527343c0fbb8e3f9168054ccef426effd8ce594b44b66e3d22d8`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Long green Chinese dragon with four attached legs, paired horns and no wings. Move visibly undulates and uncoils rather than inventing wings. Eye/muzzle and pale belly remain separable. Green mouth core, burst, shards and sparse decay read at 64 px.


### 29. species_0087 — Bạch Hổ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0087/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `11cdde42a657672f1e2cc25c8a2dfab9236fb94abe86ca856b1e8cefd9554cfd`.
- Actual trial idle height: 39.49px; nominal 64px.
- Visual evidence: White tiger face, blue stripes, gold shoulder armor and waist band are preserved as metal fitted to a quadruped; no wings/mane reinterpretation. Paw reach and four-leg motion remain coherent. Cyan core/ring/crescents/decay stays readable. Strong size caveat: 39.49 px idle height is only 61.7% of nominal64; broad body remains recognizable, but presence target needs layout/owner review, not geometry-only approval.


### 30. species_0105 — Chu Tước — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0105/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `f098d17e59dc3fb53a1c11efd0ccc2233f2890a6fc73d122a32d4db2987105ce`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Orange-magenta phoenix with long decorative tail, attached feather wings and small talons. Face direction and wing stroke stay consistent. Bright pink/gold mouth charge/ring/three shards/decay is clear at 64 px. Down folds wings and tail together.


### 31. species_0139 — Huyền Vũ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0139/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `542adb26aac9b97f3b3897a3e94fcbf320bfd80b4512f7d8ec412e81f85fef1c`.
- Actual trial idle height: 57.14px; nominal 64px.
- Visual evidence: Dragon-turtle head/neck, golden shell, four red clawed legs and tail retain original proportions. Shell follows body through steps and bite. Green geometric core/seal/projectile/decay reads at57.14 px; flat Down preserves shell.


### 32. species_0015 — Tử Thần — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0015/cohesive-20261009/attempt-06/packed.png` (selected).
- SHA-256: `00a4128e4abb701413c0ca1fd7b20cc24a79e780d501bee4841690c68a0ee8a1`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Menacing skeletal face, fully covering dark cloak without feet, and a long red scythe blade with connected shaft/grip. Glide locomotion; sweep follows actual weapon movement. Blade-tip charge/rune/red emission/motes align spatially with the scythe. Down retains the complete weapon.


### 33. species_0035 — Trưởng Lão Người Cây — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0035/cohesive-20261009/attempt-03/timing-v2/packed.png` (selected).
- SHA-256: `636cb123b8146bca7ce652df15cc01e5b83b9bc487b9a59ea487b2dcbe86433c`.
- Actual trial idle height: 59.29px; nominal 64px.
- Visual evidence: Headless log torso with leafy crown; real head remains at image-left arm end and staff remains in image-right hand. Root-like feet articulate; staff rotates coherently through sweep. Green staff core/ring/leaves/shards/decay reads at59.29 px. Fallen head, arm and staff remain attached/readable.


### 34. species_0050 — Hải Long Ba Đầu — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0050/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `ec6eac8b88ff8488043eb7b97168db457d852a20ee5eb506d6dcc4e29c828fed`.
- Actual trial idle height: 60.89px; nominal 64px.
- Visual evidence: Three separate blue heads, two lateral fins and long aquatic tail; no arms or legs. Fin/tail motion provides locomotion, heads lunge for attack. Three mouth cores, three rings and three emissions read independently before decay. Down still retains all heads and fins.


### 35. species_0122 — Trùng Hốt Lỗ — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0122/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `ec9fe9bee29cfe94c0e0c4be82519fe1b2496e09434138e1bdbd9ab5870c96bf`.
- Actual trial idle height: 55.12px; nominal 64px.
- Visual evidence: Pink body, two legs, long tail and thin arms with large splayed pink frog-like hands; resting hands turn back/down. No mitten fists. Palm reach preserves long digits; cyan/pink charge/ring/shards/decay remains readable at55.12 px. Face and long antennae remain distinct.


### 36. species_0016 — Pharaon — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0016/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `8fcee2fce5ec8fc916a34d9d5c4c35c4c7a537a41f3f2e5a66e6baeb7d040a11`.
- Actual trial idle height: 56.88px; nominal 64px.
- Visual evidence: Important: Move retains the same leading leg across R2C1–C4; C3 lifts that same forward toe while the rear leg never reaches a clear opposite leading phase. Visible pixel changes do not establish a complete alternating walk. Restore opposite leg stride/support. Pharaonic mask/nemes, cobra, mummy limbs, staff and green charge/seal/shards/decay remain coherent.


### 37. species_0036 — Hoa ăn Thịt Người Ba Đầu — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0036/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `4cef30f40b6357b0013ff7ba83c675dc2f4309fbef6b132c4e8608f60f604463`.
- Actual trial idle height: 60.16px; nominal 64px.
- Visual evidence: Exactly three toothed plant heads on green stalks and rooted base remain readable through all actions. Root sliding/twisting and independent biting distinguish locomotion/attack. Green mouth cores/starbursts/three shards/decay remain visible at60.16 px; collapsed stalks preserve all heads.


### 38. species_0051 — Long Vương Hắc Ám — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0051/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `a5ae8708c31066f15098d3cb5832cfde94471e8bc7374dc5148d2768dd9308f0`.
- Actual trial idle height: 60.80px; nominal 64px.
- Visual evidence: Dark quadrupedal dragon, grey crest, red membrane wings and attached tail preserve source. Flight Move has articulated up/down/spread wings. Jaw opens for physical attack; red mouth core/ring/shards/decay reads at60.80 px. Low Down keeps limbs/wings complete.


### 39. species_0066 — Đại Ác Ma — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0066/cohesive-20261009/attempt-03/packed.png` (selected).
- SHA-256: `5b628144bd31a6befbb74ddd0cd68b1329f76c2e08231d1ab2fb718e27ea1bfc`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Purple demon face with grey horns, fitted gold armor, attached black tail and grey/red-edged wings. No fabricated held weapon. Wing flight and fist reach remain functional. Green hand core/emission and purple-green residual decay are visible at64 px.


### 40. species_0067 — Ma Vương Địa Ngục — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0067/cohesive-20261009/attempt-03/packed.png` (selected).
- SHA-256: `123adc21342dee84bca0321572f36c1bc87beab5ba85bfbfe837a45eff1a2e7a`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Red adult demon, gold curved shoulder armor, two empty hands, two armored legs and horns. Gold structure stays attached to shoulder throughout attack/Cast/Down. Move includes different foot supports; red-orange core/ring/shards/decay is visible. No weapon invention.


### 41. species_0084 — Tinh Tinh Rock — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0084/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `ed7b23fa9289a06fd4a4554f9b839a5aad761fdfcfa33c1db57c9246cc84b7ee`.
- Actual trial idle height: 55.15px; nominal 64px.
- Visual evidence: Blue gorilla with orange-brown crest and warm muzzle retains expressive brow/eyes. Two long knuckle-bearing arms and two hind legs articulate through locomotion and punch. Blue hand core/ring/bolts/decay reads at55.15 px; full lying Down is clear.


### 42. species_0085 — Đại Tuyết Quái — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0085/cohesive-20261009/attempt-02/packed.png` (selected).
- SHA-256: `731b161e5d1a5a61f9eb93224806e08579090f5e0591945e2bb4342dc7783c41`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Soft white ape/yeti with pink head flower, two long arms and two short legs. Calm mouth/eyes remain distinct from white fur; knuckle gait and broad arm strike preserve attachments. Cyan core/snowflake/shards/decay is readable at64 px. Flower remains through Down.


### 43. species_0086 — Gấu Trúc Ma Pháp — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0086/cohesive-20261009/attempt-04/packed.png` (pending draft).
- SHA-256: `f22d5148f02416025ed8cb4d0f14c0835245f6c42a988132128b2eb11eb58ac2`.
- Actual trial idle height: 57.79px; nominal 64px.
- Visual evidence: Draft, not selected: Move R2C1/C3 repeats the same extended image-left leg and R2C2/C4 returns toward the same support without a clear opposite step. Rebuild alternating foot phases. Purple/white panda face, bamboo grip/strike and green core/ring/shards/decay are otherwise coherent. Attempt-04 only.


### 44. species_0103 — Chim Đại Phì — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0103/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `b2afbcd23e17c87de176c665a486f15af00585726a3d725328fee26ff0477fcc`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Round orange bird, hooked beak, expressive green eye, white belly, small wings and two taloned feet preserve original. Ground locomotion uses feet, avoiding unsupported wing-flight claim. Peck and gold mouth charge/three projectiles/sparse decay remain clear at64 px. Rounded fallen body stays legible.


### 45. species_0104 — Chim Đa Đa — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0104/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `b6e4ac12edaebc096eea02a2aacea9f8b5f7b8ab5778f6e75b8e77aeda76b3cf`.
- Actual trial idle height: 63.40px; nominal 64px.
- Visual evidence: Orange-red bird with purple wing/tail accents, hooked beak and two taloned feet. Wing up/down/spread Move is distinct from talon attack. Pink-gold mouth core, angular charge, three emitted shards and sparse decay remain clear at63.40 px.


### 46. species_0123 — Trùng Gai Nhọn — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0123/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `7020654874adb6f2e0cad376bf28cd92a063cbbb68452dbf2f89e7ac32c5ed1a`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Spiked magenta insect head/body, articulated jaws and exactly four brown pointed walking legs. Cyan eye remains distinct; legs flex rather than becoming arms or six-legged anatomy. Pink mouth core/ring/shards/decay reads at64 px; collapsed Down retains four legs.


### 47. species_0137 — Ma Gương Thủy Tinh — PASS

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0137/cohesive-20261009/attempt-03/packed.png` (selected).
- SHA-256: `a7d91445cecdfaf269d386f561b855119fb228e1b4b0a3cef9ee1cd1208ee84a`.
- Actual trial idle height: 64.00px; nominal 64px.
- Visual evidence: Floating red mirror with gold frame dominates silhouette; small skull, delicate bone wings and two bone legs retain spiritual object identity. Hover/glide and restrained wing articulation avoid heavy walking. Mirror core/ring/red shards/decay read at64 px; no flesh torso, huge skull or weapon.


### 48. species_0138 — Thú Lớn Dung Nham — FAIL

- Candidate: `apps/game-client/assets/pets/redraws/polish-20261008/species_0138/cohesive-20261009/attempt-01/packed.png` (selected).
- SHA-256: `25b0741369caea0f2c8fe547068fc31359297f38641bc18ff8881ed36ba9e3a8`.
- Actual trial idle height: 57.75px; nominal 64px.
- Visual evidence: Important: Move R2C1–C4 keeps the same large leading leg in front, with only its extension/toe angle and body bob changing; opposite leg remains rear support. Add a visible opposite stepping phase. Rock face/eyes, glowing seams, two fists and two legs otherwise remain coherent; orange hand core/shards/embers Cast is readable at57.75 px.


## Handoff to author

Resolve the eight listed failures and the0018 anatomy decision, preserving versioned rejected candidates. Review any replacement by its new SHA. Complete outstanding playback/raw/geometry/battle-layout gates separately. These findings do not authorize runtime routing or owner approval. This report deliberately does not overwrite result.json or progress counters.
