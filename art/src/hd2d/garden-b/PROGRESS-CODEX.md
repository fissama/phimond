# Garden-B art progress — Codex

Updated: 2026-11-12 (continuation)

## Current task and stop condition

The requested work is: plant repairs for Hoa Hồng, Dưa Hấu, Khoai Môn; pot repairs for Trúc Đồng, Linh Thạch, Đồng Cổ, Tinh Mạch; then C05 → C12 in order. No approval is assigned by Codex. Built-in ImageGen is required; do not switch generators or draw/patch pixels in code.

## ImageGen quota state

Built-in ImageGen is available again; the previous Hoa Hồng request had returned HTTP 429 before reset.

- Reset time 2026-11-11 03:48:12 UTC has passed; image generation works in this continuation.

## Ordered work state

| Order | Item | State | Latest measurement / next action |
|---:|---|---|---|
| 1 | `cr-hoa-hong` plant row 5 only | DONE, 4 ImageGen outputs | `raw-10.png` packed and measured: 10/10; h=0.8823; loop min 0.9216; ripe max 150 px. Status ready_for_claude_review, approved:false. |
| 2 | `cr-dua-hau` plant row 5 only | BLOCKED after 8 ImageGen outputs | Latest raw-09: a–g/i PASS; h=0.5710 (<0.80), j=0.8458 (<0.85). Heights sprout 65–66, grow 106–107, ripe 140–141; max width 136. ImageGen regenerated rows 1–4 despite edit-only instruction. Details in asset review and qa.json. |
| 3 | `cr-khoai-mon` | DONE, 2 new ImageGen outputs | `raw-06.png` passes 10/10: ripe=130 px, max width=131, h=0.9336, loop min=0.8661. Status ready_for_claude_review, approved:false. |
| 4 | `pot-g2b-truc-dong` | BLOCKED after 8 ImageGen outputs | Latest raw-29: body IoU min=0.9451 (<0.95), join min=0.9748, soil darkening=2.78% (<15%), bbox 155×109 (requested width 130–158, height 70–100). Continue to Linh Thạch. |
| 5 | `pot-g4b-linh-thach` | DONE, 4 new ImageGen outputs | `raw-08.png` passes 10/10: body IoU min=0.9682, join min=0.9699, soil darkening=47.16%. Status ready_for_claude_review, approved:false. |
| 6 | `pot-g5a-dong-co` | DONE, 1 new ImageGen output | `raw-02.png` passes 10/10: darkening=15.15%, adjacent body IoU min=0.9529, body 157×99. Status ready_for_claude_review, approved:false. |
| 7 | `pot-g5b-tinh-mach` | BLOCKED after 8 ImageGen outputs | Latest raw-11: body IoU min=0.9499 (<0.95); join min=0.9495; soil darkening=6.84%; body 126×119 px (required 130–158×70–100). Continue to C05. |
| 8 | C05 — Ngải Cứu, Nghệ, Đu Đủ, Hoa Súng, Ổi | COMPLETE WITH BLOCKERS | All five assets have final files and a–j measurements. `cr-ngai-cuu`, `cr-nghe`, `cr-du-du`, `cr-hoa-sung`, and `cr-oi` are marked blocked on visual contour fringe and/or a failed gate. `cr-du-du` raw-06, `cr-hoa-sung` raw-03, and `cr-oi` raw-07 pass mechanical a–j; each retains the measured visual blocker. Contact sheet refreshed. Proceeding to C06. |
| 9 | C06 — Riềng, Mướp Đắng, Kỷ Tử, Hoa Mai, Xoài | COMPLETE WITH BLOCKERS | All five have final/QA/reviews and retained outputs. Riềng h=0.7752; Kỷ Tử width=144 px; Mướp Đắng/Hoa Mai pass mechanical gates but visual fringe remains; Xoài raw-03 passes 10/10 mechanically but has visible fringe. Eight image outputs used per asset. |
| 10 | C07 — Sắn, Nấm Đầu Khỉ, Hoa Sen, Bưởi, Tam Thất | COMPLETE WITH BLOCKERS | All five have candidates, measurements, and visual reviews; persistent contour fringe and/or gate failures are recorded after the per-asset attempt limits. |
| 11 | C08 | COMPLETE WITH BLOCKERS | Dừa, Hoa Đào, Mít, Linh Chi, Chôm Chôm have candidates, reviews, and measurements; all blockers are documented after eight outputs. |
| 12 | C09 | COMPLETE WITH BLOCKERS | Five roster crops are present; visual contour failures and Thanh Long gate h failure are documented. |
| 13 | C10 | COMPLETE WITH BLOCKERS | Five crops are on disk. Sầu Riêng fails visual identity and contour review; remaining candidates are documented in reviews. |
| 14 | C11 | COMPLETE WITH BLOCKERS | Five crops have final/QA/review files. Thạch Anh Quả and Cà Phê were missing manifest records; both are now recorded blocked on visual fringe. |
| 15 | C12 | COMPLETE WITH BLOCKERS | Hồ Tiêu, Địa Mạch Kết Tinh, and Linh Mạch Mầm have candidates, QA, reviews, previews, and manifest entries. Each reaches 10/10 mechanical checks on the selected candidate but remains visually blocked by violet/magenta contour fringe after 8 outputs. |

