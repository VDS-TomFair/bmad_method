import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CORE_SKILLS_DIR = PROJECT / 'skills' / 'bmad-init' / 'core'

# Expected: each SKILL.md under core/ should have trigger_patterns in YAML frontmatter
EXPECTED_SKILL_ACTIONS = {
    'advanced-elicitation': 'bmad-advanced-elicitation',
    'brainstorming': 'bmad-brainstorming',
    'editorial-prose': 'bmad-editorial-review-prose',
    'distillator': 'bmad-distillator',
    'review-edge-case': 'bmad-review-edge-case-hunter',
    'editorial-structure': 'bmad-editorial-review-structure',
    'review-adversarial': 'bmad-review-adversarial-general',
    'index-docs': 'bmad-index-docs',
    'shard-doc': 'bmad-shard-doc',
    'help': 'bmad-help',
}


def _find_skill_md() -> dict[str, Path]:
    """Find all SKILL.md files under core/ keyed by parent dir name."""
    result = {}
    for p in CORE_SKILLS_DIR.rglob('SKILL.md'):
        key = p.parent.name
        result[key] = p
    return result


def _has_trigger_patterns(content: str) -> bool:
    """Check if YAML frontmatter contains trigger_patterns."""
    return 'trigger_patterns:' in content


class TestC6CoreTriggerPatterns(unittest.TestCase):
    """C6: All bmad-init/core SKILL.md files must have trigger_patterns."""

    def test_all_expected_skill_md_files_exist(self):
        """All 10 expected core SKILL.md files must be found."""
        found = _find_skill_md()
        for key in EXPECTED_SKILL_ACTIONS:
            self.assertIn(key, found, f'Missing SKILL.md for: {key}')

    def test_all_skill_md_have_trigger_patterns(self):
        """Every core SKILL.md must have trigger_patterns in frontmatter."""
        found = _find_skill_md()
        for key, path in found.items():
            content = path.read_text()
            self.assertTrue(_has_trigger_patterns(content),
                        f'{key}/SKILL.md missing trigger_patterns')

    def test_trigger_patterns_contain_slash_command(self):
        """Each SKILL.md trigger_patterns must include /bmad-<action> slash command."""
        found = _find_skill_md()
        for key, action in EXPECTED_SKILL_ACTIONS.items():
            if key not in found:
                continue
            content = found[key].read_text()
            slash = f'/{action}'
            self.assertIn(slash, content,
                      f'{key}/SKILL.md missing slash command {slash}')

    def test_trigger_patterns_is_yaml_list(self):
        """trigger_patterns must be a YAML list (lines starting with '  - ')."""
        found = _find_skill_md()
        for key, path in found.items():
            content = path.read_text()
            if not _has_trigger_patterns(content):
                continue
            lines = content.splitlines()
            has_list_entry = any(line.strip().startswith('- /') for line in lines)
            self.assertTrue(has_list_entry,
                        f'{key}/SKILL.md trigger_patterns is not a YAML list')


if __name__ == '__main__':
    unittest.main()
