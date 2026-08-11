from __future__ import annotations

from .models import Feedback, ToolResult


class FeedbackValidator:
    def validate(self, result: ToolResult) -> Feedback:
        if result.ok:
            return Feedback(True, "tool completed successfully", result.output)
        return Feedback(False, "tool failed; revise the next action", result.error or result.output)
