import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "bmad-init" / "scripts" / "bmad-init.sh"


class TestBmadInitSh(unittest.TestCase):
    # A1: bmad-init.sh path generation and bash hygiene
    # B11: comprehensive subprocess tests

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

    # ── B11: comprehensive subprocess tests ──────────────────────────

    def test_directories_created(self):
        """All required .a0proj directories must be created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "dir-test"
            project_dir.mkdir()

            result = subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")

            a0proj = project_dir / ".a0proj"
            expected_dirs = [
                a0proj / "_bmad-output" / "planning-artifacts" / "research",
                a0proj / "_bmad-output" / "implementation-artifacts",
                a0proj / "_bmad-output" / "test-artifacts",
                a0proj / "knowledge" / "main",
                a0proj / "knowledge" / "fragments",
                a0proj / "knowledge" / "solutions",
                a0proj / "instructions",
            ]
            for d in expected_dirs:
                self.assertTrue(d.is_dir(), f"Directory not created: {d}")

    def test_idempotent(self):
        """Running the script twice must not fail or overwrite config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "idem-test"
            project_dir.mkdir()

            # First run
            result1 = subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )
            self.assertEqual(result1.returncode, 0, f"First run failed: {result1.stderr}")

            config_path = project_dir / ".a0proj" / "instructions" / "01-bmad-config.md"
            config1 = config_path.read_text()

            # Second run
            result2 = subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )
            self.assertEqual(result2.returncode, 0, f"Second run failed: {result2.stderr}")

            # Config must be unchanged (no-clobber)
            config2 = config_path.read_text()
            self.assertEqual(config1, config2, "Config changed on second run")

    def test_user_prefs_file_created(self):
        """bmad-user-prefs.promptinclude.md must be created."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "prefs-test"
            project_dir.mkdir()

            subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )

            prefs_path = project_dir / ".a0proj" / "instructions" / "bmad-user-prefs.promptinclude.md"
            self.assertTrue(prefs_path.exists(), "User prefs file not created")

    def test_user_prefs_no_clobber(self):
        """User prefs file must not be overwritten on re-init."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "noclobber-test"
            project_dir.mkdir()

            # First run
            subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )

            prefs_path = project_dir / ".a0proj" / "instructions" / "bmad-user-prefs.promptinclude.md"
            # Modify the file
            prefs_path.write_text("CUSTOM_USER_PREFS_MARKER\n" + prefs_path.read_text())
            modified = prefs_path.read_text()

            # Second run
            subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )

            # File must still contain our marker
            self.assertIn("CUSTOM_USER_PREFS_MARKER", prefs_path.read_text(),
                         "User prefs file was overwritten on re-init")

    def test_state_file_created(self):
        """02-bmad-state.md must be created with phase: Ready."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir) / "state-test"
            project_dir.mkdir()

            subprocess.run(
                ["bash", str(SCRIPT), str(project_dir)],
                capture_output=True, text=True,
            )

            state_path = project_dir / ".a0proj" / "instructions" / "02-bmad-state.md"
            self.assertTrue(state_path.exists(), "State file not created")
            state = state_path.read_text()
            self.assertIn("ready", state.lower())


if __name__ == "__main__":
    unittest.main()
