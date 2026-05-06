"""BMAD State & Artifact Delivery Fixes — grep-based regression tests.

Verifies that all 8 workflow completion files use text_editor:patch
instead of cat> heredocs, and that celebration/verification guards are present.
"""

import subprocess
import pytest

PROJECT = "/a0/usr/projects/a0_bmad_method"

# The 8 Fix A target files
FIX_A_FILES = [
    f"{PROJECT}/skills/bmad-bmm/workflows/1-analysis/create-product-brief/steps/step-06-complete.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/2-plan-workflows/create-prd/steps-c/step-12-complete.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/3-solutioning/create-architecture/steps/step-08-complete.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/2-plan-workflows/create-ux-design/steps/step-14-complete.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/4-implementation/sprint-planning/checklist.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/4-implementation/dev-story/checklist.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-04-final-validation.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/bmad-quick-flow/quick-spec/workflow.md",
]

# Fix B2-B5 target files (display-only prefix)
FIX_B_DISPLAY_FILES = [
    f"{PROJECT}/skills/bmad-bmm/workflows/1-analysis/create-product-brief/steps/step-06-complete.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/2-plan-workflows/create-prd/steps-c/step-12-complete.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/3-solutioning/create-architecture/steps/step-08-complete.md",
    f"{PROJECT}/skills/bmad-bmm/workflows/3-solutioning/create-epics-and-stories/steps/step-04-final-validation.md",
]

# Fix C target file
FIX_C_FILE = f"{PROJECT}/agents/bmad-master/prompts/agent.system.main.communication_additions.md"

# Fix B1 target file
FIX_B1_FILE = f"{PROJECT}/prompts/bmad-agent-shared.md"


