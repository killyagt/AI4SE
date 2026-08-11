from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class HarnessConfig:
    max_steps: int = 8
    blocked_commands: frozenset[str] = field(default_factory=lambda: frozenset({"rm", "rmdir", "del", "format", "shutdown", "reboot", "mkfs", "remove-item", "clear-content"}))

    @classmethod
    def from_json(cls, path: Path) -> "HarnessConfig":
        data = json.loads(path.read_text(encoding="utf-8"))
        defaults = cls()
        commands = data.get("blocked_commands")
        return cls(max_steps=int(data.get("max_steps", defaults.max_steps)), blocked_commands=defaults.blocked_commands if commands is None else frozenset(commands))
