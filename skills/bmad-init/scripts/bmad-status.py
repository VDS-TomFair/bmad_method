#!/usr/bin/env python3
"""BMAD Framework Status Dashboard v0.4 - WHAT/WHY/NEXT + Recommendation Engine."""
import re, sys, json, urllib.request, urllib.error, base64
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path("/a0/usr/projects/a0_bmad_method")
STATE_FILE   = PROJECT_ROOT / ".a0proj/instructions/02-bmad-state.md"
AGENTS_DIR   = Path("/a0/agents")
SKILLS_DIR   = Path("/a0/skills")
TEST_DIR     = PROJECT_ROOT / ".a0proj/_bmad-output/test-artifacts"
LANGFUSE_CFG = Path("/a0/plugins/langfuse-observability/config.json")
SKILL_NAMES  = ["bmad-init","bmad-bmm","bmad-bmb","bmad-tea","bmad-cis"]
NOW          = datetime.now().strftime("%Y-%m-%d %H:%M")
DIV          = "\u2501" * 45

AGENT_NAMES = {
    "bmad-master":              "BMad Master",
    "bmad-analyst":             "Mary (Analyst)",
    "bmad-pm":                  "John (PM)",
    "bmad-architect":           "Winston (Architect)",
    "bmad-dev":                 "Amelia (Dev)",
    "bmad-qa":                  "Quinn (QA)",
    "bmad-sm":                  "Bob (Scrum Master)",
    "bmad-tech-writer":         "Paige (Tech Writer)",
    "bmad-ux-designer":         "Sally (UX)",
    "bmad-quick-dev":           "Barry (Quick Dev)",
    "bmad-agent-builder":       "Bond (Agent Builder)",
    "bmad-workflow-builder":    "Wendy (Workflow Builder)",
    "bmad-module-builder":      "Morgan (Module Builder)",
    "bmad-test-architect":      "Murat (Test Architect)",
    "bmad-brainstorming-coach": "Carson (Brainstorming)",
    "bmad-problem-solver":      "Dr. Quinn (Problem Solver)",
    "bmad-design-thinking":     "Maya (Design Thinking)",
    "bmad-innovation":          "Victor (Innovation)",
    "bmad-storyteller":         "Sophia (Storyteller)",
    "bmad-presentation":        "Caravaggio (Presentation)",
}

REQUIRED_PROMPTS = {
    "agent.system.main.role.md",
    "agent.system.main.communication_additions.md",
}

PHASE_ACTIONS = {
    "ready":   ("Start a new workflow",
                "Type LW to list workflows, or describe what you want to build"),
    "1":       ("Continue Phase 1 Analysis",
                "Ask Mary (Analyst) to continue research or finalize product brief"),
    "2":       ("Continue Phase 2 Planning",
                "Ask John (PM) to continue PRD, or Sally (UX) for UX design"),
    "3":       ("Continue Phase 3 Solutioning",
                "Ask Winston (Architect) to finalize the architecture document"),
    "4":       ("Continue Phase 4 Implementation",
                "Ask Bob (SM) for sprint planning or Amelia (Dev) for next story"),
    "unknown": ("Initialize BMAD", "Run: bmad init"),
}

def read_state():
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
        "issues":   issues
    }

def check_agents():
    healthy, broken = [], []
    for d in AGENTS_DIR.iterdir():
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

def check_skills():
    ok, broken = [], []
    for n in SKILL_NAMES:
        (ok if (SKILLS_DIR / n / "SKILL.md").exists() else broken).append(n)
    return ok, broken

def read_tests():
    if not TEST_DIR.exists(): return None, None, None
    reports = sorted(TEST_DIR.glob("behavioral-test-report*.md"),
                     key=lambda p: p.stat().st_mtime, reverse=True)
    if not reports: return None, None, None
    latest  = reports[0]
    mtime   = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    text    = latest.read_text(encoding="utf-8")
    matches = re.findall(r"(\d+)\s+of\s+(\d+)[^\n]*PASS", text)
    if matches:
        best = max(matches, key=lambda x: int(x[0]))
        return best[0], best[1], mtime
    return None, None, mtime

def read_langfuse_config():
    if not LANGFUSE_CFG.exists(): return None
    try:
        cfg = json.loads(LANGFUSE_CFG.read_text())
        if cfg.get("langfuse_enabled") and cfg.get("langfuse_public_key") and cfg.get("langfuse_secret_key"):
            return cfg
    except Exception: pass
    return None

