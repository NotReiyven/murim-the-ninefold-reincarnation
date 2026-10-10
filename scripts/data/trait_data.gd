class_name TraitData
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
