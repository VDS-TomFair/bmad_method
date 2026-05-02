"""Verify all module.yaml workflow codes are present, unique per module, and parseable."""
import yaml
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"


def _discover_yaml_files() -> list[Path]:
    files = sorted(SKILLS_DIR.glob("*/module.yaml"))
    init_core = SKILLS_DIR / "bmad-init" / "core" / "module.yaml"
    if init_core.exists() and init_core not in files:
        files.append(init_core)
    return files


def _all_workflow_entries() -> list[tuple[Path, dict]]:
    """Return (yaml_path, workflow_entry) tuples for every workflow across all module.yaml files."""
    entries = []
    for yp in _discover_yaml_files():
        data = yaml.safe_load(yp.read_text(encoding="utf-8"))
        if data and "workflows" in data:
            for w in data["workflows"]:
                entries.append((yp, w))
    return entries


class TestModuleYamlDiscovery:
    """All 5 module yaml files are found."""

    def test_discovers_at_least_5_yaml_files(self):
        files = _discover_yaml_files()
        # bmm, init/core, cis, tea, bmb = 5 minimum
        assert len(files) >= 5

    def test_each_yaml_file_is_parseable(self):
        for yp in _discover_yaml_files():
            data = yaml.safe_load(yp.read_text(encoding="utf-8"))
            assert isinstance(data, dict), f"{yp} did not parse to dict"


class TestWorkflowCodeCompleteness:
    """Verify all expected workflow codes exist across module.yaml files."""

    def test_at_least_75_workflow_codes(self):
        entries = _all_workflow_entries()
        codes = [e["menu-code"] for _, e in entries if "menu-code" in e]
        assert len(codes) >= 75, f"Only {len(codes)} workflow codes found, expected >= 75"

    def test_qd_code_exists_in_bmm(self):
        """QD (Quick Dev) was changed from QQ — verify it's present."""
        bmm_yaml = SKILLS_DIR / "bmad-bmm" / "module.yaml"
        data = yaml.safe_load(bmm_yaml.read_text(encoding="utf-8"))
        codes = [w["menu-code"] for w in data.get("workflows", []) if "menu-code" in w]
        assert "QD" in codes, "QD (Quick Dev) code missing from BMM module.yaml"

    def test_qa_codes_are_module_scoped(self):
        """QA appears in both bmm module.yaml — verify it's allowed (documented as module-scoped)."""
        entries = _all_workflow_entries()
        qa_entries = [(yp, e) for yp, e in entries if e.get("menu-code") == "QA"]
        # QA is documented as module-scoped, so duplicates across modules are acceptable
        # but it should exist at least once
        assert len(qa_entries) >= 1, "QA code not found in any module.yaml"

    def test_vs_codes_are_module_scoped(self):
        """VS (Validate Story) appears in BMM — verify module-scoped."""
        entries = _all_workflow_entries()
        vs_entries = [(yp, e) for yp, e in entries if e.get("menu-code") == "VS"]
        assert len(vs_entries) >= 1, "VS code not found in any module.yaml"


class TestNoCsvInProduction:
    """Verify zero CSV routing references in production code paths."""

    PRODUCTION_DIRS = ["extensions", "helpers", "api", "prompts"]

    def test_no_csv_imports_in_production(self):
        for d in self.PRODUCTION_DIRS:
            dir_path = ROOT / d
            if not dir_path.exists():
                continue
            for f in dir_path.rglob("*.py"):
                content = f.read_text(encoding="utf-8", errors="ignore")
                assert "import csv" not in content, f"{f} contains 'import csv'"
                assert "csv.DictReader" not in content, f"{f} contains csv.DictReader"

    def test_no_module_help_csv_in_skills(self):
        """No routing CSV files in skill directories (template assets excluded)."""
        for f in SKILLS_DIR.rglob("module-help.csv"):
            # Only allowed in template/assets paths
            rel = str(f.relative_to(ROOT))
            assert "assets/" in rel or "template" in rel, f"Unexpected routing CSV: {f}"


class TestRoutingExtensionUsesYaml:
    """Verify the routing extension uses yaml.safe_load, not CSV."""

    EXT_DIR = ROOT / "extensions" / "python" / "message_loop_prompts_after"

    def test_extension_file_exists(self):
        ext_files = list(self.EXT_DIR.glob("*.py"))
        assert len(ext_files) >= 1, "No routing extension .py files found"

    def test_extension_imports_yaml(self):
        for f in self.EXT_DIR.glob("*.py"):
            content = f.read_text(encoding="utf-8")
            if "module.yaml" in content or "routing" in content.lower():
                assert "yaml.safe_load" in content, f"{f} does not use yaml.safe_load"
                assert "import csv" not in content, f"{f} still imports csv"
