# NPC square-board portrait — edge repair candidate

The original delivery had 277 opaque fuchsia-purple pixels adjacent to alpha transparency. Reprocessing the original 1254×1254 source with edge despill radius 2, then the existing 48-color palette, reduced the strict magenta-hued edge detector to 2 pixels. Visual side-by-side review on checkerboard shows the bright fuchsia halo on hair and jewelry edges removed while the purple hair, jewelry, face, silhouette and crop remain intact.

Mechanical checks: exact 256×256; 48 visible colors; binary alpha; palette apply pass with maximum ΔE 0.12382 (limit 0.15). The sprite process QA is `warn`: `source_edge_touch_frames=[[0,0]]` for the intentional lower-torso crop, and `key_ring_spill=0.044393` remains above its 0.01 threshold. The latter may include intentional purple hair at the perimeter; it is retained verbatim as a warning and needs owner review on dark/light UI backgrounds.

This is a review-only candidate. It does not replace the current delivery and is not installed or approved.
