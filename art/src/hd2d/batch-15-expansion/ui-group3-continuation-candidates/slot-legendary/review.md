# Replacement review: orange-gold candidate

Visually inspected beside the unchanged common template; border reads as orange-gold. Dimensions, binary alpha, and color count pass. Detailed pixel-edge seam review and owner approval remain pending.

## Follow-up inspection

Pixel-level 4-connected-component inspection found a detached 4-pixel row at x=46..49, y=89, separate from the frame (frame bottom ends at y=83). Classified as an artifact. An exact-removal image-generation edit was attempted but rejected: output was 1254x1254, fully opaque, and 67,180 colors. Source candidate remains unchanged. Next step: use a pixel-addressable edit workflow to clear only (46..49,89) in the shared common source, regenerate rarity variants from that source, then rerun connected-component, dimensions, alpha, and palette QA.

Legendary contract comparison: orange-gold hue is present, but the required corner spark is absent. An exact local image-generation edit was attempted and rejected for the same 1254x1254 opaque/high-color output. Next step: add a small pixel-cluster spark at the top-right border using a pixel-addressable edit workflow, then rerun palette and alpha QA.
