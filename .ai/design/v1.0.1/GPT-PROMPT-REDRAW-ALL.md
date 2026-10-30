# Prompt gộp vẽ lại (R1 + R2 + cột) — copy nguyên khối bên dưới vào ChatGPT

Đính kèm trước khi gửi (đúng tên file):
- Nhóm A (mái nhà, R1): `city-backdrop-wide.png`, `hall-city-roofs.png`, `hall-roofs-attempt-02.png`
- Nhóm B (chạy, R2): `walker-elder.png`, `walker-traveller.png`, `player-male-contact-frame-1.png`, `player-male-contact-frame-5.png`, `player-male-contact-frame-5-legs-4x.png`, `elder-frame-1-attempt-02.png`
- Nhóm C (cột): `hall-column.png`, `palace-column.png`, `palace-marble-pillar.png`, `arena-column.png`, `city-carved-pillar.png`

```
You are producing game art assets for an HD-2D game in the style of Octopath Traveler. Work through the jobs below IN ORDER. Deliver ONE PNG per job, one job per reply, and wait for me to say "next" before starting the following job. Every PNG must be exactly the size stated.

GLOBAL RULES (apply to every job):
- Crisp pixel art with painterly shading, no anti-aliasing, no blur, no film grain, no dither noise, no watermark, no text.
- Light comes from the TOP-LEFT. Maximum 48 colours in total. Binary alpha only.
- Background is one flat magenta #FF00FF with a hard edge: no pink or lilac fringe pixels, none inside the artwork, no painted checkerboard, no ground shadow, no floor.
- Everything must be fully inside the canvas with at least 4 px of magenta margin; nothing cropped.
- Use large flat colour bands with sharp edges for surfaces. Use at most 6 tones per material.

JOB 1 - hall-column.png, 224x560. References: hall-column.png (keep only its proportions and position, do NOT copy its flaws: it is cropped on the left, has a stray line at the top-left and speckled noise), palace-column.png and palace-marble-pillar.png (match their cream-ivory stone and warm gold trim).
Tall fluted marble column for a summoning palace hall. From top to bottom: square abacus slab; gold-banded echinus with a row of rounded gold beads; straight shaft with 7 clearly visible vertical flutes (light on the left flutes, shadow on the right); thick gold ring near the base; round torus; octagonal plinth. Perfectly symmetric left-to-right, base centred, 8 px of magenta under the plinth.

JOB 2 - palace-column.png, 178x416. References: palace-column.png, palace-marble-pillar.png.
Same column as the first reference (Corinthian-style capital with gold leaf ornament, cream shaft with a gold scroll motif, grey-green stone base), redrawn cleaner with crisp outlines and no speckle. Identical composition and proportions, symmetric.

JOB 3 - arena-column.png, 148x366. References: arena-column.png, palace-column.png.
Same gold spiral-ribbon column (gold capital with leaf pattern, red trim only on the base and capital rim, ribbon winding around a gold shaft). The ribbon must wind in ONE direction with even spacing, edges crisp, symmetric silhouette.

JOB 4 - city-carved-pillar.png, 110x266. References: city-carved-pillar.png, palace-marble-pillar.png.
Same short carved stone pillar (ball finial, stepped cap, carved leaf panel, stepped base) in the cream-gold palette of palace-marble-pillar.png, crisp panel carving, symmetric.

JOB 5 - hall-outside-roofs-side.png, 512x384, OPAQUE (no magenta here). References: city-backdrop-wide.png, hall-city-roofs.png, hall-roofs-attempt-02.png (a previous try: good 4:3 framing and roof-tone strip, but its edges do not tile and it uses too many colours).
Distant city rooftops seen through the side window of a palace hall at dusk. Same muted palette and soft aerial perspective as city-backdrop-wide.png: desaturated warm-grey sky fading to pale amber at the horizon, terracotta roofs and sandstone towers in light haze, faint mountains. No foreground wall, nothing sharper or more saturated than the reference. HARD REQUIREMENT: the leftmost 32 px columns and the rightmost 32 px columns must be pixel-identical in content (same rooftops, same sky) so the image tiles horizontally with no visible seam; build the picture as a repeating band and check it. The bottom 48 px fade into a flat roof-tone strip. Maximum 48 colours.

JOB 6 - elder walk, TWO images first: walker-elder.frame1.png and walker-elder.frame5.png, each 192x192 on magenta. References: walker-elder.png (the character), elder-frame-1-attempt-02.png (a good frame 1), player-male-contact-frame-1.png and player-male-contact-frame-5.png (the leg timing to copy), player-male-contact-frame-5-legs-4x.png.
The elder walks to the RIGHT, feet at (96,184), body about 168 px tall, wooden staff in the hand.
Previous attempts failed because frame 5 had the SAME leg forward as frame 1. To make the legs unambiguous: paint the NEAR leg (the one on the viewer's side) in the normal trouser colour and the FAR leg 15% darker.
- Frame 1: the NEAR leg is forward (foot ahead of the body), the FAR leg trails behind.
- Frame 5: the FAR (darker) leg is forward, the NEAR (normal colour) leg trails behind. The two frames must be visibly different in the legs: the foot that was in front in frame 1 is behind the body in frame 5. The arm swing is opposite to the legs.
Show frame 1 and frame 5 side by side in one 384x192 image and self-check the legs before delivering.

JOB 7 - same as Job 6 for the traveller (walker-traveller.png; travel staff and pack), images walker-traveller.frame1.png and walker-traveller.frame5.png.

JOB 8 (only after I approve Jobs 6 and 7) - the six remaining frames of each walk cycle, one 1536x192 strip per character (eight 192x192 cells), frames 1 and 5 exactly as approved, frames 3 and 7 passing poses, same head height and foot line in every cell.

Start with JOB 1.
```

Ghi chú cho mình (không dán):
- R1 hai lần đều lỗi lặp mép: nếu lần 3 vẫn hỏng thì mình ghép lặp bằng code (lật gương nửa phải) thay vì chờ GPT.
- R2: nếu Job 6/7 vẫn trùng chân, phương án dự phòng là mình tự dựng khung 5–8 bằng code từ khung 1–4 (hoán đổi vùng chân) hoặc tạm dùng strip `player-male.run` đã duyệt cho hai NPC walker.
