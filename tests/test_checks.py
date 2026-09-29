import tempfile
import unittest
from pathlib import Path

from godot_link_check.parse import parse_resource
from godot_link_check.scanner import scan


class ResourceTests(unittest.TestCase):
    def test_parse_declarations_and_references(self):
        text = '[ext_resource type="Script" path="res://a.gd" id="x"]\nscript = ExtResource("x")\n'
        declarations, references = parse_resource(text)
        self.assertEqual((declarations[0].resource_id, declarations[0].path), ("x", "res://a.gd"))
        self.assertEqual((references[0].resource_id, references[0].line), ("x", 2))

    def test_missing_duplicate_and_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "project.godot").write_text("[application]\n")
            (project / "scene.tscn").write_text(
                '[gd_scene format=3]\n[ext_resource path="res://missing.gd" id="x"]\n'
                '[ext_resource path="res://missing.gd" id="x"]\n'
                '[node name="Root" type="Node"]\nscript = ExtResource("absent")\n'
            )
            self.assertEqual(
                [finding.code for finding in scan(project)],
                ["missing-file", "duplicate-id", "missing-file", "unknown-id"],
            )

    def test_backups_skipped_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "backups").mkdir()
            (project / "backups" / "old.tres").write_text('[ext_resource path="res://gone" id="x"]')
            self.assertEqual(scan(project), [])
            self.assertEqual(len(scan(project, include_backups=True)), 1)

    def test_unsafe_path(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "bad.tres").write_text('[ext_resource path="res://../other" id="x"]')
            self.assertEqual(scan(project)[0].code, "unsafe-path")


if __name__ == "__main__":
    unittest.main()
