# World Tree FX-03 review

Four-frame golden sap droplet burst: droplet, compact five-mote burst, outward green/gold fragments, then small fading fragments. This separates the effect from FX-01 falling leaves and FX-02 pollen dispersal. Final 512×128, 40 shared colors, binary alpha and cell edge alpha 0; full atlas viewed at 4× on checker/dark.

Strict sprite processing passes: 4 frames, no empty/clamped/edge-touch frames, key residue 0 and key ring spill 0. Raw spill check has no cut/cross-cell/empty/sheet-edge failures; `safe_frame` warns on 1/4 cells, while finished atlas margins are over 8 px.

One-shot effect; not a seamless loop. Candidate pending owner review.
