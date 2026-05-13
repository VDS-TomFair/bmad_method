"""Fix 3: Verify _scan_artifact_existence uses cached YAML reads.

_collect_routing_rows() uses _yaml_cache with mtime invalidation, but
_scan_artifact_existence() reads CSV via csv_path.read_text() directly,
bypassing the cache entirely. Every execute() call double-reads each CSV.
"""
import unittest
import re
from pathlib import Path

ROUTING_FILE = (
    Path(__file__).resolve().parents[1]
    / "extensions" / "python" / "message_loop_prompts_after"
    / "_80_bmad_routing_manifest.py"
)


def _extract_func_body(source: str, func_name: str) -> str:
    """Extract function body after docstring, up to next top-level def or class."""
    pattern = r'def\s+' + re.escape(func_name) + r'\s*\([^)]*\)[^:]*:\s*""".*?"""'
    match = re.search(pattern, source, re.DOTALL)
    if not match:
        return ""
    func_start = match.end()
    body_match = re.search(r'\nclass\s|\ndef\s', source[func_start:])
    if body_match:
        return source[func_start:func_start + body_match.start()]
    return source[func_start:]


class TestCSVCacheConsistency(unittest.TestCase):
    """RED: These tests must fail before the fix is applied."""

    def _get_source(self) -> str:
        return ROUTING_FILE.read_text()

    def test_cached_read_helper_exists(self):
        """A _read_yaml_cached() helper function must exist."""
        source = self._get_source()
        self.assertRegex(
            source,
            r'def\s+_read_yaml_cached\s*\(',
            "_read_yaml_cached() helper function not defined"
        )

    def test_scan_artifact_uses_cached_read(self):
        """_scan_artifact_existence must use _read_yaml_cached, not read_text directly."""
        func_body = _extract_func_body(self._get_source(), "_scan_artifact_existence")
        self.assertTrue(func_body, "_scan_artifact_existence not found")
        self.assertNotIn('.read_text(', func_body,
                          "_scan_artifact_existence still uses direct .read_text() instead of cache")
        self.assertIn('_read_yaml_cached(', func_body,
                       "_scan_artifact_existence must call _read_yaml_cached()")

    def test_collect_routing_rows_uses_cached_read(self):
        """_collect_routing_rows must also use _read_yaml_cached."""
        func_body = _extract_func_body(self._get_source(), "_collect_routing_rows")
        self.assertTrue(func_body, "_collect_routing_rows not found")
        self.assertNotIn('.read_text(', func_body,
                          "_collect_routing_rows still uses direct .read_text() instead of cache")
        self.assertIn('_read_yaml_cached(', func_body,
                       "_collect_routing_rows must call _read_yaml_cached()")


if __name__ == "__main__":
    unittest.main()
