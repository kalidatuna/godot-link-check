import pathlib, tempfile, unittest
from godot_link_check.parse import parse_resource
from godot_link_check.scanner import scan

class Godot3ResourceTests(unittest.TestCase):
    def test_numeric_resource_ids_and_references_are_supported(self):
        declarations, references = parse_resource('[ext_resource path="res://a.gd" type="Script" id=1]\nscript = ExtResource( 1 )\ntext = "ExtResource(99)"\n')
        self.assertEqual([item.resource_id for item in declarations], ['1'])
        self.assertEqual([item.resource_id for item in references], ['1'])

    def test_format_two_paths_duplicates_and_unknown_ids_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / 'project.godot').write_text('[application]\n')
            (root / 'scene.tscn').write_text('[gd_scene format=2]\n[ext_resource path="res://missing.gd" id=2]\n[ext_resource path="res://missing.gd" id=2]\nscript = ExtResource(9)\n')
            self.assertEqual([item.code for item in scan(root)], ['missing-file', 'duplicate-id', 'missing-file', 'unknown-id'])
