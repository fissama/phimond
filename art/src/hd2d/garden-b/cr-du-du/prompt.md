# Prompt & provenance — cr-du-du

- Art source: built-in ImageGen; raw-01 is the first atlas sheet (attempt 1 of 8; one standalone reference call also used).
- Character: curious baby giraffe spirit with papaya fruit mane, palm-frond canopy, narrow cream neck and small green leaf feet.
- Reference sprout source: `reference-sprout-f1.png`, SHA-256 `2cb253781bc51a24f421da12f9f86a0714a64d7b86de868558c704902f87f3ef`.
- Style references: `garden-b/cr-bac-ha/final.png` SHA-256 `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`; `garden-b/cr-moc-nhi/final.png` (approved pixel-art finish references).
- Atlas request: 4×5 cells on flat #FF00FF; rows sprout, grow, ripe, harvest, plant; crisp pixel clusters; no baked shadow, glow, scenery, text or purple/magenta in the sprite. Ripe giraffe reaches toward a star; harvest waves then fades to sparse motes; plant frame 4 repeats sprout frame 1 silhouette.
- First raw sheet SHA-256: `04dd50225969f1a9fb2b8d878699cdb6c6602ed010e915179a30903f08f40742`.

## Attempts and provenance

Standalone sprout reference ImageGen call: 1; atlas ImageGen outputs: 7 (`raw-01.png`–`raw-07.png`); total calls: 8/8. Source hashes:

| Raw | SHA-256 | Measurement outcome |
|---|---|---|
| raw-01 | `04dd50225969f1a9fb2b8d878699cdb6c6602ed010e915179a30903f08f40742` | 8/10; j 0.7895; i annotations absent |
| raw-02 | `0bf3aad9eb2e8a93be4906bb83bf0478c361c2eece3928ed380da601f605df1a` | 9/10; j 0.8065 |
| raw-03 | `60b2c76cf727858142de63e045b0c7526410a0e6e1597d67eff9494ed4a46e7a` | 8/10; grow 113 px; j 0.8080 |
| raw-04 | `42f49ec7535815ad5769b91f258ce6bdf2aac00f04512a8ac33b236a927f06e9` | 9/10; grow 120 px |
| raw-05 | `92c8fe3f8ce3db13f699fec8f507349bfb74f17748bfb97aac9f8a96598c4edf` | 9/10; grow 118 px |
| raw-06 | `d5486f038c58753265a2c1a7c5ea062a12368b272c77607497e1f917a48636a2` | 10/10 mechanical; selected measurement candidate |
| raw-07 | `b64d56c8527fe6c84a71224ba44e155a0c36d10eaac917bfeed5485ab824da1c` | 9/10; grow 84 px (<85) |

Selected packed final from raw-06 SHA-256: `6d9e44560efa1c1c25ca5b706f0b66f30374236fea7516a8ca385156d2508485`.

The first packed result measured 8/10: a–h passed; i lacked face annotations; j was 0.7895 (<0.85). The next generation is targeted at keeping silhouettes stable across each looping row.
