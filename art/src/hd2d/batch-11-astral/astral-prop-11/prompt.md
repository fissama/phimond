# Astral starlight flower — candidate

Route: built-in Codex `image_gen` (`art_source: host_image`; model identifier not exposed). Raw output preserved.

## Prompt

One large starlight flower prop for Phimond’s Astral Realm kit, isolated and fully visible on a genuine transparent background. A single five-petal violet blossom with layered lavender petals, a small warm gold center and a short dark plum stem with two leaves; elegant but readable at game scale, based on the dusk forest map in reference 1. Reference 2 is approved pixel flower art; pet sheets 3-4 only guide outline and shading. Front-facing game sprite, centered with generous clear margins. Crisp clustered pixel art, hue-matched dark outline, 33-48 useful colors, 2-4 tones per material. Subtle internal highlight only; no external glow, aura, cast shadow, ground or backdrop. No text, extra flowers, blur, gradients, cropping or clipped edges. Hard binary alpha.

## Attached references and SHA-256

- `.ai/design/map-checklists/refs/astral_realm_unnamed_area_05.jpg` — `6f8af4c0586b87a48e4b5d88e56b84b7dfa38f6e1fe19f031f47a08cb097db24`
- `apps/game-web/art-src/hd2d/batch-01-octopath/flower-purple/final.png` — `d6b77bbbe4c19c5432ea04beb65c725e60a96562a12400299873ad8c889f4049`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Finishing: alpha threshold at 128; nondithered FASTOCTREE quantization to 48 (35 visible colors); crop to complete alpha bounds plus 8px transparent margin. No code-drawn art.
