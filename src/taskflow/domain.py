from dataclasses import dataclass
from datetime import date
from typing import Literal, Optional, cast


TaskState = Literal["todo", "in_progress", "done"]
_TASK_STATES: tuple[TaskState, ...] = ("todo", "in_progress", "done")


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


def summarize_tasks_by_status(tasks: list[Task]) -> dict[TaskState, int]:
    """Count tasks in each supported state, including states with no tasks."""
    counts = {state: 0 for state in _TASK_STATES}
    for task in tasks:
        counts[task.state] += 1
    return counts


def parse_task(data: dict[str, object]) -> Task:
    """Create a Task from a dictionary, validating required and optional values."""
    for field in ("id", "title", "status"):
        if field not in data:
            raise ValueError(f"missing required field: {field}")

    task_id = data["id"]
    title = data["title"]
    status = data["status"]

    if not isinstance(task_id, str):
        raise ValueError("id must be a string")
    if not isinstance(title, str):
        raise ValueError("title must be a string")
    if not isinstance(status, str):
        raise ValueError("status must be a string")
    if not title.strip():
        raise ValueError("title must not be empty")
    if status not in _TASK_STATES:
        raise ValueError(f"unsupported task status: {status!r}")

    due_date = None
    raw_due_date = data.get("due_date")
    if raw_due_date is not None:
        if not isinstance(raw_due_date, str):
            raise ValueError("due_date must be a string in YYYY-MM-DD format")
        try:
            due_date = date.fromisoformat(raw_due_date)
        except ValueError as exc:
            raise ValueError(
                "due_date must be a valid date in YYYY-MM-DD format"
            ) from exc

    return Task(
        id=task_id,
        title=title,
        state=cast(TaskState, status),
        due_date=due_date,
    )
