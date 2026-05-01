"""Phase F - resolve_customization.py tests (F-P1-5)."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'resolve_customization.py'


class TestScriptExists(unittest.TestCase):
    """resolve_customization.py must exist and be executable."""

    def test_script_file_exists(self):
        """Script must exist at scripts/resolve_customization.py."""
        self.assertTrue(SCRIPT.exists(), f'{SCRIPT} does not exist')

    def test_script_is_python(self):
        """Script must be a valid Python file."""
        text = SCRIPT.read_text()
        self.assertTrue(text.startswith('#!/usr/bin/env python3'),
                        'Script does not have python3 shebang')


class TestScriptHelp(unittest.TestCase):
    """Script must run with --help."""

    def test_help_runs_successfully(self):
        """python3 resolve_customization.py --help must exit 0."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--help'],
            capture_output=True, text=True, timeout=10
        )
        self.assertEqual(result.returncode, 0,
                         f'--help exited with {result.returncode}: {result.stderr}')
        self.assertIn('resolve_customization', result.stdout.lower())

    def test_help_describes_skill_arg(self):
        """--help must mention --skill argument."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--help'],
            capture_output=True, text=True, timeout=10
        )
        self.assertIn('--skill', result.stdout)


class TestScriptImports(unittest.TestCase):
    """Script internals must be importable."""

    @classmethod
    def setUpClass(cls):
        import importlib.util
        spec = importlib.util.spec_from_file_location('resolve_customization', SCRIPT)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_deep_merge_importable(self):
        """deep_merge function must be importable from the script."""
        self.assertTrue(hasattr(self.mod, 'deep_merge'),
                        'Script has no deep_merge function')

    def test_find_project_root_importable(self):
        """find_project_root function must be importable."""
        self.assertTrue(hasattr(self.mod, 'find_project_root'),
                        'Script has no find_project_root function')


class TestDeepMerge(unittest.TestCase):
    """deep_merge must correctly merge TOML structures."""

    @classmethod
    def setUpClass(cls):
        import importlib.util
        spec = importlib.util.spec_from_file_location('resolve_customization', SCRIPT)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_scalar_override(self):
        """Scalar values in override win."""
        result = self.mod.deep_merge({'a': 'base'}, {'a': 'override'})
        self.assertEqual(result['a'], 'override')

    def test_deep_table_merge(self):
        """Tables are deep-merged."""
        base = {'agent': {'name': 'bob', 'title': 'SM'}}
        override = {'agent': {'title': 'PM'}}
        result = self.mod.deep_merge(base, override)
        self.assertEqual(result['agent']['name'], 'bob')
        self.assertEqual(result['agent']['title'], 'PM')

    def test_array_append(self):
        """Non-keyed arrays are appended."""
        base = {'steps': ['a', 'b']}
        override = {'steps': ['c']}
        result = self.mod.deep_merge(base, override)
        self.assertEqual(result['steps'], ['a', 'b', 'c'])

    def test_empty_override_returns_base(self):
        """Empty override returns base unchanged."""
        base = {'x': 1}
        result = self.mod.deep_merge(base, {})
        self.assertEqual(result, base)


class TestA0PathConventions(unittest.TestCase):
    """Script must use A0 path conventions, not upstream paths."""

    def test_uses_a0proj_variable(self):
        """Script must reference $A0PROJ path pattern."""
        text = SCRIPT.read_text()
        self.assertIn('$A0PROJ', text,
                      'Script does not reference $A0PROJ convention')

    def test_has_a0_path_note(self):
        """Script docstring must mention A0 path convention."""
        text = SCRIPT.read_text()
        self.assertTrue(
            'A0 Path' in text or '$A0PROJ' in text,
            'Script does not mention A0 path convention in docstring'
        )
