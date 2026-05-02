"""
Unit tests for _80_bmad_routing_manifest.py artifact-detection helpers.
Covers AC-07 requirements:
 - Alias resolution with valid config
 - Alias resolution with missing config (graceful degradation)
 - Phase completion detection when artifact exists
 - Phase completion detection when artifact missing
 - No exception raised when output-location is invalid path
"""

import yaml

import sys
import tempfile
import unittest
from pathlib import Path

# Allow importing from extension directly without Agent Zero runtime
# by stubbing out the extension base class before import.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Stub helpers so _80 import doesn't fail in unit-test context
import types

_helpers = types.ModuleType("helpers")
_helpers.files = types.ModuleType("helpers.files")
_helpers.projects = types.ModuleType("helpers.projects")
sys.modules.setdefault("helpers", _helpers)
sys.modules.setdefault("helpers.files", _helpers.files)
sys.modules.setdefault("helpers.projects", _helpers.projects)

# Stub Extension base class
_ext_mod = types.ModuleType("helpers.extension")
class _Extension:
    pass
_ext_mod.Extension = _Extension
sys.modules.setdefault("helpers.extension", _ext_mod)

# Stub agent module
_agent_mod = types.ModuleType("agent")
class _LoopData:
    pass
_agent_mod.LoopData = _LoopData
sys.modules.setdefault("agent", _agent_mod)

# Now import the helpers under test
from extensions.python.message_loop_prompts_after._80_bmad_routing_manifest import (
    _parse_alias_map,
    _resolve_dir,
    _scan_artifact_existence,
    _build_completed_phases_text,
    _alias_cache,
)
import extensions.python.message_loop_prompts_after._80_bmad_routing_manifest as _ext80


CONFIG_TEMPLATE = """## BMAD Configuration

### Path Conventions
| Alias | Resolved Path |
|---|---|
| `{{planning_artifacts}}` | {planning_artifacts_path} |
| `{{implementation_artifacts}}` | {implementation_artifacts_path} |
| `{{output_folder}}` | {output_folder_path} |
| `{{project-root}}` | {project_root_path} |
"""


class TestParseAliasMap(unittest.TestCase):
    """AC-07: alias resolution with valid / missing config."""

    def setUp(self):
        # Clear cache between tests
        _ext80._alias_cache.clear()

    def test_valid_config_parses_all_aliases(self):
        """AC-01, AC-06: valid config file returns correct alias → path mapping."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "01-bmad-config.md"
            cfg.write_text(
                CONFIG_TEMPLATE.format(
                    planning_artifacts_path="/proj/planning/",
                    implementation_artifacts_path="/proj/impl/",
                    output_folder_path="/proj/output/",
                    project_root_path="/proj/.a0proj/",
                )
            )
            alias_map = _parse_alias_map(cfg)

        self.assertEqual(alias_map["planning_artifacts"], "/proj/planning/")
        self.assertEqual(alias_map["implementation_artifacts"], "/proj/impl/")
        self.assertEqual(alias_map["output_folder"], "/proj/output/")
        self.assertEqual(alias_map["project-root"], "/proj/.a0proj/")

    def test_missing_config_returns_empty_dict(self):
        """AC-05: missing config file → empty dict, no exception."""
        result = _parse_alias_map(Path("/nonexistent/path/01-bmad-config.md"))
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})

    def test_result_is_cached(self):
        """AC-06: second call returns same object without re-reading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = Path(tmpdir) / "01-bmad-config.md"
            cfg.write_text(
                CONFIG_TEMPLATE.format(
                    planning_artifacts_path="/p/",
                    implementation_artifacts_path="/i/",
                    output_folder_path="/o/",
                    project_root_path="/r/",
                )
            )
            first = _parse_alias_map(cfg)
            second = _parse_alias_map(cfg)
        self.assertIs(first, second)  # same cached object


class TestResolveDir(unittest.TestCase):
    """AC-02, AC-05: output-location alias resolution."""

    def setUp(self):
        _ext80._alias_cache.clear()

    def test_resolves_known_alias(self):
        alias_map = {"planning_artifacts": "/proj/planning/"}
        result = _resolve_dir("planning_artifacts", alias_map)
        self.assertEqual(result, Path("/proj/planning/"))

    def test_unknown_alias_returns_none(self):
        """AC-05: unknown alias → None, no exception."""
        result = _resolve_dir("nonexistent_alias", {})
        self.assertIsNone(result)

    def test_pipe_separated_uses_first_segment(self):
        """Pipe-separated output-location uses first segment only."""
        alias_map = {"planning_artifacts": "/proj/planning/", "project_knowledge": "/proj/know/"}
        result = _resolve_dir("planning_artifacts|project_knowledge", alias_map)
        self.assertEqual(result, Path("/proj/planning/"))

    def test_empty_location_returns_none(self):
        result = _resolve_dir("", {"planning_artifacts": "/proj/planning/"})
        self.assertIsNone(result)


