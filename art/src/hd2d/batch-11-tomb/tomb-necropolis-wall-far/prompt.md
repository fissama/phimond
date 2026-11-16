# tomb-necropolis-wall-far — redraw 03

Route: built-in image_gen. Prompt: “Draw only a horizontal silhouette of a faraway ruined graveyard along the bottom of the frame, with broken low walls, varied tiny grave markers and a few thin dead trees. Skyline occupies the bottom quarter to third, leaving transparent sky above. Use 3–5 flat muted blue-gray colors in crisp pixel clusters and cutout edges. Vary all forms and gaps so no landmark tower or arch repeats. Flat cutout layer: no sky, fog, glow, gradient, light beams or ground plane. Make left and right boundaries compatible for horizontal tiling. Low detail, distant, no text or watermark.”

Raw: `raw-02.png`; prior raw-01/final/QA/review remain preserved. Raw size 2172×724. Crop `(184, 0, 2115, 724)`, nearest resize to 1024×384, threshold alpha at 128 to binary, nondithered median-cut to 48-color RGB. No painting or mirroring.

Raw SHA256: `21260f7abe46cb634b222cc9d29a5d3de9d1ab8b7f9d12483cf0c8f79a4d0c74`
Final SHA256: `ccb2dfee16a27126a44c7b119f8ada9743570842ad3bdcb192ac304dbd70fcfe`
QA: 41 opaque colors; alpha binary; horizontal seam MAE 2.260 (threshold 14); 3×1 repeat viewed. Draft remains `approved:false`; the 3× repeat is less dominated by repeating towers, but owner scene review is still pending.
