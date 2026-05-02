import unittest
from pathlib import Path

EXT_FILE = Path(__file__).resolve().parents[1] / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'


class TestC1NoDualRead(unittest.TestCase):
    """C1: Remove dual-read compatibility code from routing extension."""

    def test_no_name_fallback(self):
        """Should NOT have 'or wf.get("name"' fallback for display-name."""
        source = EXT_FILE.read_text()
        self.assertNotIn('or wf.get("name"', source,
                     'Old "name" column fallback must be removed — all YAML files now use display-name')

    def test_no_code_fallback(self):
        """Should NOT have 'or wf.get("code"' fallback for menu-code."""
        source = EXT_FILE.read_text()
        self.assertNotIn('or wf.get("code"', source,
                     'Old "code" column fallback must be removed — all YAML files now use menu-code')

    def test_no_skill_fallback(self):
        """Should NOT have 'or wf.get("skill"' fallback for agent."""
        source = EXT_FILE.read_text()
        self.assertNotIn('or wf.get("skill"', source,
                     'Old "skill" column fallback must be removed — all YAML files now use agent')

    def test_no_agent_name_fallback(self):
        """Should NOT have 'or wf.get("agent-name"' fallback for agent."""
        source = EXT_FILE.read_text()
        self.assertNotIn('or wf.get("agent-name"', source,
                     'Old "agent-name" column fallback must be removed — all YAML files now use agent')

    def test_no_agent_title_fallback(self):
        """Should NOT have 'or wf.get("agent-title"' fallback for agent-display-name."""
        source = EXT_FILE.read_text()
        self.assertNotIn('or wf.get("agent-title"', source,
                     'Old "agent-title" column fallback must be removed — all YAML files now use agent-display-name')

    def test_uses_display_name_directly(self):
        """Should use wf.get('display-name') directly."""
        source = EXT_FILE.read_text()
        self.assertIn('wf.get("display-name"', source,
                     'Must use display-name field directly')

    def test_uses_menu_code_directly(self):
        """Should use wf.get('menu-code') directly."""
        source = EXT_FILE.read_text()
        self.assertIn('wf.get("menu-code"', source,
                     'Must use menu-code field directly')


if __name__ == '__main__':
    unittest.main()
