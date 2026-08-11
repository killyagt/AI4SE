from dataclasses import dataclass, field
from typing import Any, Literal


ActionKind = Literal["tool", "final", "stop"]


@dataclass(frozen=True)
class Action:
    kind: ActionKind
    name: str = ""
    arguments: dict[str, Any] = field(default_factory=dict)
    message: str = ""


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    output: str
    error: str = ""


@dataclass(frozen=True)
class Feedback:
    ok: bool
    summary: str
    details: str = ""


@dataclass
class RunResult:
    status: str
    message: str
    steps: list[dict[str, Any]] = field(default_factory=list)
