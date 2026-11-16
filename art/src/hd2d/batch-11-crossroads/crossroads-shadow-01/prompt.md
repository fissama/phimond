# crossroads-shadow-01

Route: built-in image_gen. Model not exposed.

Built-in image_gen produced four soft cool navy-blue ground contact shadows on actual transparency in a 2x2 sheet. Source cells are 768x512. Each asset is isolated by per-cell alpha-cleanup stencil; alpha at or below 8/255 is cleared to remove negligible haze only. Original art pixels and remaining soft alpha preserved; no content was drawn or painted by code. Sizes are source footprints plus 8px transparent margin on each side, with no geometric resampling. Route: built-in image_gen; model not exposed. Alpha-preserving extraction repair: package the four shadows from isolated crops of the original generated sheet, removing only source alpha <=8/255; preserve the remaining original alpha values. Prior package attempt binarized soft alpha and was rejected; those exports are archived in each asset folder. No repaint or geometric resampling. The edit-generated alternatives did not reduce the shadows reliably and one rendered a fake checkerboard; both are retained and rejected. Selected output uses four transparent crops from initial raw-01, with only standard premultiplied Lanczos resizing of the soft shadow masks to category-appropriate native bounds (112x32, 176x48, 256x64, 384x96). No drawing or repainting.

Actual attachments (ordered):
1. .ai/design/map-checklists/refs/crossroads_unnamed_area_01.jpg — SHA256 7f6522193f17a5514164c1975e2073275cf9bc0471d2b5bf03fe50778369187a
2. apps/game-web/art-src/hd2d/batch-11-crossroads/crossroads-floor-01/final.png — SHA256 0f206a3711b3a681a4cfc374d694ea4300a77ae04c6fbc1d56b4e2ddfe83f7cf

Raw: raw-04-shadow-01.png; SHA256 a91c833bb6b1ea4f79bef7586188a989c030720ee15412c928450704f858e333; source box [0, 0, 112, 32]; sheet extraction polygon None; translation-only source registration None. Final [128, 48]. Non-dithered 48color finish, nearest scaling. No content drawn with code.

Finish details: {"visible_colors": 48, "palette_source": null, "palette_include": null, "palette_exclude": null, "palette_remap": null, "base_palette_filter": null, "native_alpha": true, "key_threshold": 100, "key_edge_threshold": 150, "despill_radius": 2, "documented_exception": null, "job_palette_note": null}