def _make_yaml_bytes(rows: list[dict]) -> bytes:
    """Helper — serialize list of workflow dicts to YAML bytes."""
    if not rows:
        return b""
    data = {"workflows": rows}
    return yaml.dump(data, default_flow_style=False).encode()


class TestScanArtifactExistence(unittest.TestCase):
    """AC-02, AC-03, AC-05: filesystem scanning and phase detection."""

    def setUp(self):
        _ext80._alias_cache.clear()

    def _make_yaml(self, tmpdir: str, rows: list[dict]) -> Path:
        skill_dir = Path(tmpdir) / "skills" / "bmad-bmm"
        skill_dir.mkdir(parents=True)
        p = skill_dir / "module.yaml"
        p.write_bytes(_make_yaml_bytes(rows))
        return p

    def test_artifact_found_marks_phase_complete(self):
        """AC-02, AC-03: existing artifact → phase True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            planning = Path(tmpdir) / "planning"
            planning.mkdir()
            (planning / "product-brief.md").touch()

            alias_map = {"planning_artifacts": str(planning)}
            yaml_path = self._make_yaml(tmpdir, [{
                "module": "bmm", "phase": "1-analysis", "required": True,
                "output-location": "planning_artifacts", "outputs": "product-brief*.md",
            }])

            result = _scan_artifact_existence([yaml_path], alias_map)

        self.assertTrue(result["1-analysis"][0])
        self.assertIn("product-brief.md", result["1-analysis"][1])

    def test_artifact_missing_marks_phase_false(self):
        """AC-02, AC-03: empty directory → phase False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            planning = Path(tmpdir) / "planning"
            planning.mkdir()
            # no files

            alias_map = {"planning_artifacts": str(planning)}
            yaml_path = self._make_yaml(tmpdir, [{
                "module": "bmm", "phase": "2-planning", "required": True,
                "output-location": "planning_artifacts", "outputs": "prd*.md",
            }])

            result = _scan_artifact_existence([yaml_path], alias_map)

        self.assertFalse(result["2-planning"][0])

    def test_invalid_path_no_exception(self):
        """AC-05: unresolvable alias → no exception, phase stays False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            alias_map = {}  # empty — alias will not resolve
            yaml_path = self._make_yaml(tmpdir, [{
                "module": "bmm", "phase": "1-analysis", "required": True,
                "output-location": "planning_artifacts", "outputs": "product-brief*.md",
            }])

            try:
                result = _scan_artifact_existence([yaml_path], alias_map)
            except Exception as exc:
                self.fail(f"_scan_artifact_existence raised unexpectedly: {exc}")

        self.assertFalse(result["1-analysis"][0])

    def test_non_required_rows_do_not_gate_phase(self):
        """AC-03: required=false rows are ignored for phase gating."""
        with tempfile.TemporaryDirectory() as tmpdir:
            planning = Path(tmpdir) / "planning"
            planning.mkdir()
            (planning / "brainstorm.md").touch()

            alias_map = {"planning_artifacts": str(planning)}
            yaml_path = self._make_yaml(tmpdir, [{
                "module": "bmm", "phase": "1-analysis", "required": False,
                "output-location": "planning_artifacts", "outputs": "brainstorm*.md",
            }])

            result = _scan_artifact_existence([yaml_path], alias_map)

        self.assertFalse(result["1-analysis"][0])  # not required → doesn't gate

    def test_all_four_phases_present_in_result(self):
        """AC-03: result always contains all 4 phase keys."""
        result = _scan_artifact_existence([], {})
        self.assertIn("1-analysis", result)
        self.assertIn("2-planning", result)
        self.assertIn("3-solutioning", result)
        self.assertIn("4-implementation", result)


class TestBuildCompletedPhasesText(unittest.TestCase):
    """AC-04: EXTRAS text formatting."""

    def test_header_present(self):
        phase_map = {
            "1-analysis": (True, "product-brief.md"),
            "2-planning": (False, "no required artifact found"),
            "3-solutioning": (False, "no required artifact found"),
            "4-implementation": (False, "no required artifact found"),
        }
        text = _build_completed_phases_text(phase_map)
        self.assertIn("## Completed Phases (filesystem scan)", text)

    def test_true_phase_shows_true(self):
        phase_map = {
            "1-analysis": (True, "product-brief.md"),
            "2-planning": (False, "no required artifact found"),
            "3-solutioning": (False, "no required artifact found"),
            "4-implementation": (False, "no required artifact found"),
        }
        text = _build_completed_phases_text(phase_map)
        self.assertIn("1-analysis: true", text)
        self.assertIn("product-brief.md", text)
        self.assertIn("2-planning: false", text)

    def test_all_false(self):
        phase_map = {
            "1-analysis": (False, "no required artifact found"),
            "2-planning": (False, "no required artifact found"),
            "3-solutioning": (False, "no required artifact found"),
            "4-implementation": (False, "no required artifact found"),
        }
        text = _build_completed_phases_text(phase_map)
        self.assertEqual(text.count("false"), 4)


if __name__ == "__main__":
    unittest.main()
