from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Task:
    """A task tracked by TaskFlow."""

    id: str
    title: str
    status: str
    due_date: Optional[date] = None
