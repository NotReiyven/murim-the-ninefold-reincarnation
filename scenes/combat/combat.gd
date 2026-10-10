extends Control

func _ready() -> void:
	$BottomBar/EndTurnButton.pressed.connect(_on_win)

func _on_win() -> void:
	Router.goto_scene("res://scenes/death/death.tscn")
