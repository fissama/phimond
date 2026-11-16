# Prompt & provenance — cr-bac-ha

- Đơn tham chiếu: `.ai/design/gpt-redo/15-garden-crops-anim-prompt.md`
- Art source: Codex built-in `image_gen` (host image generation).
- Source: `raw-01.png`; SHA-256: `e861d37ea466a6862eed1e14c5a9b92d90bb86eb8720c86419a2a6155d85c98e`.
- Processed candidate: `final.png`; SHA-256: `af324e0759efe5f294b304d0d91bbfde1e37fecc35266ab29c9d324be49033ed`.

Prompt contract: one 4×5 sprite atlas, one crop across sprout/grow/ripe/harvest/plant phases; magenta key background; 192×192 cells; anchor (96,168); 16 px safe margin; pixel art; no pot, text, blur, bloom, or baked shadow. See Đơn 15 for the complete crop-specific prompt and species description.


## Latest redraw source and reference hashes (2026-11-09)
- Source raw: `raw-09.png`; SHA-256 `dbac03782a8be2aff5bc252d25e1c89fbade32d234c0652597f78bd982952747`.
- Current candidate `final.png`; SHA-256 `9b5f6de4f726ffc37b025ee9baeade5c25ef7aef55c451acef4ce064ef0ceebd`.
- Reference image SHA-256 values:
  - `mushroom-ochre` — `2ca56af1131a94771b5065522d5a573cee0425175daf6a053058d2f881e33057` (`apps/game-web/art-src/hd2d/batch-01-octopath/mushroom-ochre/final.png`).
  - `pebbles-01` — `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a` (`apps/game-web/art-src/hd2d/batch-01-octopath/pebbles-01/final.png`).
  - `gd-decor-03` — `dd459142a3df97a3133bff663b7aa8625cb85d7d85d37a4768da8edb35064ef2` (`apps/game-web/art-src/hd2d/garden-a/gd-decor-03/final.png`).
  - `DocDangNu sprites` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da` (`apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png`).
  - `DaoThienDuong sprites` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3` (`apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png`).
- ImageGen accepted a maximum of five image references per call; references were rotated across attempts. Historical raw files remain in place.


## Pipeline v3 selected source and image reference hashes (2026-11-10)
- Selected source: `raw-09.png` — SHA-256 `dbac03782a8be2aff5bc252d25e1c89fbade32d234c0652597f78bd982952747`.
- Final atlas: `final.png` — SHA-256 `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`.
- Immediate edit/layout reference: `raw-09.png` — SHA-256 `dbac03782a8be2aff5bc252d25e1c89fbade32d234c0652597f78bd982952747`.
- Image references used:
  - `final.png` — SHA-256 `2ca56af1131a94771b5065522d5a573cee0425175daf6a053058d2f881e33057` (`apps/game-web/art-src/hd2d/batch-01-octopath/mushroom-ochre/final.png`).
  - `final.png` — SHA-256 `328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a` (`apps/game-web/art-src/hd2d/batch-01-octopath/pebbles-01/final.png`).
  - `sprites.png` — SHA-256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da` (`apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png`).
  - `sprites.png` — SHA-256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3` (`apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png`).
