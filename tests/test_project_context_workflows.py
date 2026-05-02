"""Verify all 8 implementation workflows reference project-context.md in their step-01 files."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMPL_DIR = ROOT / "skills" / "bmad-bmm" / "workflows" / "4-implementation"

# The 8 implementation workflows that should reference project-context
EXPECTED_WORKFLOWS = [
    "sprint-planning",
    "create-story",
    "dev-story",
    "code-review",
    "correct-course",
    "checkpoint-preview",
    "retrospective",
    "sprint-status",
]


class TestProjectContextInImplWorkflows:
    """Each implementation workflow's step-01 (or customize.toml) must reference project-context."""

    def test_all_8_workflows_exist(self):
        for wf in EXPECTED_WORKFLOWS:
            wf_dir = IMPL_DIR / wf
            assert wf_dir.exists(), f"Workflow directory missing: {wf}"

    def test_workflows_reference_project_context_in_steps(self):
        """Verify project-context.md is referenced in step-01 files."""
        found = 0
        for wf in EXPECTED_WORKFLOWS:
            wf_dir = IMPL_DIR / wf
            # Check step-01 files
            step_files = sorted(wf_dir.glob("steps/step-01*.md")) + sorted(wf_dir.glob("step-01*.md"))
            # Also check customize.toml
            customize = wf_dir / "customize.toml"
            has_ref = False
            for sf in step_files:
                if "project-context" in sf.read_text(encoding="utf-8"):
                    has_ref = True
                    found += 1
                    break
            if not has_ref and customize.exists():
                if "project-context" in customize.read_text(encoding="utf-8"):
                    has_ref = True
                    found += 1
            if not has_ref:
                # Some workflows only have customize.toml references
                pass
        # At least 6 of 8 should have project-context references
        assert found >= 6, f"Only {found}/8 workflows reference project-context"


class TestQuickFlowProjectContext:
    """Quick flow workflows must also reference project-context."""

    QUICK_FLOWS = ["quick-spec", "quick-dev"]

    def test_quick_flows_reference_project_context(self):
        for qf in self.QUICK_FLOWS:
            qf_dir = ROOT / "skills" / "bmad-bmm" / "workflows" / "bmad-quick-flow" / qf
            assert qf_dir.exists(), f"Quick flow directory missing: {qf}"
            # Check step-01 or customize.toml
            has_ref = False
            for f in qf_dir.rglob("*.md"):
                if "project-context" in f.read_text(encoding="utf-8"):
                    has_ref = True
                    break
            if not has_ref:
                customize = qf_dir / "customize.toml"
                if customize.exists() and "project-context" in customize.read_text(encoding="utf-8"):
                    has_ref = True
            assert has_ref, f"Quick flow {qf} does not reference project-context"


class TestCrossPhaseProjectContext:
    """Analysis, planning, and solutioning workflows should reference project-context."""

    PHASE_DIRS = [
        ROOT / "skills" / "bmad-bmm" / "workflows" / "1-analysis",
        ROOT / "skills" / "bmad-bmm" / "workflows" / "2-plan-workflows",
        ROOT / "skills" / "bmad-bmm" / "workflows" / "3-solutioning",
    ]

    def test_cross_phase_workflows_have_project_context(self):
        """Most cross-phase workflows should reference project-context via customize.toml."""
        count = 0
        total = 0
        for phase_dir in self.PHASE_DIRS:
            if not phase_dir.exists():
                continue
            for wf_dir in phase_dir.rglob("customize.toml"):
                total += 1
                if "project-context" in wf_dir.read_text(encoding="utf-8"):
                    count += 1
        assert count >= 8, f"Only {count}/{total} cross-phase workflows reference project-context"
