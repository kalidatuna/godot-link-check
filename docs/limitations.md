# Scope and limits

Godot Link Check reads `.tscn` and `.tres` files as text. It checks declared
external resource paths using the files currently on disk. It checks that
`ExtResource("id")` references have an ID declared in the same file. Numeric
IDs and `ExtResource(1)` references in Godot 3 format-2 files are also supported,
including spacing around IDs. Function-like text inside strings is ignored.

It does not run Godot, inspect binary `.res` or `.scn` files, resolve `uid://`
paths, or know whether an imported asset is valid. Dynamic paths constructed
in GDScript are outside the scan. A `res://` symlink that escapes the project
is reported as unsafe. Source scene symlinks are skipped.

The parser recognizes quoted attributes and numeric IDs on `[ext_resource ...]`
lines; it is not a full Godot text format parser. Semicolon comments are ignored
outside quoted strings, including comments following declarations and references.
Treat findings as leads to review, and use Godot's own import and scene checks
before shipping.

Format-2 resource syntax follows the [Godot 3.5 TSCN documentation](https://docs.godotengine.org/en/3.5/development/file_formats/tscn.html#resources).
