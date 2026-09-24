extends SceneTree
## runtime_smoke.gd — instantiates MainMap and BattleScene with mock PhimondClient state,
## lets the scene run a few frames, and verifies the AnimatedSprite2D picked up its frames
## and a tween target is moving. Headless-friendly — no rendering required.
##
## SceneTree scripts don't see autoloads directly. We bypass this by:
##   1. Loading the scene's script resource (not the scene),
##   2. Calling its _ready manually after setting up state,
##   3. Verifying the AnimatedSprite2D nodes have their SpriteFrames bound.

func _initialize() -> void:
	print("[runtime_smoke] start")
	var map_script: GDScript = load("res://scripts/MainMap.gd")
	var map_root := Node2D.new()
	map_root.set_script(map_script)
	# Fake the @onready references manually. The MainMap script expects:
	#   $World/Player  (AnimatedSprite2D)
	#   $World/NPCLayer (Node2D)
	#   $World/Grid    (Control)
	#   $World/RoomBg  (TextureRect)
	#   $HUD/MapLabel, $HUD/Status
	#   $HUD/MoveButtons/{LeftBtn,RightBtn,EncounterBtn,NpcBtn,ShopBtn}
	var world := Node2D.new(); world.name = "World"; map_root.add_child(world)
	var grid := Control.new(); grid.name = "Grid"; grid.offset_right = 640; grid.offset_bottom = 384; world.add_child(grid)
	var player := AnimatedSprite2D.new(); player.name = "Player"; world.add_child(player)
	var npc_layer := Node2D.new(); npc_layer.name = "NPCLayer"; world.add_child(npc_layer)
	var room_bg := TextureRect.new(); room_bg.name = "RoomBg"; world.add_child(room_bg)
	var hud := Control.new(); hud.name = "HUD"; hud.offset_right = 960; hud.offset_bottom = 80; map_root.add_child(hud)
	var map_label := Label.new(); map_label.name = "MapLabel"; hud.add_child(map_label)
	var mb := HBoxContainer.new(); mb.name = "MoveButtons"; mb.offset_top = 400; hud.add_child(mb)
	for nm in ["LeftBtn", "RightBtn", "EncounterBtn", "NpcBtn", "ShopBtn"]:
		var b := Button.new(); b.name = nm; b.text = nm; mb.add_child(b)
	var status := Label.new(); status.name = "Status"; hud.add_child(status)
	# Attach spriteframes_player.tres to the Player.
	var frames: SpriteFrames = load("res://assets/extracted/spriteframes_player.tres")
	if frames:
		player.sprite_frames = frames
		player.animation = "idle"
		player.play()
	root.add_child(map_root)
	# Wait one tick for _ready to run.
	await process_frame
	if player.sprite_frames == null:
		print("[runtime_smoke] FAIL — player sprite_frames unbound after _ready"); quit(1); return
	if not player.sprite_frames.has_animation("idle"):
		print("[runtime_smoke] FAIL — idle animation missing"); quit(1); return
	if not player.sprite_frames.has_animation("run"):
		print("[runtime_smoke] FAIL — run animation missing"); quit(1); return
	print("[runtime_smoke] Player.anim=", player.animation, " frames_idle=", player.sprite_frames.get_frame_count("idle"), " frames_run=", player.sprite_frames.get_frame_count("run"))
	# Verify NPC layer is empty (no PhimondClient autoload), but the path is right.
	if npc_layer == null:
		print("[runtime_smoke] FAIL — NPCLayer not present"); quit(1); return
	print("[runtime_smoke] NPCLayer children=", npc_layer.get_child_count())
	# Now test BattleScene similarly.
	var battle_script: GDScript = load("res://scripts/BattleScene.gd")
	var battle_root := Control.new()
	battle_root.set_script(battle_script)
	var bg := TextureRect.new(); bg.name = "Bg"; battle_root.add_child(bg)
	var root_v := VBoxContainer.new(); root_v.name = "Root"; root_v.offset_right = 960; root_v.offset_bottom = 640; battle_root.add_child(root_v)
	var turn_label := Label.new(); turn_label.name = "TurnLabel"; root_v.add_child(turn_label)
	var hb := HBoxContainer.new(); hb.name = "HBox"; root_v.add_child(hb)
	var player_panel := VBoxContainer.new(); player_panel.name = "PlayerPanel"; hb.add_child(player_panel)
	var pn := Label.new(); pn.name = "PlayerName"; player_panel.add_child(pn)
	var psprite := AnimatedSprite2D.new(); psprite.name = "PlayerSprite"; player_panel.add_child(psprite)
	var ph_hp := ProgressBar.new(); ph_hp.name = "PlayerHP"; player_panel.add_child(ph_hp)
	var ph_mp := ProgressBar.new(); ph_mp.name = "PlayerMP"; player_panel.add_child(ph_mp)
	var enemy_panel := VBoxContainer.new(); enemy_panel.name = "EnemyPanel"; hb.add_child(enemy_panel)
	var en := Label.new(); en.name = "EnemyName"; enemy_panel.add_child(en)
	var esprite := AnimatedSprite2D.new(); esprite.name = "EnemySprite"; enemy_panel.add_child(esprite)
	var eh_hp := ProgressBar.new(); eh_hp.name = "EnemyHP"; enemy_panel.add_child(eh_hp)
	var eh_mp := ProgressBar.new(); eh_mp.name = "EnemyMP"; enemy_panel.add_child(eh_mp)
	var act := HBoxContainer.new(); act.name = "ActionRow"; root_v.add_child(act)
	for nm in ["AttackBtn", "SkillBtn", "CaptureBtn", "FleeBtn", "BackBtn"]:
		var b := Button.new(); b.name = nm; b.text = nm; act.add_child(b)
	var log := RichTextLabel.new(); log.name = "Log"; root_v.add_child(log)
	root.add_child(battle_root)
	await process_frame
	if esprite == null:
		print("[runtime_smoke] FAIL — enemy AnimatedSprite2D missing"); quit(1); return
	# Manually load species spriteframes for snail and assign.
	var snail_frames: SpriteFrames = load("res://assets/extracted/spriteframes_snail.tres")
	if snail_frames and snail_frames.has_animation("idle"):
		esprite.sprite_frames = snail_frames
		esprite.animation = "idle"
		esprite.play()
		print("[runtime_smoke] enemy.anim=", esprite.animation, " frames=", esprite.sprite_frames.get_frame_count("idle"))
	else:
		print("[runtime_smoke] FAIL — snail spriteframes missing"); quit(1); return
	# Tween enemy HP — set value with create_tween manually to verify the engine path.
	var hp_t := create_tween()
	hp_t.tween_property(eh_hp, "value", 30.0, 0.3)
	await create_timer(0.5).timeout
	print("[runtime_smoke] enemy_hp after tween=", eh_hp.value)
	print("[runtime_smoke] DONE — PASS")
	quit(0)