## Already completed / preserve

- Garden-A kit and previously approved garden-B assets remain untouched in this task.
- Claude-approved assets specifically protected by the request: `cr-bi-do`, `cr-la-lot`, `pot-g3b-sanh-nau`, `pot-g4a-lam-su` (manifest status `approved_claude_20261110`).
- The two extracted sprout references for Hoa Hồng and Dưa Hấu exist. Do not regenerate them unless their source atlas changes.
- Current manifest contains 45 atlas records after adding Hoa Sen. C05/C06 and the first three C07 crops have blockers; contact sheet was regenerated after Hoa Sen and needs visual inspection. Continue C07–C12 in order.

## Continuation additions (2026-11-11)

- `cr-ngai-cuu`: 8 ImageGen outputs stored. raw-08 passes a–j (sprout/grow/ripe 65/100/142 px; width 115 px; h=0.8082; loop min=0.9307), but manual visual inspection sees purple/magenta contour fringe. A separate read-only scan found 4,856 opaque purple-like pixels. Marked `blocked_imagegen_limit`; do not exceed 8 attempts.
- `cr-ngai-cuu` folder includes final/anim/prompt/review/qa, all row PNG/GIFs, preview-anim.gif, 4× checker/dark, pivot grid and retained raw-01..08.
- Contact sheet regenerated after adding Ngải Cứu and Nghệ; visually inspect after current C05 updates.

## Resume checklist

1. Hoa Hồng is done. Dưa Hấu exhausted its eight output allowance with measured h/j failures; continue to Khoai Môn per the instruction to proceed after an exhausted item.
2. For remaining items, preserve raw files, use `pack_atlas.py` and `measure_atlas.py`, and record every result. Do not mark an asset ready unless all required mechanical and task-specific criteria pass.
3. Execute C05, C06, … C12 sequentially from the prompt files. For each batch, provide the required atlas files/previews, review the images, update QA and manifest with `approved:false`, then update the contact sheet and this progress file before the next batch.
4. Leave all existing `approved_claude_20261110` assets unchanged.

- `cr-nghe`: selected raw-05 after 8 atlas-sheet outputs; 9 ImageGen calls total including standalone sprout reference. Best gates a–g/i/j pass, h=0.7640; visual magenta fringe 17,634 pixels. Blocked, no further ImageGen calls.
- `cr-du-du`: kept raw-01..07 plus the sprout reference. The best mechanical candidate is raw-06; its measured gates all pass but manual 4× inspection shows purple contour fringe. An HSV scan of non-key pixels found 7,871 purple-like pixels. All 8 calls (1 reference + 7 sheets) are used, so status is `blocked_imagegen_limit`; no pixel edits.
- `cr-hoa-sung`: kept raw-01..08. Best mechanical candidate raw-03 passes a–j, but 4× views show pink-violet contour fringe; the edge scan found 17,236 purple-like non-key boundary pixels. After 8 atlas outputs, status is `blocked_imagegen_limit`. Continue to Ổi.
- `cr-oi`: kept raw-01..08 and both sprout crops. Raw-07 passes a–j (heights 61/91–93/129–130, width 121, h=0.8934, j=0.9180) but the 4× preview shows pink-purple fringe; boundary scan found 6,826 purple-like pixels. All 8 outputs used; status `blocked_imagegen_limit`.

## Continuation — 2026-11-12

