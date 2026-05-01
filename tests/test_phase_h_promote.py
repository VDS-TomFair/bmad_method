"""Phase H - Promote skill tests: NAME validation, TYPE routing, error handling."""
import subprocess
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMOTE_SCRIPT = PROJECT_ROOT / "skills" / "bmad-promote" / "scripts" / "promote.sh"
PLUGIN_DIR = Path("/a0/usr/plugins/bmad_method")


def _run_promote(type_arg: str, name_arg: str, project_root: str = "/tmp/test-promote",
                 force: bool = False) -> subprocess.CompletedProcess:
    """Run promote.sh with given args and return CompletedProcess."""
    env = {"PROMOTE_FORCE": "true"} if force else {"PROMOTE_FORCE": "false"}
    return subprocess.run(
        ["bash", str(PROMOTE_SCRIPT), type_arg, name_arg, project_root],
        capture_output=True, text=True, env={**_env(), **env},
    )


def _env() -> dict:
    import os
    return dict(os.environ)


class TestPromoteNameValidation:
    """NAME parameter must reject path traversal attempts."""

    def test_reject_slash_in_name(self):
        result = _run_promote("agent", "evil/path")
        assert result.returncode == 1
        assert "Invalid name" in result.stdout
        assert "'/'" in result.stdout

    def test_reject_double_dot_in_name(self):
        result = _run_promote("agent", "..evil")
        assert result.returncode == 1
        assert "Invalid name" in result.stdout
        assert "'..'" in result.stdout

    def test_reject_path_traversal_attack(self):
        result = _run_promote("agent", "../../etc/passwd")
        assert result.returncode == 1
        assert "Invalid name" in result.stdout

    def test_reject_leading_hyphen(self):
        result = _run_promote("agent", "-flag-like")
        assert result.returncode == 1
        assert "Invalid name" in result.stdout
        assert "start with '-'" in result.stdout

    def test_accept_valid_name(self):
        """Valid names should pass NAME validation (may fail later on source missing)."""
        result = _run_promote("agent", "my-valid-agent")
        # Should NOT fail with "Invalid name" - may fail with source not found (exit 2)
        if result.returncode != 0:
            assert "Invalid name" not in result.stdout

    def test_accept_name_with_dots(self):
        """Names with dots (but not ..) should be allowed."""
        result = _run_promote("agent", "my.agent.v2")
        if result.returncode != 0:
            assert "Invalid name" not in result.stdout


class TestPromoteTypeValidation:
    """TYPE parameter must accept agent, workflow, skill; reject invalid."""

    def test_reject_invalid_type(self):
        result = _run_promote("invalid", "somename")
        assert result.returncode == 1
        assert "Invalid type" in result.stdout

    def test_agent_type_routes_to_agents(self):
        """agent type should look in .a0proj/agents/ subdir."""
        result = _run_promote("agent", "nonexistent")
        # Should fail with source not found, path should contain 'agents'
        assert result.returncode == 2
        assert "/agents/" in result.stdout

    def test_workflow_type_routes_to_skills(self):
        """workflow type should look in .a0proj/skills/ subdir."""
        result = _run_promote("workflow", "nonexistent")
        assert result.returncode == 2
        assert "/skills/" in result.stdout

    def test_skill_type_routes_to_skills(self):
        """skill type should look in .a0proj/skills/ subdir (same as workflow)."""
        result = _run_promote("skill", "nonexistent")
        assert result.returncode == 2
        assert "/skills/" in result.stdout


class TestPromoteErrorHandling:
    """Promote script error handling and exit codes."""

    def test_missing_args_returns_usage(self):
        result = subprocess.run(
            ["bash", str(PROMOTE_SCRIPT)],
            capture_output=True, text=True,
        )
        assert result.returncode == 1
        assert "Usage" in result.stdout

    def test_source_not_found_exit_2(self):
        result = _run_promote("agent", "nonexistent-agent")
        assert result.returncode == 2
        assert "does not exist" in result.stdout

    def test_promote_script_exists(self):
        assert PROMOTE_SCRIPT.is_file(), f"promote.sh not found at {PROMOTE_SCRIPT}"

    def test_promote_script_syntax_valid(self):
        """Script should pass bash syntax check."""
        result = subprocess.run(
            ["bash", "-n", str(PROMOTE_SCRIPT)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, f"Syntax error: {result.stderr}"


class TestPromoteSkillTrigger:
    """Verify SKILL.md includes /promote-skill trigger."""

    SKILL_MD = PROJECT_ROOT / "skills" / "bmad-promote" / "SKILL.md"

    def test_skill_md_has_promote_skill_trigger(self):
        content = self.SKILL_MD.read_text()
        assert "/promote-skill" in content, "SKILL.md must include /promote-skill trigger"

    def test_skill_md_has_promote_skill_description(self):
        content = self.SKILL_MD.read_text()
        assert "promote skill" in content.lower(), "SKILL.md must mention 'promote skill' in description"

    def test_skill_md_has_skill_command_section(self):
        content = self.SKILL_MD.read_text()
        assert "### `/promote-skill" in content, "SKILL.md must have /promote-skill command section"
