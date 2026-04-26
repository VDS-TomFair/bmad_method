import csv
import io
import unittest
from pathlib import Path

CORE_CSV = Path(__file__).resolve().parents[1] / 'skills' / 'bmad-init' / 'core' / 'module-help.csv'
ROOT_CSV = Path(__file__).resolve().parents[1] / 'skills' / 'bmad-init' / 'module-help.csv'

NEW_HEADER = ['module', 'skill', 'display-name', 'menu-code', 'description', 'action', 'args', 'phase', 'after', 'before', 'required', 'output-location', 'outputs']


class TestC0CoreCSVSchema(unittest.TestCase):
    """C0: bmad-init/core/module-help.csv must use upstream 13-col schema."""

    def test_core_csv_has_new_header(self):
        """Header must be the 13-col upstream schema."""
        text = CORE_CSV.read_text()
        header_line = text.splitlines()[0].strip()
        expected = ','.join(NEW_HEADER)
        self.assertEqual(header_line, expected,
                     f'Header mismatch:\n  got:      {header_line}\n  expected: {expected}')

    def test_core_csv_has_exactly_13_columns(self):
        """Every data row must have exactly 13 fields."""
        text = CORE_CSV.read_text()
        reader = csv.reader(io.StringIO(text))
        headers = next(reader)
        self.assertEqual(len(headers), 13, f'Header has {len(headers)} columns, expected 13')
        for i, row in enumerate(reader, 2):
            self.assertEqual(len(row), 13, f'Row {i} has {len(row)} columns, expected 13: {row}')

    def test_core_csv_no_old_column_names(self):
        """Must NOT contain old-schema column names as standalone columns."""
        text = CORE_CSV.read_text()
        header_cols = [c.strip() for c in text.splitlines()[0].split(',')]
        old_cols = ['name', 'code', 'sequence', 'workflow-file', 'command', 'options']
        for col in old_cols:
            self.assertNotIn(col, header_cols,
                         f'Old column name "{col}" found in header: {header_cols}')

    def test_core_csv_same_row_count_as_root(self):
        """Core CSV should have same number of data rows as root module-help.csv entries for core module."""
        core_text = CORE_CSV.read_text()
        root_text = ROOT_CSV.read_text()
        core_rows = list(csv.reader(io.StringIO(core_text)))[1:]  # skip header
        root_rows = list(csv.reader(io.StringIO(root_text)))[1:]
        # Filter root rows to core module only
        core_root_rows = [r for r in root_rows if r and r[0] == 'core']
        core_data_rows = [r for r in core_rows if r and r[0]]
        self.assertEqual(len(core_data_rows), len(core_root_rows),
                     f'Core CSV has {len(core_data_rows)} rows, root has {len(core_root_rows)} core rows')

    def test_core_csv_readable_as_new_schema(self):
        """All rows must parse with DictReader using new schema fieldnames."""
        text = CORE_CSV.read_text()
        reader = csv.DictReader(io.StringIO(text))
        for i, row in enumerate(reader, 2):
            self.assertIn('display-name', row, f'Row {i} missing display-name')
            self.assertIn('menu-code', row, f'Row {i} missing menu-code')
            self.assertIn('action', row, f'Row {i} missing action')
            self.assertIn('args', row, f'Row {i} missing args')


if __name__ == '__main__':
    unittest.main()
