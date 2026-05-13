import unittest
import yaml
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
AGENTS_DIR = BASE / 'agents'
MODULE_YAML = BASE / 'skills' / 'bmad-bmm' / 'module.yaml'
DEV_CUSTOMIZE = BASE / 'skills' / 'bmad-bmm' / 'agents' / 'dev' / 'customize.toml'
CORE_PY = BASE / 'helpers' / 'bmad_status_core.py'


class TestConsolidatedAgentsRemoved(unittest.TestCase):
    """Verify SM, QA, and Quick-Dev agent directories no longer exist."""

    def test_no_bmad_sm_directory(self):
        self.assertFalse((AGENTS_DIR / 'bmad-sm').exists(),
                         'agents/bmad-sm/ should have been removed')

    def test_no_bmad_qa_directory(self):
        self.assertFalse((AGENTS_DIR / 'bmad-qa').exists(),
                         'agents/bmad-qa/ should have been removed')

    def test_no_bmad_quick_dev_directory(self):
        self.assertFalse((AGENTS_DIR / 'bmad-quick-dev').exists(),
                         'agents/bmad-quick-dev/ should have been removed')


class TestAmeliaMenus(unittest.TestCase):
    """Amelia (bmad-dev) customize.toml must include all 12 menus."""

    EXPECTED_CODES = {'SP', 'SS', 'VS', 'CS', 'DS', 'CR', 'QA', 'CC', 'ER', 'CK', 'QD', 'QS'}

    def test_dev_customize_exists(self):
        self.assertTrue(DEV_CUSTOMIZE.exists(), 'dev customize.toml must exist')

    def test_dev_has_all_menu_codes(self):
        content = DEV_CUSTOMIZE.read_text()
        found = set()
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith('code = '):
                code = stripped.split('=')[1].strip().strip('"').strip("'")
                found.add(code)
        self.assertTrue(self.EXPECTED_CODES.issubset(found),
                        f'Missing menu codes: {self.EXPECTED_CODES - found}')

    def test_dev_has_exactly_12_menus(self):
        content = DEV_CUSTOMIZE.read_text()
        count = content.count('[[agent.menu]]')
        self.assertEqual(count, 12, f'Expected 12 menus, found {count}')


class TestModuleYAMLRouting(unittest.TestCase):
    """BMM module.yaml must route consolidated skills through dev agent."""

    @classmethod
    def setUpClass(cls):
        with open(MODULE_YAML) as f:
            cls.data = yaml.safe_load(f)
        cls.workflows = cls.data.get('workflows', [])

    def test_quick_dev_code_is_QD(self):
        """Quick Dev entry must use QD (not QQ)."""
        codes = [w.get('menu-code') for w in self.workflows]
        self.assertNotIn('QQ', codes, 'QQ should have been replaced with QD')
        self.assertIn('QD', codes, 'QD menu code must exist')

    def test_no_skill_sm(self):
        """No workflow should reference skill:sm."""
        sm_skills = [w for w in self.workflows if w.get('skill') == 'sm']
        self.assertEqual(len(sm_skills), 0,
                         f'Found skill:sm entries: {sm_skills}')

    def test_no_skill_qa(self):
        """No workflow should reference skill:qa."""
        qa_skills = [w for w in self.workflows if w.get('skill') == 'qa']
        self.assertEqual(len(qa_skills), 0,
                         f'Found skill:qa entries: {qa_skills}')

    def test_sm_workflows_routed_to_dev(self):
        """Sprint planning, status, story, retrospective must route to dev."""
        sm_menus = {'SP', 'SS', 'CS', 'ER'}
        for w in self.workflows:
            if w.get('menu-code') in sm_menus:
                self.assertEqual(w.get('skill'), 'dev',
                                 f'{w["menu-code"]} should route to dev, got {w.get("skill")}')


class TestStatusCoreUpdated(unittest.TestCase):
    """bmad_status_core.py must not reference removed agents."""

    def test_no_bmad_sm_in_agent_names(self):
        source = CORE_PY.read_text()
        self.assertNotIn('"bmad-sm"', source)

    def test_no_bmad_qa_in_agent_names(self):
        source = CORE_PY.read_text()
        self.assertNotIn('"bmad-qa"', source)

    def test_no_bmad_quick_dev_in_agent_names(self):
        source = CORE_PY.read_text()
        self.assertNotIn('"bmad-quick-dev"', source)


if __name__ == '__main__':
    unittest.main()