def _grep(pattern: str, path: str) -> int:
    """Return grep match count for pattern in file (basic regex)."""
    result = subprocess.run(
        ["grep", "-c", pattern, path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return 0
    return int(result.stdout.strip())


def _grep_extended(pattern: str, path: str) -> int:
    """Return grep match count using extended regex."""
    result = subprocess.run(
        ["grep", "-cE", pattern, path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return 0
    return int(result.stdout.strip())


def _grep_fixed(pattern: str, path: str) -> int:
    """Return grep match count using fixed string matching."""
    result = subprocess.run(
        ["grep", "-cF", pattern, path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return 0
    return int(result.stdout.strip())


# ============================================================
# Fix A: No cat> heredocs, text_editor:patch present, correct values
# ============================================================

@pytest.mark.parametrize("filepath", FIX_A_FILES, ids=[
    "step-06-complete", "step-12-complete", "step-08-complete", "step-14-complete",
    "sprint-planning", "dev-story", "step-04-final-validation", "quick-spec",
])
def test_fix_a_no_cat_heredocs(filepath):
    """No cat > STATEEOF heredocs remain in any workflow file."""
    assert _grep_fixed("cat >", filepath) == 0 or _grep_fixed("STATEEOF", filepath) == 0, \
        f"cat> heredoc still present in {filepath}"


@pytest.mark.parametrize("filepath", FIX_A_FILES, ids=[
    "step-06-complete", "step-12-complete", "step-08-complete", "step-14-complete",
    "sprint-planning", "dev-story", "step-04-final-validation", "quick-spec",
])
def test_fix_a_text_editor_patch_present(filepath):
    """text_editor:patch instructions present in all 8 files."""
    assert _grep_fixed("text_editor:patch", filepath) >= 1, f"text_editor:patch missing in {filepath}"


@pytest.mark.parametrize("filepath", FIX_A_FILES, ids=[
    "step-06-complete", "step-12-complete", "step-08-complete", "step-14-complete",
    "sprint-planning", "dev-story", "step-04-final-validation", "quick-spec",
])
def test_fix_a_persona_bmad_master(filepath):
    """Persona always set to BMad Master (Orchestrator) in all 8 files."""
    assert _grep_fixed("BMad Master (Orchestrator)", filepath) >= 1, \
        f"BMad Master persona missing in {filepath}"


@pytest.mark.parametrize("filepath", FIX_A_FILES, ids=[
    "step-06-complete", "step-12-complete", "step-08-complete", "step-14-complete",
    "sprint-planning", "dev-story", "step-04-final-validation", "quick-spec",
])
def test_fix_a_state_update_not_write(filepath):
    """Section header says 'State Update' not 'State Write'."""
    assert _grep_fixed("State Update (MANDATORY)", filepath) >= 1, \
        f"State Update header missing in {filepath}"
    assert _grep_fixed("State Write (MANDATORY)", filepath) == 0, \
        f"Old 'State Write' header still in {filepath}"


# Per-file Phase/Artifact checks using extended regex for .*

def test_fix_a1_step06_phase_artifact():
    f = FIX_A_FILES[0]
    assert _grep_extended("Phase.*2-planning", f) >= 1
    assert _grep_extended("Active Artifact.*product-brief.md", f) >= 1

def test_fix_a2_step12_phase_artifact():
    f = FIX_A_FILES[1]
    assert _grep_extended("Phase.*2-planning", f) >= 1
    assert _grep_extended("Active Artifact.*prd.md", f) >= 1

def test_fix_a3_step08_phase_artifact():
    f = FIX_A_FILES[2]
    assert _grep_extended("Phase.*3-solutioning", f) >= 1
    assert _grep_extended("Active Artifact.*architecture.md", f) >= 1

def test_fix_a4_step14_phase_artifact():
    f = FIX_A_FILES[3]
    assert _grep_extended("Phase.*3-solutioning", f) >= 1
    assert _grep_extended("Active Artifact.*ux-design-specification.md", f) >= 1

def test_fix_a5_sprint_planning_phase_artifact():
    f = FIX_A_FILES[4]
    assert _grep_extended("Phase.*4-implementation", f) >= 1
    assert _grep_extended("Active Artifact.*sprint-status.yaml", f) >= 1

def test_fix_a6_dev_story_phase_artifact():
    f = FIX_A_FILES[5]
    assert _grep_extended("Phase.*4-implementation", f) >= 1
    assert _grep_extended("Active Artifact.*story.md", f) >= 1

def test_fix_a7_step04_phase_artifact():
    f = FIX_A_FILES[6]
    assert _grep_extended("Phase.*4-implementation", f) >= 1
    assert _grep_extended("Active Artifact.*epics.md", f) >= 1

def test_fix_a8_quick_spec_phase_artifact():
    f = FIX_A_FILES[7]
    assert _grep_extended("Phase.*4-implementation", f) >= 1
    assert _grep_extended("Active Artifact.*quick-spec.md", f) >= 1


# ============================================================
# Fix A: No $(date literals
# ============================================================

@pytest.mark.parametrize("filepath", FIX_A_FILES, ids=[
    "step-06-complete", "step-12-complete", "step-08-complete", "step-14-complete",
    "sprint-planning", "dev-story", "step-04-final-validation", "quick-spec",
])
def test_fix_a_no_date_literals(filepath):
    """No $(date literals remain in any workflow file."""
    assert _grep_fixed("$(date", filepath) == 0, f"$(date literal still present in {filepath}"


# ============================================================
# Fix B: Celebration guards
# ============================================================

def test_fix_b1_global_celebration_guard():
    """bmad-agent-shared.md contains the global celebration guard rule."""
    assert _grep_fixed("Never write celebration/summary files", FIX_B1_FILE) >= 1


@pytest.mark.parametrize("filepath", FIX_B_DISPLAY_FILES, ids=[
    "step-06-complete", "step-12-complete", "step-08-complete", "step-04-final-validation",
])
def test_fix_b2_b5_display_only_prefix(filepath):
    """Display-only prefix present in 4 celebration/announcement files."""
    assert _grep_fixed("Display to user (do NOT write to any file)", filepath) >= 1


# ============================================================
# Fix C: Post-delegation verification
# ============================================================

def test_fix_c1_section_header():
    """communication_additions.md contains Post-Delegation Verification section."""
    assert _grep_fixed("Post-Delegation Verification (MANDATORY)", FIX_C_FILE) >= 1


def test_fix_c1_verify_state_integrity():
    assert _grep_fixed("Verify state integrity", FIX_C_FILE) >= 1

def test_fix_c1_verify_artifact_exists():
    assert _grep_fixed("Verify artifact exists", FIX_C_FILE) >= 1

def test_fix_c1_report_results():
    assert _grep_fixed("Report results to user", FIX_C_FILE) >= 1
