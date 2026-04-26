"""Fix 1: Verify _SKILLS_DIR and _BMAD_CONFIG_DIR exist in routing extension.

These variables were accidentally deleted during Phase B7 refactoring but
are still referenced at lines 86, 342, 343, 369. Without them, execute()
raises NameError at runtime.
"""
import unittest
from pathlib import Path
import importlib.util as _ilu

ROUTING_FILE = (
    Path(__file__).resolve().parents[1]
    / "extensions" / "python" / "message_loop_prompts_after"
    / "_80_bmad_routing_manifest.py"
)


def _load_module():
    """Load the routing extension module without triggering A0 imports."""
    spec = _ilu.spec_from_file_location("routing_manifest", str(ROUTING_FILE))
    if spec is None:
        raise ImportError(f"Cannot load {ROUTING_FILE}")
    return spec


class TestRoutingVarsExist(unittest.TestCase):
    """RED: These tests must fail before the fix is applied."""

    def test_skills_dir_defined(self):
        """_SKILLS_DIR must be defined as a Path."""
        spec = _load_module()
        # We can't exec_module (A0 imports fail), so check source directly
        source = ROUTING_FILE.read_text()
        self.assertIn("_SKILLS_DIR", source,
                      "_SKILLS_DIR is not defined anywhere in the routing extension")
        # Check it's an assignment, not just a reference
        import re
        assignments = re.findall(r'^_SKILLS_DIR\s*=', source, re.MULTILINE)
        self.assertGreaterEqual(len(assignments), 1,
                                "_SKILLS_DIR is referenced but never assigned")

    def test_bmad_config_dir_defined(self):
        """_BMAD_CONFIG_DIR must be defined as a Path."""
        source = ROUTING_FILE.read_text()
        self.assertIn("_BMAD_CONFIG_DIR", source,
                      "_BMAD_CONFIG_DIR is not defined anywhere in the routing extension")
        import re
        assignments = re.findall(r'^_BMAD_CONFIG_DIR\s*=', source, re.MULTILINE)
        self.assertGreaterEqual(len(assignments), 1,
                                "_BMAD_CONFIG_DIR is referenced but never assigned")

    def test_skills_dir_value(self):
        """_SKILLS_DIR must resolve to PLUGIN_ROOT/skills."""
        source = ROUTING_FILE.read_text()
        self.assertIn('_SKILLS_DIR = _PLUGIN_ROOT / "skills"', source,
                      "_SKILLS_DIR must be _PLUGIN_ROOT / 'skills'")

    def test_bmad_config_dir_value(self):
        """_BMAD_CONFIG_DIR must resolve to PLUGIN_ROOT/skills/bmad-init/_config."""
        source = ROUTING_FILE.read_text()
        self.assertIn('_BMAD_CONFIG_DIR = _PLUGIN_ROOT / "skills" / "bmad-init" / "_config"', source,
                      "_BMAD_CONFIG_DIR must be _PLUGIN_ROOT / 'skills' / 'bmad-init' / '_config'")


if __name__ == "__main__":
    unittest.main()