- Bưởi (`cr-buoi`): completed metadata and visual review. raw-08 passes 10/10 mechanically (51 colors; stage heights 68/105–106/149–150; width 131; h=.9254; loop min .9042), but opened dark 4× view shows clear magenta/pink contour fringe. Manifest status `blocked_imagegen_limit`, 8 outputs.
- Tam Thất (`cr-tam-that`): 8 outputs saved. Best raw-07 selected; passes 8/10 (57 colors; heights 60–63/102/137–140; width 139; e pass; h=.7095; j=.8451). Opened checker and dark previews; magenta/purple outline fringe visible. Manifest status `blocked_imagegen_limit`.
- Contact sheet regenerated and visually inspected; now includes 47 existing finals including Bưởi and Tam Thất.
- C08 started with Dừa (`cr-dua`): raw-01 pack failed; raw-02 measured 8/10 (60 colors; heights 88–95/111–119/145–150; width 126; h=.9500; j=.8094). On third ImageGen call received HTTP 429 `usage_limit_reached`; no new output was produced. Reset reported at 2026-11-12 03:48:46 UTC. Continue Dừa from raw-03 after reset, then finish C08 in listed order, then C09–C12. No commits; no approved flags added.
- After adding provisional Dừa, regenerated contact sheet again and opened it; all current manifest finals including Dừa and Tam Thất are present. Dừa candidate remains in progress, not represented as approved.
- Resumed after reset. `cr-dua` used outputs raw-03..08; selected raw-07 after repacking. It passes a–j (60 colors; heights 58–60/95–97/150; width 138; h=.8307; loop min .8766), but opened dark 4× preview still has visible magenta/purple fringe. All eight outputs exhausted; status `blocked_imagegen_limit`. Next: C08 Hoa Đào.
- C08 `cr-hoa-dao`: eight outputs, best raw-07 passes 9/10; loop IoU=.8163 (<.85). 4× preview was opened and is visually clean apart from intended peach tones; blocked after 8 outputs on gate j. Next: Mít (`cr-mit`).
- C08 `cr-mit`: eight outputs; selected raw-06 passes 9/10, h=.6919 (<.80), heights 68/98/130–131, width138, loop min .9719. Opened 4× preview shows vivid magenta/purple outline fringe. Status `blocked_imagegen_limit`; next: Linh Chi (`cr-linh-chi`).


## Continuation — C08 Linh Chi and Chôm Chôm (2026-11-12)

- `cr-linh-chi`: used 8 ImageGen outputs. Selected `raw-03.png` as highest gate count, 9/10: f fails with ripe=114 px and max width=145; a–e, h, i, j pass. 4× dark preview shows magenta/purple outline fringe. Blocked.
- `cr-chom-chom`: used 8 ImageGen outputs including one standalone sprout reference. Selected `raw-07.png`, 9/10 after adding face notes; h=.5159 fails, other mechanical gates pass (sprout 57–58, grow 103–104, ripe 150, width 134, loop min .9552). Dark 4× preview shows magenta contour pixels. Blocked.
- Both have `final.png`, raw sources, anim/prompt/review/qa, row previews/GIFs, checker/dark/pivot previews. Contact sheet refreshed after both were added. C08 closed with blockers; continue C09.


## Continuation — C09 audit and C10 (2026-11-12)

- Corrected C09 manifest entries for Nhân Sâm, Thanh Long, Ngân Nhĩ, Măng Cụt after comparing each `qa.json` packed source and final SHA. All four now show `blocked_imagegen_limit` because the 4x dark previews visibly contain violet/magenta contour pixels; Thanh Long also fails h (IoU 0.7011).
- Hoa Quỳnh: raw-08 selected after 8 outputs; 10/10 mechanical checks, h=.9483, loop min=.9681; dark 4x shows violet/magenta contour. Manifest now correctly blocked.
- Đông Trùng Hạ Thảo: 8 ImageGen outputs. raw-08 passes 10/10 (54 colors; heights 54/60/55/55, 93/93/93/93, 150/150/145/150; width 81; h=.8607; loop min=.8675), but its dark 4x preview shows violet/magenta contour. Marked blocked; next is Vải Thiều.
- Contact sheet refreshed with 58 manifest assets and opened for inspection.


## Continuation — C12 and manifest audit (2026-11-12)

