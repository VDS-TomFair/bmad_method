import json
import subprocess
from pathlib import Path
from helpers.extension import Extension

# Dynamic path resolution — works regardless of install method
_PLUGIN_ROOT = Path(__file__).resolve().parents[3]
_STATUS_SCRIPT = _PLUGIN_ROOT / "skills" / "bmad-init" / "scripts" / "bmad-status.py"


def _resolve_project_path(agent) -> str | None:
    """Resolve the active project path from agent context."""
    try:
        from helpers import projects
        project_name = projects.get_context_project_name(agent.context)
        if project_name:
            folder = Path(projects.get_project_folder(project_name))
            if (folder / ".a0proj").exists():
                return str(folder)
    except Exception:
        pass

    # Fallback: scan /a0/usr/projects/ for most-recently-modified BMAD state
    try:
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
                return str(candidates[0][1])
    except Exception:
        pass

    return None


class BmadAutoBrief(Extension):
    """
    Auto-brief extension for bmad-master.
    Runs bmad-status.py and prepends its output to the initial greeting.
    Only fires for agent 0 with bmad-master profile, and only on fresh sessions.
    """

    def execute(self, **kwargs):
        # Only for main agent (not subordinates)
        if self.agent.number != 0:
            return

        # Only for bmad-master profile
        profile = getattr(self.agent.config, "profile", None) or ""
        if "bmad-master" not in str(profile):
            return

        # Only on fresh sessions (no existing logs)
        if self.agent.context.log.logs:
            return

        # Verify status script exists
        if not _STATUS_SCRIPT.exists():
            return

        # Build command args
        cmd_args = ["python", str(_STATUS_SCRIPT), "--base-path", str(_PLUGIN_ROOT)]
        project_path = _resolve_project_path(self.agent)
        if project_path:
            cmd_args.extend(["--project-path", project_path])

        # Run STATUS script synchronously
        try:
            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                timeout=10
            )
            status_output = result.stdout.strip()
        except subprocess.TimeoutExpired:
            status_output = "⚠️ Status unavailable: timeout"
        except Exception as e:
            status_output = f"⚠️ Status unavailable: {e}"

        if not status_output:
            return

        # Read existing initial message and inject status
        try:
            initial_msg_raw = self.agent.read_prompt("fw.initial_message.md")
            initial_msg_json = json.loads(initial_msg_raw)
            existing_text = initial_msg_json.get("tool_args", {}).get("text", "")

            # Prepend status block
            status_block = f"## 📊 Project Status\n\n~~~\n{status_output}\n~~~\n\n---\n\n"
            initial_msg_json["tool_args"]["text"] = status_block + existing_text

            updated_msg = json.dumps(initial_msg_json)
        except Exception:
            updated_msg = json.dumps({
                "thoughts": ["Showing BMAD project status brief"],
                "headline": "BMAD Status Brief",
                "tool_name": "response",
                "tool_args": {"text": f"## 📊 Project Status\n\n~~~\n{status_output}\n~~~"}
            })

        # Inject directly as a separate log entry before the greeting
        from agent import LoopData
        self.agent.loop_data = LoopData(user_message=None)
        self.agent.context.log.log(
            type="response",
            content=f"## 📊 Project Status\n\n```\n{status_output}\n```",
            finished=True,
            update_progress="none",
        )
