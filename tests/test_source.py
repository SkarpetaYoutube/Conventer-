"""Static regression checks for core converter safeguards.

Run with: python -m unittest discover -s tests
"""
import ast
import pathlib
import unittest


SOURCE = pathlib.Path(__file__).resolve().parents[1] / "audio_converter.py"


class ConverterSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_python_source_parses(self):
        self.assertIsInstance(self.tree, ast.Module)

    def test_ffmpeg_fallback_is_present(self):
        self.assertIn('shutil.which("ffmpeg")', self.source)

    def test_no_shell_command_for_opening_directories(self):
        self.assertNotIn("os.system(", self.source)

    def test_collision_avoidance_is_present(self):
        self.assertIn("while os.path.exists(output_file):", self.source)


if __name__ == "__main__":
    unittest.main()
