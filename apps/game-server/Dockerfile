FROM golang:1.25-bookworm AS build
WORKDIR /src
COPY apps/game-server/go.mod apps/game-server/go.sum ./
RUN go mod download
COPY apps/game-server/ ./
RUN CGO_ENABLED=0 go build -trimpath -o /phimond ./cmd/server
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=build /phimond /usr/local/bin/phimond
COPY data/ /data/
COPY migrations/ /migrations/
ENV GAME_ADDR=0.0.0.0:8090 GAME_DATA_DIR=/data
USER 65534:65534
EXPOSE 8090
ENTRYPOINT ["phimond"]
