# Prompt & provenance — G1 Thổ Đào Bồn

- Đơn tham chiếu: `.ai/design/gpt-redo/14-garden-pots-anim-prompt.md`
- Art source: Codex built-in `image_gen` (host image generation).
- Selected source: `raw-03.png`; SHA-256: `f095c7f91a403f2bbdd6c4b4492d46093b3c339dfa13700e022b1c6e66bc9267`.
- Current processed candidate: `final.png`; SHA-256: `907752be3f2c63c4db70c48d270c185b28a73ddd2a5bcc4244fb8592023e71ee`.
- Edit iteration `raw-04` was generated after inspection but was not selected.

## Normalized prompt used for the latest edit

Edit the supplied Phimond G1 terracotta garden pot atlas. Preserve the warm handmade pot design and crisp pixel-cluster style. Make a 4-column × 5-row atlas on flat #FF00FF, empty pot, same silhouette, position, palette, and registration in every cell. Pot mouth center at (96,112), base y=176, width about 120 px. Rows: idle, wet, water, upgrade, clear. Use small pixel effects only; no blur, shadow, glow, text, or magenta-colored art. Keep contents within a 16 px cell margin. Require row 3 column 4 to return to row 2 column 1, and row 4 column 4 plus row 5 column 4 to return to row 1 column 1.

## Processing

Nearest-neighbor normalization/cropping, near-magenta keying, one shared 60-color palette, and per-cell translation to hold the pot base at y=175. No painting or code-drawn pixels. Mechanical details and failed transition checks are in `qa.json`.


## Latest redraw source and reference hashes (2026-11-09)
- Source raw: `raw-11.png`; SHA-256 `8b980cbbe7be53631460da8dc92d74dd92fbee9dc80648d2412ddadce675d785`.
- Current candidate `final.png`; SHA-256 `428b8d73ba1b0010d0814afb89666cc715c8229d2533fe4b99f37e7ca0c8f893`.
- Reference image SHA-256 values:
  - `mushroom-ochre` — `2ca56af1131a94771b5065522d5a573cee0425175daf6a053058d2f881e33057` (`apps/game-web/art-src/hd2d/batch-01-octopath/mushroom-ochre/final.png`).
  - `pebbles-01` — `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a` (`apps/game-web/art-src/hd2d/batch-01-octopath/pebbles-01/final.png`).
  - `gd-decor-03` — `dd459142a3df97a3133bff663b7aa8625cb85d7d85d37a4768da8edb35064ef2` (`apps/game-web/art-src/hd2d/garden-a/gd-decor-03/final.png`).
  - `gd-roots-hang-04` — `9a23c7f7861ecd61f8b8f1ead09ef96005b650f31cdfad2498dc59b047d837e6` (`apps/game-web/art-src/hd2d/garden-a/gd-roots-hang-04/final.png`).
- ImageGen accepted a maximum of five image references per call; references were rotated across attempts. Historical raw files remain in place.


## Pipeline v3 selected source and image reference hashes (2026-11-10)
- Selected source: `raw-21.png` — SHA-256 `b749992032e27ea25f46d9da2bac4a849a742051cf25a9a93eb660d9cd17296a`.
- Final atlas: `final.png` — SHA-256 `787a60d5bcbfea5d14f407fb11579c6da377bc16f1300fdc7711300a312d75af`.
- Immediate edit/layout reference: `raw-20.png` — SHA-256 `9e2852e361ebc92317da827d9e556fa38950c3d291b67cfd61060b148e0d737c`.
- Image references used:
  - `final.png` — SHA-256 `3b7940b55638a603307a88863556f54fc887fa441f35e22482903006a7792fae` (`apps/game-web/art-src/hd2d/garden-a/gd-decor-06/final.png`).
  - `final.png` — SHA-256 `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a` (`apps/game-web/art-src/hd2d/batch-01-octopath/pebbles-01/final.png`).
