class_name ScenarioData
extends Resource

@export var id: String
@export var cluster: String
@export var prompt: String
@export var speaker: String = ""
@export var can_be_root: bool = true
@export var tag_affinity: Dictionary[String, float] = {}
@export var requires_flag: String = ""
@export var choices: Array[ChoiceData] = []
