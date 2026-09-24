# Phimond — Pokémon-like 2D Game (MVP slice)

Vertical slice for the **Godot headless server + Phaser 3 web client** architecture. Scope of this slice (Phase 0 + 1 of `IMPLEMENTATION_PLAN.md`):

- WebSocket connection between client and server
- Login screen (HTML input, name persisted to localStorage)
- 20×15 overworld rendered with placeholder tiles
- Server-authoritative player movement (arrow keys / WASD)
- Multiple browser tabs see each other's players move in real time
- Tall grass zones drawn on map (no encounter yet — Phase 2)

## Repo layout

```
phimond/
├── server/             # Godot 4 headless game server (GDScript)
├── client/             # Phaser 3 + TypeScript web client (Vite)
├── shared/PROTOCOL.md  # WebSocket message contract (source of truth)
├── .docker-cache/      # Godot binary cached for Docker build (gitignored)
├── docker-compose.yml  # server + client orchestration
├── IMPLEMENTATION_PLAN.md
├── test-ws.mjs         # single-client WS smoke test
├── test-multi.mjs      # multi-client sync test
└── README.md
```

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Docker + Compose | 24+ | https://docs.docker.com/get-docker/ |
| Node.js | 20+ (only for running client/tests outside Docker) | https://nodejs.org |

Verify:
```sh
docker --version
docker compose version
```

You do **not** need to install Godot on your machine — it runs inside the Docker container.

## Quick start (Docker, recommended)

### 1. One-time: download the Godot binary into the build cache

The Docker build copies Godot from a local cache instead of pulling it at build time (avoids GitHub access restrictions during build):

```sh
mkdir -p .docker-cache/godot
curl -L "https://github.com/godotengine/godot/releases/download/4.7.2-stable/Godot_v4.7.2-stable_linux.arm64.zip" -o /tmp/godot.zip
unzip -j -o /tmp/godot.zip -d .docker-cache/godot
mv .docker-cache/godot/Godot_v4.7.2-stable_linux.arm64 .docker-cache/godot/Godot_4.7.2_linux_arm64
chmod +x .docker-cache/godot/Godot_4.7.2_linux_arm64
rm /tmp/godot.zip
```

For Intel Macs replace `linux.arm64` with `linux.x86_64` and rename the binary accordingly.

### 2. Build & run the server

```sh
docker compose up -d --build server
docker logs -f phimond-server
```

You should see:
```
[Phimond] Booting...
[WS] Listening on ws://0.0.0.0:8080
[Phimond] Ready. WebSocket listening on ws://0.0.0.0:8080
```

The server is now reachable at `ws://localhost:8080`.

### 3. Run the client (locally with HMR — fastest dev loop)

```sh
cd client
npm install
npm run dev
```

Vite serves at http://localhost:3000. Open in 2+ tabs, enter different names, press arrow keys — they see each other move.

### 4. Or run the client in Docker (no Node install needed)

```sh
docker compose up -d client
```

Then open http://localhost:3000.

## Verify the server without a browser

Two scripts in the repo:

```sh
# Single client: HELLO + 2 MOVEs, prints every STATE message received.
cd client && node ../test-ws.mjs

# Two clients simultaneously: confirms each one sees the other.
node test-multi.mjs
```

Both expect the Godot server to be running on `ws://localhost:8080`.

## What's next

This slice implements **Phase 0 + Phase 1** of `IMPLEMENTATION_PLAN.md`. Next chunks (each is one focused session):

- **Phase 2** — Monster data + random encounter trigger
- **Phase 3** — Battle mechanics (damage formula, turn order, HP bars, 4-action menu)
- **Phase 4** — Replace placeholder tiles/player with AI-generated pixel art
- **Phase 5** — Save/Load via `saves/<name>.json` on the server
- **Phase 6** — Production deploy (Render/Railway for server, Vercel for client)

## Troubleshooting

**Server container restarts immediately** — check `docker logs phimond-server`. Common causes: missing Godot binary in `.docker-cache/godot/` (re-do step 1), port 8080 already taken on host.

**`socket not open`** in browser console — the server container isn't running, or `VITE_WS_URL` points somewhere else. Default is `ws://<hostname>:8080`. Override with `.env.local`:
```sh
# client/.env.local
VITE_WS_URL=ws://localhost:8080
```

**TypeScript errors** — run `npm install` in `client/` once. If your editor complains about `import.meta.env`, the `src/vite-env.d.ts` triple-slash reference should handle it.

**Apple Silicon Mac + Docker** — verified working with OrbStack (default on this machine). For Docker Desktop, ensure "Use Rosetta for x86_64 emulation" is off (we use arm64 native). On Intel Macs, swap the Godot binary as noted in step 1.
