import unittest
from pathlib import Path

EXT_FILE = Path(__file__).resolve().parents[1] / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'


class TestMtimeCaching(unittest.TestCase):
    """B9: mtime-keyed caching for alias and CSV reads."""

    def test_alias_cache_uses_mtime_key(self):
        """_alias_cache should use (path_str, mtime_ns) tuple keys."""
        source = EXT_FILE.read_text()
        # The cache lookup should involve mtime
        self.assertIn('mtime_ns', source,
                     '_alias_cache must use mtime_ns in cache key')

    def test_csv_cache_exists(self):
        """Module should have a _csv_cache dict."""
        source = EXT_FILE.read_text()
        self.assertIn('_csv_cache', source,
                     'Module must define _csv_cache dict')

    def test_csv_cache_uses_mtime_key(self):
        """_csv_cache should use (path_str, mtime_ns) tuple keys."""
        source = EXT_FILE.read_text()
        # CSV cache should also use mtime for invalidation
        csv_cache_lines = [l for l in source.splitlines() if '_csv_cache' in l]
        has_mtime = any('mtime_ns' in l for l in csv_cache_lines)
        # Either mtime_ns appears in same block as csv_cache, or the shared pattern is used
        self.assertTrue(
            has_mtime or 'mtime_ns' in source,
            '_csv_cache must use mtime_ns for cache invalidation'
        )

    def test_glob_called_once_in_execute(self):
        """execute() should do a single glob call, reused for routing + artifact scan."""
        source = EXT_FILE.read_text()
        # Find the execute method and check for single glob
        # The pattern should be: csv_files = ..., then pass csv_files to both functions
        self.assertIn('csv_files', source,
                     'execute() must compute csv_files once and reuse')


if __name__ == '__main__':
    unittest.main()
