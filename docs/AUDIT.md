# Phase Zero Repository Audit

## Overview
The repository is an essentially empty Godot project. The `docs/BLUEPRINT.md` file was found inside the `.godot/docs/` directory instead of the root `docs/` directory. The project settings require configuration according to the blueprint.

## 1. Works
- Godot project baseline (`project.godot` exists).

## 2. Partial
- `project.godot` exists but needs to be updated with the exact settings specified in §4.1 (e.g., `viewport_width/height`, `low_processor_mode`, `default_texture_filter`, warnings, etc.). It currently specifies "4.7" instead of "4.3" in features.

## 3. Broken
- `BLUEPRINT.md` is misplaced inside `.godot/docs/`. It should be moved to the root `docs/` folder.

## 4. Missing
The entire directory structure specified in §4.2 is missing and needs to be created:
- `docs/` (root level)
- `scenes/` and all subdirectories (`hub/`, `judgment/`, `traits/`, `map/`, `combat/`, `reward/`, `merchant/`, `rest/`, `event/`, `death/`, `ui/`)
- `scenes/boot.tscn` (main scene)
- `scripts/` and all subdirectories (`config/`, `data/`, `logic/`, `autoload/`, `persistence/`, `ui/`, `debug/`)
- `content/` and all subdirectories
- `assets/` and all subdirectories (`art/`, `fonts/`, `theme/`, `audio/`)
- `tools/` (`build_content.gd`, `validate_content.gd`)
- `tests/` (`run_tests.gd`, etc.)
- `localization/`
- All 4 autoloads (`content.gd`, `profile.gd`, `run_session.gd`, `router.gd`)
- All data resource classes and logic scripts.

## 5. Reuse
- `icon.svg` (default Godot icon, will be replaced later or used as a placeholder).
- `.gitignore` and `.gitattributes`.

## 6. Replace
- `project.godot` needs to be replaced/updated because it lacks the required screen and rendering configurations for this 2D portrait mobile game (defect: missing `display/window/size/viewport_width`, `handheld/orientation`, `low_processor_mode`, etc.).
