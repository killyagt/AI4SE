from __future__ import annotations

from pathlib import Path

from .feedback import FeedbackValidator
from .guardrails import Guardrail
from .llm import LLMClient
from .memory import Memory
from .models import Action, RunResult
from .tools import ToolRegistry


class AgentLoop:
    def __init__(self, llm: LLMClient, workspace: Path, memory: Memory | None = None, max_steps: int = 8, approval=None):
        self.llm = llm
        self.tools = ToolRegistry(workspace)
        self.guardrail = Guardrail(workspace, approval=approval)
        self.feedback = FeedbackValidator()
        self.memory = memory or Memory()
        self.max_steps = max_steps

    def run(self, goal: str) -> RunResult:
        messages = [{"role": "system", "content": "Return one JSON action. Use tools only when needed."}, {"role": "user", "content": goal}]
        steps = []
        for index in range(1, self.max_steps + 1):
            action = self.llm.complete(messages, self.tools.schemas())
            if action.kind in {"final", "stop"}:
                return RunResult("completed" if action.kind == "final" else "stopped", action.message, steps)
            policy = self.guardrail.check(action)
            if not policy.ok:
                steps.append({"step": index, "action": action.name, "status": "blocked", "feedback": policy.error})
                self.memory.add("blocked_action", policy.error)
                messages.append({"role": "tool", "content": policy.error})
                continue
            result = self.tools.execute(action)
            feedback = self.feedback.validate(result)
            steps.append({"step": index, "action": action.name, "status": "ok" if feedback.ok else "failed", "feedback": feedback.summary})
            self.memory.add("tool_feedback", feedback.summary + ": " + feedback.details)
            messages.append({"role": "tool", "content": feedback.summary + "\n" + feedback.details})
        return RunResult("max_steps", "maximum step count reached", steps)
