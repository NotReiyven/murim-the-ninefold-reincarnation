import os

files = {
    'scripts/logic/judgment/judgment_session.gd': '''class_name JudgmentSession
extends RefCounted

enum State { INTRO, ASKING, AWAITING_CONFIRM, VERDICT, DONE }

var state: State = State.INTRO
var current_step: int = 0
var max_steps: int = 5
var karma: int = 0
var tags: Dictionary = {}
var choices_made: Array[String] = []

func get_band() -> Dictionary:
	var band: Dictionary = {}
	for b in GameConfig.KARMA_BANDS.values():
		if karma >= b["min"] and karma <= b["max"]:
			return b
	return GameConfig.KARMA_BANDS["NEUTRAL"]

func transition(new_state: State) -> void:
	state = new_state

func commit_choice(choice: ChoiceData) -> void:
	if state != State.AWAITING_CONFIRM: return
	karma += choice.karma_delta
	for t in choice.tags:
		tags[t] = tags.get(t, 0) + 1
	choices_made.append(choice.id)
	current_step += 1
	if current_step >= max_steps:
		transition(State.VERDICT)
	else:
		transition(State.ASKING)
''',

    'scripts/logic/traits/trait_selection.gd': '''class_name TraitSelection
extends RefCounted

var points: int = 0
var selected_traits: Array[String] = []

func toggle_trait(t: TraitData) -> bool:
	if selected_traits.has(t.id):
		selected_traits.erase(t.id)
		points -= t.points
		return false
	else:
		selected_traits.append(t.id)
		points += t.points
		return true
''',

    'scripts/logic/run/run_state.gd': '''class_name RunState
extends RefCounted

var seed_val: int = 0
var deck: Array[String] = []
var max_hp: int = 80
var hp: int = 80
var gold: int = 100
var flags: Array[String] = []
var ledger: Dictionary = {}
var current_node_id: int = 0
var map_cleared: bool = false
var settled: bool = false

func add_soul_fragments(source: String, amount: int) -> void:
	if not ledger.has(source):
		ledger[source] = amount
''',

    'scripts/logic/combat/combat_state.gd': '''class_name CombatState
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
	enemy_hp = e.max_hp
	enemy_max_hp = e.max_hp

func end_turn() -> void:
	if is_over: return
	turn += 1
	enemy_hp -= 10
	if enemy_hp <= 0:
		is_over = true
		run_state.hp = player_hp
		run_state.add_soul_fragments("combat_" + enemy.id, 5)
''',

    'scenes/hub/hub.tscn': '''[gd_scene load_steps=2 format=3 uid="uid://hubscene"]
[ext_resource type="Script" path="res://scenes/hub/hub.gd" id="1_hub"]

[node name="Hub" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_hub")

[node name="StartButton" type="Button" parent="."]
layout_mode = 0
offset_left = 340.0
offset_top = 1500.0
offset_right = 740.0
offset_bottom = 1644.0
text = "Begin Next Life"
''',

    'scenes/hub/hub.gd': '''extends Control

func _ready() -> void:
	$StartButton.pressed.connect(_on_start)
	
func _on_start() -> void:
	Router.goto_scene("res://scenes/judgment/judgment.tscn")
''',

    'scenes/judgment/judgment.tscn': '''[gd_scene load_steps=2 format=3 uid="uid://judgementscene"]
[ext_resource type="Script" path="res://scenes/judgment/judgment.gd" id="1_judg"]

[node name="Judgment" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
script = ExtResource("1_judg")

[node name="NextButton" type="Button" parent="."]
layout_mode = 0
offset_left = 340.0
offset_top = 1500.0
offset_right = 740.0
offset_bottom = 1644.0
text = "Skip Judgment"
''',

    'scenes/judgment/judgment.gd': '''extends Control

func _ready() -> void:
	$NextButton.pressed.connect(_on_next)

func _on_next() -> void:
	Router.goto_scene("res://scenes/map/map.tscn")
''',

    'scenes/map/map.tscn': '''[gd_scene load_steps=2 format=3 uid="uid://mapscene"]
[ext_resource type="Script" path="res://scenes/map/map.gd" id="1_map"]

[node name="Map" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
script = ExtResource("1_map")

[node name="CombatButton" type="Button" parent="."]
layout_mode = 0
offset_left = 340.0
offset_top = 1500.0
offset_right = 740.0
offset_bottom = 1644.0
text = "Enter Combat"
''',

    'scenes/map/map.gd': '''extends Control

func _ready() -> void:
	$CombatButton.pressed.connect(_on_combat)

func _on_combat() -> void:
	Router.goto_scene("res://scenes/combat/combat.tscn")
''',

    'scenes/combat/combat.tscn': '''[gd_scene load_steps=2 format=3 uid="uid://combatscene"]
[ext_resource type="Script" path="res://scenes/combat/combat.gd" id="1_combat"]

[node name="Combat" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
script = ExtResource("1_combat")

[node name="EndCombatButton" type="Button" parent="."]
layout_mode = 0
offset_left = 340.0
offset_top = 1500.0
offset_right = 740.0
offset_bottom = 1644.0
text = "Win Combat"
''',

    'scenes/combat/combat.gd': '''extends Control

func _ready() -> void:
	$EndCombatButton.pressed.connect(_on_win)

func _on_win() -> void:
	Router.goto_scene("res://scenes/death/death.tscn")
''',

    'scenes/death/death.tscn': '''[gd_scene load_steps=2 format=3 uid="uid://deathscene"]
[ext_resource type="Script" path="res://scenes/death/death.gd" id="1_death"]

[node name="Death" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
script = ExtResource("1_death")

[node name="HubButton" type="Button" parent="."]
layout_mode = 0
offset_left = 340.0
offset_top = 1500.0
offset_right = 740.0
offset_bottom = 1644.0
text = "Return to Hub"
''',

    'scenes/death/death.gd': '''extends Control

func _ready() -> void:
	$HubButton.pressed.connect(_on_hub)

func _on_hub() -> void:
	Profile.soul_fragments += 5
	ProfileCodec.save_profile()
	Router.goto_scene("res://scenes/hub/hub.tscn")
'''
}

for path, content in files.items():
    with open(path, 'w') as f:
        f.write(content)
