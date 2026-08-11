from __future__ import annotations

import shlex
from pathlib import Path

from .models import Action, ToolResult


class Guardrail:
    """Deterministic policy layer between an LLM decision and execution."""

    blocked_tokens = {"rm", "rmdir", "del", "format", "shutdown", "reboot", "mkfs", "remove-item", "clear-content"}

    def __init__(self, workspace: Path, approval=None, blocked_commands=None):
        self.workspace = workspace.resolve()
        self.approval = approval or (lambda _action: False)
        self.blocked_commands = set(blocked_commands or self.blocked_tokens)

    def check(self, action: Action) -> ToolResult:
        if action.kind != "tool":
            return ToolResult(True, "allowed")
        if action.name == "run_command":
            command = str(action.arguments.get("command", ""))
            try:
                tokens = {Path(x).name.lower() for x in shlex.split(command)}
            except ValueError as exc:
                return ToolResult(False, "", f"invalid command: {exc}")
            if tokens & self.blocked_commands:
                if self.approval(action):
                    return ToolResult(True, "allowed after human approval")
                return ToolResult(False, "", "blocked dangerous command; human approval required")
        if action.name in {"write_file", "read_file"}:
            target = (self.workspace / str(action.arguments.get("path", ""))).resolve()
            if self.workspace not in target.parents and target != self.workspace:
                return ToolResult(False, "", "path escapes workspace")
            filename = target.name.lower()
            if action.name == "read_file" and (
                filename == ".env"
                or filename.startswith(".env.")
                or filename in {"credentials", "secrets"}
            ):
                return ToolResult(False, "", "blocked sensitive file")
        return ToolResult(True, "allowed")
