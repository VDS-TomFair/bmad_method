"""Verify the 8-step activation sequence in bmad-agent-shared.md appears in correct order."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED_PROMPT = ROOT / "prompts" / "bmad-agent-shared.md"


def _read_shared_prompt() -> str:
    assert SHARED_PROMPT.exists(), f"Shared prompt not found at {SHARED_PROMPT}"
    return SHARED_PROMPT.read_text(encoding="utf-8")


class TestActivationSequenceExists:
    """The 8-step activation sequence exists in the shared prompt."""

    EXPECTED_STEPS = [
        "Step 1: Resolve Customization",
        "Step 2: Execute Prepend Steps",
        "Step 3: Review Project State",
        "Step 4: Review Project Config",
        "Step 5: Load Persistent Facts",
        "Step 5.5: Load Sidecar Memory",
        "Step 6: Greet as Persona",
        "Step 7: Execute Append Steps",
        "Step 8: Present Menu or Dispatch",
    ]

    def test_all_steps_present(self):
        content = _read_shared_prompt()
        for step in self.EXPECTED_STEPS:
            assert step in content, f"Missing activation step: '{step}'"

    def test_step_count_is_correct(self):
        content = _read_shared_prompt()
        # Find all ### Step N: headings
        steps = re.findall(r"### Step (\d+(?:\.\d+)?):", content)
        assert len(steps) >= 8, f"Expected at least 8 activation steps, found {len(steps)}: {steps}"


class TestActivationStepOrder:
    """Steps must appear in the correct sequence in the file."""

    def test_resolve_before_prepend(self):
        content = _read_shared_prompt()
        resolve_pos = content.find("Step 1: Resolve Customization")
        prepend_pos = content.find("Step 2: Execute Prepend Steps")
        assert resolve_pos < prepend_pos, "Step 1 (resolve) must precede Step 2 (prepend)"

    def test_prepend_before_state(self):
        content = _read_shared_prompt()
        prepend_pos = content.find("Step 2: Execute Prepend Steps")
        state_pos = content.find("Step 3: Review Project State")
        assert prepend_pos < state_pos, "Step 2 (prepend) must precede Step 3 (state)"

    def test_state_before_config(self):
        content = _read_shared_prompt()
        state_pos = content.find("Step 3: Review Project State")
        config_pos = content.find("Step 4: Review Project Config")
        assert state_pos < config_pos, "Step 3 (state) must precede Step 4 (config)"

    def test_config_before_facts(self):
        content = _read_shared_prompt()
        config_pos = content.find("Step 4: Review Project Config")
        facts_pos = content.find("Step 5: Load Persistent Facts")
        assert config_pos < facts_pos, "Step 4 (config) must precede Step 5 (facts)"

    def test_facts_before_sidecar(self):
        content = _read_shared_prompt()
        facts_pos = content.find("Step 5: Load Persistent Facts")
        sidecar_pos = content.find("Step 5.5: Load Sidecar Memory")
        assert facts_pos < sidecar_pos, "Step 5 (facts) must precede Step 5.5 (sidecar)"

    def test_sidecar_before_greet(self):
        content = _read_shared_prompt()
        sidecar_pos = content.find("Step 5.5: Load Sidecar Memory")
        greet_pos = content.find("Step 6: Greet as Persona")
        assert sidecar_pos < greet_pos, "Step 5.5 (sidecar) must precede Step 6 (greet)"

    def test_greet_before_append(self):
        content = _read_shared_prompt()
        greet_pos = content.find("Step 6: Greet as Persona")
        append_pos = content.find("Step 7: Execute Append Steps")
        assert greet_pos < append_pos, "Step 6 (greet) must precede Step 7 (append)"

    def test_append_before_menu(self):
        content = _read_shared_prompt()
        append_pos = content.find("Step 7: Execute Append Steps")
        menu_pos = content.find("Step 8: Present Menu or Dispatch")
        assert append_pos < menu_pos, "Step 7 (append) must precede Step 8 (menu)"


class TestSidecarInstructions:
    """Sidecar loading and writing instructions exist in the shared prompt."""

    def test_sidecar_loading_instructions(self):
        content = _read_shared_prompt()
        assert "sidecar" in content.lower(), "Sidecar not mentioned in shared prompt"
        assert "_bmad/_memory" in content, "Sidecar directory path not in shared prompt"

    def test_sidecar_writing_instructions(self):
        content = _read_shared_prompt()
        assert "memories.md" in content, "memories.md not referenced in shared prompt"
        assert "append" in content.lower(), "Sidecar append instructions missing"

    def test_sidecar_path_pattern(self):
        content = _read_shared_prompt()
        assert "{your-agent-name}-sidecar" in content or "{agent}-sidecar" in content, \
            "Agent-specific sidecar path pattern not found"


class TestResolveCustomizationReference:
    """The shared prompt must reference the resolve_customization script."""

    def test_resolve_script_referenced(self):
        content = _read_shared_prompt()
        assert "resolve_customization" in content, "resolve_customization.py not referenced in shared prompt"

    def test_resolve_script_exists(self):
        script = ROOT / "scripts" / "resolve_customization.py"
        assert script.exists(), f"resolve_customization.py not found at {script}"
