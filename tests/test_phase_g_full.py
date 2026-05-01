"""Phase G: Comprehensive verification of all 10 agent prompt fixes."""
import unittest
import hashlib
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = PROJECT / "prompts"
AGENTS_DIR = PROJECT / "agents"
SHARED_PROMPT = PROMPTS_DIR / "bmad-agent-shared.md"
SHARED_SOLVING = PROMPTS_DIR / "bmad-agent-shared-solving.md"

INCLUDE_SHARED = '{{ include "bmad-agent-shared.md" }}'
INCLUDE_SOLVING = '{{ include "bmad-agent-shared-solving.md" }}'


def _get_all_agents():
    return sorted([d.name for d in AGENTS_DIR.iterdir()
                   if d.is_dir() and d.name.startswith("bmad-")
                   and d.name != "_shared"])


def _get_non_master_agents():
    return sorted([d.name for d in AGENTS_DIR.iterdir()
                   if d.is_dir() and d.name.startswith("bmad-")
                   and d.name not in ("_shared", "bmad-master")])


class TestGPSolvingInclude(unittest.TestCase):
    """G-P1-2: All 20 solving.md must use shared include."""

    def test_shared_solving_fragment_exists(self):
        self.assertTrue(SHARED_SOLVING.exists(),
                        f"Shared solving fragment not found at {SHARED_SOLVING}")

    def test_all_solving_md_use_include(self):
        for agent in _get_all_agents():
            solving = AGENTS_DIR / agent / "prompts" / "agent.system.main.solving.md"
            content = solving.read_text().strip()
            self.assertEqual(INCLUDE_SOLVING, content,
                             f"{agent} solving.md is not a clean include")

    def test_all_solving_md_identical(self):
        hashes = set()
        for agent in _get_all_agents():
            solving = AGENTS_DIR / agent / "prompts" / "agent.system.main.solving.md"
            h = hashlib.md5(solving.read_bytes()).hexdigest()
            hashes.add(h)
        self.assertEqual(len(hashes), 1,
                        f"Expected all identical, found {len(hashes)} variants")

    def test_no_high_agency_in_solving(self):
        for agent in _get_all_agents():
            solving = AGENTS_DIR / agent / "prompts" / "agent.system.main.solving.md"
            self.assertNotIn("high-agency", solving.read_text(),
                            f"{agent} solving.md still has high-agency")


class TestGPSolvingFragmentContent(unittest.TestCase):
    """Verify shared solving fragment content."""

    def test_has_follow_the_process(self):
        self.assertIn("FOLLOW THE PROCESS", SHARED_SOLVING.read_text())

    def test_has_process_driven(self):
        self.assertIn("PROCESS-DRIVEN", SHARED_SOLVING.read_text())

    def test_has_skill_loading(self):
        self.assertIn("Load the appropriate BMAD skill FIRST", SHARED_SOLVING.read_text())

    def test_has_sequential_execution(self):
        self.assertIn("sequentially", SHARED_SOLVING.read_text())


class TestGPSharedFragmentClarification(unittest.TestCase):
    """G-P0-3: Shared fragment must have process-aware Initial Clarification."""

    def test_has_initial_clarification(self):
        self.assertIn("## Initial Clarification", SHARED_PROMPT.read_text())

    def test_has_process_aware_phrase(self):
        content = SHARED_PROMPT.read_text()
        self.assertIn(
            "Clarification determines WHICH workflow step to START at, "
            "not WHETHER to follow the process", content)

    def test_no_escape_hatch(self):
        self.assertNotIn("begin autonomous work", SHARED_PROMPT.read_text(),
                         "Shared fragment still has escape hatch language")

    def test_has_always_follow_statement(self):
        self.assertIn("ALWAYS follow the step-by-step process", SHARED_PROMPT.read_text())


class TestGPMasterSpecifics(unittest.TestCase):
    """G-P0-5: Master specifics.md converted to ~29 lines with include."""

    def test_master_specifics_uses_include(self):
        spec = AGENTS_DIR / "bmad-master" / "prompts" / "agent.system.main.specifics.md"
        self.assertIn(INCLUDE_SHARED, spec.read_text())

    def test_master_specifics_line_count(self):
        spec = AGENTS_DIR / "bmad-master" / "prompts" / "agent.system.main.specifics.md"
        lines = spec.read_text().strip().split("\n")
        self.assertLessEqual(len(lines), 35,
                            f"Master specifics has {len(lines)} lines, expected ~29")

    def test_master_specifics_preserves_routing(self):
        spec = AGENTS_DIR / "bmad-master" / "prompts" / "agent.system.main.specifics.md"
        self.assertIn("module-help.csv", spec.read_text())

    def test_master_specifics_preserves_skill_table(self):
        spec = AGENTS_DIR / "bmad-master" / "prompts" / "agent.system.main.specifics.md"
        self.assertIn("Available BMAD skills", spec.read_text())

    def test_master_specifics_preserves_loading_protocol(self):
        spec = AGENTS_DIR / "bmad-master" / "prompts" / "agent.system.main.specifics.md"
        self.assertIn("Skill loading protocol", spec.read_text())


