class_name EnemyData
extends Resource

enum Tier { STANDARD, ELITE, BOSS }

@export var id: String
@export var display_name: String
@export var tier: Tier
@export var faction: String
@export var max_hp: int
@export var portrait_id: String
@export var phases: Array[EnemyPhase] = []
@export var gold_min: int
@export var gold_max: int
