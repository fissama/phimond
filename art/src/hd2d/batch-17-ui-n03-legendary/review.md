# N03 legendary redraw — not accepted

The raw image is 1254×1254 RGBA, 256 alpha values, 72,171 RGBA colors. The official sprite pipeline produced an exact 96×96 frame with no cell-edge touch; a 48-color palette apply passed, producing 39 RGBA colors and binary alpha.

Visual review at 4× found the top-right sparkle was no longer a distinct star at the required 96×96 size, and the corner ornaments/frame geometry differ from the shared slot template. The pipeline's default alpha hygiene removed 16 pixels in 7 detached components (including the small sparkle detail). Disabling hygiene preserved the detail but also preserved visible dark specks along the inner border. Both processed variants are therefore rejected as replacements. The existing `slot-legendary.png` remains unchanged; its 4-pixel detached bottom component and missing corner spark remain open.
