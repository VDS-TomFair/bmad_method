import ast
import unittest
from pathlib import Path

ROUTING_FILE = Path(__file__).resolve().parents[1] / "extensions" / "python" / "message_loop_prompts_after" / "_80_bmad_routing_manifest.py"


class TestNoDeadCode(unittest.TestCase):
    """A7: Remove dead code from routing extension."""

    def test_no_skill_to_module_constant(self):
        """SKILL_TO_MODULE dict is unused — must be removed."""
        source = ROUTING_FILE.read_text()
        self.assertNotIn("SKILL_TO_MODULE", source,
                         "SKILL_TO_MODULE is unused dead code")

    def test_no_get_routing_rows_csv(self):
        """get_routing_rows_csv function should not exist."""
        source = ROUTING_FILE.read_text()
        self.assertNotIn("get_routing_rows_csv", source,
                         "get_routing_rows_csv is unused dead code")


class TestNoDuplicatePhaseMaps(unittest.TestCase):
    """A7: Phase-bucket dicts should not be duplicated."""

    def test_phase_map_only_defined_once(self):
        """The four phase buckets should appear in exactly one dict."""
        source = ROUTING_FILE.read_text()
        # Count how many times "1-analysis" appears as a dict key
        count = source.count('"1-analysis"')
        self.assertLessEqual(count, 1,
                         f"1-analysis key appears {count} times — should be consolidated into one dict")

    def test_phase_modules_and_scan_map_are_same_keys(self):
        """PHASE_MODULES and _scan_artifact_existence phase_map should share keys."""
        source = ROUTING_FILE.read_text()
        # PHASE_MODULES should have at least the 4 main phase keys
        self.assertIn('"1-analysis"', source)
        self.assertIn('"2-planning"', source)
        self.assertIn('"3-solutioning"', source)
        self.assertIn('"4-implementation"', source)


if __name__ == "__main__":
    unittest.main()