- `cr-ho-tieu`: selected `raw-08.png`; 10/10 mechanical checks, 58 colors; stage heights 74 / 104–111 / 135–139 px; width 127; plant IoU .9246; loop min .8839. Opened 4× dark preview: visible violet/magenta contour fringe. Blocked after 8 outputs.
- `cr-dia-mach-ket-tinh`: selected `raw-07.png`; 10/10 mechanical checks, 59 colors; heights 57 / 93 / 133–134 px; width 130; plant IoU .9650; loop min .9072. Opened dark preview: visible violet/magenta contour fringe. Blocked after 8 outputs.
- `cr-linh-mach-mam`: 8 ImageGen outputs retained. Selected `raw-06.png`; all a–j pass: 60 colors; heights 60 / 103 / 150 px; width 128; plant IoU .9560; loop min .9735. Opened dark 4× preview: violet/magenta fringe remains on contours. Blocked after 8 outputs. Raw-05 removed fringe in appearance but failed f (sprout 84 px, width 160); raw-07 failed f/h; raw-08 failed h (0.6235) and width (160).
- Manifest now contains 70 atlas entries. Registered previously missing entries `cr-sau-rieng`, `cr-thach-anh-qua`, `cr-ca-phe`, `cr-ho-tieu`, `cr-dia-mach-ket-tinh`, and `cr-linh-mach-mam`, all `approved:false`. C11 missing records are restored.
- Audited `cr-sau-rieng/raw-08.png` directly: it depicts a flower-headed warrior with sword and shield, not a durian spirit; dark 4× preview also shows magenta fringe. Updated `review.md` and marked blocked.
- Regenerated and opened `contact-sheet.png`; it contains all 70 manifest entries and is newer than `manifest.json`.
- No commit, runtime/client edits, gate changes, pixel retouching, or approved flags were made.

## Metadata and sidecar repair — 2026-11-12

- `cr-ky-tu` was missing `anim.json`, `prompt.md`, and visual preview exports. Restored animation metadata and a provenance prompt record from the C06 source brief, its retained `raw-03.png`, and the existing pilot references; exported row PNG/GIF previews plus checker/dark/pivot review images from its unchanged `final.png`. Its actual blocker remains width=144 px and visible fringe; no art was modified.
- Corrected `pot-g5b-tinh-mach` manifest SHA-256 to match its unchanged final PNG.
- Final audit: all 70 manifest finals exist and match SHA-256; no non-Claude-approved entry is marked approved; all 70 have `anim.json`, `prompt.md`, `review.md`, and `qa.json`; all 70 have five row PNG/GIF previews; contact sheet has 70 tiles, was opened for visual inspection, and is newer than the manifest. `cr-ky-tu` remains blocked (mechanical 9/10, width 144 px, visual fringe).

## Current delivery state

The ordered repair items and batches C05–C12 have candidates and recorded outcomes. The remaining blockers are listed per asset in manifest/review files; numerous candidates fail visual outline/style requirements despite passing mechanical checks, and some retain numeric gate failures after eight outputs. They are not presented as approved or as 100% visually complete.

## Continuation — defringe rollout, repairs, and full remeasure (2026-11-13)

- Added `tools/defringe.py`; `pack_atlas.py` applies the requested edge-only purple/magenta replacement before shared palette reduction and records per-frame plus total before/after counts in `qa.json`. It also writes 3× dark before/after previews. `measure_atlas.py` preserves the packing/defringe provenance when refreshing measurements. The three focused defringe unit tests passed in the prior continuation.
- Part 1b repacked the 56 eligible existing/blocked assets and saved `final-before-defringe.png` comparison copies; all 70 atlas QA files now contain edge counts. The last missing comparison backup (`cr-dua-hau`) was recovered from its preserved pre-pipeline final.
- Repacked the 14 current repair candidates from the selected raws listed in their `qa.json` and `prompt.md`, regenerated visual previews for all 70 assets, then ran `measure_atlas.py` for every manifest entry. Aggregate result: 56/70 currently pass all mechanical a–j gates; 14/70 fail at least one gate. The count includes already Claude-approved records whose unchanged approval status was preserved.
- Newly ready for Claude (mechanical gates pass and dark-preview purple-edge count is zero): `cr-ngai-cuu`, `cr-oi`, `cr-muop-dang`, `cr-hoa-mai`, `cr-san`, `cr-hau-dau-co`, `cr-buoi`, `cr-dua`, `cr-nhan-sam`, `cr-dong-trung-ha-thao`, `cr-vai`. Existing Claude-approved records remain `approved:true` with their prior status; no new record was marked approved.
- The four Part 4 identity checks are documented in their `review.md`: character and face read; the remaining observed issue is a visible magenta/violet contour fringe, so no identity redraw was attempted.
- Rebuilt and opened `contact-sheet.png`; it contains all 70 manifest assets. Per-asset before/after pixel counts, mechanical summary, and status are in `DEFRINGE-REPORT-20261113.md`.

### Remaining non-approved blockers

