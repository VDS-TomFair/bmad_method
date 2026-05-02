"""Edge case tests for VERIFY phase — read_state, routing, dashboard, init."""
import yaml  # yaml for module.yaml parsing
import csv  # csv still used elsewhere
import io
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from helpers.bmad_status_core import read_state


# ── read_state edge cases ──────────────────────────────────────────


class TestReadStateEdgeCases:
    """Edge cases for the shared read_state() parser."""

    def test_malformed_file_returns_unknown(self, tmp_path):
        """Completely malformed content returns phase='unknown'."""
        state = tmp_path / "state.md"
        state.write_text("this is not valid state content at all\njust random text\n")
        result = read_state(state)
        assert "phase" in result
        assert result["phase"] == "unknown"

    def test_empty_file_returns_unknown(self, tmp_path):
        """Empty file returns phase='unknown'."""
        state = tmp_path / "state.md"
        state.write_text("")
        result = read_state(state)
        assert isinstance(result, dict)
        assert result["phase"] == "unknown"

    def test_partial_state_only_phase(self, tmp_path):
        """State with Phase: idea returns phase='idea'."""
        state = tmp_path / "state.md"
        state.write_text("# BMAD State\n\nPhase: idea\n\n## Issues\n\nNone\n")
        result = read_state(state)
        assert result["phase"] == "idea"

    def test_nonexistent_file_returns_unknown(self):
        """Nonexistent file returns phase='unknown'."""
        result = read_state(Path("/nonexistent/path/state.md"))
        assert isinstance(result, dict)
        assert result["phase"] == "unknown"

    def test_uppercase_phase_normalized(self, tmp_path):
        """Phase in uppercase is normalized to lowercase."""
        state = tmp_path / "state.md"
        state.write_text("Phase: BUILD\n\nActive Artifact: test.md\n")
        result = read_state(state)
        assert result["phase"] == "build"

    def test_mixed_case_phase(self, tmp_path):
        """Mixed case phase is normalized."""
        state = tmp_path / "state.md"
        state.write_text("Phase: SpEc\n")
        result = read_state(state)
        assert result["phase"] == "spec"

    def test_phase_with_leading_dashes(self, tmp_path):
        """Phase prefixed with dashes (list-item style) is parsed."""
        state = tmp_path / "state.md"
        state.write_text("- Phase: build\n")
        result = read_state(state)
        assert result["phase"] == "build"

    def test_multiline_phase_extracts_first(self, tmp_path):
        """Multiple Phase: lines extract the first match."""
        state = tmp_path / "state.md"
        state.write_text("Phase: build\nPhase: spec\nPhase: idea\n")
        result = read_state(state)
        assert result["phase"] == "build"

    def test_artifact_parsed_correctly(self, tmp_path):
        """Active Artifact is parsed alongside phase."""
        state = tmp_path / "state.md"
        state.write_text("Phase: build\nActive Artifact: architecture.md\n")
        result = read_state(state)
        assert result["phase"] == "build"
        assert result["artifact"] == "architecture.md"

    def test_issues_extracted(self, tmp_path):
        """ARCH- and DEFECT- prefixed PENDING issues are extracted."""
        state = tmp_path / "state.md"
        state.write_text("Phase: build\n- ARCH-001 PENDING\n- DEFECT-003 PENDING\n")
        result = read_state(state)
        assert len(result["issues"]) == 2

    def test_no_issues_returns_empty_list(self, tmp_path):
        """No issues returns empty list."""
        state = tmp_path / "state.md"
        state.write_text("Phase: idea\n")
        result = read_state(state)
        assert result["issues"] == []


# ── Dashboard error handling ───────────────────────────────────────


class TestDashboardErrorEdgeCases:
    """Dashboard error display edge cases."""

    @pytest.fixture
    def dashboard_html(self):
        return (PROJECT_ROOT / "webui" / "bmad-dashboard.html").read_text()

    @pytest.fixture
    def dashboard_store(self):
        return (PROJECT_ROOT / "webui" / "bmad-dashboard-store.js").read_text()

    def test_no_raw_html_injection(self, dashboard_html):
        """Dashboard never uses x-html for error display."""
        assert "x-html" not in dashboard_html

    def test_store_error_initial_state_empty_string(self, dashboard_store):
        """Store initializes error as empty string."""
        assert 'error: ""' in dashboard_store

    def test_x_text_used_for_errors(self, dashboard_html):
        """Error display uses x-text, not x-html."""
        error_lines = [l for l in dashboard_html.split('\n') if 'error' in l.lower() and 'x-' in l]
        for line in error_lines:
            assert 'x-html' not in line, f"Found x-html in error line: {line}"


