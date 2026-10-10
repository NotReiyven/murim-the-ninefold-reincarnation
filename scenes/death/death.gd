extends Control

const FRAGMENTS_EARNED: int = 5

func _ready() -> void:
	Profile.soul_fragments += FRAGMENTS_EARNED
	$TopArea/Fragments.text = "Soul Fragments earned: %d (Total: %d)" % [FRAGMENTS_EARNED, Profile.soul_fragments]
	ProfileCodec.save_profile()
	$BottomBar/HubButton.pressed.connect(_on_hub)

func _on_hub() -> void:
	Router.goto_scene("res://scenes/hub/hub.tscn")
