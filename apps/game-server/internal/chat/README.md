# internal/chat

Chat system — implements spec §38. TBD.

Will host channel routing (world, guild, party, private), per-channel
rate limiting and the wire namespace `chat.*` declared in spec §50.

The current `internal/transport/server.go` exposes `GAME_ALLOWED_ORIGINS`
for WebSocket handshake; once `chat/` lands it should own that allow-list
alongside the message routing.