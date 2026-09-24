extends Node
##
## Thin WebSocket server wrapper.
##
## Uses TCPServer to accept raw connections, then upgrades each one to a
## WebSocketPeer via accept_stream(). Tracks clients in a Dictionary keyed by
## the StreamPeer instance id (which is stable across the connection's lifetime).
##
## Public API:
##   start(port)        — bind & listen
##   send(id, payload)  — push JSON string to one client
##   broadcast(payload) — push to every connected client
##   clients            — read-only view: id -> { peer, player_name, hello }
##

const MAX_CLIENTS: int = 16

var port: int = 8080
var tcp_server: TCPServer = TCPServer.new()
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
		print("[WS] Listening on ws://0.0.0.0:%d" % port)
	return err


func _process(_delta: float) -> void:
	_accept_pending_connections()
	_poll_clients()


func _accept_pending_connections() -> void:
	if not tcp_server.is_connection_available():
		return
	while tcp_server.is_connection_available():
		if clients.size() >= MAX_CLIENTS:
			push_warning("[WS] Max clients reached, dropping new connection")
			var dropped: StreamPeerTCP = tcp_server.take_connection()
			dropped.disconnect_from_peer()
			continue
		var conn: StreamPeerTCP = tcp_server.take_connection()
		var ws: WebSocketPeer = WebSocketPeer.new()
		var err: int = ws.accept_stream(conn)
		if err != OK:
			push_warning("[WS] Failed to upgrade connection to WS (err=%d)" % err)
			conn.disconnect_from_peer()
			continue
		var id: int = conn.get_instance_id()
		clients[id] = {
			"peer": ws,
			"conn": conn,
			"player_name": "",
			"hello": false,
		}
		print("[WS] New connection id=%d, total=%d" % [id, clients.size()])


func _poll_clients() -> void:
	var to_remove: Array = []
	for id in clients.keys():
		var entry: Dictionary = clients[id]
		var peer: WebSocketPeer = entry["peer"]
		peer.poll()
		var state: int = peer.get_ready_state()
		if state == WebSocketPeer.STATE_OPEN:
			while peer.get_available_packet_count() > 0:
				var pkt: PackedByteArray = peer.get_packet()
				var text: String = pkt.get_string_from_utf8()
				_dispatch(id, text)
		elif state == WebSocketPeer.STATE_CLOSED:
			to_remove.append(id)
	for id in to_remove:
		_disconnect(id)


func _dispatch(client_id: int, text: String) -> void:
	router.handle(client_id, text)


func _disconnect(client_id: int) -> void:
	if not clients.has(client_id):
		return
	var entry: Dictionary = clients[client_id]
	var name: String = entry.get("player_name", "")
	if name != "" and is_instance_valid(world) and world.has_method("remove_player"):
		world.remove_player(name)
	var peer: WebSocketPeer = entry["peer"]
	peer.close()
	clients.erase(client_id)
	print("[WS] Disconnected id=%d name=%s, total=%d" % [client_id, name, clients.size()])
	# Broadcast updated state so other clients see this player gone.
	_broadcast_state()


# --- Public send helpers -----------------------------------------------------

func send(client_id: int, payload: String) -> void:
	if not clients.has(client_id):
		return
	var entry: Dictionary = clients[client_id]
	var peer: WebSocketPeer = entry["peer"]
	if peer.get_ready_state() != WebSocketPeer.STATE_OPEN:
		return
	peer.put_packet(payload.to_utf8_buffer())


func broadcast(payload: String) -> void:
	for id in clients.keys():
		send(id, payload)


func _broadcast_state() -> void:
	if not is_instance_valid(world):
		return
	broadcast(preload("res://net/protocol.gd").make_state(world.get_players_snapshot()))
