import re
import tempfile
import unittest
from pathlib import Path

CORE_FILE = Path(__file__).resolve().parents[1] / "helpers" / "bmad_status_core.py"
SCRIPTS_CORE = Path(__file__).resolve().parents[1] / "skills" / "bmad-init" / "scripts" / "bmad_status_core.py"
BMAD_STATUS = Path(__file__).resolve().parents[1] / "skills" / "bmad-init" / "scripts" / "bmad-status.py"


def _load_core_module():
    import importlib.util as ilu
    spec = ilu.spec_from_file_location("bmad_status_core_test", str(CORE_FILE))
    mod = ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestBmadStatusCoreRegex(unittest.TestCase):
    # A2: read_state() regex correctness

    def test_has_compiled_phase_re(self):
        source = CORE_FILE.read_text()
        self.assertIn("_PHASE_RE", source,
                      "Missing compiled _PHASE_RE regex")

    def test_has_compiled_artifact_re(self):
        source = CORE_FILE.read_text()
        self.assertIn("_ARTIFACT_RE", source,
                      "Missing compiled _ARTIFACT_RE regex")

    def test_phase_re_uses_multiline_ignorecase(self):
        source = CORE_FILE.read_text()
        self.assertIn("re.MULTILINE", source)
        self.assertIn("re.IGNORECASE", source)

    def test_has_logging_import(self):
        source = CORE_FILE.read_text()
        self.assertIn("import logging", source)
        self.assertIn("logging.getLogger(__name__)", source)

    def test_read_state_returns_lowercase_phase(self):
        """Phase output must always be lowercase."""
        mod = _load_core_module()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("## BMAD Active State\n- Phase: READY\n- Active Artifact: brief\n")
            f.flush()
            result = mod.read_state(Path(f.name))
        self.assertEqual(result["phase"], "ready")

    def test_read_state_multiline_phase(self):
        """Phase can be in middle of multiline content."""
        mod = _load_core_module()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Line 1\nLine 2\n- Phase: 2-Planning\nLine 4\n")
            f.flush()
            result = mod.read_state(Path(f.name))
        self.assertEqual(result["phase"], "2-planning")

    def test_read_state_case_insensitive_phase(self):
        """Phase detection must be case-insensitive."""
        mod = _load_core_module()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("- PHASE: 3-Solutioning\n")
            f.flush()
            result = mod.read_state(Path(f.name))
        self.assertEqual(result["phase"], "3-solutioning")

    def test_scripts_copy_deleted(self):
        """The scripts/bmad_status_core.py local copy must be deleted."""
        self.assertFalse(SCRIPTS_CORE.exists(),
                         f"Local copy still exists: {SCRIPTS_CORE}")

    def test_bmad_status_uses_importlib(self):
        """bmad-status.py must use importlib to load from helpers/ (no 'from bmad_status_core import')."""
        source = BMAD_STATUS.read_text()
        self.assertNotIn("from bmad_status_core import", source)
        self.assertIn("importlib", source)


class TestRoutingExtensionUsesReadState(unittest.TestCase):
    # A2: routing extension should call read_state() for phase

    def test_routing_ext_imports_read_state(self):
        ext_file = Path(__file__).resolve().parents[1] / "extensions" / "python" / "message_loop_prompts_after" / "_80_bmad_routing_manifest.py"
        source = ext_file.read_text()
        self.assertIn("read_state", source,
                      "Routing extension should call read_state() for phase parsing")


if __name__ == "__main__":
    unittest.main()
