import pytest
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_PROMPT_PATH = os.path.join(PROJECT_ROOT, 'prompts', 'bmad-agent-shared.md')

@pytest.fixture
def shared_prompt():
    with open(SHARED_PROMPT_PATH, 'r') as f:
        return f.read()

class TestActivationSequence:
    """Verify 8-step activation sequence exists in shared prompt."""
    
    def test_file_exists(self):
        assert os.path.isfile(SHARED_PROMPT_PATH)
    
    def test_activation_protocol_header(self, shared_prompt):
        assert '## BMAD Activation Protocol' in shared_prompt
    
    def test_step_1_resolve_customization(self, shared_prompt):
        assert '### Step 1: Resolve Customization' in shared_prompt
        assert 'resolve_customization.py' in shared_prompt
        assert '{skill-root}' in shared_prompt
        assert '{project-root}' in shared_prompt
    
    def test_step_2_prepend_steps(self, shared_prompt):
        assert '### Step 2: Execute Prepend Steps' in shared_prompt
        assert 'activation_steps_prepend' in shared_prompt
    
    def test_step_3_review_project_state(self, shared_prompt):
        assert '### Step 3: Review Project State' in shared_prompt
    
    def test_step_4_review_project_config(self, shared_prompt):
        assert '### Step 4: Review Project Config' in shared_prompt
    
    def test_step_5_persistent_facts(self, shared_prompt):
        assert '### Step 5: Load Persistent Facts' in shared_prompt
        assert 'persistent_facts' in shared_prompt
        assert 'file:' in shared_prompt
    
    def test_step_5_5_sidecar_loading(self, shared_prompt):
        assert '### Step 5.5: Load Sidecar Memory' in shared_prompt
        assert '-sidecar' in shared_prompt
        assert 'memories.md' in shared_prompt
    
    def test_step_6_greet(self, shared_prompt):
        assert '### Step 6: Greet as Persona' in shared_prompt
        assert 'agent.icon' in shared_prompt
    
    def test_step_7_append_steps(self, shared_prompt):
        assert '### Step 7: Execute Append Steps' in shared_prompt
        assert 'activation_steps_append' in shared_prompt
    
    def test_step_8_menu_dispatch(self, shared_prompt):
        assert '### Step 8: Present Menu or Dispatch' in shared_prompt
    
    def test_step_ordering(self, shared_prompt):
        """Verify steps appear in correct order."""
        steps = [
            '### Step 1:',
            '### Step 2:',
            '### Step 3:',
            '### Step 4:',
            '### Step 5:',
            '### Step 5.5:',
            '### Step 6:',
            '### Step 7:',
            '### Step 8:',
        ]
        positions = {step: shared_prompt.index(step) for step in steps}
        for i in range(len(steps) - 1):
            assert positions[steps[i]] < positions[steps[i + 1]], f'{steps[i]} should come before {steps[i+1]}'
    
    def test_resolve_customization_as_first_action(self, shared_prompt):
        """Verify resolve_customization is described as first action."""
        activation_start = shared_prompt.index('## BMAD Activation Protocol')
        resolve_pos = shared_prompt.index('resolve_customization.py')
        greet_pos = shared_prompt.index('### Step 6: Greet')
        assert resolve_pos < greet_pos
        assert resolve_pos > activation_start
    
    def test_prepend_before_persona(self, shared_prompt):
        """Prepend steps run BEFORE persona adoption."""
        prepend_pos = shared_prompt.index('### Step 2: Execute Prepend Steps')
        greet_pos = shared_prompt.index('### Step 6: Greet')
        assert prepend_pos < greet_pos
    
    def test_append_after_greeting_before_menu(self, shared_prompt):
        """Append steps run AFTER greeting but BEFORE menu."""
        greet_pos = shared_prompt.index('### Step 6: Greet')
        append_pos = shared_prompt.index('### Step 7: Execute Append Steps')
        menu_pos = shared_prompt.index('### Step 8: Present Menu')
        assert greet_pos < append_pos < menu_pos

class TestSidecarWritingInstructions:
    """Verify sidecar writing instructions exist."""
    
    def test_sidecar_writing_section_exists(self, shared_prompt):
        assert '## Sidecar Memory Writing' in shared_prompt
    
    def test_writing_triggers(self, shared_prompt):
        assert 'workflow execution' in shared_prompt.lower()
        assert 'memories.md' in shared_prompt
    
    def test_append_not_overwrite(self, shared_prompt):
        assert 'append' in shared_prompt.lower()
        assert 'never overwrite' in shared_prompt.lower()
    
    def test_sidecar_path_format(self, shared_prompt):
        assert '{your-agent-name}-sidecar' in shared_prompt

class TestActivationFallback:
    """Verify graceful fallback when resolver fails."""
    
    def test_resolver_failure_fallback(self, shared_prompt):
        assert 'hardcoded defaults' in shared_prompt or 'proceed with' in shared_prompt

class TestExistingSections:
    """Verify existing sections are preserved."""
    
    def test_variable_resolution(self, shared_prompt):
        assert '## A0 Variable Resolution' in shared_prompt
    
    def test_initial_clarification(self, shared_prompt):
        assert '## Initial Clarification' in shared_prompt
    
    def test_thinking_framework(self, shared_prompt):
        assert '## Thinking Framework' in shared_prompt
    
    def test_tool_calling(self, shared_prompt):
        assert '## Tool Calling' in shared_prompt
    
    def test_file_handling(self, shared_prompt):
        assert '## File and Artifact Handling' in shared_prompt
