import ast
import unittest
from pathlib import Path

API_FILE = Path(__file__).resolve().parents[1] / "api" / "_bmad_status.py"
ROUTING_FILE = Path(__file__).resolve().parents[1] / "extensions" / "python" / "message_loop_prompts_after" / "_80_bmad_routing_manifest.py"
CLI_FILE = Path(__file__).resolve().parents[1] / "skills" / "bmad-init" / "scripts" / "bmad-status.py"


class TestNoMtimeFallbackAPI(unittest.TestCase):
    """A3: API must not have cross-project mtime fallback."""

    def test_api_no_mtime_scan(self):
        source = API_FILE.read_text()
        # The production fallback that scans projects_dir should NOT exist
        self.assertNotIn("candidates.sort(reverse=True)", source,
                         "API should not have mtime-based cross-project scan")

    def test_api_no_stage3_comment(self):
        source = API_FILE.read_text()
        self.assertNotIn("Stage 3: production fallback", source,
                         "API Stage 3 mtime fallback should be removed")

    def test_api_resolve_project_returns_none_without_context(self):
        """When no context and no .a0proj ancestor, must return None (not scan)."""
        source = API_FILE.read_text()
        # Should not reference /a0/usr/projects as a scan path
        self.assertNotIn("projects_dir = Path", source)


class TestNoMtimeFallbackRouting(unittest.TestCase):
    """A3: Routing extension must not have cross-project mtime fallback."""

    def test_routing_no_mtime_scan(self):
        source = ROUTING_FILE.read_text()
        # The mtime-based scan should be removed from _resolve_state_file
        # Check for the pattern of collecting candidates with st_mtime
        lines = source.splitlines()
        in_resolve = False
        for line in lines:
            if "def _resolve_state_file" in line:
                in_resolve = True
            elif in_resolve and line.strip().startswith("def "):
                break
            elif in_resolve:
                self.assertNotIn("st_mtime", line,
                                 "_resolve_state_file should not use mtime scan")


class TestCliMtimeGatedByDevMode(unittest.TestCase):
    """A3: CLI bmad-status.py must gate mtime fallback behind BMAD_DEV_MODE."""

    def test_cli_has_dev_mode_guard(self):
        source = CLI_FILE.read_text()
        self.assertIn("BMAD_DEV_MODE", source,
                      "CLI mtime fallback must be gated behind BMAD_DEV_MODE env var")

    def test_cli_has_warning_on_dev_mode_usage(self):
        source = CLI_FILE.read_text()
        # Should warn when using the fallback
        self.assertIn("log.warning", source,
                      "CLI must log.warning when using dev mode mtime fallback")


class TestFallbackRemovedOrGatedSourceCheck(unittest.TestCase):
    """Verify the specific scan loops are removed/gated."""

    def test_api_no_iterdir_scan(self):
        source = API_FILE.read_text()
        # Check that there's no projects_dir.iterdir() pattern
        self.assertNotIn("projects_dir.iterdir()", source)

    def test_routing_no_iterdir_scan(self):
        source = ROUTING_FILE.read_text()
        # After _resolve_state_file, no projects_dir.iterdir()
        # The scan fallback should be removed from the routing extension entirely
        lines = source.splitlines()
        in_resolve = False
        for line in lines:
            if "def _resolve_state_file" in line:
                in_resolve = True
            elif in_resolve and line.strip().startswith("def "):
                break
            elif in_resolve:
                self.assertNotIn("iterdir()", line,
                                 "_resolve_state_file should not scan iterdir()")


if __name__ == "__main__":
    unittest.main()
