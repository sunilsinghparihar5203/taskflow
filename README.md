# TaskFlow

TaskFlow is a small Python task management project.

Summarize tasks by their supported state with `summarize_tasks_by_status`:

```python
from taskflow.domain import Task, summarize_tasks_by_status

summarize_tasks_by_status([])
# {"todo": 0, "in_progress": 0, "done": 0}

tasks = [
    Task(id="task-1", title="Write tests", state="todo"),
    Task(id="task-2", title="Review changes", state="todo"),
    Task(id="task-3", title="Ship release", state="done"),
]
summarize_tasks_by_status(tasks)
# {"todo": 2, "in_progress": 0, "done": 1}
```

Zero-count states are included so consumers such as dashboards can render a
consistent set of statuses even when no task currently has a particular state.

Each task gets its own labels list by default:

```python
first = Task(id="task-4", title="Fix bug", state="todo")
second = Task(id="task-5", title="Update docs", state="todo")

first.labels.append("urgent")
print(first.labels)   # ["urgent"]
print(second.labels)  # []
```
