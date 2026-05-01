"""Phase G: Verify MANDATORY PROCESS COMPLIANCE section in all 20 agent role.md files."""
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
AGENTS_DIR = PROJECT / 'agents'

COMPLIANCE_SECTION = '## MANDATORY PROCESS COMPLIANCE'
COMPLIANCE_DIRECTIVES = [
    'You are a PROCESS-DRIVEN agent',
    'You MUST load the appropriate BMAD skill',
    'You MUST follow the step-file architecture',
    'You MUST execute steps sequentially',
    'You MUST read each step file completely',
    'You MUST halt at checkpoints',
    'You MUST NOT produce workflow artifacts except through the step-by-step process',
    'Complete task" means complete the PROCESS',
]


def _get_all_agents():
    return sorted([d.name for d in AGENTS_DIR.iterdir()
                   if d.is_dir() and d.name.startswith('bmad-')
                   and d.name != '_shared'])


class TestPhaseGCompliance(unittest.TestCase):
    """G-P0-2: All 20 agent role.md must contain process compliance section."""

    def test_twenty_agents_have_compliance(self):
        """All 20 role.md files must contain MANDATORY PROCESS COMPLIANCE."""
        for agent in _get_all_agents():
            role = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.role.md'
            content = role.read_text()
            self.assertIn(COMPLIANCE_SECTION, content,
                        f'{agent} missing compliance section')

    def test_compliance_before_persona(self):
        """Compliance section must appear before persona definition."""
        for agent in _get_all_agents():
            role = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.role.md'
            content = role.read_text()
            compliance_pos = content.find(COMPLIANCE_SECTION)
            # Find persona marker
            persona_markers = ['## BMAD Persona:', '## BMAD Identity']
            persona_pos = None
            for marker in persona_markers:
                pos = content.find(marker)
                if pos != -1:
                    if persona_pos is None or pos < persona_pos:
                        persona_pos = pos
            if persona_pos is not None:
                self.assertLess(compliance_pos, persona_pos,
                              f'{agent}: compliance section must be before persona')

    def test_all_directives_present(self):
        """All 6 compliance directives must be present."""
        for agent in _get_all_agents():
            role = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.role.md'
            content = role.read_text()
            for directive in COMPLIANCE_DIRECTIVES:
                self.assertIn(directive, content,
                            f'{agent} missing directive: {directive}')


if __name__ == '__main__':
    unittest.main()
