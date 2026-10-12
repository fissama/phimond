extends SceneTree
## Audit the current 960×640 scene composition after anchor/container layout.
const VIEWPORT_SIZE := Vector2(960, 640)
const WINDOWS := [
	["LoginScreen", Vector2(234.5, 188), Vector2(491, 264)],
	["NpcMenu", Vector2(96, 80), Vector2(768, 480)],
	["ShopMenu", Vector2(96, 56), Vector2(768, 528)],
]
var failures := 0

func _initialize() -> void:
	root.content_scale_size = Vector2i(960, 640)
	root.size = Vector2i(960, 640)
	call_deferred("_run")

func _run() -> void:
	var host := Control.new()
	host.size = VIEWPORT_SIZE
	root.add_child(host)
	for entry in WINDOWS:
		var scene: Control = load("res://scenes/%s.tscn" % entry[0]).instantiate()
		host.add_child(scene)
		await process_frame
		await process_frame
		_check_rect(scene, Rect2(Vector2.ZERO, VIEWPORT_SIZE), entry[0])
		var window := scene.get_node_or_null("Window") as Control
		_check_rect(window, Rect2(entry[1], entry[2]), "%s/Window" % entry[0])
		if window != null and entry[0] == "LoginScreen":
			for name in ["UserInput", "PassInput", "LoginBtn", "RegisterBtn", "Status"]:
				_check_inside(window.get_node_or_null(name) as Control, "Login/%s" % name)
		scene.free()
	var battle: Control = load("res://scenes/BattleScene.tscn").instantiate()
	host.add_child(battle)
	await process_frame
	await process_frame
	_check_rect(battle, Rect2(Vector2.ZERO, VIEWPORT_SIZE), "BattleScene")
	var hud: Control = battle.get("hud")
	_check_rect(hud, Rect2(Vector2.ZERO, VIEWPORT_SIZE), "Battle/HUD")
	if hud != null:
		_check_rect(hud.get("world"), Rect2(0, 0, 960, 454), "Battle/world")
		for field in ["log_text", "status", "detail", "battle_bar", "menu", "auto_button"]:
			_check_inside(hud.get(field), "Battle/%s" % field)
		var buttons: Array = hud.get("battle_buttons")
		_check(buttons.size() == 6, "Battle must expose six action buttons")
		for button in buttons:
			_check_inside(button, "Battle/action button")
	battle.free()
	host.free()
	if failures == 0:
		print("PASS: layout_audit current login/NPC/shop/battle geometry and viewport bounds")
	else:
		print("FAIL: layout_audit %d failed checks" % failures)
	quit(0 if failures == 0 else 1)

func _check_rect(control: Control, expected: Rect2, label: String) -> void:
	if control == null:
		_check(false, "%s missing" % label)
		return
	var actual := control.get_global_rect()
	_check(actual.position.distance_to(expected.position) < 0.5 and actual.size.distance_to(expected.size) < 0.5,
		"%s rect %s expected %s" % [label, actual, expected])
	_check_inside(control, label)

func _check_inside(control: Control, label: String) -> void:
	if control == null:
		_check(false, "%s missing" % label)
		return
	var rect := control.get_global_rect()
	_check(rect.size.x > 0 and rect.size.y > 0 and Rect2(Vector2.ZERO, VIEWPORT_SIZE).encloses(rect),
		"%s outside viewport or empty: %s" % [label, rect])

func _check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		print("FAIL: %s" % message)
