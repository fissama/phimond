# Phimond HD-2D production

Date: 2026-10-15
Scope: isolated art only; exclude approved 160 pet atlases. No runtime changes, activation, commits or pushes.

Authoritative contract: `.ai/design/hd2d-art-master-plan.md`.

## Owner art-direction clarification — 2026-10-15

The owner explicitly requires Octopath Traveler as the primary visual style. This clarifies the visual target; it does not approve any existing Batch 00 candidate.

- Keep Phimond's original object identities and the completed 160 pet atlases.
- Target Octopath-like restrained earthy palettes, readable deliberate pixel clusters, tactile wood/stone/foliage and strong material forms. Avoid fluorescent foliage, smooth vector UI and illustrative microtexture.
- Preserve clean tinted outlines and compatibility with the approved pet anchors; do not copy Octopath characters, maps, logos or interface layouts.
- Deliver isolated PNG parts at the declared density and camera. Engine lighting, depth, atmospheric fog, contact shadows, bloom and grading provide the HD-2D presentation; do not bake them into props.
- Existing A/B assets remain unapproved drafts. Re-evaluate and revise the environment/UI anchors against this direction before mass production.
User-requested toolkit: https://github.com/0x0funky/agent-sprite-forge — generate2dmap for terrain/props, generate2dsprite for UI/icons/FX, video2dsprite for actor animation when a permitted video route exists.
Route: built-in image_gen, art_source=host_image. Never substitute paid APIs or code-drawn art. Use the project's pixel style and 128 px/world-unit scale. Forge's optional scene assembly/export remains Claude's responsibility.

## Delivery gates

Batch 00: two alternatives for forest, city and UI. Produce raw PNGs, extracted individual assets, reference hashes and prompts, mechanical QA, light/dark previews, tile repeats, contact sheet and palette/style guide. User chooses the environment/UI anchors before later production, as required by the master plan.

## Queue

- [ ] 00: environment and UI anchors, user approval
- [ ] 01: Emerald Forest kit, two maps
- [ ] 02: city/palace/hall/farm/arena kits, nine maps
- [ ] 03: beach kit, five maps
- [ ] 04: ship kit and shared interaction sprites
- [ ] 05: male/female players, 49 NPCs, 17 portraits
- [ ] 06: world HUD
- [ ] 07: battle HUD, FX and status effects
- [ ] 08: menu components and enabled screens
- [ ] 09: icons from runtime catalogs
- [ ] 10: login, loading and Phimond branding
- [ ] 11+: remaining regions, each subject to the master plan's P12 regional gate

## Capability limits

Forge doctor reports host_image ready; no video generation route is available. Static sprites, sheets, PNG extraction and QA can proceed. Character animation must use a permitted route or supplied clips; do not claim static sheets are verified organic animation.
SciPy is optional and absent; NumPy fallback is available. resvg is irrelevant because code art is prohibited by the project contract.

## Existing work

The repository contains extensive pre-existing local modifications. Preserve all of them. Art-only delivery follows the master plan's explicit instruction not to commit, activate assets, or edit runtime. Manual review is through the exported art and QA previews.
