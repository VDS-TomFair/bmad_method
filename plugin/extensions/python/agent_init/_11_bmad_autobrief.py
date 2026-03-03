import asyncio
import json
from python.helpers.extension import Extension


class BmadAutoBrief(Extension):
    """
    Auto-brief extension for bmad-master.
    Runs bmad-status.py and prepends its output to the initial greeting.
    Only fires for agent 0 with bmad-master profile, and only on fresh sessions.
    """

    async def execute(self, **kwargs):
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

        # Run STATUS script (async to avoid blocking event loop during agent_init)
        try:
            proc = await asyncio.create_subprocess_exec(
                "python", "/a0/skills/bmad-init/scripts/bmad-status.py",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            try:
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
                status_output = stdout.decode().strip()
            except asyncio.TimeoutError:
                proc.kill()
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
