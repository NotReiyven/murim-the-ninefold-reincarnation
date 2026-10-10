extends SceneTree

func _init() -> void:
	print("Running tests... (M0 stub)")
	var failures: int = 0
	
	# M0 simply runs and returns 0 if everything is fine
	if failures > 0:
		quit(failures)
	else:
		quit(0)
