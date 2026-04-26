import subprocess
import tempfile
import unittest
from pathlib import Path

INIT_SH = Path(__file__).resolve().parents[1] / 'skills' / 'bmad-init' / 'scripts' / 'bmad-init.sh'


class TestBmadInitUserPrefs(unittest.TestCase):
    """B2: User prefs moved to bmad-user-prefs.promptinclude.md."""

    def test_source_no_user_settings_block_in_config_template(self):
        """01-bmad-config.md template should NOT contain User Settings block."""
        source = INIT_SH.read_text()
        self.assertNotIn('### User Settings', source,
                         'User Settings block should be removed from config template')

    def test_source_writes_user_prefs_file(self):
        """bmad-init.sh should write bmad-user-prefs.promptinclude.md."""
        source = INIT_SH.read_text()
        self.assertIn('bmad-user-prefs.promptinclude.md', source,
                      'Script must write bmad-user-prefs.promptinclude.md')

    def test_user_prefs_file_created_on_init(self):
        """Running bmad-init.sh should create the user prefs file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ['bash', str(INIT_SH), tmpdir],
                capture_output=True, text=True, timeout=30
            )
            self.assertEqual(result.returncode, 0, f'Init failed: {result.stderr}')
            prefs_file = Path(tmpdir) / '.a0proj' / 'instructions' / 'bmad-user-prefs.promptinclude.md'
            self.assertTrue(prefs_file.exists(),
                         f'{prefs_file} should exist after init')

    def test_user_prefs_no_clobber(self):
        """Re-running init should preserve existing user prefs (no-clobber)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # First init
            subprocess.run(['bash', str(INIT_SH), tmpdir], timeout=30)
            prefs_file = Path(tmpdir) / '.a0proj' / 'instructions' / 'bmad-user-prefs.promptinclude.md'
            # Edit the file
            prefs_file.write_text('# Custom user prefs\n- **User Name:** Alice\n')
            # Re-init
            subprocess.run(['bash', str(INIT_SH), tmpdir], timeout=30)
            content = prefs_file.read_text()
            self.assertIn('Alice', content,
                         'User prefs should be preserved on re-init (no-clobber)')


if __name__ == '__main__':
    unittest.main()
