extends Node

var state: RunState = null

func start_run(seed_val: int) -> void:
	state = RunState.new()
	state.seed_val = seed_val

func advance_node(node_id: int) -> void:
	if state:
		state.current_node_id = node_id

func apply_combat_result(result: Dictionary) -> void:
	if state and result.has("hp"):
		state.hp = int(result["hp"])

func settle_run() -> void:
	if state and not state.settled:
		state.settled = true
