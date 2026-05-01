"""Phase G: Verify shared fragment include resolution for all 19 non-master agents.

After G-P0-1, the shared fragment lives at prompts/bmad-agent-shared.md (plugin root),
which IS in A0's search chain. All 19 non-master agents reference it via
{{ include "bmad-agent-shared.md" }} in their specifics.md.
"""
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = PROJECT / 'prompts'
AGENTS_DIR = PROJECT / 'agents'
SHARED_PROMPT = PROMPTS_DIR / 'bmad-agent-shared.md'


def _get_non_master_agents():
    return sorted([d.name for d in AGENTS_DIR.iterdir()
                   if d.is_dir() and d.name.startswith('bmad-')
                   and d.name not in ('_shared', 'bmad-master')])


def _get_all_agents():
    return sorted([d.name for d in AGENTS_DIR.iterdir()
                   if d.is_dir() and d.name.startswith('bmad-')
                   and d.name != '_shared'])


class TestPhaseGIncludeLocation(unittest.TestCase):
    """G-P0-1: Shared fragment must be at prompts/bmad-agent-shared.md."""

    def test_shared_fragment_in_prompts_dir(self):
        """Shared fragment must exist at plugin root prompts/ directory."""
        self.assertTrue(SHARED_PROMPT.exists(),
                        f'Shared fragment not found at {SHARED_PROMPT}')

    def test_old_shared_location_removed(self):
        """Old agents/_shared/prompts/ directory must NOT exist."""
        old_dir = AGENTS_DIR / '_shared'
        self.assertFalse(old_dir.exists(),
                        f'Old _shared directory still exists at {old_dir}')

    def test_prompts_dir_exists(self):
        """Plugin root prompts/ directory must exist."""
        self.assertTrue(PROMPTS_DIR.exists(),
                        f'prompts/ directory not found at {PROMPTS_DIR}')


class TestPhaseGIncludeDirective(unittest.TestCase):
    """G-P0-1: All 19 non-master agents must use {{ include "bmad-agent-shared.md" }}."""

    def test_non_master_agents_use_include(self):
        """All 19 non-master specifics.md must include the shared fragment."""
        for agent in _get_non_master_agents():
            spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
            content = spec.read_text()
            self.assertIn('{{ include "bmad-agent-shared.md" }}', content,
                        f'{agent} missing include directive')

    @unittest.skip('G-P0-5 not yet implemented')
    def test_master_uses_include_after_fix(self):
        """After G-P0-5, bmad-master specifics must also use the include."""
        spec = AGENTS_DIR / 'bmad-master' / 'prompts' / 'agent.system.main.specifics.md'
        content = spec.read_text()
        self.assertIn('{{ include "bmad-agent-shared.md" }}', content,
                      'bmad-master missing include directive (G-P0-5)')


class TestPhaseGAgentCount(unittest.TestCase):
    """Verify expected agent counts."""

    def test_twenty_agent_dirs(self):
        """Must have exactly 20 BMAD agent directories."""
        agents = _get_all_agents()
        self.assertEqual(len(agents), 20,
                        f'Expected 20 agents, found {len(agents)}: {agents}')

    def test_nineteen_non_master_agents(self):
        """Must have exactly 19 non-master agent directories."""
        agents = _get_non_master_agents()
        self.assertEqual(len(agents), 19,
                        f'Expected 19 non-master agents, found {len(agents)}')


class TestPhaseGSharedContent(unittest.TestCase):
    """Verify shared fragment has required sections."""

    def test_shared_has_variable_resolution(self):
        content = SHARED_PROMPT.read_text()
        self.assertIn('## A0 Variable Resolution', content)

    def test_shared_has_activation_protocol(self):
        content = SHARED_PROMPT.read_text()
        self.assertIn('## BMAD Activation Protocol', content)

    def test_shared_has_thinking_framework(self):
        content = SHARED_PROMPT.read_text()
        self.assertIn('## Thinking Framework', content)

    def test_shared_has_tool_calling(self):
        content = SHARED_PROMPT.read_text()
        self.assertIn('## Tool Calling', content)

    def test_shared_has_artifact_handling(self):
        content = SHARED_PROMPT.read_text()
        self.assertIn('## File and Artifact Handling', content)


if __name__ == '__main__':
    unittest.main()
