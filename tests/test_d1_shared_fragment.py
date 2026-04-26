import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SHARED = PROJECT / 'agents' / '_shared' / 'prompts' / 'bmad-agent-shared.md'

SHARED_SECTIONS = [
    'A0 Variable Resolution',
    'BMAD Activation Protocol',
    'Initial Clarification',
    'Thinking Framework',
    'Tool Calling',
    'File and Artifact Handling',
]


class TestD1SharedFragment(unittest.TestCase):
    """D1: Shared fragment file must exist with all 7 sections."""

    def test_shared_fragment_exists(self):
        self.assertTrue(SHARED.exists(), f'Shared fragment not found at {SHARED}')

    def test_shared_fragment_has_all_sections(self):
        content = SHARED.read_text()
        for section in SHARED_SECTIONS:
            self.assertIn(f'## {section}', content,
                        f'Shared fragment missing section: {section}')

    def test_shared_fragment_has_no_role_section(self):
        """Shared fragment must NOT contain a Role section (agent-specific)."""
        content = SHARED.read_text()
        self.assertNotIn('## Your Role', content)

    def test_shared_fragment_has_no_skills_table(self):
        """Shared fragment must NOT contain Available Skills table (agent-specific)."""
        content = SHARED.read_text()
        self.assertNotIn('Available BMAD skills', content)


if __name__ == '__main__':
    unittest.main()
