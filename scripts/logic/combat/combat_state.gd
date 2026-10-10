class_name CombatState
extends RefCounted

var run_state: RunState
var enemy: EnemyData
var player_hp: int
var player_max_hp: int
var enemy_hp: int
var enemy_max_hp: int
var turn: int = 1
var is_over: bool = false

func _init(rs: RunState, e: EnemyData):
	run_state = rs
	enemy = e
	player_hp = rs.hp
	player_max_hp = rs.max_hp
	if e:
		enemy_hp = e.max_hp
		enemy_max_hp = e.max_hp

func end_turn() -> void:
	if is_over: return
	turn += 1
	enemy_hp -= 10
	if enemy_hp <= 0:
		is_over = true
		run_state.hp = player_hp
		if enemy:
			run_state.add_soul_fragments("combat_" + enemy.id, 5)
