extends Node

var current_scene_path: String = ""

func goto_scene(path: String) -> void:
	get_tree().change_scene_to_file(path)
	current_scene_path = path
