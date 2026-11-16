# Nightmare — initial art checkpoint 2026-10-24

Status: STARTED, kit incomplete, all approved=false. This is the first asset package, not delivery of complete maps or a closed phase.

12 final drafts:3roots,3shadow-crystalclusters,and6map-specificlandmarks(onepermap).7realbuilt-inimage_gensheetsgenerated; no API/codeart/finalpropresampling. The model and dollar estimate are not exposed. All raw originals retained byte-identically; per-asset prompt.md lists actual attachment files and hashes. Landmark jobs attach a montage of six original references, with all original source hashes in job.json. Those are interpretations of observed content, never claimed recovered APK assets.

All12finals actually seen at4x over dark/checker, including split top/bottom panels for tall tree. Each48colors,binaryalpha,1connectedcomponent,adequatealpha margins. Pixel cutout/quantization and native1:1padding only. Crystal keying changed35/55RGBdistance+narrowradius1despill to preserve purple interior; old failed keyed exports retained. Bud sheet has uneven row centers: actual source ownership boundary y600 preserves full roots, not a fixed512cut. Roots large attempts and all bone/relic candidates retained as self-rejected; they are not exported or marked drawn.

Official command `python3 tools/hd2d_audit/art_gate.py batch-11-nightmare`:exit0,162assets,0errors,0warnings. Important:positional kit argument is ignored by existing script; this actually scans desert,nightmare,tomb,windrock together. Full log gate-initial-20261024.log. Separate official size_check exit0(size OK). Final hashes/checklist parity/contact freshness verified. These checks prove the existing drafted assets' mechanical properties, NOT kit completeness/navigation/collision. No audit or waiver edits.

Weakest3:
- nightmare-prop-02: bark grain busy/soft at4x
- nightmare-prop-09: violet saturation and bright facet contrast strong
- nightmare_island_survivor_camp-landmark-01: warm stone can read as bronze

Remaining before full-kit delivery:floor8,edges3,trees3withsway-split,bones/relics,ruinwall,camp tent+fire4frames,wisp4frames,backdrops(far/moon/layers),decals12,shadows4,shared-maskportalpair,arrival4frames,FX3,optional second landmarks. Portal/backdrop duplicate checklist IDs need explicit coverage mapping. Scene assembly and live screenshots/navigation are not part of this first package. No runtime/scene integration.

World backlog:54maps/14kits initially assetless. Nightmare active, remaining13kits queued(not started; no automatic background jobs). Queue at .ai/design/map-checklists/REDRAW-QUEUE-20261024.md. Other kit worker files untouched.

Manual validation runtime:Go build exit0,clean committed game-server source; git fetch origin completed and HEAD55ahead/0behind at fetch. Server PID20872,127.0.0.1:8090,GAME_METRICS=1,log/tmp/p00-serve.log,health200. Godot editor6007notlistening. Existing global dirty working tree preserved; no commit as art-worker rules require. New art is available in contact-sheet.png for manual review, not in runtime.
