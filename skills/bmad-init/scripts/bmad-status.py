#!/usr/bin/env python3
"""BMAD Framework Status Dashboard v0.5 - Dynamic path resolution + WHAT/WHY/NEXT."""
import argparse, re, sys, json, os, logging
from datetime import datetime
from pathlib import Path
import importlib.util as _ilu

log = logging.getLogger(__name__)

# Load shared state parser from helpers/ — single source of truth
_core_path = str(Path(__file__).resolve().parents[3] / "helpers" / "bmad_status_core.py")
_spec = _ilu.spec_from_file_location("bmad_status_core", _core_path)
if _spec is None:
    print(f"ERROR: Cannot load bmad_status_core from {_core_path}", file=sys.stderr)
    sys.exit(1)
_core_mod = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_core_mod)
read_state    = _core_mod.read_state
check_agents  = _core_mod.check_agents
check_modules = _core_mod.check_modules
read_tests    = _core_mod.read_tests
SKILL_NAMES   = _core_mod.SKILL_NAMES
AGENT_NAMES   = _core_mod.AGENT_NAMES
PHASE_ACTIONS = _core_mod.PHASE_ACTIONS
# All paths are resolved at runtime from CLI args or self-discovery.
# No hardcoded absolute paths.

def _resolve_plugin_root(base_path_arg: str | None) -> Path:
    """Resolve the BMAD plugin root directory."""
    if base_path_arg:
        return Path(base_path_arg).resolve()
    # Fallback: this script is at <plugin_root>/skills/bmad-init/scripts/bmad-status.py
    return Path(__file__).resolve().parents[3]

def _resolve_project_root(project_path_arg: str | None) -> Path | None:
    """Resolve the active BMAD project root."""
    if project_path_arg:
        p = Path(project_path_arg).resolve()
        if (p / ".a0proj").exists():
            return p
        return None

    # Dev-only fallback: scan /a0/usr/projects/ for most-recently-modified BMAD state
    # Gated behind BMAD_DEV_MODE env var — not for production use
    if os.environ.get("BMAD_DEV_MODE"):
        projects_dir = Path("/a0/usr/projects")
        if projects_dir.exists():
            candidates = []
            for proj in projects_dir.iterdir():
                if not proj.is_dir():
                    continue
                state = proj / ".a0proj" / "instructions" / "02-bmad-state.md"
                if state.exists():
                    candidates.append((state.stat().st_mtime, proj))
            if candidates:
                candidates.sort(reverse=True)
                log.warning("BMAD_DEV_MODE: using cross-project mtime fallback → %s", candidates[0][1])
                return candidates[0][1]
    return None


DIV          = "\u2501" * 45



def wwn(what, why, nxt, indent="   "):
    """Print WHAT / WHY / NEXT diagnostic block."""
    print(indent + "WHAT: " + what)
    print(indent + "WHY:  " + why)
    print(indent + "NEXT: " + nxt)


def recommend_next(state, broken_agents, broken_skills, passed, total_t, agents_dir):
    issues = []
    if broken_skills:
        issues.append(("\U0001f534 BLOCKER",
            str(len(broken_skills)) + " module(s) missing",
            "Verify BMAD plugin is installed and enabled"))
    if broken_agents:
        issues.append(("\U0001f7e1 WARN",
            str(len(broken_agents)) + " agent(s) unhealthy",
            "Restore missing prompt files in " + str(agents_dir)))
    if passed and total_t and int(passed) < int(total_t):
        failed = int(total_t) - int(passed)
        issues.append(("\U0001f7e1 WARN",
            str(failed) + " behavioral test(s) failing",
            "Review test-artifacts/behavioral-test-report*.md"))
    if state["issues"]:
        issues.append(("\u26a0\ufe0f  OPEN",
            str(len(state["issues"])) + " open ARCH/DEFECT item(s)",
            "Address in next sprint - see items listed above"))
    phase     = state["phase"].lower()
    phase_key = "ready"
    for k in PHASE_ACTIONS:
        if k not in ("ready","unknown") and k in phase:
            phase_key = k
            break
    if phase == "unknown":
        phase_key = "unknown"
    label, action = PHASE_ACTIONS[phase_key]
    return issues, label, action