- `pot-g2b-truc-dong` — g soil darkening=2.80%, min body IoU=0.9451; purple edge pixels remain=2866.
- `cr-dua-hau` — h IoU=0.5710 <0.80; j min loop IoU=0.8458 <0.85; purple edge pixels remain=4642.
- `pot-g5b-tinh-mach` — All mechanical gates pass, but dark-preview review still has 16475 purple-hued opaque edge pixels..
- `cr-nghe` — h IoU=0.7640 <0.80.
- `cr-du-du` — All mechanical gates pass, but dark-preview review still has 1201 purple-hued opaque edge pixels..
- `cr-hoa-sung` — All mechanical gates pass, but dark-preview review still has 2256 purple-hued opaque edge pixels..
- `cr-rieng` — h IoU=0.7752 <0.80; purple edge pixels remain=1446.
- `cr-ky-tu` — f stage heights={'1': [70, 72, 70, 70], '2': [95, 96, 95, 95], '3': [121, 120, 121, 120]}, width=144 px; purple edge pixels remain=1853.
- `cr-xoai` — All mechanical gates pass, but dark-preview review still has 2596 purple-hued opaque edge pixels..
- `cr-hoa-sen` — All mechanical gates pass, but dark-preview review still has 1 purple-hued opaque edge pixels..
- `cr-tam-that` — h IoU=0.6798 <0.80; purple edge pixels remain=389.
- `cr-hoa-dao` — f stage heights={'1': [76, 76, 76, 76], '2': [95, 97, 97, 96], '3': [121, 122, 124, 121]}, width=116 px; purple edge pixels remain=3747.
- `cr-mit` — h IoU=0.6799 <0.80; purple edge pixels remain=2711.
- `cr-chom-chom` — h IoU=0.6272 <0.80; purple edge pixels remain=3717.
- `cr-linh-chi` — All mechanical gates pass, but dark-preview review still has 4545 purple-hued opaque edge pixels..
- `cr-hoa-lan` — All mechanical gates pass, but dark-preview review still has 7631 purple-hued opaque edge pixels..
- `cr-thanh-long` — All mechanical gates pass, but dark-preview review still has 612 purple-hued opaque edge pixels..
- `cr-ngan-nhi` — All mechanical gates pass, but dark-preview review still has 630 purple-hued opaque edge pixels..
- `cr-mang-cut` — All mechanical gates pass, but dark-preview review still has 5200 purple-hued opaque edge pixels..
- `cr-ho-phach-mam` — h IoU=0.6041 <0.80.
- `cr-hoa-quynh` — All mechanical gates pass, but dark-preview review still has 3394 purple-hued opaque edge pixels..
- `cr-nguyet-huynh-tinh` — All mechanical gates pass, but dark-preview review still has 2403 purple-hued opaque edge pixels..
- `cr-tuyet-lien` — All mechanical gates pass, but dark-preview review still has 2189 purple-hued opaque edge pixels..
- `cr-tinh-hoa-lien` — All mechanical gates pass, but dark-preview review still has 2086 purple-hued opaque edge pixels..
- `cr-sau-rieng` — i face/blink annotation gate failed.
- `cr-thach-anh-qua` — All mechanical gates pass, but dark-preview review still has 3805 purple-hued opaque edge pixels..
- `cr-ca-phe` — All mechanical gates pass, but dark-preview review still has 3446 purple-hued opaque edge pixels..
- `cr-ho-tieu` — All mechanical gates pass, but dark-preview review still has 1356 purple-hued opaque edge pixels..
- `cr-dia-mach-ket-tinh` — All mechanical gates pass, but dark-preview review still has 4753 purple-hued opaque edge pixels..
- `cr-linh-mach-mam` — All mechanical gates pass, but dark-preview review still has 1343 purple-hued opaque edge pixels..

### Purple-hued edge pixel counts (before → after)