class TestGPSubordinateMode(unittest.TestCase):
    """G-P1-1: All 20 communication_additions.md must have Subordinate Mode Detection."""

    def test_all_have_subordinate_detection(self):
        for agent in _get_all_agents():
            comm = AGENTS_DIR / agent / "prompts" / "agent.system.main.communication_additions.md"
            self.assertIn("Subordinate Mode Detection", comm.read_text(),
                        f"{agent} missing Subordinate Mode Detection")

    def test_all_have_menu_suppression(self):
        for agent in _get_all_agents():
            comm = AGENTS_DIR / agent / "prompts" / "agent.system.main.communication_additions.md"
            self.assertIn("Do NOT display the menu in subordinate mode", comm.read_text(),
                        f"{agent} missing menu suppression directive")


class TestGPA0FrameworkIntegration(unittest.TestCase):
    """G-P2-1: BMB agent specifics must have A0 Framework Integration."""

    def test_workflow_builder_has_a0_integration(self):
        spec = AGENTS_DIR / "bmad-workflow-builder" / "prompts" / "agent.system.main.specifics.md"
        self.assertIn("A0 Framework Integration", spec.read_text())

    def test_agent_builder_has_a0_integration(self):
        spec = AGENTS_DIR / "bmad-agent-builder" / "prompts" / "agent.system.main.specifics.md"
        self.assertIn("A0 Framework Integration", spec.read_text())

    def test_module_builder_has_a0_integration(self):
        spec = AGENTS_DIR / "bmad-module-builder" / "prompts" / "agent.system.main.specifics.md"
        self.assertIn("A0 Framework Integration", spec.read_text())


class TestGPEdgeCases(unittest.TestCase):
    """Edge cases: no conflicts, no duplicates, master parity."""

    def test_no_inline_and_include_conflict(self):
        for agent in _get_all_agents():
            spec = AGENTS_DIR / agent / "prompts" / "agent.system.main.specifics.md"
            content = spec.read_text()
            has_include = INCLUDE_SHARED in content
            has_inline = "You are a PROCESS-DRIVEN agent" in content
            self.assertFalse(has_include and has_inline,
                           f"{agent} has both include and inline shared content")

    def test_no_duplicate_compliance_in_shared_fragment(self):
        self.assertNotIn("MANDATORY PROCESS COMPLIANCE", SHARED_PROMPT.read_text(),
                         "Shared fragment duplicates compliance from role.md")

    def test_master_has_same_solving_as_others(self):
        master = (AGENTS_DIR / "bmad-master" / "prompts" /
                  "agent.system.main.solving.md").read_text()
        other = (AGENTS_DIR / "bmad-workflow-builder" / "prompts" /
                 "agent.system.main.solving.md").read_text()
        self.assertEqual(master, other, "bmad-master solving.md differs from other agents")

    def test_master_has_compliance_section(self):
        role = AGENTS_DIR / "bmad-master" / "prompts" / "agent.system.main.role.md"
        self.assertIn("MANDATORY PROCESS COMPLIANCE", role.read_text())

    def test_master_compliance_before_persona(self):
        role = AGENTS_DIR / "bmad-master" / "prompts" / "agent.system.main.role.md"
        content = role.read_text()
        compliance_pos = content.find("## MANDATORY PROCESS COMPLIANCE")
        persona_pos = content.find("## BMAD Persona:")
        if persona_pos == -1:
            persona_pos = content.find("## BMAD Identity")
        self.assertLess(compliance_pos, persona_pos,
                       "bmad-master: compliance must be before persona")


class TestGPFailureAnalysis(unittest.TestCase):
    """G-P2-2: Failure analysis report should be updated."""

    def test_failure_analysis_exists(self):
        report = PROJECT / "docs" / "workflow-builder-failure-analysis.md"
        self.assertTrue(report.exists(), "Failure analysis report missing")

    def test_failure_analysis_mentions_solving_override(self):
        report = PROJECT / "docs" / "workflow-builder-failure-analysis.md"
        content = report.read_text().lower()
        self.assertTrue(
            "full override" in content or "clean override" in content,
            "Failure analysis does not mention solving.md full override")


if __name__ == "__main__":
    unittest.main()
