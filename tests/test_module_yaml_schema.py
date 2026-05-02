"""Module YAML schema validation — Bundle 1, Slice 1.1.

Validates that all module.yaml files follow the canonical A0-adapted schema
derived from the 13-column CSV format. Source: SPEC.md §1.1, §Migration Guide.
Upstream reference: .a0proj/upstream/BMAD-METHOD/src/bmm-skills/module.yaml

TDD: This test is written FIRST (RED). YAML files don't exist yet.
Running this test should FAIL until Slice 1.2 creates the YAML files.
"""
import unittest
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = PLUGIN_ROOT / "skills"

# Expected module.yaml locations (SPEC §1.2)
MODULE_YAML_FILES = {
    "bmad-init": SKILLS_DIR / "bmad-init" / "core" / "module.yaml",
    "bmad-bmm": SKILLS_DIR / "bmad-bmm" / "module.yaml",
    "bmad-tea": SKILLS_DIR / "bmad-tea" / "module.yaml",
    "bmad-cis": SKILLS_DIR / "bmad-cis" / "module.yaml",
    "bmad-bmb": SKILLS_DIR / "bmad-bmb" / "module.yaml",
}

# Expected workflow counts (from CSV row counts, SPEC §1.2)
EXPECTED_WORKFLOW_COUNTS = {
    "bmad-init": 11,
    "bmad-bmm": 32,
    "bmad-tea": 9,
    "bmad-cis": 6,
    "bmad-bmb": 19,
}

# Required top-level fields for each module.yaml
REQUIRED_TOP_FIELDS = ["code", "name", "workflows"]

# Required fields per workflow entry (from CSV 13-col schema, SPEC §Migration Guide)
REQUIRED_WORKFLOW_FIELDS = [
    "module",
    "skill",
    "display-name",
    "menu-code",
    "description",
    "action",
    "args",
    "phase",
    "required",
    "output-location",
    "outputs",
]

# Optional fields per workflow entry (present in CSV but often empty)
OPTIONAL_WORKFLOW_FIELDS = ["after", "before"]


class TestModuleYamlFilesExist(unittest.TestCase):
    """All 5 module.yaml files must exist at expected paths."""

    def test_all_module_yaml_files_exist(self):
        """Each module must have a module.yaml file."""
        for name, path in MODULE_YAML_FILES.items():
            self.assertTrue(
                path.exists(),
                f"module.yaml missing for {name}: expected at {path}",
            )


class TestModuleYamlParseable(unittest.TestCase):
    """All module.yaml files must parse with yaml.safe_load()."""

    def test_all_module_yaml_parse_with_safe_load(self):
        """yaml.safe_load() must succeed on every module.yaml."""
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                text = path.read_text(encoding="utf-8")
                data = yaml.safe_load(text)
                self.assertIsInstance(
                    data, dict,
                    f"{name}: yaml.safe_load must return dict, got {type(data).__name__}",
                )


class TestModuleYamlTopLevelSchema(unittest.TestCase):
    """Top-level fields: code, name, workflows must be present."""

    def test_required_top_fields_present(self):
        """Each module.yaml must have code, name, and workflows fields."""
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                for field in REQUIRED_TOP_FIELDS:
                    self.assertIn(
                        field, data,
                        f"{name}: missing required top-level field '{field}'",
                    )

    def test_code_matches_module_name(self):
        """The 'code' field must match the module's expected code."""
        expected_codes = {
            "bmad-init": "core",
            "bmad-bmm": "bmm",
            "bmad-tea": "tea",
            "bmad-cis": "cis",
            "bmad-bmb": "bmb",
        }
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    data["code"], expected_codes[name],
                    f"{name}: code field is '{data['code']}', expected '{expected_codes[name]}'",
                )

    def test_workflows_is_list(self):
        """The 'workflows' field must be a list."""
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                self.assertIsInstance(
                    data["workflows"], list,
                    f"{name}: 'workflows' must be a list, got {type(data['workflows']).__name__}",
                )


class TestModuleYamlWorkflowSchema(unittest.TestCase):
    """Each workflow entry must have required fields from CSV 13-col schema."""

    def test_workflow_count_matches_csv(self):
        """Number of workflow entries must match expected CSV row counts.
        Source: SPEC §1.2 acceptance criteria: 'Row counts match between CSV and YAML'
        """
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                workflows = data["workflows"]
                expected = EXPECTED_WORKFLOW_COUNTS[name]
                self.assertEqual(
                    len(workflows), expected,
                    f"{name}: expected {expected} workflows, got {len(workflows)}",
                )

    def test_required_workflow_fields_present(self):
        """Each workflow entry must have all required fields.
        Source: SPEC §Migration Guide — 13 CSV columns mapped to YAML fields.
        """
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                for i, wf in enumerate(data["workflows"]):
                    with self.subTest(workflow_index=i, menu_code=wf.get("menu-code", "?")):
                        for field in REQUIRED_WORKFLOW_FIELDS:
                            self.assertIn(
                                field, wf,
                                f"{name} workflow[{i}] '{wf.get('display-name', '?')}': "
                                f"missing required field '{field}'",
                            )

    def test_menu_codes_unique_per_module(self):
        """Menu codes must be unique within each module."""
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                codes = [wf["menu-code"] for wf in data["workflows"]]
                seen = set()
                dupes = []
                for code in codes:
                    if code in seen:
                        dupes.append(code)
                    seen.add(code)
                # Note: QA and VS are intentionally duplicated across BMM/BMB
                # (SPEC §4.5) but must be unique WITHIN a module
                self.assertEqual(
                    len(dupes), 0,
                    f"{name}: duplicate menu codes within module: {dupes}",
                )

    def test_phase_values_valid(self):
        """Phase values must be from the canonical set.
        Source: SPEC §1.3, routing extension PHASE_BUCKETS + 'anytime' + '0-learning'.
        """
        valid_phases = {
            "anytime",
            "0-learning",
            "1-analysis",
            "2-planning",
            "3-solutioning",
            "4-implementation",
        }
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                for i, wf in enumerate(data["workflows"]):
                    phase = wf.get("phase", "")
                    self.assertIn(
                        phase, valid_phases,
                        f"{name} workflow[{i}] '{wf.get('menu-code', '?')}': "
                        f"invalid phase '{phase}'",
                    )

    def test_required_field_is_boolean(self):
        """The 'required' field must be a boolean value."""
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                for i, wf in enumerate(data["workflows"]):
                    self.assertIsInstance(
                        wf["required"], bool,
                        f"{name} workflow[{i}] '{wf.get('menu-code', '?')}': "
                        f"'required' must be bool, got {type(wf['required']).__name__}",
                    )

    def test_skill_field_not_empty(self):
        """The 'skill' field (agent assignment) must not be empty.
        Source: Routing extension skips rows without agent_name.
        """
        for name, path in MODULE_YAML_FILES.items():
            with self.subTest(module=name):
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
                for i, wf in enumerate(data["workflows"]):
                    skill = wf.get("skill", "")
                    self.assertTrue(
                        skill.strip(),
                        f"{name} workflow[{i}] '{wf.get('menu-code', '?')}': "
                        f"'skill' must not be empty",
                    )


if __name__ == "__main__":
    unittest.main()
