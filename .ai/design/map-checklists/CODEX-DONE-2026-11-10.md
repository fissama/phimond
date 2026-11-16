# CODEX-DONE — snapshot 2026-11-10

**CHƯA ĐỦ 100%** — đây là tiến độ hiện tại, không phải nghiệm thu. ROADMAP gồm 672 dòng; vẫn còn task PENDING, FAILED_AFTER_3_TRIES và BLOCKED. Không có asset nào được tự duyệt, manifest/runtime không bị sửa.

## Số lượng theo trạng thái

| Trạng thái | Số task |
|---|---:|
| READY_FOR_CLAUDE_REVIEW | 77 |
| FAILED_AFTER_3_TRIES | 66 |
| BLOCKED | 62 |
| PENDING | 467 |

## Tiến độ trong lượt này

- Tạo 9 candidate landmark (6 desert, 2 forest, 1 ship) (6 desert M3, 2 forest M3), từng ảnh raw riêng; xử lý bằng crop, nearest resize, alpha cleanup và quantize 48 màu. Candidate và preview đã được xem; số màu 47–48, alpha nhị phân, lề tối thiểu ≥20 px.
- Đã thêm 9 dòng ledger từ PENDING sang READY_FOR_CLAUDE_REVIEW; handoff được phân thư mục desert (6), forest (2), ship (1).
- `art_gate.py --all`: exit 1; 33 pack, 1,434 assets, 367 lỗi, 0 cảnh báo. Breakdown: audit 295, bbox-edge 35, size 16, sheet 21. Kết quả là gate cơ học trên pack canonical; không chứng minh visual approval. Candidate handoff chưa được đăng ký nên gate không quét 9 file mới.
- Nguyên nhân chưa chạy gate cho candidate: script chỉ quét thư mục `art/src/hd2d/batch-*`; hướng dẫn cấm đăng ký manifest trước khi Claude nghiệm thu.

## FAILED_AFTER_3_TRIES và hướng xử lý

- `NEW-tower-floor-03` — attempts 1–2 sai chủng loại (cát), attempt 03 là gỗ nhưng wrap 2.75/4.18, autocorr 0.844 và outer 8px không phẳng. Đề xuất cần tile-generation workflow có thể kiểm soát seams/border; không chỉnh bằng code theo giới hạn hiện hành.

- `NEW-tower-floor-03` — attempts 1–2 sai chủng loại (cát), attempt 03 là gỗ nhưng wrap 2.75/4.18, autocorr 0.844, và outer 8px không phẳng. Đề xuất cần tile-generation workflow có khả năng kiểm soát seams/border; không chỉnh bằng code theo giới hạn hiện hành.

- `NEW-tower-floor-02` — attempt 03 đạt wrap 1.20/1.56 và autocorr 0.155 nhưng outer 8px border vẫn có chi tiết; không có final. Đề xuất mở lại bằng phương pháp sinh/cắt tile có thể giữ viền phẳng, không sửa pixel bằng code khi chưa cho phép.

- `NEW-tower-floor-01` — ba attempt đều có viền khung và wrap x/y không đạt; attempt 03: 4.41/5.24. Không có candidate cuối. Đề xuất dùng route tạo texture seamless hoặc chờ phê duyệt bước sửa seam riêng.

