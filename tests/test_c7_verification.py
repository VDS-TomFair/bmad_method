import unittest
from pathlib import Path
import yaml

PROJECT = Path(__file__).resolve().parents[1]
SKILLS_DIR = PROJECT / 'skills'

REQUIRED_FIELDS = ['module', 'skill', 'display-name', 'menu-code', 'description', 'action', 'args', 'phase', 'after', 'before', 'required', 'output-location', 'outputs']


def _all_module_yaml_files() -> list[Path]:
    """Find all module.yaml files across skill modules."""
    files = sorted(SKILLS_DIR.glob('*/module.yaml'))
    # Also check bmad-init/core/module.yaml
    init_core = SKILLS_DIR / 'bmad-init' / 'core' / 'module.yaml'
    if init_core.exists() and init_core not in files:
        files.append(init_core)
    return files


def _all_skill_md_files() -> list[Path]:
    """Find all SKILL.md files across all skill modules."""
    return sorted(SKILLS_DIR.rglob('SKILL.md'))


class TestC7YAMLSchemaCoverage(unittest.TestCase):
    """C7: Verify ALL module.yaml files use the upstream schema."""

    def test_all_yaml_files_found(self):
        """Must find module.yaml files in all skill modules."""
        yaml_files = _all_module_yaml_files()
        module_names = set()
        for p in yaml_files:
            # Extract module name from path
            parts = p.relative_to(SKILLS_DIR).parts
            if len(parts) >= 2:
                module_names.add(parts[0])
            if len(parts) >= 3 and parts[1] == 'core':
                module_names.add('core')
        expected = {'bmad-init', 'bmad-bmm', 'bmad-cis', 'bmad-tea', 'bmad-bmb'}
        for name in expected:
            self.assertTrue(any(name in str(p) for p in yaml_files),
                        f'No module.yaml found for module: {name}')

    def test_all_yaml_files_parse(self):
        """Every module.yaml must parse cleanly with yaml.safe_load."""
        for yaml_path in _all_module_yaml_files():
            try:
                with open(yaml_path) as f:
                    data = yaml.safe_load(f)
                self.assertIsInstance(data, dict,
                            f'{yaml_path}: must parse to a dict')
            except Exception as e:
                self.fail(f'{yaml_path}: failed to parse: {e}')

    def test_all_yaml_have_workflows(self):
        """Every module.yaml must have a workflows list."""
        for yaml_path in _all_module_yaml_files():
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            self.assertIn('workflows', data,
                        f'{yaml_path}: missing top-level "workflows" key')
            self.assertIsInstance(data['workflows'], list,
                        f'{yaml_path}: workflows must be a list')

    def test_all_workflows_have_required_fields(self):
        """All workflows must have key fields: display-name, menu-code, action, skill."""
        for yaml_path in _all_module_yaml_files():
            with open(yaml_path) as f:
                data = yaml.safe_load(f)
            for i, wf in enumerate(data.get('workflows', [])):
                self.assertIn('display-name', wf,
                            f'{yaml_path} workflow[{i}]: missing display-name')
                self.assertIn('menu-code', wf,
                            f'{yaml_path} workflow[{i}]: missing menu-code')
                self.assertIn('action', wf,
                            f'{yaml_path} workflow[{i}]: missing action')
                self.assertIn('skill', wf,
                            f'{yaml_path} workflow[{i}]: missing skill')


class TestC7TriggerPatternCoverage(unittest.TestCase):
    """C7: Verify comprehensive trigger_patterns coverage across all SKILL.md files."""

    def test_all_skill_md_files_have_trigger_patterns(self):
        """Every SKILL.md must have trigger_patterns in its YAML frontmatter."""
        failures = []
        for path in _all_skill_md_files():
            content = path.read_text()
            if 'trigger_patterns:' not in content:
                rel = path.relative_to(PROJECT)
                failures.append(str(rel))
        self.assertEqual(failures, [],
                    f'{len(failures)} SKILL.md files missing trigger_patterns: {failures}')

    def test_trigger_patterns_contain_slash_commands(self):
        """Every SKILL.md with trigger_patterns must have at least one slash command."""
        failures = []
        for path in _all_skill_md_files():
            content = path.read_text()
            if 'trigger_patterns:' not in content:
                continue
            lines = content.splitlines()
            in_triggers = False
            has_slash = False
            for line in lines:
                if 'trigger_patterns:' in line:
                    in_triggers = True
                    continue
                if in_triggers:
                    if line.strip().startswith('- /'):
                        has_slash = True
                        break
                    if not line.startswith(' '):
                        break
            if not has_slash:
                rel = path.relative_to(PROJECT)
                failures.append(str(rel))
        self.assertEqual(failures, [],
                    f'{len(failures)} SKILL.md files missing slash commands: {failures}')

    def test_skill_md_count(self):
        """Verify minimum expected number of SKILL.md files with trigger_patterns."""
        all_skills = _all_skill_md_files()
        self.assertGreaterEqual(len(all_skills), 50,
                    f'Expected at least 50 SKILL.md files, found {len(all_skills)}')


class TestC7RoutingExtensionHealth(unittest.TestCase):
    """C7: Verify routing extension is healthy after YAML migration."""

    def test_routing_ext_imports(self):
        """Routing extension must import cleanly with yaml."""
        ext_file = PROJECT / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'
        source = ext_file.read_text()
        self.assertIn('import yaml', source)
        self.assertIn('import logging', source)
        self.assertIn('from pathlib import Path', source)

    def test_routing_ext_no_dual_read(self):
        """Routing extension must NOT have dual-read compatibility code."""
        ext_file = PROJECT / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'
        source = ext_file.read_text()
        self.assertNotIn('or wf.get("name"', source)
        self.assertNotIn('or wf.get("code"', source)
        self.assertNotIn('or wf.get("agent-name"', source)

    def test_routing_ext_uses_new_fields(self):
        """Routing extension must use YAML field names directly."""
        ext_file = PROJECT / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'
        source = ext_file.read_text()
        self.assertIn('wf.get("display-name"', source)
        self.assertIn('wf.get("menu-code"', source)


if __name__ == '__main__':
    unittest.main()
