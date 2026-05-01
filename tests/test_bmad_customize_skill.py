"""Phase F - bmad-customize skill tests (F-P1-6)."""
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / 'skills' / 'bmad-customize'
SKILL_MD = SKILL_DIR / 'SKILL.md'
LIST_SCRIPT = SKILL_DIR / 'scripts' / 'list_customizable_skills.py'


class TestSkillMd(unittest.TestCase):
    """SKILL.md must have proper frontmatter."""

    def setUp(self):
        self.text = SKILL_MD.read_text()

    def test_skill_md_exists(self):
        """SKILL.md must exist."""
        self.assertTrue(SKILL_MD.exists(), 'bmad-customize SKILL.md not found')

    def test_has_name_field(self):
        """Frontmatter must have name: bmad-customize."""
        self.assertIn('name: bmad-customize', self.text,
                      'SKILL.md missing name: bmad-customize')

    def test_has_description_field(self):
        """Frontmatter must have description field."""
        self.assertIn('description:', self.text,
                      'SKILL.md missing description field')

    def test_has_trigger_patterns(self):
        """Frontmatter must have trigger_patterns."""
        self.assertIn('trigger_patterns:', self.text,
                      'SKILL.md missing trigger_patterns')

    def test_trigger_patterns_include_customize(self):
        """Trigger patterns must include /customize."""
        self.assertIn('/customize', self.text,
                      'SKILL.md missing /customize trigger')


class TestListCustomizableSkills(unittest.TestCase):
    """list_customizable_skills.py must run and produce valid output."""

    def test_script_exists(self):
        """list_customizable_skills.py must exist."""
        self.assertTrue(LIST_SCRIPT.exists(),
                        'list_customizable_skills.py not found')

    def test_script_runs(self):
        """Script must run without error on a temp directory."""
        result = subprocess.run(
            [sys.executable, str(LIST_SCRIPT), '--project-root', '/tmp/test-bmad'],
            capture_output=True, text=True, timeout=15
        )
        self.assertEqual(result.returncode, 0,
                         f'Script failed: {result.stderr}')

    def test_script_produces_json(self):
        """Output must be valid JSON with agents and workflows keys."""
        result = subprocess.run(
            [sys.executable, str(LIST_SCRIPT), '--project-root', '/tmp/test-bmad'],
            capture_output=True, text=True, timeout=15
        )
        data = json.loads(result.stdout)
        self.assertIn('agents', data)
        self.assertIn('workflows', data)


class TestCustomizeTomlFiles(unittest.TestCase):
    """customize.toml files must be valid TOML with proper sections."""

    @classmethod
    def setUpClass(cls):
        cls.toml_files = list(ROOT.glob('skills/**/customize.toml'))

    def test_at_least_25_customize_toml_files(self):
        """Must have ~30 customize.toml files (at least 25)."""
        self.assertGreaterEqual(len(self.toml_files), 25,
                                f'Found only {len(self.toml_files)} customize.toml files')

    def test_all_toml_files_parseable(self):
        """Every customize.toml must be valid TOML."""
        import tomllib
        for toml_file in self.toml_files:
            with self.subTest(file=str(toml_file.relative_to(ROOT))):
                with toml_file.open('rb') as f:
                    data = tomllib.load(f)
                self.assertIsInstance(data, dict)

    def test_all_toml_files_have_agent_or_workflow_section(self):
        """Every customize.toml must have [agent] or [workflow] section."""
        import tomllib
        for toml_file in self.toml_files:
            with self.subTest(file=str(toml_file.relative_to(ROOT))):
                with toml_file.open('rb') as f:
                    data = tomllib.load(f)
                self.assertTrue(
                    'agent' in data or 'workflow' in data,
                    f'{toml_file.name} has neither [agent] nor [workflow] section'
                )
