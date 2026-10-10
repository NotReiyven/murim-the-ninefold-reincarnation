class_name TraitEffect
extends Resource

enum Kind { STAT_MOD, CARD_ADD, COMBAT_START }

@export var kind: Kind
@export var amount: int
@export var arg: String
