# Phimond batch-06-octopath

Draft production art; approved:false. Built-in image_gen route (host_image); no paid API, internet art or code-drawn replacement art. Not activated.

manifest.json lists separate final.png paths, exactdimensions, @3x logical_body andslice guides. UI is screen-space;world:null. Each export retains byte-identical raw, full prompt with ordered reference paths/hashes, source identity card and QA. Original APK/JAR art supplies content, pet anchors only pixel edge compatibility.

contact-sheet.png overview. game-size-preview.png is logicalsize on light/dark. review-light-dark.png provides source1x/2x. stretch-preview.png performs actual9slice at originalsize and150%width/140%height; slice guides preserve corner ornaments. Initial slice-unsafe raws retained in jobs and assetraw-01; selected generic9slice template is raw-02. Generated normal/pressed/disabled rectangular button states remain distinct.

QA: {
  "count": 66,
  "rgba": 66,
  "binary_alpha": 66,
  "palette_48": 66,
  "alpha_margin_8": 66,
  "raw_integrity": 66,
  "stretch_preview_count": 6,
  "unique_final_hashes": 45,
  "owner_approved": 0,
  "warnings": [
    "Some generated buttons/slots retain richer gloss than strictest Octopath direction; owner visual review pending.",
    "Active-screen panel IDs intentionally share one reusable blank chrome template; these are modular assets, not custom compositions.",
    "UI body is3x logical;12px source alpha padding is additional.",
    "No runtime activation or integration test."
  ],
  "failures": []
}

Known limits: shared active-screen panels are explicit modular aliases. Runtime owns layouts, labels, numerals, portraits cut from existingpetatlases, and dynamic states. Menu-icon stars are framed medallions. Specialized hatch/breeding content is static. Deferred guild/friends/mail/auction/bank/manual/charge screen art excluded; guild chat chrome is only a shared world-HUD tab. No baked text or numerals; functional X/tick/plus/minus pictograms retained.

ExactIDs: asset-ids.txt. package.py crops/rotates/resizes/quantizes generated pixels andcreates previews. finalize.py refreshes mechanicalQA andlogicalsize sheets. All generatedsource attempts preserved.
