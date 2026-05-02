import unittest
from pathlib import Path
import yaml

CORE_YAML = Path(__file__).resolve().parents[1] / 'skills' / 'bmad-init' / 'core' / 'module.yaml'

REQUIRED_FIELDS = ['module', 'skill', 'display-name', 'menu-code', 'description', 'action', 'args', 'phase', 'after', 'before', 'required', 'output-location', 'outputs']


class TestC0CoreYAMLSchema(unittest.TestCase):
    """C0: bmad-init/core/module.yaml must use upstream schema."""

    def test_core_yaml_parses(self):
        """Core module.yaml must parse as valid YAML dict."""
        with open(CORE_YAML) as f:
            data = yaml.safe_load(f)
        self.assertIsInstance(data, dict, 'module.yaml must parse to a dict')
        self.assertIn('workflows', data, 'module.yaml must have top-level workflows key')

    def test_core_yaml_has_workflows_list(self):
        """Core module.yaml must have a workflows list."""
        with open(CORE_YAML) as f:
            data = yaml.safe_load(f)
        self.assertIsInstance(data['workflows'], list,
                     f'workflows must be a list, got {type(data["workflows"])}')
        self.assertGreater(len(data['workflows']), 0,
                     'workflows list must not be empty')

    def test_core_yaml_no_old_field_names(self):
        """Must NOT contain old-schema field names."""
        with open(CORE_YAML) as f:
            data = yaml.safe_load(f)
        old_fields = ['name', 'code', 'sequence', 'workflow-file', 'command', 'options']
        for wf in data['workflows']:
            for field in old_fields:
                self.assertNotIn(field, wf,
                             f'Old field "{field}" found in workflow: {wf}')

    def test_core_yaml_required_fields_present(self):
        """All workflows must have key required fields."""
        with open(CORE_YAML) as f:
            data = yaml.safe_load(f)
        for i, wf in enumerate(data['workflows']):
            self.assertIn('display-name', wf, f'workflow[{i}] missing display-name')
            self.assertIn('menu-code', wf, f'workflow[{i}] missing menu-code')
            self.assertIn('action', wf, f'workflow[{i}] missing action')
            self.assertIn('args', wf, f'workflow[{i}] missing args')


if __name__ == '__main__':
    unittest.main()
