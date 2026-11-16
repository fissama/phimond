# R3 N09 prompts and references

Generated one image per asset, using the current `ui-minimap.png`, `chat-panel.png`, and tab art as visual references. The UI frame references were used for material and proportions only.

## chat-frame.png

Create one 9-slice chat panel frame for a Three.js game, final canvas 768×176, wide and low. Use attached ui-minimap for the exact double-gold UI language and attached chat-panel for the wide panel geometry; attached chat-tab-normal is only a palette reference. Thin double gold border: dark outer gold, bright inner gold, tiny restrained gold corner ornaments. The entire panel interior must be a flat, uniform #FF00FF key color, with NO dark navy-teal band or fill inside. Border side edges between corners are plain and tileable for 9-slice. Keep all border detail within the outermost 8 pixels; no large center decoration. Pixel-art edges, no antialiasing, no blur, no text, no tabs in this image, no watermark. One image only.

References: `apps/client/public/ui/ui-minimap.png`, `apps/client/public/ui/chat-panel.png`, `apps/client/public/ui/chat-tab-normal.png`.

## chat-tab-normal.png

Create one standalone chat-tab-normal UI asset for the same game. Target 160×44, very wide low rectangle with subtly rounded/Octopath-style cut corners. Dark navy-teal filled face, thin restrained gold outline (dark outer gold, brighter inner line). Flat fill, no text, no icon, no shadow, no bottom-open gap. Match the attached chat-panel and chat-tab-normal proportions/materials but remove the blue palette: use only dark navy-teal and muted gold. Crisp pixel clusters, no blur, no antialiasing, no watermark. One tab only with transparent background outside its silhouette.

References: `apps/client/public/ui/chat-panel.png`, `apps/client/public/ui/chat-tab-normal.png`, `apps/client/public/ui/ui-minimap.png`.

## chat-tab-selected.png

Create one standalone chat-tab-selected UI asset for the same game, target 160×44, matching the attached normal tab's shape, scale, interior fill, outer dark gold stroke and corner proportions. The selected state differs only in the brighter golden outline and an OPEN BOTTOM EDGE: remove the lower gold border across the central 80% of the tab so the dark navy-teal face joins seamlessly with the chat frame below; keep only small lower-corner returns. Dark navy-teal solid face, brighter gold thin outline, no blue, no text or icon, no shadow. Pixel-art clusters, no blur or antialiasing. One tab only, transparent outside the silhouette, no checkerboard or watermark.

References: `apps/client/public/ui/chat-panel.png`, `apps/client/public/ui/chat-tab-selected.png`, `apps/client/public/ui/ui-minimap.png`, generated normal-tab candidate `r3-n09/raw/chat-tab-normal-source.png`.

## Finishing

Raw generation outputs were resized in premultiplied alpha to the target canvases, thresholded to binary alpha, then quantized together to one 48-color palette. Final files are in `delivery-palette-v1/`. See `apply-qa.json` and final-size PNGs before review.