# ── bmad-init.sh edge cases ────────────────────────────────────────


class TestBmadInitEdgeCases:
    """bmad-init.sh with unusual inputs."""

    def test_no_hardcoded_project_path(self):
        """Source script has no hard-coded /a0/usr/projects/ paths."""
        script = (PROJECT_ROOT / "skills" / "bmad-init" / "scripts" / "bmad-init.sh").read_text()
        hardcoded = re.findall(r'/a0/usr/projects/[a-zA-Z0-9_-]+', script)
        assert len(hardcoded) == 0, f"Hard-coded project paths found: {hardcoded}"

    def test_bash_syntax_valid(self):
        """Script passes bash -n syntax check."""
        script = PROJECT_ROOT / "skills" / "bmad-init" / "scripts" / "bmad-init.sh"
        result = subprocess.run(
            ["bash", "-n", str(script)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"


# ── Routing extension edge cases ───────────────────────────────────


class TestRoutingEdgeCases:
    """Routing extension behavior at boundaries."""

    def test_routing_no_dual_read_fallback(self):
        """No old dual-read compatibility code remains."""
        routing = (PROJECT_ROOT / "extensions" / "python" / "message_loop_prompts_after" / "_80_bmad_routing_manifest.py").read_text()
        bad_patterns = [
            r"if.*display_name.*else.*agent_name",
            r"if.*menu_code.*else.*skill",
            r"fallback.*old.*schema",
        ]
        for pat in bad_patterns:
            assert not re.search(pat, routing, re.IGNORECASE), f"Found dual-read pattern: {pat}"


# ── Include directive edge cases ───────────────────────────────────


class TestIncludeDirectiveEdgeCases:
    """Verify {{ include }} directive consistency."""

    def test_all_non_master_agents_have_same_include(self):
        """All 19 non-master agents use identical include syntax."""
        agents_dir = PROJECT_ROOT / "agents"
        includes = []
        for agent_dir in sorted(agents_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name == "_shared":
                continue
            if agent_dir.name == "bmad-master":
                continue
            specifics = agent_dir / "prompts" / "agent.system.main.specifics.md"
            if specifics.exists():
                content = specifics.read_text()
                include_lines = [l for l in content.split("\n") if "bmad-agent-shared.md" in l]
                includes.append((agent_dir.name, include_lines))

        for name, lines in includes:
            assert len(lines) == 1, f"{name} has {len(lines)} include lines"

        unique_includes = set(tuple(lines) for _, lines in includes)
        assert len(unique_includes) == 1, "Inconsistent include directives across agents"

    def test_shared_fragment_exists_and_nonempty(self):
        """The shared fragment file exists and has content."""
        shared = PROJECT_ROOT / "prompts" / "bmad-agent-shared.md"
        assert shared.exists()
        assert len(shared.read_text().strip()) > 100



# -- YAML schema consistency ------------------------------------------------


class TestYAMLSchemaConsistency:
    """Verify all module.yaml files use consistent schema."""

    def test_all_yaml_files_parse(self):
        """All active module.yaml files parse as valid YAML with workflows."""
        import yaml
        yaml_files = list(PROJECT_ROOT.glob("skills/*/module.yaml"))
        assert len(yaml_files) >= 4, f"Expected at least 4 YAML files, found {len(yaml_files)}"
        for yaml_file in sorted(yaml_files):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
            assert isinstance(data, dict), f"{yaml_file.relative_to(PROJECT_ROOT)} must parse to dict"
            assert "workflows" in data, f"{yaml_file.relative_to(PROJECT_ROOT)} missing workflows key"

    def test_all_workflows_have_required_fields(self):
        """All workflows in all module.yaml files have key fields."""
        import yaml
        yaml_files = list(PROJECT_ROOT.glob("skills/*/module.yaml"))
        for yaml_file in sorted(yaml_files):
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
            for i, wf in enumerate(data.get("workflows", [])):
                assert "module" in wf, f"{yaml_file.name} wf[{i}] missing module"
                assert "display-name" in wf, f"{yaml_file.name} wf[{i}] missing display-name"
                assert "menu-code" in wf, f"{yaml_file.name} wf[{i}] missing menu-code"
