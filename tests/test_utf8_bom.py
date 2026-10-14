import tempfile
import unittest
from pathlib import Path

from godot_link_check.scanner import scan


class Utf8BomTests(unittest.TestCase):
    def test_bom_does_not_hide_first_external_resource(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "script.gd").write_text("extends Node\n", encoding="utf-8")
            scene = project / "scene.tscn"
            scene.write_text(
                '[ext_resource path="res://script.gd" id="x"]\n'
                'script = ExtResource("x")\n',
                encoding="utf-8-sig",
            )
            self.assertEqual(scan(project), [])
            (project / "script.gd").unlink()
            findings = scan(project)
            self.assertEqual([(item.code, item.line) for item in findings],
                             [("missing-file", 1)])

    def test_invalid_utf8_still_reports_read_error(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "bad.tres").write_bytes(b"\xef\xbb\xbf\xff")
            self.assertEqual([item.code for item in scan(project)], ["read-error"])
