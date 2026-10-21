# Review 152 species

Open http://127.0.0.1:8125/ after starting:

```sh
rtk proxy /Users/phileanh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B tools/assets/p10_review_server.py
```

The server binds only to localhost and requires Pillow. It loads the 152-species
roster, current selected redraws, and explicit pending draft overrides from the
battle trial manifest. Restart the server after changing atlas selection.

Use sort/search, star and race filters, animation selection, pause/frame controls,
and the approval/comment panel below the preview. “Size thử trong game” is a
presentation trial, not an activated runtime configuration.

Feedback automatically saves to
`.ai/plan/phases/P10-pet-model/redraw-kit/owner-reviews.json`. Records are keyed by
species ID and atlas SHA-256 so approval of an older drawing does not approve a
new drawing. Existing explicit human approval is shown only for a matching hash.
Export downloads the saved feedback as JSON.

Focused persistence verification (uses temporary feedback only):

```sh
rtk proxy /Users/phileanh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B tools/assets/test_p10_review_server.py
```

This review tool does not change the game's runtime atlas or certify art completion.
