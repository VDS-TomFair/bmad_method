import unittest
import csv
import io
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT / 'skills' / 'bmad-init' / '_config' / 'agent-manifest.csv'
WORKFLOW = PROJECT / 'skills' / 'bmad-init' / 'core' / 'workflows' / 'party-mode' / 'workflow.md'
STEP1 = PROJECT / 'skills' / 'bmad-init' / 'core' / 'workflows' / 'party-mode' / 'steps' / 'step-01-agent-loading.md'
STEP2 = PROJECT / 'skills' / 'bmad-init' / 'core' / 'workflows' / 'party-mode' / 'steps' / 'step-02-discussion-orchestration.md'
STEP3 = PROJECT / 'skills' / 'bmad-init' / 'core' / 'workflows' / 'party-mode' / 'steps' / 'step-03-graceful-exit.md'


def _parse_manifest():
    text = MANIFEST.read_text()
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


def _all_workflow_text():
    parts = [
        WORKFLOW.read_text(),
        STEP1.read_text(),
        STEP2.read_text(),
        STEP3.read_text(),
    ]
    return '\n'.join(parts)


class TestD8PartyModeAC(unittest.TestCase):
    """D8: Party mode must satisfy all 8 acceptance criteria."""

    # AC-PM-01: On activation, load agent-manifest.csv, display roster with icon + name + one-liner
    def test_ac01_manifest_has_required_fields(self):
        """Manifest CSV must have name, displayName, icon, communicationStyle columns."""
        rows = _parse_manifest()
        self.assertGreater(len(rows), 0)
        for row in rows:
            self.assertIn('name', row, f"Missing 'name' column")
            self.assertIn('displayName', row, f"Missing 'displayName' column")
            self.assertIn('icon', row, f"Missing 'icon' column")
            self.assertIn('communicationStyle', row, f"Missing 'communicationStyle' column")

    def test_ac01_workflow_displays_roster(self):
        """Workflow must instruct to display roster with icon, name, and one-liner."""
        text = _all_workflow_text()
        self.assertIn('icon', text.lower())
        self.assertIn('displayName', text)
        self.assertIn('roster', text.lower())

    # AC-PM-02: Select 2-4 relevant agents based on content analysis
    def test_ac02_selects_2_to_4_agents(self):
        """Workflow must instruct selecting 2-4 relevant agents."""
        text = _all_workflow_text()
        self.assertTrue(
            '2-3' in text or '2-4' in text or '2 to 4' in text,
            'Workflow must specify selecting 2-4 agents'
        )

    # AC-PM-03: Each agent response strictly from communicationStyle CSV field
    def test_ac03_communication_style_enforced(self):
        """Workflow must enforce communicationStyle as the sole voice source."""
        text = _all_workflow_text()
        self.assertIn('communicationStyle', text)
        # Must have persona guard against blending
        self.assertTrue(
            'PERSONA GUARD' in text or 'no blending' in text.lower() or 'strictly' in text.lower(),
            'Workflow must guard against blended voices'
        )

    # AC-PM-04: Each agent response prefixed with {icon} **{displayName}:**
    def test_ac04_response_format_with_icon_and_name(self):
        """Workflow must specify response format: icon + bold displayName."""
        text = _all_workflow_text()
        self.assertIn('[Icon Emoji]', text)
        self.assertIn('[Agent Name]', text)

    # AC-PM-05: Support user directing named agent
    def test_ac05_named_agent_direction(self):
        """Workflow must support user addressing agents by name."""
        text = _all_workflow_text()
        self.assertTrue(
            'specific agent' in text.lower() or 'addresses specific' in text.lower() or 'by name' in text.lower(),
            'Workflow must handle user directing specific agents by name'
        )

    # AC-PM-06: Graceful exit on *exit, goodbye, end party
    def test_ac06_exit_triggers(self):
        """Workflow must define exit triggers and graceful exit."""
        text = _all_workflow_text()
        self.assertIn('*exit', text)
        self.assertIn('goodbye', text.lower())
        self.assertIn('end party', text.lower())
        # Must have graceful exit step
        self.assertTrue(STEP3.exists(), 'Missing graceful exit step file')

    # AC-PM-07: Rotate agent participation
    def test_ac07_rotation_enforced(self):
        """Workflow must enforce agent rotation to prevent domination."""
        text = _all_workflow_text()
        self.assertTrue(
            'rotate' in text.lower() or 'rotation' in text.lower(),
            'Workflow must specify agent rotation'
        )

    # AC-PM-08: communication_language from config respected
    def test_ac08_communication_language_respected(self):
        """Workflow must reference {communication_language} from config."""
        text = _all_workflow_text()
        self.assertIn('{communication_language}', text,
                    'Workflow must reference {communication_language}')

    # Known divergence: no parallel subagent spawning, no --model flag
    def test_known_divergence_no_parallel_spawning(self):
        """Party mode must document known divergence: no parallel subagent spawning."""
        text = _all_workflow_text()
        # Should NOT reference parallel spawning or subagent calls
        self.assertNotIn('call_subordinate', text,
                    'Party mode should not use call_subordinate (solo implementation)')


class TestD8ManifestData(unittest.TestCase):
    """Additional manifest data quality checks."""

    def test_manifest_has_multiple_agents(self):
        """Manifest must have at least 5 agents for meaningful party mode."""
        rows = _parse_manifest()
        self.assertGreaterEqual(len(rows), 5)

    def test_manifest_agents_have_icons(self):
        """All agents must have non-empty icons."""
        rows = _parse_manifest()
        for row in rows:
            self.assertTrue(row.get('icon', '').strip(),
                        f"Agent {row.get('name', '?')} has empty icon")

    def test_manifest_agents_have_display_names(self):
        """All agents must have non-empty displayNames."""
        rows = _parse_manifest()
        for row in rows:
            self.assertTrue(row.get('displayName', '').strip(),
                        f"Agent {row.get('name', '?')} has empty displayName")


if __name__ == '__main__':
    unittest.main()
