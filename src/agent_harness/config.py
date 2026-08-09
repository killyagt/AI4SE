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
        return cls(max_steps=int(data.get("max_steps", 8)), blocked_commands=frozenset(data.get("blocked_commands", [])))
