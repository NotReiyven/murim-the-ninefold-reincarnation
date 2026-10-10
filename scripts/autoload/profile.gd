extends Node

var soul_fragments: int = 0
var lifetime_soul_fragments: int = 0
var purchased_unlocks: Array[String] = []
var unlocked_flags: Array[String] = []
var stats: Dictionary[String, int] = {}
var last_run_summary: Dictionary = {}
var settings: Dictionary[String, Variant] = {}
var seen_hints: Array[String] = []

func has_flag(flag: String) -> bool:
	return unlocked_flags.has(flag)

func purchase_unlock(_id: String) -> Error:
	return OK
