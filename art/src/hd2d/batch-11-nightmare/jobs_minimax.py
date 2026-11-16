#!/usr/bin/env python3
"""Job definitions for the MiniMax pass over the nightmare kit (41 remaining rows).

Every job is one MiniMax image-01 call. The provider takes one subject reference and a
prompt under 1500 characters, so each sheet is small and every prompt is checked
before the call is made.

Prompts ask for a plain white studio backdrop: the provider cannot hold a magenta
chroma key, and white is the one backdrop it renders flat and clean. The finisher
keys white out and rebuilds the pixel grid.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPT_LIMIT = 1500
OVERLONG = []


def check(prompt):
    if len(prompt) >= PROMPT_LIMIT:
        OVERLONG.append((len(prompt), prompt[:90]))
    return prompt


PIX = ("DRAW AS REAL PIXEL ART: chunky pixel clusters of 3-6 px, 40-48 flat colors, 2-4 tones "
       "per material, thin 1px same-hue dark outline, warm top-left key, cool violet recesses. "
       "No anti-aliasing, no gradients, no dither, no photoreal texture, no painterly shading, "
       "no bloom, no text, no characters.")

PAL = ("Palette: plum #3A2B52, shadow #241B36, dust #5B3F7A, moss #4E7A4A, bone #C9C0A8, "
       "glow violet #B26BFF only as tiny crack accents.")

DECAL_PRE = ("GAME ASSET SPRITE SHEET, 1024x1024, 2x2 grid of 4 pixel-art GROUND DECALS, one "
             "per quadrant, each alone on a plain pure white #FFFFFF background (uniform, no "
             "shadow, no texture, no ground plane). Each decal is a flat ground detail seen from "
             "directly above: no standing props, no cast shadow. It is an irregular organic mark "
             "with a pixel-feathered outline, never a square, rectangle, ellipse or clean "
             "polygon, and NOT a slab of painted ground; gaps inside it are transparent white, not "
             "painted soil. " + PIX + " " + PAL)


def sheet(preamble, items):
    return check(preamble + " " + " ".join(f"{pos} {text}" for pos, text in items))


JOBS = [
    {
        "name": "decals-a",
        "grid": "2x2",
        "size": "1024x1024",
        "montage": "decals",
        "prompt": sheet(DECAL_PRE, [
            ("TOP LEFT", "glowing crack patch: 6-9 branching luminous fissures, #B26BFF core, "
                         "dark rim, plum soil between."),
            ("TOP RIGHT", "bone fragments: 7-10 broken bones, ribs, a cracked vertebra, 2 jaw "
                          "shards, flat, ivory, wide gaps."),
            ("BOTTOM LEFT", "poison moss patch: lumpy #4E7A4A clumps, darker core, dead tips, "
                            "4 grit chips, bitten outline."),
            ("BOTTOM RIGHT", "shattered crystal shards: 6-9 flat violet-grey chips, 2-3 facets, "
                             "#8E7BC4 highlight, #2A2135 shadow."),
        ]),
        "assets": [
            {"id": "nightmare-decal-01", "name": "Glowing crack patch", "category": "decal",
             "size": [448, 288], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-02", "name": "Bone fragments scatter", "category": "decal",
             "size": [384, 256], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-03", "name": "Poison moss patch", "category": "decal",
             "size": [384, 256], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-04", "name": "Shattered crystal shards", "category": "decal",
             "size": [320, 192], "pixel_grid": 4, "colors": 48},
        ],
    },
    {
        "name": "decals-b",
        "grid": "2x2",
        "size": "1024x1024",
        "montage": "decals",
        "prompt": sheet(DECAL_PRE, [
            ("TOP LEFT", "cracked rune stone: broken plum-grey slab, one fracture with #B26BFF "
                         "glow, 3 angular grooves, not letters."),
            ("TOP RIGHT", "ash and ember scar: flat soot smear, 8-12 dull orange ember specks, "
                          "3 charred twigs, never a flame."),
            ("BOTTOM LEFT", "grave dirt and rubble: dark soil clods, broken grey stones, 5 pale "
                            "grit chips, white gaps, no mound."),
            ("BOTTOM RIGHT", "half-buried ribcage: 4 curved ribs, 2 vertebrae half sunk in soil, "
                             "ivory tops, no skull."),
        ]),
        "assets": [
            {"id": "nightmare-decal-05", "name": "Cracked rune stone slab", "category": "decal",
             "size": [448, 288], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-06", "name": "Ash and ember scar", "category": "decal",
             "size": [448, 288], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-07", "name": "Grave dirt and rubble", "category": "decal",
             "size": [384, 256], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-08", "name": "Half-buried ribcage", "category": "decal",
             "size": [448, 288], "pixel_grid": 4, "colors": 48},
        ],
    },
    {
        "name": "decals-c",
        "grid": "2x2",
        "size": "1024x1024",
        "montage": "decals",
        "prompt": sheet(DECAL_PRE, [
            ("TOP LEFT", "fallen violet petals: 9-12 muted violet petals on plum soil, 2 curled, "
                         "3 crumpled, thin veins."),
            ("TOP RIGHT", "dark creeper trail: thin strand of dead dark ivy leaves over soil, 7-9 "
                          "pointed leaves, ragged ends."),
            ("BOTTOM LEFT", "broken urn shards: 5 cracked clay-brown pottery fragments, faded "
                            "violet glaze inside, sharp edges."),
            ("BOTTOM RIGHT", "tar puddle: flat irregular black tar pool, dull violet sheen on one "
                             "edge, 3 tiny bubbles, not a circle."),
        ]),
        "assets": [
            {"id": "nightmare-decal-09", "name": "Fallen violet petals", "category": "decal",
             "size": [320, 192], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-10", "name": "Dark creeper trail", "category": "decal",
             "size": [448, 288], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-11", "name": "Broken urn shards", "category": "decal",
             "size": [384, 256], "pixel_grid": 4, "colors": 48},
            {"id": "nightmare-decal-12", "name": "Tar puddle", "category": "decal",
             "size": [448, 288], "pixel_grid": 4, "colors": 48},
        ],
    },
    {
        "name": "edges",
        "grid": "1x3",
        "size": "1024x768",
        "montage": "decals",
        "prompt": check(
            "GAME ASSET TEXTURE SHEET, 1024x768. Three long horizontal GROUND TRANSITION STRIPS "
            "stacked vertically, one per band: the top band 1024x256, the middle band 1024x256, "
            "the bottom band 1024x256, each band separated by plain pure white #FFFFFF. "
            "Each strip is a flat ground texture seen from directly above that fades from one "
            "material into the next along its length, with an irregular torn boundary of the "
            "change, never a straight line and never a hard band. "
            "TOP STRIP fades from cracked violet plum soil into flat black stone. "
            "MIDDLE STRIP fades from black stone into broken ruin floor with pale grit chips and "
            "olive moss. "
            "BOTTOM STRIP fades from ruin floor back into cracked violet plum soil with sparse "
            "olive moss flecks. "
            + PIX +
            " No vertical side walls, no objects standing up, no cast shadow, no text. The "
            "background around every strip is uniform pure white with no shadow or gradient."
        ),
        "assets": [
            {"id": "nightmare-edge-01", "name": "Violet clay to black stone edge", "category": "edge",
             "size": [512, 128], "pixel_grid": 4, "colors": 48, "mode": "band",
             "tileable": "x", "flat_border": False},
            {"id": "nightmare-edge-02", "name": "Black stone to ruin floor edge", "category": "edge",
             "size": [512, 128], "pixel_grid": 4, "colors": 48, "mode": "band",
             "tileable": "x", "flat_border": False},
            {"id": "nightmare-edge-03", "name": "Ruin floor to violet clay edge", "category": "edge",
             "size": [512, 128], "pixel_grid": 4, "colors": 48, "mode": "band",
             "tileable": "x", "flat_border": False},
        ],
    },
    {
        "name": "floors",
        "grid": "2x2",
        "size": "1024x1024",
        "montage": "decals",
        "prompt": check(
            "GAME ASSET TEXTURE SHEET, 1024x1024, 2x2 grid of 4 square TERRAIN TILES, one per "
            "quadrant, each alone on a plain pure white #FFFFFF background with no shadow, no "
            "gradient, no frame, no border, no vignette. "
            "TOP LEFT tile: dry cracked violet clay, sparse thin hairline cracks and small grit. "
            "TOP RIGHT tile: flat black shale, fine even grain, a few pale chips. "
            "BOTTOM LEFT tile: broken ruin floor, dusty grey-violet flagstones with cracks and "
            "olive moss in the joints. "
            "BOTTOM RIGHT tile: dry purple dirt with separate hairline crack patches, clearly "
            "different from the top-left clay. "
            "Each tile is a flat top-down texture filling its whole square, seamless in every "
            "direction, texture only about 25 percent coverage over a solid flat base colour, the "
            "base colour fully solid and unvarying, small irregular patches scattered "
            "asymmetrically, no large clumps, no ring framing, no edge lighting. "
            + PIX +
            " No vertical walls, no objects standing up, no cast shadow, no text."
        ),
        "assets": [
            {"id": "nightmare-floor-extra-04", "name": "Dry cracked violet clay", "category": "floor",
             "size": [512, 512], "pixel_grid": 4, "colors": 48, "mode": "band",
             "tileable": "xy", "flat_border": True, "border_band": 8},
            {"id": "nightmare-floor-extra-05", "name": "Broken ruin floor", "category": "floor",
             "size": [512, 512], "pixel_grid": 4, "colors": 48, "mode": "band",
             "tileable": "xy", "flat_border": True, "border_band": 8},
        ],
    },
    {
        "name": "shadows",
        "grid": "2x2",
        "size": "1024x1024",
        "montage": "decals",
        "prompt": check(
            "GAME ASSET SHEET, 1024x1024, 2x2 grid of 4 separate SOFT CONTACT SHADOW shapes, one "
            "per quadrant, each floating alone on a plain pure white #FFFFFF background. Each "
            "shadow is a soft-edged grey-violet blur, darkest at the centre and fading smoothly to "
            "nothing at the rim, no hard outline, no colour, no texture, no object above it, only "
            "the shadow shape itself. "
            "TOP LEFT: a small compact irregular rounded flattened pebble shadow. "
            "TOP RIGHT: a small unequal double-lobed root shadow, clearly a different contour. "
            "BOTTOM LEFT: a medium low broad asymmetrical boulder footprint with two uneven "
            "bulges. "
            "BOTTOM RIGHT: a medium broken-oblong contact footprint, corners deeply softened and "
            "unequal, not a sharp rectangle. "
            "No cast shadow shape of a tree, no long silhouette, no sharp rectangular or elliptical "
            "boundary, no rays, no baked highlights, no text."
        ),
        "assets": [
            {"id": "nightmare-shadow-01", "name": "Small pebble contact shadow", "category": "shadow",
             "size": [128, 64], "pixel_grid": 1, "colors": 8, "mode": "shadow", "soft_alpha": True},
            {"id": "nightmare-shadow-02", "name": "Small double-lobed root shadow", "category": "shadow",
             "size": [160, 64], "pixel_grid": 1, "colors": 8, "mode": "shadow", "soft_alpha": True},
            {"id": "nightmare-shadow-03", "name": "Medium boulder contact shadow", "category": "shadow",
             "size": [256, 96], "pixel_grid": 1, "colors": 8, "mode": "shadow", "soft_alpha": True},
            {"id": "nightmare-shadow-04", "name": "Medium oblong contact shadow", "category": "shadow",
             "size": [256, 128], "pixel_grid": 1, "colors": 8, "mode": "shadow", "soft_alpha": True},
        ],
    },
    {
        "name": "portal-dormant",
        "size": "512x512",
        "montage": "props",
        "prompt": check(
            "GAME ASSET SPRITE, 512x512. ONE isolated 16-bit pixel-art object, centered, seen "
            "straight on from the front: a closed black magic portal arch. A tall gothic arch of "
            "dark violet-black stone, narrow and symmetrical, with 4 thick corner posts whose tips "
            "curve inward, a closed thorny vine seedbud sealed in the middle of the archway, faint "
            "dormant violet #B26BFF glow deep inside the opening, moss at the base. It is a flat "
            "cutout with a clean irregular silhouette, fully visible with margin around it, on a "
            "plain pure white #FFFFFF studio background with no shadow, no gradient, no ground, "
            "no scenery. " + PIX + " No text, no characters."
        ),
        "assets": [
            {"id": "nightmare-portal-dormant", "name": "Black magic portal dormant", "category": "portal",
             "size": [448, 448], "pixel_grid": 4, "colors": 48},
        ],
    },
    {
        "name": "portal-active",
        "size": "512x512",
        "montage": "props",
        "prompt": check(
            "GAME ASSET SPRITE, 512x512. ONE isolated 16-bit pixel-art object, centered, seen "
            "straight on from the front: the SAME black magic portal arch as its dormant state, "
            "same silhouette and proportions. A tall gothic arch of dark violet-black stone, narrow "
            "and symmetrical, with 4 thick corner posts whose tips curve inward, a thorny vine "
            "seedbud in the middle of the archway, but now the archway is wide open and blazing "
            "with bright violet #B26BFF energy, strong inner glow, sparks of light inside. It is a "
            "flat cutout with a clean irregular silhouette, fully visible with margin around it, on "
            "a plain pure white #FFFFFF studio background with no shadow, no gradient, no ground, "
            "no scenery. " + PIX + " No text, no characters."
        ),
        "assets": [
            {"id": "nightmare-portal-active", "name": "Black magic portal active", "category": "portal",
             "size": [448, 448], "pixel_grid": 4, "colors": 48},
        ],
    },
    {
        "name": "campfire",
        "size": "2048x512",
        "montage": "props",
        "prompt": check(
            "GAME ASSET ANIMATION SHEET, 2048x512, four 512x512 cells side by side, each holding "
            "ONE 16-bit pixel-art campfire on a plain pure white #FFFFFF background, no shadow, no "
            "ground, no scenery. All four cells show the SAME small campfire of 4 charred logs and "
            "grey stones, only the flames differ: cell 1 short tongues of orange flame, cell 2 "
            "taller licking flames, cell 3 flames leaning sideways, cell 4 flames shrinking to "
            "embers. Flames are warm orange #E08A3C with a hot yellow core, no glow spill on the "
            "background. " + PIX + " No text, no characters."
        ),
        "assets": [
            {"id": "nightmare-prop-13", "name": "Survivor camp fire", "category": "prop",
             "size": [768, 192], "frame_px": [192, 192], "frames": 4, "fps": 5,
             "pixel_grid": 4, "colors": 48, "mode": "strip"},
        ],
    },
    {
        "name": "wisp",
        "size": "2048x512",
        "montage": "props",
        "prompt": check(
            "GAME ASSET ANIMATION SHEET, 2048x512, four 512x512 cells side by side, each holding "
            "ONE 16-bit pixel-art floating ghost wisp lamp on a plain pure white #FFFFFF "
            "background, no shadow, no ground, no scenery. All four cells show the SAME wisp: a "
            "small pale violet flame-like glow with 3 thin trailing wisps curling below it and a "
            "tiny dark iron ring at the top, only the flame shape and the wisps differ between "
            "cells. The glow is cool violet #B26BFF fading to pale lavender, translucent looking, "
            "never a bright white blob. " + PIX + " No text, no characters."
        ),
        "assets": [
            {"id": "nightmare-prop-14", "name": "Ghost wisp lamp", "category": "prop",
             "size": [512, 160], "frame_px": [128, 160], "frames": 4, "fps": 5,
             "pixel_grid": 4, "colors": 48, "mode": "strip"},
        ],
    },
    {
        "name": "marker",
        "size": "2048x512",
        "montage": "props",
        "prompt": check(
            "GAME ASSET ANIMATION SHEET, 2048x512, four 512x512 cells side by side, each holding "
            "ONE 16-bit pixel-art arrival marker on a plain pure white #FFFFFF background, no "
            "shadow, no ground, no scenery. All four cells show the SAME glowing ring lying flat "
            "on the ground, seen from above, only the ring changes: cell 1 a small dim ellipse, "
            "cell 2 a brighter wider ellipse, cell 3 a bright wide ellipse with a second inner "
            "ring, cell 4 the widest brightest ellipse fading at the edges. The ring is a thin "
            "line of pale violet #B26BFF light with soft violet spill, hollow in the middle, "
            "never a filled disc. " + PIX + " No text, no characters."
        ),
        "assets": [
            {"id": "nightmare-marker-arrival", "name": "Arrival light ring", "category": "marker",
             "size": [1024, 256], "frame_px": [256, 256], "frames": 4, "fps": 6,
             "pixel_grid": 4, "colors": 48, "mode": "strip"},
        ],
    },
]

FX = [
    ("fx-01", "violet soul embers", "slow drifting motes of dull violet light, soft round sparks "
     "of 3 different sizes, fading as they rise"),
    ("fx-02", "shadow crystal shards", "small angular violet crystal chips breaking apart and "
     "falling, hard faceted bits with a cold edge"),
    ("fx-03", "poison mist puffs", "soft round clouds of sickly olive green vapour swelling and "
     "dissolving, 4 loose puffs per cell"),
]
for _id, _name, _desc in FX:
    JOBS.append({
        "name": _id,
        "size": "2048x512",
        "montage": "props",
        "prompt": check(
            "GAME ASSET ANIMATION SHEET, 2048x512, four 512x512 cells side by side, each holding "
            "ONE set of 16-bit pixel-art particles on a plain pure white #FFFFFF background, no "
            "shadow, no ground, no scenery. All four cells show the SAME particle effect in four "
            "different phases of motion: " + _desc + ". The particles are the only thing in the "
            "cell, sparse and separated, never a solid mass, no characters, no props. "
            + PIX + " No text."
        ),
        "assets": [
            {"id": f"nightmare-{_id}", "name": _name, "category": "fx",
             "size": [512, 128], "frame_px": [128, 128], "frames": 4, "fps": 6,
             "pixel_grid": 2, "colors": 48, "mode": "strip", "soft_alpha": True},
        ],
    })

BACKDROPS = [
    ("backdrop-far-01", "Black island in a purple sea",
     "a distant black island silhouette floating in a flat dark violet sea under a heavy violet sky",
     "backdrop_far"),
    ("backdrop-far-02", "Violet moon",
     "a large pale violet full moon hanging alone in an empty dark violet night sky with a few "
     "thin cloud bands",
     "backdrop_far"),
    ("backdrop-far", "Far scene of the nightmare island",
     "a far horizontal band: a low black island ridge on the horizon, a flat violet sea below it "
     "and a dark violet sky above it, one flat horizon line across the middle",
     "backdrop"),
    ("backdrop-mid", "Mid scene of the nightmare island",
     "a mid horizontal band: silhouettes of broken ruined arches, dead bare trees and a ruined "
     "tower on the horizon, a flat violet sea below, one flat horizon line across the middle",
     "backdrop"),
    ("backdrop-near", "Near scene of the nightmare island",
     "a near horizontal band: large silhouettes of dead gnarled trees, a leaning ruined wall and "
     "rocky mounds along the horizon, a flat violet sea below, one flat horizon line across the "
     "middle",
     "backdrop"),
]
for _id, _name, _desc, _cat in BACKDROPS:
    JOBS.append({
        "name": _id,
        "size": "2048x1024",
        "montage": "props",
        "prompt": check(
            "GAME BACKDROP BAND for a 2D HD-2D RPG, 2048x1024, a wide horizontal panorama band that "
            "fills the entire frame edge to edge, no border, no frame, no text, no UI, no "
            "characters, no foreground objects, no ground in front of the viewer. The scene is "
            + _desc + ". Paint it as flat 16-bit pixel art: chunky pixel clusters, 40-48 flat "
            "colors, 2-4 tones per material, hard edges, no gradients, no photoreal texture, no "
            "painterly shading, no bloom, no lens flare, no vignette. Distant layers are low "
            "contrast and slightly hazed. Palette: deep plum #241B36, violet #3A2B52, dust "
            "violet #5B3F7A, faint glow #B26BFF used sparingly, sickly olive #4E7A4A for "
            "vegetation."
        ),
        "assets": [
            {"id": f"nightmare-{_id}", "name": _name, "category": _cat,
             "size": [1280, 384], "pixel_grid": 2, "colors": 48, "mode": "sheet",
             "tileable": "x"},
        ],
    })

LANDMARKS = [
    ("survivor_camp", "Toppled stone altar segment",
     "a toppled collapsed stone altar segment lying flat on the ground: a stepped block of "
     "weathered tan and grey masonry with chipped corners, moss on one side, half sunk into the "
     "soil",
     "refs/landmark-ref-survivor_camp.png", [384, 288]),
    ("east_magic_island", "Small green bromeliad rosette",
     "a small spiky rosette plant: 9 pointed green leaves fanning from a short stem, a green "
     "center with no red core, dark green and olive leaves with yellow-green tips, on a short "
     "twisted brown root base",
     "refs/landmark-ref-east_magic_island.png", [256, 224]),
    ("ruins", "Stacked ruin boulders",
     "a stack of large weathered tan and beige boulders forming a ruined rock mound about twice "
     "the height of a person, patchy moss on the tops, dark crevices between the blocks",
     "refs/landmark-ref-ruins.png", [384, 320]),
    ("disaster_gate", "Purple flowering vine bush",
     "a leafy vine bush with a cluster of vivid magenta violet flowers at the top, dark green "
     "foliage below, thin curling tendrils",
     "refs/landmark-ref-disaster_gate.png", [320, 288]),
    ("despair_land", "Giant broadleaf fern rosette",
     "a giant tropical fern rosette: many long spear shaped fronds fanning out from a central "
     "stalk, deep forest green with olive shadows and a rust red core, about twice the height of "
     "a person",
     "refs/landmark-ref-despair_land.png", [352, 288]),
]
for _map, _name, _desc, _ref, _size in LANDMARKS:
    JOBS.append({
        "name": f"landmark-{_map}",
        "size": "512x512",
        "montage": _ref,
        "subject_ref": ROOT / _ref,
        "prompt": check(
            "GAME ASSET SPRITE, 512x512. ONE isolated 16-bit pixel-art object, centered, standing "
            "on the ground seen from a slight three-quarter front camera: " + _desc + ". "
            "The attached image is the ORIGINAL game map and is a CONTENT reference for this "
            "object only: do not draw the map, draw only this single object. It is a flat cutout "
            "with a clean irregular silhouette, fully visible with margin around it, on a plain "
            "pure white #FFFFFF studio background with no shadow, no gradient, no ground, no "
            "scenery. " + PIX + " No text, no characters."
        ),
        "assets": [
            {"id": f"nightmare_island_{_map}-landmark-02", "name": _name, "category": "prop",
             "size": list(_size), "pixel_grid": 4, "colors": 48},
        ],
    })


if __name__ == "__main__":
    print(json.dumps([{"name": j["name"], "size": j["size"],
                       "assets": [a["id"] for a in j["assets"]],
                       "prompt_chars": len(j["prompt"])} for j in JOBS],
                     ensure_ascii=False, indent=1))
    for n, head in OVERLONG:
        print("OVERLONG", n, head)
    print("jobs:", len(JOBS), "assets:", sum(len(j["assets"]) for j in JOBS))
