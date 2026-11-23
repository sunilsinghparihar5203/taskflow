from dataclasses import dataclass
from datetime import date
from typing import Literal, Optional


TaskState = Literal["todo", "in_progress", "done"]
_TASK_STATES = ("todo", "in_progress", "done")


@dataclass
class Task:
    """A task tracked by TaskFlow."""

    id: str
    title: str
    state: TaskState
    due_date: Optional[date] = None

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("title must not be empty")
        if self.state not in _TASK_STATES:
            raise ValueError(f"unsupported task state: {self.state!r}")

    def change_state(self, state: TaskState) -> None:
        """Change the task state, rejecting unsupported values at runtime."""
        if state not in _TASK_STATES:
            raise ValueError(f"unsupported task state: {state!r}")
        self.state = state
