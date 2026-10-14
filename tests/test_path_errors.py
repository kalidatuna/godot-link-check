import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from godot_link_check.cli import main
from godot_link_check.model import ExternalResource
from godot_link_check.paths import check_paths
from godot_link_check.scanner import scan


class PathErrorTests(unittest.TestCase):
    def test_null_path_is_a_finding_and_scan_continues(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "project.godot").write_text("[application]\n")
            (project / "scene.tscn").write_text(
                '[ext_resource path="res://bad\\u0000.gd" id="bad"]\n'
                '[ext_resource path="res://missing.gd" id="other"]\n'
            )
            findings = scan(project)
            self.assertEqual([(item.line, item.code) for item in findings],
                             [(1, "path-error"), (2, "missing-file")])
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                self.assertEqual(main([directory, "--json"]), 1)
            self.assertEqual(json.loads(output.getvalue())[0]["code"], "path-error")

    def test_symlink_loop_is_a_finding(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "loop.gd").symlink_to("loop.gd")
            (project / "scene.tscn").write_text(
                '[ext_resource path="res://loop.gd" id="x"]\n'
            )
            self.assertEqual([item.code for item in scan(project)], ["path-error"])

    def test_resolution_error_does_not_abort_remaining_checks(self):
        project = Path("/project")
        declarations = [ExternalResource("x", "res://script.gd", 4)]
        with patch.object(Path, "resolve", side_effect=PermissionError("denied")):
            findings = check_paths(project, project / "scene.tscn", declarations)
        self.assertEqual([(item.file, item.line, item.code) for item in findings],
                         [("scene.tscn", 4, "path-error")])
