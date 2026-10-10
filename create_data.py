import os

files = {
    'scripts/data/card_effect.gd': '''class_name CardEffect
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
''',

    'scripts/data/card_data.gd': '''class_name CardData
extends Resource

enum Style { SWORD, FIST, BODY, MOVEMENT, INTERNAL, FORBIDDEN }
enum Faction { STARTER, NEUTRAL, ORTHODOX, DEMONIC }
enum CardType { ATTACK, TECHNIQUE, STANCE, STATUS }
enum Rarity { STARTER, COMMON, UNCOMMON, RARE }

@export var id: String
@export var display_name: String
@export var style: Style
@export var faction: Faction
@export var card_type: CardType
@export var rarity: Rarity
@export var energy_cost: int
@export var blood_price: int = 0
@export enum Targeting { SELF, ENEMY }
@export var targeting: Targeting = Targeting.ENEMY
@export var tags: Array[String] = []
@export var retain: bool = false
@export var exhaust: bool = false
@export var unplayable: bool = false
@export var effects: Array[CardEffect] = []
@export var upgrade_effects: Array[CardEffect] = []
@export var upgrade_energy_cost: int = -2
@export var upgrade_blood_price: int = -2
@export var unlock_flag: String = ""
@export var job: String = ""
@export var flavor: String = ""
@export var icon_id: String = ""
''',

    'scripts/data/trait_effect.gd': '''class_name TraitEffect
extends Resource

enum Kind { STAT_MOD, CARD_ADD, COMBAT_START }

@export var kind: Kind
@export var amount: int
@export var arg: String
''',

    'scripts/data/trait_data.gd': '''class_name TraitData
extends Resource

enum Category { CONSTITUTION, INTERNAL_ENERGY, MARTIAL_APTITUDE, FORTUNE, FORBIDDEN_ARTS, PAST_LIVES }

@export var id: String
@export var display_name: String
@export var description: String
@export var category: Category
@export var points: int
@export var requires_profile_flags: Array[String] = []
@export var requires_judgment_flags: Array[String] = []
@export var requires_alignment: String = ""
@export var excludes: Array[String] = []
@export var effects: Array[TraitEffect] = []
@export var icon_id: String = ""
''',

    'scripts/data/intent_data.gd': '''class_name IntentData
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
''',

    'scripts/data/enemy_phase.gd': '''class_name EnemyPhase
extends Resource

@export var enter_at_hp_pct: int = 100
@export var entry_effects: Array[CardEffect] = []
@export var intents: Array[IntentData] = []
@export var sequence: Array[StringName] = []
''',

    'scripts/data/enemy_data.gd': '''class_name EnemyData
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
''',

    'scripts/data/choice_data.gd': '''class_name ChoiceData
extends Resource

@export var id: String
@export var label: String
@export var follow_up: String = ""
@export var karma_delta: int = 0
@export var tags: Array[String] = []
@export var grants_flags: Array[String] = []
@export var requires_flag: String = ""
''',

    'scripts/data/scenario_data.gd': '''class_name ScenarioData
extends Resource

@export var id: String
@export var cluster: String
@export var prompt: String
@export var speaker: String = ""
@export var can_be_root: bool = true
@export var tag_affinity: Dictionary = {}
@export var requires_flag: String = ""
@export var choices: Array[ChoiceData] = []
''',

    'scripts/data/event_data.gd': '''class_name EventOutcome
extends Resource

enum Kind { GAIN_GOLD, LOSE_GOLD, HEAL, LOSE_HP, MAX_HP_ADD, ADD_CARD, REMOVE_CARD_PICK, UPGRADE_CARD_PICK, ADD_STATUS_CARD_TO_DECK, SET_RUN_FLAG, START_COMBAT }

@export var kind: Kind
@export var amount: int
@export var arg: String
''',

    'scripts/data/event_choice.gd': '''class_name EventChoice
extends Resource

@export var label: String
@export var requirements: Dictionary = {}
@export var outcomes: Array[EventOutcome] = []
''',

    'scripts/data/event_def_data.gd': '''class_name EventData
extends Resource

@export var id: String
@export var title: String
@export var body: String
@export var requires_flag: String = ""
@export var choices: Array[EventChoice] = []
''',

    'scripts/data/unlock_data.gd': '''class_name UnlockData
extends Resource

@export var id: String
@export var display_name: String
@export var cost: int
@export var description: String
@export var grants_flags: Array[String] = []
@export var requires_unlocks: Array[String] = []
'''
}

for path, content in files.items():
    with open(path, 'w') as f:
        f.write(content)
