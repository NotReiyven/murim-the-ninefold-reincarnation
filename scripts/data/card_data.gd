class_name CardData
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
enum Targeting { SELF, ENEMY }
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
