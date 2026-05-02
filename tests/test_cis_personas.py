import unittest
import yaml
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
AGENTS_DIR = BASE / 'agents'

CIS_AGENTS = {
    'bmad-innovation': {
        'title': 'BMAD Innovation Strategist',
        'icon': '⚡',
        'forbidden_names': ['Victor'],
    },
    'bmad-problem-solver': {
        'title': 'BMAD Creative Problem Solver',
        'icon': '🔬',
        'forbidden_names': ['Dr. Quinn', 'Dr. Quinn'],
    },
    'bmad-design-thinking': {
        'title': 'BMAD Design Thinking Coach',
        'icon': '🎯',
        'forbidden_names': ['Maya'],
    },
    'bmad-brainstorming-coach': {
        'title': 'BMAD Brainstorming Coach',
        'icon': '🧠',
        'forbidden_names': ['Carson'],
    },
    'bmad-storyteller': {
        'title': 'BMAD Storyteller',
        'icon': '📖',
        'forbidden_names': ['Sophia'],
    },
    'bmad-presentation': {
        'title': 'BMAD Presentation Master',
        'icon': '🖼️',
        'forbidden_names': ['Caravaggio'],
    },
}

ALL_FORBIDDEN = ['Victor', 'Dr. Quinn', 'Maya', 'Carson', 'Sophia', 'Caravaggio']


class TestCISAgentTitles(unittest.TestCase):
    """CIS agent.yaml files must use generic titles, not persona names."""

    def test_cis_agent_count(self):
        """All 6 CIS agent directories must exist."""
        for agent_dir in CIS_AGENTS:
            self.assertTrue((AGENTS_DIR / agent_dir).exists(),
                            f'{agent_dir} directory must exist')

    def test_cis_titles_are_generic(self):
        """Each CIS agent.yaml must have the correct generic title."""
        for agent_dir, spec in CIS_AGENTS.items():
            yaml_path = AGENTS_DIR / agent_dir / 'agent.yaml'
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            self.assertEqual(data['title'], spec['title'],
                             f'{agent_dir}: expected title={spec["title"]}')


class TestNoPersonaNames(unittest.TestCase):
    """No CIS persona names should appear in any agent file."""

    def test_no_persona_names_in_agent_dirs(self):
        """CIS agent directories must not contain persona names."""
        for agent_dir in CIS_AGENTS:
            agent_path = AGENTS_DIR / agent_dir
            for md_file in agent_path.rglob('*.md'):
                content = md_file.read_text()
                for name in ALL_FORBIDDEN:
                    self.assertNotIn(name, content,
                                     f'{md_file.relative_to(BASE)} contains "{name}"')
            yaml_path = agent_path / 'agent.yaml'
            if yaml_path.exists():
                content = yaml_path.read_text()
                for name in ALL_FORBIDDEN:
                    self.assertNotIn(name, content,
                                     f'{yaml_path.relative_to(BASE)} contains "{name}"')

    def test_no_persona_names_in_cis_skills(self):
        """CIS skill files must not contain persona names."""
        cis_skills = BASE / 'skills' / 'bmad-cis'
        if not cis_skills.exists():
            self.skipTest('CIS skills directory not found')
        for f in cis_skills.rglob('*'):
            if f.is_file() and f.suffix in ('.md', '.yaml', '.csv', '.toml'):
                content = f.read_text()
                for name in ALL_FORBIDDEN:
                    self.assertNotIn(name, content,
                                     f'{f.relative_to(BASE)} contains "{name}"')


class TestIconCollisions(unittest.TestCase):
    """Verify no icon collisions between agents."""

    def test_paint_icon_unique_to_sally(self):
        """🎨 must only be used by Sally (bmad-ux-designer)."""
        paint_icon = '🎨'
        # Check CIS customize files don't have 🎨
        for agent_dir in CIS_AGENTS:
            role_path = AGENTS_DIR / agent_dir / 'prompts' / 'agent.system.main.role.md'
            if role_path.exists():
                content = role_path.read_text()
                # design-thinking and presentation should NOT have 🎨
                if agent_dir in ('bmad-design-thinking', 'bmad-presentation'):
                    self.assertNotIn(paint_icon, content,
                                     f'{agent_dir} should not use 🎨 icon')

    def test_design_thinking_uses_target(self):
        """bmad-design-thinking must use 🎯 (not 🎨)."""
        role_path = AGENTS_DIR / 'bmad-design-thinking' / 'prompts' / 'agent.system.main.role.md'
        content = role_path.read_text()
        self.assertIn('🎯', content, 'Design Thinking must use 🎯 icon')

    def test_presentation_uses_framed_picture(self):
        """bmad-presentation must use 🖼️ (not 🎨)."""
        role_path = AGENTS_DIR / 'bmad-presentation' / 'prompts' / 'agent.system.main.role.md'
        content = role_path.read_text()
        self.assertIn('🖼️', content, 'Presentation must use 🖼️ icon')


if __name__ == '__main__':
    unittest.main()
