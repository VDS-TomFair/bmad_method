from python.helpers.api import ApiHandler, Request, Response
import re, json, base64, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

# --- Self-aware path resolution ---
# Works in both dev (symlink) and production (direct copy) modes.
# Path(__file__).resolve() follows symlinks to the real file location.
_PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# Walk up from plugin root to find the project root (.a0proj marker)
def _find_project_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / ".a0proj").exists():
            return parent
    return start  # fallback to plugin root

PROJECT_ROOT = _find_project_root(_PLUGIN_ROOT)
STATE_FILE   = PROJECT_ROOT / ".a0proj/instructions/02-bmad-state.md"
AGENTS_DIR   = _PLUGIN_ROOT / "agents"
SKILLS_DIR   = _PLUGIN_ROOT / "skills"
TEST_DIR     = PROJECT_ROOT / ".a0proj/_bmad-output/test-artifacts"
SKILL_NAMES  = ["bmad-init","bmad-bmm","bmad-bmb","bmad-tea","bmad-cis"]

# Langfuse config: check user plugins first, then builtin (A0 priority order)
def _find_langfuse_cfg() -> Path:
    from python.helpers import plugins
    for root in plugins.get_plugin_roots("langfuse-observability"):
        cfg = Path(root) / "config.json"
        if cfg.exists():
            return cfg
    return Path("/a0/plugins/langfuse-observability/config.json")  # fallback

LANGFUSE_CFG = _find_langfuse_cfg()

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
REQUIRED_PROMPTS = {"agent.system.main.role.md","agent.system.main.communication_additions.md"}
PHASE_ACTIONS = {
    "ready":   ("Start a new workflow","Type LW to list workflows or describe what you want to build"),
    "1":       ("Continue Phase 1 Analysis","Ask Mary (Analyst) to continue research or finalize product brief"),
    "2":       ("Continue Phase 2 Planning","Ask John (PM) to continue PRD or Sally (UX) for UX design"),
    "3":       ("Continue Phase 3 Solutioning","Ask Winston (Architect) to finalize the architecture document"),
    "4":       ("Continue Phase 4 Implementation","Ask Bob (SM) for sprint planning or Amelia (Dev) for next story"),
    "unknown": ("Initialize BMAD","Run: bmad init"),
}


