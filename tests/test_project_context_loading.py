import pytest
import os
import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_PROMPT_PATH = os.path.join(PROJECT_ROOT, 'prompts', 'bmad-agent-shared.md')

WORKFLOW_STEP_FILES = [
    'skills/bmad-bmm/workflows/4-implementation/dev-story/steps/step-01-find-story.md',
    'skills/bmad-bmm/workflows/4-implementation/create-story/steps/step-01-determine-story.md',
    'skills/bmad-bmm/workflows/4-implementation/code-review/steps/step-01-gather-context.md',
    'skills/bmad-bmm/workflows/4-implementation/sprint-planning/steps/step-01-discover-epics.md',
    'skills/bmad-bmm/workflows/4-implementation/correct-course/steps/step-01-initialize.md',
    'skills/bmad-bmm/workflows/bmad-quick-flow/quick-dev/step-01-clarify-and-route.md',
    'skills/bmad-bmm/workflows/bmad-quick-flow/quick-spec/steps/step-01-understand.md',
    'skills/bmad-bmm/workflows/3-solutioning/create-architecture/steps/step-01-init.md',
]

AGENT_CUSTOMIZE_FILES = [
    'skills/bmad-bmm/agents/analyst/customize.toml',
    'skills/bmad-bmm/agents/dev/customize.toml',
    'skills/bmad-bmm/agents/pm/customize.toml',
    'skills/bmad-bmm/agents/architect/customize.toml',
    'skills/bmad-bmm/agents/ux-designer/customize.toml',
    'skills/bmad-bmm/agents/tech-writer/customize.toml',
]

class TestPersistentFactsInstructions:
    """Verify persistent_facts processing instructions exist in shared prompt."""
    
    @pytest.fixture
    def shared_prompt(self):
        with open(SHARED_PROMPT_PATH, 'r') as f:
            return f.read()
    
    def test_persistent_facts_step(self, shared_prompt):
        assert '### Step 5: Load Persistent Facts' in shared_prompt
    
    def test_file_prefix_handling(self, shared_prompt):
        assert 'file:' in shared_prompt
    
    def test_glob_pattern_support(self, shared_prompt):
        assert 'glob' in shared_prompt.lower() or '**/' in shared_prompt
    
    def test_literal_facts_handling(self, shared_prompt):
        assert 'literal' in shared_prompt.lower()
    
    def test_project_context_auto_load(self, shared_prompt):
        assert 'project-context.md' in shared_prompt

class TestWorkflowProjectContext:
    """Verify implementation workflow step-01 files have project-context pre-step."""
    
    @pytest.mark.parametrize('relative_path', WORKFLOW_STEP_FILES)
    def test_project_context_pre_step(self, relative_path):
        full_path = os.path.join(PROJECT_ROOT, relative_path)
        if not os.path.isfile(full_path):
            pytest.skip(f'File not found: {relative_path}')
        with open(full_path, 'r') as f:
            content = f.read()
        assert 'project-context' in content.lower(), f'Missing project-context reference in {relative_path}'
    
    def test_all_8_files_have_pre_step(self):
        count = 0
        for rel_path in WORKFLOW_STEP_FILES:
            full_path = os.path.join(PROJECT_ROOT, rel_path)
            if os.path.isfile(full_path):
                with open(full_path, 'r') as f:
                    if 'project-context' in f.read().lower():
                        count += 1
        assert count == 8, f'Expected 8 workflow files with project-context, found {count}'

class TestCustomizeTomlPersistentFacts:
    """Verify agent customize.toml files reference project-context.md in persistent_facts."""
    
    @pytest.mark.parametrize('relative_path', AGENT_CUSTOMIZE_FILES)
    def test_persistent_facts_in_customize(self, relative_path):
        full_path = os.path.join(PROJECT_ROOT, relative_path)
        if not os.path.isfile(full_path):
            pytest.skip(f'File not found: {relative_path}')
        with open(full_path, 'r') as f:
            content = f.read()
        assert 'persistent_facts' in content, f'Missing persistent_facts in {relative_path}'
        assert 'project-context.md' in content, f'Missing project-context.md reference in {relative_path}'

class TestInitScriptCustomDir:
    """Verify init script creates _bmad/custom/ directory."""
    
    def test_custom_dir_in_script(self):
        script_path = os.path.join(PROJECT_ROOT, 'skills', 'bmad-init', 'scripts', 'bmad-init.sh')
        with open(script_path, 'r') as f:
            content = f.read()
        assert '_bmad/custom' in content