def fetch_langfuse(cfg):
    host  = cfg.get("langfuse_host","https://cloud.langfuse.com").rstrip("/")
    pub   = cfg["langfuse_public_key"]
    sec   = cfg["langfuse_secret_key"]
    token = base64.b64encode((pub + ":" + sec).encode()).decode()
    hdrs  = {"Authorization": "Basic " + token, "Content-Type": "application/json"}
    result = {}
    try:
        req = urllib.request.Request(host + "/api/public/traces?limit=50&page=1", headers=hdrs)
        with urllib.request.urlopen(req, timeout=5) as r:
            data   = json.loads(r.read())
            traces = data.get("data",[])
            result["trace_count"] = data.get("meta",{}).get("totalItems", len(traces))
            hits = {}
            for t in traces:
                for k in AGENT_NAMES:
                    if k in t.get("name","").lower():
                        hits[k] = hits.get(k,0) + 1
            if hits:
                top = sorted(hits.items(), key=lambda x: x[1], reverse=True)[:3]
                result["top_agents"] = [(AGENT_NAMES.get(a,a), c) for a,c in top]
            if traces:
                result["last_trace"] = traces[0].get("timestamp","")[:16].replace("T"," ")
    except Exception as e:
        result["error"] = str(e)
    return result


def wwn(what, why, nxt, indent="   "):
    """Print WHAT / WHY / NEXT diagnostic block."""
    print(indent + "WHAT: " + what)
    print(indent + "WHY:  " + why)
    print(indent + "NEXT: " + nxt)


def recommend_next(state, broken_agents, broken_skills, passed, total_t):
    issues = []
    if broken_skills:
        issues.append(("\U0001f534 BLOCKER",
            str(len(broken_skills)) + " skill(s) missing",
            "ln -sf /a0/usr/projects/a0_bmad_method/skills/bmad-* /a0/skills/"))
    if broken_agents:
        issues.append(("\U0001f7e1 WARN",
            str(len(broken_agents)) + " agent(s) unhealthy",
            "Restore missing prompt files - see agent detail above"))
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
    print("\n\U0001f9d9 BMAD Framework Status")
    print(DIV)
    print("Generated: " + NOW + " (live)")

    # DS-01 State
    state = read_state()
    print("\n\U0001f4cd Phase:     " + state["phase"])
    print("\U0001f4c4 Artifact:  " + state["artifact"])
    if state["issues"]:
        print()
        for i in state["issues"]:
            print("\u26a0\ufe0f  " + i)
    else:
        print("\n\u2705 No open architecture items")

    # DS-02 Agents
    healthy, broken = check_agents()
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
                "Restore in /a0/agents/" + name + "/prompts/: " + ", ".join(missing_files)
            )
    else:
        print("\U0001f916 Agents:   " + str(total) + "/" + str(total) + " healthy  (+ 5 Party Mode archetypes)")

    # DS-03 Skills
    ok_s, broken_s = check_skills()
    if broken_s:
        print("\U0001f50c Skills:   " + str(len(ok_s)) + "/" + str(len(SKILL_NAMES)) + " OK")
        for s in broken_s:
            print("   \U0001f534 " + s)
            wwn(
                s + "/SKILL.md not found",
                "Skill symlink broken — workflow routing will fail",
                "ln -sf /a0/usr/projects/a0_bmad_method/skills/" + s + " /a0/skills/" + s
            )
    else:
        print("\U0001f50c Skills:   " + str(len(ok_s)) + "/" + str(len(SKILL_NAMES)) + " symlinks OK")

    # DS-04 Tests
    passed, total_t, mtime = read_tests()
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

    # DS-05 Langfuse
    cfg = read_langfuse_config()
    if cfg:
        print()
        lf = fetch_langfuse(cfg)
        if "error" in lf and not lf.get("trace_count"):
            print("\U0001f4ca Langfuse: \u26a0\ufe0f  API error \u2014 " + lf["error"])
        else:
            print("\U0001f4ca Langfuse: \u2705 connected (" + cfg["langfuse_host"] + ")")
            if "trace_count" in lf:
                print("   Traces:    " + str(lf["trace_count"]) + " total")
            if "last_trace" in lf:
                print("   Last run:  " + lf["last_trace"])
            if "top_agents" in lf:
                print("   Top agents:")
                for n, c in lf["top_agents"]:
                    print("      " + n + ": " + str(c) + " traces")
    else:
        print("\n\U0001f4ca Langfuse: unavailable \u2014 plugin config not found or disabled")

    # v0.4 Next-Action Recommendation Engine
    issues, label, action = recommend_next(state, broken, broken_s, passed, total_t)
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
