# World Tree FX-02 review

Rising golden seed-pollen burst, distinct from FX-01 falling leaf. Four frames disperse the golden motes while one or two green flecks rise. Final atlas 512×128; shared no-dither palette 40, binary alpha, transparent cell edges, at least 8 px final safety margins. The complete 4× atlas was viewed on checker and dark backgrounds.

Mechanical: spill check has no cuts, empty cells, cross-cell spill or sheet-edge touch; it reports `safe_frame` for 1/4 cells (raw art within the 15% safe frame). Final was scaled with extra margin. Strict sprite processing passes (four nonempty frames, no clamping/edge touch, key residue 0 and ring spill 0).

Animation is a brief one-shot that disperses; it is not a seamless loop. Candidate only; owner review pending.
