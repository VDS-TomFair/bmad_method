import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
AGENTS_DIR = PROJECT / 'agents'
SHARED = PROJECT / 'prompts' / 'bmad-agent-shared.md'


def _get_non_master_agents():
    return sorted([d.name for d in AGENTS_DIR.iterdir()
                   if d.is_dir() and d.name.startswith('bmad-')
                   and d.name not in ('_shared', 'bmad-master')])


class TestD3IncludeDirective(unittest.TestCase):
    """D3: 19 non-master agent specifics must use {{ include "bmad-agent-shared.md" }}."""

    def test_master_does_not_use_include(self):
        """bmad-master must NOT use the include directive."""
        spec = AGENTS_DIR / 'bmad-master' / 'prompts' / 'agent.system.main.specifics.md'
        content = spec.read_text()
        self.assertNotIn('bmad-agent-shared.md', content)

    def test_non_master_agents_use_include(self):
        """All 19 non-master agents must include bmad-agent-shared.md."""
        for agent in _get_non_master_agents():
            spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
            content = spec.read_text()
            self.assertIn('{{ include "bmad-agent-shared.md" }}', content,
                        f'{agent} missing include directive')

    def test_non_master_retains_role_section(self):
        """Each agent must retain its Role section."""
        for agent in _get_non_master_agents():
            spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
            content = spec.read_text()
            self.assertIn('## Your Role in the Conversation', content,
                        f'{agent} missing Role section')

    def test_non_master_retains_skills_table(self):
        """Each agent must retain its Available BMAD skills table."""
        for agent in _get_non_master_agents():
            spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
            content = spec.read_text()
            self.assertIn('Available BMAD skills:', content,
                        f'{agent} missing skills table')

    def test_non_master_no_duplicate_shared_sections(self):
        """After include, agents must NOT have inline copies of shared sections."""
        # These sections should be in the shared fragment, not inline
        shared_only_sections = [
            '## BMAD Activation Protocol',
            '## Initial Clarification',
            '## Thinking Framework',
            '## Tool Calling',
            '## File and Artifact Handling',
        ]
        for agent in _get_non_master_agents():
            spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
            content = spec.read_text()
            for section in shared_only_sections:
                self.assertNotIn(section, content,
                            f'{agent} still has inline section: {section}')


if __name__ == '__main__':
    unittest.main()
