import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
BMM_DIR = PROJECT / 'skills' / 'bmad-bmm'

# BMM SKILL.md dirs and their primary actions from module-help.csv
EXPECTED_BMM = {
    'create-product-brief': 'bmad-create-product-brief',
    'prfaq': 'bmad-prfaq',
    'domain-research': 'bmad-domain-research',
    'market-research': 'bmad-market-research',
    'technical-research': 'bmad-technical-research',
    'create-prd': 'bmad-create-prd',
    'edit-prd': 'bmad-edit-prd',
    'validate-prd': 'bmad-validate-prd',
    'create-ux-design': 'bmad-create-ux-design',
    'check-implementation-readiness': 'bmad-check-implementation-readiness',
    'create-architecture': 'bmad-create-architecture',
    'create-epics-and-stories': 'bmad-create-epics-and-stories',
    'checkpoint-preview': 'bmad-checkpoint-preview',
    'code-review': 'bmad-code-review',
    'correct-course': 'bmad-correct-course',
    'create-story': 'bmad-create-story',
    'dev-story': 'bmad-dev-story',
    'retrospective': 'bmad-retrospective',
    'sprint-planning': 'bmad-sprint-planning',
    'sprint-status': 'bmad-sprint-status',
    'quick-dev': 'bmad-quick-dev',
    'quick-spec': 'bmad-quick-spec',
    'document-project': 'bmad-document-project',
    'generate-project-context': 'bmad-generate-project-context',
    'qa-generate-e2e-tests': 'bmad-qa-automate',
}


def _find_skill_md() -> dict[str, Path]:
    result = {}
    for p in BMM_DIR.rglob('SKILL.md'):
        key = p.parent.name
        result[key] = p
    return result


class TestC2BMMTriggerPatterns(unittest.TestCase):
    """C2: All bmad-bmm SKILL.md files must have trigger_patterns."""

    def test_all_bmm_skill_md_found(self):
        found = _find_skill_md()
        for key in EXPECTED_BMM:
            self.assertIn(key, found, f'Missing SKILL.md for: {key}')

    def test_all_have_trigger_patterns(self):
        found = _find_skill_md()
        for key, path in found.items():
            content = path.read_text()
            self.assertIn('trigger_patterns:', content,
                      f'{key}/SKILL.md missing trigger_patterns')

    def test_primary_actions_have_slash_commands(self):
        found = _find_skill_md()
        for key, action in EXPECTED_BMM.items():
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
