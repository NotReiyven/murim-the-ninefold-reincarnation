extends Control

func _ready() -> void:
	$BottomBar/CombatButton.pressed.connect(_on_combat)

func _on_combat() -> void:
	Router.goto_scene("res://scenes/combat/combat.tscn")
