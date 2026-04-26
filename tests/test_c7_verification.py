import csv
import io
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SKILLS_DIR = PROJECT / 'skills'

NEW_HEADER = ['module', 'skill', 'display-name', 'menu-code', 'description', 'action', 'args', 'phase', 'after', 'before', 'required', 'output-location', 'outputs']


def _all_module_help_csvs() -> list[Path]:
    """Find all module-help.csv files across skill modules."""
    return sorted(SKILLS_DIR.glob('*/module-help.csv')) + sorted(SKILLS_DIR.glob('*/*/module-help.csv'))


def _all_skill_md_files() -> list[Path]:
    """Find all SKILL.md files across all skill modules."""
    return sorted(SKILLS_DIR.rglob('SKILL.md'))


class TestC7CSVSchemaCoverage(unittest.TestCase):
    """C7: Verify ALL module-help.csv files use the 13-col upstream schema."""

    def test_all_csv_files_found(self):
        """Must find module-help.csv files in all skill modules."""
        csvs = _all_module_help_csvs()
        module_names = set(p.parent.name for p in csvs)
        expected = {'bmad-init', 'core', 'bmad-bmm', 'bmad-cis', 'bmad-tea', 'bmad-bmb'}
        for name in expected:
            self.assertTrue(any(name in str(p) for p in csvs),
                        f'No module-help.csv found for module: {name}')

    def test_all_csvs_have_13_col_header(self):
        """Every CSV must use the 13-column upstream header."""
        expected = ','.join(NEW_HEADER)
        for csv_path in _all_module_help_csvs():
            header_line = csv_path.read_text().splitlines()[0].strip()
            self.assertEqual(header_line, expected,
                        f'{csv_path}: header mismatch.\n  got:      {header_line}\n  expected: {expected}')

    def test_all_csvs_exactly_13_columns(self):
        """Every data row in every CSV must have exactly 13 fields."""
        for csv_path in _all_module_help_csvs():
            text = csv_path.read_text()
            reader = csv.reader(io.StringIO(text))
            headers = next(reader)
            self.assertEqual(len(headers), 13, f'{csv_path}: header has {len(headers)} cols')
            for i, row in enumerate(reader, 2):
                self.assertEqual(len(row), 13,
                            f'{csv_path} row {i}: {len(row)} cols: {row}')

    def test_all_csvs_have_required_columns(self):
        """All CSVs must have key columns: display-name, menu-code, action, skill."""
        for csv_path in _all_module_help_csvs():
            text = csv_path.read_text()
            reader = csv.DictReader(io.StringIO(text))
            for i, row in enumerate(reader, 2):
                self.assertIn('display-name', row, f'{csv_path} row {i}: missing display-name')
                self.assertIn('menu-code', row, f'{csv_path} row {i}: missing menu-code')
                self.assertIn('action', row, f'{csv_path} row {i}: missing action')
                self.assertIn('skill', row, f'{csv_path} row {i}: missing skill')


class TestC7TriggerPatternCoverage(unittest.TestCase):
    """C7: Verify comprehensive trigger_patterns coverage across all SKILL.md files."""

    def test_all_skill_md_files_have_trigger_patterns(self):
        """Every SKILL.md must have trigger_patterns in its YAML frontmatter."""
        failures = []
        for path in _all_skill_md_files():
            content = path.read_text()
            if 'trigger_patterns:' not in content:
                rel = path.relative_to(PROJECT)
                failures.append(str(rel))
        self.assertEqual(failures, [],
                    f'{len(failures)} SKILL.md files missing trigger_patterns: {failures}')

    def test_trigger_patterns_contain_slash_commands(self):
        """Every SKILL.md with trigger_patterns must have at least one slash command."""
        failures = []
        for path in _all_skill_md_files():
            content = path.read_text()
            if 'trigger_patterns:' not in content:
                continue
            lines = content.splitlines()
            in_triggers = False
            has_slash = False
            for line in lines:
                if 'trigger_patterns:' in line:
                    in_triggers = True
                    continue
                if in_triggers:
                    if line.strip().startswith('- /'):
                        has_slash = True
                        break
                    if not line.startswith(' '):
                        break
            if not has_slash:
                rel = path.relative_to(PROJECT)
                failures.append(str(rel))
        self.assertEqual(failures, [],
                    f'{len(failures)} SKILL.md files missing slash commands: {failures}')

    def test_skill_md_count(self):
        """Verify minimum expected number of SKILL.md files with trigger_patterns."""
        all_skills = _all_skill_md_files()
        self.assertGreaterEqual(len(all_skills), 50,
                    f'Expected at least 50 SKILL.md files, found {len(all_skills)}')


class TestC7RoutingExtensionHealth(unittest.TestCase):
    """C7: Verify routing extension is healthy after all Phase C changes."""

    def test_routing_ext_imports(self):
        """Routing extension must import cleanly."""
        ext_file = PROJECT / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'
        source = ext_file.read_text()
        self.assertIn('import csv', source)
        self.assertIn('import io', source)
        self.assertIn('import logging', source)
        self.assertIn('from pathlib import Path', source)

    def test_routing_ext_no_dual_read(self):
        """Routing extension must NOT have dual-read compatibility code."""
        ext_file = PROJECT / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'
        source = ext_file.read_text()
        self.assertNotIn('or row.get("name"', source)
        self.assertNotIn('or row.get("code"', source)
        self.assertNotIn('or row.get("agent-name"', source)

    def test_routing_ext_uses_new_columns(self):
        """Routing extension must use new 13-col column names directly."""
        ext_file = PROJECT / 'extensions' / 'python' / 'message_loop_prompts_after' / '_80_bmad_routing_manifest.py'
        source = ext_file.read_text()
        self.assertIn('row.get("display-name"', source)
        self.assertIn('row.get("menu-code"', source)


if __name__ == '__main__':
    unittest.main()
