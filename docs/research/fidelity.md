# Historical evidence and reconstruction fidelity

Researched 2026-09-17. No original executable, complete authoritative database, or source code was supplied. Searches retrieved contemporary player guides and a later catalog description, not a complete rules specification. **100% parity is unverified and is not claimed.** Original Phimond presentation and recipe names are used.

## Sources and the decisions they support

- [2010-05-19 player guide](https://m.ali213.net/gonglue/100519/11194.html): starts with a snail; describes level-30 opposite-gender, same-star, different-race synthesis; specifically says a parent must learn a skill before it can be inherited. Its approximate inheritance estimate is not an exact recovered formula. Evidence is version-specific and rated likely.
- [2010-12-22 synthesis guide](https://m.ali213.net/gonglue/101222/9961.html): describes a revised level-20 requirement, ranch interaction, learned reusable recipes, synthesis souls and noncombat parents. This conflicts with treating the older level-30 rule as universal. Gender and race restrictions not stated here remain uncertain.
- [2010-09-08 skill guide](https://m.ali213.net/gonglue/100908/10529.html): supports seven element/race identities, status/counter relationships and race specialties. Notable quantitative claims: a sleeping target wakes on attack and takes twice normal damage; Blind reduces hit rate by 90%; Doom prevents attacks and eventually kills. Current data uses these values as likely, tied to this guide. Exact durations and petrification defense bonus are still reconstructed.
- [2010-08-05 breeding guide](https://m.ali213.net/gonglue/100805/10818.html): supports appraisal around a 1000 reference scale, training desired skills before synthesis and extended zone progression. It is player advice, not a guarantee about every version.
- [2010-10-27 capture/species guide](https://m.ali213.net/gonglue/101027/10192.html): used to correct Windmill Spirit to the spirit race and the chest/sea-demon archetypes to physical. Actual Phimond names, numeric growth and spawn distribution remain reconstructed. Windmill in the initial beach is a deliberate slice placement, differing from the guide's mountain location.
- [2009-05-12 distribution guide](https://m.ali213.net/gonglue/090512/12935.html): additional research lead for exact room/spawn reconstruction, not imported as a complete spawn table.
- [Taiwan game listing](https://acg.gamer.com.tw/acgDetail.php?s=57017): supports horizontal scenes, turn-based pet combat, synthesis, multiple pets and the later dragon expansion. It does not establish exact implementation details.

Broad searches often return unrelated games with the words spirit beast. Those results were rejected. No claims from unrelated Pokémon, World of Warcraft or modern similarly named games were used.

## Active ruleset

`data/balance/rules.json` selects the reconstructed first slice; recipes carry their own configurable requirements. `historical-rulesets.json` records alternatives, but it is a research reference, not an active selector. The default combines the later level-20 rule with the older opposite-gender condition. This is explicitly a **hybrid reconstructed ruleset**, not a claim to match one original release.

All skill costs/power/duration/learn levels, species qualities/growth, capture rates, XP/gold rewards, new recipe graph, strengthening/blessing magnitudes, map gates and quest text are reconstructed. New presentation/content is independent of the original artwork/dialogue/music. The dragon race is reserved with unknown mechanics and has no invented native skill tree.

## Still unknown

Exact damage, hit/crit, initiative, capture and inheritance formulas; original random distributions; original full species/skills/item/drop databases; complete synthesis graph; exact strengthening/blessing/appraisal formulas; original multi-pet targeting, military rank, arena/PvP/guild/auction fees and version-specific rules. Progression after the initial beach, full sub-room topology and production balance require further research and implementation.

A recovered detail should update the relevant JSON and this evidence ledger, then run content validation, deterministic battle tests and distribution simulations. Do not relabel a reconstructed value as confirmed merely because it appears in a player guide.
