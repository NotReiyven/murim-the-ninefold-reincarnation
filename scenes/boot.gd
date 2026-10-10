extends Node

func _ready() -> void:
	# Boot validates Content, loads Profile, then routes to the hub or the resume prompt.
	ProfileCodec.load_profile()
	Router.call_deferred("goto_scene", "res://scenes/hub/hub.tscn")
