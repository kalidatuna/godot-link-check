# Godot Link Check

A small offline checker for Godot text scenes (`.tscn`) and resources (`.tres`).
It reports missing `res://` files, duplicate external resource IDs, and
`ExtResource(...)` references with no declaration. No Godot installation or
third-party Python package is required.

```sh
python3 -m godot_link_check /path/to/project
python3 -m godot_link_check /path/to/project --json
```

The command exits 0 for a clean project, 1 for findings, and 2 for invalid
input. It scans the project root recursively and skips `.git`, `.godot`, and
`backups` by default. Use `--include-backups` to include the latter.

This is a static check. It does not open the project in Godot, resolve `uid://`
identifiers, or validate scripts and imported assets. See
[limitations](docs/limitations.md) for details.
