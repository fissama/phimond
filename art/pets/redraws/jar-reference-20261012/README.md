# JAR reference redraw — 2026-10-12

Owner request: redraw Đại Vương Bọ Cạp (`species_0151`) and Thần Đèn
(`species_0143`) using the newly decoded Java sprites as clearer identity
references. This is a revision of those two species only.

## Identity

- Scorpion: handsome mature masculine daddy face with groomed swept-back
  indigo/purple hair and clear broad muscular purple torso; original Java
  supplies only the large red/orange crescent
  pincers with ivory edges, purple walking legs and purple segmented tail with
  orange/gold stinger. Keep the original hybrid silhouette.
- Genie: adult muscular blue torso, readable stern eyes and moustache,
  gold earrings/cuffs/belt, flowing blue/cyan ponytail, red/orange smoke tail
  connected to one gold oil lamp; no legs. Movement shows only the hopping
  lamp, with the genie completely hidden. Final owner override: all djinn
  poses face left; ALL lamps have spout LEFT and handle RIGHT. Java's
  pre-mirrored variants do not define this project's base atlas direction.

## Output contract

Transparent RGBA 1124 × 1405, 4 columns × 5 rows, 281 × 281 cells.
Rows: idle, move, physical attack, signature skill, hurt/down. Only idle
and move loop. Complete bodies and effects must remain within each cell's
22-pixel transparent margin. Preserve the generated raw output and record
any nearest-neighbor packing using the existing project packer.

`attempt-01` preserves the first generation. It was rejected for crowded
spacing / edge contact. The revised generation must be checked separately.

This folder does not change the previous owner-selected atlas manifest,
APK source assets, runtime routing, timings or gameplay. New owner acceptance
and integration are separate from creating these review artifacts.

Tool: built-in `image_gen`; full prompts and input hashes accompany each
attempt. Original Java reference contact sheets are copied into the attempts
for review without relying on Downloads remaining available.

Latest Scorpion pincer design review: `species_0151/attempt-09/`.
Overlapping sharp armor and taller pointed elbows replace the old rounded
crab-like design. `preview/preview.html` shows all five rows; mechanical
validation passes, but size and faint alpha speckling remain visual limitations
recorded in `self-review.md`. No new owner acceptance or runtime activation.
Scorpion attempts 07/08 are retained rejected layout experiments. Genie
attempt 11 remains rejected for an incorrect tail-to-nozzle connection.
