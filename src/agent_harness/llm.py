from __future__ import annotations

import json
import os
import urllib.request
from collections.abc import Iterable
from typing import Any, Protocol

from .models import Action


class LLMClient(Protocol):
    def complete(self, messages: list[dict[str, str]], tools: list[dict[str, Any]]) -> Action: ...


def action_from_json(payload: str | dict[str, Any]) -> Action:
    data = json.loads(payload) if isinstance(payload, str) else payload
    kind = data.get("kind")
    if kind == "tool":
        return Action("tool", data["name"], data.get("arguments", {}))
    if kind == "final":
        return Action("final", message=data.get("message", ""))
    if kind == "stop":
        return Action("stop", message=data.get("message", ""))
    raise ValueError("LLM action must have kind tool, final, or stop")


class ScriptedLLM:
    """Deterministic LLM substitute used by tests and the mechanism demo."""

    def __init__(self, actions: Iterable[Action]):
        self._actions = iter(actions)
        self.calls: list[list[dict[str, str]]] = []

    def complete(self, messages: list[dict[str, str]], tools: list[dict[str, Any]]) -> Action:
        self.calls.append(messages)
        try:
            return next(self._actions)
        except StopIteration as exc:
            raise RuntimeError("scripted LLM ran out of actions") from exc


class OpenAICompatibleLLM:
    """Optional single-call adapter; the harness loop remains local code."""

    def __init__(self, endpoint: str, model: str, api_key: str | None = None):
        self.endpoint = endpoint
        self.model = model
        self.api_key = api_key or os.environ.get("AGENT_HARNESS_API_KEY")

    def complete(self, messages: list[dict[str, str]], tools: list[dict[str, Any]]) -> Action:
        if not self.api_key:
            raise RuntimeError("missing API key; use the OS credential manager or AGENT_HARNESS_API_KEY")
        body = json.dumps({"model": self.model, "messages": messages, "tools": tools}).encode()
        request = urllib.request.Request(self.endpoint, data=body, headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode())
        content = payload["choices"][0]["message"]["content"]
        return action_from_json(content)
