import unittest
from pathlib import Path

SKILL_MD = Path(__file__).resolve().parents[1] / "skills" / "bmad-init" / "SKILL.md"


class TestBmadInitTriggers(unittest.TestCase):
    """B3: bmad-init SKILL.md must have slash-style trigger patterns."""

    def test_has_trigger_patterns_block(self):
        """SKILL.md must have trigger_patterns: block."""
        content = SKILL_MD.read_text()
        self.assertIn("trigger_patterns:", content)

    def test_has_slash_bmad(self):
        """trigger_patterns must include /bmad."""
        content = SKILL_MD.read_text()
        self.assertIn('"/bmad"', content)

    def test_has_slash_bmad_init(self):
        """trigger_patterns must include /bmad-init."""
        content = SKILL_MD.read_text()
        self.assertIn('"/bmad-init"', content)

    def test_has_slash_bmad_help(self):
        """trigger_patterns must include /bmad-help."""
        content = SKILL_MD.read_text()
        self.assertIn('"/bmad-help"', content)

    def test_has_slash_bmad_status(self):
        """trigger_patterns must include /bmad-status."""
        content = SKILL_MD.read_text()
        self.assertIn('"/bmad-status"', content)


if __name__ == "__main__":
    unittest.main()
