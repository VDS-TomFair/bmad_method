import ast
import unittest
from pathlib import Path

API_FILE = Path(__file__).resolve().parents[1] / 'api' / '_bmad_status.py'


class TestNoDeadImportsApi(unittest.TestCase):
    """B8: Remove dead imports from api/_bmad_status.py."""

    def test_no_re_import(self):
        """'re' module is not used and should not be imported."""
        source = API_FILE.read_text()
        for line in source.splitlines():
            stripped = line.strip()
            if stripped == 'import re':
                self.fail('Found unused standalone import re')
            if stripped.startswith('import ') and ', ' in stripped:
                names = [n.strip() for n in stripped[len('import '):].split(',')]
                if 're' in names:
                    self.fail(f'Found unused import re in combined import: {stripped}')

    def test_no_json_import(self):
        """'json' module is not used and should not be imported."""
        source = API_FILE.read_text()
        for line in source.splitlines():
            stripped = line.strip()
            if stripped == 'import json':
                self.fail('Found unused standalone import json')
            if stripped.startswith('import ') and ', ' in stripped:
                names = [n.strip() for n in stripped[len('import '):].split(',')]
                if 'json' in names:
                    self.fail(f'Found unused import json in combined import: {stripped}')

    def test_no_duplicate_path_import(self):
        """'Path' should be imported once, not as both Path and _Path."""
        source = API_FILE.read_text()
        path_imports = [l.strip() for l in source.splitlines()
                        if l.strip().startswith('from pathlib')]
        self.assertLessEqual(len(path_imports), 1,
                         f'Multiple pathlib imports found: {path_imports}')

    def test_path_alias_is_path_not_underscore(self):
        """Path should be imported as Path, not _Path."""
        source = API_FILE.read_text()
        self.assertNotIn('Path as _Path', source,
                         'Duplicate Path import as _Path should be removed')


if __name__ == '__main__':
    unittest.main()
