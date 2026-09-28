extends SceneTree

func _initialize() -> void:
    var manifest = JSON.parse_string(FileAccess.get_file_as_string("res://assets/pets/apk84/manifest.json"))
    assert(manifest.species.size() == 152)
    var clip_count = 0
    var key_count = 0
    for id in manifest.species:
        var prefix = "res://assets/pets/apk84/" + id
        var portrait = load(prefix + "/portrait.png") as Texture2D
        assert(portrait != null and portrait.get_width() > 0, id)
        var frames = load(prefix + "/frames.tres") as SpriteFrames
        assert(frames != null, id)
        assert(frames.get_animation_names().size() == 5, id)
        for animation in manifest.species[id].clips:
            var expected = manifest.species[id].clips[animation]
            assert(frames.has_animation(animation), id)
            assert(frames.get_animation_loop(animation) == expected.loop, id)
            assert(is_equal_approx(frames.get_animation_speed(animation), 1.0), id)
            assert(frames.get_frame_count(animation) == expected.frames.size(), id)
            var total = 0.0
            for index in expected.frames.size():
                var texture = frames.get_frame_texture(animation, index)
                assert(texture != null and texture.get_width() > 0, id)
                var duration = frames.get_frame_duration(animation, index)
                assert(abs(duration - expected.frames[index].duration_seconds) < 0.000001, id)
                total += duration
                key_count += 1
            assert(abs(total - expected.duration_seconds) < 0.00001, id)
            clip_count += 1
    assert(clip_count == 760 and key_count == 1241)
    print("PASS: APK84 152 portraits + 152 SpriteFrames; 760 clips; 1241 timed frames; all resources and durations valid")
    quit()
