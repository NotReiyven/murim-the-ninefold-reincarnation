class_name RunState
extends RefCounted

var seed_val: int = 0
var deck: Array[String] = []
var max_hp: int = 80
var hp: int = 80
var gold: int = 100
var flags: Array[String] = []
var ledger: Dictionary[String, int] = {}
var current_node_id: int = 0
var map_cleared: bool = false
var settled: bool = false

func add_soul_fragments(source: String, amount: int) -> void:
	if not ledger.has(source):
		ledger[source] = amount
