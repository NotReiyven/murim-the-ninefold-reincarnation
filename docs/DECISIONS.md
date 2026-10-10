# Decisions Log

| Date | Decision | Options Considered | Choice | Reason | Rule/Ref |
| --- | --- | --- | --- | --- | --- |
| 2026-10-10 | Blueprint Location | Leave in `.godot/docs` or move to `docs/` | Move to `docs/` | Blueprint expects `docs/BLUEPRINT.md` at root | ARCH-01 |
| 2026-10-10 | Engine Version Migration | Godot 4.3 or Godot 4.7.2 | Godot 4.7.2 | Project target engine updated to Godot 4.7.2. Allowed use of Typed Dictionaries and modern APIs. | G47 |
| 2026-10-10 | Typed Dicts in Autoloads | `Dictionary[String, CardData]` vs plain `Dictionary` | Plain `Dictionary` in autoloads only | Godot parses autoloads before `class_name` scripts are registered. `CardData`, `TraitData` etc. are unknown at autoload parse time, causing a fatal parse error. Plain `Dictionary` is the only safe choice in autoload scripts. Typed dicts remain usable everywhere else. | ARCH-02, G47 |
