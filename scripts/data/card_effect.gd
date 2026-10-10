class_name CardEffect
extends Resource

enum Kind { DAMAGE, DAMAGE_FROM_BLOCK, DRAIN, BLOCK, DOUBLE_BLOCK, HEAL, ENERGY, ENERGY_NEXT_TURN, DRAW, DISCARD_HAND_DRAW_PLUS, APPLY_STATUS, LOSE_HP, ADD_STATUS_CARD }
enum Target { ACTOR, OPPONENT }
enum Condition { NONE, PREV_CARD_ATTACK, ACTOR_HAS_BLOCK, OPPONENT_HAS_STATUS }

@export var kind: Kind = Kind.DAMAGE
@export var amount: int = 0
@export var amount_b: int = 0
@export var hits: int = 1
@export var status_id: String = ""
@export var who: Target = Target.OPPONENT
@export var condition: Condition = Condition.NONE
@export var condition_arg: String = ""
