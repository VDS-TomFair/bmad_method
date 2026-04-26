import ast
import unittest
from pathlib import Path

API_FILE = Path(__file__).resolve().parents[1] / "api" / "_bmad_status.py"


class TestBmadStatusApi(unittest.TestCase):
    # A6: None-guard on spec_from_file_location

    def test_spec_none_check_exists(self):
        """After spec_from_file_location, there must be an explicit None check on _spec."""
        source = API_FILE.read_text()
        self.assertIn("if _spec is None", source,
                      "Missing 'if _spec is None' guard after spec_from_file_location")

    def test_spec_none_check_after_spec_assignment(self):
        """The None check must come right after spec assignment, before exec_module."""
        source = API_FILE.read_text()
        lines = source.splitlines()
        spec_line = None
        for i, line in enumerate(lines):
            if "_spec = _ilu.spec_from_file_location" in line:
                spec_line = i
                break
        self.assertIsNotNone(spec_line, "Could not find spec_from_file_location assignment")

        # Next few lines should contain the None check before exec_module
        block = "\n".join(lines[spec_line:spec_line + 5])
        self.assertIn("if _spec is None", block,
                      "None check not found within 5 lines of spec assignment")
        # exec_module should come AFTER the None check
        spec_idx = block.index("if _spec is None")
        exec_idx = block.find("exec_module")
        self.assertLess(spec_idx, exec_idx,
                        "None check must come before exec_module")


if __name__ == "__main__":
    unittest.main()
