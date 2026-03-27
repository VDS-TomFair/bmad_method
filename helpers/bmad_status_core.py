"""BMAD Status Core — shared data functions (zero A0 framework imports).

Exported:
    SKILL_NAMES       list[str]   — canonical 5 module skill names
    REQUIRED_PROMPTS  set[str]    — agent prompt files that must exist
    read_state(state_file)  -> dict(phase, artifact, issues)
    check_agents(agents_dir) -> (healthy_list, broken_list)
    check_modules(skills_dir) -> (ok_list, broken_list)
    read_tests(test_dir)  -> (passed_str|None, total_str|None, mtime_str|None)
"""
import re
from datetime import datetime
from pathlib import Path

SKILL_NAMES = ["bmad-init", "bmad-bmm", "bmad-bmb", "bmad-tea", "bmad-cis"]

REQUIRED_PROMPTS = {
    "agent.system.main.role.md",
    "agent.system.main.communication_additions.md",
}


def read_state(state_file: Path):
    if not state_file.exists():
        return {"phase": "unknown", "artifact": "none", "issues": []}
    text = state_file.read_text(encoding="utf-8")
    phase    = re.search(r"Phase:\s*(.+)", text)
    artifact = re.search(r"Active Artifact:\s*(.+)", text)
    issues   = [l.strip().lstrip("-# ") for l in text.splitlines()
                if re.search(r"(ARCH-|DEFECT-)\d+", l) and "PENDING" in l]
    return {
        "phase":    phase.group(1).strip()    if phase    else "unknown",
        "artifact": artifact.group(1).strip() if artifact else "none",
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
        (ok if (skills_dir / n / "module-help.csv").exists() else broken).append(n)
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
        import re as _re
        m_pass = _re.search(r"PASS:\s*(\d+)", text)
        m_partial = _re.search(r"PARTIAL:\s*(\d+)", text)
        m_fail = _re.search(r"FAIL:\s*(\d+)", text)
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
