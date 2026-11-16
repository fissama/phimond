# Prompt & provenance — cr-moc-nhi

- Đơn tham chiếu: `.ai/design/gpt-redo/15-garden-crops-anim-prompt.md`
- Art source: Codex built-in `image_gen` (host image generation).
- Source: `raw-01.png`; SHA-256: `c0ab7b8362c55dfdd27e4251e3532ecad74dde250fc35b03b1e90cdb2a7b67b2`.
- Processed candidate: `final.png`; SHA-256: `c787ba3f1c864002293224cc0506ad593150d7fccf9c0d238e4b1b0adc9b5a38`.

Prompt contract: one 4×5 sprite atlas, one crop across sprout/grow/ripe/harvest/plant phases; magenta key background; 192×192 cells; anchor (96,168); 16 px safe margin; pixel art; no pot, text, blur, bloom, or baked shadow. See Đơn 15 for the complete crop-specific prompt and species description.


## Latest redraw source and reference hashes (2026-11-09)
- Source raw: `raw-09.png`; SHA-256 `3889d6bc4441c464c02b6b994b1af09e7ad04737bfa015d4ec5cdac3e2341a35`.
- Current candidate `final.png`; SHA-256 `361855eff92e506b2c0f37a7d2eec7e2193dce7b038bf6b85f79e583936f621b`.
- Reference image SHA-256 values:
  - `mushroom-ochre` — `2ca56af1131a94771b5065522d5a573cee0425175daf6a053058d2f881e33057` (`apps/game-web/art-src/hd2d/batch-01-octopath/mushroom-ochre/final.png`).
  - `pebbles-01` — `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a` (`apps/game-web/art-src/hd2d/batch-01-octopath/pebbles-01/final.png`).
  - `gd-roots-hang-04` — `9a23c7f7861ecd61f8b8f1ead09ef96005b650f31cdfad2498dc59b047d837e6` (`apps/game-web/art-src/hd2d/garden-a/gd-roots-hang-04/final.png`).
  - `DocDangNu sprites` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da` (`apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png`).
  - `DaoThienDuong sprites` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3` (`apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png`).
- ImageGen accepted a maximum of five image references per call; references were rotated across attempts. Historical raw files remain in place.


### Exact prompt used for latest Mộc Nhĩ generation

> One exact 4×5 pixel-art atlas for Mộc Nhĩ Linh Thảo: a timid original mushroom-rabbit with wood-ear caps, face, leaf arms and root. References: mushroom-ochre and pebbles-01 for pixel style, gd-roots-hang-04 for garden palette, DocDangNu and DaoThienDuong for atlas layout/chibi proportions. Flat #FF00FF background, crisp clusters, no gradients/AA/blur/glow/shadow/text. Four sequential frames per row; sprout 38–45 px, grow 83–98 px, ripe 115–145 px; root x=96,y=168; all pixels in [16,175]. Rows 1–3 reuse identical body pixels and palette, changing eyes/mouth/ears/arms/spores only; blink in each loop. Harvest row has four nonempty frames and ends in sparse rays. Plant row ends matching sprout frame 1.


## Pipeline v3 selected source and image reference hashes (2026-11-10)
- Selected source: `raw-12.png` — SHA-256 `7bf0b93faa8ff4a3cc68b076875da007dc90a30177d8dc02f8fe84e88c5a135f`.
- Final atlas: `final.png` — SHA-256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`.
- Immediate edit/layout reference: `raw-11.png` — SHA-256 `f451f0ebf5f184f652ad484aa34171d62439275a176369b44d117a77207fc272`.
- Image references used:
  - `final.png` — SHA-256 `2ca56af1131a94771b5065522d5a573cee0425175daf6a053058d2f881e33057` (`apps/game-web/art-src/hd2d/batch-01-octopath/mushroom-ochre/final.png`).
  - `final.png` — SHA-256 `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a` (`apps/game-web/art-src/hd2d/batch-01-octopath/pebbles-01/final.png`).
  - `sprites.png` — SHA-256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da` (`apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png`).
  - `sprites.png` — SHA-256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3` (`apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png`).
