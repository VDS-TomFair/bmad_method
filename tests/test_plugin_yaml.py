import unittest
from pathlib import Path

PLUGIN_YAML = Path(__file__).resolve().parents[1] / "plugin.yaml"


class TestPluginYaml(unittest.TestCase):
    """B1: per_project_config must be true in plugin.yaml."""

    def test_per_project_config_is_true(self):
        """plugin.yaml must have per_project_config: true."""
        content = PLUGIN_YAML.read_text()
        self.assertIn("per_project_config: true", content,
                     "per_project_config must be set to true")

    def test_no_false_per_project_config(self):
        """plugin.yaml must NOT have per_project_config: false."""
        content = PLUGIN_YAML.read_text()
        self.assertNotIn("per_project_config: false", content,
                         "per_project_config: false must be changed to true")


if __name__ == "__main__":
    unittest.main()
