import unittest
from pathlib import Path
import hashlib

PROJECT = Path(__file__).resolve().parents[1]
AGENTS_DIR = PROJECT / 'agents'

SHARED_SECTIONS = [
    'A0 Variable Resolution',
    'BMAD Activation Protocol',
    'Initial Clarification',
    'Thinking Framework',
    'Using BMAD Skills',
    'Tool Calling',
    'File and Artifact Handling',
]


def _get_agents():
    return sorted([d.name for d in AGENTS_DIR.iterdir()
                   if d.is_dir() and d.name.startswith('bmad-') and d.name != '_shared'])


def _extract_section(content, section_name):
    marker = f'## {section_name}'
    if marker not in content:
        return None
    start = content.index(marker)
    rest = content[start + len(marker):]
    end = rest.find('\n## ')
    if end >= 0:
        return content[start:start + len(marker) + end]
    return content[start:]


class TestD2AuditSharedSections(unittest.TestCase):
    """D2: Audit confirms 6/7 sections identical, 'Using BMAD Skills' varies only in skills table."""

    def test_all_agents_have_specifics(self):
        """All 20 agents must have agent.system.main.specifics.md."""
        for agent in _get_agents():
            spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
            self.assertTrue(spec.exists(), f'{agent} missing specifics file')

    def test_master_lacks_full_shared_sections(self):
        """bmad-master is structurally different — no A0 Variable Resolution."""
        spec = AGENTS_DIR / 'bmad-master' / 'prompts' / 'agent.system.main.specifics.md'
        content = spec.read_text()
        self.assertNotIn('## A0 Variable Resolution', content,
                    'bmad-master should NOT have A0 Variable Resolution')

    def test_six_sections_identical_across_non_master(self):
        """6 sections (excluding Using BMAD Skills) must be identical across 19 non-master agents."""
        identical_sections = [s for s in SHARED_SECTIONS if s != 'Using BMAD Skills']
        agents = [a for a in _get_agents() if a != 'bmad-master']

        for section in identical_sections:
            hashes = set()
            for agent in agents:
                spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
                content = spec.read_text()
                extracted = _extract_section(content, section)
                self.assertIsNotNone(extracted, f'{agent} missing section: {section}')
                hashes.add(hashlib.md5(extracted.strip().encode()).hexdigest())
            self.assertEqual(len(hashes), 1,
                        f'Section "{section}" is not identical across agents: {len(hashes)} variants')

    def test_using_bmad_skills_protocol_identical(self):
        """The protocol part of 'Using BMAD Skills' (before skills table) is identical."""
        agents = [a for a in _get_agents() if a != 'bmad-master']
        hashes = set()
        for agent in agents:
            spec = AGENTS_DIR / agent / 'prompts' / 'agent.system.main.specifics.md'
            content = spec.read_text()
            section = _extract_section(content, 'Using BMAD Skills')
            # Strip the Available BMAD skills table
            if '**Available BMAD skills:**' in section:
                section = section[:section.index('**Available BMAD skills:**')]
            hashes.add(hashlib.md5(section.strip().encode()).hexdigest())
        self.assertEqual(len(hashes), 1,
                    'Using BMAD Skills protocol part varies across agents')


if __name__ == '__main__':
    unittest.main()
