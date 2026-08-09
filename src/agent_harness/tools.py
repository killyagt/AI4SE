from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Callable

from .models import Action, ToolResult


class ToolRegistry:
    def __init__(self, workspace: Path):
        self.workspace = workspace.resolve()
        self._tools: dict[str, Callable[..., ToolResult]] = {
            "read_file": self.read_file,
            "write_file": self.write_file,
            "run_command": self.run_command,
        }

    def schemas(self) -> list[dict[str, Any]]:
        return [{"name": name} for name in self._tools]

    def execute(self, action: Action) -> ToolResult:
        if action.name not in self._tools:
            return ToolResult(False, "", f"unknown tool: {action.name}")
        try:
            return self._tools[action.name](**action.arguments)
        except Exception as exc:  # tool failures become feedback, never process crashes
            return ToolResult(False, "", f"{type(exc).__name__}: {exc}")

    def read_file(self, path: str) -> ToolResult:
        return ToolResult(True, (self.workspace / path).read_text(encoding="utf-8"))

    def write_file(self, path: str, content: str) -> ToolResult:
        target = self.workspace / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return ToolResult(True, f"wrote {path}")

    def run_command(self, command: str, timeout: int = 20) -> ToolResult:
        completed = subprocess.run(command, cwd=self.workspace, shell=True, capture_output=True, text=True, timeout=timeout)
        output = (completed.stdout + completed.stderr).strip()
        return ToolResult(completed.returncode == 0, output, "" if completed.returncode == 0 else f"exit code {completed.returncode}")
