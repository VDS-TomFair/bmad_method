"""BMAD Status Core — shared data functions (zero A0 framework imports).

Exported:
    SKILL_NAMES       list[str]   — canonical 5 module skill names
    REQUIRED_PROMPTS  set[str]    — agent prompt files that must exist
    read_state(state_file)  -> dict(phase, artifact, issues)
    check_agents(agents_dir) -> (healthy_list, broken_list)
    check_modules(skills_dir) -> (ok_list, broken_list)
    read_tests(test_dir)  -> (passed_str|None, total_str|None, mtime_str|None)
"""
import logging
import re
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

# Compiled regexes — MULTILINE for ^$ per-line, IGNORECASE for case-insensitive matching
_PHASE_RE = re.compile(r"^[-\s]*Phase:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
_ARTIFACT_RE = re.compile(r"^[-\s]*Active Artifact:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
_ISSUE_RE = re.compile(r"(ARCH-|DEFECT-)\d+.*PENDING", re.IGNORECASE)

SKILL_NAMES = ["bmad-init", "bmad-bmm", "bmad-bmb", "bmad-tea", "bmad-cis"]

REQUIRED_PROMPTS = {
    "agent.system.main.role.md",
    "agent.system.main.communication_additions.md",
}

AGENT_NAMES = {
    "bmad-master": "BMad Master",
    "bmad-analyst": "Mary (Analyst)",
    "bmad-pm": "John (PM)",
    "bmad-architect": "Winston (Architect)",
    "bmad-dev": "Amelia (Dev)",
    "bmad-qa": "Quinn (QA)",
    "bmad-sm": "Bob (SM)",
    "bmad-tech-writer": "Paige (Tech Writer)",
    "bmad-ux-designer": "Sally (UX)",
    "bmad-quick-dev": "Barry (Quick Dev)",
    "bmad-agent-builder": "Bond (Agent Builder)",
    "bmad-workflow-builder": "Wendy (Workflow Builder)",
    "bmad-module-builder": "Morgan (Module Builder)",
    "bmad-test-architect": "Murat (Test Architect)",
    "bmad-brainstorming-coach": "Carson (Brainstorming)",
    "bmad-problem-solver": "Dr. Quinn (Problem Solver)",
    "bmad-design-thinking": "Maya (Design Thinking)",
    "bmad-innovation": "Victor (Innovation)",
    "bmad-storyteller": "Sophia (Storyteller)",
    "bmad-presentation": "Caravaggio (Presentation)",
}

PHASE_ACTIONS = {
    "ready":           ("Start a new workflow", "Type LW to list workflows or describe what you want to build"),
    "1":               ("Continue Phase 1 Analysis", "Ask Mary (Analyst) to continue research or finalize product brief"),
    "2":               ("Continue Phase 2 Planning", "Ask John (PM) to continue PRD or Sally (UX) for UX design"),
    "3":               ("Continue Phase 3 Solutioning", "Ask Winston (Architect) to finalize the architecture document"),
    "4":               ("Continue Phase 4 Implementation", "Ask Bob (SM) for sprint planning or Amelia (Dev) for next story"),
    "not_initialized": ("Initialize BMAD", "Create or open a project in Agent Zero, then say: bmad init"),
    "unknown":         ("Initialize BMAD", "Create or open a project in Agent Zero, then say: bmad init"),
}


def read_state(state_file: Path):
    if not state_file.exists():
        return {"phase": "unknown", "artifact": "none", "issues": []}
    text = state_file.read_text(encoding="utf-8")
    phase_match    = _PHASE_RE.search(text)
    artifact_match = _ARTIFACT_RE.search(text)
    issues   = [l.strip().lstrip("-# ") for l in text.splitlines()
                if _ISSUE_RE.search(l)]
    return {
        "phase":    phase_match.group(1).strip().lower()    if phase_match    else "unknown",
        "artifact": artifact_match.group(1).strip() if artifact_match else "none",
        "issues":   issues
    }


def check_agents(agents_dir: Path):
    healthy, broken = [], []
    if not agents_dir.exists():
        return healthy, broken
    for d in agents_dir.iterdir():
        if not d.is_dir() or not d.name.startswith("bmad-"): continue
        prompts = d / "prompts"
        if not prompts.exists():
            broken.append((d.name, ["prompts/ missing"])); continue
        missing = REQUIRED_PROMPTS - {f.name for f in prompts.iterdir()}
        if missing:
            broken.append((d.name, sorted(missing)))
        else:
            healthy.append(d.name)
    return healthy, broken


def check_modules(skills_dir: Path):
    ok, broken = [], []
    for n in SKILL_NAMES:
        (ok if (skills_dir / n / "module.yaml").exists() else broken).append(n)
    return ok, broken


def read_tests(test_dir: Path):
    if not test_dir.exists(): return None, None, None
    reports = sorted(test_dir.glob("behavioral-test-report*.md"),
                     key=lambda p: p.stat().st_mtime, reverse=True)
    if not reports: return None, None, None
    latest  = reports[0]
    mtime   = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    text    = latest.read_text(encoding="utf-8")
    matches = re.findall(r"(\d+)\s+of\s+(\d+)[^\n]*PASS", text)
    if not matches:
        m_pass = re.search(r"PASS:\s*(\d+)", text)
        m_partial = re.search(r"PARTIAL:\s*(\d+)", text)
        m_fail = re.search(r"FAIL:\s*(\d+)", text)
        if m_pass:
            passed = int(m_pass.group(1))
            partial = int(m_partial.group(1)) if m_partial else 0
            failed = int(m_fail.group(1)) if m_fail else 0
            total = passed + partial + failed
            matches = [(str(passed), str(total))]
    if matches:
        best = max(matches, key=lambda x: int(x[0]))
        return best[0], best[1], mtime
    return None, None, mtime
