from __future__ import annotations

import argparse
from pathlib import Path

from .llm import ScriptedLLM
from .loop import AgentLoop
from .models import Action


def demo() -> int:
    # Keep the demo workspace beside the source tree so it is easy to remove.
    root = Path.cwd().parent / ".agent-harness-demo"
    llm = ScriptedLLM([
        Action("tool", "run_command", {"command": "rm -rf demo.txt"}),
        Action("tool", "write_file", {"path": "demo.txt", "content": "feedback loop recovered"}),
        Action("final", message="demo completed after a guarded failure"),
    ])
    result = AgentLoop(llm, root).run("Create a demo file safely")
    print(result.message)
    for step in result.steps:
        print(step)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe Coding Agent Harness")
    parser.add_argument("command", choices=["demo"], help="run the deterministic mechanism demo")
    args = parser.parse_args()
    return demo() if args.command == "demo" else 1


if __name__ == "__main__":
    raise SystemExit(main())
