# Footstep dust FX

Create a four-frame horizontal sprite sheet, 256×64 overall, four 64×64 cells left-to-right. Pixel-art finish, compact warm gray-beige dust at ground level, transparent background, no actor, feet, floor, text, dividers, glow or blur. Phase 1: compact puff beginning; phase 2: low crescent expands; phase 3: puff breaks into three motes spreading out; phase 4: a few fading motes. Keep a shared ground baseline, consistent scale, no cell-crossing pixels, no magenta or red fringe.

Generated with Codex `image_gen`; raw resolution was 1983×793. Final frame registration, 24-color palette and exact strip dimensions were produced by the sprite pipeline and FFmpeg lossless hstack.
