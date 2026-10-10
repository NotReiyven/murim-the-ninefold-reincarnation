extends Node

# Loads and validates every .tres at boot; lookups by id.
# Does not mutate resources.
# NOTE: Plain Dictionary is used here because autoloads are parsed before
# class_name scripts (CardData, TraitData, etc.) are registered.
# Typed dicts with custom classes are safe elsewhere in the project.

var cards: Dictionary = {}
var traits: Dictionary = {}
var enemies: Dictionary = {}
var scenarios: Dictionary = {}
var events: Dictionary = {}
var unlocks: Dictionary = {}

func _ready() -> void:
	pass
