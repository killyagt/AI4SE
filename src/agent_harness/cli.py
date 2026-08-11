from __future__ import annotations

import argparse
from pathlib import Path

from .llm import ScriptedLLM
from .config import HarnessConfig
from .loop import AgentLoop
from .models import Action


def demo(config_path: str | None = None) -> int:
    # Keep the demo workspace in the user's current working directory.
    root = Path.cwd() / ".agent-harness-demo"
    llm = ScriptedLLM([
        Action("tool", "run_command", {"command": "rm -rf demo.txt"}),
        Action("tool", "write_file", {"path": "demo.txt", "content": "feedback loop recovered"}),
        Action("final", message="demo completed after a guarded failure"),
    ])
    config = HarnessConfig.from_json(Path(config_path)) if config_path else None
    result = AgentLoop(llm, root, config=config).run("Create a demo file safely")
    print(result.message)
    for step in result.steps:
        print(step)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Safe Coding Agent Harness")
    parser.add_argument("command", choices=["demo"], help="run the deterministic mechanism demo")
    parser.add_argument("--config", help="optional JSON harness configuration")
    args = parser.parse_args()
    return demo(args.config) if args.command == "demo" else 1


if __name__ == "__main__":
    raise SystemExit(main())
