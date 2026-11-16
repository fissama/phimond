# Source identification and review

Separate low forest grass, fern or flower clump; colors follow the original forest.

Declared canvas/world: [128, 96] / [1.0, 0.75]; actual body excludes alpha padding.

Mechanical status: pass. Owner approval: pending.
Failures: none.
Warnings: ['Forge source extraction: 20 visible px belong to no auto box (small or faint parts).'].

Review the native-size light/dark PNG and contact sheet. No text is baked into the runtime asset.
Finishing: Forge chroma extraction/despill, crop, nearest size normalization, shared 48-color palette with binary alpha. Raw files unchanged.
A numeric pass proves file geometry and palette only; it does not approve style, identity, nine-slice behavior or tile repetition by eye.