- `REDRAW-world_tree-floor-extra-05` — 40 colors; wrap x=2.64, y=3.37 exceed 2.0 after three raw attempts; failed. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-ancient-edge-03` — 3/3 attempts exhausted. Failed autocorr ≤0.25 despite seam <14, binary alpha and 37 colors. 3x1 preview, raw attempts and QA in handoff; visual motif rhythm needs new art approach. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-astral-floor-extra-03` — 3/3 attempts exhausted. Best attempt 2 fails wrap_x threshold; all raw images, per-attempt metrics and best 3x3 preview in handoff. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-astral-floor-extra-05` — 3/3 attempts exhausted; best attempt misses wrap_x threshold by 0.003. All raws, QA, and 3x3 preview in handoff; cross-correlation check recorded in QA. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-astral-edge-03` — 3/3 attempts exhausted. Best attempt 1 metrics pass but visual 3x1 shows repeated cluster cadence; attempts 2/3 have key artifacts. Raw variants and previews in handoff. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-01` — 3/3 attempts exhausted; all failed strict wrap threshold. Best attempt 1 staged with 3x3 preview; no flat navy cross. Per-attempt metrics in QA. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-02` — 3/3 attempts exhausted; all fail wrap threshold. Best attempt 1, 3x3 preview saved; no navy cross. Cross-texture corr with floor-01=0.0646. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-03` — 3/3 attempts exhausted; best attempt still fails wrap and visual moss cadence. 3x3 preview saved; cross-texture corr floor-01=0.0687. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-05` — 3/3 attempts exhausted; all fail wrap thresholds. Best attempt 1 with 3x3 preview; cross-texture corr floor-01=0.0618. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-04` — 3/3 attempts exhausted; all fail wrap thresholds. Best attempt 2 retained with 3x3 preview; no navy cross. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-extra-01` — 3/3 attempts exhausted; all fail wrap thresholds. Best attempt 1 retained with 3x3 preview; corr floor-01=0.0756. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-extra-02` — All 3 attempts exceeded floor wrap ≤1.25; retain best combined seam candidate-02; see QA/repeat previews. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-crossroads-floor-extra-03` — All 3 attempts exhausted; strict wrap threshold missed. candidate-02 has best seam; see 3x3 previews. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-desert-sandstone-floor` — All 3 attempts exhausted; strict wrap threshold missed. Candidate-01 is best combined seam; see previews. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-desert-sand-cracked-01` — All 3 attempts exhausted; wrap_y threshold missed. candidate-03 best combined seam retained with 3x3 previews. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-desert-sand-cracked-02` — 3 attempts used. Attempt 2 best seam but repeated polygon crack-cell pattern fails visual error criteria; retained for review. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-desert-limestone-grit-floor` — 3 attempts exhausted; strict wrap_y threshold missed. Candidate-02 retained with QA/previews. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-ghost_castle-floor-extra-01` — 3 attempts exhausted; wrap_y threshold missed. Candidate-01 retained as best combined seam. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-ghost_castle-floor-extra-05` — 3 attempts exhausted; all missed floor wrap threshold. Candidate-01 best combined seam retained. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-ghost_castle-edge-03` — 3 attempts exhausted. Best seam candidate has obvious repeated velvet motif in 3x1; attempt 3 drifted to wall/windows; retain attempt 2 for review. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-floor-02` — 3 attempts exhausted; strict wrap thresholds missed. Candidate-01 retained as best combined seam with 3x3 previews. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-floor-03` — 3 attempts exhausted; strict wrap_x missed. Candidate-01 retained as best combined seam. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-decal-03` — Attempt 3/3; binary alpha; margin 22px; 30 colors; candidate-03 + 4x QA preview. Claude visual review required. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-decal-04` — All 3 attempts failed: #1 <33 colors; #2 and #3 have diffuse baked glow/halo. Candidate-03 and 4x preview retained for audit. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-decal-06` — All 3 attempts below 33 colors (23/26/28); raw/candidates/4x retained. No palette edits applied. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-decal-08` — All 3 attempts failed 33-color minimum (27/27/10); attempt 1 also long trail; attempt 3 halo removed by key. Raw/candidates retained. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-decal-09` — All 3 attempts failed: colors 18/32/24; attempt 2 was a broad ground patch; attempts with glow alpha-keyed for third but sparse islands remain. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-decal-10` — All 3 attempts below 33 colors (26/30/6); attempt 3 also pale lavender/white facets and halo. Raw/candidates retained. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-nightmare-backdrop-near` — 3 attempts: #1 white sky; #2 repeated arches; #3 crop clips top of landmark. No compliant candidate. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-tomb-wall-sprit-torch` — 3 attempts; quantized results 22/29/29 colors, below required 33–48; candidate retained for audit, failure reason documented. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-tomb-dead-thorn-bush` — 3 fresh generations yielded 18, 21, and 24 colors after crop/resize/quantize; final below 33-color minimum. Retained candidate and raw attempts; FAILED_AFTER_3_TRIES. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-tomb-dead-tree-stump` — 3 fresh attempts yielded 23, 26, and 26 colors after processing, below 33–48 minimum. FAILED_AFTER_3_TRIES; all raws preserved. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-tomb-guardian-statue-head` — 3 fresh reference-guided generations each quantized to 26 colors (<33 minimum); candidate/raw attempts retained. Subject and approximate size met; palette complexity is blocking criterion. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-tomb-hanging-censer` — 3 fresh generations quantized to 17/21/19 colors, below 33–48. Failed palette complexity; raw attempts preserved. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-tomb-floor-golden-sand` — All 3 generated attempts reviewed; candidate 3 passes numeric seam but visibly repeats ripple bands and dark clusters in 3x3. No acceptable candidate. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-tomb-edge-ruin-rubble` — 3 attempts: candidate 3 meets 33 colors and seam<14 but repeats an arch motif at every tile and retains mound peaks; FAILED on visual repetition/type. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-windrock-grass-snow-floor` — Map palette override: brown/charcoal; snow omitted as absent from map. 3 attempts retain regular row-like grass/clump rhythm despite numeric pass; FAILED visual repetition. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-windrock-snow-crust-floor` — FAILED_AFTER_3_TRIES; prior three generated attempts already exhausted. One extra crop evaluation of new raw candidate retained only as diagnostic: wrap_x 1.3013 exceeds ≤1.25 and 3×3 visibly shows seams; raw/crop cannot remedy within pipeline. Map palette follows dark brown/charcoal with sparse gray snow crust. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-windrock-slate-floor` — 3 attempts; no seam-compliant candidate, final 3×3 visibly grids cobbles. Map palette adapted to muted dark slate/umber. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-windrock-rock-floor-03` — 3 generated attempts; no candidate meets wrap≤1.25. Attempt 3 visibly tiles as a repeated cluster in 3×3. Distinct fractured-rock concept, subdued map palette. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-windrock-edge-01` — 3 raw attempts; best crop is still visibly discontinuous/repeats a distinctive peak at each tile. End seam fails; not suitable for review. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-windrock-edge-02` — 3 generated raw attempts; best crop still has obvious end discontinuity and repeated terrain clusters in 3×1. Cannot meet wrap criterion via crop/resize/quantize pipeline. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-city-roofline-mid` — 3×1 visually repeats prominent house/stall motifs inside tile; all candidates have end seam >14. Needs different, more varied raw skyline. Map refs show modest market facades; generated tall/identical forms rejected. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-pet-floor-wood-fine` — Three raw attempts failed wrap≤1.25; candidate 03 3×3 visibly repeats horizontal plank rows and knots. Map palette matches warm honey oak; needs a genuinely tileable new texture. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.
- `REDRAW-palace-floor-marble` — Three raw attempts; no crop meets wrap≤1.25, final 3×3 shows distinct repeated cloud/vein forms. Dark slate palace floor palette followed; needs new tileable raw texture. Hướng xử lý: tạo artwork mới theo prompt, giữ attempt cũ; tối đa 3 lần cho vòng tiếp theo nếu chủ sở hữu mở lại task.

