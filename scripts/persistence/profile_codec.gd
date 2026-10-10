class_name ProfileCodec
extends RefCounted

static func save_profile() -> Error:
	var data: Dictionary = {
		"schema_version": 1,
		"profile": {
			"soul_fragments": Profile.soul_fragments,
			"lifetime_soul_fragments": Profile.lifetime_soul_fragments,
			"purchased_unlocks": Profile.purchased_unlocks,
			"unlocked_flags": Profile.unlocked_flags,
			"stats": Profile.stats,
			"last_run_summary": Profile.last_run_summary,
			"settings": Profile.settings,
			"seen_hints": Profile.seen_hints
		}
	}
	return SaveIO.save_json("profile.json", data)

static func load_profile() -> void:
	var dict: Dictionary = SaveIO.load_json("profile.json")
	if not dict.has("profile"):
		return
	var p: Dictionary = dict["profile"]
	if p.has("soul_fragments"):
		Profile.soul_fragments = clampi(int(p["soul_fragments"]), 0, 1000000)
	if p.has("lifetime_soul_fragments"):
		Profile.lifetime_soul_fragments = clampi(int(p["lifetime_soul_fragments"]), 0, 100000000)
	if p.has("purchased_unlocks"):
		var arr: Array[String] = []
		for u: Variant in p["purchased_unlocks"]:
			arr.append(str(u))
		Profile.purchased_unlocks = arr
	if p.has("unlocked_flags"):
		var arr: Array[String] = []
		for u: Variant in p["unlocked_flags"]:
			arr.append(str(u))
		Profile.unlocked_flags = arr
	if p.has("stats"):
		Profile.stats = p["stats"]
	if p.has("last_run_summary"):
		Profile.last_run_summary = p["last_run_summary"]
	if p.has("settings"):
		Profile.settings = p["settings"]
	if p.has("seen_hints"):
		var arr: Array[String] = []
		for u: Variant in p["seen_hints"]:
			arr.append(str(u))
		Profile.seen_hints = arr
