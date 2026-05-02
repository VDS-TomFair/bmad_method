"""Verify each BMM agent's customize.toml menu codes are valid and match expectations."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BMM_AGENTS_DIR = ROOT / "skills" / "bmad-bmm" / "agents"


def _read_customize(agent_name: str) -> str:
    path = BMM_AGENTS_DIR / agent_name / "customize.toml"
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _extract_menu_codes(content: str) -> list[str]:
    """Extract menu codes from customize.toml content."""
    return re.findall(r'code\s*=\s*"([A-Z]+)"', content)


class TestDevMenuCompleteness:
    """Amelia (bmad-dev) must have all 12 expected menus."""

    EXPECTED_CODES = {"DS", "QD", "QA", "CR", "SP", "CS", "ER", "SS", "VS", "CC", "CK", "QS"}

    def test_dev_has_12_menus(self):
        content = _read_customize("dev")
        codes = set(_extract_menu_codes(content))
        assert len(codes) == 12, f"Expected 12 menus, got {len(codes)}: {codes}"

    def test_dev_has_all_expected_codes(self):
        content = _read_customize("dev")
        codes = set(_extract_menu_codes(content))
        missing = self.EXPECTED_CODES - codes
        assert not missing, f"Missing menu codes: {missing}"

    def test_dev_name_is_amelia(self):
        content = _read_customize("dev")
        assert 'name = "Amelia"' in content, "Dev agent name should be Amelia"


class TestAnalystMenuCompleteness:
    """Mary (Analyst) menus should be present."""

    def test_analyst_has_customize(self):
        content = _read_customize("analyst")
        assert content, "Analyst customize.toml is missing or empty"


class TestPmMenuCompleteness:
    """John (PM) menus should be present."""

    def test_pm_has_customize(self):
        content = _read_customize("pm")
        assert content, "PM customize.toml is missing or empty"


class TestArchitectMenuCompleteness:
    """Winston (Architect) menus should be present."""

    def test_architect_has_customize(self):
        content = _read_customize("architect")
        assert content, "Architect customize.toml is missing or empty"


class TestTechWriterMenuHasUS:
    """Paige (Tech Writer) must have US (Update Standards) menu."""

    def test_tech_writer_has_us_menu(self):
        content = _read_customize("tech-writer")
        codes = _extract_menu_codes(content)
        assert "US" in codes, f"US menu code not found in tech-writer customize.toml. Found: {codes}"


class TestUxDesignerMenu:
    """Sally (UX Designer) menus should be present."""

    def test_ux_designer_has_customize(self):
        content = _read_customize("ux-designer")
        assert content, "UX Designer customize.toml is missing or empty"


class TestNoDeletedAgentsInCustomizes:
    """No customize.toml should reference fully-deleted skills."""

    # Only bmad-sm was fully removed; bmad-qa-generate-e2e-tests and bmad-quick-dev
    # are still valid skills consolidated into bmad-bmm workflows.
    DELETED_SKILLS = ["bmad-sm"]

    def test_no_deleted_skill_references(self):
        for agent_dir in BMM_AGENTS_DIR.iterdir():
            if not agent_dir.is_dir():
                continue
            customize = agent_dir / "customize.toml"
            if not customize.exists():
                continue
            content = customize.read_text(encoding="utf-8")
            for skill in self.DELETED_SKILLS:
                # Use word boundary to avoid false positives (e.g. bmad-qa matching bmad-qa-generate-e2e-tests)
                pattern = rf'\bskill\s*=\s*"{re.escape(skill)}"'
                assert not re.search(pattern, content), f"{agent_dir.name}/customize.toml references deleted skill '{skill}'"


class TestAllCustomizesHavePersistentFacts:
    """All BMM agent customizes should have persistent_facts with project-context."""

    def test_all_have_project_context_in_facts(self):
        for agent_dir in sorted(BMM_AGENTS_DIR.iterdir()):
            if not agent_dir.is_dir():
                continue
            customize = agent_dir / "customize.toml"
            if not customize.exists():
                continue
            content = customize.read_text(encoding="utf-8")
            assert "project-context.md" in content, \
                f"{agent_dir.name}/customize.toml missing project-context.md in persistent_facts"
