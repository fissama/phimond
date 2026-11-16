# Batch 9 — Octopath-directed icon draft

122 individual RGBA finals; all `approved:false`. Built-in image_gen only. No runtime/public edits, activation, commits, or pet-atlas redraws.

Coverage: 5 runtime items; 29 runtime skills; 8 races; 7 elements; 7 statuses; 31 original rank IDs; 9 stats; 2 currencies; 3 quest types; 8 NPC roles; 10 normal/dim star groups; rarity mark, rarity outline and star outline. Exact IDs are in `manifest.json`. Every icon master is 256×256, alpha margin at least 8px. Readability previews at 32px and 64px are in `game-size-light-dark.png`.

Content IDs come from `data/items/items.json`, `data/skills/skills.json`, `data/pets/races.json`, and `data/skills/statuses.json`. Race dragon has no configured element: no eighth element invented. Authoring/P13 skills are excluded until promotion is established by the owner. Pet portraits are excluded: Claude can crop approved P10 atlases.

Rank discrepancy: master plan says 26, but original Sprite files actually contain 31 IDs: rank01–05, rank11–15, rank21–25, rank31–35, rank41–45, rank51–55, rank6. All31 retained. First rank32–55 attempt drifted to heraldic leaf centers; targeted image edit restores faceted violet/red gems while retaining pip counts. Both raw attempts remain byte-identical.

Original source contacts and their JSON source-file inventories are retained at this directory root. Original identity motifs: flask/talisman/gem items, egg-shaped race symbols, original shield/wing rank tiers. Runtime item/skill IDs lack proven exact historical image mappings; those designs are explicitly semantic drafts, not claims of exact original identification. Rank ornament and pixel density still need owner style review; some generated rank edges are smoother than pet anchors.

Each asset directory contains final.png, original raw PNG attempt(s), exact selected prompt with ordered reference SHA256 hashes, provenance.json with per-attempt prompts/hashes, review.md, and qa.json. `qa-summary.json` verifies raw-byte preservation and mechanical results. Model/cost are not exposed by the host tool. Forge doctor warnings/missing optional dependencies are retained in doctor.json; no API or code-art fallback was used.

Review order: contact-sheet.png, game-size-light-dark.png, then individual final.png at full scale. Mechanical checks passed for dimensions, margins, nonempty art and raw preservation; visual approval and in-engine validation remain pending. Superseded raw attempts are evidence, not activation candidates.
