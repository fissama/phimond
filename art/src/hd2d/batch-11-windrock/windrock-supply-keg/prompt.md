# windrock-supply-keg

Route: built-in image_gen. Model not exposed.

Phimond HD2D game props at ONE CONSISTENT PHYSICAL SCALE.1536x1024sheet, THREEcolumns TWOrows. Solid#FF00FF. Do NOT scale each prop individually to fit a cell: the BIG mountain props top row should tower over the VERY TINY handheld camp items bottom row, bottom objects ONLY ONE FIFTH THE HEIGHT of top objects.
TOPLEFT: tall narrow split slate spire, leaning tip, olive lichen, little snow, body150x360px. TOPMIDDLE: different jagged twin-needle rock column, wider base and rightbroken spur, body190x340. TOPRIGHT: broad low cliff face, serrated diagonal slate layers, small flat snowy lip, body320x240.
BOTTOMLEFT: VERY TINY horizontal water keg,body65x50px, two woodfeet and smallspigot. BOTTOMMIDDLE: VERY TINY squat wood barrel,body50x60px, ironhoops and olivepatch. BOTTOMRIGHT: VERY TINY firewood bundle,body85x45px, olivewrap graymetalclasp. CRITICAL: bottom row camp items are vastly SMALLER than top cliffs; huge magenta space around them. No object fills its cell. One connected cutout each,no loosebits,ground,castshadows,letters or decorations.
Reference1 original mountain CONTENT only;2 approved GPT stone/wood STYLE;3/4 pet outlines only. Octopath crisp chunky pixels, dark material-colored contours, warm upper-left small highlights/cool recesses, broad2-4tones/material, no dither/noise/blur/bloom. Bluegrayrock, ivorysnow, olive vegetation/cloth, brownwood, coolmetal.33-48regionalcolors each. Match approvedbatch01 style.
BEFORE generation native canvases: spire01 288x512 world2.25x4; spire02 320x480 world2.5x3.75; cliff448x384 world3.5x3. These are2.29-3.05players tall. Keg160x128 world1.25x1; barrel144x128 world1.125x1; wood192x128 world1.5x1: all shorter than168pxplayer/1.31world. Each source must fit with8px alpha margins. No resizing allowed, only source1:1copy/padding. Maintain physical smallness of bottomrow relative to top.

Actual attachments (ordered):
1. /Users/phileanh/Downloads/Phimond-P12-Review/map-images/windrock_mountain_camp.png — SHA256 58d68f8dcd07e2674060f59ca7851dab25d80b8eac99153c410550c3c4712f33
2. /Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-windrock/jobs/native-mixed-scale-19/reference-approved-stone-wood.png — SHA256 5062adde64479353dc3a1fdb45e53014edcc20fcbc4a5bb11024ab9c7a476199
3. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — SHA256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
4. /Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — SHA256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

QA reference montage contains these actual approved images (unmodified pixels, padding only):
[
  {
    "path": "/Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-01-octopath/rock-large/final.png",
    "sha256": "81499f1c27baf3956588ed392d6be562129926f300aa9be9dca949c781a84ea2"
  },
  {
    "path": "/Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-large/final.png",
    "sha256": "717fdf80d11ac1dadd07357cc44936ee2c4a532116b82adacb20eb9464f09106"
  },
  {
    "path": "/Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-02-octopath/wooden-crate/final.png",
    "sha256": "41eb988f9dcfeb2a6a00443fe2fd8fc804f21684302022e7fed8cc106577a83c"
  },
  {
    "path": "/Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-02-octopath/barrel/final.png",
    "sha256": "a48199166f5a03250e480c8df0e04cd67e01041d26770e33c0c4bc168cd31c2f"
  }
]

Raw: raw-19.png; SHA256 d2de5fe0efff5699373b97b11f88e30be28da3b07af29205165189262732f634; source box [0, 740, 512, 1024]; sheet extraction polygon None; translation-only source registration None. Final [160, 128]. Non-dithered 48color finish, native1:1 pixel copy and transparent padding; NO resampling. No content drawn with code.

Native scale: {"desired_world_size_before_drawing": [1.25, 1.0], "height_relative_to_player": 0.7633587786259541, "source_footprint_px": [127, 108], "resampling": "NONE; source pixels copied1:1, transparent padding only"}

Finish details: {"visible_colors": 45, "palette_source": "palette.json", "palette_include": null, "palette_exclude": null, "palette_remap": null, "base_palette_filter": null, "native_alpha": false, "documented_exception": null, "job_palette_note": null}
