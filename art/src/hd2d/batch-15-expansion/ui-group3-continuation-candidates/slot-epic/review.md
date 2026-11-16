# Replacement review: purple candidate

Mechanically recolored from the common template; color and dimensions inspected. Formal edge/seam review and owner approval remain pending.

## Follow-up inspection

Pixel-level 4-connected-component inspection found a detached 4-pixel row at x=46..49, y=89, separate from the frame (frame bottom ends at y=83). Classified as an artifact. An exact-removal image-generation edit was attempted but rejected: output was 1254x1254, fully opaque, and 67,180 colors. Source candidate remains unchanged. Next step: use a pixel-addressable edit workflow to clear only (46..49,89) in the shared common source, regenerate rarity variants from that source, then rerun connected-component, dimensions, alpha, and palette QA.
