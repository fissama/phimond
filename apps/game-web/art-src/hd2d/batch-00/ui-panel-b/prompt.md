# Image generation provenance

Route: host_image / built-in image_gen
Model: not exposed by tool
Source job: ui-sheet

## Attempt 1

Use case: ui-mockup. Production CUTOUT game UI asset pack for Phimond HD-2D, not a full screen. Render a 3072x2048 sheet on EXACT pure solid #FF00FF magenta background. Exactly EIGHT isolated assets, generous empty gaps, no text or numbers. Arrange TWO COLUMNS, option A left and option B right. Each column: at top a large horizontal empty MENU PANEL, then below three separate identical-size tilted pill BUTTONS in normal, pressed and disabled states. Panel identity from input 1 and input 3: deep midnight-blue flat center, delicate old gold edge, elaborate asymmetric fantasy leaf scrollwork at left edge and corner ornaments, clean thin gold edge on other sides. Preserve that distinctive silhouette but redraw as crisp pixel art. Center MUST be flat and freely stretchable; ornaments limited to corner/edge regions for 9-slice; no embossed markings in center. Aim panel ~1476x696 at @3x original. Button identity from input 2: narrow diagonal oval, long axis rises from bottom left to top right at exactly 37 degrees, outer gilded rim, cyan/blue interior, entirely blank central text-safe area. Buttons aim 201x186. Normal cyan blue face, pressed deeper blue/inset bevel, disabled desaturated steel-blue with dull gold rim; same geometry in all three. A uses original sapphire/navy and bright antique gold. B uses slightly cooler indigo navy and restrained aged gold, simpler edge ornament; both match source motifs. Images 4 and 5 approved pet sheets define crisp pixel shading and colored outlines only. Clean square color clusters, 2–4 tones per material, no soft vector edges. NO built-in letters, symbols, word Choose, grid, labels, separators, drop shadows, glow, fog or gradient behind assets. Every asset fully contained with margin, no overlaps; hard opaque silhouette against flat magenta up to every edge.

## Ordered source references (first generation)

- /Users/phileanh/rust/phimond/apps/game-client/assets/reference/hud/panel_menu.png — sha256 c497133e7ca095f6eac104ba8139a008cbb43580d525c021cb94d4d5fd436a6d
- /Users/phileanh/rust/phimond/apps/game-client/assets/reference/hud/button_confirm.png — sha256 f0b9694abe1dcf6bac486c753c95923a2ec98ecf558905c1d64be465174c63d3
- /Users/phileanh/rust/phimond/apps/game-client/assets/reference/ui/UI.png — sha256 dedba6310459fb7301226aaef20e6aaf8f0b5c08234422515bfc6e67c80acee3
- /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — sha256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
- /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — sha256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

Image-edit attempts use the previous raw as their edit target, as recorded in generation-jobs.json.

## Raw SHA256

- raw-01.png: 722e791204209126dd6cd2ef4082146f3c256c3451e8d028a02c78e2061c5656


## Targeted nine-slice repair

Edit ONLY the two large menu PANELS in this source UI sheet to make them real ornament-preserving 9-slice assets. Keep their blue A / indigo B palette, old gold pixel trim, overall outer silhouettes, distinctive asymmetric left notches, and style. Return only those two panels, A on left and B on right, on a pure flat #FF00FF magenta key background with generous empty margins; omit the small buttons because they are already delivered separately. THE ESSENTIAL REPAIR: move ALL curly gold scrollwork into FIXED corner regions. The left and right edge MIDDLE 50% of each panel's height must be perfectly plain, straight thin gold vertical rails without any curl, bulge, leaf, gem or repeating ornament. The top and bottom edge middle 50% must likewise be plain straight thin gold rails. Any decorative curls from the source must be confined to the top-left and bottom-left fixed corner clusters; small right ornaments only in top-right and bottom-right corners. All corner ornament pixels fit within uppermost/lower-most 25% of panel height. Leave a flat solid navy center A and solid indigo center B, absolutely no gradient or texture. Corners will never scale; middle strips will stretch. Keep crisp square pixel clusters, hard 3-tone metal steps. No text, symbols, labels, glow, haze, ground or shadows. No blurred vector edges. Complete panel silhouettes, no clipping. This is a targeted repair of the existing approved-direction candidate, not a new design.

Reference/edit target: ui-sheet/raw-01.png. Only panels are revised. Buttons retain their original generation. Output: raw-02.png. Route: built-in image_gen.

SHA256 raw-02.png: 7cc576107c1ea7a5b1c6cb4771ca2db720aa039cc522c0007cbc0a8b07ce19fa
