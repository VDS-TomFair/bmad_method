import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CIS_DIR = PROJECT / 'skills' / 'bmad-cis'

# Expected: each SKILL.md under bmad-cis/ should have trigger_patterns
EXPECTED_CIS_ACTIONS = {
    'innovation-strategy': 'bmad-innovation-strategy',
    'problem-solving': 'bmad-problem-solving',
    'design-thinking': 'bmad-design-thinking',
    'storytelling': 'bmad-storytelling',
    'presentation': 'bmad-presentation',
}


def _find_skill_md() -> dict[str, Path]:
    result = {}
    for p in CIS_DIR.rglob('SKILL.md'):
        key = p.parent.name
        result[key] = p
    return result


class TestC3CISTriggerPatterns(unittest.TestCase):
    """C3: All bmad-cis SKILL.md files must have trigger_patterns."""

    def test_all_cis_skill_md_found(self):
        found = _find_skill_md()
        for key in EXPECTED_CIS_ACTIONS:
            self.assertIn(key, found, f'Missing SKILL.md for: {key}')

    def test_all_have_trigger_patterns(self):
        found = _find_skill_md()
        for key, path in found.items():
            content = path.read_text()
            self.assertIn('trigger_patterns:', content,
                      f'{key}/SKILL.md missing trigger_patterns')

    def test_trigger_patterns_have_slash_commands(self):
        found = _find_skill_md()
        for key, action in EXPECTED_CIS_ACTIONS.items():
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
