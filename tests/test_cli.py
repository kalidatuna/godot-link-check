import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from godot_link_check.cli import main


class CliTests(unittest.TestCase):
    def test_json_and_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "project.godot").write_text("[application]\n")
            (project / "scene.tscn").write_text('[ext_resource path="res://lost.gd" id="x"]')
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = main([directory, "--json"])
            self.assertEqual(result, 1)
            self.assertEqual(json.loads(output.getvalue())[0]["code"], "missing-file")

    def test_clean_project(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "project.godot").write_text("[application]\n")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([directory]), 0)


if __name__ == "__main__":
    unittest.main()
