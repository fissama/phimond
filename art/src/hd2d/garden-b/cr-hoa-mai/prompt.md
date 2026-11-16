# Prompt & provenance — cr-hoa-mai

- Brief: `.ai/design/gpt-redo/20-batch-C06-prompt.md`; shared rules: `.ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md`, `15-garden-crops-anim-prompt.md`, `15b-garden-crops-roster-v2.md`.
- Character: Hoa Mai, cheerful spring swallow spirit; five-petal golden blossoms form wings, dark-brown branch body, green buds, small bird face, plain red envelope.
- Selected built-in ImageGen source: `raw-02.png`, SHA-256 `1e88087fff7d297c8b2a23216789a15c30ea6d071ad7f8dae8a5bca140e09f59`.
- Packed candidate: `final.png`, built by `tools/pack_atlas.py`; no manual pixel edits.
- References attached in order: `cr-bac-ha/final.png` 8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8; `cr-moc-nhi/final.png` 2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51; `gd-roots-hang-04/final.png` 9a23c7f7861ecd61f8b8f1ead09ef96005b650f31cdfad2498dc59b047d837e6; `mushroom-ochre/final.png` 2ca56af1131a94771b5065522d5a573cee0425175daf6a053058d2f881e33057; `pebbles-01/final.png` 328f80aff0c2acab7ba50d1ce79604854a00c2b481548f6b7267703d0a4c8e8a.
- Eight ImageGen outputs retained as raw-01..08. raw-02 is the best mechanical candidate (10/10) with the requested character cues. Several alternatives had pack failures or lower plant IoU.
- Constraints: exact 4×5 key atlas, fixed pivot, staged growth, loop blinks, plant frame4 matches sprout frame1, no glow/shadows/text, crisp contours without magenta.
