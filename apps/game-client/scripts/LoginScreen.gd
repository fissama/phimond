extends Control
## Adapted account entry using APK chrome; authentication is not shown in video.
@onready var _user: LineEdit = $Window/UserInput
@onready var _pass: LineEdit = $Window/PassInput
@onready var _register_btn: BaseButton = $Window/RegisterBtn
@onready var _login_btn: BaseButton = $Window/LoginBtn
@onready var _status: Label = $Window/Status

func _ready() -> void:
	_register_btn.pressed.connect(_on_RegisterBtn_pressed)
	_login_btn.pressed.connect(_on_LoginBtn_pressed)
	for button in [_register_btn, _login_btn]:
		button.focus_entered.connect(func(): button.self_modulate = Color(1.25, 1.25, 1.1))
		button.focus_exited.connect(func(): button.self_modulate = Color.WHITE)
		button.mouse_entered.connect(func(): button.self_modulate = Color(1.25, 1.25, 1.1))
		button.mouse_exited.connect(func(): button.self_modulate = Color.WHITE)
	_user.text_submitted.connect(func(_text: String): _pass.grab_focus())
	_pass.text_submitted.connect(func(_text: String): _on_LoginBtn_pressed())
	_user.grab_focus()
	_status.text = "Enter your account to continue."

func _on_RegisterBtn_pressed() -> void:
	if _user == null or _pass == null or _status == null: return
	var u := _user.text.strip_edges()
	var p := _pass.text
	if u.is_empty() or p.is_empty():
		_status.text = "username + password required"
		return
	_status.text = "registering…"
	PhimondClient.http_register(u, p, _on_auth_done)


func _on_LoginBtn_pressed() -> void:
	if _user == null or _pass == null or _status == null: return
	var u := _user.text.strip_edges()
	var p := _pass.text
	if u.is_empty() or p.is_empty():
		_status.text = "username + password required"
		return
	_status.text = "logging in…"
	PhimondClient.http_login(u, p, _on_auth_done)


func _on_auth_done(ok: bool, msg: String) -> void:
	if not is_instance_valid(_status): return
	if not ok:
		_status.text = "auth failed: " + msg
		return
	_status.text = "auth ok, fetching catalog…"
	PhimondClient.fetch_content(func(_c): _on_catalog_ready())


func _on_catalog_ready() -> void:
	if is_instance_valid(_status):
		_status.text = "connecting websocket…"
	PhimondClient.connect_ws()
	get_tree().change_scene_to_file("res://scenes/MainMap.tscn")
