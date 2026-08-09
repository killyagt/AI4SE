from pathlib import Path

from agent_harness.guardrails import Guardrail
from agent_harness.llm import ScriptedLLM
from agent_harness.loop import AgentLoop
from agent_harness.models import Action


def test_guardrail_blocks_dangerous_command(tmp_path: Path):
    result = Guardrail(tmp_path).check(Action("tool", "run_command", {"command": "rm -rf data"}))
    assert not result.ok
    assert "dangerous" in result.error


def test_guardrail_blocks_powershell_delete_command(tmp_path: Path):
    result = Guardrail(tmp_path).check(Action("tool", "run_command", {"command": "powershell Remove-Item important.txt"}))
    assert not result.ok
    assert "dangerous" in result.error


def test_feedback_is_returned_and_next_action_changes(tmp_path: Path):
    llm = ScriptedLLM([
        Action("tool", "run_command", {"command": "python -c \"raise SystemExit(1)\""}),
        Action("tool", "write_file", {"path": "fixed.txt", "content": "fixed"}),
        Action("final", message="fixed after feedback"),
    ])
    result = AgentLoop(llm, tmp_path).run("make the task succeed")
    assert result.status == "completed"
    assert (tmp_path / "fixed.txt").read_text() == "fixed"
    assert result.steps[0]["status"] == "failed"
    assert result.steps[1]["status"] == "ok"


def test_blocked_action_does_not_execute(tmp_path: Path):
    llm = ScriptedLLM([
        Action("tool", "run_command", {"command": "rm -rf should-not-exist"}),
        Action("final", message="stopped safely"),
    ])
    result = AgentLoop(llm, tmp_path).run("do not delete files")
    assert result.status == "completed"
    assert result.steps[0]["status"] == "blocked"
