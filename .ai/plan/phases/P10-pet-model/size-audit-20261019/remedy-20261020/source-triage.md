# Read-only source triage — next 29 size-remedy species

Status: source triage only; no candidate, approval, runtime parameter or source pixel changed. Excludes species_0138/0141/0147, which the lead is handling separately.

**Result: 24 scale-first candidates; 5 scale-first with unresolved visibility questions. No source in this set has been demonstrated to require a detail redraw merely because it is short.** This does not mean 29 runtime scale-only remedies are accepted or complete.

## Evidence and the transparency trap

All 29 approved source paths were taken from `remedy-20261020/progress.json`, cross-referenced with frozen `measurements.json`. All 29 actual SHA-256 values match the frozen before hashes. The ledger below records the exact inspected paths/hashes.

Inspected all source atlases with native 281px cells. Native PNG viewing misleadingly exposed colored rectangular panels and colored fringes from hidden RGB. Actual-alpha compositing corrected this: composed every atlas over #202936, reviewed all 20 frames in an overview, reviewed first-idle native composites for a subset and first-idle 192px composites for all 29. **No visible rectangular background haze was established in actual-alpha compositions.** For example, species_0068 cell pixel(90,90) has RGB(14,15,5), alpha0; species_0037 has RGB(37,21,8), alpha0. The apparent rectangle at such pixels cannot appear under ordinary alpha blending. Red/blue fringes in several raw previews also largely vanish when alpha is respected. Hidden RGB is not by itself authorization to erase or redraw source art.

Also inspected ephemeral equal-96px first-idle current/enlarged nearest-neighbor previews for every species. These images were generated in memory only and are not persisted because this task authorizes only this Markdown output. They are visual triage, not a live-game test or 20-frame candidate validation. Full atlas effect/clipping/pivot/camera/UI checks remain mandatory before disposition.

The illustrative factor is 155/idle-height for most species, or 180/idle-width for seven broad quadruped/cavalry/insect profiles, capped at2.0. It is a **preview**, not a recommended approved runtime value; it can count horns/weapons/FX and therefore requires body-specific refinement. Same hypothetical factor would apply to all 20 frames. Preview canvas used source pivot(140,210) mapped to (48,72) at cell96.

## Per-species classification

`S` = source detail plausibly sufficient: try runtime/display sizing before commissioning redraw. `U` = same first step, but a specific visibility concern remains unresolved; only actual body/scene evidence can establish whether authored repair is needed. All dimensions below are mean idle opaque bbox H×W, not pure anatomy measurements. `Fit cap` is the existing audit all-alpha union uniform repack upper bound, not a display-scale limit.

