class_name SaveIO
extends RefCounted

const SAVE_MAX_BYTES: int = 1048576

static func save_json(file_name: String, data: Dictionary) -> Error:
	var path: String = "user://" + file_name
	var tmp_path: String = path + ".tmp"
	var bak_path: String = path + ".bak"

	var json_str: String = JSON.stringify(data)
	if json_str.length() > SAVE_MAX_BYTES:
		return ERR_FILE_CANT_WRITE

	var file: FileAccess = FileAccess.open(tmp_path, FileAccess.WRITE)
	if FileAccess.get_open_error() != OK:
		return FileAccess.get_open_error()

	file.store_string(json_str)
	var write_err: Error = file.get_error()
	if write_err != OK:
		return write_err
	file.close()

	# Verify the written data is valid JSON before swapping files.
	var vfile: FileAccess = FileAccess.open(tmp_path, FileAccess.READ)
	if FileAccess.get_open_error() != OK:
		return FileAccess.get_open_error()
	var test_str: String = vfile.get_as_text()
	var json: JSON = JSON.new()
	if json.parse(test_str) != OK:
		DirAccess.remove_absolute(tmp_path)
		return ERR_PARSE_ERROR
	vfile.close()

	if FileAccess.file_exists(path):
		if FileAccess.file_exists(bak_path):
			DirAccess.remove_absolute(bak_path)
		DirAccess.rename_absolute(path, bak_path)

	var rename_err: Error = DirAccess.rename_absolute(tmp_path, path)
	if rename_err != OK and FileAccess.file_exists(bak_path):
		DirAccess.rename_absolute(bak_path, path)
	return rename_err

static func load_json(file_name: String) -> Dictionary:
	var path: String = "user://" + file_name
	if not FileAccess.file_exists(path):
		path = "user://" + file_name + ".bak"
		if not FileAccess.file_exists(path):
			return {}

	var file: FileAccess = FileAccess.open(path, FileAccess.READ)
	if FileAccess.get_open_error() != OK:
		return {}
	var text: String = file.get_as_text()
	file.close()

	var json: JSON = JSON.new()
	if json.parse(text) == OK:
		var result: Variant = json.data
		if typeof(result) == TYPE_DICTIONARY:
			return result as Dictionary
	return {}
