"""Fix 2: Verify dashboard store.js resets loading on BOTH success and error paths.

The refresh() method sets this.loading = true but only reset it in catch.
After first successful load, the refresh button stays disabled permanently.
"""
import unittest
import re
from pathlib import Path

STORE_JS = (
    Path(__file__).resolve().parents[1]
    / "webui" / "bmad-dashboard-store.js"
)


class TestLoadingStateReset(unittest.TestCase):
    """RED: These tests must fail before the fix is applied."""

    def _get_refresh_body(self) -> str:
        """Extract the body of the refresh() method."""
        source = STORE_JS.read_text()
        # Find refresh() { ... } — match balanced braces
        match = re.search(r'async\s+refresh\(\)\s*\{', source)
        self.assertIsNotNone(match, "refresh() method not found in store.js")
        start = match.end()
        depth = 1
        pos = start
        while depth > 0 and pos < len(source):
            if source[pos] == '{':
                depth += 1
            elif source[pos] == '}':
                depth -= 1
            pos += 1
        return source[start:pos - 1]

    def test_loading_reset_on_success_path(self):
        """this.loading = false must appear OUTSIDE the catch block (success path)."""
        body = self._get_refresh_body()
        # Find the catch block
        catch_match = re.search(r'\}\s*catch\s*\(', body)
        if catch_match:
            before_catch = body[:catch_match.start()]
            # this.loading = false must exist before the catch
            self.assertIn('this.loading = false', before_catch,
                          "this.loading = false missing from success path (before catch)")
        else:
            # No catch at all — loading reset must exist somewhere
            self.assertIn('this.loading = false', body,
                          "this.loading = false missing from refresh()")

    def test_loading_reset_on_error_path(self):
        """this.loading = false must also exist INSIDE the catch block."""
        body = self._get_refresh_body()
        catch_match = re.search(r'\}\s*catch\s*\([^)]*\)\s*\{', body)
        self.assertIsNotNone(catch_match, "No catch block found in refresh()")
        catch_start = catch_match.end()
        # Find end of catch block
        depth = 1
        pos = catch_start
        while depth > 0 and pos < len(body):
            if body[pos] == '{':
                depth += 1
            elif body[pos] == '}':
                depth -= 1
            pos += 1
        catch_body = body[catch_start:pos - 1]
        self.assertIn('this.loading = false', catch_body,
                      "this.loading = false missing from catch (error) path")

    def test_loading_set_true_at_start(self):
        """refresh() must set this.loading = true at the start."""
        body = self._get_refresh_body()
        # loading = true should be one of the first statements
        self.assertIn('this.loading = true', body,
                      "this.loading = true missing from refresh()")


if __name__ == "__main__":
    unittest.main()
