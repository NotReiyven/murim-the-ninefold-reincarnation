class_name IntentData
extends Resource

enum Kind { ATTACK, DEFEND, BUFF, DEBUFF, SPECIAL }

@export var id: String
@export var kind: Kind
@export var display_name: String
@export var tell: String
@export var damage: int
@export var hits: int = 1
@export var block: int
@export var effects: Array[CardEffect] = []
@export var weight: int = 10
@export var max_consecutive: int = 2
@export var requires_stance: String = ""
@export var sets_stance: String = ""
