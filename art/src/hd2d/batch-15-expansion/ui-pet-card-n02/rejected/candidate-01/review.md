# N02 pet-card candidate 01 — rejected

Route: Codex built-in image generation (`host_image`).

The image is compositionally close to a pet HUD plate, but it is not suitable for processing as the contracted pixel-art UI asset. Source is 2103×748, while target main card is 360×128. Inspection found 147,375 RGBA colors and many intermediate alpha values (not binary). The two wells are also rendered as black-looking apertures rather than a verified exact transparent mask. Geometry therefore has not been accepted or normalized by resizing.

Required next attempt: generate a clean flat-color pixel-art plate with explicit magenta key wells, then key, crop to exact 360×128, quantize to <=48 visible colors and binary alpha, and verify the portrait ring (104 px diameter, center 68,64), level badge (28 px, center 104,100), HP trough x132–344/y40–52, and MP trough x132–344/y62–72. Generate the 264×96 sub-card separately after the main card is accepted.
