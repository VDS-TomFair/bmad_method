import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
TEA_DIR = PROJECT / 'skills' / 'bmad-tea'

# Key TEA SKILL.md dirs and their primary actions from module.yaml
EXPECTED_TEA = {
    'testarch': 'bmad-testarch',
    'teach-me-testing': 'bmad-teach-me-testing',
    'test-design': 'bmad-testarch-test-design',
    'framework': 'bmad-testarch-framework',
    'ci': 'bmad-testarch-ci',
    'atdd': 'bmad-testarch-atdd',
    'automate': 'bmad-testarch-automate',
    'test-review': 'bmad-testarch-test-review',
    'nfr-assess': 'bmad-testarch-nfr',
    'trace': 'bmad-testarch-trace',
}


def _find_skill_md() -> dict[str, Path]:
    result = {}
    for p in TEA_DIR.rglob('SKILL.md'):
        key = p.parent.name
        result[key] = p
    return result


class TestC4TEATriggerPatterns(unittest.TestCase):
    """C4: All bmad-tea SKILL.md files must have trigger_patterns."""

    def test_all_tea_skill_md_found(self):
        found = _find_skill_md()
        for key in EXPECTED_TEA:
            self.assertIn(key, found, f'Missing SKILL.md for: {key}')

    def test_all_have_trigger_patterns(self):
        found = _find_skill_md()
        for key, path in found.items():
            content = path.read_text()
            self.assertIn('trigger_patterns:', content,
                      f'{key}/SKILL.md missing trigger_patterns')

    def test_primary_actions_have_slash_commands(self):
        found = _find_skill_md()
        for key, action in EXPECTED_TEA.items():
            if key not in found:
                continue
            content = found[key].read_text()
            slash = f'/{action}'
            self.assertIn(slash, content,
                      f'{key}/SKILL.md missing slash command {slash}')

    def test_trigger_patterns_is_yaml_list(self):
        found = _find_skill_md()
        for key, path in found.items():
            content = path.read_text()
            if 'trigger_patterns:' not in content:
                continue
            lines = content.splitlines()
            has_list = any(line.strip().startswith('- /') for line in lines)
            self.assertTrue(has_list,
                        f'{key}/SKILL.md trigger_patterns not a YAML list')


if __name__ == '__main__':
    unittest.main()
