# Garden-B repairs + C05 handoff — 2026-11-10

## State

Incomplete. Built-in ImageGen returned HTTP 429 `usage_limit_reached` on the Rose plant-row edit request. Response reported `resets_in_seconds=63016` (about 17 h 30 min at that response). Per Master v2, no alternate generator or code-drawn art was used.

## A — plant-row repairs

| Asset | Current measurements | Task-specific result |
|---|---|---|
| cr-hoa-hong | Existing a–j 10/10; ripe 150 px; plant/sprout IoU 0.8819 | FAIL: plant row is not seed → sprout; also exceeds C04 ripe ≤148 px margin. Row 5 unchanged. |
| cr-dua-hau | Existing a–j 10/10; ripe 131 px; plant/sprout IoU 0.8436 | FAIL: old row 5 starts with a small character, not a seed in soil. Row 5 unchanged. |
| cr-khoai-mon | Existing final 8/10; ripe 117–119 px (<120); min loop IoU 0.7774 (<0.85). raw-04 pack failed: no common scale ≥0.6 fits safe bounds. | FAIL; redraw/pack needed. |

For Rose and Watermelon, `reference-sprout-f1.png` was cut from current packed sprout f1 and attached alongside the atlas to an ImageGen edit request. The request was rejected before output; no row was changed. SHA256 values are recorded in each `prompt.md`.

## B — pot repairs

| Asset | Latest measures | Result |
|---|---|---|
| pot-g2b-truc-dong | g FAIL: body IoU 0.9055 (<0.95); joins min 0.9495 (>=0.93); wet soil darkening 4.54% (<15%). Idle/wet body 149–151 × 92 px. | FAIL |
| pot-g4b-linh-thach | g FAIL: body IoU 0.7703; wet soil 30.45%; width 94–128 px (<130). j=0.6766. raw-04 pack failed: no common scale ≥0.6 fits safe bounds. | FAIL |
| pot-g5a-dong-co | g FAIL only soil: body IoU 0.9793; joins min 0.9665; darkening 11.34% (<15%). Size 157–158 × 98 px. | FAIL |
| pot-g5b-tinh-mach | g FAIL: body IoU 0.4441; joins min 0.9204; darkening 6.97%; size 118–120 × 119–120 px. | FAIL |

## C — batch C05

Read `.ai/design/gpt-redo/20-batch-C05-prompt.md`, Đơn 16, crop prompt v2, roster v2, and approved pilot references. No C05 raw art or atlas was generated: ImageGen is unavailable until the tool limit resets. Required assets remain: `cr-ngai-cuu`, `cr-nghe`, `cr-du-du`, `cr-hoa-sung`, `cr-oi`. Plant row must be seed → sprout, never a mature starting pose.

## Files changed for this continuation

- `cr-hoa-hong/reference-sprout-f1.png` and `cr-dua-hau/reference-sprout-f1.png` (cropped frame references only).
- `cr-hoa-hong/prompt.md`, `cr-hoa-hong/review.md`, `cr-dua-hau/prompt.md`, `cr-dua-hau/review.md` (record requested row-5 edit, reference hash, and rejected tool call).
- `manifest.json` marks the two plant-row assets blocked and retains `approved:false`; previously Claude-approved assets were not modified.
