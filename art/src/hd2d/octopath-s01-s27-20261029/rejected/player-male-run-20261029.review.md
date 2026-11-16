# S23 player-male.run — rejected

The generated strip was segmented into eight equal-height cells and palette-finished to 48 colors. Visual inspection and Sprite Forge `sheet_qc.py frames --cycle run` still fail the acceptance contract.

- `leg_alternation`: FAIL — duplicated half-cycle; frame 1 and frame 5 lead with the same leg.
- `identity_head_ratio`: FAIL — 1.078 at frames 4 and 8 against 0.95–1.05.
- `phase_coverage`: WARN — both halves lack a flight phase.
- `torso_drift`: WARN — 11.07 game pixels.

Raw image and full QA remain alongside this note. It is not a delivery and is not suitable as S24's approved reference.
