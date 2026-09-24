## Render the existing actor designs, never generate or replace artwork.
extends SceneTree
const Art = preload("res://scripts/reference_art.gd")

func _initialize() -> void: call_deferred("run")

func run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() != 1: push_error("Expected output directory"); quit(1); return
	var art = Art.new()
	art.prepare()
	DirAccess.make_dir_recursive_absolute(args[0])
	var surface := SubViewport.new()
	surface.size = Vector2i(960,640)
	surface.render_target_update_mode = SubViewport.UPDATE_ALWAYS
	root.add_child(surface)
	var names: Array = ["Boy"]
	names.append_array(Art.SPECIES.values())
	for name in names:
		surface.size = Vector2i(960,60 + art.actors.get(name, {}).size() * 130)
		var sheet := Control.new()
		sheet.size = Vector2(surface.size)
		surface.add_child(sheet)
		var bg := ColorRect.new()
		bg.color = Color("112536"); bg.size = sheet.size; sheet.add_child(bg)
		var heading := Label.new()
		heading.text = str(name) + " · source designs · frame 0 / mid-frame / mirrored"
		heading.position = Vector2(20,10); sheet.add_child(heading)
		var row := 0
		for action in art.actors.get(name, {}):
			var label := Label.new(); label.text = str(action); label.position = Vector2(20,50+row*130); sheet.add_child(label)
			var duration := float(art.actors[name][action].get("duration",1.0))
			if action == "run": duration = minf(duration,0.65)
			for column in range(3):
				var pic := TextureRect.new()
				pic.texture = art.actor_texture(str(name), str(action), duration*0.5 if column==1 else 0)
				if pic.texture == null: push_error("Missing actor texture"); quit(1); return
				pic.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
				pic.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
				pic.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
				pic.size = Vector2(180,105); pic.position = Vector2(170+column*250,50+row*130)
				pic.flip_h = column==2; sheet.add_child(pic)
			row += 1
		await process_frame
		await RenderingServer.frame_post_draw
		if surface.get_texture().get_image().save_png(args[0].path_join(str(name)+".png")) != OK:
			push_error("Cannot save actor baseline");quit(1);return
		sheet.free()
	print("PASS: actor design baseline for trainer and ten mapped species; original frames, no art edits")
	surface.queue_free()
	quit()