class BmadStatus(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        try:
            return {
                "success": True,
                "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "state":    self._read_state(),
                "agents":   self._check_agents(),
                "skills":   self._check_skills(),
                "tests":    self._read_tests(),
                "langfuse": self._fetch_langfuse(),
                "recommendation": self._recommend(),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _read_state(self):
        if not STATE_FILE.exists():
            return {"phase":"unknown","artifact":"none","issues":[]}
        text = STATE_FILE.read_text(encoding="utf-8")
        phase    = re.search(r"Phase:\s*(.+)", text)
        artifact = re.search(r"Active Artifact:\s*(.+)", text)
        issues   = [l.strip().lstrip("-# ") for l in text.splitlines()
                    if re.search(r"(ARCH-|DEFECT-)\d+", l) and "PENDING" in l]
        return {
            "phase":    phase.group(1).strip()    if phase    else "unknown",
            "artifact": artifact.group(1).strip() if artifact else "none",
            "issues":   issues,
        }

    def _check_agents(self):
        healthy, broken = [], []
        if not AGENTS_DIR.exists(): return {"healthy":[]  ,"broken":[]}
        for d in AGENTS_DIR.iterdir():
            if not d.is_dir() or not d.name.startswith("bmad-"): continue
            prompts = d / "prompts"
            if not prompts.exists():
                broken.append({"name":d.name,"display":AGENT_NAMES.get(d.name,d.name),"missing":["prompts/ missing"]})
                continue
            missing = REQUIRED_PROMPTS - {f.name for f in prompts.iterdir()}
            if missing:
                broken.append({"name":d.name,"display":AGENT_NAMES.get(d.name,d.name),"missing":sorted(missing)})
            else:
                healthy.append({"name":d.name,"display":AGENT_NAMES.get(d.name,d.name)})
        return {"healthy":healthy,"broken":broken,"total":len(healthy)+len(broken)}

    def _check_skills(self):
        ok, broken = [], []
        for n in SKILL_NAMES:
            (ok if (SKILLS_DIR/n/"SKILL.md").exists() else broken).append(n)
        return {"ok":ok,"broken":broken,"total":len(SKILL_NAMES)}

    def _read_tests(self):
        if not TEST_DIR.exists(): return {"status":"no_dir"}
        reports = sorted(TEST_DIR.glob("behavioral-test-report*.md"),
                         key=lambda p:p.stat().st_mtime, reverse=True)
        if not reports: return {"status":"no_report"}
        latest  = reports[0]
        mtime   = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        text    = latest.read_text(encoding="utf-8")
        matches = re.findall(r"(\d+)\s+of\s+(\d+)[^\n]*PASS", text)
        if matches:
            best = max(matches, key=lambda x:int(x[0]))
            return {"status":"ok","passed":int(best[0]),"total":int(best[1]),"verified":mtime,
                    "failing":int(best[1])-int(best[0])}
        return {"status":"no_match","verified":mtime}

    def _fetch_langfuse(self):
        if not LANGFUSE_CFG.exists(): return {"status":"unavailable"}
        try:
            cfg = json.loads(LANGFUSE_CFG.read_text())
            if not (cfg.get("langfuse_enabled") and cfg.get("langfuse_public_key") and cfg.get("langfuse_secret_key")):
                return {"status":"disabled"}
        except Exception: return {"status":"config_error"}
        try:
            host  = cfg.get("langfuse_host","https://cloud.langfuse.com").rstrip("/")
            token = base64.b64encode((cfg["langfuse_public_key"]+":"+cfg["langfuse_secret_key"]).encode()).decode()
            hdrs  = {"Authorization":"Basic "+token,"Content-Type":"application/json"}
            req   = urllib.request.Request(host+"/api/public/traces?limit=50&page=1",headers=hdrs)
            with urllib.request.urlopen(req,timeout=5) as r:
                data   = json.loads(r.read())
                traces = data.get("data",[])
                hits   = {}
                for t in traces:
                    for k in AGENT_NAMES:
                        if k in t.get("name","").lower(): hits[k]=hits.get(k,0)+1
                top = sorted(hits.items(),key=lambda x:x[1],reverse=True)[:3]
                return {
                    "status":      "connected",
                    "host":        cfg.get("langfuse_host",""),
                    "trace_count": data.get("meta",{}).get("totalItems",len(traces)),
                    "last_trace":  traces[0].get("timestamp","")[:16].replace("T"," ") if traces else None,
                    "top_agents":  [{"name":AGENT_NAMES.get(a,a),"count":c} for a,c in top],
                }
        except Exception as e:
            return {"status":"error","error":str(e)}

    def _recommend(self):
        state   = self._read_state()
        agents  = self._check_agents()
        skills  = self._check_skills()
        tests   = self._read_tests()
        issues  = []
        if skills["broken"]:
            issues.append({"sev":"blocker","what":str(len(skills["broken"]))+" skill(s) missing",
                "fix":"ln -sf /a0/usr/projects/a0_bmad_method/skills/bmad-* /a0/skills/"})
        if agents["broken"]:
            issues.append({"sev":"warn","what":str(len(agents["broken"]))+" agent(s) unhealthy",
                "fix":"Restore missing prompt files - see Agent Health section"})
        if tests.get("failing",0)>0:
            issues.append({"sev":"warn","what":str(tests["failing"])+" test(s) failing",
                "fix":"Review test-artifacts/behavioral-test-report*.md"})
        if state["issues"]:
            issues.append({"sev":"open","what":str(len(state["issues"]))+" open ARCH/DEFECT item(s)",
                "fix":"Address in next sprint"})
        phase = state["phase"].lower()
        phase_key = "ready"
        for k in PHASE_ACTIONS:
            if k not in ("ready","unknown") and k in phase: phase_key=k; break
        if phase=="unknown": phase_key="unknown"
        label, action = PHASE_ACTIONS[phase_key]
        return {"issues":issues,"label":label,"action":action}
