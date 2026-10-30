# Generation prompts and references

Tool: built-in `image_gen`; one generation call per candidate. All prompts request crisp HD-2D pixel art and no text/watermark. Output was resized to the exact plan dimensions and palette-limited after generation.

## `fg-deep-vines.png`

Reference: `apps/client/public/hd2d/fg-forest-branch-a.png` (style and pixel-density only).

> Use case: stylized-concept. Asset type: isolated near-camera foreground sprite for an HD-2D game. Image 1 (hanging leafy branch) is the only style and pixel-density reference. Create one distinct Deep Forest foreground asset: old tangled vines dangling from the top edge, irregular clusters of dark leaves, and 4–6 small softly luminous green mushrooms embedded in the foliage. Canvas exactly 512×384 px, landscape. Open transparent gaps between the hanging strands; no ground, no full tree, no characters. Match the reference's detailed crisp pixel art, clear clusters, top-left warm highlights and cool dark-green shadows, ≤48 colors, 1px dark outline. Transparent background with binary alpha, clean edge, no fringe; keep the luminous pixels attached to mushroom caps. No blur, text, watermark, scenery, magenta fill.

## `fg-gate-banner-edge.png`

Reference: `apps/client/public/hd2d/palace-gate.png` (style and palette only).

> Use case: stylized-concept. Asset type: isolated foreground sprite for an HD-2D Palace Gate game scene. Input image 1 is the only style and palette reference (gold sandstone palace gate). Create two separate royal blue hanging banners suspended from the upper edge, framing the gate view. Exact 384×512 px portrait canvas. Each cloth flag has a small centered gold sun emblem, slight ragged lower edge, carved gold trim, deep blue folds. Place the flags near the left and right sides with large open transparent space between them; no poles, arch, wall or scenery. Match the reference's warm gold highlights, cool shaded folds, crisp detailed pixel art and 1px dark outline, ≤48 colors. Transparent background, binary alpha, clean edges and no fringe. No text, watermark, blur, gradients or extra objects.

## `hall-side-corner.png`

References: `apps/client/public/hd2d/hall-side-pier.png` (pier material) and `apps/client/public/hd2d/hall-side-balustrade.png` (balustrade material and ornament).

> Use case: stylized-concept. Asset type: isolated architectural connector sprite for an HD-2D game hall. Input image 1 is the carved sandstone pier reference; image 2 is the matching balustrade material and ornament reference. Create a single front-side corner fragment that turns the hall railing around a corner: one tall square sandstone corner pier with a small ornate gold lotus-like cap and tiered base, with short balustrade lengths extending horizontally from the lower left and lower right sides to visually close the corner. Exact 256×400 px portrait canvas. Keep transparent margins around silhouette. Match both references' pale warm stone, gold carving, top-left light, cool shadow, crisp detailed pixel art, hard edges, 1px dark outline, ≤48 colors. Transparent background with binary alpha and clean edges, no magenta fringe. No floor, walls, other columns, text, watermark, blur or extra scene.

## `hall-outside-roofs-side.png`

Reference: `apps/client/public/hd2d/hall-city-backdrop.png` (style and palette only).

> Use case: stylized-concept. Asset type: opaque side-background plate for an HD-2D summoning-hall scene. Input image 1 is the only style and palette reference: the warm walled city skyline. Create an exterior view glimpsed from either side of the hall's outside wall: a few layered terracotta rooftops, one modest distant tower, pale-blue sky and faint far hills, composed as a calm edge-of-scene slice with the roofline mostly in the lower half and clear sky above. Exact 512×384 px landscape canvas, fully opaque all the way to every edge. Match the reference's detailed crisp pixel art, cream stone and orange roofs, warm top-left light, cool shadows, ≤48 colors, no atmospheric gradients. No hall interior, no foreground props, people, text or watermark. Keep composition suitable as a background filler; avoid a dominant central castle or large focal building.
