# S23–S24 run-strip review — Codex — 2026-10-30

Scope: the 24 currently delivered `player-*` / `walker-*` run strips in this delivery. I read the full `REVIEW-QUEUE.md`, each strip QA JSON, each eight-frame review sheet, and each available frame-1/frame-5 comparison. This is a review note only; no source PNG, QA, checklist, approval field, or public asset was changed.

## Decision summary

- **Request Claude review now:** 22 existing strips are reviewable without new drawing. The seven QA `pass` strips are the cleanest candidates. Warning-only strips remain reviewable with their mechanical caveats below. `player-male.run` is specifically cleared by manual frame-1/frame-5 inspection: opposite side-run contact legs are visible, and the eight frames retain a stable scale/root.
- **Regenerate before Claude review:** `walker-elder.run` and `walker-traveller.run`. Both show the same side-run contact-leg lead in frames 1 and 5 (and the QA confirms repeated half-cycle poses). This is a visible gait failure, not merely a luminance-classifier unknown.
- **Do not redraw solely from the numeric fail:** `walker-guard.run` and `walker-guard.run-up`. The QA flags head ratios outside its 0.95–1.05 band, but visual sheets do not show a clear head-scale jump; on the up-facing strip, the head band/spear-tip geometry can contaminate the detector. Keep these as targeted Claude review items and ask specifically about head scale/root consistency. `walker-guard.run` also has a mixed leg-alternation warning, but the full strip visibly includes alternating leg poses.

## Candidate inventory

| Candidate | QA | Visual disposition |
|---|---|---|
| `player-female.run-down` | pass | Ready for Claude review. Repeated frame silhouettes form a readable down-run; no visible attachment or registration defect. |
| `player-female.run-up` | warn: seam | Ready with loop-seam check. Head/body scale appears stable; seam warning alone does not demonstrate bad art. |
| `player-female.run` | needs-visual-review: leg alternation unknown | Ready for Claude review. The auto-luminance test cannot identify NEAR/FAR; the frame-1/5 view is still ambiguous to me, so owner should confirm contact-leg opposition. No clear duplicate-half cycle can be asserted visually. |
| `player-male.run-down` | pass | Ready for Claude review. Readable, stable down-run. |
| `player-male.run-up` | warn: seam | Ready with loop-seam check; no clear scale/root defect in the sheet. |
| `player-male.run` | needs-visual-review: leg alternation unknown | Ready for Claude review. Frame 1 has the brown/near leg forward and blue/far leg trailing; frame 5 reverses that relationship. All eight bodies remain about 166–168 px tall at a 167 px target; no detached alpha specks. This manual check resolves the stated heuristic unknown for review, without changing QA approval. |
| `walker-baker.run-down` | warn: near duplicates | Ready with duplicate-frame check. There is visible step change, no obvious frozen or broken root. |
| `walker-baker.run-up` | warn: seam | Ready with loop-seam check. Frames are close but still show leg motion. |
| `walker-baker.run` | warn: mixed leg alternation | Ready with gait check. Manual sheet shows opposing contact poses, including frame 1 versus frame 5; some intermediate pairs are similar, consistent with the mixed warning. |
| `walker-boy.run-down` | pass | Ready for Claude review. Clear alternating step poses and stable small-body scale. |
| `walker-boy.run-up` | warn: near duplicates, seam | Ready with frame-distinction and loop checks. No obvious scale/root defect. |
| `walker-boy.run` | warn: seam | Ready with loop check; side gait visibly alternates. |
| `walker-elder.run-down` | warn: seam | Ready with loop check; no clear hard defect in static review. |
| `walker-elder.run-up` | pass | Ready for Claude review. Readable alternating rear-view steps; cane remains present. |
| `walker-elder.run` | fail: duplicated half-cycle | **Regenerate.** Frame 1 and frame 5 repeat the same forward/support-leg relationship; QA's near/near sequence and high half-cycle overlap agree with the image. |
| `walker-girl.run-down` | warn: near duplicates | Ready with frame-distinction check; visible step variation remains. |
| `walker-girl.run-up` | pass | Ready for Claude review. Stable rear-view scale and leg motion. |
| `walker-girl.run` | warn: mixed leg alternation | Ready with gait check. Full sheet shows alternating contacts; classifier warning is not enough to require new art. |
| `walker-guard.run-down` | pass | Ready for Claude review. Spear and body are stable across the frames. |
| `walker-guard.run-up` | fail: identity head ratio, seam | Targeted Claude review, not a confirmed redraw. QA reports 1.06 at frames 5–6, but the eight-frame sheet has no obvious enlarged head; the tall spear/head-band silhouette may confuse measurement. Verify against original identity and loop before deciding. |
| `walker-guard.run` | fail: identity head ratio; mixed leg alternation | Targeted Claude review, not a confirmed redraw. QA head ratios dip to 0.939 in frames 1, 2, and 5, while the eight-frame sheet shows no unmistakable head-size discontinuity and does show alternating leg poses. Confirm visually before spending on new art. |
| `walker-traveller.run-down` | warn: near duplicates | Ready with frame-distinction check; the walking/running poses remain visibly distinct. |
| `walker-traveller.run-up` | pass | Ready for Claude review. Stable scale/root and readable rear-view steps; staff remains present. |
| `walker-traveller.run` | fail: duplicated half-cycle, seam | **Regenerate.** Frames 1 and 5 retain the same leading-leg pose; the full strip repeats that side-run contact pattern and QA independently reports same-leg lead across both half cycles. |

## Criteria and limits

- All reviewed strips are 1536×192: eight 192×192 cells, 48 colors, binary alpha, pivot [96,184]. Their QA registration records one shared uniform scale and translation-only placement; no per-frame warp/flip/synthesis. Measured body heights stay close to each asset's target. The guard ratio failures are image-analysis outliers, not proof of changed registration scale.
- Hard evidence for new art is the visible repeated side-run leg lead on elder and traveller, corroborated by their QA `leg_alternation: fail`. Numeric seam, near-duplicate, or luminance-only warnings do not by themselves prove an asset is unusable.
- No candidate is `approved:true`; the seven QA passes mean no automated flags, not release approval. The report only recommends what is ready to show Claude.
- References: `REVIEW-QUEUE.md`; per-asset `delivery/*.run*.qa.json`, `*.review.png`, and `*.contact-1-5.review4x.png`. No install/publication performed.
