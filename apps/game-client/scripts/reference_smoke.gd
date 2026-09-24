extends SceneTree

const Art = preload("res://scripts/reference_art.gd")

func _initialize() -> void:
	var art = Art.new()
	for map_id in ["severa", "forest", "beach", "ranch", "arena"]:
		assert(art.room_texture(map_id) != null, "Missing room: " + map_id)
	assert(art.room_texture("unknown") == null)
	for species in art.SPECIES:
		assert(art.pet_texture(species, 0) != null, "Missing creature: " + species)
	assert(art.pet_texture("unmapped_species", 0) == null)
	assert(art.actor_texture("Boy", "idle", 0) != null)
	var step: float = art.actors.Boy.run.duration / art.actors.Boy.run.frames.size()
	assert(art.actor_texture("Boy", "run", 0) != art.actor_texture("Boy", "run", step * 1.1))
	assert(art.actor_texture("unknown", "idle", 0) == null)
	print("PASS: five extracted rooms, linked actor frames, species mapping, unknown-asset handling")
	quit(0)
