# N08 dialogue-frame candidate — 2026-10-30

Reviewed the cropped and palette-finished 1024×224 PNG on a dark preview. The very wide double-gold frame reads cleanly; the left portrait ring is separate and both the portrait socket and main dialogue area are transparent. There is no text or button art. At final size the portrait ring appears about 170 px across versus the 160 px target, with its center near (112,112); keep this geometry caveat for owner/HUD comparison.

Mechanical checks: exact 1024×224; 48 visible colors; binary alpha [0,255]. Palette tool reports `status: pass`, 0 off-palette output pixels, 0 partial-alpha output pixels, max dE 0.077033. The raw ImageGen result was 2171×724; a centered 2171×475 crop was Lanczos-scaled to 1024×224, then quantized with the generated 48-color palette and alpha threshold 128.

This is an unapproved candidate. No installation or runtime sampling test was done.
