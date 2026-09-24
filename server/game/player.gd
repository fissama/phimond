extends Node
##
## Player value-object (data only, no scene). Currently inlined into World as
## a Dictionary — this class is here for future expansion (party, inventory,
## stats) so we can swap it in without rewriting consumers.
##

class_name Player

var name: String
var x: int
var y: int
var dir: String = "down"

# Phase 5+
var party: Array = []          # Array[Monster]
var inventory: Dictionary = {} # item_id -> qty
var xp: int = 0
var gold: int = 0


func _init(p_name: String, p_x: int = 10, p_y: int = 7, p_dir: String = "down") -> void:
	name = p_name
	x = p_x
	y = p_y
	dir = p_dir


func to_snapshot() -> Dictionary:
	return {
		"name": name,
		"x":    x,
		"y":    y,
		"dir":  dir,
	}
