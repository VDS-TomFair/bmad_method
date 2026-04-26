import unittest
from pathlib import Path

API_FILE = Path(__file__).resolve().parents[1] / 'api' / '_bmad_status.py'


class TestD5RecommendCaching(unittest.TestCase):
    """D5: _recommend() must accept pre-computed data to avoid double I/O."""

    def test_recommend_accepts_precomputed_params(self):
        """_recommend signature must accept state, agents, skills, tests params."""
        source = API_FILE.read_text()
        # Must have def _recommend with dict params
        self.assertIn('def _recommend(self, state: dict, agents: dict, skills: dict, tests: dict)', source,
                    '_recommend does not accept pre-computed state/agents/skills/tests params')

    def test_recommend_does_not_call_internal_methods(self):
        """_recommend must NOT call _read_state, _check_agents, _check_skills, _read_tests internally."""
        source = API_FILE.read_text()
        lines = source.splitlines()
        in_recommend = False
        recommend_body = []
        for line in lines:
            if 'def _recommend' in line:
                in_recommend = True
                continue
            if in_recommend:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                    break
                if line.startswith('    def ') and 'def _recommend' not in line:
                    break
                recommend_body.append(line)
        body = '\n'.join(recommend_body)
        self.assertNotIn('self._read_state(', body,
                    '_recommend still calls self._read_state() — should use pre-computed param')
        self.assertNotIn('self._check_agents(', body,
                    '_recommend still calls self._check_agents() — should use pre-computed param')
        self.assertNotIn('self._check_skills(', body,
                    '_recommend still calls self._check_skills() — should use pre-computed param')
        self.assertNotIn('self._read_tests(', body,
                    '_recommend still calls self._read_tests() — should use pre-computed param')

    def test_process_passes_precomputed_data(self):
        """process() must pass already-computed state/agents/skills/tests to _recommend."""
        source = API_FILE.read_text()
        self.assertIn('self._recommend(state, agents, skills, tests)', source,
                    'process() does not pass pre-computed data to _recommend')


if __name__ == '__main__':
    unittest.main()
