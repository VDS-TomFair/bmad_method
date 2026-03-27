from helpers.api import ApiHandler, Request, Response
import re, json, base64, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime
from usr.plugins.bmad_method.helpers.bmad_status_core import (
    check_agents, check_modules, read_state, read_tests, SKILL_NAMES
)

# --- Plugin-level paths (fixed, plugin-relative) ---
# Path(__file__).resolve() follows symlinks to the real file location.
_PLUGIN_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR   = _PLUGIN_ROOT / "agents"
SKILLS_DIR   = _PLUGIN_ROOT / "skills"

# --- Project-level paths (per-request, resolved from active chat context) ---
def _resolve_project_root(ctxid: str | None) -> Path | None:
    """Find the BMAD project root for the currently active chat context.

    Resolution order:
    1. Active context → project name → project folder (correct A0-aware method)
    2. Dev/symlink fallback: walk up from plugin dir looking for .a0proj
    3. Production fallback: scan /a0/usr/projects/ for most-recently-modified BMAD state
    """
    # Stage 1: resolve from active A0 context (the right way)
    if ctxid:
        try:
            from agent import AgentContext
            from helpers import projects
            context = AgentContext.get(ctxid)
            if context:
                project_name = projects.get_context_project_name(context)
                if project_name:
                    folder = Path(projects.get_project_folder(project_name))
                    if (folder / ".a0proj").exists():
                        return folder
                    else:
                        return None  # project exists but no bmad init — show not_initialized
        except Exception:
            pass  # fall through to fallbacks

    # Stage 2: dev/symlink mode — .a0proj is an ancestor of the real file location
    for parent in [_PLUGIN_ROOT, *_PLUGIN_ROOT.parents]:
        if (parent / ".a0proj").exists():
            return parent

    # Stage 3: production fallback — scan user projects for most-recently-modified BMAD state
    projects_dir = Path("/a0/usr/projects")
    if projects_dir.exists():
        candidates = []
        for proj in projects_dir.iterdir():
            if not proj.is_dir():
                continue
            state = proj / ".a0proj/instructions/02-bmad-state.md"
            if state.exists():
                candidates.append((state.stat().st_mtime, proj))
        if candidates:
            candidates.sort(reverse=True)
            return candidates[0][1]

    return None  # no BMAD project found


AGENT_NAMES = {
    "bmad-master":"BMad Master","bmad-analyst":"Mary (Analyst)",
    "bmad-pm":"John (PM)","bmad-architect":"Winston (Architect)",
    "bmad-dev":"Amelia (Dev)","bmad-qa":"Quinn (QA)",
    "bmad-sm":"Bob (SM)","bmad-tech-writer":"Paige (Tech Writer)",
    "bmad-ux-designer":"Sally (UX)","bmad-quick-dev":"Barry (Quick Dev)",
    "bmad-agent-builder":"Bond (Agent Builder)",
    "bmad-workflow-builder":"Wendy (Workflow Builder)",
    "bmad-module-builder":"Morgan (Module Builder)",
    "bmad-test-architect":"Murat (Test Architect)",
    "bmad-brainstorming-coach":"Carson (Brainstorming)",
    "bmad-problem-solver":"Dr. Quinn (Problem Solver)",
    "bmad-design-thinking":"Maya (Design Thinking)",
    "bmad-innovation":"Victor (Innovation)",
    "bmad-storyteller":"Sophia (Storyteller)",
    "bmad-presentation":"Caravaggio (Presentation)",
}
PHASE_ACTIONS = {
    "ready":           ("Start a new workflow","Type LW to list workflows or describe what you want to build"),
    "1":               ("Continue Phase 1 Analysis","Ask Mary (Analyst) to continue research or finalize product brief"),
    "2":               ("Continue Phase 2 Planning","Ask John (PM) to continue PRD or Sally (UX) for UX design"),
    "3":               ("Continue Phase 3 Solutioning","Ask Winston (Architect) to finalize the architecture document"),
    "4":               ("Continue Phase 4 Implementation","Ask Bob (SM) for sprint planning or Amelia (Dev) for next story"),
    "not_initialized": ("Initialize BMAD","Create or open a project in Agent Zero, then say: bmad init"),
    "unknown":         ("Initialize BMAD","Create or open a project in Agent Zero, then say: bmad init"),
}


class BmadStatus(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            # Resolve project root for THIS chat context
            ctxid = input.get("ctxid") or input.get("context_id")
            project_root = _resolve_project_root(ctxid)
            state_file   = (project_root / ".a0proj/instructions/02-bmad-state.md") if project_root else None
            test_dir     = (project_root / ".a0proj/_bmad-output/test-artifacts")    if project_root else None

            return {
                "success":        True,
                "generated":      datetime.now().strftime("%Y-%m-%d %H:%M"),
                "project":        str(project_root) if project_root else None,
                "state":          self._read_state(state_file),
                "agents":         self._check_agents(),
                "skills":         self._check_skills(),
                "tests":          self._read_tests(test_dir),
                "recommendation": self._recommend(state_file, test_dir),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_state(self, state_file: Path | None):
        if state_file is None or not state_file.exists():
            return {"phase": "not_initialized", "artifact": "none", "issues": []}
        return read_state(state_file)

    def _check_agents(self):
        healthy_names, broken_tuples = check_agents(AGENTS_DIR)
        healthy = [{"name": n, "display": AGENT_NAMES.get(n, n)} for n in healthy_names]
        broken  = [{"name": n, "display": AGENT_NAMES.get(n, n), "missing": mf}
                   for n, mf in broken_tuples]
        return {"healthy": healthy, "broken": broken, "total": len(healthy) + len(broken)}

    def _check_skills(self):
        ok, broken = check_modules(SKILLS_DIR)
        return {"ok": ok, "broken": broken, "total": len(SKILL_NAMES)}

    def _read_tests(self, test_dir: Path | None):
        if test_dir is None or not test_dir.exists():
            return {"status": "no_dir"}
        passed, total, mtime = read_tests(test_dir)
        if passed is None and mtime is None:
            return {"status": "no_report"}
        if passed is None:
            return {"status": "no_match", "verified": mtime}
        return {"status": "ok", "passed": int(passed), "total": int(total), "verified": mtime,
                "failing": int(total) - int(passed)}

    def _recommend(self, state_file: Path | None, test_dir: Path | None):
        state  = self._read_state(state_file)
        agents = self._check_agents()
        skills = self._check_skills()
        tests  = self._read_tests(test_dir)
        issues = []
        if skills["broken"]:
            issues.append({"sev":"blocker","what":str(len(skills["broken"]))+" module(s) missing",
                "fix":"Verify BMAD plugin is installed and enabled"})
        if agents["broken"]:
            issues.append({"sev":"warn","what":str(len(agents["broken"]))+" agent(s) unhealthy",
                "fix":"Restore missing prompt files - see Agent Health section"})
        if tests.get("failing",0) > 0:
            issues.append({"sev":"warn","what":str(tests["failing"])+" test(s) failing",
                "fix":"Review test-artifacts/behavioral-test-report*.md"})
        if state["issues"]:
            issues.append({"sev":"open","what":str(len(state["issues"]))+" open ARCH/DEFECT item(s)",
                "fix":"Address in next sprint"})
        phase     = state["phase"].lower()
        phase_key = "ready"
        for k in PHASE_ACTIONS:
            if k not in ("ready","unknown","not_initialized") and k in phase:
                phase_key = k
                break
        if phase in ("unknown","not_initialized"):
            phase_key = "not_initialized"
        label, action = PHASE_ACTIONS[phase_key]
        return {"issues":issues,"label":label,"action":action}
