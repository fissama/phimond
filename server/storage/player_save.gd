extends Node
##
## Per-player save file: stores the persistent slice of world state so a player
## can rejoin with their monster, inventory, and last position intact.
##
## Save format (JSON, one file per player):
##   {
##     "name":      "alice",
##     "x":         12,
##     "y":         8,
##     "dir":       "down",
##     "monster":   { name, level, xp, hp, max_hp, attack, defense, speed, skills },
##     "inventory": { "potion": 3 }
##   }
##
## Directory: /app/data/players/  — bind-mounted to the host so saves survive
## container restarts (see docker-compose.yml → server.volumes).
##
## Writes are atomic: write to <file>.tmp then rename, so a crash mid-write
## leaves the previous good file intact.

const SAVE_DIR: String = "/app/data/players/"


func _ready() -> void:
    DirAccess.make_dir_recursive_absolute(SAVE_DIR)


func has_save(name: String) -> bool:
    return FileAccess.file_exists(_path(name))


## Returns the saved player dict, or {} if no save exists / file is unreadable
## / contents aren't a JSON object. An empty dict signals "no prior session"
## to the caller so it can fall through to the new-player defaults.
func load_save(name: String) -> Dictionary:
    var path: String = _path(name)
    if not FileAccess.file_exists(path):
        return {}
    var f: FileAccess = FileAccess.open(path, FileAccess.READ)
    if f == null:
        push_warning("[Save] Could not open %s for read" % path)
        return {}
    var text: String = f.get_as_text()
    f.close()
    var parsed: Variant = JSON.parse_string(text)
    if parsed is Dictionary:
        return parsed
    push_warning("[Save] %s did not contain a JSON object" % path)
    return {}


## Atomic write: .tmp then rename.
func save_save(name: String, data: Dictionary) -> void:
    var path: String = _path(name)
    var tmp: String = path + ".tmp"
    var f: FileAccess = FileAccess.open(tmp, FileAccess.WRITE)
    if f == null:
        push_warning("[Save] Could not open %s for write" % tmp)
        return
    f.store_string(JSON.stringify(data))
    f.close()
    var err: int = DirAccess.rename_absolute(tmp, path)
    if err != OK:
        push_warning("[Save] Rename %s -> %s failed (err=%d)" % [tmp, path, err])
    else:
        print("[Save] Wrote %s" % path)


func delete_save(name: String) -> void:
    var path: String = _path(name)
    if FileAccess.file_exists(path):
        DirAccess.remove_absolute(path)
        print("[Save] Deleted %s" % path)


func _path(name: String) -> String:
    return SAVE_DIR + name + ".json"