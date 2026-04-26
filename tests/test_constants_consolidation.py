import unittest
from pathlib import Path

CORE_FILE = Path(__file__).resolve().parents[1] / 'helpers' / 'bmad_status_core.py'
API_FILE = Path(__file__).resolve().parents[1] / 'api' / '_bmad_status.py'
CLI_FILE = Path(__file__).resolve().parents[1] / 'skills' / 'bmad-init' / 'scripts' / 'bmad-status.py'


class TestConstantsInCore(unittest.TestCase):
    """B7: AGENT_NAMES and PHASE_ACTIONS live once in bmad_status_core.py."""

    def test_core_has_agent_names(self):
        """bmad_status_core.py must define AGENT_NAMES."""
        source = CORE_FILE.read_text()
        self.assertIn('AGENT_NAMES', source)

    def test_core_has_phase_actions(self):
        """bmad_status_core.py must define PHASE_ACTIONS."""
        source = CORE_FILE.read_text()
        self.assertIn('PHASE_ACTIONS', source)

    def test_api_no_agent_names_literal(self):
        """api/_bmad_status.py must NOT have AGENT_NAMES dict literal."""
        source = API_FILE.read_text()
        # Should not have the opening brace on same line as AGENT_NAMES =
        self.assertNotIn('AGENT_NAMES = {', source,
                     'AGENT_NAMES dict must be imported from core, not defined locally')

    def test_api_no_phase_actions_literal(self):
        """api/_bmad_status.py must NOT have PHASE_ACTIONS dict literal."""
        source = API_FILE.read_text()
        self.assertNotIn('PHASE_ACTIONS = {', source,
                     'PHASE_ACTIONS dict must be imported from core, not defined locally')

    def test_cli_no_agent_names_literal(self):
        """bmad-status.py must NOT have AGENT_NAMES dict literal."""
        source = CLI_FILE.read_text()
        self.assertNotIn('AGENT_NAMES = {', source,
                     'AGENT_NAMES dict must be imported from core, not defined locally')

    def test_cli_no_phase_actions_literal(self):
        """bmad-status.py must NOT have PHASE_ACTIONS dict literal."""
        source = CLI_FILE.read_text()
        self.assertNotIn('PHASE_ACTIONS = {', source,
                     'PHASE_ACTIONS dict must be imported from core, not defined locally')

    def test_api_imports_agent_names_from_core(self):
        """api must import AGENT_NAMES from core module."""
        source = API_FILE.read_text()
        self.assertIn('AGENT_NAMES', source)
        # Must be imported via _core_mod
        self.assertTrue(
            'AGENT_NAMES' in source and ('_core_mod.AGENT_NAMES' in source or 'AGENT_NAMES   = _core_mod' in source),
            'AGENT_NAMES must be imported from _core_mod'
        )


if __name__ == '__main__':
    unittest.main()
