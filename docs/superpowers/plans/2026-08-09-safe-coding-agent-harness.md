# Safe Coding Agent Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a testable Python CLI Coding Agent Harness with deterministic governance and feedback mechanisms.

**Architecture:** A project-owned loop coordinates an injectable LLM client, tool registry, guardrail, feedback validator, and JSON memory. Tests use a scripted LLM and never call a network provider.

**Tech Stack:** Python 3.10+, standard library, pytest for tests, setuptools for wheel packaging, GitHub Actions and GitLab CI configuration.

## Global Constraints

- The harness core must not delegate its agent loop to LangChain, AutoGen, CrewAI, LlamaIndex, or a coding-agent SDK runner.
- Dangerous-action interception and feedback must be deterministic code, not prompt-only instructions.
- Mock-LLM tests must run without network access or real credentials.
- No API key may be committed, logged, or hard-coded.

---

### Task 1: Establish the domain contracts

**Files:**
- Create: `src/agent_harness/models.py`
- Create: `src/agent_harness/llm.py`
- Test: `tests/test_harness.py`

- [x] Write a test for parsing a JSON `tool` action and a scripted LLM returning ordered actions.
- [x] Run the focused test and observe the missing contract failure.
- [x] Implement `Action`, `ToolResult`, `Feedback`, `RunResult`, `action_from_json`, and `ScriptedLLM`.
- [x] Run the focused test and verify it passes.

### Task 2: Add tools and deterministic governance

**Files:**
- Create: `src/agent_harness/tools.py`
- Create: `src/agent_harness/guardrails.py`
- Test: `tests/test_harness.py`

- [x] Write a test asserting `rm -rf` is rejected before execution.
- [x] Run the test and observe the missing guardrail failure.
- [x] Implement the workspace boundary and dangerous-command check.
- [x] Run the focused test and verify it passes.
- [x] Add the explicit approval callback path and keep the default deny behavior.

### Task 3: Close the feedback loop

**Files:**
- Create: `src/agent_harness/feedback.py`
- Create: `src/agent_harness/memory.py`
- Create: `src/agent_harness/loop.py`
- Test: `tests/test_harness.py`

- [x] Write a test with a failing command, a safe corrective action, and a final action.
- [x] Run the test and observe the missing loop behavior.
- [x] Implement result-to-feedback conversion, memory recording, max-step stopping, and action dispatch.
- [x] Run all tests and verify the failure is fed back before the corrective action.

### Task 4: Add distribution and demonstration surfaces

**Files:**
- Create: `src/agent_harness/cli.py`
- Create: `demo/mechanism_demo.py`
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `.github/workflows/ci.yml`
- Create: `.gitlab-ci.yml`

- [x] Add a deterministic demo sequence: dangerous action, safe correction, final result.
- [x] Run the demo and verify the exact three-stage trace.
- [x] Add wheel metadata, install commands, security boundaries, and known limitations.
- [ ] Build a wheel and install it in a clean environment.

### Task 5: Complete process evidence and repository validation

**Files:**
- Modify: `SPEC.md`
- Modify: `PLAN.md`
- Modify: `SPEC_PROCESS.md`
- Modify: `AGENT_LOG.md`
- Create: `REFLECTION_TEMPLATE.md`

- [ ] Record the confirmed design, actual test commands, failures, fixes, and commits without inventing conversations.
- [ ] Run the full test command from the final tree with a writable temporary directory.
- [ ] Run the mechanism demo from the final tree.
- [ ] Review every required deliverable against the course checklist.
- [ ] Initialize Git, create multiple focused commits, and record commit hashes.