| Asset | Before | After | Gates | Status |
|---|---:|---:|---:|---|
| `cr-bac-ha` | 7753 | 3161 | 10/10 | approved_claude_20261110 |
| `cr-ca-chua` | 5845 | 0 | 10/10 | approved_claude_20261110 |
| `cr-chuoi` | 7571 | 2885 | 10/10 | approved_claude_20261110 |
| `cr-cu-dau` | 10033 | 4364 | 10/10 | approved_claude_20261110 |
| `cr-cuc-hoa` | 7000 | 3742 | 10/10 | approved_claude_20261110 |
| `cr-gung` | 7951 | 2370 | 10/10 | approved_claude_20261110 |
| `cr-hoa-giay` | 11054 | 5408 | 10/10 | approved_claude_20261110 |
| `cr-huong-co` | 8659 | 7372 | 10/10 | approved_claude_20261110 |
| `cr-huong-duong` | 5730 | 0 | 10/10 | approved_claude_20261110 |
| `cr-khoai-lang` | 10113 | 4456 | 10/10 | approved_claude_20261110 |
| `cr-moc-nhi` | 8359 | 3912 | 10/10 | approved_claude_20261110 |
| `cr-nam-rom` | 5505 | 0 | 10/10 | approved_claude_20261110 |
| `cr-ot` | 6171 | 0 | 10/10 | approved_claude_20261110 |
| `cr-rau-ma` | 8074 | 4481 | 10/10 | approved_claude_20261110 |
| `cr-sa` | 6229 | 22 | 9/10 | approved_claude_20261110 |
| `cr-son-duoc` | 6220 | 2803 | 10/10 | approved_claude_20261110 |
| `cr-tia-to` | 25578 | 25600 | 9/10 | approved_claude_20261110 |
| `pot-g1-tho-dao` | 7358 | 3643 | 10/10 | approved_claude_20261110 |
| `pot-g1b-thung-tre` | 6466 | 1785 | 10/10 | approved_claude_20261110 |
| `pot-g2a-gao-dua` | 8003 | 2211 | 10/10 | approved_claude_20261110 |
| `pot-g2b-truc-dong` | 7752 | 2866 | 9/10 | blocked_imagegen_limit |
| `pot-g3a-can-moc` | 6576 | 1413 | 10/10 | approved_claude_20261110 |
| `pot-g3b-sanh-nau` | 5362 | 0 | 10/10 | approved_claude_20261110 |
| `cr-bi-do` | 7023 | 1630 | 10/10 | approved_claude_20261110 |
| `cr-la-lot` | 6042 | 0 | 10/10 | approved_claude_20261110 |
| `cr-khoai-mon` | 11340 | 9433 | 10/10 | approved_claude_20261110 |
| `cr-hoa-hong` | 5778 | 3184 | 10/10 | approved_claude_20261110 |
| `cr-dua-hau` | 8020 | 4642 | 8/10 | blocked |
| `pot-g4a-lam-su` | 6327 | 0 | 10/10 | approved_claude_20261110 |
| `pot-g4b-linh-thach` | 7343 | 1362 | 10/10 | approved_claude_20261110 |
| `pot-g5a-dong-co` | 7131 | 730 | 9/10 | approved_claude_20261110 |
| `pot-g5b-tinh-mach` | 20237 | 16475 | 10/10 | blocked |
| `cr-ngai-cuu` | 5734 | 0 | 10/10 | ready_for_claude_review |
| `cr-nghe` | 6681 | 0 | 9/10 | blocked |
| `cr-du-du` | 5835 | 1201 | 10/10 | blocked_imagegen_limit |
| `cr-hoa-sung` | 7342 | 2256 | 10/10 | blocked_imagegen_limit |
| `cr-oi` | 5131 | 0 | 10/10 | ready_for_claude_review |
| `cr-rieng` | 6356 | 1446 | 9/10 | blocked_imagegen_limit |
| `cr-muop-dang` | 4997 | 0 | 10/10 | ready_for_claude_review |
| `cr-ky-tu` | 7441 | 1853 | 9/10 | blocked |
| `cr-hoa-mai` | 7471 | 0 | 10/10 | ready_for_claude_review |
| `cr-xoai` | 6054 | 2596 | 10/10 | blocked_imagegen_limit |
| `cr-san` | 5976 | 0 | 10/10 | ready_for_claude_review |
| `cr-hau-dau-co` | 5053 | 0 | 10/10 | ready_for_claude_review |
| `cr-hoa-sen` | 4542 | 1 | 10/10 | blocked_imagegen_limit |
| `cr-buoi` | 3757 | 0 | 10/10 | ready_for_claude_review |
| `cr-tam-that` | 5369 | 389 | 9/10 | blocked |
| `cr-dua` | 7449 | 0 | 10/10 | ready_for_claude_review |
| `cr-hoa-dao` | 8464 | 3747 | 9/10 | blocked |
| `cr-mit` | 7108 | 2711 | 9/10 | blocked |
| `cr-chom-chom` | 8108 | 3717 | 9/10 | blocked |
| `cr-linh-chi` | 6576 | 4545 | 10/10 | blocked |
| `cr-hoa-lan` | 10362 | 7631 | 10/10 | blocked |
| `cr-nhan-sam` | 5423 | 0 | 10/10 | ready_for_claude_review |
| `cr-thanh-long` | 6809 | 612 | 10/10 | blocked |
| `cr-ngan-nhi` | 3555 | 630 | 10/10 | blocked_imagegen_limit |
| `cr-mang-cut` | 6784 | 5200 | 10/10 | blocked_imagegen_limit |
| `cr-dong-trung-ha-thao` | 3727 | 0 | 10/10 | ready_for_claude_review |
| `cr-vai` | 5558 | 0 | 10/10 | ready_for_claude_review |
| `cr-ho-phach-mam` | 6533 | 0 | 9/10 | blocked |
| `cr-hoa-quynh` | 6392 | 3394 | 10/10 | blocked_imagegen_limit |
| `cr-nguyet-huynh-tinh` | 5660 | 2403 | 10/10 | blocked_imagegen_limit |
| `cr-tuyet-lien` | 7149 | 2189 | 10/10 | blocked_imagegen_limit |
| `cr-tinh-hoa-lien` | 6814 | 2086 | 10/10 | blocked_imagegen_limit |
| `cr-sau-rieng` | 4823 | 0 | 9/10 | blocked_imagegen_limit |
| `cr-thach-anh-qua` | 6005 | 3805 | 10/10 | blocked_imagegen_limit |
| `cr-ca-phe` | 7289 | 3446 | 10/10 | blocked_imagegen_limit |
| `cr-ho-tieu` | 7786 | 1356 | 10/10 | blocked_imagegen_limit |
| `cr-dia-mach-ket-tinh` | 6244 | 4753 | 10/10 | blocked_imagegen_limit |
| `cr-linh-mach-mam` | 8169 | 1343 | 10/10 | blocked_imagegen_limit |

