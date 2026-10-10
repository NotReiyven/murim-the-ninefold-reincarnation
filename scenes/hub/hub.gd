extends Control

func _ready() -> void:
	$TopArea/SoulFragments.text = "Soul Fragments: %d" % Profile.soul_fragments
	$BottomBar/StartButton.pressed.connect(_on_start)

func _on_start() -> void:
	Router.goto_scene("res://scenes/judgment/judgment.tscn")
