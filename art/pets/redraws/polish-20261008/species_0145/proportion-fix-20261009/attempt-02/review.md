# Cây Cự Linh — proportion correction review

- Owner rejected the independently generated row boards because torso, stone legs and log arms changed proportions across animation states. These boards remain under `../rejected/` and are not selected.
- Selected source is one cohesive 20-frame generation using only original APK portrait and sprites of CayCuLinh. First full-atlas attempt was rejected because Attack/Cast/Down crossed visible source dividers.
- Second full-atlas source has all source dividers clear at alpha >=128. Standing neutral/Move/Cast silhouettes are approximately 170–172 source pixels tall; all twenty poses retain the same squat trunk, short stone legs and massive banded log arms. Articulation/occlusion changes the projected silhouette; there is no per-frame resizing.
- Full raw alpha is preserved. One nearest-neighbor scale 0.6805555556 applies to all frames. Source pivots align ground contact from the generated layout; destination pivot is [140,210]. No erased alpha, painted repairs or cropped-off limbs.
- Atlas checker PASS, 20 occupied and distinct frames, geometry 1124x1405 RGBA. Gray composite confirms transparent background.
- Browser playback inspected at 64/96/192 cell sizes; Move alternates short stone-foot support, Attack uses a short log thrust, Cast vine stays close to forearms, Down final two poses lie on the ground. Cast and Down also inspected on light background.
- Final battle display scale and label/HP separation remain pending under shared battle-layout gate. Owner has not approved this corrected atlas. No runtime activation.
- Candidate SHA256: cdea5c254e5074541d3942443124b1fcb1b6196a5141d1a82c6a78d7589bbd07