def main():
    NOW = datetime.now().strftime("%Y-%m-%d %H:%M")
    parser = argparse.ArgumentParser(description="BMAD Framework Status Dashboard")
    parser.add_argument("--base-path", help="BMAD plugin root directory")
    parser.add_argument("--project-path", help="Active BMAD project root directory")
    args = parser.parse_args()

    plugin_root  = _resolve_plugin_root(args.base_path)
    project_root = _resolve_project_root(args.project_path)

    agents_dir = plugin_root / "agents"
    skills_dir = plugin_root / "skills"
    test_dir   = project_root / ".a0proj/_bmad-output/test-artifacts" if project_root else Path("/nonexistent")
    state_file = project_root / ".a0proj/instructions/02-bmad-state.md" if project_root else Path("/nonexistent")

    print("\n\U0001f9d9 BMAD Framework Status")
    print(DIV)
    print("Generated: " + NOW + " (live)")
    if project_root:
        print("Project:   " + project_root.name)

    # DS-01 State
    state = read_state(state_file)
    print("\n\U0001f4cd Phase:     " + state["phase"])
    print("\U0001f4c4 Artifact:  " + state["artifact"])
    if state["issues"]:
        print()
        for i in state["issues"]:
            print("\u26a0\ufe0f  " + i)
    else:
        print("\n\u2705 No open architecture items")

    # DS-02 Agents
    healthy, broken = check_agents(agents_dir)
    total = len(healthy) + len(broken)
    print()
    if broken:
        print("\U0001f916 Agents:   " + str(len(healthy)) + "/" + str(total) + " healthy  (+ 5 Party Mode archetypes)")
        for name, missing_files in broken:
            display = AGENT_NAMES.get(name, name)
            print("   \U0001f534 " + display)
            wwn(
                str(len(missing_files)) + " required prompt file(s) missing",
                "Agent cannot be activated without all required prompt files",
                "Restore in " + str(agents_dir / name / "prompts") + ": " + ", ".join(missing_files)
            )
    else:
        print("\U0001f916 Agents:   " + str(total) + "/" + str(total) + " healthy  (+ 5 Party Mode archetypes)")

    # DS-03 Skills
    ok_s, broken_s = check_modules(skills_dir)
    if broken_s:
        print("\U0001f5c2\ufe0f Modules:  " + str(len(ok_s)) + "/" + str(len(SKILL_NAMES)) + " OK")
        for s in broken_s:
            print("   \U0001f534 " + s)
            wwn(
                s + "/module-help.csv not found",
                "Skill not accessible \u2014 workflow routing will fail",
                "Verify BMAD plugin is installed at " + str(skills_dir)
            )
    else:
        print("\U0001f5c2\ufe0f Modules:  " + str(len(ok_s)) + "/" + str(len(SKILL_NAMES)) + " OK")

    # DS-04 Tests
    passed, total_t, mtime = read_tests(test_dir)
    if passed:
        p, t = int(passed), int(total_t)
        if p < t:
            print("\U0001f9ea Tests:    " + str(p) + " of " + str(t) + " PASS \u2014 " + str(t - p) + " FAILING  (last run: " + str(mtime) + ")")
            wwn(
                str(t - p) + " behavioral check(s) failing",
                "Framework regression detected",
                "Review test-artifacts/behavioral-test-report*.md for failing IDs"
            )
        else:
            print("\U0001f9ea Tests:    " + passed + " of " + total_t + " checks PASS  (verified: " + str(mtime) + ")")
    else:
        print("\U0001f9ea Tests:    no test report found")
        wwn(
            "No behavioral test report exists",
            "Tests not yet run or report in wrong location",
            "Run test suite and save to test-artifacts/"
        )


    # v0.5 Next-Action Recommendation Engine
    issues, label, action = recommend_next(state, broken, broken_s, passed, total_t, agents_dir)
    print("\n" + DIV)
    if issues:
        print("\U0001f527 Issues requiring attention:")
        for sev, what, fix in issues:
            print("   " + sev + ": " + what)
            print("            \u2192 " + fix)
        print()
    print("\u26a1 Recommended next action: " + label)
    print("   \u2192 " + action)
    print("\n" + DIV)
    print()


if __name__ == "__main__":
    main()
