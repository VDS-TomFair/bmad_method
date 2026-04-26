import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "bmad-init" / "scripts" / "bmad-init.sh"


class TestBmadInitSh(unittest.TestCase):
    # A1: bmad-init.sh path generation and bash hygiene

    def test_bash_syntax_valid(self):
        result = subprocess.run(
            ["bash", "-n", str(SCRIPT)],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, f"bash -n failed: {result.stderr}")

    def test_script_has_strict_mode(self):
        content = SCRIPT.read_text()
        self.assertIn("set -euo pipefail", content)

    def test_no_hardcoded_paths_in_source(self):
        content = SCRIPT.read_text()
        self.assertNotIn("/a0/usr/projects/", content)

    def test_generated_config_uses_project_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "my-test-project"
            project_dir.mkdir()

            result = subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            config_path = project_dir / ".a0proj" / "instructions" / "01-bmad-config.md"
            self.assertTrue(config_path.exists(), "Config file not created")
            config = config_path.read_text()

            # Must NOT contain the hardcoded path
            self.assertNotIn("/a0/usr/projects/", config)

            # Must contain the actual project path
            expected_root = str(project_dir / ".a0proj" / "")
            self.assertIn(expected_root, config)

    def test_generated_config_all_five_path_rows(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "test-proj"
            project_dir.mkdir()

            subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )

            config_path = project_dir / ".a0proj" / "instructions" / "01-bmad-config.md"
            config = config_path.read_text()

            a0proj = str(project_dir / ".a0proj")
            self.assertIn(a0proj + "/", config)
            self.assertIn(a0proj + "/_bmad-output/planning-artifacts/", config)
            self.assertIn(a0proj + "/_bmad-output/implementation-artifacts/", config)
            self.assertIn(a0proj + "/knowledge/", config)
            self.assertIn(a0proj + "/_bmad-output/", config)


if __name__ == "__main__":
    unittest.main()
