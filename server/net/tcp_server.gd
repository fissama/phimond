extends Node
##
## Minimal TCP server with length-prefixed newline JSON protocol.
##
## Why: Godot's built-in WebSocketServer has a handshake compatibility issue with
## Chromium (browser WS upgrades come back with "Not enough response headers").
## We bypass that by speaking plain TCP from the game server and letting a tiny
## Node WS proxy (client/ws-proxy.mjs) convert to/from WebSocket for the browser.
##
## Wire format:
##   Each message is a single JSON object terminated by '\n'.
##   We read until we see a newline; anything before it is one logical message.
##   The router parses the JSON, runs the handler, and writes the response back.
##
## Public API:
##   start(port)        — bind & listen
##   send(id, payload)  — push JSON string to one client
##   broadcast(payload) — push to every connected client
##

const MAX_CLIENTS: int = 32

var port: int = 8080
var tcp_server: TCPServer = TCPServer.new()
# id -> { peer: StreamPeerTCP, player_name: String, hello: bool, buffer: String }
var clients: Dictionary = {}

# World holds authoritative game state (set at construction time).
var world: Node

# Singleton router — instantiated once, reused for every inbound message.
var router: Node


func _init(p_world: Node) -> void:
	world = p_world
	router = preload("res://net/message_router.gd").new(self, world)
	set_process(true)


func start(p_port: int) -> int:
	port = p_port
	var err: int = tcp_server.listen(port)
	if err == OK:
		print("[TCP] Listening on 0.0.0.0:%d" % port)
	return err


func _process(_delta: float) -> void:
	_accept_pending_connections()
	_poll_clients()


func _accept_pending_connections() -> void:
	if not tcp_server.is_connection_available():
		return
	while tcp_server.is_connection_available():
		if clients.size() >= MAX_CLIENTS:
			push_warning("[TCP] Max clients reached, dropping new connection")
			var dropped: StreamPeerTCP = tcp_server.take_connection()
			dropped.disconnect_from_host()
			continue
		var conn: StreamPeerTCP = tcp_server.take_connection()
		var id: int = conn.get_instance_id()
		clients[id] = {
			"peer": conn,
			"player_name": "",
			"hello": false,
			"buffer": "",
		}
		print("[TCP] New connection id=%d, total=%d" % [id, clients.size()])


func _poll_clients() -> void:
	var to_remove: Array = []
	for id in clients.keys():
		var entry: Dictionary = clients[id]
		var peer: StreamPeerTCP = entry["peer"]
		var status: int = peer.get_status()
		match status:
			StreamPeerTCP.STATUS_NONE, StreamPeerTCP.STATUS_ERROR:
				to_remove.append(id)
				continue
		# Probe for a closed peer: a 0-byte write succeeds on a healthy socket
		# but may fail (returns non-OK) once the remote end has closed. If the
		# peer is in any state other than CONNECTED at this point, disconnect.
		var write_probe: PackedByteArray = PackedByteArray()
		if peer.put_data(write_probe) != OK:
			to_remove.append(id)
			continue
		if peer.get_status() != StreamPeerTCP.STATUS_CONNECTED:
			to_remove.append(id)
			continue
		# Read available bytes; split into complete newline-terminated messages.
		var available: int = peer.get_available_bytes()
		if available > 0:
			var bytes: PackedByteArray = peer.get_data(available)[1]
			if bytes.size() > 0:
				var chunk: String = bytes.get_string_from_utf8()
				entry["buffer"] += chunk
				# Process all complete messages in buffer.
				var nl_pos: int = -1
				while true:
					nl_pos = entry["buffer"].find("\n")
					if nl_pos < 0:
						break
					var line: String = entry["buffer"].substr(0, nl_pos).strip_edges()
					entry["buffer"] = entry["buffer"].substr(nl_pos + 1)
					if line != "":
						router.handle(id, line)
		else:
			# No data buffered. Probe with get_data(1) to detect remote FIN.
			# Godot 4's StreamPeerTCP does NOT transition to STATUS_NONE on FIN —
			# get_status() keeps returning CONNECTED forever — so the only reliable
			# signal is an actual read attempt. After FIN, the first read returns
			# ERR_FILE_EOF and the peer stays marked EOF for subsequent calls.
			# If we read a real byte (rare race: data arrived between the
			# get_available_bytes() check above and this probe), we must save it
			# back to the buffer, otherwise partial messages get truncated.
			var probe: Array = peer.get_data(1)
			if probe[0] != OK:
				to_remove.append(id)
				continue
			if probe[1].size() > 0:
				entry["buffer"] += probe[1].get_string_from_utf8()
	for id in to_remove:
		force_disconnect(id)


## Force-disconnect a client (also called from the router on BYE).
## Persists the player's state to disk first so a reconnect picks up where
## they left off — even if the disconnect was ungraceful (TCP EOF).
func force_disconnect(client_id) -> void:
	if not clients.has(client_id):
		return
	var entry: Dictionary = clients[client_id]
	var name: String = entry.get("player_name", "")
	if name != "" and is_instance_valid(world):
		if world.has_method("save_player"):
			world.save_player(name)
		if world.has_method("remove_player"):
			world.remove_player(name)
	var peer: StreamPeerTCP = entry["peer"]
	peer.disconnect_from_host()
	clients.erase(client_id)
	print("[TCP] Disconnected id=%d name=%s, total=%d" % [client_id, name, clients.size()])
	_broadcast_state()


# --- Public send helpers -----------------------------------------------------

func send(client_id, payload: String) -> void:
	if not clients.has(client_id):
		return
	var entry: Dictionary = clients[client_id]
	var peer: StreamPeerTCP = entry["peer"]
	if peer.get_status() != StreamPeerTCP.STATUS_CONNECTED:
		return
	var data: PackedByteArray = (payload + "\n").to_utf8_buffer()
	peer.put_data(data)


func broadcast(payload: String) -> void:
	for id in clients.keys():
		send(id, payload)


func _broadcast_state() -> void:
	if not is_instance_valid(world):
		return
	broadcast(preload("res://net/protocol.gd").make_state(world.get_players_snapshot()))
