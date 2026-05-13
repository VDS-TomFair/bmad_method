"""Phase F - Config migration tests (F-P1-1 through F-P1-3)."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_CONFIG = ROOT / 'skills' / 'bmad-init' / 'core' / 'config.yaml'
BMM_CONFIG = ROOT / 'skills' / 'bmad-bmm' / 'config.yaml'
BMB_CONFIG = ROOT / 'skills' / 'bmad-bmb' / 'config.yaml'
CIS_CONFIG = ROOT / 'skills' / 'bmad-cis' / 'config.yaml'
TEA_CONFIG = ROOT / 'skills' / 'bmad-tea' / 'config.yaml'
ALL_CONFIGS = [BMB_CONFIG, BMM_CONFIG, CIS_CONFIG, TEA_CONFIG]


class TestProjectNameInCoreOnly(unittest.TestCase):
    """F-P1-1 / F-P1-2: project_name must exist in core config only."""

    def test_project_name_in_core_config(self):
        """project_name field must be present in bmad-init/core/config.yaml."""
        text = CORE_CONFIG.read_text()
        self.assertIn('project_name', text,
                      'project_name not found in core config')

    def test_project_name_not_in_bmm_config(self):
        """project_name field must NOT be in bmad-bmm/config.yaml."""
        text = BMM_CONFIG.read_text()
        self.assertNotIn('project_name', text,
                         'project_name still present in bmm config')


class TestConfigVersions66(unittest.TestCase):
    """F-P1-3: All config files must declare Version: 6.6.0."""

    def test_core_config_version_66(self):
        """bmad-init/core/config.yaml must have Version: 6.6.0."""
        text = CORE_CONFIG.read_text()
        self.assertIn('Version: 6.6.0', text,
                      'Core config does not have Version: 6.6.0')

    def test_all_skill_configs_version_66(self):
        """Every skills/*/config.yaml must have Version: 6.6.0."""
        for cfg in ALL_CONFIGS:
            with self.subTest(config=cfg.name):
                text = cfg.read_text()
                self.assertIn('Version: 6.6.0', text,
                              f'{cfg} does not have Version: 6.6.0')

    def test_no_old_version_strings(self):
        """No config should contain an older version string."""
        old_versions = ['Version: 6.5', 'Version: 6.4', 'Version: 6.3',
                        'Version: 6.2', 'Version: 6.1', 'Version: 6.0']
        for cfg in ALL_CONFIGS + [CORE_CONFIG]:
            text = cfg.read_text()
            for old in old_versions:
                with self.subTest(config=cfg.name, old=old):
                    self.assertNotIn(old, text,
                                     f'{cfg} still contains old version: {old}')


class TestPluginVersion(unittest.TestCase):
    """F-P2-2: plugin.yaml must declare version 1.3.0."""

    def test_plugin_version_110(self):
        """plugin.yaml version field must be 1.3.0."""
        plugin_yaml = ROOT / 'plugin.yaml'
        text = plugin_yaml.read_text()
        self.assertIn('version: 1.3.0', text,
                      'plugin.yaml does not have version: 1.3.0')


class TestChangelog(unittest.TestCase):
    """F-P2-1: CHANGELOG.md must have 1.3.0 entries."""

    def test_changelog_has_110_header(self):
        """CHANGELOG.md must contain [1.3.0] header."""
        changelog = ROOT / 'CHANGELOG.md'
        text = changelog.read_text()
        self.assertIn('[1.3.0]', text,
                      'CHANGELOG.md does not contain [1.3.0] header')

    def test_changelog_mentions_phase_f(self):
        """CHANGELOG.md must mention Phase F or upstream sync."""
        changelog = ROOT / 'CHANGELOG.md'
        text = changelog.read_text()
        self.assertTrue(
            'Phase F' in text or 'upstream' in text.lower(),
            'CHANGELOG.md does not mention Phase F or upstream sync'
        )
