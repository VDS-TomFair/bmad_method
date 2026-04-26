import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
HTML = PROJECT / 'webui' / 'bmad-dashboard.html'
STORE = PROJECT / 'webui' / 'bmad-dashboard-store.js'


class TestD6ErrorDisplay(unittest.TestCase):
    """D6: Dashboard error display uses x-text only, store-gated."""

    def test_no_x_html_in_dashboard(self):
        """Dashboard must NOT use x-html anywhere (XSS risk)."""
        content = HTML.read_text()
        self.assertNotIn('x-html', content,
                    'x-html found in dashboard HTML — must use x-text only')

    def test_error_display_uses_x_text(self):
        """Error display template must use x-text, not x-html."""
        content = HTML.read_text()
        # Must have an error state display section
        self.assertIn('error-state', content,
                    'Missing error-state CSS class for error display')
        # Error display must be gated by store error state
        self.assertIn('$store.bmadDashboard.error', content,
                    'Error display not gated by $store.bmadDashboard.error')

    def test_store_sets_error_on_failure(self):
        """Store must set this.error in catch block."""
        content = STORE.read_text()
        self.assertIn('this.error', content,
                    'Store does not set this.error')
        # error should be set in catch block
        lines = content.splitlines()
        in_catch = False
        found_error_set = False
        for line in lines:
            if 'catch' in line:
                in_catch = True
            if in_catch and 'this.error' in line:
                found_error_set = True
            if in_catch and 'finally' in line:
                in_catch = False
        self.assertTrue(found_error_set,
                    'Store catch block does not set this.error')


if __name__ == '__main__':
    unittest.main()