## BLOCKED và hướng xử lý

- `FIX-ancient-shadow-01` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=0556e652a4, QA sha=f8d2ddf199, actual sha=f8d2ddf199); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-ancient-shadow-02` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=52b965cdaf, QA sha=48d046208f, actual sha=48d046208f); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-ancient-shadow-03` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=830ee66f45, QA sha=3b562cae9c, actual sha=3b562cae9c); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-ancient-marker-arrival` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=340348e285, QA sha=340348e285, actual sha=340348e285); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-crossroads-water-foam-frame-00` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=55ff3542a7, QA sha=41078a321c, actual sha=41078a321c); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-crossroads-water-foam-frame-01` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=2b790393c0, QA sha=d5faf74240, actual sha=d5faf74240); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-crossroads-water-foam-frame-02` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=bbd62fbe8d, QA sha=a45c3cf972, actual sha=a45c3cf972); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-crossroads-water-foam-frame-03` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=6a286ee519, QA sha=bbae078218, actual sha=bbae078218); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-city-hanging-sign` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=b178e82973); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-city-bunting` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=a052bfe788); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-city-vendor-cart` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=686c41e4ea); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-city-topiary` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=3aadab7f08); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-city-iron-fence` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=a14d6c243c); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-guard-booth` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=af28bce099); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-long-planter` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=c02c9cd750); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-lion-r` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=252da123b6); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-lion-l` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=f2c2600a64); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-animal-dog` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=f6bfbc4693); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-animal-butterflies` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=92e9745242); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-animal-crow` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=1092bfc69b); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-decal-cracks` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=b922f61ca0); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-decal-puddle` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=c92a6fe85f); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-decal-petals` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=846458e82c); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-decal-hopscotch` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=f3972d4874); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-decal-ruts` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=74a80fdc26); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-rug-round` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=d7db7a5c8f, QA sha=None, actual sha=d7db7a5c8f); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-rug-long` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=b03b3b27e9, QA sha=None, actual sha=b03b3b27e9); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-cage-small` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=da37fc670e, QA sha=None, actual sha=da37fc670e); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-cage-large` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=8ee3f3fd61, QA sha=None, actual sha=8ee3f3fd61); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-perch-stand` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=c9b1d6390a, QA sha=None, actual sha=c9b1d6390a); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-toy-pile` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=433ff9adc1, QA sha=None, actual sha=433ff9adc1); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-scratch-post` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=4e19fa501c, QA sha=None, actual sha=4e19fa501c); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-sleeping-01` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=50afdb5118, QA sha=None, actual sha=50afdb5118); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-sleeping-02` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=795ff7b587, QA sha=None, actual sha=795ff7b587); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-pet-shelf-alt` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=ac9480eb10, QA sha=None, actual sha=ac9480eb10); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-arena-gate` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=efd173fbe8, QA sha=None, actual sha=efd173fbe8); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-arena-judge-podium` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=2956d8b8a7, QA sha=None, actual sha=2956d8b8a7); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-arena-barrier-h` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=b516d92b13, QA sha=None, actual sha=b516d92b13); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-arena-barrier-corner` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=f86f66805e, QA sha=None, actual sha=f86f66805e); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-arena-brazier` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=1821467bf7, QA sha=None, actual sha=1821467bf7); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-arena-center-medallion-large` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=df11756baa, QA sha=None, actual sha=df11756baa); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-arena-column-short` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=e11d59b880, QA sha=None, actual sha=e11d59b880); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-throne-dais` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=4f36f4b28d, QA sha=None, actual sha=4f36f4b28d); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-window-blue` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=fec00f3097, QA sha=None, actual sha=fec00f3097); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-window-red` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=6d71dd665f, QA sha=None, actual sha=6d71dd665f); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-banner-blue-long` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=762376e0fa, QA sha=None, actual sha=762376e0fa); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-banner-red-long` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=9b0e519bf2, QA sha=None, actual sha=9b0e519bf2); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `FIX-palace-guard-statue-gold` — BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=56da17bf4c, QA sha=None, actual sha=56da17bf4c); user forbids registering/updating manifest before Claude acceptance. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-00` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-01-octopath` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-02-octopath` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-03-octopath` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-05-octopath` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-09-octopath` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-10-octopath` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-batch-13-release` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-octopath-s01-s27-20261029` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `VIEW-p01-release-art-20261023` — BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `REDRAW-gd-trunk-seg-01` — BLOCKED: later owner-approved 13d handoff says keep gd-trunk-seg-01 as the only trunk body variant; CSV redraw task is stale/conflicting. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `REDRAW-gd-trunk-seg-02` — BLOCKED: owner retired variant 02 in 13d handoff; do not redraw or load. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.
- `REDRAW-gd-seal-strip-lit` — BLOCKED: owner superseded asset with gd-seal-rune-glow; do not re-open retired strip-lit asset. Hướng xử lý: giữ ngoài canonical pack cho tới khi ràng buộc review/manifest được giải quyết; không tự đổi gate hoặc waiver.

## Tiến độ tiếp theo

- `NEW-tower-prop-08` chuyển từ PENDING sang READY_FOR_CLAUDE_REVIEW. CSV mô tả lông vũ nhưng ảnh map cho thấy dây leo/tán lá; đã tạo ứng viên dây leo rủ, 1 lần vẽ. QA: 384×384, 48 màu, alpha nhị phân, lề tối thiểu 12 px. Candidate ở `handoffs/art-submit-2026-11-10/tower/NEW-tower-prop-08/`; chưa đăng ký canonical và chưa nghiệm thu.
- Art gate chưa quét candidate vì chỉ quét canonical packs; `--all` summary hiện có không thay đổi vì không sửa pack.

## Tiến độ tiếp theo

- `NEW-tower-prop-09` chuyển sang READY_FOR_CLAUDE_REVIEW sau 3 lần vẽ; 2 ảnh đầu có haze/glow nên bị loại. Ảnh thứ ba là đèn lồng không phát sáng trên cọc cành cây, theo diễn giải dè dặt vì chi tiết cọc trong ref rất nhỏ. 384×384, 48 màu, alpha nhị phân, lề tối thiểu 12 px. Handoff ở `handoffs/art-submit-2026-11-10/tower/NEW-tower-prop-09/`; chờ Claude xem xét.

## Blocked mới

- `NEW-tower-prop-10` — CSV yêu cầu bậc thang xoắn nhưng ảnh secret-floor chỉ thể hiện cầu ván phẳng, không có cầu thang xoắn. Không thay bằng loại asset khác. Đề xuất cập nhật roadmap hoặc cung cấp ref có bậc thang trước khi vẽ.

## Failed mới

- `NEW-tower-backdrop-far-01` — ba raw ảnh đúng cảnh thác/biển mây rừng xa nhưng seam ngang sau chuẩn hóa lần lượt 19,44; 15,18; 16,82, vượt ngưỡng <14. Không nộp candidate. Đề xuất route tạo texture có kiểm soát seam; không vá ảnh bằng code.

## Failed mới

- `NEW-tower-floor-extra-01` — cả ba ảnh gỗ đạt wrap thấp (tối đa 1,74) và 48 màu, nhưng viền ngoài 8 px có 3–7 màu nên không phẳng. Không tự dựng dải viền bằng code. Đề xuất dùng workflow sinh texture có viền được kiểm soát.

## Failed mới

- `NEW-tower-floor-extra-02` — ba bố cục ván khác nhau, mỗi ảnh 48 màu và wrap thấp; viền ngoài vẫn 4–5 màu thay vì phẳng 8 px. Không nộp. Cần công cụ sinh tile kiểm soát viền.

## Failed mới

- `NEW-tower-floor-extra-03` — ba texture gỗ vân nhánh có seam tốt, 48 màu; viền 8 px vẫn từ 5 đến 48 màu, không phẳng. Không nộp; đề xuất seam/border-controlled generator.

## Failed mới

- `NEW-tower-floor-extra-04` — ba texture rêu/vỏ cây, wrap dưới 1,15 và 48 màu; viền 8 px có 4–11 màu. Không có candidate đạt.

## Failed mới

- `NEW-tower-floor-extra-05` — ba biến thể gỗ lichen đạt wrap thấp, 48 màu; viền 8 px có 4–10 màu, không phẳng. Không nộp.

## Failed mới

- `NEW-tower-floor-extra-06` — ba tile đất/rễ có wrap thấp (≤1,97), 48 màu; dải biên có 3–7 màu, không đáp ứng viền đơn sắc 8 px. Không nộp.

- `NEW-tower-edge-01` — ba ảnh có seam màu 0–6,65, 44–46 màu nhưng cụm lá lặp nhịp rõ; autocorr proxy 0,666–0,698 vượt 0,25. Không nộp candidate.

- `NEW-tower-edge-02` — attempt 1 transparent but pattern lặp; attempts 2–3 có nền/tràn trắng, seam 15,47 và 32,87. Không nộp.

- `NEW-tower-edge-03` — ba dải rễ đạt seam 1,71–6,50, 44–45 màu nhưng hình rễ/lá lặp; autocorr proxy 0,650–0,695 >0,25. Không nộp.

- `NEW-tower-decal-01` — hai lần có glow/haze, lần giữa có viền đỏ và quá nhiều mảnh vụn. Không chọn candidate.

- `NEW-tower-decal-02` candidate selected on attempt 2 after thresholding semi-transparent haze; 384×384, 46 colors, binary alpha, 12px margin.

- `NEW-tower-decal-03` — ba ảnh đều có glow; attempt 2–3 gần như không có pixel opaque. Không nộp.

- `NEW-tower-decal-04` candidate attempt 3: leaf/bark scatter, 384×384, 48 colors, binary alpha, 12px margin; attempts 1–2 rejected for glow.

- `NEW-tower-decal-05` candidate attempt 1: pebble/moss scatter, 384×384, 47 colors, binary alpha, 12px margin; attempts 2–3 rejected for glow.

- `NEW-tower-decal-06` candidate attempt 3: moss/leaf scatter, sparse decal, 384×384, 48 colors, binary alpha, 12px margin.

- `NEW-tower-decal-07` — attempts 1–2 glow; attempt 3 yielded grains too tiny to read after alpha cleanup. No candidate.

- `NEW-tower-decal-08` candidate attempt 1: broken wood abrasion with lichen, 384×384, 47 colors, binary alpha, 12px margin; 3rd attempt glow rejected.

## PENDING

Còn 476 task PENDING; chúng vẫn có dòng ledger riêng. Tiếp tục từ task PENDING đầu theo thứ tự milestone/order của roadmap.

## Art handoff

- Desert M3 landmark candidates: `.ai/design/map-checklists/handoffs/art-submit-2026-11-10/desert/` (6 desert candidates with `montage-current-6.png`). Forest M3: 2 candidates with `montage-current-2.png`; ship M3: 1 candidate with `landmark-preview.png`. Folders include raw, prompt/review, QA, and previews.
- Ledger đầy đủ: `.ai/design/map-checklists/CODEX-LEDGER-2026-11-10.csv`.
- Toàn bộ output `art_gate.py --all`: xem kết quả tóm tắt ở `.ai/design/map-checklists/handoffs/art-submit-2026-11-10/art-gate-all-summary.md`.


## Tiến độ tiếp tục ngày 2026-11-10

Ledger vẫn có 672 task, mỗi task đúng một dòng. Tiến độ mới của lượt tiếp tục: 77 READY_FOR_CLAUDE_REVIEW, 65 FAILED_AFTER_3_TRIES, 63 BLOCKED, 467 PENDING.

- Candidate mới: `NEW-tower-decal-09`, `NEW-tower-decal-12`, `NEW-tower-shadow-04`; đều handoff-only, chưa đăng ký và chờ Claude review.
- FAILED_AFTER_3_TRIES: `NEW-tower-decal-10` (viền đỏ / nền haze), `NEW-tower-decal-11` (ba ảnh nền gradient opaque), `NEW-tower-shadow-01` (bóng mờ như khói), `NEW-tower-shadow-02` (không có silhouette pixel-art rõ), `NEW-tower-shadow-03` (hai ảnh mờ, một ảnh viền xanh sáng). Chi tiết theo từng `review.md` trong thư mục tower.
- BLOCKED: `NEW-tower-backdrop-far` — image generation trả `usage_limit_reached` trước attempt 3. Hai ảnh raw đã lưu; seam sau resize + quantize 48 màu lần lượt 17.89 và 21.59 (>14), autocorrelation max lag 8–255 lần lượt 0.756 và 0.638. Không có candidate. Cần tiếp tục sau khi quota reset.
- Art gate toàn bộ vẫn là lần chạy đã ghi ở trên: exit 1; 33 pack, 1,434 assets, 367 lỗi, 0 cảnh báo. Handoff candidate chưa được manifest quét; không có thay đổi canonical nào trong lượt này.


## Tạo ảnh tiếp sau quota giới hạn

- `NEW-tower-backdrop-far` được thử lần 3 qua một công cụ tạo ảnh đã kết nối. Seam 20.01, autocorrelation max 0.869; vẫn không đạt và đã chuyển thành `FAILED_AFTER_3_TRIES`.
- Bắt đầu `NEW-tower-backdrop-mid` bằng một raw mới; tác vụ tạo ảnh đang chạy.
- Nguồn tạo ảnh mặc định vẫn đang bị quota limit tới 2026-11-11 03:48 UTC. Công cụ tạo ảnh kết nối còn 492 credit tại thời điểm cập nhật.
