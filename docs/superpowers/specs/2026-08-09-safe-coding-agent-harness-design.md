# Safe Coding Agent Harness Design

## Goal

Build a small Python CLI Coding Agent Harness that turns an LLM's proposed actions into a controlled, testable execution loop for local coding tasks.

## Architecture

The harness owns the control loop: it sends the goal and prior tool feedback to an injected `LLMClient`, receives a structured `Action`, checks policy, dispatches a tool, converts the result into deterministic feedback, persists a compact memory record, and repeats until final output, explicit stop, or a step limit.

The LLM is deliberately replaceable. `ScriptedLLM` provides deterministic offline behavior for unit tests and the mechanism demo. An optional OpenAI-compatible single-call adapter demonstrates that the agent loop remains project-owned rather than delegated to an orchestration framework.

## Components

- `models.py`: immutable action, tool result, feedback, and run result values.
- `llm.py`: injectable client protocol, JSON action parsing, mock client, optional provider adapter.
- `tools.py`: file read/write and command execution registry.
- `guardrails.py`: workspace boundary and dangerous-command policy before execution.
- `feedback.py`: deterministic conversion of tool outcomes into loop feedback.
- `memory.py`: append-only JSON memory for feedback and blocked actions.
- `loop.py`: the project-owned Thought/Action/Observation-style control loop.
- `cli.py` and `demo/mechanism_demo.py`: reproducible CLI entry points.

## Safety and governance

The default policy blocks deletion, formatting, shutdown/reboot, and workspace-escaping file operations. The loop records the block and continues with a safe feedback message. A caller may inject an explicit approval callback; only an approved action proceeds. This is a minimal governance layer, not a complete OS sandbox.

## Feedback and main contribution

The main contribution is the governance plus feedback closed loop. A failed command is converted to a structured failure observation; the next LLM action can change because the observation is appended to its message history. Unit tests remove the real LLM and assert the behavior with a scripted action sequence.

## Testing and distribution

Tests cover dangerous-action interception, failure-feedback-driven next-action change, and safe completion. The demo deterministically shows a blocked dangerous command followed by a safe file write and final completion. The project is distributed as a Python wheel and a Git Release artifact; the demo requires no network or key.

## Deliberate non-goals

No WebUI, multi-agent scheduler, vector database, hosted service, or full OS sandbox is included in the deadline build. These would increase surface area without improving the required core mechanism evidence.
