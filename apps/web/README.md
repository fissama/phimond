# Phimond field journal

Next.js / TypeScript companion to the Go service. No gameplay formulas or content definitions are duplicated. The encyclopedia and recursive synthesis planner read `GET /api/content`; keeper records and recursive ancestry are authenticated read-only views.

## Run

```sh
rtk npm install
rtk npm run dev
```

Open http://localhost:3100. The Go service defaults to http://127.0.0.1:8090. Copy `.env.example` to `.env.local` to override `GAME_API_URL` (server-only). Use `rtk npm run build`, `rtk npm run typecheck`, and `rtk npm test` to verify; `rtk npm start` serves the production build on port 3100.

A disconnected backend produces an explicit offline state, never sample account data. Public catalog entries retain source/confidence metadata. Research confidence means the catalog author’s assessment, not a claim that reconstructed formulas match an original game. The planner expands both parent dependencies, supports alternative recipes, shows requirements without calculating outcomes, and stops cycles. Repeated branches require distinct parent instances.

Sessions use an HttpOnly, SameSite=Strict cookie and server-side proxy. The opaque Go token never enters browser JavaScript or URLs. Production cookies require HTTPS (localhost development uses `npm run dev`). Mutating auth requests require a matching Origin header. Deploy the Next server behind a trusted HTTPS reverse proxy; configure its public origin consistently. The cookie expiry is seven days; the Go service remains authoritative for token validity. No third-party authentication or game writes are exposed by this companion.

Visual identity is an original botanical field journal; specimen emblems are decorative, not creature illustrations. Google Fonts is optional and falls back to system serif/sans fonts. Public catalogs are fetched fresh, not bundled. Account and ancestry responses are no-store. No fake success view is rendered if the server is unavailable.

## Live browser smoke

With Go on port 8090 and Next on port 3100, run `rtk npm run test:live`. The script creates one random test keeper account and logs it out; the test account remains in the dedicated game database. It covers catalog tabs/search, synthesis trees, account registration/login, HttpOnly cookies, owned pets, lineage, logout, browser errors, and mobile overflow. Credentials are never printed. The browser test writes desktop, planner, and mobile screenshots to `artifacts/`.

Install the matching test browser with `rtk npx playwright install chromium`, or set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` to an existing Chromium executable. `WEB_TEST_URL` overrides the default local companion URL.
