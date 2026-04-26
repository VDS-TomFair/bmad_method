import subprocess
import tempfile
import unittest
from pathlib import Path

INIT_SH = Path(__file__).resolve().parents[1] / 'skills' / 'bmad-init' / 'scripts' / 'bmad-init.sh'


class TestBmadInitBashHardening(unittest.TestCase):
    """B6: Full bash hardening of bmad-init.sh."""

    def test_rsync_or_fallback_pattern(self):
        """Seed copy should try rsync first, fallback to cp -Rn."""
        source = INIT_SH.read_text()
        # Should have rsync command or fallback pattern
        has_rsync = 'rsync' in source
        has_cp_fallback = 'cp -R' in source or 'cp -rn' in source
        self.assertTrue(has_rsync or has_cp_fallback,
                     'Seed copy must use rsync or cp fallback')

    def test_warnings_to_stderr(self):
        """All warning messages should go to stderr (>&2)."""
        source = INIT_SH.read_text()
        for line in source.splitlines():
            if 'Warning' in line and 'echo' in line:
                self.assertIn('>&2', line,
                             f'Warning line must redirect to stderr: {line.strip()}')

    def test_bash_n_syntax_check(self):
        """bash -n syntax check must pass."""
        result = subprocess.run(
            ['bash', '-n', str(INIT_SH)],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0,
                     f'bash -n failed: {result.stderr}')

    def test_set_euo_pipefail(self):
        """Script must have set -euo pipefail."""
        source = INIT_SH.read_text()
        self.assertIn('set -euo pipefail', source)


if __name__ == '__main__':
    unittest.main()
