import os

files = {
    'tools/build_content.gd': '''extends SceneTree

func _init() -> void:
	print("Building content... (M0 stub)")
	quit(0)
''',

    'tools/validate_content.gd': '''extends SceneTree

func _init() -> void:
	print("Validating content... (M0 stub)")
	quit(0)
''',

    'tests/run_tests.gd': '''extends SceneTree

func _init() -> void:
	print("Running tests... (M0 stub)")
	var failures: int = 0
	
	# M0 simply runs and returns 0 if everything is fine
	if failures > 0:
		quit(failures)
	else:
		quit(0)
''',

    'tests/test_slop_scan.gd': '''class_name TestSlopScan
extends RefCounted

func run_tests() -> int:
	print("Running slop scan... (M0 stub)")
	return 0
'''
}

for path, content in files.items():
    with open(path, 'w') as f:
        f.write(content)
