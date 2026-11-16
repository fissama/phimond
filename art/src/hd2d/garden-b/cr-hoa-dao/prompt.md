# cr-hoa-dao — ImageGen prompts and provenance

C08 Hoa Đào: graceful cream-and-tan fawn with twig antlers, peach blossoms and green buds. Eight outputs retained raw-01…raw-08. Selected raw-07 SHA-256 `78459573cb257434f7bcb28feb6b96279258c4c4f964863f88ada1226c825d03`; packed final SHA-256 `b797ac6fa01debbdde5ea2c0be7fa5f9f7fcd725defadd62831b3a20d3272529`. Style reference hashes: Bạc Hà `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`, Mộc Nhĩ `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`. Plant-row iteration referenced raw-03/raw-04/raw-05/raw-07. No pixel edits.

## Selected repair source — 2026-11-13

Repacked from `raw-12.png` (SHA-256 `7a675abd8684b863f6af279f7fdb3868a849425923a8fcca5c2060668e7c805f`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 8464→3747. loop min .8707 passes; sprout 76 px fails f; edge 8464→3747.


## Targeted sprout-height repair — 2026-11-16

Used built-in ImageGen, surgical edit of row 1 only, retaining each generated sheet as raw-13.png through raw-16.png. Selected raw-16.png, SHA-256 `fb513c463ecfd550baa0a310d2f70cb81e021dac6137cb452114aa1cb4675ddf`. ImageGen prompt: "Shorten only the four row-1 fawn sprites about 8–10%, preserve feet baseline and keep rows 2–5 unchanged; crisp pixel art, flat #FF00FF."
