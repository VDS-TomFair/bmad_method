import unittest
from pathlib import Path

STORE_JS = Path(__file__).resolve().parents[1] / 'webui' / 'bmad-dashboard-store.js'


class TestDashboardStoreErrorState(unittest.TestCase):
    """B5: this.error must be declared in store initial state."""

    def test_error_in_initial_state(self):
        """Store initial state must include 'error' property."""
        source = STORE_JS.read_text()
        self.assertIn('error:', source,
                     "Store initial state must declare 'error' property")

    def test_error_declared_in_create_store_block(self):
        """error must be in the createStore initial state, not just set in refresh()."""
        source = STORE_JS.read_text()
        lines = source.splitlines()
        in_state = False
        state_lines = []
        for line in lines:
            stripped = line.strip()
            if 'createStore(' in stripped:
                in_state = True
                continue
            if in_state:
                if stripped.startswith('async ') or stripped.startswith('cleanup'):
                    break
                state_lines.append(stripped)
        state_block = '\n'.join(state_lines)
        self.assertIn('error:', state_block,
                     "'error' must be in the initial state object of createStore")


if __name__ == '__main__':
    unittest.main()
