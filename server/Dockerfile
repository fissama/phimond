# Phimond Godot game server.
#
# Build:  docker build -f server/Dockerfile -t phimond-server .
# Run:    docker run --rm -p 8080:8080 phimond-server
#
# Build context = project root (we COPY server/ + .docker-cache/godot/ into /app).
#
# The Godot binary is downloaded once on the host (see README → "Docker setup")
# and placed in .docker-cache/godot/. We bake the binary into the image so the
# container has no internet dependency at runtime.

FROM debian:bookworm-slim

# Runtime deps for Godot headless. libfontconfig + libfreetype are needed even
# in headless mode for the default theme/font fallback. libGL/libxinerama/libxi
# are required by Godot's core libraries.
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        libfontconfig1 \
        libfreetype6 \
        libgl1 \
        libxinerama1 \
        libxcursor1 \
        libxrandr2 \
        libxi6 \
        libpulse0 \
        libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Install Godot from local cache (the binary is reused across builds).
COPY .docker-cache/godot/Godot_4.7.2_linux_arm64 /usr/local/bin/godot
RUN chmod +x /usr/local/bin/godot && godot --version

WORKDIR /app
COPY server/ ./

# Create the player save directory at build time so the mount target exists
# even on first run. Bind-mounted from the host (see docker-compose.yml) so
# saves survive container restarts and image rebuilds.
RUN mkdir -p /app/data/players

EXPOSE 8080

CMD ["godot", "--headless", "--path", "/app", "-s", "res://server_main.gd"]
