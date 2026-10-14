import contextlib
import errno
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from godot_link_check.cli import main
from godot_link_check.scanner import scan


class WalkErrorTests(unittest.TestCase):
    def walk_with_denied_directory(self, project, **kwargs):
        kwargs["onerror"](PermissionError(errno.EACCES, "Permission denied",
                                          str(project / "restricted")))
        yield str(project), [], ["scene.tscn"]

    def test_directory_error_is_reported_and_readable_files_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "scene.tscn").write_text(
                '[ext_resource path="res://missing.gd" id="x"]\n'
            )
            with patch("godot_link_check.scanner.os.walk",
                       side_effect=self.walk_with_denied_directory):
                findings = scan(project)
            self.assertEqual([(item.file, item.code) for item in findings],
                             [("restricted", "read-error"),
                              ("scene.tscn", "missing-file")])

    def test_incomplete_scan_does_not_exit_successfully(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "project.godot").write_text("[application]\n")
            (project / "scene.tscn").write_text("[gd_scene format=3]\n")
            output = io.StringIO()
            with patch("godot_link_check.scanner.os.walk",
                       side_effect=self.walk_with_denied_directory), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(main([directory, "--json"]), 1)
            self.assertEqual(json.loads(output.getvalue())[0]["file"], "restricted")

    def test_error_without_filename_uses_project_root(self):
        with tempfile.TemporaryDirectory() as directory:
            def failed_walk(project, **kwargs):
                kwargs["onerror"](OSError("Directory disappeared"))
                return iter(())

            with patch("godot_link_check.scanner.os.walk", side_effect=failed_walk):
                findings = scan(Path(directory))
            self.assertEqual([(item.file, item.code) for item in findings],
                             [(".", "read-error")])
