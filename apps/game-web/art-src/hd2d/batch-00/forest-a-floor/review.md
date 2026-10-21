# Source identification and review

Original-biome ground texture, no props.

Declared canvas/world: [512, 512] / [4.0, 4.0]; actual body excludes alpha padding.

Mechanical status: blocked. Owner approval: pending.
Failures: ['seam_mean_below_6', 'forge_wrap_seams'].
Warnings: ['Forge source extraction: 20 visible px belong to no auto box (small or faint parts).'].

Review the native-size light/dark PNG and contact sheet. No text is baked into the runtime asset.
Finishing: Forge chroma extraction/despill, crop, nearest size normalization, shared 48-color palette with binary alpha. Raw files unchanged.
A numeric pass proves file geometry and palette only; it does not approve style, identity, nine-slice behavior or tile repetition by eye.
