# REDRAW-pet-floor-wood-fine

Built-in image_gen; raw attempts `raw-01.png` through `raw-03.png`.

Prompt: overhead warm oak pet-room floor with broad mostly-horizontal boards, varied irregular widths/lengths, staggered joints, fine grain, subtle knots; full opaque tile, seamless in both axes, flat low-contrast perimeter, crisp stepped pixel clusters. Avoid regular stripes, grid, repeated joints/knots, shadows/glow/text/magenta.

References:
- `.ai/design/map-checklists/refs/city_pet_room.jpg` SHA256 `ae78314543b5dd39111a1d52d26474e5a250452cfcca6cf435de2b4763b1cba7`
- `art/src/hd2d/batch-01-octopath/dirt-floor-01/final.png` SHA256 `bd4ba8187917b9023a9f9c9bd7ddc8ad43cb269724cbe02c1137f299ea03dff3`
- `art/src/hd2d/batch-01-octopath/dirt-floor-02/final.png` SHA256 `8a655932d1a1af4b4b600fb652a5aa6df28838798084162fb6f2971556854217`

Pipeline: crop 512×512 from raw (attempt-specific coordinates), nearest crop at source resolution, quantize 40 colors.
