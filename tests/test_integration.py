import unittest
import subprocess
import tempfile
import os
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
INIT_SCRIPT = BASE / 'skills' / 'bmad-init' / 'scripts' / 'bmad-init.sh'


class TestInitScriptIntegration(unittest.TestCase):
    """Integration test: bmad-init.sh creates expected directory structure."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='bmad_test_')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_init_creates_bmad_custom_dir(self):
        """Init script must create _bmad/custom/ directory."""
        result = subprocess.run(
            ['bash', str(INIT_SCRIPT), self.tmpdir],
            capture_output=True, text=True, timeout=30
        )
        self.assertEqual(result.returncode, 0,
                         f'Init failed: {result.stderr}')
        custom_dir = Path(self.tmpdir) / '.a0proj' / '_bmad' / 'custom'
        self.assertTrue(custom_dir.exists(),
                        f'_bmad/custom/ directory not created')

    def test_init_creates_all_standard_dirs(self):
        """Init script must create all expected directories."""
        result = subprocess.run(
            ['bash', str(INIT_SCRIPT), self.tmpdir],
            capture_output=True, text=True, timeout=30
        )
        self.assertEqual(result.returncode, 0)
        a0proj = Path(self.tmpdir) / '.a0proj'
        expected_dirs = [
            '_bmad-output/planning-artifacts/research',
            '_bmad-output/implementation-artifacts',
            '_bmad-output/test-artifacts',
            'knowledge/main',
            'knowledge/fragments',
            'knowledge/solutions',
            'instructions',
            'agents',
            'skills',
            '_bmad/custom',
        ]
        for d in expected_dirs:
            full = a0proj / d
            self.assertTrue(full.exists(),
                            f'Expected directory {d} not found')

    def test_init_creates_config_files(self):
        """Init script must create config and state files."""
        result = subprocess.run(
            ['bash', str(INIT_SCRIPT), self.tmpdir],
            capture_output=True, text=True, timeout=30
        )
        self.assertEqual(result.returncode, 0)
        a0proj = Path(self.tmpdir) / '.a0proj'
        self.assertTrue((a0proj / 'instructions' / '01-bmad-config.md').exists())
        self.assertTrue((a0proj / 'instructions' / '02-bmad-state.md').exists())
        self.assertTrue((a0proj / 'instructions' / 'bmad-user-prefs.promptinclude.md').exists())

    def test_init_idempotent(self):
        """Running init twice should not fail or overwrite config."""
        subprocess.run(
            ['bash', str(INIT_SCRIPT), self.tmpdir],
            capture_output=True, text=True, timeout=30
        )
        # Read first config
        config1 = (Path(self.tmpdir) / '.a0proj' / 'instructions' / '01-bmad-config.md').read_text()
        # Run again
        result = subprocess.run(
            ['bash', str(INIT_SCRIPT), self.tmpdir],
            capture_output=True, text=True, timeout=30
        )
        self.assertEqual(result.returncode, 0)
        config2 = (Path(self.tmpdir) / '.a0proj' / 'instructions' / '01-bmad-config.md').read_text()
        self.assertEqual(config1, config2, 'Config should not change on re-init')


class TestYAMLRoutingIntegration(unittest.TestCase):
    """Integration: Verify routing manifest generates from YAML correctly."""

    def test_all_module_yamls_parse(self):
        """All module.yaml files must parse as valid YAML."""
        import yaml
        module_dirs = ['bmad-bmm', 'bmad-bmb', 'bmad-tea', 'bmad-cis']
        for module in module_dirs:
            path = BASE / 'skills' / module / 'module.yaml'
            if path.exists():
                with open(path) as f:
                    data = yaml.safe_load(f)
                self.assertIsInstance(data, dict, f'{module}/module.yaml must be a dict')
                self.assertIn('workflows', data, f'{module}/module.yaml must have workflows')

    def test_core_module_yaml_parses(self):
        """Core module.yaml must parse as valid YAML."""
        import yaml
        path = BASE / 'skills' / 'bmad-init' / 'core' / 'module.yaml'
        with open(path) as f:
            data = yaml.safe_load(f)
        self.assertIsInstance(data, dict)
        self.assertIn('workflows', data)


if __name__ == '__main__':
    unittest.main()
