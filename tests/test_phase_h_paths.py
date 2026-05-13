"""Phase H - BMB Creation Path Fixes: config split and path verification tests."""
import pytest
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "skills" / "bmad-bmb" / "config.yaml"
INIT_SCRIPT = PROJECT_ROOT / "skills" / "bmad-init" / "scripts" / "bmad-init.sh"
BMB_DIR = PROJECT_ROOT / "skills" / "bmad-bmb"


class TestHP01ConfigSplit:
    """H-P0-1: Config split - bmb_creations_output_folder replaced with 3 paths."""

    def test_config_file_exists(self):
        assert CONFIG_PATH.is_file(), f"config.yaml not found at {CONFIG_PATH}"

    def test_config_is_valid_yaml(self):
        with open(CONFIG_PATH) as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)

    def test_new_staging_folder_defined(self):
        with open(CONFIG_PATH) as f:
            data = yaml.safe_load(f)
        assert "bmb_staging_folder" in data, "Missing bmb_staging_folder in config.yaml"
        assert "bmb-staging" in data["bmb_staging_folder"]

    def test_new_agents_output_defined(self):
        with open(CONFIG_PATH) as f:
            data = yaml.safe_load(f)
        assert "bmb_build_output_agents" in data, "Missing bmb_build_output_agents"
        assert data["bmb_build_output_agents"] == "{project-root}/agents"

    def test_new_skills_output_defined(self):
        with open(CONFIG_PATH) as f:
            data = yaml.safe_load(f)
        assert "bmb_build_output_skills" in data, "Missing bmb_build_output_skills"
        assert data["bmb_build_output_skills"] == "{project-root}/skills"

    def test_old_variable_removed_or_aliased(self):
        with open(CONFIG_PATH) as f:
            data = yaml.safe_load(f)
        if "bmb_creations_output_folder" in data:
            assert data["bmb_creations_output_folder"] == data["bmb_staging_folder"], \
                "Old bmb_creations_output_folder should alias to bmb_staging_folder for compat"


class TestHP02StepFilePaths:
    """H-P0-2: Step files must use new path variables, not old ones."""

    def _all_md_files(self):
        return list(BMB_DIR.rglob("*.md"))

    def test_agent_build_uses_new_paths(self):
        step_07 = BMB_DIR / "workflows" / "agent" / "steps-c" / "step-07-build-agent.md"
        if step_07.exists():
            content = step_07.read_text()
            assert "bmb_build_output_agents" in content, \
                "step-07-build-agent.md must reference bmb_build_output_agents"

    def test_workflow_completion_uses_new_paths(self):
        step_11 = BMB_DIR / "workflows" / "workflow" / "steps-c" / "step-11-completion.md"
        if step_11.exists():
            content = step_11.read_text()
            assert "bmb_build_output_skills" in content, \
                "step-11-completion.md must reference bmb_build_output_skills"

    def test_module_complete_uses_new_paths(self):
        step_07 = BMB_DIR / "workflows" / "module" / "steps-c" / "step-07-complete.md"
        if step_07.exists():
            content = step_07.read_text()
            assert "bmb_staging_folder" in content or "bmb_build_output_skills" in content, \
                "step-07-complete.md must reference new path variables"

    def test_staging_used_for_plans(self):
        discovery = BMB_DIR / "workflows" / "agent" / "steps-c" / "step-02-discovery.md"
        if discovery.exists():
            content = discovery.read_text()
            assert "bmb_staging_folder" in content, \
                "step-02-discovery.md must reference bmb_staging_folder for plan paths"

    def test_no_old_variable_in_step_files(self):
        violations = []
        for md_file in self._all_md_files():
            content = md_file.read_text()
            if "bmb_creations_output_folder" in content:
                violations.append(str(md_file.relative_to(PROJECT_ROOT)))
        assert violations == [], \
            f"Files still referencing bmb_creations_output_folder: {violations}"

    def test_no_bmb_creations_hardcoded_path(self):
        violations = []
        for md_file in self._all_md_files():
            content = md_file.read_text()
            if "bmb-creations" in content:
                violations.append(str(md_file.relative_to(PROJECT_ROOT)))
        assert violations == [], \
            f"Files still hardcoding bmb-creations: {violations}"


class TestHP12InitScript:
    """H-P1-2: Init script must create agents/ and skills/ dirs."""

    def test_init_script_exists(self):
        assert INIT_SCRIPT.is_file(), f"Init script not found at {INIT_SCRIPT}"

    def test_init_creates_agents_dir(self):
        content = INIT_SCRIPT.read_text()
        assert 'mkdir -p "$A0PROJ/agents"' in content, \
            "Init script must create .a0proj/agents/ directory"

    def test_init_creates_skills_dir(self):
        content = INIT_SCRIPT.read_text()
        assert 'mkdir -p "$A0PROJ/skills"' in content, \
            "Init script must create .a0proj/skills/ directory"


class TestHP21CelebrateSteps:
    """H-P2-1: Celebrate steps must show A0 auto-discovery guidance."""

    CELEBRATE_AGENT = BMB_DIR / "workflows" / "agent" / "steps-c" / "step-08-celebrate.md"
    CELEBRATE_EDIT = BMB_DIR / "workflows" / "agent" / "steps-e" / "e-09-celebrate.md"

    def test_agent_celebrate_no_npx_install(self):
        if self.CELEBRATE_AGENT.exists():
            content = self.CELEBRATE_AGENT.read_text()
            assert "npx bmad-method install" not in content, \
                "Celebrate step should not reference upstream npx install command"

    def test_edit_celebrate_no_npx_install(self):
        if self.CELEBRATE_EDIT.exists():
            content = self.CELEBRATE_EDIT.read_text()
            assert "npx bmad-method install" not in content, \
                "Edit celebrate step should not reference upstream npx install command"

    def test_agent_celebrate_mentions_a0_discovery(self):
        if self.CELEBRATE_AGENT.exists():
            content = self.CELEBRATE_AGENT.read_text()
            assert "auto-discover" in content.lower() or "project scope" in content.lower() or \
                   ".a0proj/agents" in content or "promote-agent" in content.lower(), \
                "Celebrate step should mention A0 auto-discovery or promote-agent"
