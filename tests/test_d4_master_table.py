import unittest
from pathlib import Path

ROLE_MD = Path(__file__).resolve().parents[1] / 'agents' / 'bmad-master' / 'prompts' / 'agent.system.main.role.md'


class TestD4StaticTableRemoval(unittest.TestCase):
    """D4: Static 19-agent table removed from bmad-master role, replaced with {{agent_profiles}}."""

    def test_no_static_agent_table(self):
        """The hardcoded 19-row profile|persona|module|specialty table must be gone."""
        content = ROLE_MD.read_text()
        # The old table had rows like: | `bmad-analyst` | Mary (Business Analyst)
        self.assertNotIn('| `bmad-analyst`', content,
                    'Static bmad-analyst row still present')
        self.assertNotIn('| `bmad-dev`', content,
                    'Static bmad-dev row still present')
        self.assertNotIn('| `bmad-architect`', content,
                    'Static bmad-architect row still present')

    def test_has_agent_profiles_placeholder(self):
        """Role file must reference {{agent_profiles}} for dynamic agent list."""
        content = ROLE_MD.read_text()
        self.assertIn('{{agent_profiles}}', content,
                    'Missing {{agent_profiles}} placeholder')

    def test_retains_modules_table(self):
        """The 4-row BMAD Modules table must be preserved."""
        content = ROLE_MD.read_text()
        self.assertIn('| **BMM**', content)
        self.assertIn('| **BMB**', content)
        self.assertIn('| **TEA**', content)
        self.assertIn('| **CIS**', content)

    def test_retains_routing_guidance(self):
        """Routing guidance prose must be present."""
        content = ROLE_MD.read_text()
        self.assertIn('call_subordinate', content)
        self.assertIn('profile', content)


if __name__ == '__main__':
    unittest.main()
