import pytest
import os
import subprocess
import tempfile
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INIT_SCRIPT = os.path.join(PROJECT_ROOT, 'skills', 'bmad-init', 'scripts', 'bmad-init.sh')

EXPECTED_AGENTS = [
    'analyst', 'pm', 'architect', 'dev', 'ux-designer', 'tech-writer',
    'module-builder', 'agent-builder', 'workflow-builder', 'test-architect',
    'innovation', 'problem-solver', 'design-thinking', 'brainstorming-coach',
    'storyteller', 'presentation'
]

class TestSidecarDirectories:
    """Verify init script creates sidecar directories for all agents."""
    
    @pytest.fixture(scope='class')
    def init_project(self):
        """Run init script in a temp directory and yield the path."""
        tmpdir = tempfile.mkdtemp(prefix='bmad-sidecar-test-')
        subprocess.run(['bash', INIT_SCRIPT, tmpdir], check=True, capture_output=True, text=True)
        yield tmpdir
        shutil.rmtree(tmpdir, ignore_errors=True)
    
    def test_memory_directory_exists(self, init_project):
        mem_dir = os.path.join(init_project, '.a0proj', '_bmad', '_memory')
        assert os.path.isdir(mem_dir)
    
    def test_all_16_sidecar_dirs(self, init_project):
        mem_dir = os.path.join(init_project, '.a0proj', '_bmad', '_memory')
        actual_dirs = [d for d in os.listdir(mem_dir) if d.endswith('-sidecar')]
        assert len(actual_dirs) == 16, f'Expected 16 sidecar dirs, found {len(actual_dirs)}: {actual_dirs}'
    
    @pytest.mark.parametrize('agent', EXPECTED_AGENTS)
    def test_sidecar_dir_exists(self, init_project, agent):
        sidecar_dir = os.path.join(init_project, '.a0proj', '_bmad', '_memory', f'{agent}-sidecar')
        assert os.path.isdir(sidecar_dir), f'Missing sidecar dir for {agent}'
    
    @pytest.mark.parametrize('agent', EXPECTED_AGENTS)
    def test_memories_md_exists(self, init_project, agent):
        memories_file = os.path.join(init_project, '.a0proj', '_bmad', '_memory', f'{agent}-sidecar', 'memories.md')
        assert os.path.isfile(memories_file), f'Missing memories.md for {agent}'
    
    @pytest.mark.parametrize('agent', EXPECTED_AGENTS)
    def test_memories_md_readable(self, init_project, agent):
        memories_file = os.path.join(init_project, '.a0proj', '_bmad', '_memory', f'{agent}-sidecar', 'memories.md')
        with open(memories_file, 'r') as f:
            content = f.read()
        assert isinstance(content, str)
        assert len(content) >= 0  # Can be empty or have template content

class TestSidecarIdempotency:
    """Verify init script is idempotent for sidecar dirs."""
    
    def test_rerun_preserves_content(self):
        tmpdir = tempfile.mkdtemp(prefix='bmad-sidecar-idem-')
        try:
            # First run
            subprocess.run(['bash', INIT_SCRIPT, tmpdir], check=True, capture_output=True)
            # Write custom content
            mem_file = os.path.join(tmpdir, '.a0proj', '_bmad', '_memory', 'analyst-sidecar', 'memories.md')
            with open(mem_file, 'w') as f:
                f.write('Custom memory content')
            # Second run
            subprocess.run(['bash', INIT_SCRIPT, tmpdir], check=True, capture_output=True)
            # Verify content preserved
            with open(mem_file, 'r') as f:
                content = f.read()
            assert 'Custom memory content' in content
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

class TestSidecarImportSkill:
    """Verify sidecar import skill exists and is valid."""
    
    def test_skill_md_exists(self):
        skill_path = os.path.join(PROJECT_ROOT, 'skills', 'bmad-sidecar-import', 'SKILL.md')
        assert os.path.isfile(skill_path)
    
    def test_import_script_exists(self):
        script_path = os.path.join(PROJECT_ROOT, 'skills', 'bmad-sidecar-import', 'scripts', 'import-sidecars.sh')
        assert os.path.isfile(script_path)
    
    def test_import_script_valid_bash(self):
        script_path = os.path.join(PROJECT_ROOT, 'skills', 'bmad-sidecar-import', 'scripts', 'import-sidecars.sh')
        result = subprocess.run(['bash', '-n', script_path], capture_output=True, text=True)
        assert result.returncode == 0, f'Bash syntax error: {result.stderr}'

class TestSidecarInSharedPrompt:
    """Verify shared prompt references sidecar correctly."""
    
    def test_sidecar_loading_reference(self):
        with open(os.path.join(PROJECT_ROOT, 'prompts', 'bmad-agent-shared.md'), 'r') as f:
            content = f.read()
        assert 'sidecar' in content.lower()
        assert '-sidecar' in content
