# Portrait Bia shop — edge repair candidate

The original delivery showed 180 strongly magenta-hued opaque pixels directly adjacent to transparency, all with RGB `(197,25,139)`. Reprocessing the original raw source with edge despill radius 2 reduced that count to zero while keeping the exact 256×256 canvas, 48-color palette, binary alpha, and original portrait framing. The strict palette tool gate passed with maximum ΔE 0.145981 (limit 0.15). The sprite process gate reports `warn` only for the source portrait touching the bottom crop, which is required by the prompt; output-edge contact and key-ring spill both pass.

Visual review on a dark background found the character identity, teal hair, clothing, crop, and silhouette coherent. This is a review candidate; it does not replace the existing delivery, is not installed, and still needs Claude/owner approval.