| Species | H×W px | Preview factor | Fit cap | Class | Concrete source assessment |
| --- | --- | --- | --- | --- | --- |
| species_0068 — Thanh Long | 79.25×80.5 | 1.96× | 1.0822× | S | Coiled dragon has clear jaw, gold horns, belly and teal scale clusters. Current small body is largely unused cell area, not missing identity. Long raised-body/effect extents constrain repack; trial scene presence first. |
| species_0037 — Độc Đằng Nữ | 81.5×85.5 | 1.90× | 1.3779× | S | Face, paired flower ornaments, green bodice, pink flower skirt and separate vines read at native size; enlarged preview keeps them recognizable. Preserve young/chibi anatomy rather than making an adult figure. |
| species_0086 — Gấu Trúc Ma Pháp | 89.0×95.0 | 1.74× | 1.2811× | S | Large white face/belly, purple fur and green bamboo have simple strong clusters. The enlarged preview remains crisp; no authored detail deficit established. |
| species_0087 — Bạch Hổ | 90.25×146.5 | 1.23× | 1.0628× | S | 90px height is appropriate to a 146.5px-long quadruped. Stripes, muzzle, four-leg poses and gold collar are already detailed; increase body length/presence modestly, do not force humanoid height. |
| species_0139 — Huyền Vũ | 91.5×115.0 | 1.57× | 1.1023× | S | Low turtle/dragon anatomy is intentional. Gold shell, long neck, horns and four feet remain distinct. Assess shell/body mass and length separately from horns; source detail supports a larger display. |
| species_0084 — Tinh Tinh Rock | 94.75×94.0 | 1.64× | 1.2811× | S | Simple blue-fur body, orange hands/feet and readable face survive enlargement well. Low knuckle-walking posture should remain; no need to invent texture for size. |
| species_0124 — Trùng Bất Tử Địa Huyệt | 96.0×141.5 | 1.27× | 1.0260× | S | Broad mandibles, green carapace and blue wings are already clear. Horizontal insect length, not human-height comparison, is the relevant trial. Wide wing poses leave almost no atlas repack headroom. |
| species_0017 — Rồng Xương Băng | 96.25×125.25 | 1.44× | 1.0349× | S | Ribs, skull, wing membranes and red chest core are resolved at native scale; larger preview preserves them. Judge total dragon mass/length, not just standing height. Raised flight wings constrain cell repack. |
| species_0154 — Thiết Giáp Long | 96.5×131.0 | 1.37× | 1.1023× | S | Approved Phimond-authored armored quadruped has strong plate edges, horn, claws and tail mace. Body is intentionally low. Runtime-scale trial first; large tail/fire arcs limit repack. Do not replace approved design for low height. |
| species_0069 — Trụy Thiên Sứ | 97.5×86.5 | 1.59× | 1.2216× | U | Silver hair, horns, sword, feathered wings and red-black costume read, but face is only a small cluster and dark body can merge at 96px. Scale-first is plausible; decide authored facial/body detail only after actual scene contrast and camera checks. |
| species_0067 — Ma Vương Địa Ngục | 100.0×68.0 | 1.55× | 1.4812× | S | Gold shoulder armor, red musculature, horns and skirt are readable. Uniform enlargement improves presence without changing identity. One of the better repack headroom cases, although target 155px exceeds current all-alpha upper bound. |
| species_0085 — Đại Tuyết Quái | 101.75×94.5 | 1.52× | 1.2540× | S | White fur mass, friendly face, toes and pink head flower read clearly; broad arms survive the scale trial. Keep approved gentle face/chibi shape; cutesy anatomy is not a defect requiring redesign. |
| species_0015 — Tử Thần | 103.75×94.5 | 1.49× | 1.2408× | U | Cyan skull, red scythe and dark shredded robe are identifiable, but 103.75px includes the raised weapon while the actual body is smaller. Scythe-based target alone underestimates body need; trial body readability against dark maps before deciding detail redraw. |
| species_0107 — Đại Bàng Vàng | 104.0×113.5 | 1.49× | 1.1850× | S | Orange beak/head/tail and pale blue-white feathers are already distinct. Scale preview retains the head and claws. Check body mass independently of open wing/long tail; not automatically a redraw. |
| species_0137 — Ma Gương Thủy Tinh | 104.5×93.0 | 1.48× | 1.4277× | S | Red mirror plane, gold rim, skull and thin bone appendages are clear. Simple body design scales cleanly; sparse skeletal anatomy is intentional. Check rim/skull on light and dark map backgrounds. |
| species_0156 — Đao Ma Huyết Giáp | 112.0×131.5 | 1.38× | 1.0042× | U | Approved Phimond-authored armor/large blade remain recognizable, but bright fire covers much of the small dark torso. Enlargement cannot by itself improve body-to-FX contrast. Trial scale, body mask and battle camera before deciding a narrowly scoped authored clarity repair. |
| species_0051 — Long Vương Hắc Ám | 113.25×135.5 | 1.37× | 1.0085× | U | Dragon head, silver horns, red wing membrane and dark scales are resolved; the dark torso remains low contrast. Trial size and map contrast first. No visible rectangle after actual-alpha composition; do not redraw for the misleading raw preview panel. |
| species_0122 — Trùng Hốt Lỗ | 114.25×104.5 | 1.36× | 1.0487× | S | Simple pink creature, yellow segmented belly, bright eye and tipped antenna read cleanly when enlarged. Horizontal tail/arms extend the atlas; scale trial preserves approved anatomy without additional fine detail. |
| species_0145 — Cây Cự Linh | 116.25×135.25 | 1.33× | 1.0872× | S | Tree face, leaf beard, stump crown, metal-banded arms and stone feet are already detailed. Broader/larger creature display is justified; no evidence that extra texture is required. Native face remains readable in the enlarged preview. |
| species_0126 — Trùng Mẫu Mào Vàng | 117.0×105.0 | 1.32× | 1.0441× | U | Face, gold crown, purple hair and spider abdomen/legs are identifiable, but human face/torso occupy a small fraction of overall silhouette. Scale-first preview is promising; final decision must inspect face/body separately from legs, hair and red abdomen. |
| species_0016 — Pharaon | 118.5×84.0 | 1.31× | 1.0260× | S | Gold/orange striped headcloth, blue mask, wrapped limbs and skull staff read well. Slender humanoid proportions are intentional. Uniform larger display is the first remedy; do not broaden/redesign anatomy. |
| species_0038 — Tinh Linh Bách Hoa | 120.0×110.0 | 1.29× | 1.0676× | S | Face, pink hair, green wand and pale wings remain distinct and benefit from modest enlargement. Wings/hair are not body height; do not add effects to satisfy the numeric target. |
| species_0140 — Nhân Sư | 122.75×132.0 | 1.36× | 1.0773× | S | Gold/purple armor, blue eye, human head, paws and flame-tipped tail are resolved. Treat as a wide quadruped; length/body mass is more useful than matching humanoid height. |
| species_0148 — Ngựa Bùn Cỏ | 123.75×94.5 | 1.25× | 1.0487× | S | Chibi long neck, expressive face, curled orange wool, blue saddle/bag and feet have strong clusters. Modest scale trial preserves identity; low/compact proportions do not establish a detail deficit. |
| species_0106 — Chim Cú Địa Ngục | 125.25×134.0 | 1.24× | 1.0487× | S | Green face/muzzle, brown torso and blue membrane wings are readable at native size and enlarged preview. Existing winged creature design must remain even though species name says owl; no redesign inferred from the name. |
| species_0035 — Trưởng Lão Người Cây | 126.0×121.5 | 1.23× | 1.0872× | S | Bark face/beard, leaves, roots and separate branch staff are already detailed. Modest enlargement improves presence; branch/staff height should not stand in for body mass. |
| species_0036 — Hoa ăn Thịt Người Ba Đầu | 127.25×127.5 | 1.22× | 1.0822× | S | All three distinct mouths/teeth, stems and root base remain readable. Broad plant anatomy does not need humanoid height. Modest display enlargement first; preserve three heads and existing expression/pose differences. |
| species_0103 — Chim Đại Phì | 127.75×128.0 | 1.21× | 1.0922× | S | Large green eye, beak, layered orange feathers, white breast and feet are well resolved. Source is already round and readable; a modest display increase is sufficient to trial. Raw amber panel is hidden RGB, not a visible background. |
| species_0020 — Thủ Lĩnh Hắc Ám | 128.75×147.0 | 1.22× | 1.0724× | S | Horse, rider, cloak and bright blue blade/gold armor retain distinct clusters. Total cavalry silhouette matters more than rider height. Existing detail supports a modest larger display; scene trial must include weapon/effect clearance. |

