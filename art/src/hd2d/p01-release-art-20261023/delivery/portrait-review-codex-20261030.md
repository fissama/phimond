# Codex visual review — NPC portraits and starter selects — 2026-10-30

Scope: current delivery PNGs and their existing contact/review images only. This is an additional visual review; it does not replace Claude/owner approval and does not set any QA file to `approved:true`.

## Six portraits previously missing from the contact-sheet review

Reviewed `portrait-six-pending-review.png` against the per-file 4× previews and prompt identity constraints:

- `portrait-bia_free.png`: readable woman vendor with flower basket; no clear identity/composition defect.
- `portrait-gate_guild.png`: readable armored guild guard; no clear identity/composition defect.
- `portrait-sq_exchange.png`: merchant with scales and trade goods; no clear identity/composition defect.
- `portrait-sq_mailbox.png`: mailbox object portrait, intentionally not a human per its prompt; the image matches that contract.
- `portrait-sq_skill.png`: older red-robed sage with travel pack; no clear identity/composition defect.
- `portrait-sq_warehouse.png`: warehouse worker carrying a crate; no clear identity/composition defect.

All six existing QA JSONs report 256×256, 48 colors, `partial_alpha: 0`, and retain `approved:false/status:needs_visual_review`. This visual inspection found no defect that justifies redrawing them. **State: visually reviewed by Codex; Claude/owner approval pending.**

## Three large starter portraits

Reviewed current `starter-tien_chuong.review.png`, `starter-sa_hat.review.png`, and `starter-xich_ung.review.png`. All three have coherent, legible monster identities and no obvious crop or silhouette defect. Their QA files report 512×512, 48 colors, `partial_alpha: 0`, but still say `approved:false/status:needs_visual_review`. Earlier checklist approval conflicts with the current per-image envelope, so this review does not restore the approval mark.

**State: visually reviewed by Codex; Claude/owner approval pending for the current delivered versions.**

## Limits

Review was against source previews at enlarged scale, not in the game UI or at production display scale. No portrait was edited or installed. Exact QA records remain beside each PNG.
