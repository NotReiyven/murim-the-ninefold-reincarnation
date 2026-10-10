import os

files = {
    'scripts/persistence/save_io.gd': '''class_name SaveIO
extends RefCounted

const SAVE_MAX_BYTES: int = 1048576

static func save_json(file_name: String, data: Dictionary) -> Error:
	var path: String = "user://" + file_name
	var tmp_path: String = path + ".tmp"
	var bak_path: String = path + ".bak"
	
	var json_str: String = JSON.stringify(data)
	if json_str.length() > SAVE_MAX_BYTES:
		return ERR_FILE_CANT_WRITE
		
	var file = FileAccess.open(tmp_path, FileAccess.WRITE)
	if FileAccess.get_open_error() != OK:
		return FileAccess.get_open_error()
		
	file.store_string(json_str)
	var err = file.get_error()
	if err != OK:
		return err
	file.close()
	
	# Verify
	file = FileAccess.open(tmp_path, FileAccess.READ)
	if FileAccess.get_open_error() != OK:
		return FileAccess.get_open_error()
	var test_str: String = file.get_as_text()
	var json = JSON.new()
	if json.parse(test_str) != OK:
		DirAccess.remove_absolute(tmp_path)
		return ERR_PARSE_ERROR
	file.close()
	
	if FileAccess.file_exists(path):
		if FileAccess.file_exists(bak_path):
			DirAccess.remove_absolute(bak_path)
		DirAccess.rename_absolute(path, bak_path)
		
	err = DirAccess.rename_absolute(tmp_path, path)
	if err != OK and FileAccess.file_exists(bak_path):
		DirAccess.rename_absolute(bak_path, path)
	return err

static func load_json(file_name: String) -> Dictionary:
	var path: String = "user://" + file_name
	if not FileAccess.file_exists(path):
		path = "user://" + file_name + ".bak"
		if not FileAccess.file_exists(path):
			return {}
	
	var file = FileAccess.open(path, FileAccess.READ)
	if FileAccess.get_open_error() != OK:
		return {}
	var text: String = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	if json.parse(text) == OK:
		var result = json.data
		if typeof(result) == TYPE_DICTIONARY:
			return result
	return {}
''',

    'scripts/persistence/profile_codec.gd': '''class_name ProfileCodec
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
	var dict = SaveIO.load_json("profile.json")
	if dict.has("profile"):
		var p = dict["profile"]
		if p.has("soul_fragments"): Profile.soul_fragments = clampi(int(p["soul_fragments"]), 0, 1000000)
		if p.has("lifetime_soul_fragments"): Profile.lifetime_soul_fragments = clampi(int(p["lifetime_soul_fragments"]), 0, 100000000)
		if p.has("purchased_unlocks"):
			var arr: Array[String] = []
			for u in p["purchased_unlocks"]: arr.append(str(u))
			Profile.purchased_unlocks = arr
		if p.has("unlocked_flags"):
			var arr: Array[String] = []
			for u in p["unlocked_flags"]: arr.append(str(u))
			Profile.unlocked_flags = arr
		if p.has("stats"): Profile.stats = p["stats"]
		if p.has("last_run_summary"): Profile.last_run_summary = p["last_run_summary"]
		if p.has("settings"): Profile.settings = p["settings"]
		if p.has("seen_hints"):
			var arr: Array[String] = []
			for u in p["seen_hints"]: arr.append(str(u))
			Profile.seen_hints = arr
'''
}

for path, content in files.items():
    with open(path, 'w') as f:
        f.write(content)