## What this means for implementation

Start each remaining species with a reversible preview using the existing approved atlas and a common display scale. Do not interpret an all-alpha atlas fit cap near1.0 as evidence of poor source detail: faint support, tall wings and large effects can constrain repack while runtime scaling remains possible. In-place cell enlargement must retain complete alpha and common scale and meet all20-frame containment; a larger runtime sprite has separate overlap/camera/UI implications and is not authorized by this report.

For U cases (0069,0015,0156,0051,0126), inspect the named face/body/contrast issue at actual world and battle scales. If it still fails, define the smallest authored repair with those exact frame defects before any redraw. For S cases, still reject a trial if the source motion, body readability or pixel density fails at final camera scale. No threshold such as H<80% proves redraw necessity.

## Exact inspected source ledger

- **species_0068**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0068/cohesive-20261009/attempt-03/packed.png`
  SHA-256 `c96964ca10ba527343c0fbb8e3f9168054ccef426effd8ce594b44b66e3d22d8`.
- **species_0037**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0037/cohesive-20261009/attempt-05/packed.png`
  SHA-256 `1d6033147a727270b8b76cb299e6b7f110be551988adc2e690fa4b4fd486cd6e`.
- **species_0086**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0086/cohesive-20261009/attempt-04/packed.png`
  SHA-256 `f22d5148f02416025ed8cb4d0f14c0835245f6c42a988132128b2eb11eb58ac2`.
- **species_0087**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0087/cohesive-20261009/attempt-01/packed.png`
  SHA-256 `11cdde42a657672f1e2cc25c8a2dfab9236fb94abe86ca856b1e8cefd9554cfd`.
- **species_0139**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0139/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `542adb26aac9b97f3b3897a3e94fcbf320bfd80b4512f7d8ec412e81f85fef1c`.
- **species_0084**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0084/cohesive-20261009/attempt-01/packed.png`
  SHA-256 `ed7b23fa9289a06fd4a4554f9b839a5aad761fdfcfa33c1db57c9246cc84b7ee`.
- **species_0124**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0124/cohesive-20261009/attempt-03/packed.png`
  SHA-256 `c21af4a87b11d61483d6714fdb61855d95f9d1f1aeda23909f2d78dba2b3ff6c`.
