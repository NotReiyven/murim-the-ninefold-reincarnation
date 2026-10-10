class_name EventOutcome
extends Resource

enum Kind { GAIN_GOLD, LOSE_GOLD, HEAL, LOSE_HP, MAX_HP_ADD, ADD_CARD, REMOVE_CARD_PICK, UPGRADE_CARD_PICK, ADD_STATUS_CARD_TO_DECK, SET_RUN_FLAG, START_COMBAT }

@export var kind: Kind
@export var amount: int
@export var arg: String
