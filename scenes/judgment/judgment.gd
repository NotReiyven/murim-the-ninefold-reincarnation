extends Control

func _ready() -> void:
	$BottomBar/NextButton.pressed.connect(_on_next)

func _on_next() -> void:
	Router.goto_scene("res://scenes/map/map.tscn")