## Continuation — targeted crop/pot repairs (2026-11-13; paused on ImageGen 429)

- Re-read the current manifest before edits: exactly 59 assets have Claude-approved statuses. None of their art files were edited. `cr-nghe` is among the newly approved 59, so its requested h repair was skipped and its existing final/QA/review were left untouched.
- Started `cr-dua-hau` with three new built-in ImageGen outputs saved as `raw-11.png`–`raw-13.png`; no other requested asset has been started. The latest candidate `raw-13.png` is packed and measured: 9/10 gates; a–g and i pass; h IoU=.7891 fails .80; j min loop IoU=.8524 passes. Refreshed its atlas previews and contact sheet. Attempts used for this task: 3/6.
- On the fourth ImageGen call the service returned HTTP 429 `usage_limit_reached` with `resets_in_seconds=7411`, `resets_at=1794545438`. Reset time: **2026-11-13 04:50:38 UTC / 11:50:38 Asia/Saigon**. Stop here as requested. Resume from Dưa Hấu `raw-13.png`, attempt 4/6, then pack → defringe → measure. Do not rerun or replace the first three raws.
- Remaining unstarted, non-approved repair items: `cr-tam-that`, `cr-mit`, `cr-chom-chom`, `cr-ho-phach-mam`, `cr-rieng`, `cr-hoa-dao`, `cr-ky-tu`, `cr-sau-rieng`, `pot-g2b-truc-dong`. Do not touch `cr-nghe`.
- Current manifest records Dưa Hấu as `blocked_usage_limit`, `approved:false`, with the exact h/j measurements and reset time. No approved flag was added or changed. `contact-sheet.png` was rebuilt with all 70 assets.
- Current Dưa Hấu files include retained `raw-11..13.png`, `final-before-repair-20261113.png`, current `final.png`, QA, previews, and retry details in `prompt.md`/`review.md`.

## Targeted repairs — resumed 2026-11-16

- 59 Claude-approved records remain protected; no approved art was edited. `cr-nghe` is unapproved and is being repaired (the earlier progress note incorrectly listed it as approved; manifest showed it blocked).
- `cr-dua-hau`: exhausted its six new outputs; latest raw-16 measured h=.5822 (<.80), j=.8690 (pass), other crop gates pass. Status blocked.
- `cr-nghe`: exhausted its six new outputs raw-13..18; latest raw-18 measured h=.5673 (<.80), j=.9192 (pass), other crop gates pass. Status blocked.
- Current task order resumes next at `cr-tam-that`, then `cr-mit`, `cr-chom-chom`, `cr-ho-phach-mam`, `cr-rieng`, `cr-hoa-dao`, `cr-ky-tu`, `cr-sau-rieng`, `pot-g2b-truc-dong`. Each gets up to six new ImageGen outputs. If a 429 occurs, record reset and stop.

## Continuation 2026-11-16: Tam Thất
- cr-tam-that: 6/6 attempts raw-13–18. Selected raw-17, a–j 10/10, h=.9024, j=.8525; dark preview has visible isolated magenta edge pixels; blocked. raw-18 j=.8431 fails. Next: cr-mit attempt 1/6.

