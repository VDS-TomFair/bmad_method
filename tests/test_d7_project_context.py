import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / 'skills' / 'bmad-init' / 'scripts' / 'bmad-init.sh'


class TestD7ProjectContextStub(unittest.TestCase):
    """D7: bmad-init.sh must create project-context.md stub (no-clobber)."""

    def test_creates_project_context_md(self):
        """Init creates knowledge/main/project-context.md."""
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['bash', str(SCRIPT), tmp], check=True, capture_output=True, text=True)
            ctx = Path(tmp) / '.a0proj' / 'knowledge' / 'main' / 'project-context.md'
            self.assertTrue(ctx.exists(), f'project-context.md not created at {ctx}')

    def test_project_context_is_idempotent_no_clobber(self):
        """Second init does not overwrite existing project-context.md content."""
        with tempfile.TemporaryDirectory() as tmp:
            ctx = Path(tmp) / '.a0proj' / 'knowledge' / 'main' / 'project-context.md'
            # First init
            subprocess.run(['bash', str(SCRIPT), tmp], check=True, capture_output=True, text=True)
            # Write user content
            ctx.write_text('USER CONTENT HERE')
            # Second init
            subprocess.run(['bash', str(SCRIPT), tmp], check=True, capture_output=True, text=True)
            self.assertEqual(ctx.read_text(), 'USER CONTENT HERE',
                        'project-context.md was overwritten on re-init')

    def test_source_has_project_context_creation(self):
        """bmad-init.sh source contains project-context.md creation logic."""
        source = SCRIPT.read_text()
        self.assertIn('project-context.md', source)


if __name__ == '__main__':
    unittest.main()
