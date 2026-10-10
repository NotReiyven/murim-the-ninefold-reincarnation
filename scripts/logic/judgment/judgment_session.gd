class_name JudgmentSession
extends RefCounted

enum State { INTRO, ASKING, AWAITING_CONFIRM, VERDICT, DONE }

var state: State = State.INTRO
var current_step: int = 0
var max_steps: int = 5
var karma: int = 0
var tags: Dictionary[String, int] = {}
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