- cr-mit: raw-13–16, 4/6 attempts; selected raw-16 script 10/10 h=.9260 j=.9646, visual blocker: row 1 has no blink and row 5 starts with mature plant. Scope of this request only permits editing plant f4. Next cr-chom-chom attempt 1/6.

- cr-chom-chom: raw-13, attempt 1/6; script 10/10 h=.8811 j=.9577, 60 colors, ripe 150; dark preview inspected, ready for Claude with harvest f4 observation. Next cr-ho-phach-mam attempt 1/6.
- Correction: cr-chom-chom blocked: harvest f4 still full character, contrary to harvest contract; existing measure does not check this. User limited repair to plant f4.

- cr-ho-phach-mam: raw-13–16, 4/6 attempts; selected raw-16 a–j 10/10, h=.9231 j=.9165, dark preview inspected, ready for Claude. Next cr-rieng attempt 1/6.

- cr-rieng: raw-09–13, 5/6 attempts. raw-13 a–j 10/10 (h=.8057, j=.9399), but dark 4x visibly shows hot-pink fringe around many outlines; blocked visual. Next cr-hoa-dao.

- cr-hoa-dao: targeted sprout redraw raw-13..16 (4 attempts); selected raw-16. a–j pass 10/10; heights sprout 69–70, grow 96–97, ripe 122–125; width 117; colors 59; h=.8361; j=.8707. Dark 4x opened; no detached magenta fringe noticed. Status ready_for_claude_review, approved:false. Next: cr-ky-tu.

- cr-ky-tu: targeted width redraw raw-13..14 (2 attempts); selected raw-14. a–j pass 10/10; width 128; ripe 120–121; colors 60; h=.8336; j=.8614. Dark 4x opened, no distinct detached magenta fringe. Status ready_for_claude_review, approved:false. Next: cr-sau-rieng.

- cr-sau-rieng: redesigned in raw-09..10 (2 attempts); selected raw-10. a–j pass 10/10; colors 60; heights 66 / 95–96 / 125–126; width 129; h=.9574; j=.9208. Face and blink notes added for all five rows; dark 4x confirms durian fruit silhouette, no flower mane/sword/shield, no distinct magenta fringe. Status ready_for_claude_review, approved:false. Next: pot-g2b-truc-dong.

- pot-g2b-truc-dong: six new ImageGen attempts raw-34..39 exhausted. Best raw-35 repacked. a–f,h–j pass; g fails only min adjacent body IoU=.9465 (<.95), at water row 3 frame1→2; wet soil darkening=16.15% PASS; transition min=.9814 PASS; colors=57; joins pass. raw-37 could not pack at s≥.6. Final remains blocked_imagegen_limit, approved:false. No further ImageGen attempts under current six-output allowance.


## Metadata reconciliation — 2026-11-16

- Reconciled `cr-hoa-dao`, `cr-ky-tu`, and `cr-sau-rieng` manifest fields from their current QA and final files: each is 10/10, `all_checks_pass:true`, selected sources raw-16/raw-14/raw-10, SHA-256 updated, `approved:false`.
- Corrected the Trúc Đồng review: selected raw-35 has minimum adjacent body IoU .9465099965 at water row 3 frame 1→2; .9458 belongs to another candidate. Wet darkening 16.1459%; minimum transition IoU .981353. Gate g remains blocked solely by body IoU (<.95); six new ImageGen outputs exhausted.

## Continuation — focused repair request (2026-11-16)

- Updated `tools/measure_atlas.py` per Claude’s written thresholds: crop gate h ≥0.75; pot adjacent-body IoU ≥0.94, joins ≥0.93, wet-soil darkening ≥15%. Decision is recorded in `REVIEW-CLAUDE-20261109.md` (existing dated review log).
- `cr-nghe`: selected raw-29 after 6/6 new outputs; measured 9/10, h=.6717 fails; all other gates pass. Blocked.
- `cr-mit`: selected raw-22 after 6/6 new plant-row outputs; measured 9/10, f fails (sprout 76 px; max width 151 px); all other gates pass. Blocked.
- `cr-ho-phach-mam`: selected raw-21; measured 10/10 (58 colors; heights 75/106/150; width 130; h=.8953; j=.9547). 4× dark preview inspected; finer grow/ripe pixel density is evident. Ready for Claude review, approved:false.
- `pot-g2b-truc-dong`: selected raw-44 after 6/6 new outputs; measured 9/10, g fails (min adjacent body IoU=.9371 <.94; wet darkening=3.95% <15%). Joins pass (min .9529). Blocked.
- Rebuilt contact sheet after manifest reconciliation; did not change any of the 66 Claude-approved assets. No 429 occurred.