- **species_0017**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0017/quadruped-20261009/attempt-02/packed.png`
  SHA-256 `4b38aa656023f6211adf2e7361dba15281acae47d2502dfdf0979884384ffce6`.
- **species_0154**: `apps/game-client/assets/pets/redraws/extension-20261013/species_0154/attempt-06/packed.png`
  SHA-256 `a9bbcf2a134c6a14013fd712886d6150ad0c9487bcb69698122cebc5ef9e8059`.
- **species_0069**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0069/cohesive-20261009/attempt-06/packed.png`
  SHA-256 `bf12fca5f13b3e433b8b1546fd552bca7ae1af4a06adb520c4a6dd396559073c`.
- **species_0067**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0067/cohesive-20261009/attempt-03/packed.png`
  SHA-256 `123adc21342dee84bca0321572f36c1bc87beab5ba85bfbfe837a45eff1a2e7a`.
- **species_0085**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0085/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `731b161e5d1a5a61f9eb93224806e08579090f5e0591945e2bb4342dc7783c41`.
- **species_0015**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0015/cohesive-20261009/attempt-06/packed.png`
  SHA-256 `00a4128e4abb701413c0ca1fd7b20cc24a79e780d501bee4841690c68a0ee8a1`.
- **species_0107**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0107/cohesive-20261009/attempt-01/packed.png`
  SHA-256 `74948ef8d365131cc29584139528699898346c9061cd540f99604bf391642b55`.
- **species_0137**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0137/cohesive-20261009/attempt-03/packed.png`
  SHA-256 `a7d91445cecdfaf269d386f561b855119fb228e1b4b0a3cef9ee1cd1208ee84a`.
- **species_0156**: `apps/game-client/assets/pets/redraws/extension-20261013/species_0156/attempt-07/packed.png`
  SHA-256 `a78a94ca0637ee421a946f8cb5cd800bf8162f2cf0bee90aa6f1b414027ce86c`.
- **species_0051**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0051/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `a5ae8708c31066f15098d3cb5832cfde94471e8bc7374dc5148d2768dd9308f0`.
- **species_0122**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0122/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `ec9fe9bee29cfe94c0e0c4be82519fe1b2496e09434138e1bdbd9ab5870c96bf`.
- **species_0145**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0145/proportion-fix-20261009/attempt-02/packed.png`
  SHA-256 `cdea5c254e5074541d3942443124b1fcb1b6196a5141d1a82c6a78d7589bbd07`.
- **species_0126**: `apps/game-client/assets/pets/redraws/owner-feedback-20261009/species_0126/attempt-04/packed.png`
  SHA-256 `37ef8bf3d1e0b525b241daa548dfc8edbc7120cd33265041e58ebda3602e1193`.
- **species_0016**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0016/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `8fcee2fce5ec8fc916a34d9d5c4c35c4c7a537a41f3f2e5a66e6baeb7d040a11`.
- **species_0038**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0038/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `49a501324edad9b6a744b804efa4abf09657fb1280d37c059df84f837a9e9931`.
- **species_0140**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0140/cohesive-20261009/attempt-05/packed.png`
  SHA-256 `7ba46f0ecf387643fa9cb6430c14be5e78d8f40269824e10145db7de6de0e485`.
- **species_0148**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0148/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `5fcea0d7fe9ffad0bf6d9713a494516da0ed41ad619f6cf68277c60707e3860f`.
- **species_0106**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0106/cohesive-20261009/attempt-04/packed.png`
  SHA-256 `977237ecdca2f6a5e32d3f3859b09969f8885b8683fe41288039c1f8484d8196`.
- **species_0035**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0035/cohesive-20261009/attempt-03/timing-v2/packed.png`
  SHA-256 `636cb123b8146bca7ce652df15cc01e5b83b9bc487b9a59ea487b2dcbe86433c`.
- **species_0036**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0036/cohesive-20261009/attempt-02/packed.png`
  SHA-256 `4cef30f40b6357b0013ff7ba83c675dc2f4309fbef6b132c4e8608f60f604463`.
- **species_0103**: `apps/game-client/assets/pets/redraws/polish-20261008/species_0103/cohesive-20261009/attempt-01/packed.png`
  SHA-256 `b2afbcd23e17c87de176c665a486f15af00585726a3d725328fee26ff0477fcc`.
- **species_0020**: `apps/game-client/assets/pets/redraws/owner-feedback-20261009/species_0020/attempt-02/packed.png`
  SHA-256 `978ed445bb9eb8d044559ab43af5b06354a8ca0018d03e5d73d05dca779e380a`.

Only this Markdown file was saved. All candidate/selection/runtime/owner states remain unchanged.
