from __future__ import annotations

import json
from pathlib import Path


class Memory:
    def __init__(self, path: Path | None = None):
        self.path = path
        self.items: list[dict[str, str]] = []
        if path and path.exists():
            self.items = json.loads(path.read_text(encoding="utf-8"))

    def add(self, key: str, value: str) -> None:
        self.items.append({"key": key, "value": value})
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.items, ensure_ascii=False, indent=2), encoding="utf-8")

    def search(self, query: str) -> list[dict[str, str]]:
        words = set(query.lower().split())
        return [item for item in self.items if words & set(item["value"].lower().split())]
