# Batch 05 — Octopath Human & NPC Art Suite (Complete Roster & Animations)

**130 finalized HD-2D deliverables: 2 Players, 107 NPCs (Complete Roster), 21 Main Dialogue Portraits.**

## Coverage & Deliverables

1. **Player Characters (2/2)**:
   - `player-male` & `player-female`: 192×192 master still (168px occupied height, pivot [96, 184], margins ≥ 8px).
   - **Idle animation**: 4-frame breathing cycle strip (`idle.png`, 768×192).
   - **Run animation**: 8-frame grounded stride strip (`run.png`, 1536×192).
   - Individual animation frames in `anim/`.

2. **Full 107 NPC Roster (107/107)**:
   - **49 Stage 4 Primary NPCs**: all master stills (192×192, 168px height) + 4-frame breathing idle loop strips (`idle.png`).
   - **58 Expansion NPCs**: covering all expansion biomes (Desert 01–06, Mountain 01–06, Nightmare 01–06, Tomb 01–06, Crossroads 01–06, Astral 01–06, Ancient 01–06, Ghost Castle 01–06, World Tree 01–06, Spire Tower 01–04) with master stills + 4-frame idle strips (`idle.png`).

3. **21 Dialogue Portraits (21/21 Main NPCs Complete)**:
   - All 21 main game characters have dedicated half-body dialogue bust portraits (256×256, transparent background, margins ≥ 8px, ≤ 48 colors).
   - Includes original 11 plus 10 newly finalized portraits (`gate_guild`, `pet_shop`, `pet_bless`, `pet_enhance`, `pet_hatch`, `ranch_keeper`, `deep_diver`, `isl_captain`, `sq_arena`, `act_reward`).

## Technical Specification

- **Art Style**: Octopath Traveler HD-2D (grounded pixel anatomy, hue-tinted outlines, restrained palette ≤ 48 colors, NearestFilter ready).
- **Dimensions**: Characters 192×192 px; Portraits 256×256 px; Idle strips 768×192 px; Run strips 1536×192 px.
- **QA Status**: 130/130 assets pass 100% mechanical QA checks (0 stray noise, 0 partial alpha, margins ≥ 8px).
