extends SceneTree
##
## Phimond server entry point (TCP variant).
##
## Uses a raw TCPServer on port 8080 and speaks newline-delimited JSON. A Node
## WS proxy (ws-proxy.mjs) sits in front of this for the browser; native TCP
## clients can also connect directly.
##
## Run locally:
##   cd server && godot --headless -s res://server_main.gd
## Run in Docker: same as before.
##

const PORT: int = 8080


func _init() -> void:
	print("[Phimond] Booting...")

	var root_node := Node.new()
	root.add_child(root_node)

	var world: Node = preload("res://game/world.gd").new()
	root_node.add_child(world)

	# Persistent per-player storage (JSON file per name in /app/data/players/).
	# Wired into the world so add_player() loads prior sessions and the
	# BYE/disconnect handlers write the latest state.
	var save: Node = preload("res://storage/player_save.gd").new()
	root_node.add_child(save)
	world.attach_save(save)

	# Build a minimal TCP server. The previous WS-based server had a known
	# handshake issue with Chromium; this variant only handles TCP and a tiny
	# length-prefixed JSON protocol — no WebSocket framing.
	var server: Node = preload("res://net/tcp_server.gd").new(world)
	root_node.add_child(server)

	var err: int = server.start(PORT)
	if err != OK:
		printerr("[Phimond] Failed to start TCP server on port %d (err=%d)" % [PORT, err])
		quit(1)
		return

	print("[Phimond] Ready. TCP listening on 0.0.0.0:%d" % PORT)
