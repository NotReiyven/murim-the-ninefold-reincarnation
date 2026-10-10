class_name TraitSelection
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
